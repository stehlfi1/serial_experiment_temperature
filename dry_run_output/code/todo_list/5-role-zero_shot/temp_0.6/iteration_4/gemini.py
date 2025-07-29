
import dataclasses
from typing import Dict, List, Any

@dataclasses.dataclass
class Task:
    """
    A dataclass representing a single task item.

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

    This class provides a complete interface to add, remove, search,
    and update tasks, adhering to high standards of code quality,
    safety, and efficiency.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an in-memory task store.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Args:
            task_id: The ID to validate.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer or does not exist.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to its dictionary representation.

        Args:
            task: The Task object to convert.

        Returns:
            A dictionary representing the task.
        """
        return dataclasses.asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
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
            ValueError: If task_id is invalid or not found.
        """
        self._validate_task_id(task_id)
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

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term = search_term.lower().strip()
        
        results = [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
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
            TypeError: If task_id is not an integer.
            ValueError: If task_id is invalid or not found.
        """
        self._validate_task_id(task_id)
        task = self._tasks[task_id]
        if task.is_finished:
            # Optionally, you could return False or raise an error if already finished
            # For idempotency, we allow this and simply confirm the state.
            pass
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks currently in the manager.

        Returns:
            A list of dictionaries, each representing a task.
        """
        return [self._task_to_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Removes all tasks from the manager and resets the ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        print("All tasks have been cleared.")
        return True

# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a basic integration test.

    manager = TaskManager()
    print("TaskManager Initialized.\n")

    # 1. Add tasks
    print("--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task 'Buy groceries' with ID: {id1}")
        id2 = manager.add("Write Python code", "Implement the TaskManager class")
        print(f"Added task 'Write Python code' with ID: {id2}")
        id3 = manager.add("Clean the house", "Focus on the kitchen and bathroom")
        print(f"Added task 'Clean the house' with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")
    print("\n")

    # 2. Get all tasks
    print("--- Current Tasks ---")
    all_tasks = manager.get_all()
    if all_tasks:
        for task in all_tasks:
            print(task)
    else:
        print("No tasks found.")
    print("\n")
    
    # 3. Finish a task
    print("--- Finishing a Task ---")
    try:
        manager.finish(id2)
        print(f"Task with ID {id2} marked as finished.")
    except (ValueError, TypeError) as e:
        print(f"Error finishing task: {e}")
    print("\n")

    # 4. Search for tasks
    print("--- Searching for 'code' ---")
    search_results = manager.search("code")
    if search_results:
        for task in search_results:
            print(task)
    else:
        print("No tasks found matching 'code'.")
    print("\n")

    # 5. Remove a task
    print("--- Removing a Task ---")
    try:
        manager.remove(id3)
        print(f"Task with ID {id3} removed successfully.")
    except (ValueError, TypeError) as e:
        print(f"Error removing task: {e}")
    print("\n")

    # 6. Get all tasks again to see changes
    print("--- Current Tasks After Changes ---")
    all_tasks = manager.get_all()
    if all_tasks:
        for task in all_tasks:
            print(task)
    else:
        print("No tasks found.")
    print("\n")

    # 7. Demonstrate error handling
    print("--- Demonstrating Error Handling ---")
    try:
        manager.remove(999) # Non-existent ID
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        manager.add("", "This should fail") # Empty task name
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        manager.finish("abc") # Invalid ID type
    except TypeError as e:
        print(f"Caught expected error: {e}")
    print("\n")
    
    # 8. Clear all tasks
    print("--- Clearing All Tasks ---")
    manager.clear_all()
    all_tasks = manager.get_all()
    print(f"Number of tasks after clearing: {len(all_tasks)}")
