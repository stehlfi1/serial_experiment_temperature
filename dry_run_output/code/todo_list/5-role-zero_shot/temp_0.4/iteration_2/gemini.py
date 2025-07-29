
"""
A high-quality, maintainable implementation of a Todo List application.

This module provides the TaskManager class, which handles all the core
functionalities of a todo list, such as adding, removing, and searching for tasks.
The implementation follows best practices and aligns with the principles of the
ISO/IEC 25010 standard for software quality.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any

# --- Data Model (Modularity) ---
# Using a dataclass provides a clear, concise, and robust way to represent a task.
# It's more readable and less error-prone than using raw dictionaries internally.

@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The title or name of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

# --- Core Application Logic (Functional Suitability & Maintainability) ---

class TaskManager:
    """
    Manages a collection of tasks with functionalities to add, remove, and search.

    This class provides a clean interface for interacting with an in-memory
    todo list. It is designed for correctness, efficiency, and testability.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task list.
        
        Internal data is prefixed with an underscore to indicate that it should
        not be accessed directly from outside the class, promoting encapsulation.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to its dictionary representation for external use.
        
        This helper method ensures a consistent output format as required by the
        interface, promoting modularity and preventing code duplication.

        Args:
            task (Task): The task object to convert.

        Returns:
            Dict[str, Any]: A dictionary representing the task.
        """
        return {
            "id": task.id,
            "task_name": task.name,
            "task_description": task.description,
            "is_finished": task.is_finished,
        }

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name/title of the task. Must be a non-empty string.
            task_description (str): A description of the task.

        Returns:
            int: The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty or not a string.
            TypeError: If inputs are not of type string.
        """
        # --- Safety & Reliability: Input Validation ---
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
        
        # --- Performance Efficiency: O(1) insertion ---
        self._tasks[task_id] = new_task
        self._next_id += 1
        
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.
        
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        # --- Performance Efficiency: O(1) lookup and deletion ---
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks where the search term appears in the name or description.
        The search is case-insensitive.

        Args:
            search_term (str): The term to search for.

        Returns:
            List[Dict[str, Any]]: A list of tasks that match the search criteria.
                                  Returns an empty list if no matches are found.
        
        Raises:
            ValueError: If search_term is empty or not a string.
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = search_term.lower()
        
        # --- Performance Efficiency: O(n) search, which is optimal without indexing ---
        results = [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task's status was changed to finished,
                  False if the task was not found or was already finished.
                  
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        # --- Performance Efficiency: O(1) lookup and update ---
        task_to_update = self._tasks.get(task_id)
        
        if task_to_update and not task_to_update.is_finished:
            task_to_update.is_finished = True
            return True
        
        # Return False if task doesn't exist or is already finished
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks in the list.

        Returns:
            List[Dict[str, Any]]: A list of all tasks.
        """
        return [self._task_to_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            bool: True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a fresh start
        return True


# --- Example Usage (Demonstration & Basic Testability) ---
# This block demonstrates how to use the TaskManager and also serves as a
# basic, runnable test suite.

if __name__ == "__main__":
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
        
        # Demonstrate validation
        print("\nAttempting to add a task with an empty name...")
        manager.add("  ", "This should fail")
    except (ValueError, TypeError) as e:
        print(f"Caught expected error: {e}")

    # 2. Get all tasks
    print("\n--- 2. Getting All Tasks ---")
    all_tasks = manager.get_all()
    print("Current tasks:")
    for task in all_tasks:
        print(f"  - {task}")

    # 3. Search for a task
    print("\n--- 3. Searching for Tasks ---")
    print("Searching for 'report':")
    search_results = manager.search("report")
    for task in search_results:
        print(f"  - Found: {task}")
        
    print("\nSearching for 'kitchen':")
    search_results = manager.search("kitchen")
    for task in search_results:
        print(f"  - Found: {task}")

    # 4. Finish a task
    print("\n--- 4. Finishing a Task ---")
    print(f"Marking task {id2} as finished...")
    success = manager.finish(id2)
    print(f"Operation successful: {success}")
    
    print(f"Attempting to finish task {id2} again...")
    success_again = manager.finish(id2)
    print(f"Operation successful: {success_again} (as expected, no change)")

    print("\nAll tasks after finishing one:")
    for task in manager.get_all():
        print(f"  - {task}")

    # 5. Remove a task
    print("\n--- 5. Removing a Task ---")
    print(f"Removing task {id1}...")
    removed = manager.remove(id1)
    print(f"Removal successful: {removed}")
    
    print("Attempting to remove a non-existent task (ID 99)...")
    removed_non_existent = manager.remove(99)
    print(f"Removal successful: {removed_non_existent}")

    # 6. Get all tasks again
    print("\n--- 6. Final Task List ---")
    final_tasks = manager.get_all()
    print("Current tasks:")
    for task in final_tasks:
        print(f"  - {task}")

    # 7. Clear all tasks
    print("\n--- 7. Clearing All Tasks ---")
    cleared = manager.clear_all()
    print(f"All tasks cleared: {cleared}")
    print(f"Number of tasks remaining: {len(manager.get_all())}")
