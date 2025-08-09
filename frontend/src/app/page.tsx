'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FileSpreadsheet, Sparkles, Activity } from 'lucide-react'
import { FileUpload } from '@/components/ui/FileUpload'
import { ParseButton } from '@/components/ui/ParseButton'
import { DataPreview } from '@/components/ui/DataPreview'
import { ThemeToggle } from '@/components/ui/ThemeToggle'
import { LanguageSelector } from '@/components/ui/LanguageSelector'
import { UploadedFile, ExcelParseResponse } from '@/types'
import { api } from '@/lib/api'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'
import { getErrorMessage, getErrorInfo } from '@/lib/errorMessages'

export default function HomePage() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [parsedData, setParsedData] = useState<ExcelParseResponse[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<{ message: string; code?: string } | null>(null)
  const { language } = useLanguage()

  const handleFilesAccepted = (files: UploadedFile[]) => {
    setUploadedFiles(prev => [...prev, ...files])
    setError(null)
  }

  const handleFileRemoved = (fileId: string) => {
    console.log('🗑️ [PAGE] 删除文件:', fileId)
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const handleParse = async () => {
    console.log('🚀 [PAGE] 开始解析流程')
    if (uploadedFiles.length === 0) {
      console.log('⚠️ [PAGE] 没有上传的文件')
      return
    }

    console.log('🔄 [PAGE] 设置加载状态')
    setIsLoading(true)
    setError(null)

    try {
      const filesToProcess = uploadedFiles
        .filter(f => f.status === 'uploaded')

      console.log(`📋 [PAGE] 待处理文件数量: ${filesToProcess.length}/${uploadedFiles.length}`)

      if (filesToProcess.length === 0) {
        console.log('❌ [PAGE] 没有有效的待处理文件')
        throw new Error(getErrorMessage('NO_VALID_FILES', language))
      }

      console.log('🔄 [PAGE] 更新文件状态为处理中')
      // Update file status to processing
      setUploadedFiles(prev => 
        prev.map(f => 
          f.status === 'uploaded' 
            ? { ...f, status: 'processing' }
            : f
        )
      )

      // Process multiple files
      const files = filesToProcess.map(f => f.file)
      console.log('📤 [PAGE] 调用API生成Excel')
      const response = await api.generateMultipleExcel(files)
      
      console.log('📥 [PAGE] API响应:', {
        success: response.success,
        hasData: !!response.data,
        error: response.error,
        error_code: response.error_code
      })

      if (!response.success || !response.data) {
        console.log('❌ [PAGE] API响应失败')
        const errorMessage = getErrorMessage(response.error_code, language, response.error)
        throw { message: errorMessage, code: response.error_code }
      }

      const { results, errors, summary } = response.data
      console.log('📊 [PAGE] 处理结果:', {
        resultCount: results?.length || 0,
        errorCount: errors?.length || 0,
        summary
      })

      // Handle errors for individual files
      if (errors && errors.length > 0) {
        setUploadedFiles(prev =>
          prev.map(f => {
            const error = errors.find(e => e.filename === f.name)
            if (error) {
              const errorMessage = getErrorMessage(error.error_code, language, error.error)
              return { ...f, status: 'error', error: errorMessage }
            }
            return f
          })
        )
      }

      // Create parsed data for preview
      const previewDataList: ExcelParseResponse[] = results.map(result => ({
        headers: result.md_parsing.headers || [],
        data: [],
        summary: {
          totalRows: result.md_parsing.rows_count || 0,
          totalColumns: result.md_parsing.headers?.length || 0,
          fileName: result.filename,
          fileSize: 0,
          parsedAt: result.timestamp
        },
        metadata: {
          excel_output: result.output_filename,
          download_url: result.download_url,
          excel_writing: result.excel_writing
        }
      }))

      setParsedData(previewDataList)

      // Update file status to completed for successful files
      setUploadedFiles(prev =>
        prev.map(f => {
          const result = results.find(r => r.filename === f.name)
          if (result) {
            return { ...f, status: 'completed' }
          }
          return f
        })
      )

      // Auto-download all generated Excel files
      console.log('⬇️ [PAGE] 开始自动下载Excel文件')
      for (const result of results) {
        if (result.output_filename) {
          console.log(`⬇️ [PAGE] 下载文件: ${result.output_filename}`)
          await downloadExcelFile(result.output_filename)
        }
      }
      console.log('✅ [PAGE] 所有文件下载完成')

      // Show summary message
      if (errors && errors.length > 0) {
        const message = language === 'ja' 
          ? `${summary.success_count}個のExcelファイルを正常に生成しました。${summary.error_count}個のファイルが失敗しました。`
          : language === 'zh'
          ? `成功生成${summary.success_count}个Excel文件。${summary.error_count}个文件失败。`
          : `Generated ${summary.success_count} Excel files successfully. ${summary.error_count} files failed.`
        setError({ message })
      }

    } catch (err) {
      if (err && typeof err === 'object' && 'message' in err) {
        setError(err as { message: string; code?: string })
      } else {
        const errorMessage = err instanceof Error ? err.message : getErrorMessage('UNEXPECTED_ERROR', language)
        setError({ message: errorMessage })
      }
      
      // Update file status to error
      setUploadedFiles(prev =>
        prev.map(f =>
          f.status === 'processing'
            ? { ...f, status: 'error', error: error?.message || '' }
            : f
        )
      )
    } finally {
      setIsLoading(false)
    }
  }

  const downloadExcelFile = async (filename: string) => {
    try {
      console.log(`⬇️ [DOWNLOAD] 开始下载: ${filename}`)
      const blob = await api.downloadExcel(filename)
      if (blob) {
        console.log(`📦 [DOWNLOAD] 创建下载链接: ${filename}`)
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        console.log(`✅ [DOWNLOAD] 下载成功: ${filename}`)
      } else {
        console.error(`❌ [DOWNLOAD] 下载失败，未获取到文件数据: ${filename}`)
      }
    } catch (err) {
      console.error(`💥 [DOWNLOAD] 下载异常: ${filename}`, err)
    }
  }

  // Health check on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.healthCheck()
        if (!response.success) {
          console.warn('API health check failed:', response.error)
        }
      } catch (err) {
        console.warn('API health check failed:', err)
      }
    }

    checkHealth()
  }, [])

  const validFileCount = uploadedFiles.filter(f => f.status === 'uploaded').length

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
        >
          <div className="flex items-center gap-3">
            <motion.div
              className="p-3 glass-card rounded-xl"
              whileHover={{ rotate: 10 }}
              transition={{ duration: 0.2 }}
            >
              <FileSpreadsheet className="w-8 h-8 text-primary" />
            </motion.div>
            <div>
              <motion.h1 
                className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                {t('app.title', language)}
              </motion.h1>
              <motion.p 
                className="text-muted-foreground text-sm md:text-base"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                {t('app.subtitle', language)}
              </motion.p>
            </div>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="flex items-center gap-2"
          >
            <LanguageSelector />
            <ThemeToggle />
          </motion.div>
        </motion.header>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.section
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">{t('app.uploadSection', language)}</h2>
            </div>

            <FileUpload 
              onFilesAccepted={handleFilesAccepted}
              onFileRemoved={handleFileRemoved}
              maxFiles={10}
            />

            <div className="flex flex-col sm:flex-row gap-4">
              <ParseButton
                onParse={handleParse}
                disabled={validFileCount === 0}
                fileCount={validFileCount}
                className="flex-1"
              />
              
              {validFileCount > 0 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex items-center gap-2 px-4 py-2 glass-card rounded-xl text-sm text-muted-foreground"
                >
                  <Activity className="w-4 h-4" />
                  <span>{t('status.ready', language, { count: validFileCount })}</span>
                </motion.div>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 glass-card border border-red-500/50 bg-red-500/10 rounded-xl"
              >
                <h3 className="font-medium text-red-400 mb-1">{t('errors.parseError', language)}</h3>
                <p className="text-sm text-red-300">{error.message}</p>
                {error.code && (() => {
                  const errorInfo = getErrorInfo(error.code, language)
                  return errorInfo.suggestions.length > 0 ? (
                    <div className="mt-2 text-xs text-red-200">
                      <p className="font-medium">{t('errors.suggestions', language)}</p>
                      <ul className="list-disc list-inside mt-1">
                        {errorInfo.suggestions.map((suggestion, idx) => (
                          <li key={idx}>{suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  ) : null
                })()}
              </motion.div>
            )}
          </motion.section>

          {/* Preview Section */}
          <motion.section
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">{t('app.dataPreview', language)}</h2>
            </div>

            {parsedData.length > 0 ? (
              <DataPreview data={parsedData} />
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass-card p-8 text-center border border-dashed border-white/20"
              >
                <FileSpreadsheet className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-lg font-medium mb-2">{t('app.noDataPreview', language)}</h3>
                <p className="text-muted-foreground">
                  {t('app.noDataPreviewDesc', language)}
                </p>
              </motion.div>
            )}
          </motion.section>
        </div>

        {/* Features */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          {[
            { icon: '📝', key: 'markdownTables' },
            { icon: '🚀', key: 'fastProcessing' },
            { icon: '📱', key: 'responsive' },
            { icon: '🎨', key: 'modernDesign' },
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="glass-card p-4 text-center"
            >
              <div className="text-2xl mb-2">{feature.icon}</div>
              <h3 className="font-medium mb-1">{t(`features.${feature.key}.title`, language)}</h3>
              <p className="text-sm text-muted-foreground">{t(`features.${feature.key}.desc`, language)}</p>
            </motion.div>
          ))}
        </motion.section>
      </div>
    </div>
  )
}