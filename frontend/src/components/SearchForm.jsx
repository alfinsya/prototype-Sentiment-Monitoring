import React, { useState } from 'react';
import './SearchForm.css';

function SearchForm({ onSearch, loading }) {
  const [keyword, setKeyword] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [platforms, setPlatforms] = useState({
    youtube: true,
    twitter: true,
    facebook: true,
    google: true,
  });

  const handlePlatformChange = (platform) => {
    setPlatforms(prev => ({
      ...prev,
      [platform]: !prev[platform]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (keyword.trim()) {
      const selectedPlatforms = Object.keys(platforms).filter(p => platforms[p]);
      onSearch(keyword, selectedPlatforms, maxResults);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-input-group">
        <input
          type="text"
          placeholder="Search for products, brands, topics... (e.g., 'laptop samsung')"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          disabled={loading}
          className="search-input"
        />
        <button type="submit" disabled={loading || !keyword.trim()} className="search-button">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="form-controls">
        <div className="platforms-group">
          <label className="label">Platforms:</label>
          <div className="platform-checkboxes">
            {['youtube', 'twitter', 'facebook', 'google'].map(platform => (
              <label key={platform} className="platform-label">
                <input
                  type="checkbox"
                  checked={platforms[platform]}
                  onChange={() => handlePlatformChange(platform)}
                  disabled={loading}
                  className="platform-checkbox"
                />
                <span className="platform-name">
                  {platform === 'youtube' && '📺 YouTube'}
                  {platform === 'twitter' && '𝕏 Twitter'}
                  {platform === 'facebook' && 'f Facebook'}
                  {platform === 'google' && '🔎 Google'}
                </span>
              </label>
            ))}
          </div>
        </div>

        <div className="results-group">
          <label className="label">Results per platform:</label>
          <input
            type="number"
            min="1"
            max="50"
            value={maxResults}
            onChange={(e) => setMaxResults(e.target.value)}
            disabled={loading}
            className="results-input"
          />
        </div>
      </div>
    </form>
  );
}

export default SearchForm;
