import threading
import time
from datetime import datetime
import pyttsx3
from plyer import notification

engine = pyttsx3.init()
tasks = []

def notify_task(task):
    """Alert user for a pending task: 10 times per minute for 3 minutes."""
    alerts = 30  # 10 alerts/min * 3 minutes
    for _ in range(alerts):
        if task['completed']:
            break  # Stop if completed
        notification.notify(
            title="Task Incomplete!",
            message=f"Task '{task['name']}' is still pending!",
            timeout=5
        )
        engine.say(f"Task {task['name']} is incomplete! Please check your tasks.")
        engine.runAndWait()
        time.sleep(6)  # 6 seconds between alerts

def check_tasks():
    """Continuously check all tasks and alert for pending tasks."""
    while True:
        now = datetime.now()
        for task in tasks:
            if not task['completed']:
                task_time = datetime.strptime(task['time'], "%Y-%m-%d %I:%M %p")
                # Only alert if current time >= task time
                if now >= task_time:
                    # Start alert thread
                    t = threading.Thread(target=notify_task, args=(task,), daemon=True)
                    t.start()
                    # Mark task as alerted for this check to avoid multiple threads simultaneously
                    task['alerted'] = True
        time.sleep(60)  # Check every minute for new tasks

def show_tasks():
    print("\nCurrent Tasks:")
    for i, task in enumerate(tasks, start=1):
        status = "Completed" if task['completed'] else "Pending"
        print(f"{i}. {task['name']} at {task['time']} - {status}")

def add_task_cli():
    name = input("Task Name: ").strip()
    date_str = input("Date & Time (YYYY-MM-DD HH:MM AM/PM): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d %I:%M %p")  # Validate format
        tasks.append({'name': name, 'time': date_str, 'completed': False})
        print(f"Task '{name}' added at {date_str}")
    except ValueError:
        print("Invalid date/time format! Use YYYY-MM-DD HH:MM AM/PM")

def mark_task_completed():
    show_tasks()
    idx = int(input("Enter task number to mark completed: ")) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]['completed'] = True
        print(f"Task '{tasks[idx]['name']}' marked as completed!")
    else:
        print("Invalid task number!")

def run_task_notifier_cli():
    threading.Thread(target=check_tasks, daemon=True).start()
    print("Priority Task Notifier running in background...")
    
    while True:
        print("\nOptions:\n1. Add Task\n2. Mark Task Completed\n3. Show Tasks\n4. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_task_cli()
        elif choice == "2":
            mark_task_completed()
        elif choice == "3":
            show_tasks()
        elif choice == "4":
            print("Exiting notifier CLI...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    run_task_notifier_cli()
