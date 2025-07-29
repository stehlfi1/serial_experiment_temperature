
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
        Returns a dictionary representation of the task.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages a collection of Tasks with operations to add, remove, search,
    finish, list, and clear tasks.

    All mutations and lookups are efficient (dict-based storage).
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task. Returns the unique ID of the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Returns:
            bool: True if removal was successful, False if task_id does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description containing the search term (case-insensitive).

        Returns:
            List of dicts representing matching tasks.

        Raises:
            ValueError: If search term is empty.
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string.")
        term = task_term.strip().lower()
        if not term:
            raise ValueError("Search term cannot be empty.")
        matches = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Returns:
            bool: True if the task was marked as finished, False if task_id does not exist.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks as a list of dictionaries.

        Returns:
            List of dicts representing all tasks.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks.

        Returns:
            bool: True if tasks were cleared (i.e., at least one task existed), False otherwise.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


def print_tasks(tasks: List[Dict]):
    """
    Prints tasks in a readable format.
    """
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✔" if task["is_finished"] else "✗"
        print(f"[{status}] ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']}")


def main():
    """
    Console-based interface for TaskManager.
    """
    manager = TaskManager()
    menu = (
        "\nTodo List App\n"
        "--------------\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Show All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
    )
    while True:
        print(menu)
        choice = input("Enter your choice (1-7): ").strip()
        try:
            if choice == "1":
                name = input("Task name: ").strip()
                desc = input("Task description: ").strip()
                task_id = manager.add(name, desc)
                print(f"Task added with ID {task_id}.")
            elif choice == "2":
                task_id = int(input("Enter Task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == "3":
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                print_tasks(results)
            elif choice == "4":
                task_id = int(input("Enter Task ID to mark as finished: "))
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
                print("Exiting Todo List App.")
                break
            else:
                print("Invalid choice. Please select an option from 1 to 7.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting Todo List App.")
            break

if __name__ == "__main__":
    main()
