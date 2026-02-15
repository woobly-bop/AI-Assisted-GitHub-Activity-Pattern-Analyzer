"""
AI/ML Models for Advanced Pattern Recognition
Currently uses rule-based analysis, can be extended with ML models
"""
import numpy as np
from collections import defaultdict


class ActivityPredictor:
    """Predicts future activity patterns based on historical data"""
    
    def __init__(self):
        self.model = None
    
    def predict_next_activity(self, patterns):
        """
        Predict likely next activity based on patterns
        
        Args:
            patterns (dict): Analyzed patterns from analyzer.py
            
        Returns:
            dict: Predictions about future activity
        """
        predictions = {
            'likely_next_event_type': self._predict_event_type(patterns),
            'likely_active_time': self._predict_active_time(patterns),
            'productivity_trend': self._analyze_productivity_trend(patterns)
        }
        
        return predictions
    
    def _predict_event_type(self, patterns):
        """Predict the most likely next event type"""
        activity_patterns = patterns.get('activity_patterns', {})
        event_dist = activity_patterns.get('event_type_distribution', {})
        
        if not event_dist:
            return None
        
        # Simple prediction: most common event type
        most_common = max(event_dist.items(), key=lambda x: x[1])
        
        return {
            'event_type': most_common[0],
            'confidence': most_common[1] / sum(event_dist.values())
        }
    
    def _predict_active_time(self, patterns):
        """Predict likely active hours"""
        time_patterns = patterns.get('time_patterns', {})
        peak_hours = time_patterns.get('peak_hours', [])
        
        if not peak_hours:
            return None
        
        return {
            'most_likely_hour': peak_hours[0]['hour'] if peak_hours else None,
            'peak_hours': [h['hour'] for h in peak_hours]
        }
    
    def _analyze_productivity_trend(self, patterns):
        """Analyze productivity trend"""
        metrics = patterns.get('productivity_metrics', {})
        daily_avg = metrics.get('daily_average_events', 0)
        
        # Simple classification
        if daily_avg > 10:
            trend = 'highly_active'
        elif daily_avg > 5:
            trend = 'moderately_active'
        elif daily_avg > 2:
            trend = 'occasionally_active'
        else:
            trend = 'low_activity'
        
        return {
            'trend': trend,
            'daily_average': daily_avg,
            'description': self._get_trend_description(trend)
        }
    
    def _get_trend_description(self, trend):
        """Get human-readable trend description"""
        descriptions = {
            'highly_active': 'User shows very high engagement with consistent daily activity',
            'moderately_active': 'User maintains regular activity with good consistency',
            'occasionally_active': 'User contributes periodically with moderate engagement',
            'low_activity': 'User shows minimal activity, possibly inactive or new account'
        }
        return descriptions.get(trend, 'Unknown activity pattern')


class DeveloperProfiler:
    """Creates developer profile based on activity patterns"""
    
    def create_profile(self, patterns, user_data):
        """
        Create comprehensive developer profile
        
        Args:
            patterns (dict): Analyzed patterns
            user_data (dict): Raw user data
            
        Returns:
            dict: Developer profile
        """
        lang_patterns = patterns.get('language_patterns', {})
        repo_patterns = patterns.get('repository_patterns', {})
        collab_patterns = patterns.get('collaboration_patterns', {})
        
        profile = {
            'expertise_level': self._determine_expertise_level(patterns, user_data),
            'primary_language': lang_patterns.get('primary_language'),
            'specialization': self._determine_specialization(lang_patterns),
            'collaboration_style': self._determine_collaboration_style(collab_patterns),
            'project_focus': self._determine_project_focus(repo_patterns),
            'activity_consistency': self._measure_consistency(patterns)
        }
        
        return profile
    
    def _determine_expertise_level(self, patterns, user_data):
        """Determine developer expertise level"""
        repo_count = patterns.get('repository_patterns', {}).get('total_repositories', 0)
        total_stars = patterns.get('repository_patterns', {}).get('total_stars', 0)
        diversity = patterns.get('language_patterns', {}).get('language_diversity', 0)
        
        # Simple scoring system
        score = 0
        score += min(repo_count / 10, 3)  # Max 3 points for repos
        score += min(total_stars / 100, 3)  # Max 3 points for stars
        score += min(diversity / 3, 2)  # Max 2 points for diversity
        
        if score >= 6:
            return 'expert'
        elif score >= 4:
            return 'intermediate'
        elif score >= 2:
            return 'beginner'
        else:
            return 'novice'
    
    def _determine_specialization(self, lang_patterns):
        """Determine area of specialization"""
        primary_lang = lang_patterns.get('primary_language')
        
        specializations = {
            'Python': 'Data Science/Backend Development',
            'JavaScript': 'Web Development',
            'TypeScript': 'Modern Web Development',
            'Java': 'Enterprise/Android Development',
            'Go': 'Systems/Backend Development',
            'Rust': 'Systems Programming',
            'C++': 'Systems/Game Development',
            'Ruby': 'Web Development',
            'PHP': 'Web Development'
        }
        
        return specializations.get(primary_lang, 'General Development')
    
    def _determine_collaboration_style(self, collab_patterns):
        """Determine collaboration style"""
        collab_freq = collab_patterns.get('collaboration_frequency', 0)
        
        if collab_freq > 50:
            return 'highly_collaborative'
        elif collab_freq > 20:
            return 'team_player'
        elif collab_freq > 5:
            return 'occasional_collaborator'
        else:
            return 'solo_developer'
    
    def _determine_project_focus(self, repo_patterns):
        """Determine project focus"""
        total_repos = repo_patterns.get('total_repositories', 0)
        avg_stars = repo_patterns.get('average_stars', 0)
        
        if avg_stars > 50:
            return 'quality_focused'
        elif total_repos > 50:
            return 'quantity_focused'
        else:
            return 'balanced'
    
    def _measure_consistency(self, patterns):
        """Measure activity consistency"""
        metrics = patterns.get('productivity_metrics', {})
        active_days = metrics.get('active_days', 0)
        daily_avg = metrics.get('daily_average_events', 0)
        
        if active_days > 60 and daily_avg > 3:
            return 'very_consistent'
        elif active_days > 30 and daily_avg > 2:
            return 'consistent'
        elif active_days > 15:
            return 'moderately_consistent'
        else:
            return 'sporadic'
