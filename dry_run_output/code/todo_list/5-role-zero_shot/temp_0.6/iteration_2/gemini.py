
"""
Module for a high-quality, in-memory Todo List application.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, ensuring it is maintainable, reliable, and efficient.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides a robust, readable, and boilerplate-free
    way to represent our data structure. It is a self-contained and
    reusable component.

    Attributes:
        id (int): A unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Task instance to a dictionary."""
        return asdict(self)

class TaskManager:
    """
    Manages a collection of tasks in-memory.

    This class provides a complete interface for adding, removing, searching,
    and updating tasks, with a focus on efficiency and safety.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        The internal data structure `_tasks` is a dictionary for efficient
        O(1) average time complexity for lookups, insertions, and deletions
        by task ID. `_next_id` ensures unique ID generation.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _get_task(self, task_id: int) -> Optional[Task]:
        """A helper method to safely retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: The description for the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or not a string.
            TypeError: If task_description is not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
            
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
            
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        task = self._get_task(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If search_term is empty or not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        normalized_term = search_term.lower().strip()
        results = [
            task.to_dict() for task in self._tasks.values()
            if normalized_term in task.name.lower() or \
               normalized_term in task.description.lower()
        ]
        return results

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all tasks as dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        # Note: _next_id is not reset to prevent potential ID collisions
        # if this manager's state were ever persisted and reloaded.
        return True


if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a basic integration test.

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Finish report", "Complete the Q3 financial report.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")
        print(f"Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    print("\n--- Getting All Tasks ---")
    all_tasks = manager.get_all()
    print(all_tasks)

    print("\n--- Finishing a Task (ID 2) ---")
    success = manager.finish(2)
    print(f"Operation successful: {success}")
    print(manager.get_all())

    print("\n--- Searching for 'report' ---")
    search_results = manager.search("report")
    print(search_results)
    
    print("\n--- Searching for 'kitchen' ---")
    search_results_2 = manager.search("kitchen")
    print(search_results_2)

    print("\n--- Removing a Task (ID 1) ---")
    success = manager.remove(1)
    print(f"Operation successful: {success}")
    print(manager.get_all())

    print("\n--- Attempting to Remove a Non-existent Task (ID 99) ---")
    success = manager.remove(99)
    print(f"Operation successful: {success}")

    print("\n--- Demonstrating Error Handling: Invalid Input ---")
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        manager.remove("abc")
    except TypeError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Clearing All Tasks ---")
    success = manager.clear_all()
    print(f"Operation successful: {success}")
    print("All tasks after clearing:", manager.get_all())
