
import sys
from typing import List, Dict, Optional

class TaskError(Exception):
    """Custom exception class for task-related errors."""
    pass

class Task:
    """
    Represents a single task with all its attributes.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.task_name = name
        self.task_description = description
        self.is_finished = False

    def to_dict(self) -> dict:
        """
        Converts the Task instance to a dictionary.
        """
        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_description": self.task_description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages tasks using in-memory data structure.

    Methods adhere to the specified interface for interacting with tasks.
    """
    def __init__(self):
        # Internal storage: {id: Task}
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task.

        :param task_name: Name of the task (non-empty)
        :param task_description: Description of the task (non-empty)
        :return: The unique ID of the created task
        :raises ValueError: If task_name or task_description is empty
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        :param task_id: Positive integer ID of the task
        :return: True if removal is successful; False otherwise
        :raises ValueError: For invalid task_id
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search tasks by a term (case-insensitive substring match in name or description).

        :param task_term: Term to search for in the tasks
        :return: List of task dictionaries that match
        :raises ValueError: If search term is empty
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.task_name.lower() or term in task.task_description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        :param task_id: Positive integer ID of the task
        :return: True if marking as finished is successful; False otherwise
        :raises ValueError: For invalid task_id
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task is None:
            return False
        if task.is_finished:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Get all tasks with their details.

        :return: List of all task dictionaries
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.

        :return: True if tasks were cleared, False if already empty
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


if __name__ == "__main__":
    # Example interactive console test
    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("[No tasks]")
            return
        for task in tasks:
            status = "✔" if task["is_finished"] else "✗"
            print(
                f"[{task['id']}] {task['task_name']} - {task['task_description']} (Finished: {status})"
            )

    manager = TaskManager()
    help_text = """
    Todo List Commands:
     add <name>|<description>     Add a task
     remove <id>                  Remove a task by id
     finish <id>                  Mark a task as finished
     search <term>                Search tasks by term
     list                         List all tasks
     clear                        Clear all tasks
     help                         Show this message
     exit                         Exit
    """

    print("Welcome to Todo List App")
    print(help_text)
    while True:
        try:
            cmd = input(">> ").strip()
            if not cmd:
                continue
            if cmd == "help":
                print(help_text)
            elif cmd.startswith("add "):
                try:
                    rest = cmd[4:]
                    if "|" not in rest:
                        print("Usage: add <name>|<description>")
                        continue
                    name, description = rest.split("|", 1)
                    task_id = manager.add(name, description)
                    print(f"Added task ID: {task_id}")
                except Exception as e:
                    print(f"Error: {e}")
            elif cmd.startswith("remove "):
                try:
                    task_id = int(cmd.split(" ", 1)[1])
                    success = manager.remove(task_id)
                    print("Task removed." if success else "Task not found.")
                except Exception as e:
                    print(f"Error: {e}")
            elif cmd.startswith("finish "):
                try:
                    task_id = int(cmd.split(" ", 1)[1])
                    success = manager.finish(task_id)
                    if success:
                        print("Task marked as finished.")
                    else:
                        print("Task not found or already finished.")
                except Exception as e:
                    print(f"Error: {e}")
            elif cmd.startswith("search "):
                try:
                    term = cmd.split(" ", 1)[1]
                    results = manager.search(term)
                    print_tasks(results)
                except Exception as e:
                    print(f"Error: {e}")
            elif cmd == "list":
                print_tasks(manager.get_all())
            elif cmd == "clear":
                cleared = manager.clear_all()
                print("All tasks cleared." if cleared else "Task list already empty.")
            elif cmd == "exit":
                print("Goodbye!")
                break
            else:
                print("Unknown command. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
