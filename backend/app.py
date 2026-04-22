from flask import Flask, jsonify, request
from flask_cors import CORS
from config import init_db
import os
from dotenv import load_dotenv

# Import service modules
from services.youtube_service import search_youtube
from services.twitter_service import search_twitter
from services.facebook_service import search_facebook_posts
from services.google_service import search_google
from services.sentiment_service import analyze_sentiment, analyze_sentiments_batch, get_sentiment_summary
from services.dummy_data import get_dummy_tweets, get_dummy_facebook_posts, get_dummy_google_results

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize database connection (optional for MVP)
db = init_db()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'API is running', 'message': 'Monitoring Web Backend'}), 200

@app.route('/api/search', methods=['POST'])
def search():
    """
    Multi-platform search endpoint
    Body: {
        "keyword": "laptop samsung",
        "platforms": ["youtube", "twitter", "facebook", "google"],
        "max_results": 10
    }
    """
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        platforms = data.get('platforms', ['youtube', 'twitter', 'facebook', 'google'])
        max_results = data.get('max_results', 10)
        
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        
        if not isinstance(platforms, list) or len(platforms) == 0:
            return jsonify({'error': 'Platforms must be a non-empty list'}), 400
        
        # Aggregate results from all platforms
        all_results = []
        errors = []
        
        if 'youtube' in platforms:
            youtube_result = search_youtube(keyword, max_results)
            if youtube_result.get('success'):
                all_results.extend(youtube_result.get('results', []))
            else:
                errors.append(f"YouTube: {youtube_result.get('error', 'Unknown error')}")
        
        if 'twitter' in platforms:
            twitter_result = search_twitter(keyword, max_results)
            if twitter_result.get('success'):
                all_results.extend(twitter_result.get('results', []))
            else:
                # Use dummy data as fallback
                dummy_result = get_dummy_tweets(keyword, max_results)
                all_results.extend(dummy_result.get('results', []))
                errors.append(f"Twitter: Using mock data (API error: {twitter_result.get('error', 'Unknown')})")
        
        if 'facebook' in platforms:
            facebook_result = search_facebook_posts(keyword, max_results)
            if facebook_result.get('success'):
                all_results.extend(facebook_result.get('results', []))
            else:
                # Use dummy data as fallback
                dummy_result = get_dummy_facebook_posts(keyword, max_results)
                all_results.extend(dummy_result.get('results', []))
                errors.append(f"Facebook: Using mock data (API error: {facebook_result.get('error', 'Unknown')})")
        
        if 'google' in platforms:
            google_result = search_google(keyword, max_results)
            if google_result.get('success'):
                all_results.extend(google_result.get('results', []))
            else:
                # Use dummy data as fallback
                dummy_result = get_dummy_google_results(keyword, max_results)
                all_results.extend(dummy_result.get('results', []))
                errors.append(f"Google: Using mock data (API error: {google_result.get('error', 'Unknown')})")
        
        # Analyze sentiment for text content
        for result in all_results:
            text_to_analyze = result.get('text', result.get('description', ''))
            if text_to_analyze:
                sentiment = analyze_sentiment(text_to_analyze)
                result['sentiment'] = sentiment.get('sentiment', 'unknown')
                result['polarity'] = sentiment.get('polarity', 0)
                result['subjectivity'] = sentiment.get('subjectivity', 0)
        
        # Generate sentiment summary
        sentiments = [r.get('sentiment', 'unknown') for r in all_results]
        sentiment_summary = get_sentiment_summary(all_results)
        
        response = {
            'success': True,
            'keyword': keyword,
            'platforms': platforms,
            'total_results': len(all_results),
            'results': all_results,
            'sentiment_summary': sentiment_summary,
            'errors': errors if errors else None
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/api/sentiment', methods=['POST'])
def sentiment():
    """
    Analyze sentiment of text
    Body: {
        "text": "This product is amazing!",
        "batch": false (optional, for multiple texts)
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = analyze_sentiment(text)
        return jsonify({'success': True, 'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': f'Sentiment analysis failed: {str(e)}'}), 500

@app.route('/api/sentiment/batch', methods=['POST'])
def sentiment_batch():
    """
    Analyze sentiment of multiple texts
    Body: {
        "texts": ["text1", "text2", "text3"]
    }
    """
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not isinstance(texts, list) or len(texts) == 0:
            return jsonify({'error': 'Texts must be a non-empty list'}), 400
        
        results = analyze_sentiments_batch(texts)
        summary = get_sentiment_summary(results)
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Batch sentiment analysis failed: {str(e)}'}), 500

@app.route('/api/insights', methods=['GET'])
def insights():
    """
    Get AI insights based on search results
    """
    try:
        # TODO: Implement advanced AI insights
        # For now, return placeholder
        return jsonify({
            'message': 'AI insights - coming soon',
            'features': ['sentiment trends', 'engagement analysis', 'topic extraction', 'recommendations']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Insights generation failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
