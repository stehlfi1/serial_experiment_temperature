
"""
A module for managing a collection of tasks in memory.

This module provides the TaskManager class, which offers a clean,
object-oriented interface for a todo list application. It is designed
with best practices and ISO/IEC 25010 quality characteristics in mind,
emphasizing reliability, efficiency, and maintainability.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# For Python versions < 3.9, use List and Dict from typing
if sys.version_info < (3, 9):
    from typing import List, Dict
else:
    List = list
    Dict = dict


@dataclass
class Task:
    """
    A dataclass representing a single task.

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
    Manages a collection of tasks with an object-oriented interface.

    This class handles all core logic for a todo list, including adding,
    removing, searching, and updating tasks. It uses an in-memory dictionary
    for efficient data storage and retrieval.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer or does not exist.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID '{task_id}' not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task. Must not be empty.
            task_description (str): The description for the task.

        Returns:
            int: The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is empty or contains only whitespace.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description.strip()
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.
        """
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            return True
        except (ValueError, TypeError):
            # Gracefully handle invalid IDs by returning False
            return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term (str): The term to search for.

        Returns:
            List[Dict[str, Any]]: A list of tasks that match the search term.
                                  Each task is a dictionary.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        
        if not search_term.strip():
            return [] # Return empty list for empty search term

        normalized_term = search_term.strip().lower()
        
        results = [
            asdict(task) for task in self._tasks.values()
            if normalized_term in task.name.lower() or \
               normalized_term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished,
                  False otherwise.
        """
        try:
            self._validate_task_id(task_id)
            self._tasks[task_id].is_finished = True
            return True
        except (ValueError, TypeError):
            return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks, sorted by their ID.

        Returns:
            List[Dict[str, Any]]: A list of all tasks. Each task is a dictionary.
        """
        # Sorting by ID provides a consistent and predictable order
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [asdict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: Always returns True to indicate success.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Example Usage ---
def print_tasks(tasks: List[Dict[str, Any]]):
    """Helper function to neatly print a list of tasks."""
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✓" if task['is_finished'] else "✗"
        print(
            f"[{status}] ID: {task['id']} | "
            f"Name: {task['name']} | "
            f"Description: {task['description']}"
        )

if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class.
    # It acts as a simple, interactive console client.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n--- 1. Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Finish report", "Complete the Q3 financial report.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")
        print(f"Added task with ID: {id3}")
        # Add a task with an invalid name (will raise ValueError)
        # manager.add("   ", "This should fail")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n--- 2. Current Tasks ---")
    all_tasks = manager.get_all()
    print_tasks(all_tasks)

    # 3. Finish a task
    print("\n--- 3. Finishing a Task (ID 2) ---")
    success = manager.finish(2)
    print(f"Task finished successfully: {success}")
    
    # Try to finish a non-existent task
    success_fail = manager.finish(99)
    print(f"Attempt to finish non-existent task (ID 99) was successful: {success_fail}")

    print("\n--- Current Tasks After Finishing One ---")
    print_tasks(manager.get_all())

    # 4. Search for tasks
    print("\n--- 4. Searching for 'report' ---")
    search_results = manager.search("report")
    print_tasks(search_results)
    
    print("\n--- Searching for 'kitchen' ---")
    search_results_2 = manager.search("kitchen")
    print_tasks(search_results_2)

    # 5. Remove a task
    print("\n--- 5. Removing a Task (ID 1) ---")
    removed = manager.remove(1)
    print(f"Task removed successfully: {removed}")
    
    print("\n--- Current Tasks After Removal ---")
    print_tasks(manager.get_all())

    # 6. Clear all tasks
    print("\n--- 6. Clearing All Tasks ---")
    cleared = manager.clear_all()
    print(f"All tasks cleared: {cleared}")

    print("\n--- Final Task List ---")
    print_tasks(manager.get_all())

    # 7. Add a new task to confirm ID resets
    print("\n--- 7. Adding a new task after clearing ---")
    new_id = manager.add("Start fresh", "A new beginning.")
    print(f"Added new task with ID: {new_id}")
    print_tasks(manager.get_all())
