from datetime import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=4)


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=4)


class Product(BaseModel):
    id: int
    title: str = Field(max_length=50)
    description: str = Field(max_length=516)
    price: int = Field(default=0, ge=0)


class ProductIn(BaseModel):
    title: str = Field(max_length=64)
    description: str = Field(max_length=516)
    price: int = Field(default=0, ge=0)


class Order(BaseModel):
    id: int
    user_id: int
    prod_id: int
    date: datetime = Field(default=datetime.now())
    status: str = Field(default="created")


class OrderIn(BaseModel):
    user_id: int
    prod_id: int
    date: str
    status: str = Field(default="created")