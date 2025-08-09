'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { 
  Upload, 
  File, 
  X, 
  CheckCircle, 
  AlertCircle, 
  FileSpreadsheet,
  Loader2
} from 'lucide-react'
import { cn, formatFileSize, validateMDFile, generateId } from '@/lib/utils'
import { UploadedFile } from '@/types'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'
import { getErrorMessage } from '@/lib/errorMessages'

interface FileUploadProps {
  onFilesAccepted: (files: UploadedFile[]) => void
  maxFiles?: number
  className?: string
}

export function FileUpload({ onFilesAccepted, maxFiles = 5, className }: FileUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isDragActive, setIsDragActive] = useState(false)
  const { language } = useLanguage()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map(file => {
      const validation = validateMDFile(file)
      return {
        id: generateId(),
        file,
        name: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date(),
        status: validation.valid ? 'uploaded' : 'error',
        error: validation.error,
      }
    })

    setUploadedFiles(prev => [...prev, ...newFiles])
    onFilesAccepted(newFiles.filter(f => f.status === 'uploaded'))
  }, [onFilesAccepted])

  const { getRootProps, getInputProps, isDragActive: dropzoneActive } = useDropzone({
    onDrop,
    accept: {
      'text/markdown': ['.md'],
      'text/x-markdown': ['.markdown'],
      'text/plain': ['.txt'],
      'application/octet-stream': ['.md', '.markdown']
    },
    maxFiles,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
    onDropAccepted: () => setIsDragActive(false),
    onDropRejected: () => setIsDragActive(false),
  })

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id))
  }

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
      case 'uploaded':
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-success" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      case 'processing':
        return <Loader2 className="w-4 h-4 animate-spin text-yellow-500" />
      default:
        return <File className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
      case 'processing':
        return 'border-blue-500/50 bg-blue-500/10'
      case 'uploaded':
      case 'completed':
        return 'border-success/50 bg-success/10'
      case 'error':
        return 'border-red-500/50 bg-red-500/10'
      default:
        return 'border-gray-500/50 bg-gray-500/10'
    }
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={cn(
          'relative overflow-hidden glass-card p-8 border-2 border-dashed transition-all duration-300 cursor-pointer',
          isDragActive || dropzoneActive
            ? 'border-primary/50 bg-primary/10 scale-105'
            : 'border-white/20 hover:border-primary/30 hover:bg-white/5'
        )}
      >
        <input {...getInputProps()} />
        
        {isDragActive || dropzoneActive ? (
          <div className="text-center animate-scale-in">
            <div className="animate-bounce">
              <Upload className="w-12 h-12 mx-auto mb-4 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-primary mb-2">
              {t('fileUpload.dropActive', language)}
            </h3>
            <p className="text-muted-foreground">
              {t('fileUpload.dropActiveDesc', language)}
            </p>
          </div>
        ) : (
          <div className="text-center animate-fade-in">
            <FileSpreadsheet className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-xl font-semibold mb-2">
              {t('fileUpload.uploadTitle', language)}
            </h3>
            <p className="text-muted-foreground mb-4">
              {t('fileUpload.uploadDesc', language)}
            </p>
            <div className="flex flex-wrap justify-center gap-2 text-sm text-muted-foreground">
              <span className="px-2 py-1 bg-white/10 rounded">*.md</span>
              <span className="px-2 py-1 bg-white/10 rounded">*.markdown</span>
              <span className="px-2 py-1 bg-white/10 rounded">*.txt</span>
            </div>
          </div>
        )}

        {/* Animated background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        </div>
      </div>

      {/* File List */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2 animate-slide-up">
          <h4 className="text-sm font-medium text-muted-foreground">
            {t('fileUpload.uploadedFiles', language)} ({uploadedFiles.length})
          </h4>
          
          {uploadedFiles.map((file) => (
            <div
              key={file.id}
              className={cn(
                'flex items-center justify-between p-3 rounded-lg border glass animate-slide-in-left',
                getStatusColor(file.status)
              )}
            >
              <div className="flex items-center gap-3 min-w-0 flex-1">
                {getStatusIcon(file.status)}
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium truncate">
                    {file.name}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{formatFileSize(file.size)}</span>
                    <span>•</span>
                    <span className="capitalize">{t(`fileUpload.fileStatus.${file.status}`, language)}</span>
                  </div>
                  {file.error && (
                    <p className="text-xs text-red-500 mt-1">{file.error}</p>
                  )}
                </div>
              </div>
              
              <button
                onClick={() => removeFile(file.id)}
                className="p-1 rounded hover:bg-white/10 text-muted-foreground hover:text-foreground transition-all hover:scale-110"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}