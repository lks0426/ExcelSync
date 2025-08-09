#!/usr/bin/env python3
"""
MD文件到Excel的测试脚本
读取MD格式的财务报表，转换为JSON，然后写入Excel
"""

import json
from pathlib import Path
from excel_sync import ExcelSync
from md_parser import MDFinancialParser
import tempfile
import os


def main():
    """测试MD到Excel的完整流程"""
    print("=== MD到Excel测试 ===")
    
    # 检查MD文件是否存在
    md_file = "test_new.md"
    if not Path(md_file).exists():
        print(f"❌ 错误: 找不到MD文件 '{md_file}'")
        return 1
    
    print(f"📁 使用MD文件: {md_file}")
    
    try:
        # 1. 解析MD文件
        print("\n🔄 步骤1: 解析MD文件...")
        parser = MDFinancialParser()
        financial_data = parser.parse_md_file(md_file)
        
        print(f"✅ 成功解析MD文件")
        print(f"📊 提取了 {len(financial_data)} 个字段")
        
        # 显示部分数据作为示例
        print("📋 数据示例:")
        for i, (key, value) in enumerate(financial_data.items()):
            if i < 5:
                print(f"   {key}: {value}")
            elif i == 5:
                print(f"   ... 以及其他 {len(financial_data)-5} 个字段")
                break
        
        # 2. 创建临时JSON文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, 
                                       dir='.', prefix='temp_financial_') as tmp_file:
            json.dump(financial_data, tmp_file, ensure_ascii=False, indent=2)
            temp_json_path = tmp_file.name
        
        print(f"\n🔄 步骤2: 创建临时JSON文件: {temp_json_path}")
        
        # 3. 使用ExcelSync处理数据
        print("\n🔄 步骤3: 写入Excel...")
        sync = ExcelSync()
        result = sync.sync_from_json_file(temp_json_path)
        
        # 4. 清理临时文件
        os.unlink(temp_json_path)
        print(f"🧹 已清理临时文件")
        
        # 5. 显示结果
        print("\n=== 测试结果 ===")
        if result["status"] == "success":
            print(f"✅ 测试成功!")
            print(f"📊 成功率: {result['success_rate']} ({result['successful_writes']}/{result['total_fields']} 字段)")
            print(f"📄 输出文件: {result['output_file']}")
            print(f"🔄 备份文件: {result['backup_file']}")
            print("\n💡 提示: 检查output文件夹查看生成的Excel文件")
        elif result["status"] == "partial_success":
            print(f"⚠️  测试部分成功")
            print(f"📊 成功率: {result['success_rate']} ({result['successful_writes']}/{result['total_fields']} 字段)")
            print(f"📄 输出文件: {result['output_file']}")
            print(f"🔄 备份文件: {result['backup_file']}")
            
            # 显示失败的字段
            failed_fields = [field for field, status in result["write_status"].items() 
                            if status != "success"]
            if failed_fields:
                print(f"❌ 失败字段: {failed_fields}")
        else:
            print(f"❌ 测试失败: {result.get('error', '未知错误')}")
            return 1
        
        print("\n✨ MD到Excel转换完成!")
        return 0
        
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())