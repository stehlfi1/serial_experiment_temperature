
"""
Todo List Application - A console-based task management system.

This module implements a TaskManager class that provides comprehensive
task management functionality following ISO/IEC 25010 standards.
"""

from typing import Dict, List, Optional
import threading
from datetime import datetime


class Task:
    """
    Represents a single task with its properties.
    
    This class encapsulates task data and provides a clean interface
    for task manipulation while ensuring data integrity.
    """
    
    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name
            description: Task description
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False
        self.created_at = datetime.now()
        self.finished_at: Optional[datetime] = None
    
    def mark_finished(self) -> None:
        """Mark the task as completed."""
        self.is_finished = True
        self.finished_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary representation.
        
        Returns:
            Dictionary containing task information
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat(),
            'finished_at': self.finished_at.isoformat() if self.finished_at else None
        }


class TaskManager:
    """
    Manages todo list operations with thread-safe implementation.
    
    This class provides a complete task management system with efficient
    data structures and comprehensive error handling.
    """
    
    def __init__(self) -> None:
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
            ValueError: If task name is invalid
            TypeError: If task name is not a string
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:  # Reasonable limit
            raise ValueError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description: The task description to validate
            
        Raises:
            ValueError: If task description is invalid
            TypeError: If task description is not a string
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace only")
        if len(task_description.strip()) > 500:  # Reasonable limit
            raise ValueError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id: The task ID to validate
            
        Raises:
            TypeError: If task ID is not an integer
            ValueError: If task ID is invalid
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term: The search term to validate
            
        Raises:
            TypeError: If search term is not a string
            ValueError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name of the task
            task_description: Description of the task
            
        Returns:
            Unique ID of the created task
            
        Raises:
            ValueError: If task name or description is invalid
            TypeError: If inputs are not strings
        """
        # Validate inputs
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Clean the inputs
            clean_name = task_name.strip()
            clean_description = task_description.strip()
            
            # Create new task
            task_id = self._next_id
            new_task = Task(task_id, clean_name, clean_description)
            
            # Store task and increment ID counter
            self._tasks[task_id] = new_task
            self._next_id += 1
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was removed successfully, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is invalid
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
            search_term: Term to search for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is invalid
        """
        self._validate_search_term(search_term)
        
        with self._lock:
            clean_term = search_term.strip().lower()
            matching_tasks = []
            
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (clean_term in task.name.lower() or 
                    clean_term in task.description.lower()):
                    matching_tasks.append(task.to_dict())
            
            # Sort by creation time for consistent results
            matching_tasks.sort(key=lambda x: x['created_at'])
            return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is invalid
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
            List of dictionaries containing all task information,
            sorted by creation time
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            # Sort by creation time for consistent ordering
            all_tasks.sort(key=lambda x: x['created_at'])
            return all_tasks
    
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
            Number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to test
    the TaskManager operations.
    """
    task_manager = TaskManager()
    
    print("Todo List Application")
    print("=" * 50)
    
    try:
        # Demonstrate adding tasks
        print("\n1. Adding tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Write report", "Complete the quarterly sales report")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
        
        # Demonstrate getting all tasks
        print("\n2. All tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate searching
        print("\n3. Searching for 'report':")
        search_results = task_manager.search("report")
        for task in search_results:
            print(f"  Found: [{task['id']}] {task['task_name']}")
        
        # Demonstrate finishing a task
        print(f"\n4. Marking task {id2} as finished...")
        task_manager.finish(id2)
        
        # Show updated status
        print("\n5. Updated tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}")
        
        # Demonstrate task statistics
        print(f"\n6. Statistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed: {task_manager.get_completed_count()}")
        
        # Demonstrate removing a task
        print(f"\n7. Removing task {id1}...")
        removed = task_manager.remove(id1)
        print(f"  Removal successful: {removed}")
        
        # Final state
        print("\n8. Final task list:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
