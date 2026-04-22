"""Twitter Search Service using Twitter API v2"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
BASE_URL = 'https://api.twitter.com/2'

def get_twitter_headers():
    """Get headers with Bearer token for Twitter API"""
    return {
        'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}',
        'User-Agent': 'Monitoring-Web-Bot/1.0'
    }

def search_twitter(keyword, max_results=10):
    """
    Search tweets based on keyword using Twitter API v2
    Returns list of tweet results with metadata
    """
    if not TWITTER_BEARER_TOKEN:
        return {
            'success': False,
            'error': 'Twitter Bearer Token not configured',
            'results': []
        }
    
    try:
        headers = get_twitter_headers()
        
        # Twitter API v2 endpoint
        url = f'{BASE_URL}/tweets/search/recent'
        
        params = {
            'query': keyword,
            'max_results': min(max_results, 100),  # Max 100 per request
            'tweet.fields': 'created_at,public_metrics,author_id',
            'expansions': 'author_id',
            'user.fields': 'username,name,verified'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Twitter API error: {response.status_code} - {response.text}',
                'results': []
            }
        
        data = response.json()
        
        results = []
        users_map = {}
        
        # Map users
        if 'includes' in data and 'users' in data['includes']:
            for user in data['includes']['users']:
                users_map[user['id']] = {
                    'username': user['username'],
                    'name': user['name'],
                    'verified': user.get('verified', False)
                }
        
        # Process tweets
        for tweet in data.get('data', []):
            author_id = tweet['author_id']
            author = users_map.get(author_id, {})
            metrics = tweet['public_metrics']
            
            result = {
                'id': tweet['id'],
                'platform': 'twitter',
                'text': tweet['text'],
                'author': author.get('username', 'Unknown'),
                'author_name': author.get('name', 'Unknown'),
                'verified': author.get('verified', False),
                'created_at': tweet['created_at'],
                'likes': metrics['like_count'],
                'retweets': metrics['retweet_count'],
                'replies': metrics['reply_count'],
                'quotes': metrics['quote_count'],
                'url': f'https://twitter.com/{author.get("username", "")}/status/{tweet["id"]}'
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
            'error': f'Unexpected error: {str(e)}',
            'results': []
        }


def search_twitter_stream(keyword, max_results=10):
    """
    Alternative: Search using Twitter Standard Search (older tweets)
    Fallback if recent tweets are limited
    """
    try:
        headers = get_twitter_headers()
        
        url = f'{BASE_URL}/tweets/search/all'  # Requires Academic or Premium access
        
        params = {
            'query': keyword,
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,public_metrics,author_id',
            'expansions': 'author_id',
            'user.fields': 'username,name,verified'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return {'error': f'Twitter API error: {response.status_code}'}
        
        return response.json()
        
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}
