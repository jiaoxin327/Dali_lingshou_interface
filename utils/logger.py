import logging
import os
import sys
from datetime import datetime

class Logger:
    def __init__(self, name: str):
        # 创建logs目录
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 设置日志文件名，包含日期
        log_file = f'logs/{datetime.now().strftime("%Y%m%d")}_{name}.log'
        
        # 创建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 设置控制台编码
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        
        # 创建文件处理器，使用 utf-8-sig 编码（带 BOM）
        file_handler = logging.FileHandler(log_file, encoding='utf-8-sig', mode='a')
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, msg: str):
        self.logger.info(msg)
        
    def error(self, msg: str):
        self.logger.error(msg)
        
    def warning(self, msg: str):
        self.logger.warning(msg)
        
    def debug(self, msg: str):
        self.logger.debug(msg) 