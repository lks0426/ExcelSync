#!/usr/bin/env python3
"""
MarkdownSync Backend Server
启动脚本：简化版MD解析服务器
"""

from app import app

if __name__ == '__main__':
    print("🚀 Starting MarkdownSync Backend Server...")
    print("📝 Supports: .md, .markdown, .txt files")
    print("🌐 Server running at: http://localhost:8001")
    print("📊 API Endpoints:")
    print("   - POST /api/parse-md (single file)")
    print("   - POST /api/parse-multiple-md (multiple files)")  
    print("   - POST /api/parse-md-text (text content)")
    print("   - GET  /api/sample-md (sample content)")
    print("   - GET  /api/health (health check)")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8001)