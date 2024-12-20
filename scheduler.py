import schedule
import time
from datetime import datetime
from main import main
from utils.logger import Logger

logger = Logger('scheduler')

class TaskStats:
    def __init__(self):
        self.total_runs = 0
        self.success_runs = 0
        self.fail_runs = 0
        self.last_run_time = None
        self.last_success_time = None
        self.last_error = None
        
    def record_success(self):
        self.total_runs += 1
        self.success_runs += 1
        self.last_run_time = datetime.now()
        self.last_success_time = self.last_run_time
        
    def record_failure(self, error):
        self.total_runs += 1
        self.fail_runs += 1
        self.last_run_time = datetime.now()
        self.last_error = str(error)
        
    def get_stats(self):
        return (
            f"运行统计:\n"
            f"- 总运行次数: {self.total_runs}\n"
            f"- 成功次数: {self.success_runs}\n"
            f"- 失败次数: {self.fail_runs}\n"
            f"- 成功率: {(self.success_runs/self.total_runs*100 if self.total_runs else 0):.1f}%\n"
            f"- 上次运行: {self.last_run_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_run_time else 'Never'}\n"
            f"- 上次成功: {self.last_success_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_success_time else 'Never'}\n"
            f"- 上次错误: {self.last_error if self.last_error else 'None'}"
        )

stats = TaskStats()

def job():
    """定时任务"""
    logger.info("开始执行定时任务")
    try:
        main()
        logger.info("定时任务执行完成")
        stats.record_success()
    except Exception as e:
        error_msg = f"定时任务执行失败: {str(e)}"
        logger.error(error_msg)
        stats.record_failure(error_msg)

def run_scheduler():
    """运行定时任务"""
    # 测试用：每5分钟执行一次
    schedule.every(5).minutes.do(job)
    
    # 测试用：整点过1分时执行
    schedule.every().hour.at(":01").do(job)
    
    logger.info("定时任务已启动")
    logger.info("测试配置: 每5分钟执行一次，整点过1分执行")
    
    while True:
        try:
            # 打印统计信息和下一次执行时间
            next_run = schedule.next_run()
            logger.info("\n" + stats.get_stats())
            logger.info(f"下一次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
        except Exception as e:
            logger.error(f"定时任务异常: {str(e)}")
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
        logger.info("\n最终统计:\n" + stats.get_stats())
    except Exception as e:
        logger.error(f"程序异常终止: {str(e)}") 