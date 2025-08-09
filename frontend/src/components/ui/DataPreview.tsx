'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { 
  Table, 
  FileText, 
  Download, 
  Eye, 
  EyeOff,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { useState } from 'react'
import { ExcelParseResponse } from '@/types'
import { cn, formatFileSize } from '@/lib/utils'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'

interface DataPreviewProps {
  data: ExcelParseResponse[]
  className?: string
}

export function DataPreview({ data, className }: DataPreviewProps) {
  const [selectedFileIndex, setSelectedFileIndex] = useState(0)
  const [isExpanded, setIsExpanded] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const rowsPerPage = 10
  const { language } = useLanguage()

  if (!data || data.length === 0) return null

  const selectedFile = data[selectedFileIndex]
  const totalPages = Math.ceil(selectedFile.data.length / rowsPerPage)
  const startIndex = (currentPage - 1) * rowsPerPage
  const endIndex = startIndex + rowsPerPage
  const currentData = selectedFile.data.slice(startIndex, endIndex)

  const handlePrevFile = () => {
    if (selectedFileIndex > 0) {
      setSelectedFileIndex(selectedFileIndex - 1)
      setCurrentPage(1)
    }
  }

  const handleNextFile = () => {
    if (selectedFileIndex < data.length - 1) {
      setSelectedFileIndex(selectedFileIndex + 1)
      setCurrentPage(1)
    }
  }

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1)
    }
  }

  const downloadCSV = () => {
    const csvContent = [
      selectedFile.headers.join(','),
      ...selectedFile.data.map(row => 
        selectedFile.headers.map(header => `"${row[header] || ''}"`).join(',')
      )
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${selectedFile.summary.fileName.replace(/\.[^/.]+$/, '')}_parsed.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <div className={cn('glass-card border animate-slide-up', className)}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <Table className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold">{t('dataPreview.parsedData', language) || 'Parsed Data'}</h3>
          {data.length > 1 && (
            <span className="px-2 py-1 bg-primary/20 text-primary text-xs rounded-full">
              {data.length} {t('dataPreview.files', language) || 'files'}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={downloadCSV}
            className="p-2 rounded-lg hover:bg-white/10 text-muted-foreground hover:text-foreground transition-all hover:scale-105 active:scale-95"
            title={t('dataPreview.downloadCSV', language) || 'Download as CSV'}
          >
            <Download className="w-4 h-4" />
          </button>
          
          <motion.button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 rounded-lg hover:bg-white/10 text-muted-foreground hover:text-foreground transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </motion.button>
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* File Navigation */}
            {data.length > 1 && (
              <div className="flex items-center justify-between p-4 border-b border-white/10 bg-white/5">
                <div className="flex items-center gap-2">
                  <motion.button
                    onClick={handlePrevFile}
                    disabled={selectedFileIndex === 0}
                    className="p-1 rounded hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </motion.button>

                  <motion.button
                    onClick={handleNextFile}
                    disabled={selectedFileIndex === data.length - 1}
                    className="p-1 rounded hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <ChevronRight className="w-4 h-4" />
                  </motion.button>
                </div>

                <div className="text-sm text-center">
                  <div className="font-medium text-foreground">
                    {selectedFile.summary.fileName}
                  </div>
                  <div className="text-muted-foreground">
                    {t('dataPreview.fileNav', language, { current: selectedFileIndex + 1, total: data.length }) || `File ${selectedFileIndex + 1} of ${data.length}`}
                  </div>
                </div>

                <div className="text-xs text-muted-foreground text-right">
                  <div>{formatFileSize(selectedFile.summary.fileSize)}</div>
                  <div>{selectedFile.summary.totalRows} rows</div>
                </div>
              </div>
            )}

            {/* Summary Stats */}
            <div className="p-4 border-b border-white/10 bg-white/5">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">
                    {selectedFile.summary.totalRows}
                  </div>
                  <div className="text-muted-foreground">{t('dataPreview.totalRows', language)}</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">
                    {selectedFile.summary.totalColumns}
                  </div>
                  <div className="text-muted-foreground">{t('dataPreview.totalColumns', language)}</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">
                    {formatFileSize(selectedFile.summary.fileSize)}
                  </div>
                  <div className="text-muted-foreground">{t('dataPreview.fileSize', language) || 'File Size'}</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">
                    {selectedFile.metadata?.excel_writing?.success_rate || 'N/A'}
                  </div>
                  <div className="text-muted-foreground">{t('dataPreview.successRate', language)}</div>
                </div>
              </div>

              {/* Excel Generation Info */}
              {selectedFile.metadata?.excel_output && (
                <div className="mt-4 p-3 bg-success/10 border border-success/20 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-sm font-medium text-success">{t('dataPreview.excelGenerated', language) || 'Excel File Generated'}</h4>
                      <p className="text-xs text-success-light dark:text-success-light mt-1 font-medium">
                        {selectedFile.metadata.excel_output}
                      </p>
                      {selectedFile.metadata.excel_writing && (
                        <p className="text-xs text-success-light dark:text-success-light mt-1 font-medium">
                          {selectedFile.metadata.excel_writing.successful_writes}/{selectedFile.metadata.excel_writing.total_fields} {t('dataPreview.fieldsMapped', language) || 'fields mapped successfully'}
                        </p>
                      )}
                    </div>
                    {selectedFile.metadata.download_url && (
                      <motion.a
                        href={`http://localhost:8001${selectedFile.metadata.download_url}`}
                        download
                        className="px-3 py-1 bg-success hover:bg-success-dark text-success-foreground text-xs rounded-md transition-colors"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        {t('dataPreview.downloadExcel', language)}
                      </motion.a>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Data Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/10 bg-white/5">
                    {selectedFile.headers.map((header, index) => (
                      <th
                        key={index}
                        className="text-left p-3 text-sm font-medium text-muted-foreground"
                      >
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {currentData.map((row, rowIndex) => (
                    <motion.tr
                      key={startIndex + rowIndex}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: rowIndex * 0.05 }}
                      className="border-b border-white/5 hover:bg-white/5 transition-colors"
                    >
                      {selectedFile.headers.map((header, colIndex) => (
                        <td
                          key={colIndex}
                          className="p-3 text-sm text-foreground"
                        >
                          <div className="max-w-xs truncate">
                            {row[header] || '-'}
                          </div>
                        </td>
                      ))}
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between p-4 border-t border-white/10">
                <div className="text-sm text-muted-foreground">
                  Showing {startIndex + 1}-{Math.min(endIndex, selectedFile.data.length)} of {selectedFile.data.length} rows
                </div>
                
                <div className="flex items-center gap-2">
                  <motion.button
                    onClick={handlePrevPage}
                    disabled={currentPage === 1}
                    className="px-3 py-1 rounded hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Previous
                  </motion.button>
                  
                  <span className="text-sm text-muted-foreground">
                    Page {currentPage} of {totalPages}
                  </span>
                  
                  <motion.button
                    onClick={handleNextPage}
                    disabled={currentPage === totalPages}
                    className="px-3 py-1 rounded hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Next
                  </motion.button>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}