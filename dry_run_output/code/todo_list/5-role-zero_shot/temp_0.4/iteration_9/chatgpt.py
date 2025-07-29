
import sys
from typing import List, Dict, Optional


class Task:
    """
    Represents a single todo task.
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


class TaskManager:
    """
    TaskManager manages a collection of todo tasks.
    Provides methods to add, remove, search, finish, get all, and clear all tasks.
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task list.

        Args:
            task_name (str): Name of the task (non-empty).
            task_description (str): Description of the task (non-empty).

        Returns:
            int: Unique ID of the added task.

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
            bool: True if task was removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The search term.

        Returns:
            list[dict]: List of matching tasks.

        Raises:
            ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The unique ID of the task.

        Returns:
            bool: True if task was marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is not None:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: List of all tasks with their details.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks.

        Returns:
            bool: True if tasks were cleared, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


def main():
    """
    Console-based interface for the TaskManager.
    """
    manager = TaskManager()

    MENU = """
    Todo List App
    -------------
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Finish Task
    5. List All Tasks
    6. Clear All Tasks
    7. Exit
    """

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
            return
        print(f"{'ID':<5} {'Name':<20} {'Description':<40} {'Finished':<10}")
        print("-" * 80)
        for t in tasks:
            print(f"{t['id']:<5} {t['task_name']:<20} {t['task_description']:<40} {str(t['is_finished']):<10}")

    while True:
        print(MENU)
        choice = input("Enter choice (1-7): ").strip()
        try:
            if choice == "1":
                name = input("Task name: ").strip()
                desc = input("Task description: ").strip()
                task_id = manager.add(name, desc)
                print(f"Task added with ID {task_id}.")
            elif choice == "2":
                task_id = int(input("Enter task ID to remove: ").strip())
                if manager.remove(task_id):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == "3":
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                print_tasks(results)
            elif choice == "4":
                task_id = int(input("Enter task ID to finish: ").strip())
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif choice == "5":
                tasks = manager.get_all()
                print_tasks(tasks)
            elif choice == "6":
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")
            elif choice == "7":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
