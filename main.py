from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

# -------------------------
# DATA STRUCTURES
# -------------------------

class Node:
    def __init__(self, task, priority):
        self.task = task
        self.priority = priority
        self.next = None

class TaskManager:
    def __init__(self):
        self.head = None
        self.tasks_set = set()
        self.undo_stack = []

    def add_task(self, task, priority):
        if task in self.tasks_set:
            return False
        new_node = Node(task, priority)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.tasks_set.add(task)
        self.undo_stack.append(("delete", task))
        return True

    def delete_task(self, task):
        cur = self.head
        prev = None
        while cur and cur.task != task:
            prev = cur
            cur = cur.next
        if not cur:
            return False
        if prev:
            prev.next = cur.next
        else:
            self.head = cur.next
        self.tasks_set.remove(task)
        self.undo_stack.append(("add", cur.task, cur.priority))
        return True

    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        if action[0] == "add":
            _, task, priority = action
            self.add_task(task, priority)
            self.undo_stack.pop()
        elif action[0] == "delete":
            _, task = action
            self.delete_task(task)
            self.undo_stack.pop()

    def get_tasks(self, sort=None):
        tasks = []
        cur = self.head
        while cur:
            tasks.append({"task": cur.task, "priority": cur.priority})
            cur = cur.next

        if sort == "alpha":
            tasks.sort(key=lambda x: x["task"])
        elif sort == "priority":
            tasks.sort(key=lambda x: x["priority"])

        return tasks

# -------------------------
# FASTAPI APP
# -------------------------

app = FastAPI()
manager = TaskManager()

# -------------------------
# MODELS
# -------------------------

class Task(BaseModel):
    task: str
    priority: int

# -------------------------
# ROUTES
# -------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()

@app.post("/add")
def add(task: Task):
    success = manager.add_task(task.task, task.priority)
    return {"success": success, "tasks": manager.get_tasks()}

@app.post("/delete")
def delete(task: dict):
    success = manager.delete_task(task["task"])
    return {"success": success, "tasks": manager.get_tasks()}

@app.post("/undo")
def undo():
    manager.undo()
    return {"tasks": manager.get_tasks()}

@app.get("/tasks")
def tasks(sort: str = None):
    return manager.get_tasks(sort)
