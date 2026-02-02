from pydantic import BaseModel
from typing import Optional


class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    price: float
    mileage: int
    color: str
    condition: str
    description: Optional[str] = None


class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    description: Optional[str] = None


class CarResponse(BaseModel):
    id: str
    make: str
    model: str
    year: int
    price: float
    mileage: int
    color: str
    condition: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    car_id: str
    user_id: str
    price: float
    status: str = "Completed"


class OrderResponse(BaseModel):
    id: str
    car_id: str
    user_id: str
    price: float
    status: str

    class Config:
        from_attributes = True


class CarStatsByMake(BaseModel):
    make: str
    count: int
    avg_price: float
    total_mileage: int
    min_year: int
    max_year: int


class CarStatsByCondition(BaseModel):
    condition: str
    count: int
    avg_price: float


class CarAggregationStats(BaseModel):
    total_cars: int
    by_make: list[CarStatsByMake]
    by_condition: list[CarStatsByCondition]
    price_range: dict
