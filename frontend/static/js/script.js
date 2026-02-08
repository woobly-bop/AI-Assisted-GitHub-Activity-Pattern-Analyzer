// API Configuration
const API_URL = 'http://127.0.0.1:5000';

// DOM Elements
const usernameInput = document.getElementById('username-input');
const analyzeBtn = document.getElementById('analyze-btn');
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const errorMessageEl = document.getElementById('error-message');
const resultsEl = document.getElementById('results');

// Event Listeners
analyzeBtn.addEventListener('click', handleAnalyze);
usernameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleAnalyze();
    }
});

// Main Analysis Function
async function handleAnalyze() {
    const username = usernameInput.value.trim();
    
    if (!username) {
        showError('Please enter a GitHub username');
        return;
    }
    
    showLoading();
    hideError();
    hideResults();
    
    try {
        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze activity');
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Display Functions
function displayResults(data) {
    const { data: userData, patterns, insights } = data;
    
    // Display Profile
    displayProfile(userData.profile);
    
    // Display Insights Summary
    displayInsightsSummary(insights.summary);
    
    // Display Productivity Metrics
    displayProductivityMetrics(patterns.productivity_metrics);
    
    // Display Language Distribution
    displayLanguageChart(patterns.language_patterns);
    
    // Display Time Patterns
    displayTimePatterns(patterns.time_patterns);
    
    // Display Activity Types
    displayActivityTypes(patterns.activity_patterns);
    
    // Display Recommendations
    displayRecommendations(insights);
    
    showResults();
}

function displayProfile(profile) {
    document.getElementById('user-avatar').src = profile.avatar_url;
    document.getElementById('user-name').textContent = profile.name || profile.login;
    document.getElementById('user-bio').textContent = profile.bio || 'No bio available';
    document.getElementById('user-repos').textContent = profile.public_repos || 0;
    document.getElementById('user-followers').textContent = profile.followers || 0;
    document.getElementById('user-following').textContent = profile.following || 0;
}

function displayInsightsSummary(summary) {
    document.getElementById('insights-summary').textContent = summary;
}

function displayProductivityMetrics(metrics) {
    const container = document.getElementById('productivity-metrics');
    container.innerHTML = '';
    
    const metricsToDisplay = [
        { label: 'Total Events', value: metrics.total_events },
        { label: 'Active Days', value: metrics.active_days },
        { label: 'Daily Average', value: metrics.daily_average_events },
        { label: 'Total Commits', value: metrics.total_commits },
        { label: 'Commits/Day', value: metrics.commits_per_day }
    ];
    
    metricsToDisplay.forEach(metric => {
        const item = createMetricItem(metric.label, metric.value);
        container.appendChild(item);
    });
}

function displayLanguageChart(langPatterns) {
    const container = document.getElementById('language-chart');
    container.innerHTML = '';
    
    const languages = langPatterns.language_distribution || {};
    const sortedLangs = Object.entries(languages)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const maxCount = sortedLangs[0] ? sortedLangs[0][1] : 1;
    
    sortedLangs.forEach(([lang, count]) => {
        const bar = createChartBar(lang, count, maxCount);
        container.appendChild(bar);
    });
}

function displayTimePatterns(timePatterns) {
    const container = document.getElementById('time-patterns');
    container.innerHTML = '';
    
    const peakHours = timePatterns.peak_hours || [];
    const mostActiveDay = timePatterns.most_active_day;
    
    if (peakHours.length > 0) {
        const item = document.createElement('div');
        item.className = 'pattern-item';
        item.innerHTML = `
            <h4>Peak Activity Hours</h4>
            <p>${peakHours.map(h => `${h.hour}:00 (${h.count} events)`).join(', ')}</p>
        `;
        container.appendChild(item);
    }
    
    if (mostActiveDay) {
        const item = document.createElement('div');
        item.className = 'pattern-item';
        item.innerHTML = `
            <h4>Most Active Day</h4>
            <p>${mostActiveDay}</p>
        `;
        container.appendChild(item);
    }
}

function displayActivityTypes(activityPatterns) {
    const container = document.getElementById('activity-types');
    container.innerHTML = '';
    
    const events = activityPatterns.event_type_distribution || {};
    const sortedEvents = Object.entries(events)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const maxCount = sortedEvents[0] ? sortedEvents[0][1] : 1;
    
    sortedEvents.forEach(([type, count]) => {
        const bar = createChartBar(type.replace('Event', ''), count, maxCount);
        container.appendChild(bar);
    });
}

function displayRecommendations(insights) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';
    
    const recommendations = insights.recommendations || [];
    
    recommendations.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <div class="recommendation-icon">💡</div>
            <div class="recommendation-text">${rec}</div>
        `;
        container.appendChild(item);
    });
}

// Helper Functions
function createMetricItem(label, value) {
    const item = document.createElement('div');
    item.className = 'metric-item';
    item.innerHTML = `
        <span class="metric-label">${label}</span>
        <span class="metric-value">${value}</span>
    `;
    return item;
}

function createChartBar(label, value, maxValue) {
    const percentage = (value / maxValue) * 100;
    const bar = document.createElement('div');
    bar.className = 'chart-bar';
    bar.innerHTML = `
        <span class="chart-label">${label}</span>
        <div class="chart-bar-fill" style="width: ${percentage}%"></div>
        <span class="chart-value">${value}</span>
    `;
    return bar;
}

// UI State Functions
function showLoading() {
    loadingEl.classList.remove('hidden');
}

function hideLoading() {
    loadingEl.classList.add('hidden');
}

function showError(message) {
    errorMessageEl.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError() {
    errorEl.classList.add('hidden');
}

function showResults() {
    resultsEl.classList.remove('hidden');
}

function hideResults() {
    resultsEl.classList.add('hidden');
}
