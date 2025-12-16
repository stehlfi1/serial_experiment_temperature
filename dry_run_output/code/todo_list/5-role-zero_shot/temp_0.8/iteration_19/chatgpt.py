
import sys
from typing import List, Dict, Optional

class TaskValidationError(ValueError):
    """Exception raised for invalid task parameters."""
    pass

class TaskNotFoundError(KeyError):
    """Exception raised for operations on non-existent tasks."""
    pass

class Task:
    """
    Represents a single task.
    """
    def __init__(self, task_id: int, task_name: str, task_description: str):
        self.id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Returns dictionary representation of the task."""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Task management system that supports basic CRUD operations on tasks.
    """

    def __init__(self):
        # Store tasks by their id for O(1) lookup, insert, and delete.
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the manager.
        Args:
            task_name (str): Name/title of the task; must be non-empty.
            task_description (str): Description of the task; must be non-empty.
        Returns:
            int: The unique ID assigned to the new task.
        Raises:
            TaskValidationError: If input is invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        Args:
            task_id (int): The id of the task to remove.
        Returns:
            bool: True if removed, False otherwise.
        Raises:
            TaskValidationError: If task_id is invalid.
        """
        self._validate_task_id(task_id)
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks containing the term in name or description.
        Args:
            task_term (str): The string term to search for.
        Returns:
            List[Dict]: List of matching tasks.
        Raises:
            TaskValidationError: If task_term is invalid.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")

        term_lower = task_term.lower()
        result = [
            task.to_dict()
            for task in self._tasks.values()
            if term_lower in task.task_name.lower()
            or term_lower in task.task_description.lower()
        ]
        return result

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        Args:
            task_id (int): The id of the task to mark as completed.
        Returns:
            bool: True if successful, False otherwise.
        Raises:
            TaskValidationError: If task_id is invalid.
        """
        self._validate_task_id(task_id)
        task = self._tasks.get(task_id)
        if task is None:
            return False
        if not task.is_finished:
            task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        Returns:
            List[Dict]: All task representations.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.
        Returns:
            bool: True if the tasks were cleared, False if already empty.
        """
        had_tasks = bool(self._tasks)
        self._tasks.clear()
        return had_tasks

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validates that a task_id is a positive integer.
        Args:
            task_id (int): The id to validate.
        Raises:
            TaskValidationError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")

    # Optionally, you can add more helper methods for maintainability.

# Example usage & simple interactive console demo (comment out if used with unit tests)
if __name__ == "__main__":
    manager = TaskManager()
    print("Welcome to the Console-based ToDo List App.")
    print("Type 'help' to see available commands.\n")

    commands = {
        'add': "Add a new task: add <name> | <description>",
        'remove': "Remove a task by ID: remove <id>",
        'finish': "Mark a task as finished: finish <id>",
        'search': "Search tasks: search <term>",
        'get_all': "Retrieve all tasks: get_all",
        'clear_all': "Delete all tasks: clear_all",
        'exit': "Exit the application: exit",
        'help': "Show this help message.",
    }

    def display_help():
        print("Available commands:")
        for cmd, desc in commands.items():
            print(f"  {desc}")

    while True:
        try:
            command = input("> ").strip()
            if not command:
                continue
            if command == "exit":
                print("Goodbye!")
                break
            if command == "help":
                display_help()
                continue
            if command.startswith("add "):
                if "|" not in command:
                    print("Format: add <name> | <description>")
                    continue
                name_desc = command[4:].split("|", 1)
                if len(name_desc) < 2:
                    print("Format: add <name> | <description>")
                    continue
                name, desc = name_desc[0].strip(), name_desc[1].strip()
                try:
                    task_id = manager.add(name, desc)
                    print(f"Task added with ID: {task_id}")
                except TaskValidationError as ve:
                    print(f"Error: {ve}")
                continue
            elif command.startswith("remove "):
                try:
                    task_id = int(command.split(" ", 1)[1])
                    if manager.remove(task_id):
                        print("Task removed.")
                    else:
                        print("Task not found.")
                except (ValueError, TaskValidationError) as e:
                    print("Invalid task ID.")
                continue
            elif command.startswith("finish "):
                try:
                    task_id = int(command.split(" ", 1)[1])
                    if manager.finish(task_id):
                        print("Task marked as finished.")
                    else:
                        print("Task not found.")
                except (ValueError, TaskValidationError):
                    print("Invalid task ID.")
                continue
            elif command.startswith("search "):
                term = command[7:].strip()
                try:
                    results = manager.search(term)
                    if results:
                        for t in results:
                            print(t)
                    else:
                        print("No tasks found with the given term.")
                except TaskValidationError as ve:
                    print(f"Error: {ve}")
                continue
            elif command == "get_all":
                tasks = manager.get_all()
                if tasks:
                    for t in tasks:
                        print(t)
                else:
                    print("No tasks to show.")
                continue
            elif command == "clear_all":
                cleared = manager.clear_all()
                print("All tasks cleared." if cleared else "Task list is already empty.")
                continue
            else:
                print("Unknown command. Type 'help' for instructions.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

