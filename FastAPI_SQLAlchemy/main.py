import databases
import sqlalchemy
import uvicorn
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = 'sqlite:///my_database.db'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('email', sqlalchemy.String(128)),
)
# Параметр connect_args нужен только в случа работы с БД SQLite в одном фале,
# который влияет на взаимодействие потоков при общении БД и FastAPI
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     # Создаем таблицы
#     metadata.create_all(bind=engine)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


# # Для наполнения фековыми данными.
# @app.get("/fake_users/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = users.insert().values(name=f"Jhon{i}", email=f"Jhon{i}@mail.ru")
#         await database.execute(query)
#     return {"message": f"Created {count} fake users."}
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    # query = users.insert().values(name=user.name, email=user.email)
    query = users.insert().values(**user.dict())
    last_update = await database.execute(query)
    return {**user.dict(), "id": last_update}


@app.get("/user/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/user/{user_id}", response_model=User)
async def read_users(user_id):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_all(query)


@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete("/user/{user_id}", response_model=User)
async def delet_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message', 'User deleted'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
