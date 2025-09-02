# database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://vasanthperumal29:mdnZdJcAyw3ZmBIX@cluster0.ys0hthc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["stockdb"]

# 🔹 Specific functions for each collection
def get_users_collection():
    return db["users"]

def get_submissions_collection():
    return db["submissions"]

def get_stock_collection():
    return db["stocks"]  # example for dashboard if needed
