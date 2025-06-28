import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.utils
import os

def process_listening_data(recent_tracks: List[Dict]) -> Dict[str, Any]:
    """
    Process recently played tracks data for analysis
    
    Args:
        recent_tracks: List of recently played track objects from Spotify API
        
    Returns:
        Dictionary containing processed listening data
    """
    if not recent_tracks:
        return {}
    
    listening_times = []
    total_duration = 0
    track_counts = {}
    artist_counts = {}
    genre_counts = {}
    
    for item in recent_tracks:
        track = item['track']
        played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
        
        # Track listening time data
        listening_times.append({
            'hour': played_at.hour,
            'day': played_at.strftime('%A'),
            'date': played_at.date(),
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name']
        })
        
        # Track counts
        track_name = track['name']
        track_counts[track_name] = track_counts.get(track_name, 0) + 1
        
        # Artist counts
        for artist in track['artists']:
            artist_name = artist['name']
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1
        
        if 'duration_ms' in track:
            total_duration += track['duration_ms']
    
    return {
        'listening_times': listening_times,
        'total_duration': total_duration,
        'total_tracks': len(recent_tracks),
        'track_counts': track_counts,
        'artist_counts': artist_counts,
        'genre_counts': genre_counts
    }

def create_heatmap_data(listening_times: List[Dict]) -> np.ndarray:
    """
    Create heatmap data from listening times
    
    Args:
        listening_times: List of listening time dictionaries
        
    Returns:
        2D numpy array for heatmap visualization
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    
    heatmap_data = np.zeros((len(days), len(hours)))
    
    for time_data in listening_times:
        day_idx = days.index(time_data['day'])
        hour_idx = time_data['hour']
        heatmap_data[day_idx][hour_idx] += 1
    
    return heatmap_data

def create_top_items_chart(items: List[Dict], item_type: str = 'tracks', limit: int = 10) -> str:
    """
    Create a bar chart for top tracks or artists
    
    Args:
        items: List of track or artist objects
        item_type: Type of items ('tracks' or 'artists')
        limit: Number of items to include
        
    Returns:
        JSON string of Plotly chart
    """
    if not items:
        return ""
    
    # Get top items
    top_items = items[:limit]
    
    if item_type == 'tracks':
        names = [track['name'] for track in top_items]
        values = [track['popularity'] for track in top_items]
        color = 'rgb(30, 215, 96)'  # Spotify green
        title = 'Your Top Tracks'
        xaxis_title = 'Track'
    else:  # artists
        names = [artist['name'] for artist in top_items]
        values = [artist['popularity'] for artist in top_items]
        color = 'rgb(255, 107, 107)'  # Red
        title = 'Your Top Artists'
        xaxis_title = 'Artist'
    
    fig = go.Figure(data=[
        go.Bar(x=names, y=values, marker_color=color)
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title='Popularity',
        template='plotly_dark',
        showlegend=False
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_heatmap_chart(heatmap_data: np.ndarray) -> str:
    """
    Create a heatmap chart from listening data
    
    Args:
        heatmap_data: 2D numpy array of listening frequency
        
    Returns:
        JSON string of Plotly heatmap
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=hours,
        y=days,
        colorscale='Viridis',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Listening Time Heatmap',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        template='plotly_dark'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def analyze_listening_patterns(listening_times: List[Dict]) -> Dict[str, Any]:
    """
    Analyze listening patterns from time data
    
    Args:
        listening_times: List of listening time dictionaries
        
    Returns:
        Dictionary containing pattern analysis
    """
    if not listening_times:
        return {}
    
    df = pd.DataFrame(listening_times)
    
    # Count listening by hour
    hour_counts = {}
    for time_data in listening_times:
        hour = time_data['hour']
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    # Count listening by day
    day_counts = {}
    for time_data in listening_times:
        day = time_data['day']
        day_counts[day] = day_counts.get(day, 0) + 1
    
    # Find most active hour and day
    most_active_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else 0
    most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 'Unknown'
    
    # Calculate time range
    dates = [time_data['date'] for time_data in listening_times]
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        time_range_days = (max_date - min_date).days + 1
        unique_days = len(set(dates))
    else:
        time_range_days = 0
        unique_days = 0
    
    return {
        'most_active_hour': most_active_hour,
        'most_active_day': most_active_day,
        'total_sessions': len(listening_times),
        'avg_sessions_per_day': round(len(listening_times) / max(time_range_days, 1), 1),
        'time_range_days': time_range_days,
        'unique_days': unique_days,
        'hour_distribution': hour_counts,
        'day_distribution': day_counts
    }

