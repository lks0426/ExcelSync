import { ApiResponse, ExcelParseResponse } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `HTTP error! status: ${response.status}`,
        }
      }

      return {
        success: true,
        data: data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'An unexpected error occurred',
      }
    }
  }

  async uploadAndParseExcel(file: File): Promise<ApiResponse<ExcelParseResponse>> {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE_URL}/api/parse-md`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `Upload failed: ${response.status}`,
        }
      }

      return {
        success: true,
        data: data.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      }
    }
  }

  async parseMultipleExcel(files: File[]): Promise<ApiResponse<ExcelParseResponse[]>> {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })

    try {
      const response = await fetch(`${API_BASE_URL}/api/parse-multiple-md`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `Batch upload failed: ${response.status}`,
        }
      }

      return {
        success: true,
        data: data.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Batch upload failed',
      }
    }
  }

  // 新增：解析MD文本内容的方法
  async parseMDText(content: string, filename: string = 'untitled.md'): Promise<ApiResponse<ExcelParseResponse>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/parse-md-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          filename
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `Parse failed: ${response.status}`,
        }
      }

      return {
        success: true,
        data: data.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Parse failed',
      }
    }
  }

  // 新增：获取示例MD内容
  async getSampleMD(): Promise<ApiResponse<{ content: string; filename: string }>> {
    return this.request<{ content: string; filename: string }>('/api/sample-md')
  }

  // 新增：生成Excel文件（支持单文件）
  async generateExcel(file: File): Promise<ApiResponse<{
    output_filename: string;
    download_url: string;
    md_parsing: any;
    excel_writing: any;
    timestamp: string;
  }>> {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-excel`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `Excel generation failed: ${response.status}`,
          error_code: data.error_code,
        }
      }

      // 处理多文件响应格式，取第一个结果
      if (data.data && data.data.results && data.data.results.length > 0) {
        return {
          success: true,
          data: data.data.results[0],
        }
      }

      return {
        success: true,
        data: data.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Excel generation failed',
      }
    }
  }

  // 新增：批量生成Excel文件
  async generateMultipleExcel(files: File[]): Promise<ApiResponse<{
    results: Array<{
      filename: string;
      output_filename: string;
      download_url: string;
      md_parsing: any;
      excel_writing: any;
      timestamp: string;
    }>;
    errors: Array<{
      filename: string;
      error: string;
      error_code: string;
      stage?: string;
    }>;
    summary: {
      total_files: number;
      success_count: number;
      error_count: number;
    };
  }>> {
    console.log('🚀 [API] 开始生成Excel - 文件数量:', files.length)
    
    const formData = new FormData()
    files.forEach((file, index) => {
      console.log(`📁 [API] 添加文件 ${index + 1}: ${file.name} (${file.size} bytes)`)
      formData.append('files', file)
    })

    try {
      console.log('📤 [API] 发送请求到:', `${API_BASE_URL}/api/generate-excel`)
      const startTime = Date.now()
      
      const response = await fetch(`${API_BASE_URL}/api/generate-excel`, {
        method: 'POST',
        body: formData,
      })

      const requestDuration = Date.now() - startTime
      console.log(`⏱️ [API] 请求耗时: ${requestDuration}ms`)
      console.log('📥 [API] 响应状态:', response.status, response.statusText)

      const data = await response.json()
      console.log('📋 [API] 响应数据:', JSON.stringify(data, null, 2))

      if (!response.ok && !data.data?.results?.length) {
        console.error('❌ [API] 请求失败:', {
          status: response.status,
          error: data.error,
          error_code: data.error_code
        })
        return {
          success: false,
          error: data.error || `Excel generation failed: ${response.status}`,
          error_code: data.error_code,
        }
      }

      const success = data.success || (data.data?.results?.length > 0)
      console.log(`✅ [API] 请求${success ? '成功' : '失败'}:`, {
        success,
        resultCount: data.data?.results?.length || 0,
        errorCount: data.data?.errors?.length || 0
      })

      return {
        success,
        data: data.data,
      }
    } catch (error) {
      console.error('💥 [API] 网络或解析错误:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Excel generation failed',
      }
    }
  }

  // 新增：从文本内容生成Excel
  async generateExcelFromText(content: string, filename: string = 'untitled.md'): Promise<ApiResponse<{
    output_filename: string;
    download_url: string;
    md_parsing: any;
    excel_writing: any;
    timestamp: string;
  }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-excel-text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          filename
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `Excel generation failed: ${response.status}`,
        }
      }

      return {
        success: true,
        data: data.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Excel generation failed',
      }
    }
  }

  // 新增：下载Excel文件
  async downloadExcel(filename: string): Promise<Blob | null> {
    try {
      console.log('⬇️ [API] 开始下载文件:', filename)
      const startTime = Date.now()
      
      const response = await fetch(`${API_BASE_URL}/api/download-excel/${filename}`)
      
      const downloadDuration = Date.now() - startTime
      console.log(`⏱️ [API] 下载请求耗时: ${downloadDuration}ms`)
      console.log('📥 [API] 下载响应状态:', response.status, response.statusText)
      
      if (!response.ok) {
        console.error('❌ [API] 下载失败:', response.status, response.statusText)
        throw new Error(`Download failed: ${response.status}`)
      }

      const blob = await response.blob()
      console.log('✅ [API] 文件下载成功:', {
        filename,
        size: blob.size,
        type: blob.type
      })
      
      return blob
    } catch (error) {
      console.error('💥 [API] 下载错误:', error)
      return null
    }
  }

  // Health check endpoint
  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    return this.request<{ status: string; timestamp: string }>('/api/health')
  }
}

