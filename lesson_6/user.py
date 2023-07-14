from fastapi import APIRouter, HTTPException
from db import users, database
from models import User, UserIn

router = APIRouter()


@router.get("/fake_users/{count}")
async def create_fake_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}',
                                      surname=f'surname{i}',
                                      email=f'test{i}@gmail.com',
                                      password=f'qwerty{i}')

        await database.execute(query)
    return {'message': f'{count} fake users created'}


@router.get("/users", response_model=list[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@router.post("/users", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user)
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}
