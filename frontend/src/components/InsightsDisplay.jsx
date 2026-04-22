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
  const keyInsights = insightsData.key_insights || [];
  const sentimentKeywords = insightsData.sentiment_keywords || {};
  const mainProblems = insightsData.main_problems || [];
  const customerDesires = insightsData.customer_desires || [];
  const recommendations = insightsData.actionable_recommendations || [];
  const summary = insightsData.summary || {};

  return (
    <div className="insights-container">
      <div className="insights-header">
        <h2>🤖 AI Insights & Analysis</h2>
        <p className="insights-timestamp">
          Generated: {new Date(insightsData.timestamp).toLocaleString()}
        </p>
      </div>

      {/* Summary Stats */}
      <div className="insights-summary-stats">
        <div className="stat-item">
          <span className="stat-label">Positive</span>
          <span className="stat-value positive">{summary.positive_percentage || 0}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Neutral</span>
          <span className="stat-value neutral">{summary.neutral_percentage || 0}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Negative</span>
          <span className="stat-value negative">{summary.negative_percentage || 0}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Analyzed</span>
          <span className="stat-value">{summary.total_analyzed || 0}</span>
        </div>
      </div>

      {/* Key Insights / Kesimpulan Utama */}
      <div className="insights-section key-insights-section">
        <h3>📌 Key Insights & Conclusions</h3>
        <div className="insights-list">
          {keyInsights.map((insight, idx) => (
            <div key={idx} className="insight-item">
              <div className="insight-icon">
                {insight.includes('Strong Market')
                  ? '📈'
                  : insight.includes('Concern')
                  ? '⚠️'
                  : insight.includes('Positive')
                  ? '💚'
                  : insight.includes('Concern Area')
                  ? '💔'
                  : insight.includes('Main Issue')
                  ? '🔴'
                  : insight.includes('Market Want')
                  ? '🎯'
                  : insight.includes('Most Active')
                  ? '📱'
                  : '💡'}
              </div>
              <p className="insight-text">{insight}</p>
            </div>
          ))}
        </div>
      </div>

      {/* What People Are Saying (Sentiment by Keyword) */}
      {Object.keys(sentimentKeywords).length > 0 && (
        <div className="insights-section sentiment-keywords-section">
          <h3>💬 What People Are Saying</h3>
          <p className="section-description">
            Breakdown of sentiment by main topics
          </p>
          <div className="keywords-grid">
            {Object.entries(sentimentKeywords)
              .slice(0, 6)
              .map(([keyword, data]) => (
                <div key={keyword} className={`keyword-card sentiment-${data.sentiment}`}>
                  <div className="keyword-name">{keyword}</div>
                  <div className="keyword-stats">
                    <span className="stat positive">✓ {data.positive_pct}%</span>
                    <span className="stat negative">✗ {data.negative_pct}%</span>
                  </div>
                  <div className="keyword-mention">
                    {data.mentions} mentions
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Main Problems / Masalah Utama */}
      {mainProblems.length > 0 && (
        <div className="insights-section problems-section">
          <h3>⚠️ Main Issues to Address</h3>
          <div className="problems-list">
            {mainProblems.map((problem, idx) => (
              <div key={idx} className="problem-item">
                <div className="problem-header">
                  <span className="problem-icon">🔴</span>
                  <h4>{problem.issue}</h4>
                  <span className="problem-frequency">{problem.frequency} complaints</span>
                </div>
                <div className="problem-examples">
                  {problem.examples.map((example, eIdx) => (
                    <p key={eIdx} className="example-text">
                      "{example.substring(0, 100)}..."
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Customer Desires / Apa Yang Diinginkan Customer */}
      {customerDesires.length > 0 && (
        <div className="insights-section desires-section">
          <h3>💡 What Customers Want</h3>
          <div className="desires-list">
            {customerDesires.map((desire, idx) => (
              <div key={idx} className="desire-item">
                <div className="desire-header">
                  <span className="desire-icon">🎯</span>
                  <h4>{desire.type}</h4>
                  <span className="desire-frequency">{desire.frequency} mentions</span>
                </div>
                <div className="desire-examples">
                  {desire.examples.map((example, eIdx) => (
                    <p key={eIdx} className="example-text">
                      "{example.substring(0, 100)}..."
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actionable Recommendations */}
      {recommendations.length > 0 && (
        <div className="insights-section recommendations-section">
          <h3>🎯 Action Items & Recommendations</h3>
          <div className="recommendations-list">
            {recommendations.map((rec, idx) => (
              <div key={idx} className={`recommendation-item priority-${rec.priority.toLowerCase()}`}>
                <div className="recommendation-header">
                  <h4>{rec.title}</h4>
                  <span className={`priority-badge priority-${rec.priority.toLowerCase()}`}>
                    {rec.priority}
                  </span>
                </div>
                <p className="recommendation-description">{rec.description}</p>
                <div className="recommendation-action">
                  <h5>What to do:</h5>
                  <p>{rec.action}</p>
                </div>
                <div className="recommendation-impact">
                  <span className="impact-label">Expected Impact:</span>
                  <span className="impact-value">{rec.estimated_impact}</span>
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
