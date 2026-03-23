import { motion } from 'framer-motion'
import { Award, TrendingUp } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

function levelVariant(level) {
  const l = (level || '').toLowerCase()
  if (l === 'high') return 'success'
  if (l === 'medium') return 'warning'
  return 'secondary'
}

export function ScoreCard({ placement }) {
  const score = placement?.score ?? 0
  const level = placement?.level ?? '—'
  const reason = placement?.reason ?? ''
  const breakdown = placement?.breakdown || {}

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.45 }}
    >
      <Card className="relative overflow-hidden border-violet-500/30 bg-gradient-to-br from-violet-600/15 via-background to-sky-600/10 shadow-2xl shadow-violet-900/20">
        <div className="pointer-events-none absolute -right-24 -top-24 size-64 rounded-full bg-violet-500/20 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-16 -left-16 size-48 rounded-full bg-sky-500/15 blur-3xl" />
        <CardHeader className="relative flex flex-row items-start justify-between gap-4 pb-2">
          <div>
            <CardTitle className="flex items-center gap-2 text-lg font-semibold">
              <Award className="size-5 text-amber-300" />
              Placement readiness
            </CardTitle>
            <p className="mt-1 text-sm text-muted-foreground">
              Holistic score from consistency, collaboration, repos & languages.
            </p>
          </div>
          <Badge variant={levelVariant(level)} className="shrink-0 capitalize">
            {level}
          </Badge>
        </CardHeader>
        <CardContent className="relative space-y-6">
          <div className="flex flex-wrap items-end gap-6">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                Score
              </p>
              <p
                className={cn(
                  'text-6xl font-black tabular-nums tracking-tight',
                  'bg-gradient-to-br from-white to-violet-200 bg-clip-text text-transparent',
                )}
              >
                {Number(score).toFixed(1)}
                <span className="text-2xl font-semibold text-muted-foreground">
                  /100
                </span>
              </p>
            </div>
            <div className="min-w-[200px] flex-1 pb-2">
              <div className="mb-2 flex items-center justify-between text-xs text-muted-foreground">
                <span>Progress</span>
                <span className="flex items-center gap-1 text-emerald-400">
                  <TrendingUp className="size-3.5" />
                  benchmarked
                </span>
              </div>
              <Progress value={Number(score)} />
            </div>
          </div>

          {reason && (
            <p className="rounded-xl border border-border/50 bg-muted/40 px-4 py-3 text-sm leading-relaxed text-muted-foreground">
              {reason}
            </p>
          )}

          {Object.keys(breakdown).length > 0 && (
            <div className="grid gap-3 sm:grid-cols-2">
              {Object.entries(breakdown).map(([k, v]) => (
                <div
                  key={k}
                  className="rounded-xl border border-border/40 bg-background/40 px-3 py-2"
                >
                  <p className="text-[10px] font-medium uppercase tracking-wide text-muted-foreground">
                    {k.replace(/_/g, ' ')}
                  </p>
                  <p className="text-lg font-semibold tabular-nums">
                    {typeof v === 'number' ? v.toFixed(1) : v}
                  </p>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}
