"""
Application Runner
Runs the Flask backend server
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("AI-Assisted GitHub Activity Pattern Analyzer")
    print("=" * 60)
    print(f"Server starting at http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    app.run()
