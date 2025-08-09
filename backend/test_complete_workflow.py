#!/usr/bin/env python3
"""
测试完整的MD到Excel工作流程
"""

import requests
import json
import io
import tempfile
from pathlib import Path

# API配置
API_BASE_URL = "http://localhost:8001"

def test_complete_workflow():
    """测试完整的MD到Excel工作流程"""
    print("🚀 测试完整MD到Excel工作流程")
    print("=" * 50)
    
    # 测试MD内容
    test_md_content = """# 财务报表测试

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
        # 1. 测试从文本生成Excel
        print("🔍 步骤1: 从MD文本生成Excel...")
        response = requests.post(
            f"{API_BASE_URL}/api/generate-excel-text",
            json={
                "content": test_md_content,
                "filename": "test_balance_sheet.md"
            }
        )
        
        if response.status_code != 200:
            print(f"❌ 生成Excel失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
        
        result = response.json()
        if not result['success']:
            print(f"❌ 生成Excel失败: {result.get('error', 'Unknown error')}")
            return False
        
        data = result['data']
        print(f"✅ Excel文件生成成功")
        print(f"📄 输出文件: {data['output_filename']}")
        print(f"📊 MD解析: {data['md_parsing']['rows_count']} 行, {len(data['md_parsing']['headers'])} 列")
        print(f"📈 Excel写入成功率: {data['excel_writing']['success_rate']}")
        
        # 2. 测试下载Excel文件
        print("\n🔍 步骤2: 下载生成的Excel文件...")
        download_response = requests.get(f"{API_BASE_URL}{data['download_url']}")
        
        if download_response.status_code != 200:
            print(f"❌ 下载文件失败: {download_response.status_code}")
            return False
        
        # 保存文件到临时目录进行验证
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            temp_file.write(download_response.content)
            temp_path = temp_file.name
        
        file_size = len(download_response.content)
        print(f"✅ 文件下载成功")
        print(f"📦 文件大小: {file_size} 字节")
        print(f"📍 临时文件: {temp_path}")
        
        # 3. 测试文件上传方式
        print("\n🔍 步骤3: 测试文件上传方式...")
        
        # 创建临时MD文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
            temp_md.write(test_md_content)
            temp_md_path = temp_md.name
        
        # 上传文件
        with open(temp_md_path, 'rb') as f:
            files = {'file': ('test.md', f, 'text/markdown')}
            upload_response = requests.post(
                f"{API_BASE_URL}/api/generate-excel",
                files=files
            )
        
        if upload_response.status_code != 200:
            print(f"❌ 文件上传失败: {upload_response.status_code}")
            print(f"响应: {upload_response.text}")
            return False
        
        upload_result = upload_response.json()
        if not upload_result['success']:
            print(f"❌ 文件上传失败: {upload_result.get('error', 'Unknown error')}")
            return False
        
        upload_data = upload_result['data']
        print(f"✅ 文件上传和处理成功")
        print(f"📄 输出文件: {upload_data['output_filename']}")
        print(f"📈 Excel写入成功率: {upload_data['excel_writing']['success_rate']}")
        
        # 清理临时文件
        Path(temp_path).unlink()
        Path(temp_md_path).unlink()
        
        print("\n" + "=" * 50)
        print("🎉 完整工作流程测试成功！")
        print("✅ MD解析 → Excel生成 → 文件下载 全部正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        return False

def test_health_check():
    """测试健康检查"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接后端服务: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🧪 ExcelSync 完整工作流程测试")
    print("=" * 60)
    
    # 健康检查
    if not test_health_check():
        print("\n请先启动后端服务器: python run.py")
        return 1
    
    print()
    
    # 完整工作流程测试
    if test_complete_workflow():
        print("\n🏆 所有测试通过！系统工作正常")
        return 0
    else:
        print("\n💥 测试失败，请检查系统配置")
        return 1

if __name__ == "__main__":
    exit(main())