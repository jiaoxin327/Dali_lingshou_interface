-- 创建数据库
CREATE DATABASE IF NOT EXISTS retail_report;
USE retail_report;

-- 创建零售数据表
CREATE TABLE IF NOT EXISTS retail_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    social_credit_code VARCHAR(50) DEFAULT '91532901792864164X1' COMMENT '统一社会信用代码',
    comp_name VARCHAR(100) DEFAULT '云南市四方街商贸有限公司' COMMENT '企业名称',
    retail_store_code VARCHAR(50) DEFAULT 'SFJRPA1234' COMMENT '零售点编码',
    retail_store_name VARCHAR(100) DEFAULT '四方街商贸零售点' COMMENT '零售点名称',
    report_date DATE NOT NULL COMMENT '上报日期',
    commodity_code VARCHAR(50) NOT NULL COMMENT '商品编码',
    commodity_name VARCHAR(100) NOT NULL COMMENT '商品名称',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    spec VARCHAR(50) NOT NULL COMMENT '规格',
    barcode VARCHAR(50) NOT NULL COMMENT '条码',
    data_type INT NOT NULL COMMENT '数据类型:1进货量,2零售量,3库存量,4价格',
    data_value DECIMAL(10,2) NOT NULL COMMENT '数据值',
    data_convert_flag INT DEFAULT 2 COMMENT '转换标志',
    standard_commodity_code VARCHAR(50) DEFAULT '' COMMENT '标准商品编码',
    standard_commodity_name VARCHAR(100) DEFAULT '' COMMENT '标准商品名称',
    package_name VARCHAR(50) DEFAULT '' COMMENT '包装名称',
    supplier_code VARCHAR(50) NOT NULL COMMENT '供应商编码',
    supplier_name VARCHAR(100) NOT NULL COMMENT '供应商名称',
    manufacturer VARCHAR(100) NOT NULL COMMENT '生产商名称',
    origin_code VARCHAR(10) DEFAULT '530000' COMMENT '原产地编码',
    origin_name VARCHAR(50) DEFAULT '云南省' COMMENT '原产地名称',
    scene_flag INT DEFAULT 1 COMMENT '采集场景',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
);

-- 插入测试数据
INSERT INTO retail_data (
    social_credit_code, comp_name, retail_store_code, retail_store_name,
    report_date, commodity_code, commodity_name, unit, spec, barcode,
    data_type, data_value, data_convert_flag,
    standard_commodity_code, standard_commodity_name, package_name,
    supplier_code, supplier_name, manufacturer,
    origin_code, origin_name, scene_flag
) VALUES
-- 蔬菜类
('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '170001', '大白菜', '公斤', '散装', '170001',
 4, 7.00, 2,
 '', '', '',
 'SUP001', '大理批发市场', '大理蔬菜基地',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '170001', '大白菜', '公斤', '散装', '170001',
 1, 100.00, 2,
 '', '', '',
 'SUP001', '大理批发市场', '大理蔬菜基地',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '170001', '大白菜', '公斤', '散装', '170001',
 2, 80.00, 2,
 '', '', '',
 'SUP001', '大理批发市场', '大理蔬菜基地',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '170001', '大白菜', '公斤', '散装', '170001',
 3, 50.00, 2,
 '', '', '',
 'SUP001', '大理批发市场', '大理蔬菜基地',
 '530000', '云南省', 1),

-- 饮料类
('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '10002791', '银鹭花生牛奶', '瓶', '1.5L', '6901234567890',
 4, 8.50, 2,
 '', '', '',
 'SUP001', '大理食品配送有限公司', '银鹭食品有限公司',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '10002791', '银鹭花生牛奶', '瓶', '1.5L', '6901234567890',
 1, 200.00, 2,
 '', '', '',
 'SUP001', '大理食品配送有限公司', '银鹭食品有限公司',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '10002791', '银鹭花生牛奶', '瓶', '1.5L', '6901234567890',
 2, 150.00, 2,
 '', '', '',
 'SUP001', '大理食品配送有限公司', '银鹭食品有限公司',
 '530000', '云南省', 1),

('91532901792864164X1', '云南市四方街商贸有限公司', 'SFJRPA1234', '四方街商贸零售点',
 CURDATE(), '10002791', '银鹭花生牛奶', '瓶', '1.5L', '6901234567890',
 3, 100.00, 2,
 '', '', '',
 'SUP001', '大理食品配送有限公司', '银鹭食品有限公司',
 '530000', '云南省', 1);
 