import os
import time
from datetime import datetime, timedelta

# =========================
# TO DO LIST DAILY LIFE APP
# =========================

# Folder and file setup
folder_name = "MyTasks"
file_name = "tasks.txt"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

file_path = os.path.join(folder_name, file_name)

tasks = []


# =========================
# LOAD TASKS FROM FILE
# =========================

def load_tasks():
    global tasks

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()

                if line:
                    parts = line.split("|")

                    if len(parts) == 4:
                        task_data = {
                            "task": parts[0].strip(),
                            "deadline": parts[1].strip(),
                            "priority": parts[2].strip().capitalize(),
                            "completed": parts[3].strip().capitalize()
                        }

                        tasks.append(task_data)


# =========================
# SAVE TASKS TO FILE
# =========================

def save_tasks():
    with open(file_path, "w") as file:
        for task in tasks:
            line = f"{task['task']}|{task['deadline']}|{task['priority']}|{task['completed']}\n"
            file.write(line)


# =========================
# ADD TASK
# =========================

# =========================
# EASY DATE INPUT FUNCTION
# =========================

def get_easy_deadline():

    print("\nExamples:")
    print("today 18:00")
    print("tomorrow 09:30")
    print("2026-05-20 18:00")

    user_input = input("Enter deadline: ").lower()

    now = datetime.now()

    try:

        # TODAY
        if "today" in user_input:

            time_part = user_input.replace("today", "").strip()

            hour, minute = map(int, time_part.split(":"))

            final_date = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            return final_date.strftime("%Y-%m-%d %H:%M")

        # TOMORROW
        elif "tomorrow" in user_input:

            time_part = user_input.replace("tomorrow", "").strip()

            hour, minute = map(int, time_part.split(":"))

            tomorrow = now + timedelta(days=1)

            final_date = tomorrow.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            return final_date.strftime("%Y-%m-%d %H:%M")

        # FULL DATE
        else:

            datetime.strptime(user_input, "%Y-%m-%d %H:%M")

            return user_input

    except:

        print("Invalid format. Try again.")
        return get_easy_deadline()

def add_task():
    print("\n------ ADD TASK ------")

    task_name = input("Enter task name: ")

    deadline = get_easy_deadline()

    print("\nPriority Levels")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    priority_choice = input("Choose priority: ")

    if priority_choice == "1":
        priority = "High"

    elif priority_choice == "2":
        priority = "Medium"

    else:
        priority = "Low"

    task_data = {
        "task": task_name,
        "deadline": deadline,
        "priority": priority,
        "completed": "No"
    }

    tasks.append(task_data)

    save_tasks()

    print("Task added successfully!")


# =========================
# VIEW TASKS
# =========================

def get_sorted_task_indices(include_completed=True):
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    indices = (
        range(len(tasks))
        if include_completed
        else [i for i, task in enumerate(tasks) if task["completed"] == "No"]
    )

    return sorted(
        indices,
        key=lambda i: priority_order.get(tasks[i]["priority"].strip().lower(), 4)
    )


def view_tasks():
    print("\n------ YOUR TASKS ------")

    sorted_indices = get_sorted_task_indices(include_completed=False)

    if len(sorted_indices) == 0:
        print("No tasks available.")
        return

    for display_index, task_index in enumerate(sorted_indices):
        task = tasks[task_index]

        print(f"""
Task Number : {display_index + 1}
Task        : {task['task']}
Deadline    : {task['deadline']}
Priority    : {task['priority']}
Completed   : {task['completed']}
        """)

        # Reminder for High Priority Tasks
        if task["priority"] == "High":
            print("!!! IMPORTANT TASK - DON'T FORGET !!!")


# =========================
# REMOVE TASK
# =========================

def remove_task():
    view_tasks()

    sorted_indices = get_sorted_task_indices(include_completed=False)

    if len(sorted_indices) == 0:
        print("No active tasks to remove.")
        return

    try:
        task_number = int(input("Enter task number to remove: "))

        if 1 <= task_number <= len(sorted_indices):
            actual_index = sorted_indices[task_number - 1]

            removed_task = tasks.pop(actual_index)

            save_tasks()

            print(f"Removed Task: {removed_task['task']}")

        else:
            print("Invalid task number.")

    except:
        print("Please enter a valid number.")


# =========================
# EDIT TASK
# =========================

def edit_task():
    view_tasks()

    sorted_indices = get_sorted_task_indices(include_completed=False)

    if len(sorted_indices) == 0:
        print("No active tasks to edit.")
        return

    try:
        task_number = int(input("Enter task number to edit: "))

        if 1 <= task_number <= len(sorted_indices):
            actual_index = sorted_indices[task_number - 1]
            task = tasks[actual_index]

            print("\nLeave blank if you don't want to change something.")

            new_name = input("Enter new task name: ")
            new_deadline = input("Enter new deadline: ")
            new_priority = input("Enter new priority (High/Medium/Low): ")

            if new_name != "":
                task["task"] = new_name

            if new_deadline != "":
                task["deadline"] = new_deadline

            if new_priority != "":
                normalized_priority = new_priority.strip().capitalize()
                if normalized_priority in ["High", "Medium", "Low"]:
                    task["priority"] = normalized_priority
                else:
                    print("Invalid priority. Keeping previous value.")

            save_tasks()

            print("Task updated successfully!")

        else:
            print("Invalid task number.")

    except:
        print("Please enter a valid number.")


# =========================
# COMPLETE TASK
# =========================

def complete_task():
    view_tasks()

    sorted_indices = get_sorted_task_indices(include_completed=False)

    if len(sorted_indices) == 0:
        print("No active tasks to complete.")
        return

    try:
        task_number = int(input("Enter task number completed: "))

        if 1 <= task_number <= len(sorted_indices):
            actual_index = sorted_indices[task_number - 1]

            tasks[actual_index]["completed"] = "Yes"

            save_tasks()

            print("Task marked as completed!")

        else:
            print("Invalid task number.")

    except:
        print("Please enter a valid number.")


# =========================
# TIMER AND REMINDER
# =========================

def check_deadlines():
    current_time = datetime.now()

    for task in tasks:

        if task["completed"] == "No":

            try:
                task_deadline = datetime.strptime(
                    task["deadline"],
                    "%Y-%m-%d %H:%M"
                )

                remaining_time = task_deadline - current_time

                hours_left = remaining_time.total_seconds() / 3600

                # Reminder if deadline is close
                if 0 <= hours_left <= 24:

                    print("\n================================")
                    print("REMINDER !!!")
                    print(f"Task: {task['task']}")
                    print(f"Deadline: {task['deadline']}")
                    print("Complete it soon!")
                    print("================================\n")

            except:
                pass


# =========================
# MAIN PROGRAM
# =========================

load_tasks()

while True:

    check_deadlines()

    print("""
===============================
      TO DO LIST DAILY LIFE
===============================

1. Add Task
2. View Tasks
3. Remove Task
4. Edit Task
5. Complete Task
6. Exit

===============================
""")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        remove_task()

    elif choice == "4":
        edit_task()

    elif choice == "5":
        complete_task()

    elif choice == "6":
        print("Saving tasks...")
        save_tasks()
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")

    time.sleep(1)