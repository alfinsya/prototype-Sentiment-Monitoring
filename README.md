# Web Monitoring - Sentiment Analysis & Insights

A comprehensive web platform to monitor mentions of products, services, or topics across multiple platforms (YouTube, Twitter, TikTok, Instagram, Google News) with sentiment analysis and AI-powered insights.

## Features

- 🔍 **Multi-Platform Search**: Search keywords across YouTube, Twitter, Google News, and more
- 📊 **Sentiment Analysis**: Automatic sentiment classification (Positive, Neutral, Negative)
- 📈 **Data Visualization**: Interactive charts and graphs for sentiment trends
- 🤖 **AI Insights**: AI-generated insights and recommendations
- 🖼️ **Media Gallery**: Aggregated images and videos from search results
- 📱 **Responsive Dashboard**: User-friendly interface for monitoring and analysis
- 💾 **Data Export**: Export reports in PDF/CSV format

## Project Structure

```
monitoring-web/
├── backend/          # Flask API backend
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.example
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend folder:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from `.env.example` and add your API keys:
   ```bash
   copy .env.example .env
   ```

5. Run the backend:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

## API Documentation

- `GET /api/health` - Health check
- `POST /api/search` - Search keywords across platforms
- `POST /api/sentiment` - Analyze sentiment of text
- `GET /api/insights` - Get AI insights

## Requirements

- Python 3.8+
- Node.js 14+
- MongoDB (local or Atlas)
- API Keys: YouTube, Twitter, Google

## License

MIT
