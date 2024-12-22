import mysql.connector
from typing import List, Dict
from datetime import datetime
import json
from decimal import Decimal

class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'connect_timeout': 10,
            'use_pure': True,  # 使用纯Python实现
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'auth_plugin': 'mysql_native_password',
            'raise_on_warnings': True,
            'connection_timeout': 10,
            'buffered': True
        }
        self.conn = None
        
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            print(f"尝试连接数据库: {self.config['host']}:{self.config['port']}")
            print(f"数据库名: {self.config['database']}")
            print(f"用户名: {self.config['user']}")
            
            # 先尝试不带数据库名连接
            test_config = self.config.copy()
            test_config.pop('database', None)  # 移除数据库名
            
            test_conn = mysql.connector.connect(**test_config)
            print("基础连接成功，检查数据库...")
            
            cursor = test_conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{self.config['database']}'")
            if not cursor.fetchone():
                print(f"数据库 {self.config['database']} 不存在，尝试创建...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                test_conn.commit()
                print("数据库创建成功")
                
            cursor.close()
            test_conn.close()
            
            # 尝试连接到指定数据库
            print("尝试连接到指定数据库...")
            full_conn = mysql.connector.connect(**self.config)
            print("数据库连接测试完全成功")
            full_conn.close()
            return True
            
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("用户名或密码错误")
                print("请检查用户名和密码是否正确")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("数据库不存在且无法创建")
                print("请检查用户权限")
            elif err.errno == mysql.connector.errorcode.CR_CONN_HOST_ERROR:
                print("无法连接到数据库服务器，请检查：")
                print("1. MySQL服务是否启动")
                print("2. 主机名是否正确")
                print("3. 端口是否正确")
                print("4. 防火墙设置")
            else:
                print(f"MySQL错误 [{err.errno}]: {err}")
            return False
        except Exception as e:
            print(f"连接异常: {str(e)}")
            print("请检查MySQL服务是否正常运行")
            return False
            
    def connect(self):
        """连接数据库"""
        try:
            if not self.conn or not self.conn.is_connected():
                self.conn = mysql.connector.connect(**self.config)
                self.conn.ping(reconnect=True, attempts=3, delay=5)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            raise
            
    def close(self):
        """关闭数据库连接"""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("数据库连接已关闭")
            
    def check_table_exists(self) -> bool:
        """检查数据表是否存在"""
        if not self.conn:
            self.connect()
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'retail_data'
            """, (self.config['database'],))
            
            result = cursor.fetchone()[0]
            exists = bool(result)
            if exists:
                print("数据表 retail_data 存在")
            else:
                print("数据表 retail_data 不存在")
            return exists
        except Exception as e:
            print(f"检查数据表失败: {str(e)}")
            return False
        finally:
            cursor.close()
            
    def get_retail_data(self) -> List[Dict]:
        """获取零售数据"""
        if not self.conn:
            self.connect()
            
        try:
            # 加载字段映射配置
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                mapping_config = config.get('table_mapping', {})
                table_name = mapping_config.get('table_name', 'retail_data')
                
                # 验证表名
                if not table_name or not table_name.replace('_', '').isalnum():
                    print(f"无效的表名: {table_name}，使用默认表名: retail_data")
                    table_name = 'retail_data'
                    
                field_mappings = mapping_config.get('fields', {})
                if not field_mappings:
                    raise ValueError("字段映射配置为空")
            
            cursor = self.conn.cursor(dictionary=True)
            
            # 验证表是否存在
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not cursor.fetchone():
                print(f"表 {table_name} 不存在，使用默认表名: retail_data")
                table_name = 'retail_data'
            
            # 动态构建SQL查询
            field_list = []
            for db_field, api_field in field_mappings.items():
                if db_field == 'report_date':
                    field_list.append(f"DATE_FORMAT({db_field}, '%Y-%m-%d') as {api_field}")
                else:
                    field_list.append(f"{db_field} as {api_field}")
                
            query = f"""
                SELECT 
                    CONCAT('YN', DATE_FORMAT(report_date, '%Y%m%d'), LPAD(id, 6, '0')) as itemId,
                    {', '.join(field_list)}
                FROM {table_name}
                WHERE report_date = CURDATE()
            """
            
            print(f"执行SQL查询: {query}")  # 添加日志
            cursor.execute(query)
            results = cursor.fetchall()
            
            # 处理数据类型
            processed_results = []
            for row in results:
                processed_row = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        processed_row[key] = value.strftime('%Y-%m-%d')
                    elif isinstance(value, Decimal):
                        processed_row[key] = float(value)
                    else:
                        processed_row[key] = value
                processed_results.append(processed_row)
            
            print(f"获取到 {len(processed_results)} 条数据")  # 添加日志
            return processed_results
            
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return []
        finally:
            cursor.close() 