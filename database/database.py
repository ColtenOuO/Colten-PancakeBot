from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URL, MONGO_DB_NAME

client = AsyncIOMotorClient(MONGO_DB_URL)

DB = client[MONGO_DB_NAME]
