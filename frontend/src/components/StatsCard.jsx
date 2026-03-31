import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

const iconWrap = 'flex size-10 items-center justify-center rounded-xl bg-gradient-to-br shadow-inner'

export function StatsCard({ title, value, subtitle, icon: Icon, delay = 0, className }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.35 }}
    >
      <Card
        className={cn(
          'glass border-border/50 transition-transform hover:-translate-y-0.5',
          className,
        )}
      >
        <CardContent className="p-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                {title}
              </p>
              <p className="mt-2 text-3xl font-bold tabular-nums tracking-tight">
                {value}
              </p>
              {subtitle && (
                <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p>
              )}
            </div>
            {Icon && (
              <div
                className={cn(
                  iconWrap,
                  'from-violet-500/25 to-indigo-500/15 text-violet-300',
                )}
              >
                <Icon className="size-5" />
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
