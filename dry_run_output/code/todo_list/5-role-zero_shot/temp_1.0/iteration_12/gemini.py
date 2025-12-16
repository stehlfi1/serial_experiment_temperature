
import sys
from typing import List, Dict, Any, Union

# Define a type alias for a task dictionary for better readability and maintainability.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks in-memory.

    This class provides a complete interface to add, remove, search, finish,
    and manage tasks, adhering to ISO/IEC 25010 quality standards by being
    efficient, reliable, and maintainable.

    Attributes:
        _tasks (Dict[int, Task]): A dictionary to store tasks, mapping task ID to task data.
        _next_id (int): A counter to generate unique IDs for new tasks.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task list.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the collection.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description of the task. Must be a non-empty string.

        Returns:
            The unique integer ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description are empty or whitespace only.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The unique ID of the task to remove.

        Returns:
            True if the task was found and removed, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks where the search term appears in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search criteria. The list is
            empty if no tasks match or the search term is empty.
            
        Raises:
            ValueError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise ValueError("Search term must be a string.")

        if not search_term.strip():
            return []
            
        lower_term = search_term.lower()
        
        return [
            task
            for task in self._tasks.values()
            if lower_term in task["name"].lower()
            or lower_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The unique ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
            
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
            
        if task_id in self._tasks:
            if not self._tasks[task_id]["is_finished"]:
                self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns a copy to prevent
            unintended modification of the internal task list.
        """
        return list(self._tasks.values())
        
    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.
        
        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- DEMONSTRATION ---
def print_tasks(title: str, tasks: List[Task]) -> None:
    """Helper function to print tasks in a readable format."""
    print(f"\n--- {title} ---")
    if not tasks:
        print("No tasks to show.")
        return
    for task in tasks:
        status = "Finished" if task["is_finished"] else "Pending"
        print(f"ID: {task['id']}, Name: {task['name']}, Desc: {task['description']}, Status: {status}")
    print("-" * (len(title) + 8))

if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a simple integration test.

    print("Initializing Task Manager...")
    manager = TaskManager()

    # 1. Add tasks
    print("\n1. Adding new tasks...")
    try:
        id1 = manager.add("Implement Core Logic", "Write the main TaskManager class.")
        id2 = manager.add("Write Unit Tests", "Use pytest to test the TaskManager.")
        id3 = manager.add("Refactor Database Module", "Prepare for production database.")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
    except ValueError as e:
        print(f"Error adding task: {e}", file=sys.stderr)
        
    print_tasks("Current Tasks After Adding", manager.get_all())

    # 2. Finish a task
    print("\n2. Finishing task with ID 2...")
    if manager.finish(id2):
        print("Task 2 marked as finished.")
    else:
        print("Failed to finish task 2.")
    
    print_tasks("Current Tasks After Finishing One", manager.get_all())
    
    # 3. Search for tasks
    print("\n3. Searching for tasks containing 'database'...")
    search_results = manager.search("database")
    print_tasks("Search Results for 'database'", search_results)
    
    print("\n4. Searching for tasks containing 'write'...")
    search_results_write = manager.search("Write") # Case-insensitive
    print_tasks("Search Results for 'Write'", search_results_write)

    # 5. Remove a task
    print("\n5. Removing task with ID 1...")
    if manager.remove(id1):
        print("Task 1 removed successfully.")
    else:
        print("Failed to remove task 1.")
        
    print_tasks("Current Tasks After Removing One", manager.get_all())
    
    # 6. Demonstrate Error Handling
    print("\n6. Demonstrating Error Handling...")
    
    # Trying to add an empty task
    try:
        manager.add("  ", "Empty task name")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # Trying to remove a non-existent task
    if not manager.remove(999):
        print("Caught expected result: Cannot remove non-existent task ID 999.")

    # Trying to use an invalid ID
    try:
        manager.finish(-5)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # 7. Clear all tasks
    print("\n7. Clearing all tasks...")
    if manager.clear_all():
        print("All tasks have been cleared.")

    print_tasks("Final State of Tasks", manager.get_all())
