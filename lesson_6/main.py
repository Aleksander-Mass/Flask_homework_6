from fastapi import FastAPI
import uvicorn
import user, order, product
from db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(user.router, tags=["users"])
app.include_router(order.router, tags=["orders"])
app.include_router(product.router, tags=["products"])


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)