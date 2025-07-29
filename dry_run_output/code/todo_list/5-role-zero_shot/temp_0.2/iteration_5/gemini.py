
"""
A high-quality, maintainable implementation of a Todo List application.

This module provides a TaskManager class that handles all the core logic
for managing tasks, adhering to the principles of ISO/IEC 25010 for
software quality.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# --- Data Model (Modularity & Readability) ---
# Using a dataclass provides type safety, immutability for certain fields,
# and a clear, readable structure for what a "Task" is.

@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id: A unique integer identifier for the task.
        name: The name or title of the task.
        description: A more detailed description of the task.
        is_finished: A boolean indicating if the task is completed.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

# --- Core Logic (TaskManager Class) ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean interface for adding, removing, searching,
    and updating tasks. It is designed for correctness, performance, and safety.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up the in-memory data store and the ID counter.
        Using a dictionary for `_tasks` ensures O(1) average time complexity
        for lookups, insertions, and deletions by ID, which is highly efficient.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID. (Safety & Reusability)

        Args:
            task_id: The ID to validate.

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

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to a dictionary. (Modularity)

        This ensures a consistent output format for all public methods
        that return task details.
        """
        return asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: The description for the task.

        Returns:
            The unique integer ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        # --- Safety: Input Validation ---
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

        # --- Correctness: Core Logic ---
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
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        # --- Reliability: Graceful Error Handling ---
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            return True
        except (TypeError, ValueError, KeyError) as e:
            # In a real application, this could be logged.
            print(f"Error removing task: {e}", file=sys.stderr)
            return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        # --- Safety: Input Validation ---
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        # --- Performance: Efficient Iteration ---
        # A list comprehension is generally faster than a for-loop with appends.
        normalized_term = search_term.lower()
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if normalized_term in task.name.lower() or \
               normalized_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        # --- Reliability: Graceful Error Handling ---
        try:
            self._validate_task_id(task_id)
            if self._tasks[task_id].is_finished:
                # Optional: Inform the user if the task is already finished.
                print(f"Info: Task {task_id} was already finished.", file=sys.stderr)
            self._tasks[task_id].is_finished = True
            return True
        except (TypeError, ValueError, KeyError) as e:
            print(f"Error finishing task: {e}", file=sys.stderr)
            return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries representing all tasks.
            The list is sorted by task ID for consistent ordering.
        """
        # Sort by key (task.id) for predictable output
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- Example Usage (Testability & Usability) ---
# This block demonstrates how to use the TaskManager class.
# It is separated from the class logic, making the class itself
# highly testable and reusable in other contexts (e.g., a web API).

if __name__ == "__main__":
    print("--- Todo List Application Demo ---")

    # 1. Initialize the manager
    manager = TaskManager()
    print("\n[OK] TaskManager initialized.")

    # 2. Add tasks
    print("\n--> Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"[OK] Added task with ID: {id1}")
        id2 = manager.add("  Write Python code  ", "Implement the TaskManager class.")
        print(f"[OK] Added task with ID: {id2}")
        id3 = manager.add("Read a book", "Chapter 3 of 'Clean Architecture'")
        print(f"[OK] Added task with ID: {id3}")
        # Add an invalid task
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"[FAIL] Caught expected error: {e}")

    # 3. Get all tasks
    print("\n--> Current tasks:")
    all_tasks = manager.get_all()
    for t in all_tasks:
        print(f"  - {t}")

    # 4. Finish a task
    print("\n--> Finishing task 2...")
    if manager.finish(2):
        print("[OK] Task 2 marked as finished.")
    else:
        print("[FAIL] Could not finish task 2.")

    # Try to finish a non-existent task
    print("\n--> Finishing non-existent task 99...")
    if not manager.finish(99):
        print("[OK] Correctly failed to finish non-existent task.")

    # 5. Search for tasks
    print("\n--> Searching for 'code'...")
    search_results = manager.search("code")
    print(f"[OK] Found {len(search_results)} result(s):")
    for t in search_results:
        print(f"  - {t}")

    # 6. Remove a task
    print("\n--> Removing task 1...")
    if manager.remove(1):
        print("[OK] Task 1 removed.")
    else:
        print("[FAIL] Could not remove task 1.")

    # 7. Get all tasks again to see the changes
    print("\n--> Current tasks after updates:")
    all_tasks = manager.get_all()
    for t in all_tasks:
        print(f"  - {t}")

    # 8. Clear all tasks
    print("\n--> Clearing all tasks...")
    if manager.clear_all():
        print("[OK] All tasks have been cleared.")
    
    # 9. Final check
    print("\n--> Final task list:")
    final_tasks = manager.get_all()
    print(f"[OK] Task count: {len(final_tasks)}")

