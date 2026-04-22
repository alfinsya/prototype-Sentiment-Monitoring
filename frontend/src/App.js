import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import SentimentSummary from './components/SentimentSummary';
import SentimentChart from './components/SentimentChart';
import ResultsDisplay from './components/ResultsDisplay';
import InsightsDisplay from './components/InsightsDisplay';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [sentimentSummary, setSentimentSummary] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedPlatforms, setSelectedPlatforms] = useState(['youtube', 'twitter', 'facebook', 'google']);

  const handleSearch = async (keyword, platforms, maxResults) => {
    setLoading(true);
    setError(null);
    setResults([]);
    setSentimentSummary(null);
    setInsights(null);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keyword,
          platforms,
          max_results: parseInt(maxResults),
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setResults(data.results || []);
        setSentimentSummary(data.sentiment_summary);
        setSelectedPlatforms(platforms);

        // Log API warnings if any
        if (data.errors && data.errors.length > 0) {
          console.warn('API Warnings:', data.errors);
        }

        // Fetch insights after successful search
        if (data.results && data.sentiment_summary) {
          fetchInsights(data.results, data.sentiment_summary);
        }
      } else {
        setError(data.error || 'Search failed');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchInsights = async (searchResults, sentimentSummary) => {
    setInsightsLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/insights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          results: searchResults,
          sentiment_summary: sentimentSummary,
        }),
      });

      if (!response.ok) {
        console.warn('Insights API error:', response.status);
        return;
      }

      const data = await response.json();

      if (data.success) {
        setInsights(data);
      }
    } catch (err) {
      console.warn('Error fetching insights:', err.message);
      // Don't show error to user, insights are optional
    } finally {
      setInsightsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>🔍 Sentiment Monitor</h1>
          <p>Monitor mentions, analyze sentiment, and get insights across multiple platforms</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container">
        {/* Search Section */}
        <SearchForm onSearch={handleSearch} loading={loading} />

        {/* Error Display */}
        {error && (
          <div className="error-box">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading-box">
            <div className="spinner"></div>
            <p>Searching across platforms...</p>
          </div>
        )}

        {/* Results Section */}
        {results.length > 0 && !loading && (
          <div className="results-section">
            {/* Analytics Dashboard */}
            <AnalyticsDashboard 
              results={results} 
              sentimentSummary={sentimentSummary}
              isLoading={loading}
            />

            {/* AI Insights */}
            <InsightsDisplay insights={insights} loading={insightsLoading} />

            {/* Results Display */}
            <div className="results-box">
              <h2>Results ({results.length})</h2>
              <ResultsDisplay results={results} />
            </div>
          </div>
        )}

        {/* No Results Message */}
        {results.length === 0 && !loading && !error && (
          <div className="no-results-box">
            <p>🔎 Enter a keyword and click Search to get started</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2026 Sentiment Monitor. Powered by YouTube, Twitter, Facebook & Google data.</p>
      </footer>
    </div>
  );
}

export default App;
