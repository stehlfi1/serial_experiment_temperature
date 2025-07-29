
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for not found task operations."""
    pass


class Task:
    """
    Represents a single todo task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Name of the task.
        description (str): Description of the task.
        is_finished (bool): Completion status of the task.
    """
    __slots__ = ['id', 'name', 'description', 'is_finished']

    def __init__(self, task_id: int, name: str, description: str) -> None:
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Converts the Task object to a dictionary."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages todo tasks in-memory.

    Methods:
        add(task_name: str, task_description: str) -> int
        remove(task_id: int) -> bool
        search(task_term: str) -> list[dict]
        finish(task_id: int) -> bool
        get_all() -> list[dict]
        clear_all() -> bool
    """
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        Args:
            task_name (str): Name of the task.
            task_description (str): Description of the task.

        Returns:
            int: The unique ID of the added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")
        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if removed, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description (case-insensitive).

        Args:
            task_term (str): Text to search for.

        Returns:
            List[Dict]: List of matching tasks as dictionaries.

        Raises:
            ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")
        term = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The unique ID of the task to finish.

        Returns:
            bool: True if marked as finished, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            List[Dict]: List of all tasks as dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks.

        Returns:
            bool: True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False


def main():
    """
    Example interactive console for TaskManager.
    """
    import textwrap

    manager = TaskManager()

    menu = textwrap.dedent("""
    ==== TODO LIST MENU ====
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Mark Task as Finished
    5. View All Tasks
    6. Clear All Tasks
    7. Exit
    """)

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(f"ID: {task['id']}, Name: {task['task_name']}, "
                      f"Description: {task['task_description']}, "
                      f"Finished: {'Yes' if task['is_finished'] else 'No'}")

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()
        try:
            if choice == '1':
                name = input("Task Name: ").strip()
                desc = input("Task Description: ").strip()
                task_id = manager.add(name, desc)
                print(f"Task added with ID {task_id}.")
            elif choice == '2':
                tid = int(input("Enter Task ID to remove: ").strip())
                if manager.remove(tid):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == '3':
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                print_tasks(results)
            elif choice == '4':
                tid = int(input("Enter Task ID to finish: ").strip())
                if manager.finish(tid):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif choice == '5':
                print_tasks(manager.get_all())
            elif choice == '6':
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")
            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select from 1 to 7.")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
