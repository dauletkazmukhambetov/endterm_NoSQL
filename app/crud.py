from app.db import MongoDB, get_db
from app.schemas import (
    CarCreate, CarUpdate, CarResponse,
    CarStatsByMake, CarStatsByCondition, CarAggregationStats,
    UserCreate, UserResponse, OrderCreate, OrderResponse,
)
from fastapi import HTTPException
from bson import ObjectId
from typing import Optional


class CarCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("cars")

    def _to_response(self, doc: dict) -> CarResponse:
        doc["id"] = str(doc["_id"])
        return CarResponse(**{k: v for k, v in doc.items() if k != "_id"})

    async def create_car(self, car: CarCreate) -> CarResponse:
        car_dict = car.model_dump() if hasattr(car, 'model_dump') else car.dict()
        result = await self.db.insert_one(car_dict)
        car_dict["id"] = str(result.inserted_id)
        return CarResponse(**car_dict)

    async def get_all_cars(
        self,
        make: Optional[str] = None,
        condition: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
    ) -> list[CarResponse]:
        query: dict = {}
        if make:
            query["make"] = make
        if condition:
            query["condition"] = condition
        if min_price is not None or max_price is not None:
            query["price"] = {}
            if min_price is not None:
                query["price"]["$gte"] = min_price
            if max_price is not None:
                query["price"]["$lte"] = max_price
        if min_year is not None or max_year is not None:
            query["year"] = {}
            if min_year is not None:
                query["year"]["$gte"] = min_year
            if max_year is not None:
                query["year"]["$lte"] = max_year

        cars = []
        cursor = self.db.find(query).sort("make", 1).sort("year", -1)
        async for doc in cursor:
            cars.append(self._to_response(dict(doc)))
        return cars

    async def get_car_by_id(self, car_id: str) -> CarResponse:
        doc = await self.db.find_one({"_id": ObjectId(car_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Car not found")
        return self._to_response(dict(doc))

    async def update_car(self, car_id: str, car: CarUpdate) -> CarResponse:
        update_dict = {
            k: v
            for k, v in (car.model_dump() if hasattr(car, 'model_dump') else car.dict()).items()
            if v is not None
        }
        if not update_dict:
            return await self.get_car_by_id(car_id)
        result = await self.db.update_one(
            {"_id": ObjectId(car_id)},
            {"$set": update_dict},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Car not found")
        return await self.get_car_by_id(car_id)

    async def delete_car(self, car_id: str) -> CarResponse:
        doc = await self.db.find_one({"_id": ObjectId(car_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Car not found")
        await self.db.delete_one({"_id": ObjectId(car_id)})
        return self._to_response(dict(doc))

    async def get_aggregation_stats(
        self,
        make: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> CarAggregationStats:
        match_stage: dict = {}
        if make:
            match_stage["make"] = make
        if min_price is not None or max_price is not None:
            match_stage["price"] = {}
            if min_price is not None:
                match_stage["price"]["$gte"] = min_price
            if max_price is not None:
                match_stage["price"]["$lte"] = max_price

        pipeline = []
        if match_stage:
            pipeline.append({"$match": match_stage})

        pipeline.append(
            {
                "$facet": {
                    "by_make": [
                        {"$group": {"_id": "$make", "count": {"$sum": 1}, "avg_price": {"$avg": "$price"}, "total_mileage": {"$sum": "$mileage"}, "min_year": {"$min": "$year"}, "max_year": {"$max": "$year"}}},
                        {"$sort": {"count": -1}},
                        {"$project": {"make": "$_id", "count": 1, "avg_price": {"$round": ["$avg_price", 2]}, "total_mileage": 1, "min_year": 1, "max_year": 1, "_id": 0}},
                    ],
                    "by_condition": [
                        {"$group": {"_id": "$condition", "count": {"$sum": 1}, "avg_price": {"$avg": "$price"}}},
                        {"$sort": {"count": -1}},
                        {"$project": {"condition": "$_id", "count": 1, "avg_price": {"$round": ["$avg_price", 2]}, "_id": 0}},
                    ],
                    "price_range": [
                        {"$group": {"_id": None, "min": {"$min": "$price"}, "max": {"$max": "$price"}, "avg": {"$avg": "$price"}}},
                        {"$project": {"min": {"$round": ["$min", 2]}, "max": {"$round": ["$max", 2]}, "avg": {"$round": ["$avg", 2]}, "_id": 0}},
                    ],
                    "total": [{"$count": "count"}],
                }
            }
        )

        result = None
        async for doc in self.db.aggregate(pipeline):
            result = doc
            break

        if not result:
            return CarAggregationStats(
                total_cars=0,
                by_make=[],
                by_condition=[],
                price_range={"min": 0, "max": 0, "avg": 0},
            )

        total = result.get("total", [{}])[0].get("count", 0)
        price_range = result.get("price_range", [{}])[0] if result.get("price_range") else {"min": 0, "max": 0, "avg": 0}

        return CarAggregationStats(
            total_cars=total,
            by_make=[CarStatsByMake(**m) for m in result.get("by_make", [])],
            by_condition=[CarStatsByCondition(**c) for c in result.get("by_condition", [])],
            price_range=price_range,
        )


class UserCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("users")

    async def create_user(self, user: UserCreate) -> UserResponse:
        u_dict = user.model_dump() if hasattr(user, 'model_dump') else user.dict()
        existing = await self.db.find_one({"email": u_dict["email"]})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        result = await self.db.insert_one(u_dict)
        u_dict["id"] = str(result.inserted_id)
        return UserResponse(**{k: v for k, v in u_dict.items() if k != "password"})

    async def authenticate_user(self, email: str, password: str) -> UserResponse:
        doc = await self.db.find_one({"email": email})
        if not doc or doc.get("password") != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        doc["id"] = str(doc["_id"])
        return UserResponse(**{k: v for k, v in doc.items() if k not in ("_id", "password")})


class OrderCRUD:
    def __init__(self, db: MongoDB):
        self.db = db.get_collection("orders")

    def _to_response(self, doc: dict) -> OrderResponse:
        doc["id"] = str(doc["_id"])
        return OrderResponse(**{k: v for k, v in doc.items() if k != "_id"})

    async def create_order(self, order: OrderCreate) -> OrderResponse:
        o_dict = order.model_dump() if hasattr(order, 'model_dump') else order.dict()
        result = await self.db.insert_one(o_dict)
        o_dict["id"] = str(result.inserted_id)
        return OrderResponse(**o_dict)

    async def get_orders_by_user(self, user_id: str) -> list[OrderResponse]:
        orders = []
        async for doc in self.db.find({"user_id": user_id}):
            orders.append(self._to_response(dict(doc)))
        return orders
