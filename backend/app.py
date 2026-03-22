"""
Flask Application Entry Point
Handles API routes and serves the frontend
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import config
from github_api import GitHubAPI
from analyzer import PatternAnalyzer
from insights import InsightGenerator

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)

github_api = GitHubAPI(config.GITHUB_TOKEN)
analyzer = PatternAnalyzer()
insight_gen = InsightGenerator()


@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_activity():
    """
    Analyze GitHub activity for a given username
    Expects JSON: {"username": "github_username"}
    """
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Fetch GitHub data
        user_data = github_api.fetch_user_activity(username)
        
        # Analyze patterns
        patterns = analyzer.analyze_patterns(user_data)
        
        # Generate insights
        insights = insight_gen.generate_insights(patterns)
        
        return jsonify({
            'success': True,
            'data': user_data,
            'patterns': patterns,
            'insights': insights
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
