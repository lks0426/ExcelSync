'use client'

import { useState, useEffect } from 'react'
import { FileSpreadsheet, Sparkles, Activity } from 'lucide-react'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'

export default function DebugPage() {
  const [mounted, setMounted] = useState(false)
  const { language } = useLanguage()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <div>Loading...</div>
  }

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 glass-card rounded-xl">
              <FileSpreadsheet className="w-8 h-8 text-primary" />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
                {t('app.title', language)}
              </h1>
              <p className="text-muted-foreground text-sm md:text-base">
                {t('app.subtitle', language)}
              </p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">{t('app.uploadSection', language)}</h2>
            </div>

            {/* Simplified upload area */}
            <div className="glass-card p-8 border-2 border-dashed border-white/20 rounded-xl">
              <div className="text-center">
                <FileSpreadsheet className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-xl font-semibold mb-2">
                  {t('fileUpload.uploadTitle', language)}
                </h3>
                <p className="text-muted-foreground mb-4">
                  {t('fileUpload.uploadDesc', language)}
                </p>
              </div>
            </div>
          </section>

          {/* Preview Section */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold">{t('app.dataPreview', language)}</h2>
            </div>

            <div className="glass-card p-8 text-center border border-dashed border-white/20">
              <FileSpreadsheet className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-medium mb-2">{t('app.noDataPreview', language)}</h3>
              <p className="text-muted-foreground">
                {t('app.noDataPreviewDesc', language)}
              </p>
            </div>
          </section>
        </div>

        {/* Debug Info */}
        <div className="glass-card p-4 space-y-2">
          <h3 className="font-bold">Debug Info:</h3>
          <p>✅ Language: {language}</p>
          <p>✅ Mounted: {mounted ? 'true' : 'false'}</p>
          <p>✅ LanguageProvider working</p>
          <p>✅ i18n working</p>
          <p>✅ Icons working</p>
          <p>✅ CSS working</p>
        </div>
      </div>
    </div>
  )
}