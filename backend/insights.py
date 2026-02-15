"""
Insights Generation
Converts analyzed data into human-readable insights
"""
from ml_model import ActivityPredictor, DeveloperProfiler


class InsightGenerator:
    """Generates human-readable insights from analyzed patterns"""
    
    def __init__(self):
        self.predictor = ActivityPredictor()
        self.profiler = DeveloperProfiler()
    
    def generate_insights(self, patterns, user_data=None):
        """
        Generate comprehensive insights from patterns
        
        Args:
            patterns (dict): Analyzed patterns from analyzer.py
            user_data (dict): Optional user data for enhanced insights
            
        Returns:
            dict: Human-readable insights
        """
        insights = {
            'summary': self._generate_summary(patterns),
            'time_insights': self._generate_time_insights(patterns),
            'activity_insights': self._generate_activity_insights(patterns),
            'language_insights': self._generate_language_insights(patterns),
            'productivity_insights': self._generate_productivity_insights(patterns),
            'recommendations': self._generate_recommendations(patterns)
        }
        
        # Add predictions if user_data is available
        if user_data:
            insights['predictions'] = self.predictor.predict_next_activity(patterns)
            insights['developer_profile'] = self.profiler.create_profile(patterns, user_data)
        
        return insights
    
    def _generate_summary(self, patterns):
        """Generate overall summary"""
        metrics = patterns.get('productivity_metrics', {})
        repo_patterns = patterns.get('repository_patterns', {})
        lang_patterns = patterns.get('language_patterns', {})
        
        summary = f"Developer has been active for {metrics.get('active_days', 0)} days with "
        summary += f"{metrics.get('total_events', 0)} total events. "
        summary += f"Primary language is {lang_patterns.get('primary_language', 'Unknown')} "
        summary += f"with {repo_patterns.get('total_repositories', 0)} repositories."
        
        return summary
    
    def _generate_time_insights(self, patterns):
        """Generate insights about time patterns"""
        time_patterns = patterns.get('time_patterns', {})
        peak_hours = time_patterns.get('peak_hours', [])
        most_active_day = time_patterns.get('most_active_day')
        
        insights = []
        
        if peak_hours:
            top_hour = peak_hours[0]['hour']
            time_period = self._get_time_period(top_hour)
            insights.append(f"Most active during {time_period} hours (around {top_hour}:00)")
        
        if most_active_day:
            insights.append(f"Most productive on {most_active_day}s")
        
        return insights
    
    def _generate_activity_insights(self, patterns):
        """Generate insights about activity types"""
        activity_patterns = patterns.get('activity_patterns', {})
        event_dist = activity_patterns.get('event_type_distribution', {})
        
        insights = []
        
        # Analyze Push events
        if 'PushEvent' in event_dist:
            push_count = event_dist['PushEvent']
            total = sum(event_dist.values())
            push_percentage = (push_count / total * 100) if total > 0 else 0
            insights.append(f"Pushes code frequently ({push_percentage:.1f}% of activity)")
        
        # Analyze Pull Request events
        if 'PullRequestEvent' in event_dist:
            insights.append("Actively participates in code reviews via pull requests")
        
        # Analyze Issue events
        if 'IssuesEvent' in event_dist:
            insights.append("Engages in issue tracking and project management")
        
        # Analyze diversity
        diversity = activity_patterns.get('activity_diversity', 0)
        if diversity > 5:
            insights.append("Shows diverse contribution patterns across multiple activity types")
        
        return insights
    
    def _generate_language_insights(self, patterns):
        """Generate insights about programming languages"""
        lang_patterns = patterns.get('language_patterns', {})
        lang_dist = lang_patterns.get('language_distribution', {})
        primary = lang_patterns.get('primary_language')
        diversity = lang_patterns.get('language_diversity', 0)
        
        insights = []
        
        if primary:
            insights.append(f"Primary expertise in {primary}")
        
        if diversity > 5:
            insights.append(f"Polyglot developer with experience in {diversity} languages")
        elif diversity > 3:
            insights.append(f"Works with multiple languages ({diversity} total)")
        
        # Check for trending languages
        trending = {'Rust', 'Go', 'TypeScript', 'Kotlin'}
        user_langs = set(lang_dist.keys())
        if user_langs & trending:
            trending_used = user_langs & trending
            insights.append(f"Adopts modern languages: {', '.join(trending_used)}")
        
        return insights
    
    def _generate_productivity_insights(self, patterns):
        """Generate productivity-related insights"""
        metrics = patterns.get('productivity_metrics', {})
        repo_patterns = patterns.get('repository_patterns', {})
        
        insights = []
        
        daily_avg = metrics.get('daily_average_events', 0)
        if daily_avg > 10:
            insights.append("Extremely active developer with high daily engagement")
        elif daily_avg > 5:
            insights.append("Maintains consistent daily activity")
        elif daily_avg > 2:
            insights.append("Regular contributor with steady activity")
        
        commits_per_day = metrics.get('commits_per_day', 0)
        if commits_per_day > 5:
            insights.append(f"High commit frequency ({commits_per_day:.1f} commits/day)")
        
        total_stars = repo_patterns.get('total_stars', 0)
        if total_stars > 100:
            insights.append(f"Creates popular projects ({total_stars} total stars)")
        
        return insights
    
    def _generate_recommendations(self, patterns):
        """Generate actionable recommendations"""
        recommendations = []
        
        metrics = patterns.get('productivity_metrics', {})
        lang_patterns = patterns.get('language_patterns', {})
        collab_patterns = patterns.get('collaboration_patterns', {})
        
        # Activity recommendations
        active_days = metrics.get('active_days', 0)
        if active_days < 30:
            recommendations.append("Consider maintaining more consistent activity for better project momentum")
        
        # Language diversity
        diversity = lang_patterns.get('language_diversity', 0)
        if diversity < 3:
            recommendations.append("Explore additional programming languages to broaden your skill set")
        
        # Collaboration
        collab_freq = collab_patterns.get('collaboration_frequency', 0)
        if collab_freq < 10:
            recommendations.append("Increase collaboration through code reviews and pull requests")
        
        # Documentation
        recommendations.append("Continue documenting your projects to increase visibility and adoption")
        
        return recommendations
    
    def _get_time_period(self, hour):
        """Convert hour to time period description"""
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
