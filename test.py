#!/usr/bin/env python3
"""
ExcelSync测试脚本
简单测试JSON到Excel的功能
"""

import json
from pathlib import Path
from excel_sync import ExcelSync

def main():
    """测试ExcelSync功能"""
    print("=== ExcelSync 测试 ===")
    
    # 检查JSON文件是否存在
    json_file = "sample_api_data.json"
    if not Path(json_file).exists():
        print(f"❌ 错误: 找不到测试文件 '{json_file}'")
        print("请确保sample_api_data.json文件存在")
        return 1
    
    # 显示要测试的数据
    print(f"📁 使用测试文件: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📊 测试数据包含 {len(data)} 个字段")
        
        # 显示前几个字段作为示例
        print("📋 数据示例:")
        for i, (key, value) in enumerate(data.items()):
            if i < 5:  # 只显示前5个字段
                print(f"   {key}: {value}")
            elif i == 5:
                print(f"   ... 以及其他 {len(data)-5} 个字段")
                break
                
    except Exception as e:
        print(f"❌ 读取测试文件出错: {e}")
        return 1
    
    # 执行测试
    print("\n🔄 开始测试...")
    sync = ExcelSync()
    result = sync.sync_from_json_file(json_file)
    
    # 显示结果
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
    
    print("\n✨ 测试完成!")
    return 0

if __name__ == "__main__":
    exit(main())