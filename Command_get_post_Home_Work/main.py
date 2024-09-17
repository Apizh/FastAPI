from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Модели данных
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskInResponse(Task):
    id: int


# Хранилище задач (в реальном приложении это будет база данных)
tasks_db = {}
next_id = 1


# Конечные точки API
@app.get("/tasks", response_model=List[TaskInResponse])
async def get_tasks():
    return [TaskInResponse(id=task_id, **task) for task_id, task in tasks_db.items()]


@app.get("/tasks/{task_id}", response_model=TaskInResponse)
async def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskInResponse(id=task_id, **task)


@app.post("/tasks", response_model=TaskInResponse)
async def create_task(task: Task):
    global next_id
    task_id = next_id
    next_id += 1
    tasks_db[task_id] = task.dict()
    return TaskInResponse(id=task_id, **tasks_db[task_id])


@app.put("/tasks/{task_id}", response_model=TaskInResponse)
async def update_task(task_id: int, task: Task):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id] = task.dict()
    return TaskInResponse(id=task_id, **tasks_db[task_id])


@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return {"detail": "Task deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="127.0.0.1", port=8000)
