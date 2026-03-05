import axios from 'axios'

const baseURL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, '') || ''

const client = axios.create({
  baseURL: baseURL || undefined,
  timeout: 120000,
  headers: { 'Content-Type': 'application/json' },
})

/** Embedded demo payload when API is unreachable or token missing */
export const DUMMY_ANALYSIS = {
  username: 'octocat',
  profile: {
    login: 'octocat',
    avatar_url: 'https://github.githubassets.com/images/modules/logos_page/Octocat.png',
    name: 'The Octocat',
    bio: 'GitHub mascot and assistant',
    public_repos: 8,
    followers: 5000,
    following: 0,
  },
  patterns: {
    time_patterns: {
      peak_hours: [
        { hour: 14, count: 42 },
        { hour: 15, count: 38 },
        { hour: 16, count: 31 },
        { hour: 10, count: 24 },
        { hour: 20, count: 18 },
      ],
      most_active_day: 'Wednesday',
      weekend_ratio: 0.12,
      hourly_distribution: {
        9: 12, 10: 18, 11: 22, 12: 15, 13: 28, 14: 42, 15: 38, 16: 31,
        17: 20, 18: 14, 19: 10, 20: 18, 21: 8,
      },
      daily_distribution: {
        Monday: 35, Tuesday: 40, Wednesday: 48, Thursday: 38, Friday: 32,
        Saturday: 12, Sunday: 10,
      },
    },
    activity_patterns: {
      event_type_distribution: {
        PushEvent: 130,
        PullRequestEvent: 45,
        IssuesEvent: 30,
        CreateEvent: 25,
        WatchEvent: 20,
      },
      activity_diversity: 5,
      total_events: 250,
    },
    language_patterns: {
      primary_language: 'JavaScript',
      language_diversity: 4,
      language_distribution: {
        JavaScript: 40,
        Python: 25,
        Ruby: 20,
        Shell: 15,
      },
      top_languages: ['JavaScript', 'Python', 'Ruby', 'Shell'],
    },
    repository_patterns: {
      total_repositories: 8,
      total_stars: 320,
      total_forks: 150,
      average_stars: 40,
    },
    collaboration_patterns: {
      pull_requests: 45,
      issues: 30,
      collaboration_frequency: 75,
      collaboration_ratio: 0.3,
    },
    productivity_metrics: {
      total_events: 250,
      active_days: 65,
      commits_per_day: 6.5,
      daily_average_events: 3.85,
      consistency_ratio: 0.722,
    },
  },
  insights: {
    summary:
      'Developer has been active for 65 days with 250 total events. Primary language is JavaScript across 8 repositories.',
    time_insights: [
      'Most active during afternoon hours (around 14:00)',
      'Most productive on Wednesdays',
    ],
    activity_insights: [
      'Pushes code frequently (52.0% of activity)',
      'Diverse contribution profile spanning 5 event types',
    ],
    language_insights: [
      'Primary expertise in JavaScript (40.0% of repos)',
      'Polyglot developer with experience in 4 languages',
    ],
    productivity_insights: [
      'Regular contributor with steady activity',
      'Excellent consistency — active on most days in the analysis window',
    ],
    comparative_insights: [
      'Repositories are gaining healthy community recognition',
      'Good language diversity across projects',
    ],
    recommendations: [
      'Increase collaboration through code reviews, pull requests, and issue discussions',
      'Continue documenting your projects to increase visibility and adoption',
    ],
    placement_score: {
      score: 78.5,
      level: 'High',
      reason:
        'strong activity consistency; excellent collaboration record; high-quality repositories',
      breakdown: {
        activity_consistency: 22,
        collaboration: 23.5,
        repository_quality: 18,
        language_diversity: 15,
      },
    },
  },
}

/**
 * POST /api/analyze — uses Vite proxy to backend when VITE_API_URL is empty.
 */
export async function analyzeUser(username) {
  const { data } = await client.post('/api/analyze', { username })
  return data
}

export async function analyzeUserWithFallback(username) {
  try {
    return await analyzeUser(username)
  } catch (err) {
    console.warn('[api] Falling back to demo data:', err?.message || err)
    return {
      ...DUMMY_ANALYSIS,
      username,
      _demo: true,
      _error: err?.response?.data?.message || err?.message || 'Unknown error',
    }
  }
}
