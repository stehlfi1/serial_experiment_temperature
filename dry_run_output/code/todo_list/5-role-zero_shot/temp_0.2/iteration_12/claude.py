
"""
High-quality Todo List Application
Implements a console-based task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        task_name (str): Name/title of the task
        task_description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
        created_at (datetime): Timestamp when task was created
    """
    id: int
    task_name: str
    task_description: str
    is_finished: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external consumption.
        
        Returns:
            dict: Task data in dictionary format
        """
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for when a task is not found."""
    pass


class TaskManager:
    """
    Thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and managing task completion status.
    All operations are thread-safe and include proper validation.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) lookups and a lock for thread safety.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): The task name to validate
            task_description (str): The task description to validate
            
        Raises:
            TaskValidationError: If inputs are invalid
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        
        if not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term parameter.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            TypeError: If search_term is not a string
            TaskValidationError: If search_term is empty
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        if not search_term.strip():
            raise TaskValidationError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (non-empty)
            task_description (str): Description of the task (non-empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If task inputs are invalid
            TypeError: If inputs are not strings
            
        Time Complexity: O(1)
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            self._tasks[task_id] = task
            self._next_id += 1
            
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove (positive integer)
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TaskValidationError: If task_id is invalid
            TypeError: If task_id is not an integer
            
        Time Complexity: O(1)
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring matching on both task name and description.
        
        Args:
            search_term (str): Term to search for (non-empty)
            
        Returns:
            list[dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search_term is invalid
            TypeError: If search_term is not a string
            
        Time Complexity: O(n) where n is the number of tasks
        """
        self._validate_search_term(search_term)
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished (positive integer)
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TaskValidationError: If task_id is invalid
            TypeError: If task_id is not an integer
            
        Time Complexity: O(1)
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            list[dict]: List of all tasks in dictionary format, sorted by ID
            
        Time Complexity: O(n log n) where n is the number of tasks (due to sorting)
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful operation
            
        Time Complexity: O(1)
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
        
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks in the system
            
        Time Complexity: O(1)
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
            
        Time Complexity: O(n) where n is the number of tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to test the TaskManager
    and demonstrates proper usage of all implemented methods.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===\n")
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added task {task1_id}: Buy groceries")
        print(f"Added task {task2_id}: Complete project")
        print(f"Added task {task3_id}: Exercise")
        
        # Display all tasks
        print(f"\nAll tasks ({task_manager.get_task_count()} total):")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display completion statistics
        completed = task_manager.get_completed_count()
        total = task_manager.get_task_count()
        print(f"\nProgress: {completed}/{total} tasks completed")
        
        # Remove a task
        print(f"\nRemoving task {task3_id}...")
        if task_manager.remove(task3_id):
            print("Task removed successfully")
        
        # Final task list
        print(f"\nFinal task list ({task_manager.get_task_count()} tasks):")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (TaskValidationError, TaskNotFoundError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
