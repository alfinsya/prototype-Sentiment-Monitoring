"""Dummy Data Service - Mock data for platforms without working API"""
from services.sentiment_service import analyze_sentiment
from datetime import datetime, timedelta
import random

# Dummy Twitter data
DUMMY_TWEETS = [
    "Laptop Samsung Galaxy Book Pro adalah pilihan terbaik untuk produktivitas. Spesifikasi tinggi dengan harga yang kompetitif! #SamsungLaptop",
    "Just got my new Samsung laptop, it's amazing! The display is so crisp and the performance is incredible.",
    "Samsung laptops are overpriced compared to competitors. Better options available in the market.",
    "Menggunakan Samsung Galaxy Book selama 6 bulan. Sangat puas dengan kualitas dan daya tahan baterainya.",
    "The keyboard on Samsung laptops feels cheap. Not worth the premium price tag.",
]

DUMMY_FACEBOOK_POSTS = [
    {
        "text": "Baru beli laptop Samsung Galaxy Book Pro. Pertama kali pakai Samsung laptop dan sejauh ini sangat memuaskan!",
        "source": "Tech Enthusiast Group"
    },
    {
        "text": "Samsung laptops offer great value for money. The build quality is solid and performance is reliable.",
        "source": "Laptop Reviews Community"
    },
    {
        "text": "Tidak rekomendasikan Samsung laptop, sering hang dan customer service kurang responsif.",
        "source": "Consumer Feedback Forum"
    },
    {
        "text": "Samsung Galaxy Book 5 Pro - worth every penny! Amazing specs, beautiful design.",
        "source": "Tech Reviews Channel"
    }
]

DUMMY_GOOGLE_NEWS = [
    {
        "title": "Samsung Launches Latest Galaxy Book Pro with Advanced Features",
        "description": "Samsung announces new Galaxy Book Pro with improved processor and longer battery life",
        "source": "TechNews Today"
    },
    {
        "title": "Samsung Laptop Sales Surge in Q1 2026",
        "description": "Market analysis shows Samsung laptops gaining popularity among professionals",
        "source": "Tech Industry Report"
    },
    {
        "title": "Comparison: Samsung vs Dell Laptops for Business",
        "description": "Expert review comparing Samsung and Dell laptops for enterprise use",
        "source": "Business Tech Magazine"
    }
]

def get_dummy_tweets(keyword, max_results=5):
    """Generate dummy Twitter search results"""
    results = []
    
    for i in range(min(max_results, len(DUMMY_TWEETS))):
        tweet_text = DUMMY_TWEETS[i]
        sentiment = analyze_sentiment(tweet_text)
        
        result = {
            'id': f'dummy_tweet_{i}',
            'platform': 'twitter',
            'text': tweet_text,
            'author': f'user_{i}',
            'author_name': f'Tech User {i}',
            'verified': random.choice([True, False]),
            'created_at': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat() + 'Z',
            'likes': random.randint(10, 500),
            'retweets': random.randint(5, 200),
            'replies': random.randint(2, 100),
            'quotes': random.randint(1, 50),
            'sentiment': sentiment.get('sentiment', 'neutral'),
            'polarity': sentiment.get('polarity', 0),
            'subjectivity': sentiment.get('subjectivity', 0),
            'url': f'https://twitter.com/user_{i}/status/dummy{i}'
        }
        results.append(result)
    
    return {'success': True, 'results': results, 'total': len(results)}


def get_dummy_facebook_posts(keyword, max_results=5):
    """Generate dummy Facebook search results"""
    results = []
    
    for i in range(min(max_results, len(DUMMY_FACEBOOK_POSTS))):
        post = DUMMY_FACEBOOK_POSTS[i]
        sentiment = analyze_sentiment(post['text'])
        
        result = {
            'id': f'dummy_fb_{i}',
            'platform': 'facebook',
            'text': post['text'],
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat() + 'Z',
            'source': post['source'],
            'url': f'https://facebook.com/dummy-post-{i}',
            'likes': random.randint(10, 300),
            'comments': random.randint(5, 100),
            'shares': random.randint(1, 50),
            'sentiment': sentiment.get('sentiment', 'neutral'),
            'polarity': sentiment.get('polarity', 0),
            'subjectivity': sentiment.get('subjectivity', 0)
        }
        results.append(result)
    
    return {'success': True, 'results': results, 'total': len(results)}


def get_dummy_google_results(keyword, max_results=5):
    """Generate dummy Google News search results"""
    results = []
    
    for i in range(min(max_results, len(DUMMY_GOOGLE_NEWS))):
        article = DUMMY_GOOGLE_NEWS[i]
        sentiment = analyze_sentiment(article['description'])
        
        result = {
            'id': f'dummy_google_{i}',
            'platform': 'google_news',
            'title': article['title'],
            'description': article['description'],
            'url': f'https://example.com/article-{i}',
            'published_at': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat() + 'Z',
            'source': article['source'],
            'image': 'https://via.placeholder.com/400x300?text=Tech+News',
            'sentiment': sentiment.get('sentiment', 'neutral'),
            'polarity': sentiment.get('polarity', 0),
            'subjectivity': sentiment.get('subjectivity', 0)
        }
        results.append(result)
    
    return {'success': True, 'results': results, 'total': len(results)}
