import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './SentimentByPlatformChart.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function SentimentByPlatformChart({ results }) {
  if (!results || results.length === 0) {
    return <div className="chart-empty">No data available</div>;
  }

  // Group sentiment by platform
  const platformSentiments = {};

  results.forEach(result => {
    const platform = result.platform || 'unknown';
    const sentiment = result.sentiment || 'neutral';

    if (!platformSentiments[platform]) {
      platformSentiments[platform] = {
        positive: 0,
        neutral: 0,
        negative: 0,
      };
    }

    platformSentiments[platform][sentiment] += 1;
  });

  const platforms = Object.keys(platformSentiments);
  const positiveData = platforms.map(p => platformSentiments[p].positive);
  const neutralData = platforms.map(p => platformSentiments[p].neutral);
  const negativeData = platforms.map(p => platformSentiments[p].negative);

  const data = {
    labels: platforms.map(p => p.toUpperCase()),
    datasets: [
      {
        label: 'Positive',
        data: positiveData,
        backgroundColor: 'rgba(39, 174, 96, 0.8)',
        borderColor: 'rgba(39, 174, 96, 1)',
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Neutral',
        data: neutralData,
        backgroundColor: 'rgba(243, 156, 18, 0.8)',
        borderColor: 'rgba(243, 156, 18, 1)',
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Negative',
        data: negativeData,
        backgroundColor: 'rgba(231, 76, 60, 0.8)',
        borderColor: 'rgba(231, 76, 60, 1)',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: { size: 11 },
          padding: 10,
          boxWidth: 12,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 10,
        titleFont: { size: 12 },
        bodyFont: { size: 11 },
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        stacked: false,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          font: { size: 11 },
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          font: { size: 11 },
        },
      },
    },
  };

  return (
    <div className="sentiment-by-platform-chart-container">
      <div className="chart-header">
        <h3>📊 Sentiment Distribution by Platform</h3>
        <p className="chart-description">Positive, Neutral, and Negative mentions across platforms</p>
      </div>
      <div className="chart-wrapper">
        <Bar data={data} options={options} height={300} />
      </div>
    </div>
  );
}

export default SentimentByPlatformChart;
