
import sys
from typing import List, Dict


class TaskNotFoundError(Exception):
    """Custom exception raised when a specified task is not found."""
    pass


class InvalidTaskInputError(ValueError):
    """Custom exception raised when the input to a task function is invalid."""
    pass


class TaskManager:
    """
    A class for managing a todo list.
    
    Implements operations to add, remove, search, finish, list, and clear tasks.
    Tasks are stored in-memory and uniquely identified by integer IDs.
    """

    def __init__(self) -> None:
        """
        Initializes an empty task list and sets the initial ID counter.
        """
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task with the given name and description.

        Args:
            task_name (str): The name of the task (non-empty).
            task_description (str): The description of the task (non-empty).

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            InvalidTaskInputError: If task_name or task_description are empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskInputError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise InvalidTaskInputError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes the task with the specified ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task existed and was removed, False otherwise.

        Raises:
            InvalidTaskInputError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing the task_term in their name or description.

        Args:
            task_term (str): The term to search for (case-insensitive, non-empty).

        Returns:
            list[dict]: List of matching tasks, each a dictionary containing
                        (id, task_name, task_description, is_finished).

        Raises:
            InvalidTaskInputError: If task_term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise InvalidTaskInputError("Search term must be a non-empty string.")

        term_lower = task_term.strip().lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if term_lower in task["task_name"].lower() or term_lower in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks the task with the specified ID as finished.

        Args:
            task_id (int): The ID of the task to finish.

        Returns:
            bool: True if the task existed and was marked as finished, False otherwise.

        Raises:
            InvalidTaskInputError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is None:
            return False
        if not task["is_finished"]:
            task["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks in the todo list.

        Returns:
            list[dict]: List of all tasks, each a dictionary containing
                        (id, task_name, task_description, is_finished).
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks from the todo list.

        Returns:
            bool: True if the todo list was cleared, False if it was already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False


# Simple Console-Based Application for Demonstration and Testing
def print_task(task: Dict):
    print(f"ID: {task['id']} | Name: {task['task_name']} | Description: {task['task_description']} | Finished: {task['is_finished']}")


def main():
    manager = TaskManager()
    actions = {
        "add": "Add a new task",
        "remove": "Remove a task by ID",
        "search": "Search tasks",
        "finish": "Finish a task by ID",
        "get_all": "Display all tasks",
        "clear_all": "Clear all tasks",
        "exit": "Exit the application"
    }

    print("Welcome to Todo List App")
    while True:
        print("\nChoose an action:")
        for cmd, desc in actions.items():
            print(f"  {cmd}: {desc}")
        choice = input("\nEnter action: ").strip().lower()

        try:
            if choice == "add":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task added successfully with ID {task_id}.")

            elif choice == "remove":
                task_id = int(input("Enter task ID to remove: "))
                if manager.remove(task_id):
                    print(f"Task {task_id} removed.")
                else:
                    print(f"Task {task_id} not found.")

            elif choice == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                if results:
                    print("Search results:")
                    for task in results:
                        print_task(task)
                else:
                    print("No matching tasks found.")

            elif choice == "finish":
                task_id = int(input("Enter task ID to mark as finished: "))
                if manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Task {task_id} not found.")

            elif choice == "get_all":
                tasks = manager.get_all()
                if tasks:
                    print("All tasks:")
                    for task in tasks:
                        print_task(task)
                else:
                    print("No tasks in the list.")

            elif choice == "clear_all":
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")

            elif choice == "exit":
                print("Exiting Todo List App.")
                break

            else:
                print("Invalid action. Please try again.")

        except (ValueError, InvalidTaskInputError) as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
