'use client'

import { useState } from 'react'
import { FileSpreadsheet } from 'lucide-react'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { t } from '@/lib/i18n'

export default function SimplePage() {
  const [test, setTest] = useState('working')
  const { language } = useLanguage()

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">
          <FileSpreadsheet className="w-8 h-8 inline mr-2" />
          {t('app.title', language)}
        </h1>
        <p className="mb-4">Language: {language}</p>
        <p className="mb-4">Test state: {test}</p>
        <p className="text-green-600">✅ LanguageProvider is working</p>
        <p className="text-blue-600">✅ i18n translations are working</p>
        <p className="text-purple-600">✅ React state is working</p>
      </div>
    </div>
  )
}