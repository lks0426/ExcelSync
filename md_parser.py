#!/usr/bin/env python3
"""
MD财务报表解析模块
将MD格式的财务报表转换为JSON格式
"""

import re
import json
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from mapping_config import TRIAL_BALANCE_MAPPING, CELL_DESCRIPTIONS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MDFinancialParser:
    """
    解析MD格式的财务报表并转换为JSON格式
    """
    
    def __init__(self):
        """初始化解析器"""
        self.japanese_to_field_mapping = self._build_japanese_mapping()
        logger.info(f"已构建 {len(self.japanese_to_field_mapping)} 个日文到字段的映射")
        
    def _build_japanese_mapping(self) -> Dict[str, str]:
        """
        从mapping_config构建日文科目名到JSON字段的映射
        
        返回:
            日文科目名到JSON字段名的映射字典
        """
        mapping = {}
        
        # 从CELL_DESCRIPTIONS中提取日文名称
        for cell, description in CELL_DESCRIPTIONS.items():
            # 提取日文部分（括号前的内容）
            japanese_name = description.split(' (')[0].strip()
            
            # 查找对应的JSON字段
            for field, cell_ref in TRIAL_BALANCE_MAPPING.items():
                if cell_ref == cell:
                    mapping[japanese_name] = field
                    break
        
        # 添加一些特殊的映射（处理格式差异）
        special_mappings = {
            "現金及び預金合計": "cash_and_deposits_total",
            "売上債権合計": "receivables_total",
            "その他流動資産合計": "other_current_assets_total",
            "流動資産合計": "current_assets_total",
            "有形固定資産合計": "tangible_fixed_assets_total",
            "投資その他の資産合計": "investment_assets_total",
            "固定資產合計": "fixed_assets_total",  # 注意是資產不是資産
            "資産の部合計": "total_assets",
            "その他流動負債合計": "other_current_liabilities_total",
            "流動負債合計": "current_liabilities_total",
            "固定負債合計": "fixed_liabilities_total",
            "負債の部合計": "total_liabilities",
            "資本金合計": "capital_stock_duplicate",  # 特殊处理
            "資本剰余金合計": "capital_surplus_total",
            "利益剩余金合計": "retained_earnings_total",  # 注意是剩余不是剰余
            "株主資本合計": "shareholders_equity_total",
            "純資産の部合計": "net_assets_total",
            "負債·純資産の部合計": "total_liabilities_and_equity",
            "負債・純資産の部合計": "total_liabilities_and_equity",  # 处理不同的中点符号
            "繰越利益剩余金": "retained_earnings"  # 添加留存收益映射
        }
        
        mapping.update(special_mappings)
        
        logger.debug("映射关系构建完成:")
        for jp, en in mapping.items():
            logger.debug(f"  {jp} -> {en}")
            
        return mapping
    
    def _clean_subject_name(self, name: str) -> str:
        """
        清理科目名称
        
        参数:
            name: 原始科目名称
            
        返回:
            清理后的科目名称
        """
        if not name:
            return ""
            
        # 去除前后空格
        name = name.strip()
        
        # 去除【】符号
        name = name.replace('【', '').replace('】', '')
        
        # 统一全角半角
        # 这里可以根据需要添加更多转换
        
        return name
    
    def _parse_numeric_value(self, value_str: str) -> float:
        """
        解析数值字符串
        
        参数:
            value_str: 数值字符串（可能包含逗号、负号等）
            
        返回:
            解析后的浮点数
        """
        if not value_str or value_str.strip() == "":
            return 0.0
            
        # 去除空格
        value_str = value_str.strip()
        
        # 处理负数（可能是负号开头）
        is_negative = value_str.startswith('-') or value_str.startswith('−')
        
        # 去除所有非数字字符（保留小数点）
        value_str = re.sub(r'[^0-9.-]', '', value_str)
        
        try:
            value = float(value_str)
            return -abs(value) if is_negative else value
        except ValueError:
            logger.warning(f"无法解析数值: {value_str}")
            return 0.0
    
    def parse_md_file(self, md_file_path: str) -> Dict[str, Any]:
        """
        解析MD文件并提取财务数据
        
        参数:
            md_file_path: MD文件路径
            
        返回:
            JSON格式的财务数据
        """
        logger.info(f"开始解析MD文件: {md_file_path}")
        
        # 读取MD文件
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用BeautifulSoup解析HTML表格
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            raise ValueError("MD文件中未找到表格")
        
        logger.info(f"找到 {len(tables)} 个表格")
        
        # 解析第一个表格（貸借対照表）
        result = self._parse_balance_sheet_table(tables[0])
        
        # 验证结果
        self._validate_result(result)
        
        return result
    
    def _parse_balance_sheet_table(self, table) -> Dict[str, Any]:
        """
        解析资产负债表表格
        
        参数:
            table: BeautifulSoup的table对象
            
        返回:
            提取的数据字典
        """
        result = {}
        capital_stock_count = 0  # 用于区分两个資本金
        
        # 遍历所有行
        rows = table.find_all('tr')
        logger.info(f"表格包含 {len(rows)} 行")
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            
            # 跳过表头或不完整的行
            if len(cells) < 5:
                continue
            
            # 提取科目名称（第1列）和当月残高（第5列）
            subject_name = cells[0].get_text()
            value_text = cells[4].get_text()  # 索引4是第5列
            
            # 清理科目名称
            subject_name = self._clean_subject_name(subject_name)
            
            if not subject_name:
                continue
            
            # 特殊处理資本金（出现两次）
            if subject_name == "資本金":
                capital_stock_count += 1
                if capital_stock_count == 1:
                    field_name = "capital_stock"
                else:
                    field_name = "capital_stock_duplicate"
            # 特殊处理一些没有【】的总计项目
            elif subject_name == "流動資産合計":
                field_name = "current_assets_total"
            elif subject_name == "固定資產合計":
                field_name = "fixed_assets_total"
            elif subject_name == "流動負債合計":
                field_name = "current_liabilities_total"
            elif subject_name == "固定負債合計":
                field_name = "fixed_liabilities_total"
            elif subject_name == "負債の部合計":
                field_name = "total_liabilities"
            elif subject_name == "資本金合計":
                field_name = "capital_stock_duplicate"
            elif subject_name == "資本剰余金合計" or subject_name == "資本剩余金合計":
                field_name = "capital_surplus_total"
            elif subject_name == "利益剰余金合計":
                field_name = "retained_earnings_total"
            elif subject_name == "株主資本合計":
                field_name = "shareholders_equity_total"
            elif subject_name == "純資産の部合計":
                field_name = "net_assets_total"
            elif subject_name == "負債·純資産の部合計" or subject_name == "負債・純資産の部合計":
                field_name = "total_liabilities_and_equity"
            else:
                # 查找对应的JSON字段名
                field_name = self.japanese_to_field_mapping.get(subject_name)
            
            if field_name:
                # 解析数值
                value = self._parse_numeric_value(value_text)
                result[field_name] = value
                logger.debug(f"行 {i+1}: {subject_name} -> {field_name} = {value}")
            else:
                logger.debug(f"行 {i+1}: 未找到映射 - {subject_name}")
        
        return result
    
    def _validate_result(self, result: Dict[str, Any]):
        """
        验证解析结果的完整性
        
        参数:
            result: 解析结果字典
        """
        # 检查必需字段
        required_fields = set(TRIAL_BALANCE_MAPPING.keys())
        extracted_fields = set(result.keys())
        
        missing_fields = required_fields - extracted_fields
        extra_fields = extracted_fields - required_fields
        
        if missing_fields:
            logger.warning(f"缺少 {len(missing_fields)} 个字段: {missing_fields}")
        
        if extra_fields:
            logger.warning(f"多余 {len(extra_fields)} 个字段: {extra_fields}")
        
        logger.info(f"成功提取 {len(extracted_fields)} / {len(required_fields)} 个字段")
    
    def save_to_json(self, data: Dict[str, Any], output_path: str):
        """
        将数据保存为JSON文件
        
        参数:
            data: 要保存的数据
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存到: {output_path}")


def main():
    """测试MD解析功能"""
    parser = MDFinancialParser()
    
    # 解析MD文件
    md_file = "corrected_financial_statement.md"
    
    try:
        data = parser.parse_md_file(md_file)
        
        # 保存为JSON
        output_file = "parsed_financial_data.json"
        parser.save_to_json(data, output_file)
        
        print(f"\n✅ 成功解析MD文件并生成JSON")
        print(f"📄 输出文件: {output_file}")
        print(f"📊 提取字段数: {len(data)}")
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        logger.error(f"解析失败: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()