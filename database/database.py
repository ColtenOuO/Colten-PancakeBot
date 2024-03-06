from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB

client = AsyncIOMotorClient(**MONGO_DB.model_dump())

DB = client["pythondb"]
