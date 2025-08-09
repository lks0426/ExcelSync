'use client'

import { Moon, Sun, Monitor } from 'lucide-react'
import { useTheme } from '@/components/providers/ThemeProvider'
// Removed framer-motion for better performance

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  const themes = [
    { value: 'light' as const, icon: Sun, label: 'Light' },
    { value: 'dark' as const, icon: Moon, label: 'Dark' },
    { value: 'system' as const, icon: Monitor, label: 'System' },
  ]

  return (
    <div className="flex items-center gap-1 glass-card p-1">
      {themes.map(({ value, icon: Icon, label }) => (
        <button
          key={value}
          onClick={() => setTheme(value)}
          className={`relative p-2 rounded-lg transition-all hover:scale-105 active:scale-95 ${
            theme === value
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-white/10 dark:hover:bg-white/5 text-muted-foreground hover:text-foreground'
          }`}
          title={label}
        >
          <div className="transition-all">
            <Icon size={18} />
          </div>
          {theme === value && (
            <div className="absolute inset-0 rounded-lg bg-primary/20" />
          )}
        </button>
      ))}
    </div>
  )
}