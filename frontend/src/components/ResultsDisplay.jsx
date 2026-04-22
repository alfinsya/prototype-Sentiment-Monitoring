import React, { useState } from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ results }) {
  const [expandedId, setExpandedId] = useState(null);

  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'youtube':
        return '📺';
      case 'twitter':
        return '𝕏';
      case 'facebook':
        return 'f';
      case 'google_news':
        return '🔎';
      case 'instagram':
        return '📷';
      case 'tiktok':
        return '🎵';
      default:
        return '📄';
    }
  };

  const getSentimentBadge = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return { text: '👍 Positive', class: 'badge-positive' };
      case 'negative':
        return { text: '👎 Negative', class: 'badge-negative' };
      default:
        return { text: '➖ Neutral', class: 'badge-neutral' };
    }
  };

  const truncateText = (text, length = 150) => {
    return text && text.length > length ? text.substring(0, length) + '...' : text;
  };

  const getSourceName = (result) => {
    if (result.channel) return result.channel;
    if (result.author_name) return result.author_name;
    if (result.author) return result.author;
    if (result.source) return result.source;
    return 'Unknown Source';
  };

  const getThumbnail = (result) => {
    if (result.thumbnail) return result.thumbnail;
    if (result.image) return result.image;
    return 'https://via.placeholder.com/200x150?text=' + encodeURIComponent(getPlatformIcon(result.platform));
  };

  return (
    <div className="results-display">
      <div className="results-grid">
        {results.map((result, index) => {
          const sentiment = getSentimentBadge(result.sentiment || 'neutral');
          const isExpanded = expandedId === result.id;

          return (
            <div key={result.id || index} className="result-card">
              {/* Thumbnail */}
              <div className="result-thumbnail">
                <img
                  src={getThumbnail(result)}
                  alt={result.title || 'Result'}
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/200x150?text=No+Image';
                  }}
                />
                <div className="platform-badge">
                  {getPlatformIcon(result.platform)} {result.platform}
                </div>
              </div>

              {/* Content */}
              <div className="result-content">
                <div className="result-header">
                  <h3>{result.title || result.text?.substring(0, 80) || 'Untitled'}</h3>
                  <div className={`sentiment-badge ${sentiment.class}`}>
                    {sentiment.text}
                  </div>
                </div>

                <p className="result-description">
                  {truncateText(result.description || result.text || '', 120)}
                </p>

                <div className="result-meta">
                  <span className="meta-item">📌 {getSourceName(result)}</span>
                  {result.published_at && (
                    <span className="meta-item">
                      📅 {new Date(result.published_at).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {/* Sentiment Metrics */}
                <div className="sentiment-metrics">
                  {result.polarity !== undefined && (
                    <span className="metric">Polarity: {result.polarity.toFixed(2)}</span>
                  )}
                  {result.subjectivity !== undefined && (
                    <span className="metric">Subjectivity: {result.subjectivity.toFixed(2)}</span>
                  )}
                  {result.likes && result.likes !== 'N/A' && (
                    <span className="metric">👍 {result.likes}</span>
                  )}
                  {result.retweets && (
                    <span className="metric">🔄 {result.retweets}</span>
                  )}
                </div>

                {/* Actions */}
                <div className="result-actions">
                  <button
                    className="action-btn expand-btn"
                    onClick={() => setExpandedId(isExpanded ? null : result.id)}
                  >
                    {isExpanded ? 'Show Less' : 'Show More'}
                  </button>
                  <a href={result.url} target="_blank" rel="noopener noreferrer" className="action-btn link-btn">
                    View Source
                  </a>
                </div>

                {/* Expanded Content */}
                {isExpanded && (
                  <div className="expanded-content">
                    <p className="full-text">{result.text || result.description || ''}</p>
                    {result.channel && <p><strong>Channel:</strong> {result.channel}</p>}
                    {result.author && <p><strong>Author:</strong> {result.author}</p>}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ResultsDisplay;
