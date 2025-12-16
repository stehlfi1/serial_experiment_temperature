
import sys
from typing import List, Dict

class TaskValidationError(ValueError):
    """Exception raised for invalid task input."""
    pass

class TaskNotFoundError(KeyError):
    """Exception raised when a task is not found by its ID."""
    pass

class Task:
    """
    Represents a single todo task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Task title.
        description (str): Task description.
        is_finished (bool): Task completion status.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Returns a dictionary representation of the task."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages todo tasks in-memory, supporting add, remove, finish, search, retrieval, and clear operations.

    Adheres to ISO/IEC 25010 requirements for maintainability, correctness, safety, modularity, and testability.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        Args:
            task_name (str): Task title (must be non-empty).
            task_description (str): Task description (must be non-empty).

        Returns:
            int: Unique task ID.

        Raises:
            ValueError: If inputs are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The task's unique identifier.

        Returns:
            bool: True if removed, False if not found or invalid input.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description (case-insensitive, substring).

        Args:
            task_term (str): Search term.

        Returns:
            List[dict]: Matched tasks or empty list.

        Raises:
            ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term cannot be empty.")
        term = task_term.strip().lower()
        matches = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The task's unique identifier.

        Returns:
            bool: True if marked as finished; False if not found.

        Raises:
            ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            List[dict]: All tasks, including their ID, name, description, and status.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if cleared, False otherwise.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


if __name__ == '__main__':
    # Sample CLI for demonstration and testing
    manager = TaskManager()

    menu = """
--- Todo List Menu ---
1. Add Task
2. Remove Task
3. Finish Task
4. Search Tasks
5. Show All Tasks
6. Clear All Tasks
7. Exit
Enter option (1-7): """

    def print_tasks(tasks):
        if not tasks:
            print("No tasks found.")
            return
        print("Tasks:")
        for t in tasks:
            finished = "✓" if t['is_finished'] else " "
            print(f"[{finished}] (ID: {t['id']}) {t['task_name']}: {t['task_description']}")

    while True:
        try:
            choice = input(menu).strip()
            if choice == '1':
                name = input("Task name: ")
                desc = input("Task description: ")
                task_id = manager.add(name, desc)
                print(f"Task added. ID: {task_id}")
            elif choice == '2':
                tid = int(input("Task ID to remove: "))
                if manager.remove(tid):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == '3':
                tid = int(input("Task ID to finish: "))
                if manager.finish(tid):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif choice == '4':
                term = input("Enter search term: ")
                results = manager.search(term)
                print_tasks(results)
            elif choice == '5':
                tasks = manager.get_all()
                print_tasks(tasks)
            elif choice == '6':
                confirmed = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirmed.lower() == 'y':
                    manager.clear_all()
                    print("All tasks cleared.")
            elif choice == '7':
                print("Goodbye.")
                break
            else:
                print("Invalid option. Please enter a number (1-7).")
        except TaskValidationError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
