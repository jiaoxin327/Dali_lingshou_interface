import pandas as pd
import numpy as np
from datetime import datetime

# 创建示例数据
example_data = {
    '统一社会信用代码 (socialCreditCode)': ['91532901792864164X1'] * 4,
    '企业名称 (compName)': ['云南市四方街商贸有限公司'] * 4,
    '零售点编码 (retailStoreCode)': ['SFJRPA1234'] * 4,
    '零售点名称 (retailStoreName)': ['四方街商贸零售点'] * 4,
    '上报日期 (reportDate)': [datetime.now().strftime('%Y-%m-%d')] * 4,
    '商品编码 (selfCommondityCode)': ['170060'] * 4,
    '商品名称 (selfCommondityName)': ['大白菜'] * 4,
    '单位 (unit)': ['公斤'] * 4,
    '规格 (spec)': ['散装'] * 4,
    '条码 (barcode)': ['170060'] * 4,
    '数据类型 (dataType)': [1, 2, 3, 4],  # 期初库存、入库量、销售量、价格
    '数据值 (dataValue)': [100, 80, 50, 7.00],
    '转换标志 (dataConvertFlag)': [2] * 4,
    '供应商编码 (supplierCode)': ['SUP001'] * 4,
    '供应商名称 (supplierName)': ['大理批发市场'] * 4,
    '生产商名称 (manufatureName)': ['大理蔬菜基地'] * 4,
    '产地编码 (originCode)': ['530000'] * 4,
    '产地名称 (originName)': ['云南省'] * 4,
    '场景标志 (sceneflag)': [1] * 4
}

# 创建DataFrame
df = pd.DataFrame(example_data)

# 添加说明行
description_data = {
    '统一社会信用代码 (socialCreditCode)': '企业统一社会信用代码',
    '企业名称 (compName)': '企业全称',
    '零售点编码 (retailStoreCode)': '零售点唯一编码',
    '零售点名称 (retailStoreName)': '零售点名称',
    '上报日期 (reportDate)': '数据日期（格式：YYYY-MM-DD）',
    '商品编码 (selfCommondityCode)': '商品唯一编码',
    '商品名称 (selfCommondityName)': '商品名称',
    '单位 (unit)': '计量单位',
    '规格 (spec)': '商品规格',
    '条码 (barcode)': '商品条形码',
    '数据类型 (dataType)': '1期初库存、2入库量、3销售量、4价格',
    '数据值 (dataValue)': '对应数据类型的数值',
    '转换标志 (dataConvertFlag)': '默认值2',
    '供应商编码 (supplierCode)': '供应商编码',
    '供应商名称 (supplierName)': '供应商名称',
    '生产商名称 (manufatureName)': '生产厂家名称',
    '产地编码 (originCode)': '产地编码（示例：530000）',
    '产地名称 (originName)': '产地名称（示例：云南省）',
    '场景标志 (sceneflag)': '场景标志（默认值1）'
}

description_df = pd.DataFrame([description_data])

# ��并说明和示例数据
final_df = pd.concat([description_df, df], ignore_index=True)

# 创建Excel写入器
with pd.ExcelWriter('数据导入模板.xlsx', engine='openpyxl') as writer:
    # 写入数据页
    final_df.to_excel(writer, sheet_name='数据模板', index=False)
    
    # 获取工作簿和工作表
    workbook = writer.book
    worksheet = writer.sheets['数据模板']
    
    # 设置列宽
    for column in worksheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
    # 设置说明行样式
    from openpyxl.styles import PatternFill, Font
    yellow_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
    red_font = Font(color='FF0000')
    
    for cell in worksheet[1]:
        cell.fill = yellow_fill
        cell.font = red_font

print("模板文件已创建：数据导入模板.xlsx") 