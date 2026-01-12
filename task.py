import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, priority, deadline):
        task = {
            "title": title,
            "priority": priority,
            "deadline": deadline,
            "done": False
        }
        self.tasks.append(task)
        self.save()
        print("✅ Task added")

    def view_tasks(self):
        if not self.tasks:
            print("📭 No tasks")
            return

        for i, t in enumerate(self.tasks, 1):
            status = "✔" if t["done"] else "❌"
            print(f"{i}. {t['title']} | {t['priority']} | Due: {t['deadline']} | {status}")

    def mark_done(self, index):
        self.tasks[index]["done"] = True
        self.save()

    def delete(self, index):
        self.tasks.pop(index)
        self.save()

    def search(self, keyword):
        results = [t for t in self.tasks if keyword.lower() in t["title"].lower()]
        for t in results:
            print(t)

def menu():
    print("""
1. Add task
2. View tasks
3. Mark done
4. Delete task
5. Search
6. Exit
""")

def main():
    tm = TaskManager()

    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            title = input("Title: ")
            priority = input("Priority (Low/Medium/High): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            tm.add_task(title, priority, deadline)

        elif choice == "2":
            tm.view_tasks()

        elif choice == "3":
            tm.view_tasks()
            tm.mark_done(int(input("Task number: ")) - 1)

        elif choice == "4":
            tm.view_tasks()
            tm.delete(int(input("Task number: ")) - 1)

        elif choice == "5":
            tm.search(input("Keyword: "))

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
