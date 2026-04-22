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
import './TopWordsChart.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function TopWordsChart({ results }) {
  if (!results || results.length === 0) {
    return <div className="chart-empty">No data available</div>;
  }

  // Extract all text and count word frequencies
  const wordFreq = {};
  const stopWords = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'have', 'has', 'do', 'does', 'can', 'could', 'would', 'should', 'may',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these',
    'those', 'as', 'if', 'because', 'then', 'so', 'not', 'no', 'yes',
  ]);

  results.forEach(result => {
    const text = (result.text || result.description || result.title || '').toLowerCase();
    const words = text.match(/\b[a-z]+\b/g) || [];
    
    words.forEach(word => {
      if (word.length > 3 && !stopWords.has(word)) {
        wordFreq[word] = (wordFreq[word] || 0) + 1;
      }
    });
  });

  // Get top 10 words
  const topWords = Object.entries(wordFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  if (topWords.length === 0) {
    return <div className="chart-empty">No keywords found</div>;
  }

  const data = {
    labels: topWords.map(([word]) => word),
    datasets: [
      {
        label: 'Word Frequency',
        data: topWords.map(([, count]) => count),
        backgroundColor: [
          'rgba(74, 144, 226, 0.8)',
          'rgba(52, 152, 219, 0.8)',
          'rgba(39, 174, 96, 0.8)',
          'rgba(155, 89, 182, 0.8)',
          'rgba(230, 126, 34, 0.8)',
          'rgba(231, 76, 60, 0.8)',
          'rgba(41, 128, 185, 0.8)',
          'rgba(26, 188, 156, 0.8)',
          'rgba(241, 196, 15, 0.8)',
          'rgba(142, 68, 173, 0.8)',
        ],
        borderColor: [
          'rgba(74, 144, 226, 1)',
          'rgba(52, 152, 219, 1)',
          'rgba(39, 174, 96, 1)',
          'rgba(155, 89, 182, 1)',
          'rgba(230, 126, 34, 1)',
          'rgba(231, 76, 60, 1)',
          'rgba(41, 128, 185, 1)',
          'rgba(26, 188, 156, 1)',
          'rgba(241, 196, 15, 1)',
          'rgba(142, 68, 173, 1)',
        ],
        borderWidth: 1,
        borderRadius: 6,
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 10,
        titleFont: { size: 13 },
        bodyFont: { size: 12 },
        callbacks: {
          label: function (context) {
            return 'Mentions: ' + context.parsed.x;
          },
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          font: { size: 11 },
        },
      },
      y: {
        grid: {
          display: false,
        },
        ticks: {
          font: { size: 11, weight: 'bold' },
        },
      },
    },
  };

  return (
    <div className="top-words-chart-container">
      <div className="chart-header">
        <h3>📊 Top 10 Keywords Frequency</h3>
        <p className="chart-description">Most frequently mentioned words in search results</p>
      </div>
      <div className="chart-wrapper">
        <Bar data={data} options={options} height={300} />
      </div>
      <div className="chart-footer">
        <small>Total unique keywords: {Object.keys(wordFreq).length}</small>
      </div>
    </div>
  );
}

export default TopWordsChart;