def format_duration(duration_ms: int) -> str:
    """
    Format duration from milliseconds to mm:ss format
    
    Args:
        duration_ms: Duration in milliseconds
        
    Returns:
        Formatted duration string
    """
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

def get_audio_features_summary(tracks: List[Dict]) -> Dict[str, float]:
    """
    Calculate average audio features from a list of tracks
    
    Args:
        tracks: List of track objects with audio features
        
    Returns:
        Dictionary of average audio features
    """
    if not tracks:
        return {}
    
    features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']
    summary = {}
    
    for feature in features:
        values = [track.get(feature, 0) for track in tracks if track.get(feature) is not None]
        if values:
            summary[feature] = round(sum(values) / len(values), 3)
    
    return summary

def create_mood_analysis_chart(audio_features: Dict[str, float]) -> str:
    """
    Create a radar chart for mood analysis based on audio features
    
    Args:
        audio_features: Dictionary of audio features
        
    Returns:
        JSON string of Plotly radar chart
    """
    if not audio_features:
        return ""
    
    # Select relevant features for mood analysis
    mood_features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
    available_features = {k: v for k, v in audio_features.items() if k in mood_features}
    
    if not available_features:
        return ""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(available_features.values()),
        theta=list(available_features.keys()),
        fill='toself',
        name='Your Music Profile',
        line_color='rgb(30, 215, 96)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title='Your Music Mood Profile',
        template='plotly_dark'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def export_data_to_csv(data: Dict[str, Any], filename: str) -> str:
    """
    Export data to CSV format
    
    Args:
        data: Dictionary containing data to export
        filename: Name of the file to create
        
    Returns:
        Path to the created CSV file
    """
    try:
        if 'tracks' in data:
            df = pd.DataFrame(data['tracks'])
            df.to_csv(f'static/exports/{filename}_tracks.csv', index=False)
        
        if 'artists' in data:
            df = pd.DataFrame(data['artists'])
            df.to_csv(f'static/exports/{filename}_artists.csv', index=False)
        
        return f'static/exports/{filename}'
    except Exception as e:
        print(f"Error exporting data: {e}")
        return ""

def validate_spotify_credentials(client_id: str, client_secret: str) -> bool:
    """
    Validate Spotify API credentials
    
    Args:
        client_id: Spotify client ID
        client_secret: Spotify client secret
        
    Returns:
        True if credentials are valid, False otherwise
    """
    return bool(client_id and client_secret and len(client_id) > 0 and len(client_secret) > 0)

