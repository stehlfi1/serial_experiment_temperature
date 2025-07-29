
"""
High-Quality Todo List Application

A console-based todo list application implementing the TaskManager class
with full CRUD operations, following ISO/IEC 25010 quality standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a task with all its attributes.
    
    Attributes:
        id: Unique identifier for the task
        task_name: Name/title of the task
        task_description: Detailed description of the task
        is_finished: Boolean indicating if task is completed
        created_at: Timestamp when task was created
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
        """Convert task to dictionary format for external use."""
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
    """Raised when a task with specified ID is not found."""
    pass


class InvalidInputError(TaskManagerError):
    """Raised when invalid input is provided."""
    pass


class TaskManager:
    """
    A thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. All operations
    are thread-safe and include proper input validation.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) task lookup by ID and maintains
        a counter for generating unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_string_input(self, value: str, field_name: str) -> None:
        """
        Validate string input for non-empty content.
        
        Args:
            value: String value to validate
            field_name: Name of the field being validated
            
        Raises:
            InvalidInputError: If value is None, empty, or only whitespace
        """
        if not isinstance(value, str):
            raise InvalidInputError(f"{field_name} must be a string")
        if not value or not value.strip():
            raise InvalidInputError(f"{field_name} cannot be empty or whitespace")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id: Task ID to validate
            
        Raises:
            InvalidInputError: If task_id is not a positive integer
        """
        if not isinstance(task_id, int):
            raise InvalidInputError("Task ID must be an integer")
        if task_id <= 0:
            raise InvalidInputError("Task ID must be a positive integer")
    
    def _get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve task by ID with validation.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task object with the specified ID
            
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
            task_name: Name/title of the task (cannot be empty)
            task_description: Detailed description of the task (cannot be empty)
            
        Returns:
            int: Unique ID assigned to the new task
            
        Raises:
            InvalidInputError: If task_name or task_description is empty/invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")
        
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
        Remove a task from the todo list by its ID.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            InvalidInputError: If task_id is invalid
            
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
        
        Performs case-insensitive search across both task name and description.
        
        Args:
            search_term: Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            InvalidInputError: If search_term is empty or invalid
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("milk")
            >>> print(len(results))
            1
        """
        self._validate_string_input(search_term, "Search term")
        
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
            InvalidInputError: If task_id is invalid
            TaskNotFoundError: If task with given ID doesn't exist
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
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
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> print(len(all_tasks))
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully cleared
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> success = tm.clear_all()
            >>> print(success)
            True
            >>> print(len(tm.get_all()))
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
            int: Total number of tasks in the system
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
    
    This function provides a simple console interface to test
    all the TaskManager operations.
    """
    print("=== Todo List Application Demo ===\n")
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding sample tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the final report and presentation")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {task1_id}, {task2_id}, {task3_id}\n")
        
        # Display all tasks
        print("All tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Mark a task as finished
        print(f"Marking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("Searching for tasks containing 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Display updated task list
        print("Updated task list:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Show statistics
        total_tasks = task_manager.get_task_count()
        completed_tasks = task_manager.get_completed_count()
        print(f"Statistics: {completed_tasks}/{total_tasks} tasks completed")
        
        # Remove a task
        print(f"\nRemoving task {task2_id}...")
        removed = task_manager.remove(task2_id)
        print(f"Task removal {'successful' if removed else 'failed'}")
        
        # Final task list
        print("\nFinal task list:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (TaskManagerError, Exception) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
