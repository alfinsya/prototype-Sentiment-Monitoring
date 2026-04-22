import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import './PlatformDistributionChart.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function PlatformDistributionChart({ results }) {
  if (!results || results.length === 0) {
    return <div className="chart-empty">No data available</div>;
  }

  // Count mentions by platform
  const platformCounts = {};
  results.forEach(result => {
    const platform = result.platform || 'unknown';
    platformCounts[platform] = (platformCounts[platform] || 0) + 1;
  });

  // Platform colors and icons
  const platformColors = {
    youtube: 'rgba(255, 0, 0, 0.8)',
    twitter: 'rgba(29, 161, 242, 0.8)',
    facebook: 'rgba(59, 89, 152, 0.8)',
    instagram: 'rgba(217, 33, 125, 0.8)',
    tiktok: 'rgba(0, 0, 0, 0.8)',
    google_news: 'rgba(74, 144, 226, 0.8)',
  };

  const platformBorderColors = {
    youtube: 'rgba(255, 0, 0, 1)',
    twitter: 'rgba(29, 161, 242, 1)',
    facebook: 'rgba(59, 89, 152, 1)',
    instagram: 'rgba(217, 33, 125, 1)',
    tiktok: 'rgba(0, 0, 0, 1)',
    google_news: 'rgba(74, 144, 226, 1)',
  };

  const data = {
    labels: Object.keys(platformCounts).map(p => p.toUpperCase()),
    datasets: [
      {
        data: Object.values(platformCounts),
        backgroundColor: Object.keys(platformCounts).map(
          p => platformColors[p] || 'rgba(100, 100, 100, 0.8)'
        ),
        borderColor: Object.keys(platformCounts).map(
          p => platformBorderColors[p] || 'rgba(100, 100, 100, 1)'
        ),
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: { size: 12 },
          padding: 15,
          boxWidth: 12,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        callbacks: {
          label: function (context) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((context.parsed / total) * 100).toFixed(1);
            return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
          },
        },
      },
    },
  };

  return (
    <div className="platform-distribution-chart-container">
      <div className="chart-header">
        <h3>📱 Platform Distribution</h3>
        <p className="chart-description">Mentions breakdown by social media platform</p>
      </div>
      <div className="chart-wrapper">
        <Doughnut data={data} options={options} height={250} />
      </div>
      <div className="platform-stats">
        {Object.entries(platformCounts).map(([platform, count]) => (
          <div key={platform} className="stat-item">
            <span className="stat-label">{platform.toUpperCase()}</span>
            <span className="stat-value">{count} posts</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PlatformDistributionChart;
