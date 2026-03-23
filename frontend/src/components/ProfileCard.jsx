import { motion } from 'framer-motion'
import { ExternalLink, Users, GitBranch } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

function shortBio(bio) {
  if (!bio) return 'No bio available'
  return bio.length > 140 ? `${bio.slice(0, 137)}…` : bio
}

export function ProfileCard({ profile, username }) {
  const login = profile?.login || username
  const avatar =
    profile?.avatar_url ||
    `https://github.com/${login}.png?size=128`
  const name = profile?.name || login

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className="glass overflow-hidden border-border/50">
        <CardContent className="flex flex-col gap-6 p-6 sm:flex-row sm:items-center">
          <div className="relative mx-auto sm:mx-0">
            <div className="absolute -inset-1 rounded-2xl bg-gradient-to-br from-violet-500/40 to-sky-500/30 blur-md" />
            <img
              src={avatar}
              alt={login}
              className="relative size-24 rounded-2xl border border-white/10 object-cover shadow-xl sm:size-28"
            />
          </div>
          <div className="flex-1 text-center sm:text-left">
            <div className="flex flex-wrap items-center justify-center gap-2 sm:justify-start">
              <h2 className="text-2xl font-bold tracking-tight">{name}</h2>
              <a
                href={`https://github.com/${login}`}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-sm text-violet-400 hover:text-violet-300"
              >
                @{login}
                <ExternalLink className="size-3.5" />
              </a>
            </div>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              {shortBio(profile?.bio)}
            </p>
            <div className="mt-4 flex flex-wrap justify-center gap-4 sm:justify-start">
              <div className="flex items-center gap-2 rounded-xl bg-muted/50 px-3 py-2 text-sm">
                <GitBranch className="size-4 text-violet-400" />
                <span className="text-muted-foreground">Public repos</span>
                <span className="font-semibold tabular-nums">
                  {profile?.public_repos ?? '—'}
                </span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-muted/50 px-3 py-2 text-sm">
                <Users className="size-4 text-sky-400" />
                <span className="text-muted-foreground">Followers</span>
                <span className="font-semibold tabular-nums">
                  {profile?.followers?.toLocaleString?.() ?? '—'}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
