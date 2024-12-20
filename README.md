# 零售数据上报系统
## 项目说明
于向供应链安全监管平台上报零售数据的自动化程序。支持数据验证、定时上报和日志记录功能。
## 环境要求
 Python 3.6+
 MySQL 5.7+
 依赖包：
 - requests>=2.25.1
 - urllib3>=2.0.0
 - mysql-connector-python>=8.0.26
 - schedule>=1.1.0
## 快速开始
### 1. 安装依赖
```bash
pip install -r requirements.txt
```
### 2. 数据库配置
bash
创建数据库和测试数据
mysql -u root -pCes123456 < create_test_data.sql
### 3. 运行程序
bash
手动运行
python main.py
定时任务运行
python scheduler.py
## 功能特性
- 用户认证和 Token 管理
- 数据自动验证
- 定时上报（默认每天 9:00 和 15:00）
- 详细的日志记录
- 完整的错误处理

## 目录结构
├── main.py # 主程序入口
├── scheduler.py # 定时任务
├── db_utils.py # 数据库操作工具
├── retail_api.py # API接口封装
├── create_test_data.sql # 数据库初始化脚本
├── requirements.txt # 依赖包列表
├── utils/
│ ├── logger.py # 日志工具
│ └── validator.py # 数据验证工具
└── logs/ # 日志文件目录
## 配置说明

### 数据库配置
python
main.py
db = DatabaseConnection(
host='localhost',
user='root',
password='Ces123456',
database='retail_report'
)
### API配置
python
main.py
api = RetailAPI("http://49.235.172.155:3727/supply-security-api")
api.login("SFJRPA1234", "Dlbg@123")
### 定时任务配置
python
scheduler.py
schedule.every().day.at("09:00").do(job) # 每天9点执行
schedule.every().day.at("15:00").do(job) # 每天15点执行
## 数据格式说明

### 上报数据字段
| 字段名 | 说明 | 必填 | 类型 |
|--------|------|------|------|
| itemId | 唯一标识 | 是 | string |
| socialCreditCode | 统一社会信用代码 | 是 | string |
| compName | 企业名称 | 是 | string |
| retailStoreCode | 零售点代码 | 是 | string |
| retailStoreName | 零售点名称 | 是 | string |
| reportDate | 上报日期 | 是 | string(YYYY-MM-DD) |
| selfCommondityCode | 商品编码 | 是 | string |
| selfCommondityName | 商品名称 | 是 | string |
| dataType | 数据类型 | 是 | int(1-4) |
| dataValue | 数据值 | 是 | float |

### 数据类型说明
- 1: 进货量
- 2: 零售量
- 3: 库存量
- 4: 价格

## 日志说明
- 位置：logs 目录
- 格式：YYYYMMDD_模块名.log
- 内容：时间戳、日志级别、模块名、行号和详细信息

## 错误处理
程序会处理以下情况：
1. 网络连接错误
2. 数据库连接错误
3. 数据验证错误
4. API响应错误
5. 定时任务异常

## 部署说明

### Windows
batch
创建启动脚本 start.bat
@echo off
python scheduler.py > logs/scheduler.log 2>&1
### Linux
bash
使用 nohup
nohup python scheduler.py > logs/scheduler.log 2>&1 &
或使用 screen
screen -S retail_scheduler
python scheduler.py
Ctrl+A+D 分离 screen
## 注意事项
1. 确保网络连接稳定
2. 确保数据库服务正常运行
3. 定期检查日志文件
4. 建议配置监控告警

## 更新日志

### v1.1.0 (2024-03-20)
- 添加数据验证功能
- 添加日志记录功能
- 添加定时任务功能
- 完善错误处理机制

### v1.0.0 (2024-03-19)
- 实现基本的登录认证功能
- 实现数据上报功能

## 联系方式
- 作者：焦鑫
- 邮箱：939813944@qq.com
