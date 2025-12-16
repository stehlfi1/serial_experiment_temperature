
"""
High-quality console-based todo list application implementing ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with full CRUD operations,
input validation, and efficient data handling.
"""

from typing import List, Dict, Optional
import threading
from datetime import datetime


class Task:
    """
    Represents a single todo task with all its properties.
    
    This class encapsulates task data and provides a clean interface
    for task manipulation while ensuring data integrity.
    """
    
    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name (must be non-empty)
            description: Task description (must be non-empty)
            
        Raises:
            ValueError: If name or description is empty
        """
        if not name or not name.strip():
            raise ValueError("Task name cannot be empty")
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
            
        self._id = task_id
        self._name = name.strip()
        self._description = description.strip()
        self._is_finished = False
        self._created_at = datetime.now()
        self._completed_at: Optional[datetime] = None
    
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
        if not self._is_finished:
            self._is_finished = True
            self._completed_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary representation.
        
        Returns:
            Dictionary containing task information in the required format
        """
        return {
            'id': self._id,
            'task_name': self._name,
            'task_description': self._description,
            'is_finished': self._is_finished
        }
    
    def matches_search_term(self, search_term: str) -> bool:
        """
        Check if task matches the given search term.
        
        Args:
            search_term: Term to search for in name or description
            
        Returns:
            True if task matches search term, False otherwise
        """
        if not search_term:
            return False
        
        search_lower = search_term.lower().strip()
        return (search_lower in self._name.lower() or 
                search_lower in self._description.lower())


class TaskManager:
    """
    High-performance task manager implementing efficient todo list operations.
    
    This class provides thread-safe operations for managing tasks with
    optimized data structures for fast lookups and operations.
    
    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects for O(1) lookups
        _next_id: Counter for generating unique task IDs
        _lock: Thread lock for ensuring thread safety
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name of the task (must be non-empty string)
            task_description: Description of the task (must be non-empty string)
            
        Returns:
            Unique ID of the created task
            
        Raises:
            TypeError: If task_name or task_description is not a string
            ValueError: If task_name or task_description is empty
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        
        with self._lock:
            try:
                task = Task(self._next_id, task_name, task_description)
                self._tasks[self._next_id] = task
                task_id = self._next_id
                self._next_id += 1
                return task_id
            except ValueError as e:
                # Re-raise validation errors from Task constructor
                raise e
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id < 0:
            raise ValueError("Task ID must be non-negative")
        
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
            List of dictionaries containing matching task information
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty
            
        Time Complexity: O(n) where n is the number of tasks
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty")
        
        with self._lock:
            matching_tasks = []
            for task in self._tasks.values():
                if task.matches_search_term(task_term):
                    matching_tasks.append(task.to_dict())
            
            # Sort by ID for consistent ordering
            matching_tasks.sort(key=lambda x: x['id'])
            return matching_tasks
    
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
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id < 0:
            raise ValueError("Task ID must be non-negative")
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].mark_finished()
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List of dictionaries containing all task information,
            sorted by task ID for consistent ordering
            
        Time Complexity: O(n log n) where n is the number of tasks
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            # Sort by ID for consistent ordering
            all_tasks.sort(key=lambda x: x['id'])
            return all_tasks
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            True indicating successful clearing of all tasks
            
        Time Complexity: O(1)
        """
        with self._lock:
            self._tasks.clear()
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            Number of tasks currently stored
            
        Time Complexity: O(1)
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            Number of completed tasks
            
        Time Complexity: O(n) where n is the number of tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main() -> None:
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to demonstrate
    the various operations supported by the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===\n")
    
    try:
        # Demonstrate adding tasks
        print("Adding tasks...")
        id1 = task_manager.add("Buy groceries", "Purchase milk, bread, and eggs")
        id2 = task_manager.add("Write report", "Complete quarterly sales report")
        id3 = task_manager.add("Exercise", "30-minute morning workout")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
        
        # Demonstrate getting all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate finishing a task
        print(f"\nMarking task {id1} as finished...")
        task_manager.finish(id1)
        
        # Demonstrate searching
        print("\nSearching for 'report':")
        search_results = task_manager.search("report")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Show final state
        print(f"\nFinal state - Total tasks: {task_manager.get_task_count()}, "
              f"Completed: {task_manager.get_completed_count()}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
