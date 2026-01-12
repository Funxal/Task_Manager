from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks")
def create_task(title: str, priority: str, deadline: str, db: Session = Depends(get_db)):
    task = Task(title=title, priority=priority, deadline=deadline)
    db.add(task)
    db.commit()
    return {"message": "Task added"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.put("/tasks/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    task.done = True
    db.commit()
    return {"message": "Task completed"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
