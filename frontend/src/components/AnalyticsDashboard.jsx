import React from 'react';
import TopWordsChart from './TopWordsChart';
import PlatformDistributionChart from './PlatformDistributionChart';
import SentimentByPlatformChart from './SentimentByPlatformChart';
import EngagementMetricsChart from './EngagementMetricsChart';
import SentimentChart from './SentimentChart';
import './AnalyticsDashboard.css';

function AnalyticsDashboard({ results, sentimentSummary, isLoading }) {
  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h2>📊 Analytics Dashboard</h2>
        <p>Comprehensive data visualization and insights</p>
      </div>

      {/* Row 1: Sentiment Overview + Platform Distribution */}
      <div className="analytics-grid-row">
        <div className="grid-col col-1">
          <SentimentChart data={sentimentSummary} />
        </div>
        <div className="grid-col col-1">
          <PlatformDistributionChart results={results} />
        </div>
      </div>

      {/* Row 2: Sentiment by Platform (Full Width) */}
      <div className="analytics-grid-row full-width">
        <div className="grid-col col-full">
          <SentimentByPlatformChart results={results} />
        </div>
      </div>

      {/* Row 3: Top Keywords + Engagement Metrics */}
      <div className="analytics-grid-row">
        <div className="grid-col col-1">
          <TopWordsChart results={results} />
        </div>
        <div className="grid-col col-1">
          <EngagementMetricsChart results={results} />
        </div>
      </div>

      {/* Analytics Summary */}
      <div className="analytics-summary">
        <div className="summary-card">
          <h4>📈 Total Results Analyzed</h4>
          <span className="summary-value">{results.length}</span>
        </div>
        <div className="summary-card">
          <h4>🎯 Average Polarity</h4>
          <span className="summary-value">
            {(
              results.reduce((sum, r) => sum + (r.polarity || 0), 0) / results.length
            ).toFixed(2)}
          </span>
        </div>
        <div className="summary-card">
          <h4>💬 Unique Platforms</h4>
          <span className="summary-value">
            {new Set(results.map(r => r.platform)).size}
          </span>
        </div>
        <div className="summary-card">
          <h4>🔍 Unique Keywords</h4>
          <span className="summary-value">
            {new Set(
              results
                .flatMap(r => (r.text || '').split(/\s+/))
                .filter(w => w.length > 3)
            ).size}
          </span>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
