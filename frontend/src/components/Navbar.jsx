import { Github, Moon, Sparkles, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function Navbar({ theme, onToggleTheme }) {
  return (
    <header className="sticky top-0 z-50 border-b border-border/40 bg-background/70 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-2">
          <div className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 shadow-lg shadow-violet-500/25">
            <Sparkles className="size-5 text-white" />
          </div>
          <span className="font-semibold tracking-tight text-foreground">
            GitHub Analyzer
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="rounded-xl border-border/60"
            onClick={onToggleTheme}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <Sun className="size-4" />
            ) : (
              <Moon className="size-4" />
            )}
          </Button>
          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="inline-flex"
          >
            <Button variant="ghost" size="sm" className="gap-2 rounded-xl">
              <Github className="size-4" />
              GitHub
            </Button>
          </a>
        </div>
      </div>
    </header>
  )
}
