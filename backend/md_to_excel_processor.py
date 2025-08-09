#!/usr/bin/env python3
"""
MD到Excel处理器
将Markdown表格解析并生成带有D列数据的Excel文件
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from md_parser import MDParser
from excel_writer import ExcelWriter
from data_validator import prepare_api_data
from mapping_config import TRIAL_BALANCE_MAPPING, CELL_DESCRIPTIONS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MDToExcelProcessor:
    """
    处理MD文件到Excel文件的完整工作流程
    """
    
    def __init__(self, excel_template_path: str = "mapping.xlsx", sheet_name: str = "A社貼り付けBS"):
        """
        初始化处理器
        
        参数:
            excel_template_path: Excel模板文件路径
            sheet_name: 工作表名称
        """
        self.excel_template_path = Path(excel_template_path)
        self.sheet_name = sheet_name
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化组件
        self.md_parser = MDParser()
        self.excel_writer = ExcelWriter(str(self.excel_template_path), sheet_name)
        
        # 构建完整的日文到英文字段映射
        self.japanese_to_field_mapping = self._build_japanese_mapping()
        logger.info(f"已构建 {len(self.japanese_to_field_mapping)} 个日文到字段的映射")
        
    def process_md_content(self, md_content: str, filename: str = "uploaded.md") -> Dict[str, Any]:
        """
        处理MD文本内容并生成Excel文件
        
        参数:
            md_content: Markdown文本内容
            filename: 原始文件名
            
        返回:
            处理结果字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 解析MD内容
            logger.info(f"🔍 开始解析Markdown内容 (文件: {filename})...")
            logger.debug(f"MD内容长度: {len(md_content)} 字符")
            parsed_result = self.md_parser.parse(md_content)
            logger.info(f"📊 MD解析完成，发现 {len(parsed_result.get('rows', []))} 行数据")
            
            if not parsed_result.get('rows') or len(parsed_result['rows']) == 0:
                logger.error("❌ MD文件中没有找到有效的表格数据")
                return {
                    "success": False,
                    "error": "MD文件中没有找到有效的表格数据",
                    "stage": "md_parsing"
                }
            
            # 将解析结果转换为API数据格式
            logger.info("🔄 将解析结果转换为API数据格式...")
            api_data = self._convert_md_to_api_data(parsed_result)
            logger.info(f"✅ 转换完成，数据包含 {len(api_data)} 个字段")
            
            # 清理和验证数据
            logger.info("🧹 清理和验证数据...")
            cleaned_data = prepare_api_data(api_data)
            logger.info(f"✅ 数据清理完成，清理后数据: {len(cleaned_data)} 个字段")
            
            # 生成输出文件路径
            base_name = Path(filename).stem
            output_filename = f"{base_name}_output_{timestamp}.xlsx"
            output_path = self.output_dir / output_filename
            logger.info(f"📄 输出文件路径: {output_path}")
            
            # 使用Excel写入器处理数据
            logger.info("📝 开始生成Excel文件...")
            excel_result = self.excel_writer.process_api_data(
                cleaned_data, 
                TRIAL_BALANCE_MAPPING, 
                str(output_path)
            )
            logger.info(f"📊 Excel写入完成，状态: {excel_result['status']}")
            
            # 计算统计信息
            successful_writes = sum(1 for status in excel_result["write_status"].values() 
                                  if status == "success")
            total_fields = len(TRIAL_BALANCE_MAPPING)
            
            # 准备返回结果
            result = {
                "success": excel_result["status"] in ["success", "partial_success"],
                "timestamp": timestamp,
                "input_filename": filename,
                "output_filename": output_filename,
                "output_path": str(output_path),
                "stage": "completed",
                
                # MD解析信息
                "md_parsing": {
                    "headers": parsed_result.get('headers', []),
                    "rows_count": len(parsed_result.get('rows', [])),
                    "metadata": parsed_result.get('metadata', {})
                },
                
                # Excel写入信息
                "excel_writing": {
                    "status": excel_result["status"],
                    "total_fields": total_fields,
                    "successful_writes": successful_writes,
                    "success_rate": f"{(successful_writes/total_fields)*100:.1f}%",
                    "write_status": excel_result["write_status"],
                    "mapping_valid": excel_result["mapping_valid"]
                },
                
                # 错误信息
                "errors": excel_result.get("errors", [])
            }
            
            if result["success"]:
                logger.info(f"处理成功完成: {output_filename}")
                logger.info(f"Excel写入成功率: {result['excel_writing']['success_rate']}")
            else:
                logger.warning(f"处理部分成功或失败: {excel_result['status']}")
            
            return result
            
        except Exception as e:
            error_msg = f"处理MD内容时发生错误: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "stage": "processing",
                "timestamp": timestamp
            }
    
    def process_md_file(self, md_file_path: str) -> Dict[str, Any]:
        """
        处理MD文件
        
        参数:
            md_file_path: MD文件路径
            
        返回:
            处理结果字典
        """
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = Path(md_file_path).name
            return self.process_md_content(content, filename)
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"找不到MD文件: {md_file_path}",
                "stage": "file_reading"
            }
        except UnicodeDecodeError:
            return {
                "success": False,
                "error": f"MD文件编码错误，请确保文件为UTF-8编码: {md_file_path}",
                "stage": "file_reading"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"读取MD文件时发生错误: {str(e)}",
                "stage": "file_reading"
            }
    
    def _convert_md_to_api_data(self, parsed_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        将MD解析结果转换为API数据格式
        使用完整的财务字段映射逻辑
        
        参数:
            parsed_result: MD解析结果
            
        返回:
            API数据格式字典
        """
        api_data = {}
        rows = parsed_result.get('rows', [])
        capital_stock_count = 0  # 用于区分两个資本金
        
        logger.info(f"开始转换MD解析结果，共有 {len(rows)} 行数据")
        
        # 根据实际的MD表格结构来映射数据
        if rows:
            for i, row in enumerate(rows):
                # 表格格式：['', '前月残高', '借方金額', '貸方金額', '当月残高', '構成比']
                # 第一列（空列名）包含科目名称，当月残高列包含我们需要的数值
                subject_name = None
                value = None
                
                # 查找科目名称和数值
                for key, val in row.items():
                    if key == '' and val:  # 第一列（空列名）包含科目名称
                        subject_name = val
                    elif key == '当月残高' and val is not None:  # 当月残高列包含数值
                        value = val
                
                if subject_name:
                    # 清理科目名称
                    subject_name = self._clean_subject_name(str(subject_name))
                    
                    if not subject_name:
                        continue
                    
                    # 特殊处理資本金（出现两次）
                    if subject_name == "資本金":
                        capital_stock_count += 1
                        if capital_stock_count == 1:
                            field_name = "capital_stock"
                        else:
                            field_name = "capital_stock_duplicate"
                    # 其他特殊处理和映射
                    elif subject_name == "流動資産合計":
                        field_name = "current_assets_total"
                    elif subject_name == "固定資産合計" or subject_name == "固定資產合計":
                        field_name = "fixed_assets_total"
                    elif subject_name == "流動負債合計":
                        field_name = "current_liabilities_total"
                    elif subject_name == "固定負債合計":
                        field_name = "fixed_liabilities_total"
                    elif subject_name == "負債の部合計":
                        field_name = "total_liabilities"
                    elif subject_name == "資本金合計":
                        field_name = "capital_stock_duplicate"
                    elif subject_name in ["資本剰余金合計", "資本剩余金合計"]:
                        field_name = "capital_surplus_total"
                    elif subject_name == "利益剰余金合計":
                        field_name = "retained_earnings_total"
                    elif subject_name == "株主資本合計":
                        field_name = "shareholders_equity_total"
                    elif subject_name == "純資産の部合計":
                        field_name = "net_assets_total"
                    elif subject_name in ["負債·純資産の部合計", "負債・純資産の部合計"]:
                        field_name = "total_liabilities_and_equity"
                    else:
                        # 使用完整映射查找对应的JSON字段名
                        field_name = self.japanese_to_field_mapping.get(subject_name)
                    
                    if field_name and value is not None:
                        # 解析数值
                        if isinstance(value, str):
                            parsed_value = self._parse_numeric_value(value)
                        else:
                            parsed_value = float(value) if value != 0 else 0.0
                        
                        api_data[field_name] = parsed_value
                        logger.debug(f"行 {i+1}: {subject_name} -> {field_name} = {parsed_value}")
                    else:
                        if not field_name:
                            logger.debug(f"行 {i+1}: 未找到映射 - {subject_name}")
                        if value is None:
                            logger.debug(f"行 {i+1}: 未找到数值 - {subject_name}")
        
        logger.info(f"转换完成，成功映射 {len(api_data)} 个字段")
        logger.debug(f"转换的API数据: {json.dumps(api_data, ensure_ascii=False, indent=2)}")
        return api_data
    
    def _parse_numeric_value(self, value_str: str) -> float:
        """
        解析数值字符串
        
        参数:
            value_str: 数值字符串（可能包含逗号、负号等）
            
        返回:
            解析后的浮点数
        """
        if not value_str or str(value_str).strip() == "":
            return 0.0
            
        # 去除空格
        value_str = str(value_str).strip()
        
        # 处理负数（可能是负号开头）
        is_negative = value_str.startswith('-') or value_str.startswith('−')
        
        # 去除所有非数字字符（保留小数点）
        import re
        value_str = re.sub(r'[^0-9.-]', '', value_str)
        
        try:
            value = float(value_str)
            return -abs(value) if is_negative else value
        except ValueError:
            logger.warning(f"无法解析数值: {value_str}")
            return 0.0
    
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
            "繰越利益剩余金": "retained_earnings",  # 添加留存收益映射
            # 中文映射（保留原有的映射）
            "现金": "cash",
            "银行存款": "ordinary_deposits", 
            "现金及存款合计": "cash_and_deposits_total",
            "现金及预金合计": "cash_and_deposits_total",
            "应收账款": "accounts_receivable",
            "应收票据": "notes_receivable",
            "其他应收款": "other_receivables",
            "应收债权合计": "receivables_total",
            "库存": "inventory",
            "库存商品": "inventory",
            "其他流动资产": "other_current_assets",
            "流动资产合计": "current_assets_total",
            "建筑物": "buildings",
            "机械设备": "machinery_equipment",
            "车辆": "vehicles",
            "有形固定资产合计": "tangible_fixed_assets_total",
            "投资有价证券": "investment_securities",
            "投资其他资产合计": "investment_assets_total",
            "固定资产合计": "fixed_assets_total",
            "资产合计": "total_assets",
            "总资产": "total_assets",
            "应付账款": "accounts_payable",
            "应付票据": "notes_payable",
            "短期借款": "short_term_loans",
            "其他流动负债": "other_current_liabilities",
            "流动负债合计": "current_liabilities_total",
            "长期借款": "long_term_loans",
            "固定负债合计": "fixed_liabilities_total",
            "负债合计": "total_liabilities",
            "总负债": "total_liabilities",
            "资本金": "capital_stock",
            "资本公积": "capital_surplus",
            "利润公积": "retained_earnings",
            "股东权益合计": "shareholders_equity_total",
            "纯资产合计": "net_assets_total",
            "负债及资本合计": "total_liabilities_and_equity",
            "负债和权益合计": "total_liabilities_and_equity"
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
    
    def _map_md_field_to_api_field(self, md_field: str) -> Optional[str]:
        """
        将MD表格字段名映射到API字段名
        
        参数:
            md_field: MD表格中的字段名
            
        返回:
            对应的API字段名，如果没有映射则返回None
        """
        # 构建完整的日文到英文映射（如果还没有构建）
        if not hasattr(self, 'japanese_to_field_mapping'):
            self.japanese_to_field_mapping = self._build_japanese_mapping()
            logger.info(f"已构建 {len(self.japanese_to_field_mapping)} 个日文到字段的映射")
        
        # 清理字段名
        cleaned_field = self._clean_subject_name(md_field)
        
        # 先尝试直接匹配
        if cleaned_field in self.japanese_to_field_mapping:
            return self.japanese_to_field_mapping[cleaned_field]
        
        # 如果没有直接匹配，尝试模糊匹配
        for key, value in self.japanese_to_field_mapping.items():
            if key in cleaned_field or cleaned_field in key:
                return value
        
        # 如果都没有匹配，返回None
        logger.debug(f"未找到字段映射: {md_field} (清理后: {cleaned_field})")
        return None
    
    def get_output_file(self, output_filename: str) -> Optional[str]:
        """
        获取输出文件的完整路径
        
        参数:
            output_filename: 输出文件名
            
        返回:
            完整文件路径，如果文件不存在返回None
        """
        file_path = self.output_dir / output_filename
        return str(file_path) if file_path.exists() else None


def main():
    """测试MD到Excel处理功能"""
    processor = MDToExcelProcessor()
    
    # 测试内容
    test_content = """
# 资产负债表

| 科目 | 金额 |
|------|------|
| 现金 | 1000000 |
| 银行存款 | 5000000 |
| 应收账款 | 2000000 |
| 库存商品 | 3000000 |
| 流动资产合计 | 11000000 |
| 建筑物 | 8000000 |
| 机械设备 | 2000000 |
| 固定资产合计 | 10000000 |
| 总资产 | 21000000 |
"""
    
    try:
        result = processor.process_md_content(test_content, "test.md")
        
        print("\n=== MD到Excel处理结果 ===")
        print(f"✅ 处理状态: {'成功' if result['success'] else '失败'}")
        
        if result['success']:
            print(f"📄 输出文件: {result['output_filename']}")
            print(f"📊 MD解析: {result['md_parsing']['rows_count']} 行数据")
            print(f"📈 Excel写入: {result['excel_writing']['success_rate']}")
        else:
            print(f"❌ 错误: {result.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    main()