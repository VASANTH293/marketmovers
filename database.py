from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://vasanthperumal29:mdnZdJcAyw3ZmBIX@cluster0.ys0hthc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["stockdb"]
collection = db["leads"]
