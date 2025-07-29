
import sys
from typing import List, Dict


class Task:
    """
    Represents a single todo task.
    """

    def __init__(self, task_id: int, task_name: str, task_description: str):
        """
        Initializes a Task object.

        :param task_id: Unique identifier for the task.
        :param task_name: Name of the task.
        :param task_description: Description of the task.
        """
        self.id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the task.

        :return: Dict containing task information.
        """
        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_description": self.task_description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Provides an interface for managing todo tasks.
    Fulfills ISO/IEC 25010 standards for maintainability, reliability, and usability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and the ID counter.
        """
        self._tasks = {}  # type: Dict[int, Task]
        self._next_id = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the task manager.

        :param task_name: The name of the task.
        :param task_description: The description of the task.
        :return: The unique ID of the newly added task.
        :raises ValueError: If task_name or task_description is empty.
        """
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name must be a non-empty string.")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        :param task_id: The ID of the task to remove.
        :return: True if removal was successful, False if task was not found.
        :raises ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks that contain the search term in their name or description.

        :param task_term: The search term string.
        :return: List of matching tasks as dicts.
        :raises ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = []
        for task in self._tasks.values():
            if term in task.task_name.lower() or term in task.task_description.lower():
                results.append(task.to_dict())
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        :param task_id: The ID of the task to mark as finished.
        :return: True if the operation was successful, False if task was not found.
        :raises ValueError: If task_id is not a positive integer.
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
        Retrieves all tasks with their details.

        :return: List of all tasks as dicts.
        """
        # Sorted by task_id for consistency
        return [self._tasks[tid].to_dict() for tid in sorted(self._tasks.keys())]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the manager.

        :return: True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False


# Console-based UI for demonstration and testing
def display_tasks(tasks: List[Dict]):
    if not tasks:
        print("No tasks found.")
        return
    print("\nID | Name           | Description               | Finished")
    print("-" * 60)
    for t in tasks:
        print(f"{t['id']:2} | {t['task_name'][:15]:15} | {t['task_description'][:25]:25} | {'Yes' if t['is_finished'] else 'No'}")
    print()


def main():
    manager = TaskManager()

    commands = {
        "add": "Add a new task",
        "remove": "Remove a task by ID",
        "search": "Search for tasks",
        "finish": "Mark a task as finished",
        "get_all": "List all tasks",
        "clear_all": "Delete all tasks",
        "quit": "Exit"
    }

    while True:
        print("\nAvailable commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd}: {desc}")
        choice = input("\nEnter command: ").strip().lower()

        try:
            if choice == "add":
                name = input("Task name: ")
                desc = input("Task description: ")
                task_id = manager.add(name, desc)
                print(f"Task added with ID {task_id}.")

            elif choice == "remove":
                task_id = int(input("Task ID to remove: "))
                if manager.remove(task_id):
                    print("Task removed.")
                else:
                    print("Task not found.")

            elif choice == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                display_tasks(results)

            elif choice == "finish":
                task_id = int(input("Task ID to finish: "))
                if manager.finish(task_id):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")

            elif choice == "get_all":
                all_tasks = manager.get_all()
                display_tasks(all_tasks)

            elif choice == "clear_all":
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")

            elif choice == "quit":
                print("Exiting...")
                break

            else:
                print("Invalid command. Please try again.")

        except ValueError as ve:
            print(f"[ValueError] {ve}")
        except Exception as e:
            print(f"[Error] {e}")


if __name__ == "__main__":
    main()
