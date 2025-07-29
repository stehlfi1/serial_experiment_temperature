
"""
A high-quality, maintainable, and efficient console-based Todo List application.

This module provides a TaskManager class that handles the core logic for managing
a list of tasks in memory. It is designed following the principles of the
ISO/IEC 25010 standard for software quality.

Key Quality Characteristics Addressed:
- Functional Suitability: Implements all required features (add, remove, etc.).
- Performance Efficiency: Uses a dictionary for O(1) average time complexity for
  lookups, insertions, and deletions by ID.
- Reliability: Includes robust error handling and input validation to prevent
  crashes and ensure data integrity.
- Maintainability: The code is modular (Task and TaskManager classes), readable,
  and well-documented, making it easy to understand, modify, and extend.
- Testability: The TaskManager class is decoupled from the UI, allowing its
  methods to be easily unit-tested.
- Safety: Protects against invalid inputs by raising appropriate, specific errors.
"""

import dataclasses
from typing import Dict, List, Any, Union

# Using a dataclass for the Task provides type safety, immutability benefits
# (if frozen=True), and auto-generated methods like __init__ and __repr__.
# It's a modern and readable way to represent simple data structures.
@dataclasses.dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    name: str
    description: str
    is_finished: bool = False

class TaskManager:
    """
    Manages a collection of tasks with high-performance and robust logic.

    This class provides a clean interface for adding, removing, searching,
    and updating tasks. It uses a dictionary for efficient in-memory storage,
    ensuring fast operations.
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
            ValueError: If task_id is a non-positive integer.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

    @staticmethod
    def _format_task_as_dict(task: Task) -> Dict[str, Union[int, str, bool]]:
        """
        Formats a Task object into the specified dictionary format for output.
        This centralizes the output structure for consistency and easy modification.
        """
        return {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "is_finished": task.is_finished,
        }

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task (must be a non-empty string).
            task_description: A description for the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty string.
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
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is a non-positive integer.
            KeyError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks where the name or description contains the search term.
        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if the search term is empty or no tasks match.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            return []

        normalized_term = search_term.lower()
        
        # List comprehension is efficient and readable for filtering.
        return [
            self._format_task_as_dict(task)
            for task in self._tasks.values()
            if normalized_term in task.name.lower()
            or normalized_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is a non-positive integer.
            KeyError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks currently in the list.

        Returns:
            A list of dictionaries, representing all tasks.
        """
        return [self._format_task_as_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list and resets the ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Demonstration of Usage ---
def main():
    """
    Main function to demonstrate the TaskManager functionality.
    This acts as the console-based user interface for the application.
    """
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"  - Added task with ID: {id1}")
        id2 = manager.add("Learn Python OOP", "Study classes, inheritance, and polymorphism.")
        print(f"  - Added task with ID: {id2}")
        id3 = manager.add("Write Project Documentation", "Document the TaskManager class.")
        print(f"  - Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"  - Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Displaying all tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    # 3. Finish a task
    print("\n3. Finishing a task...")
    try:
        if manager.finish(id2):
            print(f"  - Task {id2} marked as finished.")
    except (KeyError, ValueError, TypeError) as e:
        print(f"  - Error finishing task: {e}")

    print("\n   Displaying all tasks after update:")
    for task in manager.get_all():
        print(f"  - {task}")

    # 4. Search for tasks
    print("\n4. Searching for tasks containing 'project':")
    search_results = manager.search("project")
    if search_results:
        for task in search_results:
            print(f"  - Found: {task}")
    else:
        print("  - No tasks found.")

    # 5. Remove a task
    print("\n5. Removing a task...")
    try:
        if manager.remove(id1):
            print(f"  - Task {id1} removed successfully.")
    except (KeyError, ValueError, TypeError) as e:
        print(f"  - Error removing task: {e}")

    print("\n   Displaying all tasks after removal:")
    for task in manager.get_all():
        print(f"  - {task}")

    # 6. Demonstrate Error Handling
    print("\n6. Demonstrating error handling:")
    print("  - Attempting to add a task with an empty name...")
    try:
        manager.add("", "This should fail.")
    except ValueError as e:
        print(f"    -> Caught expected error: {e}")

    print("  - Attempting to remove a non-existent task (ID 99)...")
    try:
        manager.remove(99)
    except KeyError as e:
        print(f"    -> Caught expected error: {e}")
        
    print("  - Attempting to use an invalid ID type...")
    try:
        manager.finish("abc")
    except TypeError as e:
        print(f"    -> Caught expected error: {e}")

    # 7. Clear all tasks
    print("\n7. Clearing all tasks...")
    if manager.clear_all():
        print("  - All tasks have been cleared.")

    print("\n   Final task list:")
    print(f"  - {manager.get_all()}")


if __name__ == "__main__":
    main()
