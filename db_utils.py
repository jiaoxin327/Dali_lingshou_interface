import mysql.connector
from typing import List, Dict
from datetime import datetime

class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': 3306,
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
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT 
                    CONCAT('YN', DATE_FORMAT(report_date, '%Y%m%d'), LPAD(id, 6, '0')) as itemId,
                    social_credit_code as socialCreditCode,
                    comp_name as compName,
                    retail_store_code as retailStoreCode,
                    retail_store_name as retailStoreName,
                    report_date as reportDate,
                    commodity_code as selfCommondityCode,
                    commodity_name as selfCommondityName,
                    unit,
                    spec,
                    barcode,
                    data_type as dataType,
                    data_value as dataValue,
                    data_convert_flag as dataConvertFlag,
                    standard_commodity_code as standardCommondityCode,
                    standard_commodity_name as standardCommondityName,
                    package_name as packageName,
                    supplier_code as supplierCode,
                    supplier_name as supplierName,
                    manufacturer as manufatureName,
                    origin_code as originCode,
                    origin_name as originName,
                    scene_flag as sceneflag
                FROM retail_data
                WHERE report_date = CURDATE()
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # 处理日期和Decimal类型
            processed_results = []
            for row in results:
                processed_row = {}
                for key, value in row.items():
                    if key == 'reportDate':
                        processed_row[key] = value.strftime('%Y-%m-%d')
                    elif key == 'dataValue':
                        processed_row[key] = float(value)  # 转换Decimal为float
                    else:
                        processed_row[key] = value
                processed_results.append(processed_row)
            
            print(f"处理后的数据示例: {processed_results[0] if processed_results else 'No data'}")
            return processed_results
            
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return []
        finally:
            cursor.close() 