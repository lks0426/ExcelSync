# MarkdownSync API 接口文档

## 概述

MarkdownSync 后端API提供Markdown文件上传和表格解析功能，将MD文件中的表格转换为结构化的JSON数据。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json` 或 `multipart/form-data`
- **支持格式**: `.md`, `.markdown`, `.txt`
- **最大文件大小**: 16MB

## API接口列表

### 1. 健康检查

**接口**: `GET /api/health`

**描述**: 检查API服务器状态

**请求参数**: 无

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0"
}
```

---

### 2. 生成Excel文件 (文件上传)

**接口**: `POST /api/generate-excel`

**描述**: 上传MD文件并生成包含映射数据的Excel文件

**请求参数**:
- **Content-Type**: `multipart/form-data`
- **file**: File - Markdown文件

**响应示例**:
```json
{
  "success": true,
  "data": {
    "output_filename": "test_output_20240115_103000.xlsx",
    "download_url": "/api/download-excel/test_output_20240115_103000.xlsx",
    "md_parsing": {
      "headers": ["科目", "金额"],
      "rows_count": 9
    },
    "excel_writing": {
      "status": "success",
      "total_fields": 34,
      "successful_writes": 8,
      "success_rate": "23.5%"
    },
    "timestamp": "20240115_103000"
  }
}
```

### 3. 生成Excel文件 (文本内容)

**接口**: `POST /api/generate-excel-text`

**描述**: 从MD文本内容生成Excel文件

**请求参数**:
- **Content-Type**: `application/json`
- **content**: string - Markdown文本内容
- **filename**: string (可选) - 文件名

**响应示例**: 同上

### 4. 下载Excel文件

**接口**: `GET /api/download-excel/{filename}`

**描述**: 下载生成的Excel文件

**请求参数**:
- **filename**: string - Excel文件名

**响应**: Excel文件二进制数据

---

### 2. 解析单个MD文件

**接口**: `POST /api/parse-md`

**描述**: 上传并解析单个Markdown文件中的表格

**请求参数**:
- **Content-Type**: `multipart/form-data`
- **file**: File - Markdown文件

**请求示例**:
```javascript
const formData = new FormData()
formData.append('file', markdownFile)

fetch('/api/parse-md', {
  method: 'POST',
  body: formData
})
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "headers": ["产品名称", "型号", "价格", "库存", "类别"],
    "data": [
      {
        "产品名称": "笔记本电脑",
        "型号": "XPS-15", 
        "价格": 12999,
        "库存": 50,
        "类别": "电子产品"
      }
    ],
    "summary": {
      "totalRows": 5,
      "totalColumns": 5,
      "fileName": "products.md",
      "fileSize": 2048,
      "parsedAt": "2024-01-15T10:30:00.000Z"
    },
    "metadata": {
      "type": "markdown_table",
      "encoding": "utf-8",
      "hasHeaders": true
    }
  }
}
```

**错误响应**:
```json
{
  "success": false,
  "error": "Invalid file type. Only .md, .markdown, and .txt files are allowed"
}
```

---

### 3. 批量解析MD文件

**接口**: `POST /api/parse-multiple-md`

**描述**: 批量上传并解析多个Markdown文件

**请求参数**:
- **Content-Type**: `multipart/form-data`
- **files**: File[] - 多个Markdown文件

