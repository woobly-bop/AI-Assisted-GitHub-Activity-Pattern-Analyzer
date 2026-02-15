"""
Pattern Analysis Logic
Analyzes GitHub activity data to identify patterns and trends
"""
from datetime import datetime, timedelta
from collections import Counter, defaultdict


class PatternAnalyzer:
    """Analyzes GitHub activity patterns"""
    
    def analyze_patterns(self, user_data):
        """
        Analyze user activity data for patterns
        
        Args:
            user_data (dict): User activity data from GitHub API
            
        Returns:
            dict: Analyzed patterns and statistics
        """
        patterns = {
            'time_patterns': self._analyze_time_patterns(user_data['events']),
            'activity_patterns': self._analyze_activity_patterns(user_data['events']),
            'repository_patterns': self._analyze_repository_patterns(user_data['repositories']),
            'language_patterns': self._analyze_language_patterns(user_data['repositories']),
            'collaboration_patterns': self._analyze_collaboration_patterns(user_data['events']),
            'productivity_metrics': self._calculate_productivity_metrics(user_data)
        }
        
        return patterns
    
    def _analyze_time_patterns(self, events):
        """Analyze temporal patterns in activity"""
        hour_distribution = Counter()
        day_distribution = Counter()
        
        for event in events:
            created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            hour_distribution[created_at.hour] += 1
            day_distribution[created_at.strftime('%A')] += 1
        
        # Find peak hours
        peak_hours = sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'hour_distribution': dict(hour_distribution),
            'day_distribution': dict(day_distribution),
            'peak_hours': [{'hour': h, 'count': c} for h, c in peak_hours],
            'most_active_day': max(day_distribution.items(), key=lambda x: x[1])[0] if day_distribution else None
        }
    
    def _analyze_activity_patterns(self, events):
        """Analyze types of activities"""
        event_types = Counter()
        
        for event in events:
            event_types[event['type']] += 1
        
        return {
            'event_type_distribution': dict(event_types),
            'most_common_activity': event_types.most_common(1)[0] if event_types else None,
            'activity_diversity': len(event_types)
        }
    
    def _analyze_repository_patterns(self, repositories):
        """Analyze repository-related patterns"""
        if not repositories:
            return {}
        
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repositories)
        total_forks = sum(repo.get('forks_count', 0) for repo in repositories)
        
        # Sort by various metrics
        most_starred = sorted(repositories, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:5]
        most_recent = sorted(repositories, key=lambda x: x.get('updated_at', ''), reverse=True)[:5]
        
        return {
            'total_repositories': len(repositories),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'average_stars': total_stars / len(repositories) if repositories else 0,
            'most_starred_repos': [{'name': r['name'], 'stars': r['stargazers_count']} for r in most_starred],
            'recently_updated': [{'name': r['name'], 'updated': r['updated_at']} for r in most_recent]
        }
    
    def _analyze_language_patterns(self, repositories):
        """Analyze programming language usage"""
        languages = Counter()
        
        for repo in repositories:
            lang = repo.get('language')
            if lang:
                languages[lang] += 1
        
        return {
            'language_distribution': dict(languages),
            'primary_language': languages.most_common(1)[0][0] if languages else None,
            'language_diversity': len(languages)
        }
    
    def _analyze_collaboration_patterns(self, events):
        """Analyze collaboration and interaction patterns"""
        collaborations = defaultdict(int)
        
        for event in events:
            if event['type'] in ['PullRequestEvent', 'IssueCommentEvent', 'PullRequestReviewEvent']:
                repo = event.get('repo', {}).get('name')
                if repo:
                    collaborations[repo] += 1
        
        return {
            'collaborative_repos': dict(collaborations),
            'collaboration_frequency': sum(collaborations.values()),
            'most_collaborated_repo': max(collaborations.items(), key=lambda x: x[1])[0] if collaborations else None
        }
    
    def _calculate_productivity_metrics(self, user_data):
        """Calculate productivity metrics"""
        events = user_data['events']
        contributions = user_data['contributions']
        
        if not events:
            return {}
        
        # Calculate daily average
        active_days = len(contributions['active_days'])
        daily_average = len(events) / active_days if active_days > 0 else 0
        
        # Calculate commit frequency
        push_events = [e for e in events if e['type'] == 'PushEvent']
        total_commits = sum(len(e.get('payload', {}).get('commits', [])) for e in push_events)
        
        return {
            'total_events': len(events),
            'active_days': active_days,
            'daily_average_events': round(daily_average, 2),
            'total_commits': total_commits,
            'commits_per_day': round(total_commits / active_days, 2) if active_days > 0 else 0
        }
