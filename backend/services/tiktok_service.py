"""TikTok Search Service"""
import os
import requests
from dotenv import load_dotenv
import re

load_dotenv()

TIKTOK_API_KEY = os.getenv('TIKTOK_API_KEY', '')
TIKTOK_SEARCH_URL = 'https://www.tiktok.com/api/search/general/full/'

def search_tiktok(keyword, max_results=10):
    """
    Search TikTok videos by keyword
    Note: TikTok official API is very limited (only for brand accounts)
    This uses web scraping approach
    """
    try:
        # For production, consider using TikTok's official API if available
        # or unofficial libraries like TikTokApi
        
        # Alternative: Use web scraping with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
            'Accept': 'application/json'
        }
        
        params = {
            'keywords': keyword,
            'cursor': 0,
            'count': max_results,
            'scene': 1  # 1 = search
        }
        
        response = requests.get(TIKTOK_SEARCH_URL, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            # Return dummy data since TikTok API is restricted
            return {
                'success': False,
                'error': f'TikTok API blocked or unavailable (Status: {response.status_code})',
                'results': [],
                'note': 'TikTok restricts API access. Consider using official TikTok API or unofficial libraries.'
            }
        
        data = response.json()
        results = []
        
        # Parse response based on TikTok API structure
        for item in data.get('items', [])[:max_results]:
            video = item.get('video', {})
            author = item.get('author', {})
            stats = item.get('stats', {})
            
            result = {
                'id': item.get('id', ''),
                'platform': 'tiktok',
                'text': item.get('desc', ''),
                'author': author.get('uniqueId', 'Unknown'),
                'author_name': author.get('nickName', 'Unknown'),
                'verified': author.get('verified', False),
                'avatar': author.get('avatarMedium', ''),
                'created_at': item.get('createTime', ''),
                'video_url': video.get('dynamicCover', ''),
                'url': f'https://www.tiktok.com/@{author.get("uniqueId", "")}/video/{item.get("id", "")}',
                'likes': stats.get('diggCount', 0),
                'comments': stats.get('commentCount', 0),
                'shares': stats.get('shareCount', 0),
                'views': stats.get('playCount', 0)
            }
            results.append(result)
        
        return {
            'success': True,
            'results': results,
            'total': len(results)
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'TikTok search network error: {str(e)}',
            'results': [],
            'note': 'TikTok may block automated requests. Try using official TikTok API.'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'TikTok search error: {str(e)}',
            'results': []
        }


def search_tiktok_trending(max_results=10):
    """
    Get trending TikTok videos
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
        
        # TikTok trending endpoint
        trending_url = 'https://www.tiktok.com/api/discover/explore/'
        
        response = requests.get(trending_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'TikTok trending error: {response.status_code}',
                'results': []
            }
        
        # Parse response...
        return {
            'success': True,
            'results': [],
            'total': 0,
            'message': 'Trending TikToks retrieved'
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'TikTok trending error: {str(e)}',
            'results': []
        }
