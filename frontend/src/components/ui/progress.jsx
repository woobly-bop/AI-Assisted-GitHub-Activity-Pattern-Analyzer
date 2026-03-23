import * as React from 'react'
import { cn } from '@/lib/utils'

const Progress = React.forwardRef(({ className, value = 0, ...props }, ref) => {
  const v = Math.min(100, Math.max(0, Number(value) || 0))
  return (
    <div
      ref={ref}
      role="progressbar"
      aria-valuenow={v}
      aria-valuemin={0}
      aria-valuemax={100}
      className={cn(
        'relative h-3 w-full overflow-hidden rounded-full bg-muted/80',
        className,
      )}
      {...props}
    >
      <div
        className="h-full rounded-full bg-gradient-to-r from-violet-500 via-indigo-500 to-sky-400 transition-all duration-700 ease-out"
        style={{ width: `${v}%` }}
      />
    </div>
  )
})
Progress.displayName = 'Progress'

export { Progress }
