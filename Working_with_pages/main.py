from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory='./templates')


@app.get('/')
async def read_root():
    return {'First message': 'Hello, World!'}


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}


@app.get('/page/', response_class=HTMLResponse)
async def read_page():
    return "<h1>Hello World<br><em>This`s new page!</em></h1>"


@app.get('/message/')
async def read_message():
    message = {'New message': 'Second Hello World'}
    return JSONResponse(content=message, status_code=200)


@app.get('/name/{name}/', response_class=HTMLResponse)
async def read_items(request: Request, name: str):
    print(request)
    return templates.TemplateResponse("item.html", {"request": request, "name": name})


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080)
