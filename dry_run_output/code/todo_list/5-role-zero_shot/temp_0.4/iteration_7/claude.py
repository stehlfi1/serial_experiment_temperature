
"""
Todo List Application

A console-based todo list application implementing the TaskManager class
with comprehensive task management functionality following ISO/IEC 25010 standards.
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


class TaskManager:
    """
    A thread-safe task management system for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. All operations
    are optimized for performance and include proper error handling.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage and thread safety."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name/title of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace
            TypeError: If task_name or task_description is not a string
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("task_name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("task_description must be a string")
        
        # Check for empty or whitespace-only strings
        if not task_name.strip():
            raise ValueError("task_name cannot be empty or contain only whitespace")
        if not task_description.strip():
            raise ValueError("task_description cannot be empty or contain only whitespace")
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            # Create new task
            new_task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            
            # Store task using ID as key for O(1) lookup
            self._tasks[task_id] = new_task
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if task_id < 0:
            raise ValueError("task_id must be non-negative")
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Args:
            task_term (str): Search term to match against task names and descriptions
            
        Returns:
            List[Dict]: List of dictionaries containing matching task information
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("task_term must be a string")
        if not task_term.strip():
            raise ValueError("task_term cannot be empty or contain only whitespace")
        
        search_term = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term in task.task_name.lower() or 
                    search_term in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
        # Sort by creation time for consistent ordering
        matching_tasks.sort(key=lambda x: x['id'])
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if task_id < 0:
            raise ValueError("task_id must be non-negative")
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of dictionaries containing all task information,
                       sorted by task ID
        """
        with self._lock:
            all_tasks = [self._task_to_dict(task) for task in self._tasks.values()]
            # Sort by ID for consistent ordering
            all_tasks.sort(key=lambda x: x['id'])
            return all_tasks
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful clearing
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to dictionary format for external consumption.
        
        Args:
            task (Task): Task object to convert
            
        Returns:
            Dict: Dictionary containing task information in the required format
        """
        return {
            'id': task.id,
            'task_name': task.task_name,
            'task_description': task.task_description,
            'is_finished': task.is_finished
        }
    
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
    Main function demonstrating the TaskManager functionality.
    
    This function provides a simple console interface for testing
    the TaskManager class capabilities.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===\n")
    
    try:
        # Demonstrate adding tasks
        print("Adding tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Complete project", "Finish the Python todo list application")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}\n")
        
        # Demonstrate getting all tasks
        print("All tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Demonstrate finishing a task
        print(f"Marking task {id1} as finished...")
        task_manager.finish(id1)
        
        # Demonstrate searching
        print("Searching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Show statistics
        print("Statistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed: {task_manager.get_completed_count()}")
        print(f"  Pending: {task_manager.get_pending_count()}")
        print()
        
        # Demonstrate removing a task
        print(f"Removing task {id2}...")
        removed = task_manager.remove(id2)
        print(f"Task removed: {removed}\n")
        
        # Show final state
        print("Final task list:")
        final_tasks = task_manager.get_all()
        for task in final_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
