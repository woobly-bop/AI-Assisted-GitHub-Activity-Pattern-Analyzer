import { useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function SearchBar({ onAnalyze, loading }) {
  const [value, setValue] = useState('')

  const submit = (e) => {
    e.preventDefault()
    const u = value.trim()
    if (!u || loading) return
    onAnalyze(u)
  }

  return (
    <form
      onSubmit={submit}
      className="glass flex flex-col gap-3 rounded-2xl p-2 sm:flex-row sm:items-center sm:gap-2"
    >
      <Input
        placeholder="Enter GitHub username (e.g. octocat)"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={loading}
        className="h-12 flex-1 border-border/50 bg-background/40"
        autoComplete="off"
        spellCheck={false}
      />
      <Button
        type="submit"
        disabled={loading || !value.trim()}
        className="h-12 shrink-0 rounded-xl px-8"
      >
        {loading ? 'Analyzing…' : 'Analyze'}
        {!loading && <ArrowRight className="size-4" />}
      </Button>
    </form>
  )
}
