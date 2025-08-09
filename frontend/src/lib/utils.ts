import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export function validateMDFile(file: File): { valid: boolean; error?: string } {
  const validExtensions = ['.md', '.markdown', '.txt']
  const fileName = file.name.toLowerCase()
  
  // 检查文件扩展名
  const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext))
  
  // 如果MIME类型不正确但扩展名正确，也允许（因为有些系统MIME类型设置不准确）
  const validTypes = [
    'text/markdown',
    'text/x-markdown',
    'text/plain',
    'application/octet-stream' // 有时MD文件会被识别为这个类型
  ]

  if (!hasValidExtension && !validTypes.includes(file.type)) {
    return {
      valid: false,
      error: 'Please upload a valid Markdown file (.md, .markdown) or text file (.txt).'
    }
  }

  // Max file size: 16MB
  const maxSize = 16 * 1024 * 1024
  if (file.size > maxSize) {
    return {
      valid: false,
      error: 'File size must be less than 16MB.'
    }
  }

  return { valid: true }
}

// 为了兼容性保留原函数名
export const validateExcelFile = validateMDFile

export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}