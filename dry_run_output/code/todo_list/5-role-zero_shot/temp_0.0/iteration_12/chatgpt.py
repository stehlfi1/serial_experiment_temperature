
"""
todo_app.py - Console-based Todo List Application

Implements a high-quality, maintainable Todo List manager adhering to ISO/IEC 25010 standards.
Follows an OOP design using the TaskManager class, providing interface functions for manageability,
efficiency, and safety. All validation and data access mechanisms are strictly enforced for robustness.
"""

from typing import List, Dict
import threading

class TaskManager:
    """
    Manages a collection of todo tasks in memory.
    Provides methods for adding, removing, searching, finishing, retrieving, and clearing tasks,
    with robust error handling and validation as per best practices.
    """

    class _Task:
        """
        Internal representation of a task.
        """
        def __init__(self, task_id: int, name: str, description: str):
            self.id = task_id
            self.name = name
            self.description = description
            self.is_finished = False

        def to_dict(self) -> Dict:
            """
            Returns the task as a dictionary.
            """
            return {
                "id": self.id,
                "task_name": self.name,
                "task_description": self.description,
                "is_finished": self.is_finished
            }

    def __init__(self) -> None:
        """
        Initializes the task manager with an empty task store.
        """
        self._tasks = {}  # {id: _Task}
        self._next_id = 1
        self._lock = threading.Lock()  # Thread-safety if required for future needs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task and returns its unique ID.
        Raises:
            ValueError: if task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        with self._lock:
            task_id = self._next_id
            self._tasks[task_id] = self._Task(task_id, task_name.strip(), task_description.strip())
            self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by ID.
        Returns True if successful, False if not found.
        Raises:
            ValueError: if task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by task name or description (case-insensitive).
        Returns a list of matched tasks' dictionaries.
        Raises:
            ValueError: if task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        task_term_lower = task_term.strip().lower()
        with self._lock:
            matches = [
                t.to_dict()
                for t in self._tasks.values()
                if task_term_lower in t.name.lower() or task_term_lower in t.description.lower()
            ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.
        Returns True if successful, False if not found.
        Raises:
            ValueError: if task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            task.is_finished = True
            return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks as a list of dictionaries.
        """
        with self._lock:
            return [t.to_dict() for t in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        Returns True if tasks were deleted.
        """
        with self._lock:
            had_tasks = bool(self._tasks)
            self._tasks.clear()
        return had_tasks

# Example usage & CLI demonstration:
if __name__ == "__main__":
    manager = TaskManager()
    print("Todo List App (Type 'help' for available commands)")

    def print_tasks(tasks):
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                print(f"[{'X' if t['is_finished'] else ' '}] (ID: {t['id']}) {t['task_name']}: {t['task_description']}")

    commands = """
add <name> <description>       : Add a new task
remove <id>                    : Remove task by ID
finish <id>                    : Mark task as finished
search <term>                  : Search tasks
list                           : List all tasks
clear                          : Clear all tasks
exit                           : Exit the application
help                           : Show this help message
"""

    while True:
        try:
            inp = input(">> ").strip()
            if not inp:
                continue
            parts = inp.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd == "add" and len(parts) == 3:
                task_id = manager.add(parts[1], parts[2])
                print(f"Added task with ID {task_id}.")

            elif cmd == "remove" and len(parts) == 2:
                success = manager.remove(int(parts[1]))
                print("Task removed." if success else "Task not found.")

            elif cmd == "finish" and len(parts) == 2:
                success = manager.finish(int(parts[1]))
                print("Task marked as finished." if success else "Task not found.")

            elif cmd == "search" and len(parts) == 2:
                results = manager.search(parts[1])
                print_tasks(results)

            elif cmd == "list":
                print_tasks(manager.get_all())

            elif cmd == "clear":
                success = manager.clear_all()
                print("All tasks cleared." if success else "No tasks to clear.")

            elif cmd == "help":
                print(commands)

            elif cmd == "exit":
                print("Goodbye!")
                break

            else:
                print("Invalid command. Type 'help' for available commands.")

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")
