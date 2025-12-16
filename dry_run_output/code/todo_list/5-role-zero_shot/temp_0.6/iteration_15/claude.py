
"""
High-quality console-based todo list application following ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with full CRUD operations,
input validation, and efficient data handling.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task with all its properties.
    
    Attributes:
        id: Unique identifier for the task
        task_name: Name/title of the task
        task_description: Detailed description of the task
        is_finished: Completion status of the task
        created_at: Timestamp when the task was created
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
    """Custom exception for task not found errors."""
    pass


class TaskManager:
    """
    A thread-safe task manager for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and updating tasks with proper validation
    and error handling.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name: The task name to validate
            
        Raises:
            TaskValidationError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise TaskValidationError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:
            raise TaskValidationError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description: The task description to validate
            
        Raises:
            TaskValidationError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise TaskValidationError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
        if len(task_description.strip()) > 500:
            raise TaskValidationError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id: The task ID to validate
            
        Raises:
            TaskValidationError: If task ID is invalid
            TaskNotFoundError: If task ID doesn't exist
        """
        if not isinstance(task_id, int):
            raise TaskValidationError("Task ID must be an integer")
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term: The search term to validate
            
        Raises:
            TaskValidationError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise TaskValidationError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise TaskValidationError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name of the task (1-100 characters)
            task_description: Description of the task (1-500 characters)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If input parameters are invalid
        """
        # Validate inputs
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Create new task with sanitized inputs
            task = Task(
                id=self._next_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            
            # Store task and increment ID counter
            self._tasks[self._next_id] = task
            task_id = self._next_id
            self._next_id += 1
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            del self._tasks[task_id]
            return True
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term: Term to search for (case-insensitive)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search_term is invalid
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
            task_id: ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            self._tasks[task_id].is_finished = True
            return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks
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
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to interact with
    the TaskManager for testing and demonstration purposes.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Manager Demo ===\n")
    
    try:
        # Add some sample tasks
        print("Adding sample tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Complete project", "Finish the Python todo list application")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}\n")
        
        # Display all tasks
        print("All tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Mark a task as finished
        print(f"Marking task {id1} as finished...")
        task_manager.finish(id1)
        
        # Search for tasks
        print("Searching for 'project':")
        results = task_manager.search("project")
        for task in results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Display statistics
        total = task_manager.get_task_count()
        completed = task_manager.get_completed_count()
        print(f"Statistics: {completed}/{total} tasks completed")
        
        # Remove a task
        print(f"\nRemoving task {id2}...")
        task_manager.remove(id2)
        
        # Display final state
        print("\nFinal task list:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (TaskValidationError, TaskNotFoundError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
