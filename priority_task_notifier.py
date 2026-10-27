import threading
import time
from datetime import datetime
import pyttsx3
from plyer import notification

engine = pyttsx3.init()
tasks = []
running_alerts = {}  # Store running alert threads' stop flags

def repeated_alert(task_name, stop_flag):
    """Continuously send alerts until stop_flag['stop'] is True."""
    while not stop_flag['stop']:
        print(f"🔔 Alert for task '{task_name}'")
        notification.notify(
            title="Task Reminder",
            message=f"Task '{task_name}' is still pending!",
            timeout=5
        )
        engine.say(f"Task {task_name} is still pending! Please complete it.")
        engine.runAndWait()
        time.sleep(10)
    print(f"🛑 Alerts stopped for task '{task_name}'.")

def start_alert(task_name):
    """Start alert thread for given task if not already running."""
    if task_name in running_alerts and not running_alerts[task_name]['stop']:
        print(f"⚠️ Alerts already running for '{task_name}'!")
        return
    stop_flag = {'stop': False}
    running_alerts[task_name] = stop_flag
    t = threading.Thread(target=repeated_alert, args=(task_name, stop_flag), daemon=True)
    t.start()
    print(f"🚀 Started alerts for '{task_name}'.")

def stop_alert(task_name):
    """Stop alert thread for given task if running."""
    if task_name in running_alerts:
        running_alerts[task_name]['stop'] = True
        print(f"🛑 Stopping alerts for '{task_name}'...")
        del running_alerts[task_name]
    else:
        print(f"❌ No running alerts found for '{task_name}'.")

def add_task():
    name = input("Task Name: ").strip()
    date_str = input("Date & Time (YYYY-MM-DD HH:MM AM/PM): ").strip()
    try:
        task_time = datetime.strptime(date_str, "%Y-%m-%d %I:%M %p")
        tasks.append({'name': name, 'time': task_time, 'completed': False})
        print(f"✅ Task '{name}' added at {task_time.strftime('%Y-%m-%d %I:%M %p')}")
    except ValueError:
        print("❌ Invalid date/time format! Use YYYY-MM-DD HH:MM AM/PM")

def show_tasks():
    print("\n📋 Tasks List:")
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        status = "Completed" if task['completed'] else "Pending"
        print(f"{i}. {task['name']} at {task['time'].strftime('%Y-%m-%d %I:%M %p')} - {status}")

def mark_completed():
    show_tasks()
    task_name = input("Enter task name to mark as completed: ").strip()
    for task in tasks:
        if task['name'].lower() == task_name.lower():
            if task['completed']:
                print(f"⚠️ Task '{task['name']}' is already marked completed.")
            else:
                task['completed'] = True
                stop_alert(task['name'])
                print(f"✅ Task '{task['name']}' marked as completed and alerts stopped.")
            return
    print("❌ Task not found!")

def task_checker():
    """Periodically check tasks and start alerts for pending tasks whose time has arrived."""
    while True:
        now = datetime.now()
        for task in tasks:
            if not task['completed'] and now >= task['time'] and task['name'] not in running_alerts:
                start_alert(task['name'])
        time.sleep(5)

def main():
    threading.Thread(target=task_checker, daemon=True).start()
    print("🚀 Task Notifier running...")

    while True:
        print("\nOptions:\n1. Add Task\n2. Show Tasks\n3. Mark Task Completed\n4. Stop Alerts\n5. Start Alerts Manually\n6. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            task_name = input("Enter task name to stop alerts: ").strip()
            stop_alert(task_name)
        elif choice == "5":
            task_name = input("Enter task name to start alerts manually: ").strip()
            start_alert(task_name)
        elif choice == "6":
            print("👋 Exiting... Stopping all alerts.")
            for flag in running_alerts.values():
                flag['stop'] = True
            time.sleep(1)  # Allow threads to exit
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
