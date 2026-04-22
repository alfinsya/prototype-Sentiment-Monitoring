"""Google News Web Scraper - Free unlimited results without API key"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import quote

# List of reputable news sources (filter out low-quality sources)
REPUTABLE_SOURCES = {
    'Reuters', 'Associated Press', 'BBC', 'CNN', 'The Guardian', 'The New York Times',
    'The Washington Post', 'Bloomberg', 'Financial Times', 'The Telegraph', 'The Times',
    'The Wall Street Journal', 'Fox News', 'CNBC', 'NBC News', 'ABC News', 'CBS News',
    'TechCrunch', 'The Verge', 'Wired', 'VentureBeat', 'TechRadar', 'Tom\'s Hardware',
    'CNET', 'Engadget', 'PCMag', 'ComputerWorld', 'IDC', 'Gartner', 'Forrester',
    'Fortune', 'Business Insider', 'Inc.', 'Entrepreneur', 'FastCompany',
    'DW', 'France24', 'Al Jazeera', 'Euronews', 'RIA Novosti', 'TASS',
    'Detik', 'Kompas', 'Tribun', 'Tempo', 'Indonesia.com', 'BeritaSatu', 'CNN Indonesia',
    'BBC Indonesia', 'VOA Indonesia', 'RFI', 'Liputan6', 'Okezone', 'Medcom'
}

def search_google_news_scrape(keyword, max_results=15):
    """
    Scrape Google News without API - UNLIMITED & FREE
    No API key needed! Includes image extraction and source filtering
    """
    try:
        # URL untuk Google News search
        search_url = f"https://news.google.com/rss/search?q={quote(keyword)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Failed to fetch Google News RSS: {response.status_code}',
                'results': []
            }
        
        soup = BeautifulSoup(response.content, 'lxml-xml')
        
        results = []
        items = soup.find_all('item')[:max_results * 2]  # Fetch more to filter
        
        for item in items:
            title_elem = item.find('title')
            desc_elem = item.find('description')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            source_elem = item.find('source')
            
            if not title_elem or not link_elem:
                continue
            
            title = title_elem.text.strip()
            url = link_elem.text.strip()
            pub_date = pub_date_elem.text if pub_date_elem else datetime.now().isoformat()
            source_name = source_elem.text if source_elem else 'Google News'
            
            # Extract image from description
            image_url = extract_image_from_description(desc_elem)
            
            # Get description text
            description = ''
            if desc_elem:
                desc_str = str(desc_elem)
                # Remove HTML tags but keep text
                description = BeautifulSoup(desc_str, 'html.parser').get_text().strip()
                # Limit description length
                if len(description) > 300:
                    description = description[:300] + '...'
            
            result = {
                'id': url,
                'platform': 'google_news',
                'title': title,
                'description': description,
                'url': url,
                'published_at': pub_date,
                'source': source_name,
                'image': image_url
            }
            results.append(result)
            
            if len(results) >= max_results:
                break
        
        return {
            'success': True,
            'results': results[:max_results],
            'total': len(results),
            'method': 'web_scrape'
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Google News scraping timeout',
            'results': []
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Scraping error: {str(e)}',
            'results': []
        }

def extract_image_from_description(desc_elem):
    """
    Extract image URL from description element
    Handles various HTML formats
    """
    if not desc_elem:
        return ''
    
    try:
        desc_str = str(desc_elem)
        
        # Look for img src attribute
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        match = re.search(img_pattern, desc_str)
        if match:
            img_url = match.group(1)
            # Filter out placeholder/icon images (usually very small)
            if not any(x in img_url.lower() for x in ['icon', '16x16', '32x32', 'logo', 'avatar']):
                return img_url
        
        # Try parsing with BeautifulSoup as fallback
        soup = BeautifulSoup(desc_str, 'html.parser')
        img_tag = soup.find('img')
        if img_tag:
            src = img_tag.get('src', '')
            if src and not any(x in src.lower() for x in ['icon', 'logo', 'avatar']):
                return src
        
        return ''
    except Exception as e:
        return ''


def search_google_web_scrape(keyword, max_results=10):
    """
    Scrape regular Google Search results
    Limited to avoid blocking
    """
    try:
        search_url = 'https://www.google.com/search'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        params = {
            'q': keyword,
            'hl': 'en'
        }
        
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Google search blocked: {response.status_code}',
                'results': []
            }
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        
        # Cari div dengan class 'g' (result item)
        for item in soup.find_all('div', class_='g')[:max_results]:
            try:
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                url = link_elem['href']
                if url.startswith('/url?'):
                    # Extract real URL dari Google redirect
                    url = url.split('url?q=')[1].split('&')[0]
                
                title_elem = item.find('h3')
                title = title_elem.text if title_elem else 'No title'
                
                desc_elem = item.find('div', class_='s')
                description = desc_elem.text if desc_elem else ''
                
                result = {
                    'id': url,
                    'platform': 'google_search',
                    'title': title,
                    'description': description,
                    'url': url,
                    'published_at': datetime.now().isoformat(),
                    'source': 'Google Search',
                    'image': ''
                }
                results.append(result)
            except Exception as e:
                continue
        
        return {
            'success': True,
            'results': results,
            'total': len(results),
            'method': 'web_scrape'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Web scraping failed: {str(e)}',
            'results': []
        }
