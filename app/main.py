from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import (
    CarCreate, CarUpdate, CarResponse,
    CarAggregationStats,
    UserCreate, UserResponse, OrderCreate, OrderResponse,
)
from app.crud import CarCRUD, UserCRUD, OrderCRUD
from app.db import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.create_indexes()
    yield


app = FastAPI(title="Car Store API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5500", "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5500", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_car_crud() -> CarCRUD:
    return CarCRUD(get_db())


def get_user_crud() -> UserCRUD:
    return UserCRUD(get_db())


def get_order_crud() -> OrderCRUD:
    return OrderCRUD(get_db())


@app.get("/cars/", response_model=list[CarResponse])
async def get_cars(
    make: str | None = Query(None, description="Filter by make"),
    condition: str | None = Query(None, description="Filter by condition"),
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maximum price"),
    min_year: int | None = Query(None, description="Minimum year"),
    max_year: int | None = Query(None, description="Maximum year"),
    crud: CarCRUD = Depends(get_car_crud),
):
    return await crud.get_all_cars(
        make=make,
        condition=condition,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
    )


@app.post("/cars/", response_model=CarResponse)
async def create_car(car: CarCreate, crud: CarCRUD = Depends(get_car_crud)):
    return await crud.create_car(car)


@app.get("/cars/{car_id}", response_model=CarResponse)
async def get_car(car_id: str, crud: CarCRUD = Depends(get_car_crud)):
    return await crud.get_car_by_id(car_id)


@app.put("/cars/{car_id}", response_model=CarResponse)
async def update_car(car_id: str, car: CarUpdate, crud: CarCRUD = Depends(get_car_crud)):
    return await crud.update_car(car_id, car)


@app.delete("/cars/{car_id}", response_model=CarResponse)
async def delete_car(car_id: str, crud: CarCRUD = Depends(get_car_crud)):
    return await crud.delete_car(car_id)


@app.get("/cars/stats/aggregation", response_model=CarAggregationStats)
async def get_cars_aggregation_stats(
    make: str | None = Query(None, description="Filter by make before aggregation"),
    min_price: float | None = Query(None, description="Minimum price filter"),
    max_price: float | None = Query(None, description="Maximum price filter"),
    crud: CarCRUD = Depends(get_car_crud),
):
    return await crud.get_aggregation_stats(make=make, min_price=min_price, max_price=max_price)


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, crud: UserCRUD = Depends(get_user_crud)):
    return await crud.create_user(user)


@app.post("/users/login/")
async def login_user(email: str, password: str, crud: UserCRUD = Depends(get_user_crud)):
    user = await crud.authenticate_user(email, password)
    return {"message": "Login successful", "user_id": user.id, "email": user.email, "name": user.name}


@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, crud: OrderCRUD = Depends(get_order_crud)):
    return await crud.create_order(order)


@app.get("/orders/", response_model=list[OrderResponse])
async def get_orders(user_id: str = Query(..., description="User ID"), crud: OrderCRUD = Depends(get_order_crud)):
    return await crud.get_orders_by_user(user_id)
