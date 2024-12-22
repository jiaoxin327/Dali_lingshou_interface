# 零售数据上报系统

## 项目说明
用于向供应链安全监管平台上报零售数据的自动化程序。支持数据验证、定时上报和日志记录功能。

## 环境要求
- Python 3.6+
- MySQL 5.7+ 或 SQL Server 2014+
- Windows 系统
- 依赖包：
  - requests>=2.25.1
  - urllib3>=2.0.0
  - mysql-connector-python>=8.0.26
  - pyodbc>=4.0.39  # SQL Server支持
  - schedule>=1.1.0
  - PyQt5>=5.15.0
  - pandas>=2.2.3
  - openpyxl>=3.1.0
  - xlrd>=2.0.1

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
├── db_utils.py         # 数据操作工具
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

## 配置文件设置
- 复制 `config.json.example` 为 `config.json`
- 修改数据库连接信息和API配置

## 使用说明

### 1. 基本配置
- 数据库配置：设置数据库连接信息
- API配置：设置API接口地址和认证信息
- 字段映射：配置数据库字段与API字段的对应关系

### 2. 数据上报方式

#### 2.1 数据库直连上报
1. 在"基本配置"中设置数据库连接
2. 在"字段映射"中配置字段对应关系
3. 点击主页面"开始上报"按钮

#### 2.2 Excel文件导入上报
1. 在"Excel映射"中创建映射配置
2. 在"数据导入"页面选择Excel文件
3. 验证数据后点击"上报数据"按钮

### 3. 定时任务配置
1. 进入"定时任务"页面
2. 启用定时任务并设置执行时间
3. 点击"启动任务"按钮

### 4. API接口配置
- 支持查看默认接口配置
- 可导入/导出配置
- 支持新建自定义配置
- 提供字段说明和验证

## 数据格式要求

### Excel文件格式
必须包含以下字段：
- 统一社会信用代码
- 企业名称
- 零售点编码
- 零售点名称
- 上报日期（格式：YYYY-MM-DD）
- 商品编码
- 商品名称
- 单位
- 规格
- 条码
- 数据类型（1:期初库存、2:入库量、3:销售量、4:价格）
- 数据值
- 转换标志（默认值：2）
- 供应商编码
- 供应商名称
- 生产商名称
- 产地编码
- 产地名称
- 场景标志（默认值：1）

### 数据库表结构
详见 `create_test_data.sql` 文件

## 文件说明
- `main.py`: 程序入口
- `gui.py`: 主要GUI实现
- `retail_api.py`: API接口封装
- `db_utils.py`: 数据库操作工具
- `utils/`: 工具类目录
- `requirements.txt`: 依赖包列表
- `create_test_data.sql`: 数据库建表脚本

## 配置文件
- `config.json`: 主配置文件
- `api_config.json`: API接口配置
- `mapping_history.json`: 字段映射配置
- `excel_mapping_history.json`: Excel映射配置
- `upload_history.json`: 上报历史记录

## 日志文件
- 位置：`logs/` 目录
- 格式：`YYYYMMDD_main.log`
- 内容：包含运行日志和错误信息

## 常见问题
1. 数据库连接失败
   - 检查数据库配置信息
   - 确认数据库服务是否运行
   - 验证用户权限

2. API上报失败
   - 检查网络连接
   - 验证API配置信息
   - 查看错误日志

3. Excel导入失败
   - 确认文件格式是否正确
   - 检查必要字段是否完整
   - 验证数据格式是否符合要求

## 更新日志
### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本数据上报功能
- 实现Excel导入功能
- 添加定时任务支持

### v1.1.0 (2024-01-15)
- 添加API配置管理
- 优化Excel映射功能
- 改进错误处理
- 添加历史记录查询

## 开发团队
- 开发人员：[开发者名单]
- 技术支持：[支持团队]
- 联系方式：[联系信息]

## 许可证
[许可证类型]

## 技术支持
如需帮助，请联系：
- 邮箱：939813944@qq.com
- 电话：
### 问题反馈
1. 提供详细的错误信息
2. 附上相关的日志文件
3. 说明操作步骤
4. 提供测试数据（可选）

## 许可说明
版权所有 © 2024 [公司名称]
保留所有权利。

## 免责声明
1. 本工具仅用于数据上报
2. 请确保数据准确性
3. 及时备份重要数据
4. 遵守相关法律法规

## 数据库配置
### MySQL
```json
{
    "database": {
        "type": "mysql",
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "your_password",
        "database": "retail_report"
    }
}
```

### SQL Server
```json
{
    "database": {
        "type": "sqlserver",
        "host": "localhost",
        "port": 1433,
        "user": "sa",
        "password": "your_password",
        "database": "retail_report"
    }
}
```

## SQL Server注意事项
1. 确保已安装SQL Server ODBC驱动
2. 启用SQL Server身份验证模式
3. 确保用户有足够的数据库权限
4. 检查SQL Server网络配置是否允许TCP/IP连接