import React from 'react';
import './SentimentSummary.css';

function SentimentSummary({ data }) {
  if (!data) {
    return <div className="sentiment-summary">No data available</div>;
  }

  const getSentimentColor = (sentiment, value) => {
    if (sentiment === 'positive') return '#4CAF50';
    if (sentiment === 'negative') return '#f44336';
    return '#FFC107';
  };

  return (
    <div className="sentiment-summary">
      <h2>📊 Sentiment Analysis</h2>
      
      <div className="summary-stats">
        <div className="stat-item">
          <div className="stat-label">Total Results</div>
          <div className="stat-value">{data.total}</div>
        </div>

        <div className="stat-item positive">
          <div className="stat-label">Positive</div>
          <div className="stat-value">{data.positive}</div>
          <div className="stat-percent">{data.positive_percentage.toFixed(1)}%</div>
        </div>

        <div className="stat-item neutral">
          <div className="stat-label">Neutral</div>
          <div className="stat-value">{data.neutral}</div>
          <div className="stat-percent">{data.neutral_percentage.toFixed(1)}%</div>
        </div>

        <div className="stat-item negative">
          <div className="stat-label">Negative</div>
          <div className="stat-value">{data.negative}</div>
          <div className="stat-percent">{data.negative_percentage.toFixed(1)}%</div>
        </div>
      </div>

      <div className="avg-polarity">
        <div className="polarity-label">Average Polarity</div>
        <div className="polarity-bar">
          <div 
            className="polarity-fill" 
            style={{ 
              width: `${((data.average_polarity + 1) / 2) * 100}%`,
              backgroundColor: data.average_polarity > 0.1 ? '#4CAF50' : (data.average_polarity < -0.1 ? '#f44336' : '#FFC107')
            }}
          ></div>
        </div>
        <div className="polarity-value">{data.average_polarity.toFixed(3)}</div>
      </div>

      <div className="summary-info">
        <p>📌 Sentiment is classified as positive, negative, or neutral based on text analysis.</p>
      </div>
    </div>
  );
}

export default SentimentSummary;
