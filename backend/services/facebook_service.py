"""Facebook Search Service"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
FACEBOOK_API_VERSION = 'v18.0'
BASE_URL = f'https://graph.facebook.com/{FACEBOOK_API_VERSION}'

def search_facebook_posts(keyword, max_results=10):
    """
    Search public posts mentioning keyword on Facebook
    Note: Limited access, only public posts and pages you manage
    """
    if not FACEBOOK_ACCESS_TOKEN:
        return {'error': 'Facebook Access Token not configured'}
    
    try:
        # Search in public posts (limited functionality)
        url = f'{BASE_URL}/search'
        
        params = {
            'q': keyword,
            'type': 'post',
            'fields': 'id,message,created_time,story,permalink_url,type',
            'limit': max_results,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return {'error': f'Facebook API error: {response.status_code} - {response.text}'}
        
        data = response.json()
        
        results = []
        for post in data.get('data', []):
            result = {
                'id': post.get('id', ''),
                'platform': 'facebook',
                'text': post.get('message', post.get('story', '')),
                'created_at': post.get('created_time', ''),
                'url': post.get('permalink_url', ''),
                'type': post.get('type', 'post'),
                'likes': 'N/A',  # Need separate call for engagement
                'comments': 'N/A',
                'shares': 'N/A'
            }
            results.append(result)
        
        return {'success': True, 'results': results, 'total': len(results)}
        
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


def get_facebook_page_posts(page_id, max_results=10):
    """
    Get posts from a specific Facebook page you manage
    Requires page access token
    """
    if not FACEBOOK_ACCESS_TOKEN:
        return {'error': 'Facebook Access Token not configured'}
    
    try:
        url = f'{BASE_URL}/{page_id}/posts'
        
        params = {
            'fields': 'id,message,created_time,permalink_url,story,type,engagement',
            'limit': max_results,
            'access_token': FACEBOOK_ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return {'error': f'Facebook API error: {response.status_code}'}
        
        data = response.json()
        
        results = []
        for post in data.get('data', []):
            engagement = post.get('engagement', {})
            result = {
                'id': post.get('id', ''),
                'platform': 'facebook',
                'text': post.get('message', post.get('story', '')),
                'created_at': post.get('created_time', ''),
                'url': post.get('permalink_url', ''),
                'type': post.get('type', 'post'),
                'likes': engagement.get('like_count', 0),
                'comments': engagement.get('comment_count', 0),
                'shares': engagement.get('share_count', 0)
            }
            results.append(result)
        
        return {'success': True, 'results': results, 'total': len(results)}
        
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}
