
"""
Console-based Todo List Application

This module implements a task management system that allows users to add, remove,
search, finish, and manage todo tasks efficiently.

Author: Senior Software Developer
Standards: ISO/IEC 25010 compliant
"""

from typing import List, Dict, Optional
import re


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
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages todo tasks with CRUD operations and search functionality.
    
    This class provides a complete interface for managing tasks while
    ensuring data consistency, performance, and error handling.
    """
    
    def __init__(self) -> None:
        """Initialize the task manager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: Name of the task (must not be empty)
            task_description: Description of the task (must not be empty)
            
        Returns:
            Unique ID of the created task
            
        Raises:
            ValueError: If task_name or task_description is empty or whitespace-only
            TypeError: If arguments are not strings
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        
        # Check for empty or whitespace-only strings
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace-only")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace-only")
        
        # Create and store the task
        task_id = self._next_id
        task = Task(task_id, task_name.strip(), task_description.strip())
        self._tasks[task_id] = task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Attempt to remove the task
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring search in both task name
        and description fields.
        
        Args:
            search_term: Term to search for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or whitespace-only
        """
        # Input validation
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty or whitespace-only")
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        # Search through all tasks
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
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was successfully marked as finished, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be positive")
        
        # Attempt to finish the task
        if task_id in self._tasks:
            self._tasks[task_id].is_finished = True
            return True
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.
        
        Returns:
            List of dictionaries containing all task information,
            sorted by task ID
        """
        return sorted([task.to_dict() for task in self._tasks.values()], 
                     key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            True indicating successful clearing of all tasks
        """
        self._tasks.clear()
        self._next_id = 1
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            Number of tasks currently stored
        """
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            Number of tasks marked as finished
        """
        return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Main function demonstrating the TaskManager functionality.
    
    This function provides a simple console interface for testing
    the task management system.
    """
    task_manager = TaskManager()
    
    print("Todo List Application")
    print("====================")
    
    # Demonstration of functionality
    try:
        # Add some tasks
        id1 = task_manager.add("Buy groceries", "Buy milk, bread, and eggs from the store")
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
        total = task_manager.get_task_count()
        completed = task_manager.get_completed_count()
        print(f"\nStatistics: {completed}/{total} tasks completed")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
