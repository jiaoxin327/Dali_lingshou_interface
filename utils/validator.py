from typing import Dict, List, Optional
from datetime import datetime

class DataValidator:
    @staticmethod
    def validate_retail_data(data: Dict) -> Optional[str]:
        """验证单条零售数据"""
        required_fields = {
            'socialCreditCode': '统一社会信用代码',
            'compName': '企业名称',
            'retailStoreCode': '零售点编码',
            'retailStoreName': '零售点名称',
            'reportDate': '上报日期',
            'selfCommondityCode': '商品编码',
            'selfCommondityName': '商品名称',
            'unit': '单位',
            'spec': '规格',
            'barcode': '条码',
            'dataType': '数据类型',
            'dataValue': '数据值'
        }
        
        # 检查必填字段
        for field, name in required_fields.items():
            if field not in data or not data[field]:
                return f"{name}不能为空"
        
        # 验证数据类型
        try:
            # 验证日期格式
            datetime.strptime(data['reportDate'], '%Y-%m-%d')
            
            # 验证数据类��
            if not isinstance(data['dataType'], int):
                return "数据类型必须是整数"
            if data['dataType'] not in [1, 2, 3, 4]:
                return "数据类型必须是1,2,3,4之一"
                
            # 验证数据值
            if not isinstance(data['dataValue'], (int, float)):
                return "数据值必须是数字"
            if data['dataValue'] < 0:
                return "数据值不能为负数"
                
        except ValueError:
            return "日期格式错误，应为YYYY-MM-DD"
            
        return None
    
    @staticmethod
    def validate_batch_data(data_list: List[Dict]) -> List[Dict]:
        """验证批量数据，返回验证失败的记录列表"""
        failed_records = []
        
        for data in data_list:
            error = DataValidator.validate_retail_data(data)
            if error:
                failed_records.append({
                    'data': data,
                    'error': error
                })
                
        return failed_records 