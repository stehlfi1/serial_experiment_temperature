
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
    Manages a collection of todo tasks with operations to add, remove, search,
    finish, retrieve, and clear tasks.
    """

    def __init__(self):
        # Store tasks in a dict for O(1) access by id
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1  # Auto-incrementing task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.
        Returns the unique ID of the created task.

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
        Removes the task with the specified ID.
        Returns True if the task was removed, False if not found.

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
        Searches for tasks containing the term in their name or description (case-insensitive).
        Returns a list of matching task dictionaries.

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
        Marks the task with the specified ID as finished.
        Returns True if successful, False if task not found.

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
        Retrieves all tasks as a list of dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        Returns True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False


def print_menu():
    """
    Prints the main menu options.
    """
    print("\nTodo List Manager")
    print("-----------------")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Search Tasks")
    print("4. Finish Task")
    print("5. Show All Tasks")
    print("6. Clear All Tasks")
    print("0. Exit")


def print_tasks(tasks: List[Dict]):
    """
    Prints a list of tasks in a user-friendly format.
    """
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✔" if task["is_finished"] else "✗"
        print(f"ID: {task['id']} | Name: {task['task_name']} | "
              f"Description: {task['task_description']} | Finished: {status}")


def main():
    """
    Console-based UI for interacting with TaskManager.
    """
    manager = TaskManager()
    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        try:
            if choice == "1":
                name = input("Enter task name: ").strip()
                desc = input("Enter task description: ").strip()
                task_id = manager.add(name, desc)
                print(f"Task added with ID: {task_id}")
            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            elif choice == "3":
                term = input("Enter search term: ").strip()
                results = manager.search(term)
                print_tasks(results)
            elif choice == "4":
                task_id = int(input("Enter task ID to finish: "))
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
            elif choice == "0":
                print("Exiting Todo List Manager.")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
