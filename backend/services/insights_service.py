"""Enhanced AI Insights Service - Meaningful Conclusions & Patterns"""
from typing import Dict, List
from collections import Counter
import re
from datetime import datetime

def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """Extract keywords from text"""
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
    
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    word_freq = Counter(filtered_words)
    
    return [word for word, _ in word_freq.most_common(top_n)]


def analyze_sentiment_by_keyword(results: List[Dict]) -> Dict:
    """
    Analyze sentiment for each keyword
    Shows what people are saying positive vs negative about
    """
    keyword_sentiment = {}
    
    for result in results:
        text = result.get('text', '') or result.get('description', '')
        sentiment = result.get('sentiment', 'neutral')
        
        if text:
            keywords = extract_keywords(text, top_n=3)
            for keyword in keywords:
                if keyword not in keyword_sentiment:
                    keyword_sentiment[keyword] = {
                        'positive': 0,
                        'negative': 0,
                        'neutral': 0,
                        'mentions': 0
                    }
                
                keyword_sentiment[keyword][sentiment] += 1
                keyword_sentiment[keyword]['mentions'] += 1
    
    # Calculate percentages and find dominant sentiment
    insights = {}
    for keyword, counts in sorted(keyword_sentiment.items(), 
                                   key=lambda x: x[1]['mentions'], reverse=True)[:10]:
        total = counts['mentions']
        positive_pct = (counts['positive'] / total * 100) if total > 0 else 0
        negative_pct = (counts['negative'] / total * 100) if total > 0 else 0
        
        if positive_pct > 60:
            dominant = 'positive'
        elif negative_pct > 60:
            dominant = 'negative'
        else:
            dominant = 'mixed'
        
        insights[keyword] = {
            'mentions': total,
            'positive': int(counts['positive']),
            'negative': int(counts['negative']),
            'neutral': int(counts['neutral']),
            'positive_pct': round(positive_pct, 1),
            'negative_pct': round(negative_pct, 1),
            'sentiment': dominant
        }
    
    return insights


def extract_problems_and_complaints(results: List[Dict]) -> List[Dict]:
    """
    Extract main problems and complaints from negative/neutral mentions
    """
    complaints = []
    
    # Problem keywords
    problem_keywords = [
        'problem', 'issue', 'bug', 'error', 'crash', 'fail', 'broken',
        'not work', 'waste', 'bad', 'worst', 'disappointed', 'poor',
        'slow', 'expensive', 'expensive', 'overpriced', 'complaint',
        'complain', 'regret', 'avoid', 'dont buy', 'dont use', 'scam',
        'fraud', 'cheat', 'misleading', 'false'
    ]
    
    for result in results:
        text = (result.get('text', '') or result.get('description', '')).lower()
        sentiment = result.get('sentiment', 'neutral')
        
        # Look for complaints in negative or neutral mentions
        if sentiment in ['negative', 'neutral'] and text:
            for problem in problem_keywords:
                if problem in text:
                    complaints.append({
                        'issue': problem,
                        'text': text[:200],
                        'sentiment': sentiment,
                        'source': result.get('platform', 'unknown')
                    })
                    break
    
    # Group complaints by issue
    issue_counts = Counter([c['issue'] for c in complaints])
    top_issues = [
        {
            'issue': issue,
            'frequency': count,
            'examples': [c['text'] for c in complaints if c['issue'] == issue][:2]
        }
        for issue, count in issue_counts.most_common(5)
    ]
    
    return top_issues


def extract_preferences_and_desires(results: List[Dict]) -> List[Dict]:
    """
    Extract what people want or prefer
    """
    preferences = []
    
    # Preference keywords
    preference_keywords = [
        'prefer', 'prefer', 'like', 'love', 'want', 'need', 'recommend',
        'better', 'best', 'should have', 'wish', 'hope', 'expect',
        'should', 'would like', 'interested in', 'looking for'
    ]
    
    for result in results:
        text = (result.get('text', '') or result.get('description', '')).lower()
        sentiment = result.get('sentiment', 'neutral')
        
        # Look for preferences in positive mentions
        if sentiment in ['positive', 'neutral'] and text:
            for pref_keyword in preference_keywords:
                if pref_keyword in text:
                    # Extract what they prefer
                    idx = text.find(pref_keyword)
                    preference_context = text[max(0, idx-20):min(len(text), idx+80)]
                    
                    preferences.append({
                        'preference_type': pref_keyword,
                        'text': preference_context.strip(),
                        'full_text': text[:200],
                        'sentiment': sentiment,
                        'source': result.get('platform', 'unknown')
                    })
                    break
    
    # Group preferences
    pref_types = Counter([p['preference_type'] for p in preferences])
    top_preferences = [
        {
            'type': pref_type,
            'frequency': count,
            'examples': [p['full_text'] for p in preferences if p['preference_type'] == pref_type][:2]
        }
        for pref_type, count in pref_types.most_common(5)
    ]
    
    return top_preferences


