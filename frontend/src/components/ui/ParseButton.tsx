'use client'

import { useState } from 'react'
import { Play, Loader2, CheckCircle, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'

interface ParseButtonProps {
  onParse: () => Promise<void>
  disabled?: boolean
  fileCount: number
  className?: string
}

export function ParseButton({ onParse, disabled, fileCount, className }: ParseButtonProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const { language } = useLanguage()

  const handleParse = async () => {
    if (disabled || isLoading) return

    setIsLoading(true)
    setStatus('idle')

    try {
      await onParse()
      setStatus('success')
      
      // Reset status after 3 seconds
      setTimeout(() => {
        setStatus('idle')
      }, 3000)
    } catch (error) {
      setStatus('error')
      
      // Reset status after 3 seconds
      setTimeout(() => {
        setStatus('idle')
      }, 3000)
    } finally {
      setIsLoading(false)
    }
  }

  const getButtonContent = () => {
    if (isLoading) {
      return (
        <>
          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
          {t('parseButton.parsing', language)}
        </>
      )
    }

    if (status === 'success') {
      return (
        <>
          <CheckCircle className="w-5 h-5 mr-2 text-success" />
          {t('parseButton.success', language)}
        </>
      )
    }

    if (status === 'error') {
      return (
        <>
          <AlertTriangle className="w-5 h-5 mr-2 text-red-400" />
          {t('parseButton.failed', language)}
        </>
      )
    }

    return (
      <>
        <Play className="w-5 h-5 mr-2" />
        {t('parseButton.generate', language)} {fileCount > 0 ? `(${t(fileCount === 1 ? 'parseButton.fileCount_one' : 'parseButton.fileCount_other', language, { count: fileCount })})` : ''}
      </>
    )
  }

  const getButtonColors = () => {
    if (disabled) {
      return 'bg-muted text-muted-foreground cursor-not-allowed'
    }

    if (status === 'success') {
      return 'bg-success hover:bg-success-dark text-success-foreground'
    }

    if (status === 'error') {
      return 'bg-red-600 hover:bg-red-700 text-white'
    }

    return 'bg-primary hover:bg-primary/90 text-primary-foreground'
  }

  return (
    <button
      onClick={handleParse}
      disabled={disabled || isLoading}
      className={cn(
        'relative inline-flex items-center justify-center px-6 py-3 rounded-xl font-medium transition-all duration-300 glass-card border',
        getButtonColors(),
        'hover:scale-105 active:scale-95',
        'shadow-lg hover:shadow-xl',
        className
      )}
      style={{
        boxShadow: status === 'success' 
          ? '0 0 20px hsla(var(--success) / 0.4)' 
          : status === 'error'
          ? '0 0 20px rgba(239, 68, 68, 0.4)'
          : '0 10px 25px rgba(0, 0, 0, 0.1)'
      }}
    >
      <div className={cn(
        'flex items-center transition-transform duration-200',
        isLoading && 'scale-95'
      )}>
        {getButtonContent()}
      </div>

      {/* Loading subtle glow effect */}
      {isLoading && (
        <div 
          className="absolute inset-0 rounded-xl bg-primary/10"
          style={{
            animation: 'gentle-pulse 2s ease-in-out infinite'
          }}
        />
      )}
      
      <style jsx>{`
        @keyframes gentle-pulse {
          0%, 100% { 
            opacity: 0.1;
            transform: scale(1);
          }
          50% { 
            opacity: 0.3;
            transform: scale(1.02);
          }
        }
      `}</style>
    </button>
  )
}