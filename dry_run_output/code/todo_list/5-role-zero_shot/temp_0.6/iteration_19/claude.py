
"""
Todo List Application
A high-quality, maintainable console-based task management system.

This module implements a TaskManager class that provides comprehensive
task management functionality with proper error handling, validation,
and efficient data operations.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task with all its properties.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Task name/title
        description (str): Detailed task description
        is_finished (bool): Completion status
        created_at (datetime): Task creation timestamp
    """
    id: int
    name: str
    description: str
    is_finished: bool
    created_at: datetime

    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external consumption."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat()
        }


class TaskManagerError(Exception):
    """Base exception class for TaskManager-related errors."""
    pass


class TaskNotFoundError(TaskManagerError):
    """Raised when attempting to access a non-existent task."""
    pass


class InvalidInputError(TaskManagerError):
    """Raised when invalid input parameters are provided."""
    pass


class TaskManager:
    """
    A comprehensive task management system with CRUD operations.
    
    This class provides thread-safe operations for managing tasks including
    adding, removing, searching, marking as complete, and bulk operations.
    All operations are optimized for performance and include proper validation.
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Thread safety for concurrent access

    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): The task name to validate
            
        Raises:
            InvalidInputError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise InvalidInputError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise InvalidInputError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:  # Reasonable length limit
            raise InvalidInputError("Task name cannot exceed 100 characters")

    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            InvalidInputError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise InvalidInputError("Task description must be a string")
        if len(task_description) > 1000:  # Reasonable length limit
            raise InvalidInputError("Task description cannot exceed 1000 characters")

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            InvalidInputError: If task ID is invalid
            TaskNotFoundError: If task ID doesn't exist
        """
        if not isinstance(task_id, int):
            raise InvalidInputError("Task ID must be an integer")
        if task_id <= 0:
            raise InvalidInputError("Task ID must be a positive integer")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            InvalidInputError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise InvalidInputError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise InvalidInputError("Search term cannot be empty or whitespace only")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): The name/title of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            InvalidInputError: If input parameters are invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            task_id = self._next_id
            task = Task(
                id=task_id,
                name=task_name.strip(),
                description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            self._tasks[task_id] = task
            self._next_id += 1
            
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            InvalidInputError: If task ID is invalid
            TaskNotFoundError: If task doesn't exist
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Description")
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
        
        Args:
            search_term (str): The term to search for (case-insensitive)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            InvalidInputError: If search term is invalid
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("milk")
            >>> len(results)
            1
        """
        self._validate_search_term(search_term)
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by creation date for consistent results
        matching_tasks.sort(key=lambda x: x['created_at'])
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished
            
        Raises:
            InvalidInputError: If task ID is invalid
            TaskNotFoundError: If task doesn't exist
            
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
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by creation date
            
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
        
        # Sort by creation date for consistent ordering
        all_tasks.sort(key=lambda x: x['created_at'])
        return all_tasks

    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            bool: True if all tasks were successfully cleared
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
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

    def get_pending_count(self) -> int:
        """
        Get the number of pending (incomplete) tasks.
        
        Returns:
            int: Number of pending tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function showcases all the main features of the TaskManager
    with proper error handling and user-friendly output.
    """
    print("=== Todo List Application Demo ===\n")
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the quarterly report and submit it")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute jog in the park")
        
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
        
        # Display statistics
        print(f"\nTask Statistics:")
        print(f"  Total: {task_manager.get_task_count()}")
        print(f"  Completed: {task_manager.get_completed_count()}")
        print(f"  Pending: {task_manager.get_pending_count()}")
        
        # Remove a task
        print(f"\nRemoving task {task2_id}...")
        task_manager.remove(task2_id)
        
        print(f"\nRemaining tasks ({task_manager.get_task_count()} total):")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (TaskManagerError, Exception) as e:
        print(f"Error: {e}")
    
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    main()
