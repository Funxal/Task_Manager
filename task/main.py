from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Task
from schemas import TaskCreate, TaskResponse
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    existing = db.query(Task).filter(Task.task == task.task).first()
    if existing:
        raise HTTPException(status_code=400, detail="Task already exists")

    new_task = Task(task=task.task, priority=task.priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(sort: str = None, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    if sort == "alpha":
        tasks.sort(key=lambda x: x.task)
    elif sort == "priority":
        tasks.sort(key=lambda x: x.priority)

    return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
