"""
GitHub API Integration
Handles all GitHub data fetching operations
"""
import requests
from datetime import datetime, timedelta
import config


class GitHubAPI:
    """Class to handle GitHub API interactions"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = config.GITHUB_API_URL
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def fetch_user_activity(self, username):
        """
        Fetch comprehensive activity data for a GitHub user
        
        Args:
            username (str): GitHub username
            
        Returns:
            dict: User activity data including events, repos, and stats
        """
        user_data = {
            'username': username,
            'profile': self._get_user_profile(username),
            'events': self._get_user_events(username),
            'repositories': self._get_user_repos(username),
            'contributions': self._get_contribution_stats(username)
        }
        
        return user_data
    
    def _get_user_profile(self, username):
        """Fetch user profile information"""
        url = f'{self.base_url}/users/{username}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def _get_user_events(self, username):
        """Fetch recent user events"""
        url = f'{self.base_url}/users/{username}/events'
        params = {'per_page': min(config.MAX_EVENTS, 100)}
        
        events = []
        page = 1
        
        while len(events) < config.MAX_EVENTS:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            page_events = response.json()
            if not page_events:
                break
                
            events.extend(page_events)
            page += 1
        
        return events[:config.MAX_EVENTS]
    
    def _get_user_repos(self, username):
        """Fetch user repositories"""
        url = f'{self.base_url}/users/{username}/repos'
        params = {'sort': 'updated', 'per_page': 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def _get_contribution_stats(self, username):
        """
        Calculate contribution statistics
        Note: GitHub doesn't provide a direct API for contribution graph,
        this is computed from events data
        """
        events = self._get_user_events(username)
        
        stats = {
            'total_events': len(events),
            'event_types': {},
            'active_days': set(),
            'repositories_contributed': set()
        }
        
        for event in events:
            # Count event types
            event_type = event.get('type', 'Unknown')
            stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
            
            # Track active days
            created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            stats['active_days'].add(created_at.date().isoformat())
            
            # Track repositories
            if event.get('repo'):
                stats['repositories_contributed'].add(event['repo']['name'])
        
        # Convert sets to lists for JSON serialization
        stats['active_days'] = sorted(list(stats['active_days']), reverse=True)
        stats['repositories_contributed'] = list(stats['repositories_contributed'])
        
        return stats
