# 零售数据上报接口
这是一个用于向供应链安全监管平台上报零售数据的 Python 接口程序。
## 功能特性
- 支持用户认证和 Token 获取
 支持零售数据上报
 详细的日志输出
 完整的错误处理
## 安装要求
- Python 3.6+
 requests>=2.25.1
 urllib3>=2.0.0
## 安装步骤
1. 克隆代码库：
bash
git clone [https://github.com/jiaoxin327/Dali_Interface.git]
2. 安装依赖：
bash
pip install -r requirements.txt
## 使用说明

1. 配置登录信息：
   - 在 `main.py` 中设置正确的用户名和密码
   - 确认服务器地址和端口号

2. 运行程序：
bash
python main.py
3. 数据格式说明：
python
{
"itemId": "唯一标识",
"socialCreditCode": "统一社会信用代码",
"compName": "企业名称",
"retailStoreCode": "零售点代码",
"retailStoreName": "零售点名称",
"reportDate": "上报日期",
"selfCommondityCode": "商品编码",
"selfCommondityName": "商品名称",
"unit": "单位",
"spec": "规格",
"barcode": "条码",
"dataType": "数据类型",
"dataValue": "数据值",
"dataConvertFlag": "转换标志",
"supplierCode": "供应商编码",
"supplierName": "供应商名称",
"manufatureName": "生产商名称",
"originCode": "原产地代码",
"originName": "原产地名称",
"sceneflag": "采集场景"
}
## 配置说明

- `base_url`: API服务器地址
- `username`: 登录用户名
- `password`: 登录密码

## 错误处理

程序会处理以下情况：
- 网络连接错误
- 认证失败
- 数据上报失败
- 服务器响应异常

## 注意事项

1. 确保网络连接稳定
2. 正确设置登录凭证
3. 确保数据格式符合要求
4. 注意数据值的类型正确性

## 更新日志

### v1.0.0 (2024-03-20)
- 实现基本的登录认证功能
- 实现数据上报功能
- 添加详细的日志输出
- 完善错误处理机制
