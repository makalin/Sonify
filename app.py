import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import plotly.graph_objects as go
import plotly.utils
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from utils import (
    process_listening_data, create_heatmap_data, create_top_items_chart,
    create_heatmap_chart, analyze_listening_patterns, format_duration,
    get_audio_features_summary, create_mood_analysis_chart, export_data_to_csv
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Spotify API configuration
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:5000/callback')

# Scopes for Spotify API access
SCOPES = [
    'user-read-recently-played',
    'user-top-read',
    'user-read-playback-state',
    'playlist-read-private',
    'user-read-private'
]

def create_spotify_oauth():
    """Create Spotify OAuth object"""
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=' '.join(SCOPES)
    )

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Initiate Spotify login"""
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback"""
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    if not token_info:
        flash('Failed to get access token', 'error')
        return redirect(url_for('index'))
    
    session['token_info'] = token_info
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

def get_spotify_client():
    """Get authenticated Spotify client"""
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    sp_oauth = create_spotify_oauth()
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    
    return spotipy.Spotify(auth=token_info['access_token'])

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        # Get user profile
        user = sp.current_user()
        
        # Get top tracks and artists
        top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
        top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
        
        # Get recently played tracks
        recent_tracks = sp.current_user_recently_played(limit=50)
        
        # Analyze listening patterns
        listening_data = process_listening_data(recent_tracks['items'])
        patterns = analyze_listening_patterns(listening_data.get('listening_times', []))
        
        return render_template('dashboard.html', 
                             user=user, 
                             top_tracks=top_tracks['items'],
                             top_artists=top_artists['items'],
                             recent_tracks=recent_tracks['items'],
                             patterns=patterns)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/visualizations')
def visualizations():
    """Visualizations page"""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        # Get data for visualizations
        top_tracks = sp.current_user_top_tracks(limit=50, time_range='short_term')
        top_artists = sp.current_user_top_artists(limit=50, time_range='short_term')
        recent_tracks = sp.current_user_recently_played(limit=100)
        
        # Create visualizations
        charts = create_visualizations(top_tracks, top_artists, recent_tracks)
        
        return render_template('visualizations.html', charts=charts)
    except Exception as e:
        flash(f'Error loading visualizations: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/mood-analysis')
def mood_analysis():
    """Mood analysis page with audio features"""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        # Get top tracks for analysis
        top_tracks = sp.current_user_top_tracks(limit=50, time_range='short_term')
        
        # Get audio features for tracks
        track_ids = [track['id'] for track in top_tracks['items']]
        audio_features = sp.audio_features(track_ids)
        
        # Process audio features
        features_summary = get_audio_features_summary(audio_features)
        
        # Create mood analysis chart
        mood_chart = create_mood_analysis_chart(features_summary)
        
        # Analyze mood characteristics
        mood_insights = analyze_mood_characteristics(features_summary)
        
        return render_template('mood_analysis.html', 
                             features_summary=features_summary,
                             mood_chart=mood_chart,
                             mood_insights=mood_insights,
                             tracks_with_features=zip(top_tracks['items'], audio_features))
    except Exception as e:
        flash(f'Error loading mood analysis: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/insights')
def insights():
    """Detailed insights page"""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        # Get comprehensive data
        top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
        top_artists = sp.current_user_top_artists(limit=20, time_range='short_term')
        recent_tracks = sp.current_user_recently_played(limit=100)
        
        # Get user's playlists
        playlists = sp.current_user_playlists(limit=20)
        
        # Analyze data
        listening_data = process_listening_data(recent_tracks['items'])
        patterns = analyze_listening_patterns(listening_data.get('listening_times', []))
        
        # Generate insights
        insights_data = generate_insights(top_tracks, top_artists, recent_tracks, playlists)
        
        return render_template('insights.html', 
                             insights=insights_data,
                             patterns=patterns,
                             playlists=playlists['items'])
    except Exception as e:
        flash(f'Error loading insights: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/export-data')
def export_data():
    """Export user data as CSV"""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        # Get user data
        top_tracks = sp.current_user_top_tracks(limit=100, time_range='short_term')
        top_artists = sp.current_user_top_artists(limit=100, time_range='short_term')
        
        # Prepare data for export
        export_data = {
            'tracks': [],
            'artists': []
        }
        
        for track in top_tracks['items']:
            export_data['tracks'].append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'duration': format_duration(track['duration_ms'])
            })
        
        for artist in top_artists['items']:
            export_data['artists'].append({
                'name': artist['name'],
                'popularity': artist['popularity'],
                'genres': ', '.join(artist['genres'][:3]),
                'followers': artist['followers']['total']
            })
        
        # Export to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'sonify_data_{timestamp}'
        export_path = export_data_to_csv(export_data, filename)
        
        if export_path:
            flash('Data exported successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error exporting data', 'error')
            return redirect(url_for('dashboard'))
            
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

