#!/usr/bin/env python3
"""
ExcelSync项目的主模块
简单实现：JSON输入 → Excel输出
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import shutil

from excel_writer import ExcelWriter
from data_validator import prepare_api_data
from mapping_config import TRIAL_BALANCE_MAPPING

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('excel_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ExcelSync:
    """
    简单的JSON到Excel同步器
    """
    
    def __init__(self, excel_path: str = "mapping.xlsx", sheet_name: str = "A社貼り付けBS"):
        """
        初始化ExcelSync
        
        参数:
            excel_path: Excel文件路径
            sheet_name: 工作表名称
        """
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.writer = ExcelWriter(excel_path, sheet_name)
        
        # 创建输出文件夹
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def sync_from_json_file(self, json_path: str) -> Dict[str, Any]:
        """
        从JSON文件读取数据并写入Excel
        
        参数:
            json_path: JSON文件路径
            
        返回:
            同步结果字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 读取JSON数据
            logger.info(f"读取JSON文件: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                api_data = json.load(f)
            
            # 清理数据
            logger.info("清理数据...")
            cleaned_data = prepare_api_data(api_data)
            
            # 创建输出文件路径
            output_filename = f"mapping_output_{timestamp}.xlsx"
            output_path = self.output_dir / output_filename
            
            # 备份原文件到输出文件夹
            backup_filename = f"mapping_backup_{timestamp}.xlsx"
            backup_path = self.output_dir / backup_filename
            shutil.copy2(self.excel_path, backup_path)
            logger.info(f"已创建备份: {backup_path}")
            
            # 写入数据到输出文件
            logger.info("写入数据到Excel...")
            result = self.writer.process_api_data(cleaned_data, TRIAL_BALANCE_MAPPING, str(output_path))
            
            # 计算成功率
            successful_writes = sum(1 for status in result["write_status"].values() 
                                  if status == "success")
            total_fields = len(TRIAL_BALANCE_MAPPING)
            
            result.update({
                "timestamp": timestamp,
                "json_file": json_path,
                "output_file": str(output_path),
                "backup_file": str(backup_path),
                "total_fields": total_fields,
                "successful_writes": successful_writes,
                "success_rate": f"{(successful_writes/total_fields)*100:.1f}%"
            })
            
            if successful_writes == total_fields:
                logger.info(f"同步成功完成: {successful_writes}/{total_fields} 字段已写入")
                logger.info(f"输出文件: {output_path}")
            else:
                logger.warning(f"同步部分完成: {successful_writes}/{total_fields} 字段已写入")
            
            return result
            
        except FileNotFoundError:
            error_msg = f"找不到JSON文件: {json_path}"
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}
        except json.JSONDecodeError as e:
            error_msg = f"JSON文件格式错误: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}
        except Exception as e:
            error_msg = f"同步失败: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}


def main():
    """单一主函数 - 从JSON文件同步到Excel"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ExcelSync - 简单的JSON到Excel数据同步工具")
    parser.add_argument("json_file", help="包含数据的JSON文件路径")
    parser.add_argument("--excel", default="mapping.xlsx", help="Excel文件路径")
    parser.add_argument("--sheet", default="A社貼り付けBS", help="工作表名称")
    
    args = parser.parse_args()
    
    # 检查JSON文件是否存在
    if not Path(args.json_file).exists():
        print(f"错误: 找不到JSON文件 '{args.json_file}'")
        return 1
    
    # 执行同步
    sync = ExcelSync(args.excel, args.sheet)
    result = sync.sync_from_json_file(args.json_file)
    
    # 输出结果
    print("\n=== 同步结果 ===")
    if result["status"] == "success":
        print(f"✅ 成功: {result['success_rate']} ({result['successful_writes']}/{result['total_fields']} 字段)")
        print(f"📄 输出文件: {result['output_file']}")
        print(f"🔄 备份文件: {result['backup_file']}")
    elif result["status"] == "partial_success":
        print(f"⚠️  部分成功: {result['success_rate']} ({result['successful_writes']}/{result['total_fields']} 字段)")
        print(f"📄 输出文件: {result['output_file']}")
        print(f"🔄 备份文件: {result['backup_file']}")
    else:
        print(f"❌ 失败: {result.get('error', '未知错误')}")
    
    return 0 if result["status"] in ["success", "partial_success"] else 1


if __name__ == "__main__":
    exit(main())