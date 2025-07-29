
import sys
from typing import List, Dict, Optional

class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass

class TaskNotFoundError(KeyError):
    """Custom exception for non-existent task IDs."""
    pass

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
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Manages a collection of tasks with add, remove, search, finish, get_all, and clear_all operations.
    Adheres to ISO/IEC 25010 quality requirements.
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task (non-empty).
            task_description (str): The description of the task (non-empty).

        Returns:
            int: The unique ID of the newly added task.

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
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed, False if not found.

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
        Searches for tasks by name or description (case-insensitive substring match).

        Args:
            task_term (str): The search term.

        Returns:
            list[dict]: List of matching tasks.

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
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was marked as finished, False if not found.

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
            list[dict]: List of all tasks with their details.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False

def main():
    """
    Console-based interface for the TaskManager.
    """
    manager = TaskManager()

    menu = (
        "\nTodo List Menu:\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. List All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
    )

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            status = "Finished" if task['is_finished'] else "Pending"
            print(f"ID: {task['id']} | Name: {task['task_name']} | "
                  f"Description: {task['task_description']} | Status: {status}")

    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()
        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Task added with ID: {task_id}")
            elif choice == '2':
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            elif choice == '3':
                term = input("Enter search term: ")
                results = manager.search(term)
                print_tasks(results)
            elif choice == '4':
                task_id = int(input("Enter task ID to finish: "))
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif choice == '5':
                tasks = manager.get_all()
                print_tasks(tasks)
            elif choice == '6':
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")
            elif choice == '7':
                print("Exiting Todo List. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
