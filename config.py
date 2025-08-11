# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API key for authentication
API_KEY = os.getenv("API_KEY", "changeme123")

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI", "")

# Server host and port (optional for local testing)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))