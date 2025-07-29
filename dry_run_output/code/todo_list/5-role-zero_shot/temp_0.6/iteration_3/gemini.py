
"""
This module provides a TaskManager for a console-based To-Do list application.

It adheres to the principles of the ISO/IEC 25010 standard:
- **Functional Suitability**: Implements all required functionalities (add, remove, etc.)
  correctly and completely.
- **Performance Efficiency**: Utilizes a dictionary for data storage, ensuring
  efficient O(1) time complexity for common operations like adding, removing,
  and retrieving tasks by ID.
- **Reliability**: Incorporates robust error handling and input validation to
  ensure maturity and fault tolerance.
- **Security**: Protects the application's state from invalid data through
  rigorous input validation.
- **Maintainability**: Employs a modular, object-oriented design with clear
  separation of concerns (e.g., Task data class, TaskManager class). The code
  is well-documented, readable, and easily testable, facilitating future
  modifications and analysis.
- **Portability**: Uses standard Python libraries, making it adaptable to
  different environments without modification.
"""

import dataclasses
from typing import List, Dict, Any, Union

# --- Custom Exceptions for Clearer Error Handling ---

class TaskNotFoundError(KeyError):
    """Custom exception raised when a task with a given ID is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID '{task_id}' not found.")

class InvalidTaskDataError(ValueError):
    """Custom exception raised for invalid task data, like empty strings."""
    def __init__(self, message: str):
        super().__init__(message)


# --- Data Model for a Task ---

@dataclasses.dataclass
class Task:
    """
    Represents a single task in the to-do list.

    Using a dataclass provides a clear, concise, and robust way to model
    the data structure for a task, improving maintainability and readability.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Union[int, str, bool]]:
        """Converts the Task object to a dictionary."""
        return dataclasses.asdict(self)


# --- Core Application Logic ---

class TaskManager:
    """
    Manages all operations for the to-do list.

    This class encapsulates the logic for adding, removing, searching, and
    updating tasks, providing a clean and maintainable interface.
    """

    def __init__(self):
        """Initializes the TaskManager with an in-memory data store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_strings(self, *args: str):
        """
        Internal helper to validate that string inputs are not empty or just whitespace.

        Raises:
            InvalidTaskDataError: If any provided string is empty or contains only whitespace.
        """
        for arg in args:
            if not arg or not arg.strip():
                raise InvalidTaskDataError("Task name and description cannot be empty.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            InvalidTaskDataError: If task_name or task_description is empty.
        """
        self._validate_task_strings(task_name, task_description)

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description.strip())
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
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
            InvalidTaskDataError: If the search_term is empty.
        """
        self._validate_task_strings(search_term)
        
        normalized_term = search_term.lower()
        
        return [
            task.to_dict()
            for task in self._tasks.values()
            if normalized_term in task.name.lower() or normalized_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
        """
        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks currently in the list.

        Returns:
            A list of all tasks, where each task is a dictionary.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True

    def get_by_id(self, task_id: int) -> Dict[str, Any]:
        """
        Retrieves a single task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            A dictionary representing the task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id].to_dict()


# --- Example Usage ---

if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class.
    # It also serves as a basic integration test.

    manager = TaskManager()
    print("--- To-Do List Application ---")

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Code review", "Review the new feature branch for the project.")
        id3 = manager.add("Plan weekend trip", "Research destinations and book accommodation.")
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
        print(f"Added task with ID: {id3}")
    except InvalidTaskDataError as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Current tasks:")
    all_tasks = manager.get_all()
    for task_info in all_tasks:
        print(f"  - {task_info}")

    # 3. Finish a task
    print("\n3. Finishing task with ID 2...")
    if manager.finish(id2):
        print("  Task finished successfully.")
        print("  Updated task details:", manager.get_by_id(id2))
    else:
        print("  Failed to finish task.")

    # 4. Search for tasks
    print("\n4. Searching for tasks containing 'plan'...")
    search_results = manager.search("plan")
    if search_results:
        for task_info in search_results:
            print(f"  - Found: {task_info}")
    else:
        print("  No tasks found.")

    # 5. Remove a task
    print("\n5. Removing task with ID 1...")
    if manager.remove(id1):
        print("  Task removed successfully.")
    else:
        print("  Failed to remove task.")

    # 6. Show final list of tasks
    print("\n6. Final list of tasks:")
    for task_info in manager.get_all():
        print(f"  - {task_info}")
        
    # 7. Demonstrate error handling
    print("\n7. Testing error handling...")
    try:
        # Attempt to get a non-existent task
        manager.get_by_id(999)
    except TaskNotFoundError as e:
        print(f"  Successfully caught expected error: {e}")
        
    try:
        # Attempt to add a task with invalid data
        manager.add("  ", " ")
    except InvalidTaskDataError as e:
        print(f"  Successfully caught expected error: {e}")

    # 8. Clear all tasks
    print("\n8. Clearing all tasks...")
    if manager.clear_all():
        print("  All tasks cleared.")
    
    print("\nFinal task count:", len(manager.get_all()))
    print("\n--- Demo Finished ---")

