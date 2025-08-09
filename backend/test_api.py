#!/usr/bin/env python3
"""
测试API接口功能
"""

import requests
import json
import io
from pathlib import Path

# API配置
API_BASE_URL = "http://localhost:8001"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

def test_parse_md_text():
    """测试解析MD文本内容接口"""
    print("\n🔍 测试解析MD文本内容接口...")
    
    test_content = """
# 员工信息表

| 姓名 | 部门 | 工资 | 入职时间 |
|------|------|------|----------|
| 张三 | 技术部 | 15000 | 2023-01-15 |
| 李四 | 销售部 | 12000 | 2023-02-20 |
| 王五 | 财务部 | 13000 | 2023-03-10 |
"""
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/parse-md-text",
            json={
                "content": test_content,
                "filename": "test.md"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 文本解析成功")
            print(f"📊 表头: {data['data']['headers']}")
            print(f"📄 数据行数: {len(data['data']['data'])}")
            print(f"📝 示例数据: {data['data']['data'][0]}")
            return True
        else:
            print(f"❌ 文本解析失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 文本解析异常: {str(e)}")
        return False

def test_sample_md():
    """测试获取示例MD内容接口"""
    print("\n🔍 测试获取示例MD内容接口...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/sample-md")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取示例内容成功")
            print(f"📄 文件名: {data['filename']}")
            print(f"📝 内容长度: {len(data['content'])} 字符")
            return True
        else:
            print(f"❌ 获取示例内容失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 获取示例内容异常: {str(e)}")
        return False

def create_test_md_file():
    """创建测试MD文件"""
    content = """# 测试产品清单

| 产品ID | 产品名称 | 单价 | 数量 | 总价 |
|--------|----------|------|------|------|
| P001 | 笔记本电脑 | 5999.99 | 10 | 59999.9 |
| P002 | 无线鼠标 | 199.5 | 50 | 9975 |
| P003 | 机械键盘 | 599 | 30 | 17970 |
| P004 | 显示器 | 2999 | 5 | 14995 |
"""
    
    with open('test_products.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return 'test_products.md'

def test_parse_md_file():
    """测试解析MD文件接口"""
    print("\n🔍 测试解析MD文件接口...")
    
    # 创建测试文件
    test_file = create_test_md_file()
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'text/markdown')}
            response = requests.post(
                f"{API_BASE_URL}/api/parse-md",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 文件解析成功")
            print(f"📊 表头: {data['data']['headers']}")
            print(f"📄 数据行数: {data['data']['summary']['totalRows']}")
            print(f"📝 示例数据: {data['data']['data'][0] if data['data']['data'] else 'No data'}")
            return True
        else:
            print(f"❌ 文件解析失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 文件解析异常: {str(e)}")
        return False
    finally:
        # 清理测试文件
        try:
            Path(test_file).unlink()
        except:
            pass

def main():
    """运行所有测试"""
    print("🚀 开始测试MarkdownSync API接口")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_sample_md,
        test_parse_md_text,
        test_parse_md_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！API接口工作正常")
    else:
        print("⚠️  部分测试失败，请检查服务器状态")

if __name__ == "__main__":
    main()