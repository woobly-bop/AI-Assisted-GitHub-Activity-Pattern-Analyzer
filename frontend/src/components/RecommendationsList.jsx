import { motion } from 'framer-motion'
import { Lightbulb } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function RecommendationsList({ items }) {
  const list = Array.isArray(items) ? items : []

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className="glass border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base font-semibold">
            <span className="flex size-8 items-center justify-center rounded-lg bg-amber-500/15">
              <Lightbulb className="size-4 text-amber-300" />
            </span>
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {list.map((text, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.04 }}
                className="flex gap-3 rounded-xl border border-border/40 bg-muted/25 px-4 py-3 text-sm leading-relaxed text-muted-foreground"
              >
                <span className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full bg-violet-500/20 text-xs font-bold text-violet-300">
                  {i + 1}
                </span>
                <span>{text}</span>
              </motion.li>
            ))}
            {list.length === 0 && (
              <li className="text-sm text-muted-foreground">No recommendations.</li>
            )}
          </ul>
        </CardContent>
      </Card>
    </motion.div>
  )
}
