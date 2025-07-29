
"""
A high-quality, maintainable implementation of a console-based To-Do list application.

This module provides a TaskManager class that adheres to the principles of the
ISO/IEC 25010 standard for software quality, emphasizing reliability,
performance, and maintainability.
"""

from typing import Dict, List, Any

class Task:
    """
    Represents a single task in the to-do list.

    This class encapsulates the properties of a task, promoting modularity and
    making the system easier to maintain.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the task object to a dictionary."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

    def __repr__(self) -> str:
        """Provides an unambiguous string representation of the Task object."""
        status = "Finished" if self.is_finished else "Pending"
        return (
            f"Task(id={self.id}, name='{self.name}', "
            f"description='{self.description}', status='{status}')"
        )


class TaskManager:
    """
    Manages a collection of tasks with high performance and reliability.

    This class provides a complete interface for adding, removing, searching,
    and modifying tasks. It uses a dictionary for efficient O(1) lookups.
    """
    def __init__(self):
        """Initializes the TaskManager with an in-memory data store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_exists(self, task_id: int) -> None:
        """
        Internal helper to validate the existence of a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not found in the task list.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Error: Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: The description of the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name is an empty or whitespace-only string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            task_description = "" # Ensure description is a string

        task_id = self._next_id
        new_task = Task(task_id, task_name.strip(), task_description.strip())
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
            ValueError: If task_id is not found.
        """
        self._validate_task_exists(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a term in their name or description.
        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task. Returns an empty list if no matches are found.

        Raises:
            ValueError: If the search term is empty or whitespace-only.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        
        # Use a list comprehension for concise and readable filtering
        return [
            task.to_dict() for task in self._tasks.values()
            if lower_term in task.name.lower() or \
               lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not found.
        """
        self._validate_task_exists(task_id)
        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries. The list is sorted by task ID.
        """
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True

# --- Example Usage ---
# This block demonstrates how to use the TaskManager and its error handling.
# It also serves as a basic integration test.
if __name__ == "__main__":
    def print_tasks(tasks: List[Dict[str, Any]]):
        """Helper function to pretty-print a list of tasks."""
        if not tasks:
            print("  No tasks found.")
            return
        for task in tasks:
            status = "✅" if task['is_finished'] else "◻️"
            print(
                f"  {status} ID: {task['id']} | "
                f"Name: {task['task_name']} | "
                f"Desc: {task['task_description']}"
            )

    task_manager = TaskManager()
    print("--- Initializing To-Do List ---")

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = task_manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"  Added task with ID: {id1}")
        id2 = task_manager.add("Code review", "Review PR #42 for the new feature")
        print(f"  Added task with ID: {id2}")
        id3 = task_manager.add("Workout", "Go for a 5km run")
        print(f"  Added task with ID: {id3}")
    except ValueError as e:
        print(f"  Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Current tasks:")
    print_tasks(task_manager.get_all())

    # 3. Finish a task
    print("\n3. Finishing task ID 1...")
    try:
        task_manager.finish(1)
        print("  Task finished successfully.")
    except ValueError as e:
        print(f"  Error: {e}")
    print_tasks(task_manager.get_all())

    # 4. Search for tasks
    print("\n4. Searching for 'review'...")
    search_results = task_manager.search("review")
    print_tasks(search_results)
    
    print("\n5. Searching for 'gym' (no results expected)...")
    search_results_empty = task_manager.search("gym")
    print_tasks(search_results_empty)

    # 5. Remove a task
    print("\n6. Removing task ID 3...")
    try:
        task_manager.remove(3)
        print("  Task removed successfully.")
    except (ValueError, TypeError) as e:
        print(f"  Error: {e}")
    print("   Current tasks after removal:")
    print_tasks(task_manager.get_all())
    
    # 6. Demonstrate Error Handling
    print("\n7. Demonstrating error handling:")
    
    # Try to remove a non-existent task
    print("  - Attempting to remove non-existent task ID 99...")
    try:
        task_manager.remove(99)
    except ValueError as e:
        print(f"    Caught expected error: {e}")

    # Try to add a task with an empty name
    print("  - Attempting to add a task with an empty name...")
    try:
        task_manager.add("   ", "This should fail")
    except ValueError as e:
        print(f"    Caught expected error: {e}")

    # 7. Clear all tasks
    print("\n8. Clearing all tasks...")
    task_manager.clear_all()
    print("   Tasks cleared. Current list:")
    print_tasks(task_manager.get_all())

    print("\n--- Demo Finished ---")

