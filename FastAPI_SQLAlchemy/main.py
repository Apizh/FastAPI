import databases
import sqlalchemy
import uvicorn
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
    name: str=Field(max_length=32)
    email: str=Field(max_length=128)


class User(BaseModel):
    id: int
    name: str=Field(max_length=32)
    email: str=Field( max_length=128)


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(name=f"Jhon{i}", email=f"Jhon{i}@mail.ru")
        await database.execute(query)
    return {"message": f"Created {count} fake users."}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