def generate_meaningful_insights(results: List[Dict], sentiment_summary: Dict) -> List[str]:
    """
    Generate meaningful text insights/conclusions
    Returns human-readable insights like "Most people prefer X because Y"
    """
    insights = []
    
    if not results:
        return insights
    
    # 1. Overall sentiment insight
    positive_pct = sentiment_summary.get('positive_percentage', 0)
    negative_pct = sentiment_summary.get('negative_percentage', 0)
    
    if positive_pct > 70:
        insights.append(
            f"📈 Strong Market Interest: {positive_pct}% of mentions show positive sentiment, indicating "
            f"strong customer interest and satisfaction with the topic/product."
        )
    elif negative_pct > 60:
        insights.append(
            f"⚠️ Customer Concerns Detected: {negative_pct}% of mentions are negative, suggesting "
            f"significant issues or concerns that need to be addressed immediately."
        )
    elif positive_pct > negative_pct + 10:
        insights.append(
            f"✓ Positive Reception: {positive_pct}% positive vs {negative_pct}% negative mentions show "
            f"a favorable overall reception in the market."
        )
    else:
        insights.append(
            f"↔️ Mixed Reception: Opinions are balanced ({positive_pct}% positive, {negative_pct}% negative), "
            f"indicating diverse market perspectives."
        )
    
    # 2. Main topics/keywords insight
    keyword_sentiment = analyze_sentiment_by_keyword(results)
    
    # Find most positively discussed topics
    positive_topics = [
        (kw, data) for kw, data in keyword_sentiment.items() 
        if data['sentiment'] == 'positive'
    ]
    
    if positive_topics:
        top_positive = positive_topics[0]
        insights.append(
            f"💚 Positive Focus: People frequently discuss '{top_positive[0]}' in a positive light "
            f"({top_positive[1]['positive_pct']}% positive mentions). This is a strong selling point."
        )
    
    # Find most negatively discussed topics
    negative_topics = [
        (kw, data) for kw, data in keyword_sentiment.items() 
        if data['sentiment'] == 'negative'
    ]
    
    if negative_topics:
        top_negative = negative_topics[0]
        insights.append(
            f"💔 Concern Area: '{top_negative[0]}' is frequently mentioned negatively ({top_negative[1]['negative_pct']}% negative). "
            f"This requires attention and improvement."
        )
    
    # 3. Problems/Complaints insight
    top_issues = extract_problems_and_complaints(results)
    
    if top_issues:
        main_issue = top_issues[0]
        insights.append(
            f"🔴 Main Issue: The most common complaint is '{main_issue['issue']}' "
            f"(mentioned {main_issue['frequency']} times). Address this to improve satisfaction."
        )
    
    # 4. Preferences/Desires insight
    top_prefs = extract_preferences_and_desires(results)
    
    if top_prefs:
        main_pref = top_prefs[0]
        insights.append(
            f"🎯 Market Want: '{main_pref['type']}' is the most common desire expressed "
            f"({main_pref['frequency']} mentions). Focus on meeting this need."
        )
    
    # 5. Platform-specific insight
    platform_counts = Counter([r.get('platform', 'unknown') for r in results])
    if platform_counts:
        most_active_platform = platform_counts.most_common(1)[0]
        insights.append(
            f"📱 Most Active: {most_active_platform[0]} has the highest mention volume ({most_active_platform[1]} posts). "
            f"Focus on this platform for maximum reach."
        )
    
    return insights


