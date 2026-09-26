import datetime
import json
import os

class StudentPlanner:
    def __init__(self, filename="planner.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, subject, deadline, priority, duration):
        task = {
            "title": title,
            "subject": subject,
            "deadline": deadline,
            "priority": priority,
            "duration": duration,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"\n✅ Task '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("\n📭 No tasks found.")
            return
        print("\n📌 Your Tasks:")
        for i, task in enumerate(self.tasks, 1):
            status = "✔️ Done" if task["completed"] else "⏳ Pending"
            duration = task.get("duration", 1)  # safe default
            print(f"{i}. {task['title']} ({task['subject']}) - Deadline: {task['deadline']} | Priority: {task['priority']} | Duration: {duration} hrs | Status: {status}")

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()
            print(f"\n🎉 Task '{self.tasks[index]['title']}' marked as completed!")
        else:
            print("\n❌ Invalid task index.")

    def upcoming_tasks(self):
        today = datetime.date.today()
        upcoming = [task for task in self.tasks if not task["completed"] and datetime.date.fromisoformat(task["deadline"]) >= today]
        upcoming.sort(key=lambda x: (x["priority"], x["deadline"]))
        if not upcoming:
            print("\n📭 No upcoming tasks.")
            return
        print("\n📅 Upcoming Tasks:")
        for task in upcoming:
            print(f"- {task['title']} ({task['subject']}) | Deadline: {task['deadline']} | Priority: {task['priority']}")

    def progress_report(self):
        if not self.tasks:
            print("\n📭 No tasks to track.")
            return
        completed = sum(1 for task in self.tasks if task["completed"])
        total = len(self.tasks)
        percent = (completed / total) * 100
        print(f"\n📊 Progress Report: {completed}/{total} tasks completed ({percent:.2f}%)")

    def study_schedule(self, hours_available):
        pending = [task for task in self.tasks if not task["completed"]]
        if not pending:
            print("\n🎉 All tasks completed! Free time unlocked.")
            return
        pending.sort(key=lambda x: (x["priority"], x["deadline"]))
        print(f"\n📅 Suggested Study Schedule for {hours_available} hrs:")
        allocated = 0
        for task in pending:
            if allocated >= hours_available:
                break
            # Safe default if duration missing
            duration = task.get("duration", 1)
            time_for_task = min(duration, hours_available - allocated)
            print(f"- {task['title']} ({task['subject']}) → {time_for_task} hrs")
            allocated += time_for_task

def main():
    planner = StudentPlanner()

    while True:
        print("\n=== Smart Student Planner ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. View Upcoming Tasks")
        print("5. Progress Report")
        print("6. Generate Study Schedule")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            subject = input("Enter subject: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            priority = input("Enter priority (High/Medium/Low): ")
            duration = float(input("Estimated duration (hours): "))
            planner.add_task(title, subject, deadline, priority, duration)
            input("\nPress Enter to continue...")

        elif choice == "2":
            planner.view_tasks()
            input("\nPress Enter to continue...")

        elif choice == "3":
            planner.view_tasks()
            index = int(input("Enter task number to mark as completed: ")) - 1
            planner.mark_completed(index)
            input("\nPress Enter to continue...")

        elif choice == "4":
            planner.upcoming_tasks()
            input("\nPress Enter to continue...")

        elif choice == "5":
            planner.progress_report()
            input("\nPress Enter to continue...")

        elif choice == "6":
            hours = float(input("Enter available study hours today: "))
            planner.study_schedule(hours)
            input("\nPress Enter to continue...")

        elif choice == "7":
            print("\n👋 Exiting Smart Student Planner. Stay productive!")
            break

        else:
            print("\n❌ Invalid choice. Try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
