
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

    def to_dict(self) -> dict:
        """
        Converts the Task object to a dictionary.
        Returns:
            dict: Task information.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages a collection of todo tasks in memory.
    Provides methods to add, remove, search, finish, get all, and clear tasks.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.
        Args:
            task_name (str): Name of the task (must not be empty).
            task_description (str): Description of the task (must not be empty).
        Returns:
            int: Unique ID of the created task.
        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.
        Args:
            task_id (int): Task ID to remove.
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

    def search(self, task_term: str) -> List[dict]:
        """
        Searches tasks by name or description.
        Args:
            task_term (str): Search term (must not be empty).
        Returns:
            list[dict]: List of matching tasks.
        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
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
        Args:
            task_id (int): Task ID to finish.
        Returns:
            bool: True if successfully marked as finished, False if task not found.
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

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks.
        Returns:
            list[dict]: List of all tasks with their details.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        Returns:
            bool: True if tasks cleared successfully.
        """
        self._tasks.clear()
        return True


def main():
    """
    Simple console interface for the TaskManager.
    """
    manager = TaskManager()

    MENU = """
    Todo List Manager
    ----------------
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Finish Task
    5. Get All Tasks
    6. Clear All Tasks
    7. Exit
    """

    while True:
        print(MENU)
        choice = input("Select an option (1-7): ").strip()
        try:
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task added with ID {task_id}\n")
            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed successfully.\n")
                else:
                    print("Task not found.\n")
            elif choice == "3":
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    print("Search results:")
                    for task in results:
                        print(task)
                else:
                    print("No matching tasks found.")
                print()
            elif choice == "4":
                task_id = int(input("Enter task ID to finish: "))
                if manager.finish(task_id):
                    print("Task marked as finished.\n")
                else:
                    print("Task not found.\n")
            elif choice == "5":
                tasks = manager.get_all()
                if not tasks:
                    print("No tasks available.\n")
                else:
                    for task in tasks:
                        print(task)
                    print()
            elif choice == "6":
                confirm = input("Are you sure you want to clear all tasks? (y/n): ")
                if confirm.lower() == "y":
                    manager.clear_all()
                    print("All tasks cleared.\n")
            elif choice == "7":
                print("Exiting Todo List Manager.")
                break
            else:
                print("Invalid option. Please select a number between 1 and 7.\n")
        except ValueError as ve:
            print(f"Input Error: {ve}\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}\n")


if __name__ == "__main__":
    main()
