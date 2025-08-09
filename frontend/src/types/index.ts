export interface UploadedFile {
  id: string
  file: File
  name: string
  size: number
  type: string
  uploadedAt: Date
  status: 'uploading' | 'uploaded' | 'processing' | 'completed' | 'error'
  progress?: number
  error?: string
}

export interface ParsedData {
  headers: string[]
  rows: any[][]
  totalRows: number
  fileName: string
  parsedAt: Date
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  error_code?: string
  message?: string
}

export interface MDParseResponse {
  headers: string[]
  data: Record<string, any>[]
  summary: {
    totalRows: number
    totalColumns: number
    fileName: string
    fileSize: number
    parsedAt?: string
  }
  metadata?: Record<string, any>
}

// 为了兼容性，保留原名称但指向MD解析响应
export type ExcelParseResponse = MDParseResponse

export type Theme = 'light' | 'dark' | 'system'

export interface ThemeConfig {
  theme: Theme
  setTheme: (theme: Theme) => void
}