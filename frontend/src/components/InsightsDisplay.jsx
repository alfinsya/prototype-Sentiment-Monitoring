import React from 'react';
import './InsightsDisplay.css';

function InsightsDisplay({ insights, loading }) {
  if (loading) {
    return (
      <div className="insights-container">
        <div className="insights-loading">
          <div className="insights-spinner"></div>
          <p>Generating AI insights...</p>
        </div>
      </div>
    );
  }

  if (!insights || !insights.success) {
    return null;
  }

  const insightsData = insights.insights || {};
  const sentimentAnalysis = insightsData.sentiment_analysis || {};
  const engagementAnalysis = insightsData.engagement_analysis || {};
  const topicsAndKeywords = insightsData.topics_and_keywords || {};
  const recommendations = insightsData.recommendations || [];
  const summary = insightsData.summary || {};

  return (
    <div className="insights-container">
      <div className="insights-header">
        <h2>🤖 AI Insights & Recommendations</h2>
        <p className="insights-timestamp">Generated: {new Date(insightsData.timestamp).toLocaleString()}</p>
      </div>

      {/* Overall Score */}
      <div className="insights-overall-score">
        <div className="score-card">
          <h3>Overall Analysis Score</h3>
          <div className="score-value">
            {(insightsData.overall_score * 100).toFixed(1)}%
          </div>
          <p className="score-description">
            {insightsData.overall_score > 0.7
              ? '✨ Excellent'
              : insightsData.overall_score > 0.4
              ? '👍 Good'
              : '⚠️ Needs Attention'}
          </p>
        </div>
      </div>

      {/* Sentiment Analysis Section */}
      <div className="insights-section sentiment-section">
        <h3>📊 Sentiment Trends</h3>
        <div className="sentiment-grid">
          <div className="sentiment-stat">
            <span className="stat-label">Trend Status</span>
            <span className={`stat-value trend-${sentimentAnalysis.trend_status}`}>
              {sentimentAnalysis.trend_status?.toUpperCase()}
            </span>
          </div>
          <div className="sentiment-stat">
            <span className="stat-label">Average Polarity</span>
            <span className="stat-value">
              {(sentimentAnalysis.average_polarity || 0).toFixed(3)}
            </span>
          </div>
          <div className="sentiment-stat">
            <span className="stat-label">Total Analyzed</span>
            <span className="stat-value">{sentimentAnalysis.total_analyzed || 0}</span>
          </div>
        </div>

        {sentimentAnalysis.sentiment_distribution && (
          <div className="sentiment-distribution">
            <p className="distribution-title">Sentiment Distribution:</p>
            <div className="distribution-bars">
              <div className="distribution-item">
                <label>Positive</label>
                <div className="bar-container">
                  <div
                    className="bar positive"
                    style={{
                      width: `${sentimentAnalysis.sentiment_percentages?.positive || 0}%`,
                    }}
                  ></div>
                </div>
                <span>{sentimentAnalysis.sentiment_percentages?.positive || 0}%</span>
              </div>
              <div className="distribution-item">
                <label>Neutral</label>
                <div className="bar-container">
                  <div
                    className="bar neutral"
                    style={{
                      width: `${sentimentAnalysis.sentiment_percentages?.neutral || 0}%`,
                    }}
                  ></div>
                </div>
                <span>{sentimentAnalysis.sentiment_percentages?.neutral || 0}%</span>
              </div>
              <div className="distribution-item">
                <label>Negative</label>
                <div className="bar-container">
                  <div
                    className="bar negative"
                    style={{
                      width: `${sentimentAnalysis.sentiment_percentages?.negative || 0}%`,
                    }}
                  ></div>
                </div>
                <span>{sentimentAnalysis.sentiment_percentages?.negative || 0}%</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Engagement Analysis Section */}
      <div className="insights-section engagement-section">
        <h3>👥 Engagement Metrics</h3>
        <div className="engagement-grid">
          <div className="engagement-stat">
            <span className="stat-label">Overall Engagement Score</span>
            <span className="stat-value">
              {(engagementAnalysis.overall_engagement_score * 100).toFixed(1)}%
            </span>
          </div>
          <div className="engagement-stat">
            <span className="stat-label">Engagement Level</span>
            <span className={`stat-value level-${engagementAnalysis.engagement_level}`}>
              {engagementAnalysis.engagement_level?.toUpperCase()}
            </span>
          </div>
          <div className="engagement-stat">
            <span className="stat-label">Total Mentions</span>
            <span className="stat-value">{engagementAnalysis.total_mentions || 0}</span>
          </div>
        </div>

        {engagementAnalysis.platform_metrics && Object.keys(engagementAnalysis.platform_metrics).length > 0 && (
          <div className="platform-breakdown">
            <p className="breakdown-title">Platform Breakdown:</p>
            <div className="platforms-list">
              {Object.entries(engagementAnalysis.platform_metrics).map(([platform, metrics]) => (
                <div key={platform} className="platform-item">
                  <div className="platform-name">{platform.toUpperCase()}</div>
                  <div className="platform-details">
                    <span className="metric">Posts: {metrics.count}</span>
                    <span className="metric">Engagement: {(metrics.engagement_score * 100).toFixed(1)}%</span>
                    <span className="metric">Polarity: {metrics.avg_polarity}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Topics & Keywords Section */}
      <div className="insights-section topics-section">
        <h3>🏷️ Topics & Keywords</h3>
        <div className="topics-grid">
          <div className="topics-subsection">
            <h4>Top Keywords</h4>
            <div className="keywords-list">
              {topicsAndKeywords.top_keywords &&
                topicsAndKeywords.top_keywords.map((keyword, idx) => (
                  <span key={idx} className="keyword-tag">
                    {keyword}
                  </span>
                ))}
            </div>
          </div>
          <div className="topics-subsection">
            <h4>Main Topics</h4>
            <div className="keywords-list">
              {topicsAndKeywords.main_topics &&
                topicsAndKeywords.main_topics.map((topic, idx) => (
                  <span key={idx} className="topic-tag">
                    {topic}
                  </span>
                ))}
            </div>
          </div>
        </div>
        <div className="topics-stats">
          <p>
            <strong>{topicsAndKeywords.total_unique_keywords || 0}</strong> unique keywords found
          </p>
          <p>
            <strong>{topicsAndKeywords.keyword_mentions || 0}</strong> total keyword mentions
          </p>
        </div>
      </div>

      {/* Recommendations Section */}
      {recommendations.length > 0 && (
        <div className="insights-section recommendations-section">
          <h3>💡 Actionable Recommendations</h3>
          <div className="recommendations-list">
            {recommendations.map((rec, idx) => (
              <div key={idx} className={`recommendation-card priority-${rec.priority}`}>
                <div className="recommendation-header">
                  <h4>{rec.title}</h4>
                  <span className={`priority-badge ${rec.priority}`}>{rec.priority.toUpperCase()}</span>
                </div>
                <p className="recommendation-description">{rec.description}</p>
                <div className="recommendation-action">
                  <span className="action-label">Action:</span>
                  <span className="action-text">{rec.action}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default InsightsDisplay;
