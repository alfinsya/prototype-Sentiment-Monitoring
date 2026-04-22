"""Google Search API Service for News and Web Results"""
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY', '')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')

BASE_URL = 'https://www.googleapis.com/customsearch/v1'
NEWSAPI_URL = 'https://newsapi.org/v2/everything'

def search_google(keyword, max_results=10):
    """
    Search using multiple methods in priority order:
    1. Web Scraping (UNLIMITED - No API key needed!)
    2. NewsAPI (Free tier - 100 req/day)
    3. Google Custom Search API (Paid)
    """
    # Try web scraping first (unlimited & free!)
    from services.google_scraper import search_google_news_scrape
    result = search_google_news_scrape(keyword, max_results)
    if result.get('success') and len(result.get('results', [])) > 0:
        return result
    
    # Try NewsAPI as fallback
    if NEWSAPI_KEY:
        result = search_with_newsapi(keyword, max_results)
        if result.get('success'):
            return result
    
    # Try Google Custom Search API as last fallback
    if GOOGLE_SEARCH_API_KEY:
        result = search_with_google_cse(keyword, max_results)
        if result.get('success'):
            return result
    
    # If no method works, return error
    return {
        'success': False,
        'error': 'All search methods failed',
        'results': []
    }


def search_with_newsapi(keyword, max_results=10):
    """
    Search using NewsAPI - Returns news articles
    Free tier: 100 requests per day
    """
    try:
        params = {
            'q': keyword,
            'sortBy': 'relevancy',
            'language': 'id,en',  # Indonesian and English
            'pageSize': min(max_results, 100),
            'apiKey': NEWSAPI_KEY
        }
        
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'NewsAPI error: {response.status_code}',
                'results': []
            }
        
        data = response.json()
        
        if data.get('status') != 'ok':
            return {
                'success': False,
                'error': f"NewsAPI returned: {data.get('message', 'Unknown error')}",
                'results': []
            }
        
        results = []
        for article in data.get('articles', []):
            result = {
                'id': article.get('url', ''),
                'platform': 'google_news',
                'title': article.get('title', ''),
                'description': article.get('description', '') or article.get('content', ''),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'image': article.get('urlToImage', ''),
                'author': article.get('author', '')
            }
            results.append(result)
        
        return {
            'success': True,
            'results': results[:max_results],
            'total': len(results[:max_results])
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'NewsAPI request timeout',
            'results': []
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'NewsAPI error: {str(e)}',
            'results': []
        }

def search_with_google_cse(keyword, max_results=10):
    """
    Search using Google Custom Search Engine
    Requires: GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID
    """
    try:
        params = {
            'q': keyword,
            'key': GOOGLE_SEARCH_API_KEY,
            'num': min(max_results, 10),
            'searchType': 'news'
        }
        
        if GOOGLE_SEARCH_ENGINE_ID:
            params['cx'] = GOOGLE_SEARCH_ENGINE_ID
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Google API error: {response.status_code}',
                'results': []
            }
        
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
        
        return {
            'success': True,
            'results': results,
            'total': len(results)
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Google API request timeout',
            'results': []
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Google API error: {str(e)}',
            'results': []
        }
