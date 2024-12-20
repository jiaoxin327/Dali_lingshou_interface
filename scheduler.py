import schedule
import time
from datetime import datetime
from main import main
from utils.logger import Logger

logger = Logger('scheduler')

def job():
    """定时任务"""
    logger.info("开始执行定时任务")
    try:
        main()
        logger.info("定时任务执行完成")
    except Exception as e:
        logger.error(f"定时任务执行失败: {str(e)}")

def run_scheduler():
    """运行定时任务"""
    # 设置定时任务
    schedule.every().day.at("09:00").do(job)  # 每天9点执行
    schedule.every().day.at("15:00").do(job)  # 每天15点执行
    
    # 也可以设置其他时间
    # schedule.every(1).hours.do(job)  # 每小时执行
    # schedule.every().monday.at("12:00").do(job)  # 每周一12点执行
    # schedule.every(10).minutes.do(job)  # 每10分钟执行
    
    logger.info("定时任务已启动")
    logger.info("预设执行时间: 每天 09:00 和 15:00")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
        except Exception as e:
            logger.error(f"定��任务异常: {str(e)}")
            time.sleep(300)  # 发生异常时等待5分钟后继续

if __name__ == "__main__":
    try:
        logger.info("=== 定时任务程序启动 ===")
        # 启动时先执行一次
        logger.info("执行启动时任务")
        job()
        # 启动定时任务
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("程序被手动终止")
    except Exception as e:
        logger.error(f"程序异常终止: {str(e)}") 