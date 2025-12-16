
"""
High-quality Todo List Application following ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with
full CRUD operations, search functionality, and proper error handling.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class Task:
    """
    Represents a single todo task.
    
    Attributes:
        id: Unique identifier for the task
        name: Task name/title
        description: Detailed task description
        is_finished: Completion status
        created_at: Task creation timestamp
    """
    id: int
    name: str
    description: str
    is_finished: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external consumption."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat()
        }


class TaskValidationError(ValueError):
    """Raised when task validation fails."""
    pass


class TaskNotFoundError(KeyError):
    """Raised when a task with specified ID is not found."""
    pass


class TaskManager:
    """
    Thread-safe task manager for todo list operations.
    
    Provides comprehensive task management with validation, error handling,
    and efficient operations following ISO/IEC 25010 quality standards.
    """
    
    def __init__(self) -> None:
        """Initialize TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name: Task name to validate
            task_description: Task description to validate
            
        Raises:
            TaskValidationError: If validation fails
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
            task_id: Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be positive")
    
    def _get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve task by ID with validation.
        
        Args:
            task_id: ID of task to retrieve
            
        Returns:
            Task object
            
        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return self._tasks[task_id]
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name/title of the task
            task_description: Detailed description of the task
            
        Returns:
            Unique ID of the created task
            
        Raises:
            TypeError: If inputs are not strings
            TaskValidationError: If inputs are empty or invalid
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
            task_id: ID of task to remove
            
        Returns:
            True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
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
        
        Performs case-insensitive substring search across task names and descriptions.
        
        Args:
            search_term: Term to search for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching tasks
            
        Raises:
            TypeError: If search_term is not a string
            TaskValidationError: If search_term is empty
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        search_term = search_term.strip()
        if not search_term:
            raise TaskValidationError("Search term cannot be empty or whitespace only")
        
        search_term_lower = search_term.lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of task to mark as finished
            
        Returns:
            True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            try:
                task = self._get_task_by_id(task_id)
                task.is_finished = True
                return True
            except TaskNotFoundError:
                return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List of dictionaries containing all tasks, sorted by ID
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
            self._next_id = 1
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            Total number of tasks in the system
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            Number of tasks marked as finished
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of TaskManager functionality.
    
    This function showcases the basic usage of the TaskManager class
    and can serve as a simple console interface.
    """
    task_manager = TaskManager()
    
    print("Todo List Manager Demo")
    print("=" * 30)
    
    try:
        # Add some sample tasks
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Complete project", "Finish the Python todo list application")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
        
        # Display all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        task_manager.finish(id1)
        print(f"\nMarked task {id1} as finished")
        
        # Search for tasks
        search_results = task_manager.search("project")
        print(f"\nSearch results for 'project': {len(search_results)} found")
        for task in search_results:
            print(f"  [{task['id']}] {task['task_name']}")
        
        # Display statistics
        print(f"\nStatistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed: {task_manager.get_completed_count()}")
        
    except (TaskValidationError, TaskNotFoundError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
