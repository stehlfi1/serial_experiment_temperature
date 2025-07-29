
"""
Console-based Todo List Application

A high-quality, maintainable todo list application implementing the ISO/IEC 25010 
standard for software quality. Provides efficient task management with comprehensive 
error handling and validation.

Author: Senior Software Developer
Version: 1.0.0
"""

from typing import Dict, List, Optional
import threading
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Enumeration for task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """
    Data class representing a task with all its attributes.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Name/title of the task
        description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
    """
    id: int
    name: str
    description: str
    is_finished: bool = False
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external representation.
        
        Returns:
            Dict: Task data in dictionary format
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskValidationError(Exception):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(Exception):
    """Custom exception for task not found errors."""
    pass


class TaskManager:
    """
    High-performance task manager for todo list operations.
    
    Implements efficient in-memory storage with O(1) lookups and thread-safe operations.
    Provides comprehensive validation and error handling following ISO/IEC 25010 standards.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses dictionary for O(1) task lookups and maintains thread safety.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): Task name to validate
            task_description (str): Task description to validate
            
        Raises:
            TaskValidationError: If validation fails
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        
        if not task_description or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve task by ID with validation.
        
        Args:
            task_id (int): ID of the task to retrieve
            
        Returns:
            Task: The requested task
            
        Raises:
            TaskNotFoundError: If task with given ID doesn't exist
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (non-empty)
            task_description (str): Description of the task (non-empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If task name or description is invalid
            TypeError: If inputs are not strings
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            task = Task(
                id=task_id,
                name=task_name.strip(),
                description=task_description.strip()
            )
            
            self._tasks[task_id] = task
            
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove (positive integer)
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring search across task names and descriptions.
        
        Args:
            task_term (str): Search term to look for
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or whitespace only
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        search_term = task_term.strip()
        if not search_term:
            raise ValueError("Search term cannot be empty or whitespace only")
        
        search_term_lower = search_term.lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
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
            bool: True if task was successfully marked as finished
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            TaskNotFoundError: If task with given ID doesn't exist
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            task = self._get_task_by_id(task_id)
            task.is_finished = True
            return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
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
            bool: True indicating successful clearing of all tasks
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
        
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks currently in the system
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
    
    def get_pending_count(self) -> int:
        """
        Get the number of pending tasks.
        
        Returns:
            int: Number of pending tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    Shows basic usage patterns and error handling capabilities.
    """
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Write report", "Complete the quarterly sales report")
        task3_id = task_manager.add("Call dentist", "Schedule appointment for teeth cleaning")
        
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
        print("\nSearching for 'report':")
        search_results = task_manager.search("report")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nStatistics:")
        print(f"Total tasks: {task_manager.get_task_count()}")
        print(f"Completed: {task_manager.get_completed_count()}")
        print(f"Pending: {task_manager.get_pending_count()}")
        
    except (TaskValidationError, TaskNotFoundError, TypeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
