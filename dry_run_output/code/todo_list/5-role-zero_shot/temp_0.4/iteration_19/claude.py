
"""
High-Quality Todo List Application

A console-based todo list application implementing ISO/IEC 25010 quality standards.
Provides comprehensive task management functionality with robust error handling
and efficient data operations.
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
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external consumption.
        
        Returns:
            Dict: Task data in dictionary format
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
    High-performance task management system with comprehensive CRUD operations.
    
    This class provides thread-safe operations for managing todo tasks with
    efficient lookup, insertion, and deletion capabilities. Implements
    ISO/IEC 25010 quality characteristics including reliability, performance,
    and maintainability.
    
    Attributes:
        _tasks (Dict[int, Task]): Internal storage for tasks using hash map
        _next_id (int): Counter for generating unique task IDs
        _lock (threading.RLock): Thread safety lock for concurrent operations
    """
    
    def __init__(self):
        """
        Initialize TaskManager with empty task storage.
        
        Uses dictionary for O(1) average case lookup performance and
        reentrant lock for thread safety.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): Task name to validate
            task_description (str): Task description to validate
            
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
        
        if len(task_name.strip()) > 100:
            raise TaskValidationError("Task name cannot exceed 100 characters")
        
        if len(task_description.strip()) > 500:
            raise TaskValidationError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            TaskNotFoundError: If task doesn't exist
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (1-100 characters, non-empty)
            task_description (str): Description of the task (1-500 characters, non-empty)
            
        Returns:
            int: Unique ID assigned to the created task
            
        Raises:
            TypeError: If parameters are not strings
            TaskValidationError: If task name or description are invalid
            
        Time Complexity: O(1) average case
        Space Complexity: O(1)
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
            task_id (int): Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Args:
            search_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or whitespace only
            
        Time Complexity: O(n) where n is the number of tasks
        Space Complexity: O(k) where k is the number of matching tasks
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        search_term = search_term.strip()
        if not search_term:
            raise ValueError("Search term cannot be empty or whitespace only")
        
        search_term_lower = search_term.lower()
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
            task_id (int): Unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            TaskNotFoundError: If task with given ID doesn't exist
            
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            self._tasks[task_id].is_finished = True
            
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Time Complexity: O(n log n) where n is the number of tasks (due to sorting)
        Space Complexity: O(n) where n is the number of tasks
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
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1
            
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
    
    This function provides a simple console interface to interact with
    the TaskManager and demonstrates all available operations.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("High-quality task management system\n")
    
    try:
        # Demonstrate adding tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Purchase milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo application with full documentation")
        task3_id = task_manager.add("Exercise", "30-minute workout at the gym")
        
        print(f"Added task {task1_id}: Buy groceries")
        print(f"Added task {task2_id}: Complete project")
        print(f"Added task {task3_id}: Exercise")
        
        # Demonstrate getting all tasks
        print(f"\nAll tasks ({task_manager.get_task_count()} total):")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate finishing a task
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Demonstrate search functionality
        print("\nSearching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Show completion statistics
        completed = task_manager.get_completed_count()
        total = task_manager.get_task_count()
        print(f"\nProgress: {completed}/{total} tasks completed")
        
        # Demonstrate removal
        print(f"\nRemoving task {task3_id}...")
        if task_manager.remove(task3_id):
            print("Task removed successfully")
        
        print(f"\nFinal task list ({task_manager.get_task_count()} tasks):")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
            
    except (TaskValidationError, TaskNotFoundError, TypeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
