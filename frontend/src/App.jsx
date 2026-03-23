import { useCallback, useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Navbar } from '@/components/Navbar'
import { HeroSection } from '@/components/HeroSection'
import { Loader } from '@/components/Loader'
import { Dashboard } from '@/pages/Dashboard'
import { analyzeUserWithFallback, DUMMY_ANALYSIS } from '@/services/api'
import { Button } from '@/components/ui/button'

const THEME_KEY = 'gha-theme'

function getInitialTheme() {
  if (typeof window === 'undefined') return 'dark'
  return localStorage.getItem(THEME_KEY) || 'dark'
}

export default function App() {
  const [theme, setTheme] = useState(getInitialTheme)
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const dashboardRef = useRef(null)

  useEffect(() => {
    document.documentElement.classList.toggle('light', theme === 'light')
    document.documentElement.classList.toggle('dark', theme === 'dark')
    localStorage.setItem(THEME_KEY, theme)
  }, [theme])

  const onToggleTheme = () => {
    setTheme((t) => (t === 'dark' ? 'light' : 'dark'))
  }

  const onAnalyze = useCallback(async (username) => {
    setLoading(true)
    setData(null)
    const result = await analyzeUserWithFallback(username)
    setData(result)
    setLoading(false)
    requestAnimationFrame(() => {
      dashboardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }, [])

  const onDownloadReport = () => {
    const blob = new Blob(
      [JSON.stringify(data || DUMMY_ANALYSIS, null, 2)],
      { type: 'application/json' },
    )
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `github-analysis-${data?.username || 'report'}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar theme={theme} onToggleTheme={onToggleTheme} />

      <HeroSection onAnalyze={onAnalyze} loading={loading} />

      <AnimatePresence mode="wait">
        {loading && (
          <motion.section
            key="loader"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mx-auto max-w-xl px-4"
          >
            <Loader />
          </motion.section>
        )}
      </AnimatePresence>

      <div ref={dashboardRef}>
        {data && !loading && (
          <Dashboard data={data} onDownloadReport={onDownloadReport} />
        )}
      </div>

      {!data && !loading && (
        <section className="mx-auto max-w-3xl px-4 pb-16 text-center">
          <p className="text-sm text-muted-foreground">
            Tip: start the Flask API on port 5000 for live data. Without it, the
            app falls back to polished demo data.
          </p>
          <Button
            type="button"
            variant="ghost"
            className="mt-4"
            onClick={() => onAnalyze('octocat')}
          >
            Try demo with octocat
          </Button>
        </section>
      )}

      <footer className="border-t border-border/40 py-8 text-center text-xs text-muted-foreground">
        GitHub Developer Analyzer · Built with React, Tailwind, Recharts & Framer Motion
      </footer>
    </div>
  )
}
