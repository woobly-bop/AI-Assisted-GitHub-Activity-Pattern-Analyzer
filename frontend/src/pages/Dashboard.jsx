import { Activity, BarChart3, CalendarDays, Download, Gauge } from 'lucide-react'
import { motion } from 'framer-motion'
import { ChartSection } from '@/components/ChartCard'
import { InsightsCard } from '@/components/InsightsCard'
import { ProfileCard } from '@/components/ProfileCard'
import { RecommendationsList } from '@/components/RecommendationsList'
import { ScoreCard } from '@/components/ScoreCard'
import { StatsCard } from '@/components/StatsCard'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

function formatPct(n) {
  if (n == null || Number.isNaN(n)) return '—'
  return `${(Number(n) * 100).toFixed(0)}%`
}

export function Dashboard({ data, onDownloadReport }) {
  const demo = data?._demo
  const apiNote = data?._error
  const profile = data?.profile
  const patterns = data?.patterns
  const insights = data?.insights
  const username = data?.username

  const pm = patterns?.productivity_metrics
  const tp = patterns?.time_patterns

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="mx-auto max-w-7xl space-y-10 px-4 pb-20 pt-8 sm:px-6"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {insights?.summary?.slice(0, 160)}
            {(insights?.summary?.length || 0) > 160 ? '…' : ''}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {demo && (
            <Badge variant="warning" className="max-w-full whitespace-normal text-left text-xs">
              Demo data
              {apiNote ? `: ${apiNote}` : ' (API unavailable or error)'}
            </Badge>
          )}
          <Button
            type="button"
            variant="outline"
            className="rounded-xl border-border/60"
            onClick={onDownloadReport}
          >
            <Download className="size-4" />
            Download report
          </Button>
        </div>
      </div>

      <ProfileCard profile={profile} username={username} />

      <div>
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Activity overview
        </h3>
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatsCard
            title="Total events"
            value={pm?.total_events?.toLocaleString?.() ?? '—'}
            subtitle="From recent public events"
            icon={BarChart3}
            delay={0}
          />
          <StatsCard
            title="Active days"
            value={pm?.active_days?.toLocaleString?.() ?? '—'}
            subtitle="Unique days with activity"
            icon={CalendarDays}
            delay={0.05}
          />
          <StatsCard
            title="Commits / day"
            value={pm?.commits_per_day ?? '—'}
            subtitle="Estimated from push payloads"
            icon={Activity}
            delay={0.1}
          />
          <StatsCard
            title="Consistency"
            value={formatPct(pm?.consistency_ratio)}
            subtitle="Active days in window"
            icon={Gauge}
            delay={0.15}
          />
        </div>
      </div>

      {tp?.most_active_day && (
        <p className="text-center text-sm text-muted-foreground">
          Most active day:{' '}
          <span className="font-medium text-foreground">
            {tp.most_active_day}s
          </span>
        </p>
      )}

      <ChartSection patterns={patterns} />

      <ScoreCard placement={insights?.placement_score} />

      <div>
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Insights
        </h3>
        <InsightsCard insights={insights} />
      </div>

      <RecommendationsList items={insights?.recommendations} />

      {insights?.comparative_insights?.length > 0 && (
        <div className="glass rounded-2xl border border-border/50 p-6">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            Comparative
          </h3>
          <ul className="space-y-2 text-sm text-muted-foreground">
            {insights.comparative_insights.map((c, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-violet-400">▹</span>
                {c}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  )
}
