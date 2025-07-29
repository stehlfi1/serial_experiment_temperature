
"""
A high-quality, maintainable implementation of a console-based Todo List Manager.

This module provides the TaskManager class, which adheres to the principles of
the ISO/IEC 25010 standard for software quality.
"""

import dataclasses
from typing import Dict, List, Any

# --- Data Model ---

@dataclasses.dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides type safety, automatic __init__ and __repr__,
    and clearly defines the data structure, enhancing maintainability.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


# --- Core Logic ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search, and
    update tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        A dictionary is used for self._tasks to allow for O(1) average time
        complexity for lookups, insertions, and deletions by task ID.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to a dictionary for external representation.
        
        This helper method ensures a consistent output format for all functions
        that return task details.
        """
        return dataclasses.asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty or just whitespace.
            task_description: A description for the task.

        Returns:
            The unique ID of the newly created task.

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
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a case-insensitive search term in name or description.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found or search_term is empty.
        
        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        normalized_term = search_term.lower().strip()
        if not normalized_term:
            return []

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
        
        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            self._tasks[task_id].is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        return [self._task_to_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        # Note: _next_id is not reset to prevent potential ID reuse if this
        # manager instance is part of a longer-running application.
        return True


# --- Example Usage ---

if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a basic integration test.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n--- 1. Adding Tasks ---")
    id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
    print(f"Added task with ID: {id1}")
    id2 = manager.add("Code review", "Review the new feature branch for project X.")
    print(f"Added task with ID: {id2}")
    id3 = manager.add("Plan weekend trip", "Research destinations and book hotel.")
    print(f"Added task with ID: {id3}")

    # 2. Get all tasks
    print("\n--- 2. Getting All Tasks ---")
    all_tasks = manager.get_all()
    print("Current tasks:")
    for task in all_tasks:
        print(f"  {task}")

    # 3. Finish a task
    print("\n--- 3. Finishing a Task ---")
    print(f"Marking task {id2} as finished...")
    success = manager.finish(id2)
    print(f"Operation successful: {success}")
    print("Status of task 2:", manager.search("Code review")[0])

    # 4. Search for tasks
    print("\n--- 4. Searching for Tasks ---")
    search_results = manager.search("trip")
    print("Search results for 'trip':")
    for task in search_results:
        print(f"  {task}")

    # 5. Remove a task
    print("\n--- 5. Removing a Task ---")
    print(f"Removing task {id1}...")
    success = manager.remove(id1)
    print(f"Operation successful: {success}")

    # 6. Get all tasks again
    print("\n--- 6. Getting All Tasks After Changes ---")
    all_tasks = manager.get_all()
    print("Current tasks:")
    for task in all_tasks:
        print(f"  {task}")

    # 7. Handle errors gracefully
    print("\n--- 7. Error Handling ---")
    print("Attempting to remove a non-existent task (ID 99)...")
    success = manager.remove(99)
    print(f"Operation successful: {success}")

    try:
        print("Attempting to add a task with an empty name...")
        manager.add(" ", "This should fail.")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # 8. Clear all tasks
    print("\n--- 8. Clearing All Tasks ---")
    success = manager.clear_all()
    print(f"Clear all successful: {success}")
    print("Final task list:", manager.get_all())
