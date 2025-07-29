
"""
A high-quality console-based todo list application implementing ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with full CRUD operations,
validation, and error handling.
"""

from typing import List, Dict, Optional
import threading
from datetime import datetime


class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID is not found."""
    pass


class InvalidTaskDataError(Exception):
    """Raised when invalid task data is provided."""
    pass


class Task:
    """
    Represents a single task with all its properties.
    
    This class encapsulates task data and provides a clean interface
    for task operations while maintaining data integrity.
    """
    
    def __init__(self, task_id: int, name: str, description: str):
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name (must not be empty)
            description: Task description (must not be empty)
            
        Raises:
            InvalidTaskDataError: If name or description is empty
        """
        if not name or not name.strip():
            raise InvalidTaskDataError("Task name cannot be empty")
        if not description or not description.strip():
            raise InvalidTaskDataError("Task description cannot be empty")
            
        self._id = task_id
        self._name = name.strip()
        self._description = description.strip()
        self._is_finished = False
        self._created_at = datetime.now()
    
    @property
    def id(self) -> int:
        """Get task ID."""
        return self._id
    
    @property
    def name(self) -> str:
        """Get task name."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get task description."""
        return self._description
    
    @property
    def is_finished(self) -> bool:
        """Get task completion status."""
        return self._is_finished
    
    def mark_finished(self) -> None:
        """Mark the task as completed."""
        self._is_finished = True
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format.
        
        Returns:
            Dictionary containing task information in the specified format
        """
        return {
            'id': self._id,
            'task_name': self._name,
            'task_description': self._description,
            'is_finished': self._is_finished
        }
    
    def matches_search_term(self, search_term: str) -> bool:
        """
        Check if task matches the search term.
        
        Args:
            search_term: Term to search for in name or description
            
        Returns:
            True if task matches the search term, False otherwise
        """
        if not search_term:
            return False
            
        search_term_lower = search_term.lower().strip()
        return (search_term_lower in self._name.lower() or 
                search_term_lower in self._description.lower())


class TaskManager:
    """
    A thread-safe task manager for handling todo list operations.
    
    This class provides a complete interface for managing tasks with
    efficient operations, proper validation, and comprehensive error handling.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name of the task (must not be empty)
            task_description: Description of the task (must not be empty)
            
        Returns:
            Unique ID of the created task
            
        Raises:
            InvalidTaskDataError: If task_name or task_description is empty
            TypeError: If arguments are not strings
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        
        with self._lock:
            task_id = self._next_id
            task = Task(task_id, task_name, task_description)
            self._tasks[task_id] = task
            self._next_id += 1
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
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
        
        Args:
            task_term: Search term to look for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
        
        with self._lock:
            matching_tasks = []
            for task in self._tasks.values():
                if task.matches_search_term(task_term):
                    matching_tasks.append(task.to_dict())
            
            # Sort by task ID for consistent results
            return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].mark_finished()
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List of dictionaries containing all task information, sorted by ID
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            True indicating successful clearing of all tasks
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id: Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id < 0:
            raise ValueError("Task ID cannot be negative")
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            Number of tasks currently stored
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            Number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function shows basic usage of the TaskManager class
    and can serve as a simple console interface.
    """
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Complete project", "Finish the Python todo list application")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
        
        # Display all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\nMarking task {id1} as finished...")
        task_manager.finish(id1)
        
        # Search for tasks
        print("\nSearching for 'project':")
        results = task_manager.search("project")
        for task in results:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nStatistics:")
        print(f"Total tasks: {task_manager.get_task_count()}")
        print(f"Completed tasks: {task_manager.get_completed_count()}")
        
    except (InvalidTaskDataError, TaskNotFoundError, TypeError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
