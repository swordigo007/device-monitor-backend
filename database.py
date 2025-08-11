# database.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# Get Mongo URI from .env
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing in .env file")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Use a database (you can rename 'device_monitor')
db = client["device_monitor"]

# Example collections
devices_collection = db["devices"]
logs_collection = db["logs"]

# Example function: save device info
def save_device_info(data: dict):
    """Insert or update a device record."""
    devices_collection.update_one(
        {"device_id": data.get("device_id")},
        {"$set": data},
        upsert=True
    )

# Example function: save a log entry
def save_log(data: dict):
    """Insert a log entry."""
    logs_collection.insert_one(data)