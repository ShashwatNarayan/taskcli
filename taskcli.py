import argparse
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def generate_task_id(tasks):
    return max([t['id'] for t in tasks], default=0) + 1

def add_task(title, due, priority):
    tasks = load_tasks()
    new_task = {
        'id': generate_task_id(tasks),
        'title': title,
        'due_date': due,
        'priority': priority,
        'completed': False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(Fore.GREEN + f"Task '{title}' added successfully.")

def list_tasks(show_all=False):
    tasks = load_tasks()
    if not tasks:
        print(Fore.CYAN + "No tasks found.")
        return

    for task in tasks:
        if not show_all and task['completed']:
            continue

        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
        days_left = (due_date - datetime.today()).days

        color = (
            Fore.RED if task['priority'] == 'high'
            else Fore.YELLOW if task['priority'] == 'medium'
            else Fore.GREEN
        )

        status = '✅' if task['completed'] else '❌'
        due_text = f"{task['due_date']} ({days_left} days left)"
        print(f"[{task['id']}] {status} {color}{task['title']} - {task['priority'].capitalize()} priority - Due: {due_text}")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) == len(new_tasks):
        print(Fore.RED + f"No task found with ID {task_id}.")
    else:
        save_tasks(new_tasks)
        print(Fore.YELLOW + f"Task {task_id} deleted.")

def complete_task(task_id):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = True
            found = True
            break
    if found:
        save_tasks(tasks)
        print(Fore.GREEN + f"Task {task_id} marked as completed.")
    else:
        print(Fore.RED + f"No task found with ID {task_id}.")

def clear_completed():
    tasks = load_tasks()
    new_tasks = [t for t in tasks if not t['completed']]
    removed = len(tasks) - len(new_tasks)
    save_tasks(new_tasks)
    print(Fore.MAGENTA + f"Cleared {removed} completed task(s).")

def main():
    parser = argparse.ArgumentParser(description='TaskCLI – Command-line Task Manager')
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    add = subparsers.add_parser('add', help='Add a new task')
    add.add_argument('title', help='Task title')
    add.add_argument('--due', required=True, help='Due date (YYYY-MM-DD)')
    add.add_argument('--priority', choices=['low', 'medium', 'high'], default='low')

    # List command
    list_cmd = subparsers.add_parser('list', help='List all tasks')
    list_cmd.add_argument('--all', action='store_true', help='Include completed tasks')

    # Delete command
    delete = subparsers.add_parser('delete', help='Delete a task by ID')
    delete.add_argument('id', type=int)

    # Complete command
    complete = subparsers.add_parser('complete', help='Mark a task as complete')
    complete.add_argument('id', type=int)

    # Clear completed
    clear = subparsers.add_parser('clear', help='Remove all completed tasks')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.title, args.due, args.priority)
    elif args.command == 'list':
        list_tasks(args.all)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'complete':
        complete_task(args.id)
    elif args.command == 'clear':
        clear_completed()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()