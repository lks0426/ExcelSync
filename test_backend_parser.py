#!/usr/bin/env python3
"""
测试后端MD解析器的HTML表格支持
演示web界面现在可以成功解析用户的HTML表格MD文件
"""

from backend.md_parser import MDParser
import json

def main():
    """测试后端解析器对HTML表格的支持"""
    print("=== Backend MD Parser HTML Table Support Test ===")
    
    parser = MDParser()
    
    # 1. 测试用户的MD文件
    print("\n🔄 Step 1: Testing user's MD file...")
    try:
        result = parser.parse_file('test_new.md')
        print(f"✅ Successfully parsed user MD file")
        print(f"📊 Table type: {result['metadata']['type']}")  
        print(f"📋 Headers: {result['headers']}")
        print(f"📄 Rows count: {len(result['rows'])}")
        
        # 显示前5行数据结构
        print("\n📝 Sample parsed data (first 5 rows):")
        for i, row in enumerate(result['rows'][:5]):
            print(f"  Row {i+1}: {row}")
            
        print(f"\n💡 The web interface can now process this HTML table format!")
        
    except Exception as e:
        print(f"❌ Failed to parse user MD file: {str(e)}")
        return False
        
    # 2. 对比：测试Markdown格式的表格
    print("\n🔄 Step 2: Testing Markdown table format for comparison...")
    
    markdown_table = """
| 項目 | 前月残高 | 借方金額 | 貸方金額 |
|------|----------|----------|----------|
| 現金 | 58,013 | 0 | 0 |
| 普通預金 | 50,709,138 | 28,700,448 | 26,365,776 |
"""
    
    try:
        result = parser.parse(markdown_table)
        print(f"✅ Successfully parsed Markdown table")
        print(f"📊 Table type: {result['metadata']['type']}")
        print(f"📋 Headers: {result['headers']}")
        print(f"📄 Rows count: {len(result['rows'])}")
        
    except Exception as e:
        print(f"❌ Failed to parse Markdown table: {str(e)}")
        return False
    
    print("\n✨ Both HTML and Markdown table formats are now supported!")
    print("🌐 The web interface parsing error should be resolved.")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)