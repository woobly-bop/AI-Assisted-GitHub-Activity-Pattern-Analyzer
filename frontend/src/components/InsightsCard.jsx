import { motion } from 'framer-motion'
import { Activity, Clock, Languages, Zap } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

const SECTIONS = [
  {
    key: 'time_insights',
    title: 'Time insights',
    icon: Clock,
    gradient: 'from-violet-500/20 to-transparent',
  },
  {
    key: 'activity_insights',
    title: 'Activity insights',
    icon: Activity,
    gradient: 'from-indigo-500/20 to-transparent',
  },
  {
    key: 'productivity_insights',
    title: 'Productivity insights',
    icon: Zap,
    gradient: 'from-sky-500/20 to-transparent',
  },
  {
    key: 'language_insights',
    title: 'Language insights',
    icon: Languages,
    gradient: 'from-emerald-500/15 to-transparent',
  },
]

export function InsightsCard({ insights }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {SECTIONS.map((s, i) => {
        const items = insights?.[s.key]
        const list = Array.isArray(items) ? items : []
        const Icon = s.icon
        return (
          <motion.div
            key={s.key}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Card className="glass h-full border-border/50 overflow-hidden">
              <div
                className={`h-1 w-full bg-gradient-to-r ${s.gradient} via-transparent`}
              />
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-base font-semibold">
                  <span className="flex size-8 items-center justify-center rounded-lg bg-muted/60">
                    <Icon className="size-4 text-violet-300" />
                  </span>
                  {s.title}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 pt-0">
                {list.length === 0 && (
                  <p className="text-sm text-muted-foreground">No data.</p>
                )}
                {list.map((line, j) => (
                  <p
                    key={j}
                    className="rounded-xl border border-border/40 bg-muted/30 px-3 py-2 text-sm leading-relaxed text-muted-foreground"
                  >
                    {line}
                  </p>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )
      })}
    </div>
  )
}
