#!/usr/bin/env python3
"""
Sonify - Spotify Data Visualizer
Run script for the Flask application
"""

import os
import sys
from app import app
from config import config

def main():
    """Main function to run the Flask application"""
    
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Check if Spotify credentials are set
    if not os.getenv('SPOTIPY_CLIENT_ID') or not os.getenv('SPOTIPY_CLIENT_SECRET'):
        print("❌ Error: Spotify API credentials not found!")
        print("Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in your .env file")
        print("Get your credentials from: https://developer.spotify.com/dashboard/applications")
        sys.exit(1)
    
    # Configure the app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Create necessary directories
    os.makedirs('static/exports', exist_ok=True)
    os.makedirs('flask_session', exist_ok=True)
    
    print("🎶 Starting Sonify - Spotify Data Visualizer")
    print(f"📊 Environment: {config_name}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📝 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=app.config.get('DEBUG', False)
        )
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using Sonify!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 