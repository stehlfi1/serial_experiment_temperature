
"""
Todo List Application - Console-based Task Manager

A high-quality, maintainable Python application for managing todo tasks
that adheres to ISO/IEC 25010 standard for software quality.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a single task.
    
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
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external consumption."""
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
    High-performance task manager for console-based todo list application.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. It uses
    efficient data structures and includes comprehensive error handling.
    
    Thread-safe operations are ensured through the use of threading locks.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) average-case lookups and a counter
        for generating unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): The name of the task
            task_description (str): The description of the task
            
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
            task_id (int): The ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is not positive
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term parameter.
        
        Args:
            search_term (str): The term to validate
            
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
        Add a new task to the task manager.
        
        Args:
            task_name (str): Name of the task (cannot be empty)
            task_description (str): Description of the task (cannot be empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If task_name or task_description are invalid
            TypeError: If parameters are not strings
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Buy milk, bread, and eggs")
            >>> print(task_id)
            1
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
        Remove a task by its ID.
        
        Args:
            task_id (int): ID of the task to remove (must be positive)
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TaskValidationError: If task_id is not positive
            TypeError: If task_id is not an integer
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
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
        
        Performs case-insensitive substring matching on both task name
        and description fields.
        
        Args:
            search_term (str): Term to search for (cannot be empty)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search_term is empty or whitespace
            TypeError: If search_term is not a string
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Buy milk and bread")
            >>> results = tm.search("milk")
            >>> len(results)
            1
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
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished,
                  False if task not found
            
        Raises:
            TaskValidationError: If task_id is not positive
            TypeError: If task_id is not an integer
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
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
            List[Dict]: List of all tasks in dictionary format,
                       sorted by task ID
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> len(all_tasks)
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            bool: Always returns True to indicate successful clearing
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> success = tm.clear_all()
            >>> print(success)
            True
            >>> len(tm.get_all())
            0
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
        
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks in the manager
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Main function demonstrating the TaskManager usage.
    
    This function provides a simple console interface for testing
    the TaskManager functionality.
    """
    task_manager = TaskManager()
    
    print("Todo List Application")
    print("====================")
    
    try:
        # Demonstrate adding tasks
        task1_id = task_manager.add("Buy groceries", "Buy milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the final report for the client")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {task1_id}, {task2_id}, {task3_id}")
        
        # Demonstrate getting all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate finishing a task
        task_manager.finish(task1_id)
        print(f"\nMarked task {task1_id} as completed")
        
        # Demonstrate searching
        search_results = task_manager.search("project")
        print(f"\nSearch results for 'project': {len(search_results)} found")
        for task in search_results:
            print(f"  [{task['id']}] {task['task_name']}")
        
        # Show statistics
        print(f"\nStatistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed tasks: {task_manager.get_completed_count()}")
        
    except (TaskValidationError, TaskNotFoundError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
