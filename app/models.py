from typing import Optional
from pydantic import BaseModel


class Car(BaseModel):
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


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class Order(BaseModel):
    car_id: str
    user_id: str
    price: float
    status: str = "Completed"

    class Config:
        from_attributes = True
