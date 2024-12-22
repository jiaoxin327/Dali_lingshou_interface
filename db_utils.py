import mysql.connector
import pyodbc
from typing import List, Dict
from datetime import datetime
import json
from decimal import Decimal

class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306, db_type: str = 'mysql'):
        self.db_type = db_type.lower()
        self.conn = None
        
        if self.db_type == 'mysql':
            self.config = {
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port,
                'connect_timeout': 10,
                'use_pure': True,
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci',
                'auth_plugin': 'mysql_native_password',
                'raise_on_warnings': True,
                'connection_timeout': 10,
                'buffered': True
            }
        elif self.db_type == 'sqlserver':
            self.config = {
                'server': host,
                'database': database,
                'user': user,
                'password': password,
                'port': port,
                'driver': '{SQL Server}'  # 或者使用 '{ODBC Driver 17 for SQL Server}'
            }
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
            
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            print(f"尝试连接数据库: {self.config.get('host') or self.config.get('server')}:{self.config.get('port')}")
            print(f"数据库名: {self.config['database']}")
            print(f"用户名: {self.config['user']}")
            
            if self.db_type == 'mysql':
                return self._test_mysql_connection()
            else:
                return self._test_sqlserver_connection()
                
        except Exception as e:
            print(f"连接异常: {str(e)}")
            print("请检查数据库服务是否正常运行")
            return False
            
    def _test_mysql_connection(self) -> bool:
        """测试MySQL连接"""
        try:
            # MySQL连接测试代码保持不变
            test_config = self.config.copy()
            test_config.pop('database', None)
            
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
            
            full_conn = mysql.connector.connect(**self.config)
            print("数据库连接测试完全成功")
            full_conn.close()
            return True
            
        except Exception as e:
            print(f"MySQL连接测试失败: {str(e)}")
            return False
            
    def _test_sqlserver_connection(self) -> bool:
        """测试SQL Server连接"""
        try:
            conn_str = (
                f"DRIVER={self.config['driver']};"
                f"SERVER={self.config['server']},{self.config['port']};"
                f"DATABASE={self.config['database']};"
                f"UID={self.config['user']};"
                f"PWD={self.config['password']}"
            )
            
            # 先测试基础连接
            test_conn = pyodbc.connect(conn_str, timeout=5)
            print("基础连接成功，检查数据库...")
            
            cursor = test_conn.cursor()
            cursor.execute("SELECT DB_ID(?)", (self.config['database'],))
            if not cursor.fetchone():
                print(f"数据库 {self.config['database']} 不存在，尝试创建...")
                cursor.execute(f"CREATE DATABASE {self.config['database']}")
                test_conn.commit()
                print("数据库创建成功")
                
            cursor.close()
            test_conn.close()
            return True
            
        except Exception as e:
            print(f"SQL Server连接测试失败: {str(e)}")
            return False
            
    def connect(self):
        """连接数据库"""
        try:
            if self.db_type == 'mysql':
                if not self.conn or not self.conn.is_connected():
                    self.conn = mysql.connector.connect(**self.config)
                    self.conn.ping(reconnect=True, attempts=3, delay=5)
            else:
                if not self.conn:
                    conn_str = (
                        f"DRIVER={self.config['driver']};"
                        f"SERVER={self.config['server']},{self.config['port']};"
                        f"DATABASE={self.config['database']};"
                        f"UID={self.config['user']};"
                        f"PWD={self.config['password']}"
                    )
                    self.conn = pyodbc.connect(conn_str, timeout=30)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            raise
            
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
                field_mappings = mapping_config.get('fields', {})
                
            if not field_mappings:
                raise ValueError("字段映射配置为空")
                
            cursor = self.conn.cursor(dictionary=True) if self.db_type == 'mysql' else self.conn.cursor()
            
            # 构建SQL查询
            field_list = []
            for db_field, api_field in field_mappings.items():
                if self.db_type == 'mysql':
                    if db_field == 'report_date':
                        field_list.append(f"DATE_FORMAT({db_field}, '%Y-%m-%d') as {api_field}")
                    else:
                        field_list.append(f"{db_field} as {api_field}")
                else:
                    if db_field == 'report_date':
                        field_list.append(f"CONVERT(VARCHAR(10), {db_field}, 120) as {api_field}")
                    else:
                        field_list.append(f"{db_field} as {api_field}")
                        
            # 构建不同数据库的SQL语句
            if self.db_type == 'mysql':
                query = f"""
                    SELECT 
                        CONCAT('YN', DATE_FORMAT(report_date, '%Y%m%d'), LPAD(id, 6, '0')) as itemId,
                        {', '.join(field_list)}
                    FROM {table_name}
                    WHERE report_date = CURDATE()
                """
            else:
                query = f"""
                    SELECT 
                        'YN' + CONVERT(VARCHAR(8), report_date, 112) + RIGHT('000000' + CAST(id AS VARCHAR), 6) as itemId,
                        {', '.join(field_list)}
                    FROM {table_name}
                    WHERE CONVERT(DATE, report_date) = CAST(GETDATE() AS DATE)
                """
            
            print(f"执行SQL查询: {query}")
            cursor.execute(query)
            
            if self.db_type == 'mysql':
                results = cursor.fetchall()
            else:
                # 处理SQL Server的结果
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
            
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
            
            print(f"获取到 {len(processed_results)} 条数据")
            return processed_results
            
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return []
        finally:
            cursor.close() 