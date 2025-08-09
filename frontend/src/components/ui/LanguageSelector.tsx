'use client'

import { useState, useRef, useEffect } from 'react'
// Removed framer-motion for better performance
import { Globe, Check } from 'lucide-react'
import { Language, languageNames } from '@/lib/i18n'
import { useLanguage } from '@/components/providers/LanguageProvider'
import { cn } from '@/lib/utils'

export function LanguageSelector() {
  const { language, setLanguage } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const languages: Language[] = ['ja', 'zh', 'en']

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'inline-flex items-center gap-2 px-4 py-2 rounded-xl',
          'glass-card border border-white/20',
          'hover:bg-white/10 dark:hover:bg-white/5',
          'transition-all duration-300 hover:scale-105 active:scale-95',
          'text-sm font-medium'
        )}
      >
        <Globe className="w-4 h-4" />
        <span>{languageNames[language]}</span>
        <svg
          className={cn(
            "w-4 h-4 transition-transform duration-200",
            isOpen && "rotate-180"
          )}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div
          className={cn(
            'absolute right-0 mt-2 w-48',
            'glass-card border border-white/20',
            'rounded-xl overflow-hidden',
            'shadow-xl animate-scale-in'
          )}
        >
          <div className="py-1">
            {languages.map((lang) => (
              <button
                key={lang}
                onClick={() => {
                  setLanguage(lang)
                  setIsOpen(false)
                }}
                className={cn(
                  'w-full px-4 py-2.5 text-left text-sm',
                  'flex items-center justify-between',
                  'hover:bg-white/10 dark:hover:bg-white/5',
                  'transition-all duration-200 hover:translate-x-1',
                  language === lang && 'bg-primary/10 text-primary'
                )}
              >
                <span className="font-medium">{languageNames[lang]}</span>
                {language === lang && (
                  <div className="animate-scale-in">
                    <Check className="w-4 h-4" />
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}