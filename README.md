# 零售数据上报系统

## 项目说明
用于向供应链安全监管平台上报零售数据的自动化程序。支持数据验证、定时上报和日志记录功能。

## 环境要求
- Python 3.6+
- MySQL 5.7+
- Windows 系统（批处理脚本支持）
- 依赖包：
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
```sql
-- 创建数据库和测试数据
mysql -u root -pCes123456 < create_test_data.sql
```

### 3. 运行程序

#### 开发测试模式
```bash
# 直接运行，查看输出
test_scheduler.bat
```

#### 生产环境模式
```bash
# 后台运行
start_scheduler.bat

# 停止程序
stop_scheduler.bat
```

## 功能特性
- 用户认证和 Token 管理
- 数据自动验证
- 定时上报（默认每5分钟）
- 详细的日志记录
- 完整的错误处理
- 运行状态统计

## 目录结构
```
├── main.py              # 主程序入口
├── scheduler.py         # 定时任务
├── db_utils.py         # 数据库操作工具
├── retail_api.py       # API接口封装
├── requirements.txt    # 依赖包列表
├── utils/
│   ├── logger.py      # 日志工具
│   └── validator.py   # 数据验证工具
├── logs/              # 日志文件目录
├── start_scheduler.bat # 启动脚本
├── stop_scheduler.bat  # 停止脚本
└── test_scheduler.bat  # 测试脚本
```

## 配置说明

### 数据库配置
```python
# main.py
db = DatabaseConnection(
    host='localhost',
    user='root',
    password='Ces123456',
    database='retail_report'
)
```

### 定时任务配置
```python
# scheduler.py
# 每5分钟执行一次
schedule.every(5).minutes.do(job)

# 整点过1分执行
schedule.every().hour.at(":01").do(job)
```

## 运行管理

### 启动程序
1. 测试模式：
   - 双击运行 `test_scheduler.bat`
   - 在控制台查看输出
   - Ctrl+C 停止

2. 生产模式：
   - 双击运行 `start_scheduler.bat`
   - 程序在后台运行
   - 通过日志文件监控

### 停止程序
1. 双击运行 `stop_scheduler.bat`
2. 确认进程信息
3. 选择 Y 确认停止

### 日志查看
- 位置：logs 目录
- 文件命名：YYYYMMDD_模块名.log
- 编码：UTF-8 with BOM
- 格式：
  ```
  [时间] 级别 [模块:行号] 消息
  ```

### 运行统计
程序会记录以下统计信息：
- 总运行次数
- 成功次数
- 失败次数
- 成功率
- 上次运行时间
- 上次成功时间
- 上次错误信息

## 错误处理
程序会处理以下情况：
1. 网络连接错误
2. 数据库连接错误
3. 数据验证错误
4. API响应错误
5. 定时任务异常

## 注意事项
1. 确保网络连接稳定
2. 确保数据库服务正常运行
3. 定期检查日志文件
4. 建议配置监控告警
5. 使用停止脚本而不是直接关闭进程

## 更新日志

### v1.1.0 (2024-03-20)
- 添加数据验证功能
- 添加日志记录功能
- 添加定时任务功能
- 完善错误处理机制
- 添加运行状态统计
- 优化批处理脚本

### v1.0.0 (2024-03-19)
- 实现基本的登录认证功能
- 实现数据上报功能

## 联系方式
- 作者：焦鑫
- 邮箱：939813944@qq.com
