
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception class for task input validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception class for handling missing task IDs."""
    pass


class Task:
    """
    Represents a single todo task.
    Attributes:
        id (int): Unique identifier of the task.
        name (str): Name/title of the task.
        description (str): Detailed description of the task.
        is_finished (bool): Completion status of the task.
    """
    def __init__(self, task_id: int, name: str, description: str) -> None:
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Returns a dictionary representation of the task."""
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished,
        }


class TaskManager:
    """
    Manages a collection of tasks, supporting add, remove, search, finish, retrieval,
    and clearing of all tasks. All operations are performed in-memory for performance and reliability.
    """

    def __init__(self) -> None:
        # Dictionary for efficient O(1) lookup, insertion, and deletion by task ID.
        self._tasks: Dict[int, Task] = {}
        # Internal counter for unique task IDs.
        self._next_id: int = 1

    def _validate_task_name_description(self, name: str, description: str) -> None:
        """Validate input for name and description."""
        if not isinstance(name, str) or not name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")
        if not isinstance(description, str) or not description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

    def _validate_task_id(self, task_id: int) -> None:
        """Check if a task ID is valid and exists."""
        if not isinstance(task_id, int) or task_id < 0:
            raise TaskValidationError("Task ID must be a non-negative integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} does not exist.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task. Returns the unique task ID.
        Raises:
            TaskValidationError: On invalid inputs.
        """
        self._validate_task_name_description(task_name, task_description)
        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by ID.
        Returns True on success.
        Handles non-existent task gracefully.
        """
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            return True
        except (TaskValidationError, TaskNotFoundError):
            return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by case-insensitive substring match in name or description.
        Returns a list of matching task dictionaries.
        Empty string returns empty list.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            # Returning empty list for empty term as reasonable fallback
            return []
        term = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.
        Returns True if successful.
        Handles non-existent task gracefully.
        """
        try:
            self._validate_task_id(task_id)
            task = self._tasks[task_id]
            task.is_finished = True
            return True
        except (TaskValidationError, TaskNotFoundError):
            return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks sorted by their IDs.
        """
        return [
            self._tasks[task_id].to_dict() for task_id in sorted(self._tasks)
        ]

    def clear_all(self) -> bool:
        """
        Removes all tasks.
        Returns True on success.
        """
        self._tasks.clear()
        return True


def _main():
    """
    Simple interactive console interface for TaskManager.
    Demonstrates usage and testability.
    """
    manager = TaskManager()
    print("Simple Todo List App (type 'help' for instructions, 'exit' to quit)\n")
    commands = {
        "add": "Add a task: add <name>;<description>",
        "remove": "Remove task by id: remove <id>",
        "search": "Search tasks: search <term>",
        "finish": "Mark task as finished: finish <id>",
        "get_all": "List all tasks: get_all",
        "clear_all": "Delete all tasks: clear_all",
        "exit": "Exit program",
        "help": "Show this help"
    }

    def print_tasks(tasks):
        if not tasks:
            print("(no tasks)")
        else:
            for t in tasks:
                finished = "✓" if t["is_finished"] else " "
                print(f"ID: {t['id']} | [{finished}] {t['task_name']}: {t['task_description']}")

    while True:
        try:
            command = input(">> ").strip()
            if not command:
                continue
            if command == "exit":
                break
            if command == "help":
                for k, v in commands.items():
                    print(f"{k}: {v}")
                continue
            if command.startswith("add "):
                try:
                    args = command[4:].split(";", 1)
                    if len(args) != 2:
                        print("Invalid format. Usage: add <name>;<description>")
                        continue
                    task_id = manager.add(args[0], args[1])
                    print(f"Task added with ID {task_id}.")
                except TaskValidationError as e:
                    print(f"Add failed:", e)
            elif command.startswith("remove "):
                try:
                    task_id = int(command[7:].strip())
                except ValueError:
                    print("Invalid ID format.")
                    continue
                if manager.remove(task_id):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif command.startswith("search "):
                term = command[7:].strip()
                results = manager.search(term)
                print_tasks(results)
            elif command.startswith("finish "):
                try:
                    task_id = int(command[7:].strip())
                except ValueError:
                    print("Invalid ID format.")
                    continue
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif command == "get_all":
                tasks = manager.get_all()
                print_tasks(tasks)
            elif command == "clear_all":
                manager.clear_all()
                print("All tasks cleared.")
            else:
                print("Unknown command. Type 'help' for options.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

if __name__ == "__main__":
    _main()
