from flask import Flask, render_template, request, redirect, url_for
# Import TaskManager classes
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class TaskManager:
    def __init__(self):
        self.head = None
        self.tasks_set = set()
        self.undo_stack = []

    def add_task(self, task):
        if task in self.tasks_set:
            return False
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.tasks_set.add(task)
        self.undo_stack.append(("delete", task))
        return True

    def delete_task(self, task):
        current = self.head
        prev = None
        while current and current.task != task:
            prev = current
            current = current.next
        if not current:
            return False
        if prev:
            prev.next = current.next
        else:
            self.head = current.next
        self.tasks_set.remove(task)
        self.undo_stack.append(("add", task))
        return True

    def undo(self):
        if not self.undo_stack:
            return "Nothing to undo"
        action, task = self.undo_stack.pop()
        if action == "add":
            self.add_task(task)
            self.undo_stack.pop()
            return f"Task '{task}' restored"
        elif action == "delete":
            self.delete_task(task)
            self.undo_stack.pop()
            return f"Task '{task}' removed"

    def list_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks

manager = TaskManager()

app = Flask(__name__)

# -----------------------
# ROUTES
# -----------------------
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        task = request.form.get("task")

        if action == "add" and task:
            if manager.add_task(task):
                message = f"Task '{task}' added"
            else:
                message = f"Task '{task}' already exists"

        elif action == "delete" and task:
            if manager.delete_task(task):
                message = f"Task '{task}' deleted"
            else:
                message = f"Task '{task}' not found"

        elif action == "undo":
            message = manager.undo()

    tasks = manager.list_tasks()
    return render_template("index.html", tasks=tasks, message=message)

if __name__ == "__main__":
    app.run(debug=True)
