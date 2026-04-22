"""AI Insights Service - Advanced Analytics & Recommendations"""
from typing import Dict, List
from collections import Counter
import re
from datetime import datetime

def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """
    Extract keywords from text using simple frequency analysis
    Removes common stop words
    """
    # Common English stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
        'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
        'as', 'if', 'because', 'than', 'while', 'about', 'so', 'not', 'no',
        'just', 'very', 'too', 'more', 'most', 'less', 'least', 'such'
    }
    
    # Convert to lowercase and extract words
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    
    # Filter out stop words and get top keywords
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    word_freq = Counter(filtered_words)
    
    return [word for word, _ in word_freq.most_common(top_n)]

def analyze_sentiment_trends(results: List[Dict]) -> Dict:
    """
    Analyze sentiment trends across results
    Returns distribution, trends, and insights
    """
    if not results:
        return {'error': 'No results to analyze'}
    
    sentiments = [r.get('sentiment', 'unknown') for r in results]
    polarities = [r.get('polarity', 0) for r in results if r.get('polarity')]
    
    # Count sentiments
    sentiment_counts = {
        'positive': sentiments.count('positive'),
        'negative': sentiments.count('negative'),
        'neutral': sentiments.count('neutral'),
        'unknown': sentiments.count('unknown')
    }
    
    total = len(results)
    sentiment_percentages = {
        k: round((v / total * 100) if total > 0 else 0, 2)
        for k, v in sentiment_counts.items()
    }
    
    # Calculate polarity statistics
    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    
    # Trend interpretation
    positive_ratio = sentiment_counts['positive'] / total if total > 0 else 0
    trend_status = 'positive' if positive_ratio > 0.6 else 'negative' if positive_ratio < 0.4 else 'neutral'
    
    return {
        'sentiment_distribution': sentiment_counts,
        'sentiment_percentages': sentiment_percentages,
        'average_polarity': round(avg_polarity, 3),
        'trend_status': trend_status,
        'total_analyzed': total
    }

def calculate_engagement_metrics(results: List[Dict]) -> Dict:
    """
    Calculate engagement metrics based on available data
    Returns engagement scores and platform-specific metrics
    """
    if not results:
        return {'error': 'No results to analyze'}
    
    # Analyze by platform
    platform_metrics = {}
    total_engagement_score = 0
    
    for result in results:
        platform = result.get('platform', 'unknown')
        
        if platform not in platform_metrics:
            platform_metrics[platform] = {
                'count': 0,
                'avg_polarity': 0,
                'engagement_score': 0,
                'items': []
            }
        
        platform_metrics[platform]['count'] += 1
        platform_metrics[platform]['items'].append(result)
        
        # Calculate engagement score based on polarity and sentiment
        polarity = result.get('polarity', 0)
        sentiment = result.get('sentiment', 'neutral')
        
        sentiment_weight = {
            'positive': 1.0,
            'neutral': 0.5,
            'negative': 0.3,
            'unknown': 0.0
        }.get(sentiment, 0.5)
        
        engagement = (polarity + 1) / 2 * sentiment_weight  # Normalize to 0-1
        platform_metrics[platform]['engagement_score'] += engagement
        total_engagement_score += engagement
    
    # Average metrics per platform
    for platform in platform_metrics:
        count = platform_metrics[platform]['count']
        items = platform_metrics[platform]['items']
        
        polarities = [item.get('polarity', 0) for item in items]
        avg_polarity = sum(polarities) / len(polarities) if polarities else 0
        
        platform_metrics[platform]['avg_polarity'] = round(avg_polarity, 3)
        platform_metrics[platform]['engagement_score'] = round(
            platform_metrics[platform]['engagement_score'] / count, 3
        )
        del platform_metrics[platform]['items']  # Remove items list from response
    
    # Overall engagement score
    total_results = len(results)
    overall_engagement = round(
        total_engagement_score / total_results if total_results > 0 else 0, 3
    )
    
    return {
        'overall_engagement_score': overall_engagement,
        'engagement_level': 'high' if overall_engagement > 0.7 else 'moderate' if overall_engagement > 0.4 else 'low',
        'platform_metrics': platform_metrics,
        'total_mentions': total_results
    }

def extract_topics_and_keywords(results: List[Dict], top_n: int = 10) -> Dict:
    """
    Extract topics and keywords from all results
    Returns most mentioned topics and keywords
    """
    if not results:
        return {'error': 'No results to analyze'}
    
    all_keywords = []
    text_sources = []
    
    # Extract keywords from text and descriptions
    for result in results:
        text = result.get('text', '') or result.get('description', '') or result.get('title', '')
        if text:
            text_sources.append(text)
            keywords = extract_keywords(text, top_n=3)
            all_keywords.extend(keywords)
    
    # Get top keywords
    keyword_freq = Counter(all_keywords)
    top_keywords = [word for word, _ in keyword_freq.most_common(top_n)]
    
    # Extract topics from titles/descriptions
    all_titles = [r.get('title', '') for r in results if r.get('title')]
    topics_text = ' '.join(all_titles)
    topics = extract_keywords(topics_text, top_n=5)
    
    return {
        'top_keywords': top_keywords,
        'keyword_frequency': dict(keyword_freq.most_common(top_n)),
        'main_topics': topics,
        'total_unique_keywords': len(keyword_freq),
        'keyword_mentions': sum(keyword_freq.values())
    }

