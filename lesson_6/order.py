import datetime
from fastapi import APIRouter, HTTPException
from db import orders, database
from random import randint
from models import Order, OrderIn

router = APIRouter()


@router.get("/fake_orders/{count}")
async def create_note(count: int):
    for i in range(count):
        query = orders.insert().values(user_id=randint(1, 20),
                                       prod_id=randint(1, 20),
                                       status="created",
                                       date=datetime.datetime.now())
        await database.execute(query)
    return {'message': f'{count} fake orders created'}


@router.get("/orders", response_model=list[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router.post("/orders", response_model=Order)
async def create_order(order: OrderIn):
    query = order.insert().values(
        user_id=order.user_id,
        prod_id=order.prod_id,
        status=order.status,
        date=order.date
    )
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    query = orders.select().where(database.orders.c.id == order_id)
    return await database.fetch_one(query)


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order)
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}