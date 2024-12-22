import pandas as pd
import numpy as np
from datetime import datetime

# 创建示例数据
example_data = [
    {
        '统一社会信用代码': '91532901792864164X1',
        '企业名称': '云南市四方街商贸有限公司',
        '零售点编码': 'SFJRPA1234',
        '零售点名称': '四方街商贸零售点',
        '上报日期': datetime.now().strftime('%Y-%m-%d'),
        '商品编码': '170060',
        '商品名称': '大白菜',
        '单位': '公斤',
        '规格': '散装',
        '条码': '170060',
        '数据类型': 1,
        '数据值': 100.00,
        '转换标志': 2,
        '供应商编码': 'SUP001',
        '供应商名称': '大理批发市场',
        '生产商名称': '大理蔬菜基地',
        '产地编码': '530000',
        '产地名称': '云南省',
        '场景标志': 1
    },
    {
        '统一社会信用代码': '91532901792864164X1',
        '企业名称': '云南市四方街商贸有限公司',
        '零售点编码': 'SFJRPA1234',
        '零售点名称': '四方街商贸零售点',
        '上报日期': datetime.now().strftime('%Y-%m-%d'),
        '商品编码': '170060',
        '商品名称': '大白菜',
        '单位': '公斤',
        '规格': '散装',
        '条码': '170060',
        '数据类型': 2,
        '数据值': 80.00,
        '转换标志': 2,
        '供应商编码': 'SUP001',
        '供应商名称': '大理批发市场',
        '生产商名称': '大理蔬菜基地',
        '产地编码': '530000',
        '产地名称': '云南省',
        '场景标志': 1
    },
    {
        '统一社会信用代码': '91532901792864164X1',
        '企业名称': '云南市四方街商贸有限公司',
        '零售点编码': 'SFJRPA1234',
        '零售点名称': '四方街商贸零售点',
        '上报日期': datetime.now().strftime('%Y-%m-%d'),
        '商品编码': '170060',
        '商品名称': '大白菜',
        '单位': '公斤',
        '规格': '散装',
        '条码': '170060',
        '数据类型': 3,
        '数据值': 50.00,
        '转换标志': 2,
        '供应商编码': 'SUP001',
        '供应商名称': '大理批发市场',
        '生产商名称': '大理蔬菜基地',
        '产地编码': '530000',
        '产地名称': '云南省',
        '场景标志': 1
    },
    {
        '统一社会信用代码': '91532901792864164X1',
        '企业名称': '云南市四方街商贸有限公司',
        '零售点编码': 'SFJRPA1234',
        '零售点名称': '四方街商贸零售点',
        '上报日期': datetime.now().strftime('%Y-%m-%d'),
        '商品编码': '170060',
        '商品名称': '大白菜',
        '单位': '公斤',
        '规格': '散装',
        '条码': '170060',
        '数据类型': 4,
        '数据值': 7.00,
        '转换标志': 2,
        '供应商编码': 'SUP001',
        '供应商名称': '大理批发市场',
        '生产商名称': '大理蔬菜基地',
        '产地编码': '530000',
        '产地名称': '云南省',
        '场景标志': 1
    }
]

# 创建DataFrame
df = pd.DataFrame(example_data)

# 创建Excel写入器
with pd.ExcelWriter('数据导入模板.xlsx', engine='openpyxl') as writer:
    # 直接写入数据，不包含说明行
    df.to_excel(writer, sheet_name='数据模板', index=False)
    
    # 获取工作表
    worksheet = writer.sheets['数据模板']
    
    # 设置列宽并处理中文字符
    for idx, column in enumerate(worksheet.columns):
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                # 处理中文字符
                if isinstance(cell.value, str):
                    length = sum(2 if ord(c) > 127 else 1 for c in cell.value)
                else:
                    length = len(str(cell.value))
                max_length = max(max_length, length)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # 增加一些额外宽度
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

print("模板文件已创建：数据导入模板.xlsx") 