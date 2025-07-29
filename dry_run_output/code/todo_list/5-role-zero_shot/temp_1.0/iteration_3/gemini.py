
"""
A module for managing a high-quality, in-memory todo list application.

This module provides a TaskManager class that adheres to the principles of
the ISO/IEC 25010 standard for software quality, focusing on maintainability,
efficiency, and reliability.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# For a more robust solution in production, consider using a logging framework.
# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface for adding, removing, searching,
    and updating tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an in-memory storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validates a given task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: The description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or just whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
             raise TypeError("Task description must be a string.")

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description)
        self._tasks[task_id] = new_task
        self._next_id += 1
        # logging.info(f"Task {task_id} added: '{task_name}'")
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        # logging.info(f"Task {task_id} removed.")
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by name or description (case-insensitive).

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            An empty list is returned if the term is empty or no matches are found.

        Raises:
            TypeError: if search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
            
        if not search_term.strip():
            return []

        lower_term = search_term.lower()
        results = [
            asdict(task) for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id].is_finished = True
        # logging.info(f"Task {task_id} marked as finished.")
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
            The list is sorted by task ID.
        """
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [asdict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This action is irreversible.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        # logging.warning("All tasks have been cleared.")
        return True


# --- Example Usage ---
def main() -> None:
    """
    A simple command-line interface to demonstrate the TaskManager.
    This function showcases the core functionality and error handling.
    """
    print("--- Todo List App Demo ---")
    manager = TaskManager()

    try:
        # 1. Add tasks
        print("\n1. Adding tasks...")
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Finish report", "Complete the Q3 financial report.")
        id3 = manager.add("Call mom", "Check in with mom about her trip.")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")

        # 2. Get all tasks
        print("\n2. Current tasks:")
        for task in manager.get_all():
            print(f"  - {task}")

        # 3. Finish a task
        print(f"\n3. Finishing task {id2}...")
        manager.finish(id2)
        print(f"Task {id2} finished successfully.")

        # 4. Search for a task
        print("\n4. Searching for 'report'...")
        results = manager.search("report")
        if results:
            print("  Found matching tasks:")
            for task in results:
                print(f"  - {task}")
        else:
            print("  No tasks found.")
            
        # 5. Remove a task
        print(f"\n5. Removing task {id3}...")
        manager.remove(id3)
        print(f"Task {id3} removed successfully.")

        # 6. Get all tasks again
        print("\n6. Current tasks after changes:")
        for task in manager.get_all():
            print(f"  - {task}")

        # 7. Demonstrate error handling
        print("\n7. Demonstrating error handling...")
        print("  - Trying to remove a non-existent task (ID 99)...")
        try:
            manager.remove(99)
        except KeyError as e:
            print(f"    SUCCESSFULLY CAUGHT ERROR: {e}")

        print("  - Trying to add a task with an empty name...")
        try:
            manager.add("   ", "This should fail.")
        except ValueError as e:
            print(f"    SUCCESSFULLY CAUGHT ERROR: {e}")
            
        print("  - Trying to use a non-integer ID...")
        try:
            manager.finish("invalid_id")
        except TypeError as e:
            print(f"    SUCCESSFULLY CAUGHT ERROR: {e}")

        # 8. Clear all tasks
        print("\n8. Clearing all tasks...")
        manager.clear_all()
        print("  All tasks cleared.")
        print(f"  Final task list: {manager.get_all()}")

    except (ValueError, TypeError, KeyError) as e:
        print(f"\nAn unexpected critical error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
