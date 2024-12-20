from retail_api import RetailAPI
from datetime import datetime

def get_sample_data():
    """
    生成示例零售数据
    Returns:
        List[Dict]: 包含一条零售数据的列表
    """
    return [{
        # 使用时间戳生成唯一ID，确保每条数据都有唯一标识
        "itemId": "YN" + datetime.now().strftime("%Y%m%d%H%M%S"),
        
        # 企业基本信息
        "socialCreditCode": "91532901792864164X1",  # 统一社会信用代码
        "compName": "云南市四方街商贸有限公司",     # 企业名称
        "retailStoreCode": "SFJRPA1234",           # 零售点编码
        "retailStoreName": "四方街商贸零售点",      # 零售点名称
        
        # 上报日期，使用当前日期
        "reportDate": datetime.now().strftime("%Y-%m-%d"),
        
        # 商品信息
        "selfCommondityCode": "10002791",          # 商品编码
        "selfCommondityName": "银鹭花生牛奶1.5L",   # 商品名称
        "unit": "瓶",                              # 商品单位
        "spec": "1.5L",                           # 商品规格
        "barcode": "6901234567890",               # 商品条码
        
        # 数据类型和值
        "dataType": 1,                            # 1：进货量
        "dataValue": 100.0,                       # 数据值
        "dataConvertFlag": 2,                     # 2：需要转换
        
        # 标准商品信息（转换相关）
        "standardCommondityCode": "",             # 标准品名编码
        "standardCommondityName": "",             # 标准品名
        "packageName": "",                        # 标准单位
        
        # 供应商和生产商信息
        "supplierCode": "SUP001",                 # 供应商编码
        "supplierName": "示例供应商",              # 供应商名称
        "manufatureName": "银鹭食品有限公司",       # 生产商名称
        
        # 产地信息
        "originCode": "530000",                   # 原产地编码（云南省）
        "originName": "云南省",                    # 原产地名称
        
        # 采集场景：1-日常采集，2-应急采集
        "sceneflag": 1
    }]

def main():
    """主程序入口"""
    # 初始化API客户端，使用新的服务器地址和端口
    api = RetailAPI("http://49.235.172.155:3727/supply-security-api")
    
    # 登录系统（使用正确的密码）
    if not api.login("SFJRPA1234", "Dlbg@123"):
        print("登录失败")
        return
        
    # 获取要上报的数据
    retail_data = get_sample_data()
    
    # 上报数据并处理响应
    result = api.upload_retail_data(retail_data)
    if result and result.get("code") == 200:
        print("数据上报成功")
        # 打印每条数据的处理结果
        for item in result.get("content", []):
            print(f"数据ID: {item['soureId']}, 状态: {item['code']}, 消息: {item['msg']}")
    else:
        print("数据上报失败")
        print(result)

if __name__ == "__main__":
    main() 