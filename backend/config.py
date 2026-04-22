import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'monitoring_web')

def init_db():
    """Initialize MongoDB connection"""
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        # Test connection
        client.admin.command('ping')
        print("MongoDB connected successfully!")
        return db
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

# API Keys Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY', '')
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')

# Optional: OpenAI or Hugging Face for advanced AI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
