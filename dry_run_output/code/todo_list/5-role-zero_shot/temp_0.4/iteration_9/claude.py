
"""
Todo List Application - Task Manager Module

A high-quality, maintainable console-based todo list application
that adheres to ISO/IEC 25010 standards.
"""

from typing import Dict, List, Optional
import threading
from dataclasses import dataclass, asdict


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        task_name (str): Name/title of the task
        task_description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
    """
    id: int
    task_name: str
    task_description: str
    is_finished: bool = False

    def to_dict(self) -> Dict:
        """Convert task to dictionary format."""
        return asdict(self)

    def matches_search_term(self, search_term: str) -> bool:
        """
        Check if task matches the given search term.
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            bool: True if task matches search term
        """
        search_term_lower = search_term.lower()
        return (search_term_lower in self.task_name.lower() or 
                search_term_lower in self.task_description.lower())


class TaskManager:
    """
    A thread-safe task manager for handling todo list operations.
    
    This class provides a complete interface for managing tasks including
    adding, removing, searching, marking as complete, and retrieving tasks.
    All operations are optimized for performance and include comprehensive
    error handling and validation.
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Thread-safe operations

    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): Task name to validate
            
        Raises:
            ValueError: If task name is invalid
            TypeError: If task name is not a string
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")

    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): Task description to validate
            
        Raises:
            ValueError: If task description is invalid
            TypeError: If task description is not a string
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace only")

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task ID is not an integer
            ValueError: If task ID is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): Search term to validate
            
        Raises:
            TypeError: If search term is not a string
            ValueError: If search term is empty
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")

    def _task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists by ID.
        
        Args:
            task_id (int): Task ID to check
            
        Returns:
            bool: True if task exists, False otherwise
        """
        return task_id in self._tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (non-empty string)
            task_description (str): Description of the task (non-empty string)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task name or description is empty/whitespace
            TypeError: If inputs are not strings
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Input validation
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Create new task with unique ID
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            
            # Store task and increment ID counter
            self._tasks[task_id] = task
            self._next_id += 1
            
            return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by ID.
        
        Args:
            task_id (int): ID of the task to remove (positive integer)
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Input validation
        self._validate_task_id(task_id)
        
        with self._lock:
            if not self._task_exists(task_id):
                return False
            
            # Remove task from storage
            del self._tasks[task_id]
            return True

    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term (str): Term to search for (non-empty string)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty/whitespace
            
        Time Complexity: O(n) where n is the number of tasks
        Space Complexity: O(k) where k is the number of matching tasks
        """
        # Input validation
        self._validate_search_term(search_term)
        
        with self._lock:
            matching_tasks = []
            search_term_stripped = search_term.strip()
            
            # Search through all tasks
            for task in self._tasks.values():
                if task.matches_search_term(search_term_stripped):
                    matching_tasks.append(task.to_dict())
            
            # Sort by task ID for consistent ordering
            matching_tasks.sort(key=lambda x: x['id'])
            return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished (positive integer)
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Input validation
        self._validate_task_id(task_id)
        
        with self._lock:
            if not self._task_exists(task_id):
                return False
            
            # Mark task as finished
            self._tasks[task_id].is_finished = True
            return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Time Complexity: O(n log n) where n is the number of tasks (due to sorting)
        Space Complexity: O(n) where n is the number of tasks
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            
            # Sort by task ID for consistent ordering
            all_tasks.sort(key=lambda x: x['id'])
            return all_tasks

    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful operation
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self._lock:
            self._tasks.clear()
            # Reset ID counter for efficiency
            self._next_id = 1
            return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks in the todo list
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self._lock:
            return len(self._tasks)

    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
            
        Time Complexity: O(n) where n is the number of tasks
        Space Complexity: O(1)
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple example of how to use the TaskManager
    class and its various methods.
    """
    # Create task manager instance
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Buy milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {task1_id}, {task2_id}, {task3_id}")
        
        # Display all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nStatistics:")
        print(f"Total tasks: {task_manager.get_task_count()}")
        print(f"Completed tasks: {task_manager.get_completed_count()}")
        
        # Remove a task
        print(f"\nRemoving task {task2_id}...")
        if task_manager.remove(task2_id):
            print("Task removed successfully")
        
        # Display final state
        print("\nFinal task list:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
            
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
