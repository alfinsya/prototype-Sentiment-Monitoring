"""Instagram Search Service using Instagram Graph API"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
BASE_URL = 'https://graph.instagram.com/v18.0'

def search_instagram_hashtag(keyword, max_results=10):
    """
    Search Instagram posts by hashtag using Instagram Graph API
    Requires Instagram Business Account and valid access token
    """
    if not INSTAGRAM_ACCESS_TOKEN:
        return {
            'success': False,
            'error': 'Instagram Access Token not configured',
            'results': []
        }
    
    try:
        # First, search for hashtag
        hashtag_url = f'{BASE_URL}/ig_hashtag_search'
        
        hashtag_params = {
            'user_id': INSTAGRAM_BUSINESS_ACCOUNT_ID,
            'fields': 'id,name',
            'access_token': INSTAGRAM_ACCESS_TOKEN
        }
        
        # Add search query
        hashtag_params['q'] = keyword
        
        hashtag_response = requests.get(hashtag_url, params=hashtag_params)
        
        if hashtag_response.status_code != 200:
            return {
                'success': False,
                'error': f'Instagram Hashtag search error: {hashtag_response.status_code}',
                'results': []
            }
        
        hashtag_data = hashtag_response.json()
        
        if not hashtag_data.get('data'):
            return {
                'success': True,
                'results': [],
                'total': 0,
                'message': f'No hashtag found for "{keyword}"'
            }
        
        hashtag_id = hashtag_data['data'][0]['id']
        
        # Get recent posts from hashtag
        posts_url = f'{BASE_URL}/{hashtag_id}/recent_media'
        
        posts_params = {
            'user_id': INSTAGRAM_BUSINESS_ACCOUNT_ID,
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
            'limit': max_results,
            'access_token': INSTAGRAM_ACCESS_TOKEN
        }
        
        posts_response = requests.get(posts_url, params=posts_params)
        
        if posts_response.status_code != 200:
            return {
                'success': False,
                'error': f'Instagram posts search error: {posts_response.status_code}',
                'results': []
            }
        
        posts_data = posts_response.json()
        
        results = []
        for post in posts_data.get('data', []):
            result = {
                'id': post.get('id', ''),
                'platform': 'instagram',
                'text': post.get('caption', ''),
                'media_type': post.get('media_type', 'image'),  # image, video, carousel
                'image': post.get('media_url', ''),
                'created_at': post.get('timestamp', ''),
                'url': post.get('permalink', ''),
                'likes': post.get('like_count', 0),
                'comments': post.get('comments_count', 0)
            }
            results.append(result)
        
        return {
            'success': True,
            'results': results,
            'total': len(results)
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Instagram search error: {str(e)}',
            'results': []
        }


def search_instagram_posts(keyword, max_results=10):
    """
    Alternative: Search Instagram posts directly
    For now, redirects to hashtag search
    """
    return search_instagram_hashtag(keyword, max_results)
