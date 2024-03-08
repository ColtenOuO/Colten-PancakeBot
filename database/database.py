from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB

client = AsyncIOMotorClient(**MONGO_DB.model_dump()) if MONGO_DB.srvServiceName is None else AsyncIOMotorClient(MONGO_DB.srvServiceName)

DB = client["pythondb"]
