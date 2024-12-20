from retail_api import RetailAPI
from db_utils import DatabaseConnection
from utils.logger import Logger
from utils.validator import DataValidator
from datetime import datetime
import sys

logger = Logger('main')

def get_data_from_db():
    """从数据库获取数据"""
    logger.info("开始获取数据库数据...")
    db = DatabaseConnection(
        host='localhost',
        user='root',
        password='Ces123456',
        database='retail_report'
    )
    
    try:
        if not db.test_connection():
            logger.error("数据库连接测试失败")
            return []
            
        if not db.check_table_exists():
            logger.error("数据表不存在")
            return []
            
        data = db.get_retail_data()
        
        # 数据验证
        failed_records = DataValidator.validate_batch_data(data)
        if failed_records:
            logger.error("数据验证失败:")
            for record in failed_records:
                logger.error(f"数据: {record['data']}")
                logger.error(f"错误: {record['error']}")
            return []
            
        logger.info(f"获取到 {len(data)} 条有效数据")
        return data
        
    except Exception as e:
        logger.error(f"数据库操作失败: {str(e)}")
        return []
    finally:
        db.close()

def main():
    """主程序入口"""
    try:
        logger.info("=== 程序开始执行 ===")
        
        # 初始化API客户端
        api = RetailAPI("http://49.235.172.155:3727/supply-security-api")
        
        # 登录系统
        if not api.login("SFJRPA1234", "Dlbg@123"):
            logger.error("登录失败")
            return
            
        # 获取数据
        retail_data = get_data_from_db()
        if not retail_data:
            logger.warning("没有获取到需要上报的数据")
            return
            
        # 上报数据
        result = api.upload_retail_data(retail_data)
        if result and result.get("code") == 200:
            logger.info("数据上报成功")
            for item in result.get("content", []):
                logger.info(f"数据ID: {item['soureId']}, 状态: {item['code']}, 消息: {item['msg']}")
        else:
            logger.error("数据上报失败")
            logger.error(str(result))
            
    except Exception as e:
        logger.error(f"程序执行异常: {str(e)}")
    finally:
        logger.info("=== 程序执行完成 ===")

if __name__ == "__main__":
    main() 