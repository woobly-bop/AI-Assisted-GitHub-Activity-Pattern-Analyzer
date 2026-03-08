import { motion } from 'framer-motion'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

const COLORS = [
  '#8b5cf6',
  '#6366f1',
  '#38bdf8',
  '#22d3ee',
  '#34d399',
  '#fbbf24',
  '#fb7185',
]

function shortenEventType(t) {
  return t.replace(/Event$/, '')
}

export function ActivityBarChart({ distribution }) {
  const data = Object.entries(distribution || {}).map(([name, value]) => ({
    name: shortenEventType(name),
    value,
  }))

  if (data.length === 0) {
    return (
      <Card className="glass border-border/50">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">
            Activity distribution
          </CardTitle>
        </CardHeader>
        <CardContent className="flex h-[280px] items-center justify-center text-sm text-muted-foreground">
          No activity data
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="glass border-border/50">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold">
          Activity distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[280px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(240 10% 22%)" />
            <XAxis
              dataKey="name"
              tick={{ fill: 'hsl(240 6% 58%)', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: 'hsl(240 6% 58%)', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                background: 'hsl(240 10% 10%)',
                border: '1px solid hsl(240 10% 22%)',
                borderRadius: '12px',
              }}
            />
            <Bar dataKey="value" radius={[8, 8, 0, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export function LanguagePieChart({ languageDistribution }) {
  const data = Object.entries(languageDistribution || {}).map(
    ([name, value]) => ({
      name,
      value,
    }),
  )

  if (data.length === 0) {
    return (
      <Card className="glass border-border/50">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">
            Language distribution
          </CardTitle>
        </CardHeader>
        <CardContent className="flex h-[280px] items-center justify-center text-sm text-muted-foreground">
          No language data
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="glass border-border/50">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold">
          Language distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[280px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={56}
              outerRadius={96}
              paddingAngle={3}
            >
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} stroke="none" />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                background: 'hsl(240 10% 10%)',
                border: '1px solid hsl(240 10% 22%)',
                borderRadius: '12px',
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export function HourlyLineChart({ hourlyDistribution }) {
  const entries = Object.entries(hourlyDistribution || {})
    .map(([h, v]) => ({
      hour: `${h}:00`,
      hourNum: Number(h),
      events: v,
    }))
    .sort((a, b) => a.hourNum - b.hourNum)

  if (entries.length === 0) {
    return (
      <Card className="glass border-border/50">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">
            Hourly activity
          </CardTitle>
        </CardHeader>
        <CardContent className="flex h-[280px] items-center justify-center text-sm text-muted-foreground">
          No hourly data
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="glass border-border/50">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold">
          Hourly activity
        </CardTitle>
      </CardHeader>
      <CardContent className="h-[280px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={entries} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(240 10% 22%)" />
            <XAxis
              dataKey="hour"
              tick={{ fill: 'hsl(240 6% 58%)', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fill: 'hsl(240 6% 58%)', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                background: 'hsl(240 10% 10%)',
                border: '1px solid hsl(240 10% 22%)',
                borderRadius: '12px',
              }}
            />
            <Line
              type="monotone"
              dataKey="events"
              stroke="url(#lineGrad)"
              strokeWidth={3}
              dot={{ r: 3, fill: '#8b5cf6' }}
              activeDot={{ r: 5 }}
            />
            <defs>
              <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#8b5cf6" />
                <stop offset="100%" stopColor="#38bdf8" />
              </linearGradient>
            </defs>
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export function ChartSection({ patterns }) {
  const activity = patterns?.activity_patterns?.event_type_distribution
  const langs =
    patterns?.language_patterns?.language_distribution ||
    (patterns?.language_patterns?.language_repo_counts
      ? Object.fromEntries(
          Object.entries(patterns.language_patterns.language_repo_counts).map(
            ([k, v]) => [k, v],
          ),
        )
      : {})
  const hourly = patterns?.time_patterns?.hourly_distribution

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid gap-6 lg:grid-cols-3"
    >
      <div className="lg:col-span-1">
        <ActivityBarChart distribution={activity} />
      </div>
      <div className="lg:col-span-1">
        <LanguagePieChart languageDistribution={langs} />
      </div>
      <div className="lg:col-span-1">
        <HourlyLineChart hourlyDistribution={hourly} />
      </div>
    </motion.div>
  )
}
