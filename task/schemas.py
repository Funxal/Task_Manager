from pydantic import BaseModel

class TaskCreate(BaseModel):
    task: str
    priority: int

class TaskResponse(TaskCreate):
    id: int
