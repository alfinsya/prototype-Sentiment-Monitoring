"""YouTube Search Service"""
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

def search_youtube(keyword, max_results=10):
    """
    Search YouTube videos based on keyword
    Returns list of video results with metadata
    """
    if not YOUTUBE_API_KEY:
        return {'error': 'YouTube API key not configured'}
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.search().list(
            q=keyword,
            part='snippet',
            maxResults=max_results,
            type='video',
            order='relevance'
        )
        
        response = request.execute()
        
        results = []
        for item in response.get('items', []):
            video_id = item['id'].get('videoId')
            snippet = item['snippet']
            
            result = {
                'id': video_id,
                'platform': 'youtube',
                'title': snippet['title'],
                'description': snippet['description'],
                'channel': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'thumbnail': snippet['thumbnails'].get('high', {}).get('url', ''),
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'views': 'N/A',  # Need to fetch stats separately
                'likes': 'N/A',
                'comments': 'N/A'
            }
            results.append(result)
        
        return {'success': True, 'results': results, 'total': len(results)}
        
    except HttpError as e:
        return {'error': f'YouTube API error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


def get_video_stats(video_id):
    """
    Get video statistics (views, likes, comments)
    """
    if not YOUTUBE_API_KEY:
        return {'error': 'YouTube API key not configured'}
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.videos().list(
            id=video_id,
            part='statistics'
        )
        
        response = request.execute()
        
        if response['items']:
            stats = response['items'][0]['statistics']
            return {
                'views': stats.get('viewCount', '0'),
                'likes': stats.get('likeCount', '0'),
                'comments': stats.get('commentCount', '0')
            }
        
        return {'error': 'Video not found'}
        
    except HttpError as e:
        return {'error': f'YouTube API error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}
