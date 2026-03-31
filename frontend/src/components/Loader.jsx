import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

export function Loader({ label = 'Analyzing GitHub activity…' }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center gap-4 py-16"
    >
      <div className="relative">
        <div className="absolute inset-0 animate-ping rounded-full bg-violet-500/30 blur-xl" />
        <Loader2 className="relative size-12 animate-spin text-violet-400" />
      </div>
      <p className="text-sm text-muted-foreground">{label}</p>
      <div className="h-2 w-48 overflow-hidden rounded-full bg-muted">
        <motion.div
          className="h-full w-1/3 rounded-full bg-gradient-to-r from-violet-500 to-sky-400"
          animate={{ x: ['-100%', '200%'] }}
          transition={{ repeat: Infinity, duration: 1.2, ease: 'easeInOut' }}
        />
      </div>
    </motion.div>
  )
}