def generate_actionable_recommendations(
    results: List[Dict], 
    sentiment_summary: Dict,
    keyword_insights: Dict
) -> List[Dict]:
    """
    Generate specific, actionable recommendations
    """
    recommendations = []
    
    if not results:
        return recommendations
    
    positive_pct = sentiment_summary.get('positive_percentage', 0)
    negative_pct = sentiment_summary.get('negative_percentage', 0)
    
    # Recommendation 1: Crisis Management
    if negative_pct > 50:
        top_issues = extract_problems_and_complaints(results)
        if top_issues:
            issue = top_issues[0]['issue']
            recommendations.append({
                'title': '🚨 Crisis Management Action Required',
                'description': f"High negative sentiment detected ({negative_pct}%). The main issue is '{issue}'.",
                'action': f'Immediately: Create a response plan to address "{issue}" complaints. Consider refund policy, '
                         f'product recalls, or service improvements. Respond to complaints publicly within 24 hours.',
                'priority': 'CRITICAL',
                'estimated_impact': 'High - Can prevent reputation damage'
            })
    
    # Recommendation 2: Quality Improvement
    top_issues = extract_problems_and_complaints(results)
    if top_issues and len(top_issues) > 0:
        issue = top_issues[0]['issue']
        recommendations.append({
            'title': '⚡ Address Quality Issues',
            'description': f'Customer complaint analysis shows "{issue}" is the primary concern.',
            'action': f'Schedule QA meeting to investigate "{issue}" reports. Allocate engineering resources '
                     f'to fix this within 2-4 weeks. Set up monitoring for this issue.',
            'priority': 'HIGH',
            'estimated_impact': 'High - Improves customer satisfaction'
        })
    
    # Recommendation 3: Marketing Amplification
    if positive_pct > 60:
        keyword_insights = analyze_sentiment_by_keyword(results)
        positive_keywords = [(k, v) for k, v in keyword_insights.items() if v['sentiment'] == 'positive']
        
        if positive_keywords:
            main_strength = positive_keywords[0][0]
            recommendations.append({
                'title': '📢 Amplify Positive Message',
                'description': f'Strong positive sentiment ({positive_pct}%) about "{main_strength}".',
                'action': f'Launch marketing campaign highlighting "{main_strength}" as key selling point. '
                         f'Collect testimonials and case studies. Create social media content around this strength.',
                'priority': 'MEDIUM',
                'estimated_impact': 'Medium - Increases conversions'
            })
    
    # Recommendation 4: Feature Development
    top_prefs = extract_preferences_and_desires(results)
    if top_prefs:
        main_desire = top_prefs[0]['type']
        recommendations.append({
            'title': '💡 Market-Driven Product Development',
            'description': f'Customers frequently express desire to "{main_desire}" ({top_prefs[0]["frequency"]} mentions).',
            'action': f'Add "{main_desire}" to product roadmap. Conduct user interviews to understand exact requirements. '
                     f'Prioritize this for next sprint/release cycle.',
            'priority': 'MEDIUM',
            'estimated_impact': 'High - Directly addresses customer needs'
        })
    
    # Recommendation 5: Engagement Strategy
    if positive_pct > negative_pct:
        recommendations.append({
            'title': '👥 Engagement & Community Building',
            'description': 'Overall sentiment is positive - good opportunity for community engagement.',
            'action': 'Increase social media engagement: respond to all positive comments, create user-generated content campaigns, '
                     'host community events or Q&A sessions. Build brand loyalty.',
            'priority': 'LOW',
            'estimated_impact': 'Medium - Long-term brand loyalty'
        })
    
    return recommendations


def get_comprehensive_insights(results: List[Dict], sentiment_summary: Dict) -> Dict:
    """
    Main function: Generate comprehensive meaningful insights
    """
    if not results:
        return {
            'success': False,
            'error': 'No results to analyze',
            'timestamp': datetime.now().isoformat()
        }
    
    try:
        # Generate different types of insights
        meaningful_insights = generate_meaningful_insights(results, sentiment_summary)
        recommendations = generate_actionable_recommendations(results, sentiment_summary, {})
        
        keyword_sentiment = analyze_sentiment_by_keyword(results)
        problems = extract_problems_and_complaints(results)
        preferences = extract_preferences_and_desires(results)
        
        # Compile everything
        insights = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'key_insights': meaningful_insights,  # Main conclusions
            'sentiment_keywords': keyword_sentiment,  # What's being discussed
            'main_problems': problems,  # Issues to address
            'customer_desires': preferences,  # What people want
            'actionable_recommendations': recommendations,  # What to do
            'summary': {
                'total_analyzed': len(results),
                'positive_percentage': sentiment_summary.get('positive_percentage', 0),
                'negative_percentage': sentiment_summary.get('negative_percentage', 0),
                'neutral_percentage': sentiment_summary.get('neutral_percentage', 0),
            }
        }
        
        return insights
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Insights generation failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