export const apiService = new ApiService()

// Mock API service for development
export class MockApiService {
  private delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  async uploadAndParseExcel(file: File): Promise<ApiResponse<ExcelParseResponse>> {
    await this.delay(2000) // Simulate API delay

    // Mock successful response for MD file parsing
    return {
      success: true,
      data: {
        headers: ['产品名称', '型号', '价格', '库存', '类别'],
        data: [
          { '产品名称': '笔记本电脑', '型号': 'XPS-15', '价格': 12999, '库存': 50, '类别': '电子产品' },
          { '产品名称': '无线鼠标', '型号': 'M705', '价格': 299, '库存': 200, '类别': '配件' },
          { '产品名称': '机械键盘', '型号': 'K870', '价格': 599, '库存': 150, '类别': '配件' },
          { '产品名称': '显示器', '型号': 'U2720Q', '价格': 3999, '库存': 30, '类别': '电子产品' },
          { '产品名称': 'USB集线器', '型号': 'H7', '价格': 199, '库存': 300, '类别': '配件' },
        ],
        summary: {
          totalRows: 5,
          totalColumns: 5,
          fileName: file.name,
          fileSize: file.size,
          parsedAt: new Date().toISOString()
        },
        metadata: {
          type: 'markdown_table',
          encoding: 'utf-8',
          hasHeaders: true
        }
      }
    }
  }

  async parseMultipleExcel(files: File[]): Promise<ApiResponse<ExcelParseResponse[]>> {
    await this.delay(3000) // Simulate longer delay for multiple files

    const results = await Promise.all(
      files.map(async (file) => {
        const response = await this.uploadAndParseExcel(file)
        return response.data!
      })
    )

    return {
      success: true,
      data: results
    }
  }

  // Mock版本的generateExcel方法
  async generateExcel(file: File): Promise<ApiResponse<{
    output_filename: string;
    download_url: string;
    md_parsing: any;
    excel_writing: any;
    timestamp: string;
  }>> {
    await this.delay(3000) // Simulate Excel generation delay

    const timestamp = new Date().toISOString().replace(/[-:T]/g, '').split('.')[0]
    const filename = `${file.name.replace('.md', '')}_output_${timestamp}.xlsx`

    return {
      success: true,
      data: {
        output_filename: filename,
        download_url: `/api/download-excel/${filename}`,
        md_parsing: {
          headers: ['科目', '金额'],
          rows_count: 9,
          metadata: { type: 'markdown_table' }
        },
        excel_writing: {
          status: 'success',
          total_fields: 34,
          successful_writes: 8,
          success_rate: '23.5%',
          mapping_valid: true
        },
        timestamp: timestamp
      }
    }
  }

  // Mock版本的generateExcelFromText方法
  async generateExcelFromText(content: string, filename: string = 'untitled.md'): Promise<ApiResponse<{
    output_filename: string;
    download_url: string;
    md_parsing: any;
    excel_writing: any;
    timestamp: string;
  }>> {
    return this.generateExcel(new File([content], filename, { type: 'text/markdown' }))
  }

  // Mock版本的downloadExcel方法
  async downloadExcel(filename: string): Promise<Blob | null> {
    await this.delay(1000)
    
    // 返回一个模拟的Excel文件Blob
    const mockExcelData = new ArrayBuffer(1024) // 1KB的模拟数据
    return new Blob([mockExcelData], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
  }

  // Mock版本的getSampleMD方法
  async getSampleMD(): Promise<ApiResponse<{ content: string; filename: string }>> {
    await this.delay(500)
    
    const sampleContent = `# 资产负债表

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
`

    return {
      success: true,
      data: {
        content: sampleContent,
        filename: 'sample_balance_sheet.md'
      }
    }
  }

  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    await this.delay(500)
    return {
      success: true,
      data: {
        status: 'healthy',
        timestamp: new Date().toISOString()
      }
    }
  }
}

// Use real API service (changed from mock to connect to backend)
export const api = apiService