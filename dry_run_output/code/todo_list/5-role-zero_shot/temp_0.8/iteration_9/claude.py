
"""
Console-based Todo List Application

A high-quality, maintainable todo list manager implementing ISO/IEC 25010 standards.
Provides functionality to add, remove, search, finish, and manage tasks efficiently.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import threading
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
    is_finished: bool
    created_at: datetime

    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external consumption."""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskManagerError(Exception):
    """Base exception class for TaskManager operations."""
    pass


class TaskNotFoundError(TaskManagerError):
    """Raised when attempting to operate on a non-existent task."""
    pass


class InvalidInputError(TaskManagerError):
    """Raised when invalid input parameters are provided."""
    pass


class TaskManager:
    """
    A thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. All operations
    are thread-safe and include proper input validation.
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety

    def _validate_string_input(self, value: str, field_name: str) -> None:
        """
        Validate string input parameters.
        
        Args:
            value: The string value to validate
            field_name: Name of the field for error messages
            
        Raises:
            InvalidInputError: If value is None, not a string, or empty after stripping
        """
        if value is None:
            raise InvalidInputError(f"{field_name} cannot be None")
        if not isinstance(value, str):
            raise InvalidInputError(f"{field_name} must be a string")
        if not value.strip():
            raise InvalidInputError(f"{field_name} cannot be empty or whitespace")

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id: The task ID to validate
            
        Raises:
            InvalidInputError: If task_id is None, not an integer, or negative
        """
        if task_id is None:
            raise InvalidInputError("Task ID cannot be None")
        if not isinstance(task_id, int):
            raise InvalidInputError("Task ID must be an integer")
        if task_id <= 0:
            raise InvalidInputError("Task ID must be positive")

    def _get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            Task: The task object
            
        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: The name/title of the task
            task_description: Detailed description of the task
            
        Returns:
            int: Unique ID of the newly created task
            
        Raises:
            InvalidInputError: If task_name or task_description are invalid
        """
        # Input validation
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")
        
        with self._lock:
            # Create new task with trimmed inputs
            task = Task(
                id=self._next_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
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
            task_id: The ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            InvalidInputError: If task_id is invalid
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
            task_term: Search term to match against task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            InvalidInputError: If task_term is invalid
        """
        self._validate_string_input(task_term, "Search term")
        
        search_term_lower = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished
            
        Raises:
            InvalidInputError: If task_id is invalid
            TaskNotFoundError: If no task exists with the given ID
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
            return sorted(all_tasks, key=lambda x: x['id'])

    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful operation
        """
        with self._lock:
            self._tasks.clear()
            return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks in the system
        """
        with self._lock:
            return len(self._tasks)

    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of tasks marked as finished
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)

    def get_pending_count(self) -> int:
        """
        Get the number of pending (unfinished) tasks.
        
        Returns:
            int: Number of tasks not yet finished
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to showcase
    the various operations available in the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("Todo List Application - Demo")
    print("=" * 40)
    
    try:
        # Add some sample tasks
        print("Adding sample tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Write report", "Complete the quarterly financial report")
        id3 = task_manager.add("Call dentist", "Schedule appointment for teeth cleaning")
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
        print("\nSearching for 'report':")
        results = task_manager.search("report")
        for task in results:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nTask Statistics:")
        print(f"Total tasks: {task_manager.get_task_count()}")
        print(f"Completed: {task_manager.get_completed_count()}")
        print(f"Pending: {task_manager.get_pending_count()}")
        
        # Remove a task
        print(f"\nRemoving task {id2}...")
        if task_manager.remove(id2):
            print("Task removed successfully")
        
        # Display remaining tasks
        print("\nRemaining tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
            
    except (TaskManagerError, Exception) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
