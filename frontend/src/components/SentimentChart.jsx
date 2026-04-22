import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import './SentimentChart.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function SentimentChart({ data }) {
  if (!data) {
    return <div className="sentiment-chart">No data available</div>;
  }

  const chartData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        label: 'Sentiment Distribution',
        data: [data.positive_percentage, data.neutral_percentage, data.negative_percentage],
        backgroundColor: [
          '#4CAF50', // Positive - Green
          '#FFC107', // Neutral - Amber
          '#f44336', // Negative - Red
        ],
        borderColor: ['#388E3C', '#FFA000', '#d32f2f'],
        borderWidth: 2,
        hoverOffset: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          font: {
            size: 13,
            weight: '600',
          },
          padding: 20,
          usePointStyle: true,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: ${context.parsed}%`;
          }
        }
      }
    },
  };

  return (
    <div className="sentiment-chart">
      <h2>📈 Sentiment Distribution</h2>
      <div className="chart-container">
        <Pie data={chartData} options={options} />
      </div>
    </div>
  );
}

export default SentimentChart;
