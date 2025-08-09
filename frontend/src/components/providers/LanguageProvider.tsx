'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { Language, getBrowserLanguage } from '@/lib/i18n'

interface LanguageContextType {
  language: Language
  setLanguage: (language: Language) => void
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>('ja')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // Get saved language from localStorage or use browser language
    const savedLanguage = localStorage.getItem('language') as Language
    const initialLanguage = savedLanguage || getBrowserLanguage()
    setLanguageState(initialLanguage)
    setMounted(true)
  }, [])

  const setLanguage = (newLanguage: Language) => {
    setLanguageState(newLanguage)
    localStorage.setItem('language', newLanguage)
  }

  // Prevent SSR issues - show children with default language while mounting
  if (!mounted) {
    return (
      <LanguageContext.Provider value={{ language: 'ja', setLanguage: () => {} }}>
        {children}
      </LanguageContext.Provider>
    )
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  )
}

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}