def create_visualizations(top_tracks, top_artists, recent_tracks):
    """Create Plotly visualizations"""
    charts = {}
    
    # Top tracks chart
    if top_tracks['items']:
        track_names = [track['name'] for track in top_tracks['items']]
        track_popularity = [track['popularity'] for track in top_tracks['items']]
        
        fig_tracks = go.Figure(data=[
            go.Bar(x=track_names, y=track_popularity, 
                   marker_color='rgb(30, 215, 96)')
        ])
        fig_tracks.update_layout(
            title='Your Top Tracks',
            xaxis_title='Track',
            yaxis_title='Popularity',
            template='plotly_dark'
        )
        charts['top_tracks'] = json.dumps(fig_tracks, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Top artists chart
    if top_artists['items']:
        artist_names = [artist['name'] for artist in top_artists['items']]
        artist_popularity = [artist['popularity'] for artist in top_artists['items']]
        
        fig_artists = go.Figure(data=[
            go.Bar(x=artist_names, y=artist_popularity,
                   marker_color='rgb(255, 107, 107)')
        ])
        fig_artists.update_layout(
            title='Your Top Artists',
            xaxis_title='Artist',
            yaxis_title='Popularity',
            template='plotly_dark'
        )
        charts['top_artists'] = json.dumps(fig_artists, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Listening time heatmap
    if recent_tracks['items']:
        # Create listening time data
        listening_times = []
        for item in recent_tracks['items']:
            played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
            listening_times.append({
                'hour': played_at.hour,
                'day': played_at.strftime('%A'),
                'date': played_at.date()
            })
        
        # Create heatmap data
        heatmap_data = create_heatmap_data(listening_times)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=list(range(24)),
            y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(
            title='Listening Time Heatmap',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            template='plotly_dark'
        )
        charts['heatmap'] = json.dumps(fig_heatmap, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

def analyze_mood_characteristics(features_summary):
    """Analyze mood characteristics from audio features"""
    insights = {}
    
    if not features_summary:
        return insights
    
    # Energy analysis
    energy = features_summary.get('energy', 0)
    if energy > 0.7:
        insights['energy'] = 'High energy - You prefer energetic, upbeat music!'
    elif energy > 0.4:
        insights['energy'] = 'Moderate energy - You enjoy a balanced mix of energetic and calm music.'
    else:
        insights['energy'] = 'Low energy - You prefer calm, relaxing music.'
    
    # Valence (happiness) analysis
    valence = features_summary.get('valence', 0)
    if valence > 0.7:
        insights['mood'] = 'Positive mood - Your music choices reflect a happy, upbeat personality!'
    elif valence > 0.4:
        insights['mood'] = 'Balanced mood - You enjoy a mix of happy and melancholic music.'
    else:
        insights['mood'] = 'Melancholic mood - You prefer introspective, emotional music.'
    
    # Danceability analysis
    danceability = features_summary.get('danceability', 0)
    if danceability > 0.7:
        insights['dance'] = 'High danceability - You love music you can dance to!'
    elif danceability > 0.4:
        insights['dance'] = 'Moderate danceability - You enjoy some danceable tracks.'
    else:
        insights['dance'] = 'Low danceability - You prefer music for listening rather than dancing.'
    
    # Acousticness analysis
    acousticness = features_summary.get('acousticness', 0)
    if acousticness > 0.7:
        insights['acoustic'] = 'High acoustic preference - You love organic, acoustic sounds!'
    elif acousticness > 0.4:
        insights['acoustic'] = 'Mixed acoustic preference - You enjoy both acoustic and electronic music.'
    else:
        insights['acoustic'] = 'Electronic preference - You prefer electronic and produced music.'
    
    return insights

def generate_insights(top_tracks, top_artists, recent_tracks, playlists):
    """Generate comprehensive insights about user's music taste"""
    insights = {}
    
    # Genre analysis
    all_genres = []
    for artist in top_artists['items']:
        all_genres.extend(artist['genres'])
    
    genre_counts = {}
    for genre in all_genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    insights['top_genres'] = top_genres
    
    # Listening time analysis
    if recent_tracks['items']:
        listening_data = process_listening_data(recent_tracks['items'])
        patterns = analyze_listening_patterns(listening_data.get('listening_times', []))
        insights['listening_patterns'] = patterns
    
    # Artist diversity
    unique_artists = len(set([track['artists'][0]['id'] for track in top_tracks['items']]))
    insights['artist_diversity'] = {
        'unique_artists': unique_artists,
        'total_tracks': len(top_tracks['items']),
        'diversity_score': unique_artists / len(top_tracks['items']) if top_tracks['items'] else 0
    }
    
    # Playlist analysis
    if playlists['items']:
        insights['playlist_count'] = len(playlists['items'])
        insights['total_playlist_tracks'] = sum(playlist['tracks']['total'] for playlist in playlists['items'])
    
    return insights

@app.route('/api/user-data')
def api_user_data():
    """API endpoint for user data"""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        user = sp.current_user()
        return jsonify({
            'id': user['id'],
            'display_name': user['display_name'],
            'email': user.get('email', ''),
            'country': user.get('country', ''),
            'followers': user['followers']['total'] if user['followers'] else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-tracks')
def api_top_tracks():
    """API endpoint for top tracks"""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        time_range = request.args.get('time_range', 'short_term')
        limit = int(request.args.get('limit', 20))
        
        top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        
        tracks_data = []
        for track in top_tracks['items']:
            tracks_data.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        
        return jsonify(tracks_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mood-insights')
def api_mood_insights():
    """API endpoint for mood insights"""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
        track_ids = [track['id'] for track in top_tracks['items']]
        audio_features = sp.audio_features(track_ids)
        
        features_summary = get_audio_features_summary(audio_features)
        mood_insights = analyze_mood_characteristics(features_summary)
        
        return jsonify({
            'features': features_summary,
            'insights': mood_insights
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 