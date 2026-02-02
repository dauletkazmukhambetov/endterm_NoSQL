from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pymongo.collection import Collection

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "car_store")


class MongoDB:
    def __init__(self, uri: str, db_name: str = DB_NAME):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    async def create_indexes(self) -> None:
        try:
            cars = self.db["cars"]
            users = self.db["users"]
            orders = self.db["orders"]

            await cars.create_index([("make", 1), ("year", -1)])
            await cars.create_index([("condition", 1), ("price", 1)])
            await cars.create_index([("make", 1), ("condition", 1)])
            await cars.create_index([("price", 1)])
            await cars.create_index([("year", -1)])

            await users.create_index([("email", 1)], unique=True)

            await orders.create_index([("user_id", 1)])
            await orders.create_index([("car_id", 1), ("user_id", 1)])
        except Exception:
            pass


def get_db() -> MongoDB:
    return MongoDB(MONGO_URI)
