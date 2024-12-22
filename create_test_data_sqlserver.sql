-- 创建数据库
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'retail_report')
BEGIN
    CREATE DATABASE retail_report;
END
GO

USE retail_report;
GO

-- 创建零售数据表
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[retail_data]') AND type in (N'U'))
BEGIN
    CREATE TABLE retail_data (
        id INT IDENTITY(1,1) PRIMARY KEY,
        social_credit_code VARCHAR(50) DEFAULT '91532901792864164X1',
        comp_name NVARCHAR(100) DEFAULT N'云南市四方街商贸有限公司',
        retail_store_code VARCHAR(50) DEFAULT 'SFJRPA1234',
        retail_store_name NVARCHAR(100) DEFAULT N'四方街商贸零售点',
        report_date DATE NOT NULL,
        commodity_code VARCHAR(50) NOT NULL,
        commodity_name NVARCHAR(100) NOT NULL,
        unit NVARCHAR(20) NOT NULL,
        spec NVARCHAR(50) NOT NULL,
        barcode VARCHAR(50) NOT NULL,
        data_type INT NOT NULL,
        data_value DECIMAL(10,2) NOT NULL,
        data_convert_flag INT DEFAULT 2,
        supplier_code VARCHAR(50) NOT NULL,
        supplier_name NVARCHAR(100) NOT NULL,
        manufacturer NVARCHAR(100) NOT NULL,
        origin_code VARCHAR(10) DEFAULT '530000',
        origin_name NVARCHAR(50) DEFAULT N'云南省',
        scene_flag INT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE()
    );
END
GO

-- 插入测试数据
INSERT INTO retail_data (
    social_credit_code, comp_name, retail_store_code, retail_store_name,
    report_date, commodity_code, commodity_name, unit, spec, barcode,
    data_type, data_value, data_convert_flag,
    supplier_code, supplier_name, manufacturer,
    origin_code, origin_name, scene_flag
)
VALUES
-- 蔬菜类数据
(
    '91532901792864164X1', N'云南市四方街商贸有限公司', 'SFJRPA1234', N'四方街商贸零售点',
    GETDATE(), '170001', N'大白菜', N'公斤', N'散装', '170001',
    4, 7.00, 2,
    'SUP001', N'大理批发市场', N'大理蔬菜基地',
    '530000', N'云南省', 1
);
GO 