def generate_recommendations(results: List[Dict], sentiment_summary: Dict) -> List[Dict]:
    """
    Generate AI-powered recommendations based on analysis
    Returns actionable recommendations
    """
    recommendations = []
    
    if not results or not sentiment_summary:
        return recommendations
    
    # Analyze sentiment to provide recommendations
    positive_pct = sentiment_summary.get('positive_percentage', 0)
    negative_pct = sentiment_summary.get('negative_percentage', 0)
    avg_polarity = sentiment_summary.get('average_polarity', 0)
    
    # Recommendation 1: Sentiment-based
    if positive_pct > 70:
        recommendations.append({
            'type': 'sentiment',
            'title': 'Strong Positive Sentiment',
            'description': f'{positive_pct}% of mentions are positive. Leverage this momentum to amplify your marketing message.',
            'priority': 'high',
            'action': 'Increase marketing activities and gather user testimonials'
        })
    elif negative_pct > 50:
        recommendations.append({
            'type': 'sentiment',
            'title': 'Negative Sentiment Alert',
            'description': f'{negative_pct}% of mentions are negative. Address customer concerns and improve product/service quality.',
            'priority': 'critical',
            'action': 'Analyze negative feedback and create action plan for improvement'
        })
    elif positive_pct > negative_pct:
        recommendations.append({
            'type': 'sentiment',
            'title': 'Balanced Positive Trend',
            'description': f'Positive mentions ({positive_pct}%) slightly exceed negative ({negative_pct}%). Maintain current efforts.',
            'priority': 'medium',
            'action': 'Continue monitoring and optimize based on feedback'
        })
    
    # Recommendation 2: Engagement-based
    engagement = calculate_engagement_metrics(results)
    engagement_score = engagement.get('overall_engagement_score', 0)
    
    if engagement_score > 0.7:
        recommendations.append({
            'type': 'engagement',
            'title': 'High Engagement Detected',
            'description': f'Engagement score is {round(engagement_score * 100)}%. Your brand is generating strong interest.',
            'priority': 'high',
            'action': 'Scale up campaigns and explore new marketing channels'
        })
    elif engagement_score < 0.4:
        recommendations.append({
            'type': 'engagement',
            'title': 'Low Engagement Alert',
            'description': f'Engagement score is only {round(engagement_score * 100)}%. Consider refreshing your strategy.',
            'priority': 'medium',
            'action': 'Review campaign strategy and try new content approaches'
        })
    
    # Recommendation 3: Volume-based
    total_mentions = len(results)
    if total_mentions > 100:
        recommendations.append({
            'type': 'volume',
            'title': 'High Mention Volume',
            'description': f'Your brand received {total_mentions} mentions. You have strong market presence.',
            'priority': 'high',
            'action': 'Monitor discussions and engage with your audience'
        })
    elif total_mentions < 20:
        recommendations.append({
            'type': 'volume',
            'title': 'Low Mention Volume',
            'description': f'Only {total_mentions} mentions found. Consider increasing visibility.',
            'priority': 'medium',
            'action': 'Increase marketing efforts and improve SEO strategy'
        })
    
    # Recommendation 4: Topic-based
    topics = extract_topics_and_keywords(results)
    top_keywords = topics.get('top_keywords', [])
    
    if top_keywords:
        recommendations.append({
            'type': 'topics',
            'title': 'Key Topics Identified',
            'description': f'Main topics discussed: {", ".join(top_keywords[:3])}. Focus content around these themes.',
            'priority': 'medium',
            'action': 'Create targeted content addressing these topics'
        })
    
    return recommendations

def get_comprehensive_insights(results: List[Dict], sentiment_summary: Dict) -> Dict:
    """
    Generate comprehensive AI insights combining all analyses
    Main function that orchestrates all insights generation
    """
    if not results:
        return {
            'success': False,
            'error': 'No results to analyze',
            'timestamp': datetime.now().isoformat()
        }
    
    try:
        # Get all analyses
        sentiment_trends = analyze_sentiment_trends(results)
        engagement_metrics = calculate_engagement_metrics(results)
        topics = extract_topics_and_keywords(results)
        recommendations = generate_recommendations(results, sentiment_summary)
        
        # Compile comprehensive insights
        insights = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_analyzed': len(results),
                'analysis_type': 'comprehensive',
                'platforms_included': list(set(r.get('platform', 'unknown') for r in results))
            },
            'sentiment_analysis': sentiment_trends,
            'engagement_analysis': engagement_metrics,
            'topics_and_keywords': topics,
            'recommendations': recommendations,
            'insights_count': len(recommendations),
            'overall_score': round((
                sentiment_trends.get('average_polarity', 0) * 0.4 +
                engagement_metrics.get('overall_engagement_score', 0) * 0.6
            ), 3)
        }
        
        return insights
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Insights generation failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
