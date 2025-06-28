import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class SonifyTestCase(unittest.TestCase):
    """Test cases for the Sonify Flask application"""
    
    def setUp(self):
        """Set up test client and configuration"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Mock session data
        with self.client.session_transaction() as sess:
            sess['token_info'] = {
                'access_token': 'test_token',
                'refresh_token': 'test_refresh',
                'expires_at': 9999999999
            }
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_index_page(self):
        """Test that the index page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sonify', response.data)
        self.assertIn(b'Spotify Data Visualizer', response.data)
    
    def test_login_redirect(self):
        """Test that login redirects to Spotify OAuth"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_logout(self):
        """Test logout functionality"""
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Redirect to index
    
    def test_dashboard_requires_auth(self):
        """Test that dashboard requires authentication"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_visualizations_requires_auth(self):
        """Test that visualizations require authentication"""
        response = self.client.get('/visualizations')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_api_user_data_requires_auth(self):
        """Test that API endpoints require authentication"""
        response = self.client.get('/api/user-data')
        self.assertEqual(response.status_code, 401)
    
    def test_api_top_tracks_requires_auth(self):
        """Test that top tracks API requires authentication"""
        response = self.client.get('/api/top-tracks')
        self.assertEqual(response.status_code, 401)
    
    @patch('app.get_spotify_client')
    def test_dashboard_with_mock_data(self, mock_get_client):
        """Test dashboard with mocked Spotify data"""
        # Mock Spotify client
        mock_sp = MagicMock()
        mock_get_client.return_value = mock_sp
        
        # Mock user data
        mock_sp.current_user.return_value = {
            'id': 'test_user',
            'display_name': 'Test User',
            'images': [{'url': 'test.jpg'}],
            'followers': {'total': 100}
        }
        
        # Mock top tracks
        mock_sp.current_user_top_tracks.return_value = {
            'items': [
                {
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist'}],
                    'album': {'name': 'Test Album', 'images': [{'url': 'test.jpg'}]},
                    'popularity': 80,
                    'duration_ms': 180000
                }
            ]
        }
        
        # Mock top artists
        mock_sp.current_user_top_artists.return_value = {
            'items': [
                {
                    'name': 'Test Artist',
                    'genres': ['pop', 'rock'],
                    'images': [{'url': 'test.jpg'}],
                    'popularity': 85,
                    'followers': {'total': 1000}
                }
            ]
        }
        
        # Mock recently played
        mock_sp.current_user_recently_played.return_value = {
            'items': [
                {
                    'track': {
                        'name': 'Recent Track',
                        'artists': [{'name': 'Recent Artist'}],
                        'album': {'name': 'Recent Album'},
                        'duration_ms': 200000
                    },
                    'played_at': '2024-01-01T12:00:00Z'
                }
            ]
        }
        
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)
    
    @patch('app.get_spotify_client')
    def test_visualizations_page(self, mock_get_client):
        """Test visualizations page with mocked data"""
        mock_sp = MagicMock()
        mock_get_client.return_value = mock_sp
        
        # Mock data for visualizations
        mock_sp.current_user_top_tracks.return_value = {'items': []}
        mock_sp.current_user_top_artists.return_value = {'items': []}
        mock_sp.current_user_recently_played.return_value = {'items': []}
        
        response = self.client.get('/visualizations')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Visualizations', response.data)
    
    @patch('app.get_spotify_client')
    def test_mood_analysis_page(self, mock_get_client):
        """Test mood analysis page with mocked data"""
        mock_sp = MagicMock()
        mock_get_client.return_value = mock_sp
        
        # Mock top tracks for mood analysis
        mock_sp.current_user_top_tracks.return_value = {
            'items': [
                {
                    'id': 'track1',
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist'}],
                    'album': {'name': 'Test Album', 'images': [{'url': 'test.jpg'}]}
                }
            ]
        }
        
        # Mock audio features
        mock_sp.audio_features.return_value = [
            {
                'danceability': 0.8,
                'energy': 0.7,
                'valence': 0.6,
                'tempo': 120,
                'acousticness': 0.3,
                'instrumentalness': 0.1
            }
        ]
        
        response = self.client.get('/mood_analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mood Analysis', response.data)
    
    @patch('app.get_spotify_client')
    def test_insights_page(self, mock_get_client):
        """Test insights page with mocked data"""
        mock_sp = MagicMock()
        mock_get_client.return_value = mock_sp
        
        # Mock data for insights
        mock_sp.current_user_top_tracks.return_value = {'items': []}
        mock_sp.current_user_top_artists.return_value = {'items': []}
        mock_sp.current_user_recently_played.return_value = {'items': []}
        mock_sp.current_user_playlists.return_value = {'items': []}
        
        response = self.client.get('/insights')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Music Insights', response.data)
    
    @patch('app.get_spotify_client')
    def test_export_data(self, mock_get_client):
        """Test data export functionality"""
        mock_sp = MagicMock()
        mock_get_client.return_value = mock_sp
        
        # Mock data for export
        mock_sp.current_user_top_tracks.return_value = {
            'items': [
                {
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist'}],
                    'album': {'name': 'Test Album'},
                    'popularity': 80,
                    'duration_ms': 180000
                }
            ]
        }
        
        mock_sp.current_user_top_artists.return_value = {
            'items': [
                {
                    'name': 'Test Artist',
                    'popularity': 85,
                    'genres': ['pop', 'rock'],
                    'followers': {'total': 1000}
                }
            ]
        }
        
        response = self.client.get('/export-data')
        self.assertEqual(response.status_code, 302)  # Redirect after export
    
    def test_api_user_data(self):
        """Test API endpoint for user data"""
        response = self.client.get('/api/user-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
    
    def test_api_mood_insights(self):
        """Test API endpoint for mood insights"""
        response = self.client.get('/api/mood-insights')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('features', data)
    
    def test_invalid_route(self):
        """Test that invalid routes return 404"""
        response = self.client.get('/invalid-route')
        self.assertEqual(response.status_code, 404)

    def test_dark_theme_support(self):
        """Test that dark theme CSS variables are present"""
        response = self.client.get('/')
        self.assertIn(b'data-theme="light"', response.data)
        self.assertIn(b'--bg-primary', response.data)
        self.assertIn(b'--text-primary', response.data)

    def test_floating_action_button(self):
        """Test that floating action button is present when authenticated"""
        response = self.client.get('/dashboard')
        self.assertIn(b'fab', response.data)
        self.assertIn(b'Quick Actions', response.data)

    def test_mood_analysis_features(self):
        """Test mood analysis features are present"""
        response = self.client.get('/mood_analysis')
        self.assertIn(b'mood-radar-chart', response.data)
        self.assertIn(b'Music Personality', response.data)

    def test_insights_features(self):
        """Test insights features are present"""
        response = self.client.get('/insights')
        self.assertIn(b'Listening Patterns', response.data)
        self.assertIn(b'Genre Analysis', response.data)

class UtilsTestCase(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_format_duration(self):
        """Test duration formatting"""
        from utils import format_duration
        
        # Test various durations
        self.assertEqual(format_duration(60000), "1:00")  # 1 minute
        self.assertEqual(format_duration(90000), "1:30")  # 1 minute 30 seconds
        self.assertEqual(format_duration(30000), "0:30")  # 30 seconds
        self.assertEqual(format_duration(0), "0:00")      # 0 seconds
    
    def test_validate_spotify_credentials(self):
        """Test Spotify credentials validation"""
        from utils import validate_spotify_credentials
        
        # Valid credentials
        self.assertTrue(validate_spotify_credentials("valid_id", "valid_secret"))
        
        # Invalid credentials
        self.assertFalse(validate_spotify_credentials("", "valid_secret"))
        self.assertFalse(validate_spotify_credentials("valid_id", ""))
        self.assertFalse(validate_spotify_credentials("", ""))
        self.assertFalse(validate_spotify_credentials(None, "valid_secret"))
        self.assertFalse(validate_spotify_credentials("valid_id", None))

if __name__ == '__main__':
    unittest.main() 