def create_genre_analysis_chart(artists_data):
    """Create a genre analysis chart"""
    if not artists_data:
        return None
    
    # Collect all genres
    all_genres = []
    for artist in artists_data:
        all_genres.extend(artist.get('genres', []))
    
    # Count genre occurrences
    genre_counts = {}
    for genre in all_genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Get top genres
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if not top_genres:
        return None
    
    genres, counts = zip(*top_genres)
    
    fig = go.Figure(data=[
        go.Bar(x=list(genres), y=list(counts), marker_color='rgb(255, 107, 107)')
    ])
    
    fig.update_layout(
        title='Top Genres',
        xaxis_title='Genre',
        yaxis_title='Number of Artists',
        template='plotly_dark'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def analyze_music_taste_complexity(audio_features):
    """Analyze the complexity of music taste based on audio features"""
    if not audio_features:
        return {}
    
    valid_features = [f for f in audio_features if f is not None]
    
    if not valid_features:
        return {}
    
    # Calculate standard deviations to measure variety
    features_to_analyze = ['danceability', 'energy', 'valence', 'acousticness']
    
    complexity_scores = {}
    for feature in features_to_analyze:
        values = [f.get(feature, 0) for f in valid_features if f.get(feature) is not None]
        if len(values) > 1:
            complexity_scores[feature] = np.std(values)
        else:
            complexity_scores[feature] = 0
    
    # Overall complexity score
    overall_complexity = sum(complexity_scores.values()) / len(complexity_scores)
    
    return {
        'overall_complexity': overall_complexity,
        'feature_complexity': complexity_scores,
        'complexity_level': 'High' if overall_complexity > 0.3 else 'Medium' if overall_complexity > 0.15 else 'Low'
    }

def create_listening_timeline_chart(listening_times):
    """Create a timeline chart of listening activity"""
    if not listening_times:
        return None
    
    # Group by date
    date_counts = {}
    for time_data in listening_times:
        date = time_data['date']
        date_counts[date] = date_counts.get(date, 0) + 1
    
    # Sort by date
    sorted_dates = sorted(date_counts.items())
    dates, counts = zip(*sorted_dates)
    
    fig = go.Figure(data=[
        go.Scatter(x=list(dates), y=list(counts), mode='lines+markers', 
                  line=dict(color='rgb(30, 215, 96)', width=3),
                  marker=dict(size=8, color='rgb(30, 215, 96)'))
    ])
    
    fig.update_layout(
        title='Listening Activity Timeline',
        xaxis_title='Date',
        yaxis_title='Number of Tracks',
        template='plotly_dark'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generate_music_personality_insights(audio_features, listening_patterns):
    """Generate personality insights based on music data"""
    insights = []
    
    if audio_features:
        features_summary = get_audio_features_summary(audio_features)
        
        # Energy insights
        energy = features_summary.get('energy', 0)
        if energy > 0.7:
            insights.append("You prefer high-energy music, suggesting an active and dynamic personality.")
        elif energy < 0.3:
            insights.append("You enjoy calm, low-energy music, indicating a reflective and peaceful nature.")
        
        # Valence (happiness) insights
        valence = features_summary.get('valence', 0)
        if valence > 0.7:
            insights.append("Your music choices are predominantly positive, reflecting an optimistic outlook.")
        elif valence < 0.3:
            insights.append("You gravitate toward melancholic music, suggesting depth and emotional sensitivity.")
        
        # Danceability insights
        danceability = features_summary.get('danceability', 0)
        if danceability > 0.7:
            insights.append("You love danceable music, indicating a social and energetic personality.")
        elif danceability < 0.3:
            insights.append("You prefer music for listening rather than dancing, suggesting an introspective nature.")
    
    if listening_patterns:
        # Listening time insights
        most_active_hour = listening_patterns.get('most_active_hour', 0)
        if most_active_hour < 12:
            insights.append("You're most active in the morning, suggesting you're an early bird.")
        elif most_active_hour > 18:
            insights.append("You're most active in the evening, indicating you're a night owl.")
        
        # Consistency insights
        avg_sessions = listening_patterns.get('avg_sessions_per_day', 0)
        if avg_sessions > 10:
            insights.append("You listen to music constantly, showing it's a central part of your life.")
        elif avg_sessions < 3:
            insights.append("You listen to music occasionally, suggesting it's a background element.")
    
    return insights

def create_playlist_analysis_chart(playlists_data):
    """Create a chart analyzing playlist characteristics"""
    if not playlists_data:
        return None
    
    # Extract playlist sizes
    playlist_sizes = [playlist.get('tracks', {}).get('total', 0) for playlist in playlists_data]
    playlist_names = [playlist.get('name', f'Playlist {i+1}') for i, playlist in enumerate(playlists_data)]
    
    fig = go.Figure(data=[
        go.Bar(x=playlist_names, y=playlist_sizes, marker_color='rgb(138, 43, 226)')
    ])
    
    fig.update_layout(
        title='Playlist Sizes',
        xaxis_title='Playlist',
        yaxis_title='Number of Tracks',
        template='plotly_dark'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 