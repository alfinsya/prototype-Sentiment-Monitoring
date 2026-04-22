import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './EngagementMetricsChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function EngagementMetricsChart({ results }) {
  if (!results || results.length === 0) {
    return <div className="chart-empty">No data available</div>;
  }

  // Calculate engagement metrics
  const engagementData = results.map((result, idx) => {
    const likes = parseInt(result.likes) || 0;
    const comments = parseInt(result.comments) || 0;
    const retweets = parseInt(result.retweets) || 0;
    const shares = parseInt(result.shares) || 0;
    
    const totalEngagement = likes + comments + retweets + shares;
    
    // Polarity score
    const polarity = result.polarity || 0;
    
    return {
      index: idx + 1,
      engagement: totalEngagement,
      polarity: polarity,
    };
  });

  // Sort by index and take last 20
  const displayData = engagementData.slice(-20);

  const data = {
    labels: displayData.map(d => `#${d.index}`),
    datasets: [
      {
        label: 'Engagement Score',
        data: displayData.map(d => d.engagement),
        borderColor: 'rgba(74, 144, 226, 1)',
        backgroundColor: 'rgba(74, 144, 226, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(74, 144, 226, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverRadius: 6,
        yAxisID: 'y',
      },
      {
        label: 'Polarity Score',
        data: displayData.map(d => (d.polarity + 1) * 10), // Scale to 0-20 for visibility
        borderColor: 'rgba(155, 89, 182, 1)',
        backgroundColor: 'rgba(155, 89, 182, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointBackgroundColor: 'rgba(155, 89, 182, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointHoverRadius: 6,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
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
        padding: 12,
        titleFont: { size: 12 },
        bodyFont: { size: 11 },
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          font: { size: 10 },
        },
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        grid: {
          color: 'rgba(74, 144, 226, 0.1)',
        },
        ticks: {
          font: { size: 11 },
        },
        title: {
          display: true,
          text: 'Engagement',
          font: { size: 11 },
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: {
          drawOnChartArea: false,
        },
        ticks: {
          font: { size: 11 },
          callback: function (value) {
            return ((value / 10) - 1).toFixed(1);
          },
        },
        title: {
          display: true,
          text: 'Polarity',
          font: { size: 11 },
        },
      },
    },
  };

  return (
    <div className="engagement-metrics-chart-container">
      <div className="chart-header">
        <h3>📈 Engagement Metrics Trend</h3>
        <p className="chart-description">Engagement score and polarity for recent mentions (last 20)</p>
      </div>
      <div className="chart-wrapper">
        <Line data={data} options={options} height={300} />
      </div>
    </div>
  );
}

export default EngagementMetricsChart;
