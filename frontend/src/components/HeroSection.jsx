import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { SearchBar } from '@/components/SearchBar'

const LINES = [
  'Analyze coding patterns',
  'Measure productivity trends',
  'Score placement readiness',
]

function TypingLine({ text }) {
  const [display, setDisplay] = useState('')

  useEffect(() => {
    let i = 0
    const id = setInterval(() => {
      i += 1
      setDisplay(text.slice(0, i))
      if (i >= text.length) clearInterval(id)
    }, 42)
    return () => clearInterval(id)
  }, [text])

  return (
    <>
      <span className="text-muted-foreground">$ </span>
      {display}
      <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-sky-400 align-middle" />
    </>
  )
}

export function HeroSection({ onAnalyze, loading }) {
  const [lineIndex, setLineIndex] = useState(0)

  useEffect(() => {
    const t = setTimeout(() => {
      setLineIndex((p) => (p + 1) % LINES.length)
    }, 3200)
    return () => clearTimeout(t)
  }, [lineIndex])

  return (
    <section className="relative overflow-hidden hero-gradient">
      <div className="mx-auto max-w-4xl px-4 pb-16 pt-12 text-center sm:px-6 sm:pt-20">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <p className="mb-3 inline-flex items-center gap-2 rounded-full border border-violet-500/25 bg-violet-500/10 px-3 py-1 text-xs font-medium text-violet-300">
            Powered by pattern analysis & ML
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            <span className="gradient-text">GitHub Developer Analyzer</span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
            Analyze coding patterns, productivity & placement readiness from
            public GitHub activity — in one polished dashboard.
          </p>
          <p className="mt-6 min-h-[1.75rem] font-mono text-sm text-sky-300/90 sm:text-base">
            <TypingLine key={lineIndex} text={LINES[lineIndex]} />
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.5 }}
          className="mx-auto mt-10 max-w-xl"
        >
          <SearchBar onAnalyze={onAnalyze} loading={loading} />
        </motion.div>
      </div>
    </section>
  )
}
