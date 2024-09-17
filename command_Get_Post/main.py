import logging
import uvicorn
from http.cookiejar import debug
from urllib.request import localhost

from fastapi import FastAPI
from model_verification import Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
async def root():
    logger.info('Обработал GET запрос.')
    return {'message': 'Hello world'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str = None):
    logger.info('Обработал GET запрос.')
    return {'item_id': item_id, 'q': q}


@app.post('/items/')
async def create_item(item: Item):
    logger.info('Обработал POST запрос.')
    return item


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    logger.info('Обработал PUT запрос.')
    return {'item_id': item_id, 'item': item}


@app.delete('/items/{item_id}')
async def delete_item(item_id: int):
    logger.info(f'Обработал DELETE запрос. {item_id}')
    return {'item_id': item_id}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)