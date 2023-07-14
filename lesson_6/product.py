from random import randint
from fastapi import APIRouter, HTTPException
from db import products, database
from models import Product, ProductIn

router = APIRouter()


@router.get("/fake_products/{count}")
async def create_fake_products(count: int):
    for i in range(count):
        query = products.insert().values(title=f'product {i}',
                                         description=f'description {i}',
                                         price=randint(1, 10000))
        await database.execute(query)
    return {'message': f'{count} fake products created'}


@router.get("/products", response_model=list[Product])
async def get_products():
    query = database.products.select()
    return await database.database.fetch_all(query)


@router.post("/products", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(
        title=product.title,
        description=product.description,
        price=product.price
    )
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@router.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id ==
                                    product_id).values(**new_product)
    await database.database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = database.products.delete().where(products.c.id == product_id)
    await database.database.execute(query)
    return {'message': 'Product deleted'}