**请求示例**:
```javascript
const formData = new FormData()
files.forEach(file => {
  formData.append('files', file)
})

fetch('/api/parse-multiple-md', {
  method: 'POST',
  body: formData
})
```

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "headers": ["产品名称", "价格"],
      "data": [...],
      "summary": {...},
      "metadata": {...}
    }
  ],
  "errors": null,
  "summary": {
    "totalFiles": 3,
    "successCount": 2,
    "errorCount": 1
  }
}
```

---

### 4. 解析MD文本内容

**接口**: `POST /api/parse-md-text`

**描述**: 直接解析Markdown文本内容，无需上传文件

**请求参数**:
- **Content-Type**: `application/json`
- **content**: string - Markdown文本内容
- **filename**: string (可选) - 文件名

**请求示例**:
```javascript
fetch('/api/parse-md-text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: "# 标题\n\n| 列1 | 列2 |\n|-----|-----|\n| 值1 | 值2 |",
    filename: "test.md"
  })
})
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "headers": ["列1", "列2"],
    "data": [{"列1": "值1", "列2": "值2"}],
    "summary": {
      "totalRows": 1,
      "totalColumns": 2,
      "fileName": "test.md",
      "fileSize": 45,
      "parsedAt": "2024-01-15T10:30:00.000Z"
    }
  }
}
```

---

### 5. 获取示例MD内容

**接口**: `GET /api/sample-md`

**描述**: 获取示例Markdown文件内容用于测试

**请求参数**: 无

**响应示例**:
```json
{
  "success": true,
  "content": "# 产品清单\n\n| 产品名称 | 价格 |\n|---------|------|\n| 笔记本 | 5999 |",
  "filename": "sample.md"
}
```

---

## 错误代码说明

| HTTP状态码 | 错误类型 | 说明 |
|-----------|---------|------|
| 400 | Bad Request | 请求参数错误或文件格式不支持 |
| 413 | Request Entity Too Large | 文件大小超过16MB限制 |
| 500 | Internal Server Error | 服务器内部错误 |

## 响应数据结构

### MDParseResponse 结构

```typescript
interface MDParseResponse {
  headers: string[]                    // 表格列名
  data: Record<string, any>[]         // 表格数据行
  summary: {
    totalRows: number                 // 数据行数
    totalColumns: number              // 列数
    fileName: string                  // 文件名
    fileSize: number                  // 文件大小(字节)
    parsedAt: string                 // 解析时间(ISO格式)
  }
  metadata: {                        // 元数据(可选)
    type: string                     // 数据类型
    encoding: string                 // 文件编码
    hasHeaders: boolean              // 是否包含表头
  }
}
```

### ApiResponse 结构

```typescript
interface ApiResponse<T> {
  success: boolean                   // 请求是否成功
  data?: T                          // 响应数据
  error?: string                    // 错误信息
  errors?: Array<{                  // 批量操作错误详情
    file: string
    error: string
  }>
}
```

## 使用示例

### React前端调用示例

```typescript
import { api } from '@/lib/api'

// 单文件上传解析
const handleFileUpload = async (file: File) => {
  try {
    const response = await api.uploadAndParseExcel(file)
    if (response.success) {
      console.log('解析成功:', response.data)
      // 处理解析后的数据
    } else {
      console.error('解析失败:', response.error)
    }
  } catch (error) {
    console.error('请求失败:', error)
  }
}

// 文本内容解析
const handleTextParse = async (content: string) => {
  try {
    const response = await api.parseMDText(content, 'input.md')
    if (response.success) {
      console.log('解析成功:', response.data)
    }
  } catch (error) {
    console.error('解析失败:', error)
  }
}
```

### curl命令行示例

```bash
# 健康检查
curl -X GET http://localhost:8000/api/health

# 上传文件解析
curl -X POST \
  -F "file=@example.md" \
  http://localhost:8000/api/parse-md

# 文本内容解析
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"content":"| 名称 | 价格 |\n|------|------|\n| 商品A | 100 |"}' \
  http://localhost:8000/api/parse-md-text
```

## 部署说明

### 环境要求

- Python 3.8+
- Flask 2.3.3
- Flask-CORS 4.0.0

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务器

```bash
python run.py
```

服务器将在 `http://localhost:8000` 启动。

## 前端集成

前端已经配置好了完整的API调用逻辑，只需要：

1. 启动后端服务器：`python run.py`
2. 启动前端服务器：`npm run dev`
3. 确保前端环境变量配置正确：`NEXT_PUBLIC_API_URL=http://localhost:8000`

前端会自动调用后端API进行MD文件解析和数据展示。