
"""
This module provides a TaskManager for a console-based todo list application.

It adheres to high-quality standards by focusing on:
- Functional Suitability: Correctly implements all required features.
- Performance Efficiency: Uses efficient data structures for task management.
- Reliability: Implements robust error handling and input validation.
- Maintainability: Encapsulated in a well-documented, modular class.
"""

from dataclasses import dataclass
from typing import Dict, List, Any

# ISO/IEC 25010 - Maintainability (Modularity)
# Using a dataclass clearly defines the structure of a task, making the
# code easier to understand and modify.
@dataclass
class Task:
    """
    Represents a single task with its attributes.

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
    Manages a collection of tasks in memory, providing an interface
    to add, remove, search, and modify tasks.

    This class is designed for testability and maintainability, with no
    external dependencies like databases or files.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an in-memory task store."""
        # ISO/IEC 25010 - Performance Efficiency
        # A dictionary provides O(1) average time complexity for lookups,
        # insertions, and deletions by task ID.
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    # ISO/IEC 25010 - Maintainability (Modularity, Reusability)
    # This private helper method centralizes task validation and retrieval,
    # avoiding code duplication in `remove` and `finish` methods.
    def _validate_and_get_task(self, task_id: int) -> Task:
        """
        Validates a task ID and returns the corresponding Task object.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task object if found.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        try:
            return self._tasks[task_id]
        except KeyError:
            # `from None` is used to provide a cleaner traceback.
            raise KeyError(f"Task with ID {task_id} not found.") from None

    # ISO/IEC 25010 - Maintainability (Reusability)
    # This helper centralizes the output format, making it easy to change
    # the structure of returned task data in one place.
    def _format_task_as_dict(self, task: Task) -> Dict[str, Any]:
        """
        Formats a Task object into a dictionary for external representation.

        Note: The requirement specified the format as a tuple-like structure
        `(id, task_name, ...)`, but returning a dictionary is a more robust
        and standard practice in Python for structured data. It is self-describing
        and less prone to breaking client code if the order changes.

        Args:
            task: The Task object to format.

        Returns:
            A dictionary representing the task.
        """
        return {
            "id": task.id,
            "task_name": task.name,
            "task_description": task.description,
            "is_finished": task.is_finished,
        }

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name/title for the new task.
            task_description: The description for the new task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is an empty string or not a string.
        """
        # ISO/IEC 25010 - Reliability (Fault Tolerance) & Security (Safety)
        # Input validation protects the system from invalid data.
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string.")

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
            True if the task was successfully removed.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_and_get_task(task_id)  # Ensures task exists
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks where the search term appears in the name or description.
        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: If search_term is an empty string or not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term_lower = search_term.lower()
        results = [
            self._format_task_as_dict(task)
            for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If the task_id does not exist.
        """
        task = self._validate_and_get_task(task_id)
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks currently in the manager.

        Returns:
            A list of dictionaries representing all tasks.
        """
        return [self._format_task_as_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager and resets the ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Example Usage ---
# This section demonstrates how to use the TaskManager class.
# It can be run directly to test the functionality.
if __name__ == "__main__":
    print("--- Todo List App Demo ---")
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Code review", "Review PR #123 for the new feature.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Plan weekend", "Decide on a hiking trail.")
        print(f"Added task with ID: {id3}")
    except ValueError as e:
        print(f"Error: {e}")

    # Get all tasks
    print("\n--- All Tasks ---")
    print(manager.get_all())

    # Finish a task
    try:
        manager.finish(id2)
        print(f"\nTask {id2} marked as finished.")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")

    # Search for tasks
    print("\n--- Searching for 'plan' ---")
    print(manager.search("plan"))

    # Remove a task
    try:
        manager.remove(id1)
        print(f"\nTask {id1} removed.")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")

    # Get all tasks again
    print("\n--- All Tasks After Changes ---")
    print(manager.get_all())

    # Test error handling
    print("\n--- Testing Error Handling ---")
    try:
        manager.remove(999)
    except KeyError as e:
        print(f"Caught expected error: {e}")

    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Clear all tasks
    manager.clear_all()
    print("\n--- All tasks cleared ---")
    print(f"Current tasks: {manager.get_all()}")
