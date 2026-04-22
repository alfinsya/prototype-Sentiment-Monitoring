"""Sentiment Analysis Service"""
from textblob import TextBlob
from typing import Dict, List

def analyze_sentiment(text: str) -> Dict:
    """
    Analyze sentiment of text using TextBlob
    Returns polarity (-1 to 1) and subjectivity (0 to 1)
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        
        # Classify sentiment
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3)
        }
    except Exception as e:
        return {
            'error': f'Sentiment analysis failed: {str(e)}',
            'sentiment': 'unknown'
        }

def analyze_sentiments_batch(texts: List[str]) -> List[Dict]:
    """
    Analyze sentiment for multiple texts
    Returns list of sentiment results
    """
    results = []
    for text in texts:
        result = analyze_sentiment(text)
        results.append(result)
    return results

def get_sentiment_summary(sentiments: List[Dict]) -> Dict:
    """
    Generate summary statistics from sentiment analysis
    Returns counts and percentages
    """
    positive = sum(1 for s in sentiments if s.get('sentiment') == 'positive')
    negative = sum(1 for s in sentiments if s.get('sentiment') == 'negative')
    neutral = sum(1 for s in sentiments if s.get('sentiment') == 'neutral')
    total = len(sentiments)
    
    return {
        'total': total,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'positive_percentage': round((positive / total * 100) if total > 0 else 0, 2),
        'negative_percentage': round((negative / total * 100) if total > 0 else 0, 2),
        'neutral_percentage': round((neutral / total * 100) if total > 0 else 0, 2),
        'average_polarity': round(sum(s.get('polarity', 0) for s in sentiments) / total if total > 0 else 0, 3)
    }
