"""Google Search API Service for News and Web Results"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY', '')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')  # Custom Search Engine ID
BASE_URL = 'https://www.googleapis.com/customsearch/v1'

def search_google(keyword, max_results=10):
    """
    Search using Google Custom Search API
    Returns web results including news
    Note: Requires Custom Search Engine setup
    """
    if not GOOGLE_SEARCH_API_KEY:
        return {'error': 'Google Search API key not configured'}
    
    try:
        params = {
            'q': keyword,
            'key': GOOGLE_SEARCH_API_KEY,
            'num': min(max_results, 10),  # Max 10 per request
            'searchType': 'news'  # Search news specifically
        }
        
        # If you have CXID (Custom Search Engine ID), include it
        if GOOGLE_SEARCH_ENGINE_ID:
            params['cx'] = GOOGLE_SEARCH_ENGINE_ID
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code != 200:
            return {'error': f'Google API error: {response.status_code}'}
        
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            result = {
                'id': item.get('link', ''),
                'platform': 'google_news',
                'title': item.get('title', ''),
                'description': item.get('snippet', ''),
                'url': item.get('link', ''),
                'published_at': item.get('publication', 'N/A'),
                'source': item.get('displayLink', ''),
                'image': item.get('image', {}).get('url', '') if 'image' in item else ''
            }
            results.append(result)
        
        return {'success': True, 'results': results, 'total': len(results)}
        
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


def search_google_news_fallback(keyword, max_results=10):
    """
    Fallback: Use NewsAPI or other alternative if Google Custom Search fails
    This is optional - for demonstration
    """
    try:
        # Using NewsAPI as fallback (free tier available)
        news_url = 'https://newsapi.org/v2/everything'
        
        params = {
            'q': keyword,
            'sortBy': 'relevancy',
            'language': 'en',
            'pageSize': max_results
            # Note: Requires API key from newsapi.org
        }
        
        response = requests.get(news_url, params=params)
        
        if response.status_code != 200:
            return {'error': f'News API error: {response.status_code}'}
        
        data = response.json()
        
        results = []
        for article in data.get('articles', []):
            result = {
                'id': article.get('url', ''),
                'platform': 'google_news',
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', ''),
                'image': article.get('urlToImage', '')
            }
            results.append(result)
        
        return {'success': True, 'results': results, 'total': len(results)}
        
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}
