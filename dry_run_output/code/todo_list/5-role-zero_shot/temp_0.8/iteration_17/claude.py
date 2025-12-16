
"""
High-quality console-based todo list application implementing ISO/IEC 25010 standards.

This module provides a TaskManager class for managing tasks with full CRUD operations,
input validation, and efficient data handling.
"""

from typing import List, Dict, Optional
import threading
from datetime import datetime


class TaskManager:
    """
    A thread-safe task management system for console-based todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks with proper
    validation and error handling.
    
    Attributes:
        _tasks (Dict[int, Dict]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
        _lock (threading.RLock): Thread lock for concurrent access safety
    """
    
    def __init__(self) -> None:
        """
        Initialize the TaskManager with empty task storage.
        
        Creates an empty task dictionary, initializes ID counter, and sets up
        thread safety mechanisms.
        """
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()
    
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
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        # Input validation
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or contain only whitespace")
        
        if not task_description.strip():
            raise ValueError("Task description cannot be empty or contain only whitespace")
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            # Create task with normalized strings and metadata
            self._tasks[task_id] = {
                'id': task_id,
                'task_name': task_name.strip(),
                'task_description': task_description.strip(),
                'is_finished': False,
                'created_at': datetime.now(),
                'completed_at': None
            }
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
        """
        # Input validation
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
            search_term (str): The term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks with format (id, task_name, task_description, is_finished)
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or contains only whitespace
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("milk")
            >>> print(len(results))
            1
        """
        # Input validation
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        if not search_term.strip():
            raise ValueError("Search term cannot be empty or contain only whitespace")
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term_lower in task['task_name'].lower() or 
                    search_term_lower in task['task_description'].lower()):
                    matching_tasks.append(self._format_task_output(task))
        
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to complete
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            List[Dict]: List of all tasks with format (id, task_name, task_description, is_finished)
            Tasks are sorted by ID for consistent ordering.
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> print(len(all_tasks))
            2
        """
        with self._lock:
            # Return tasks sorted by ID for consistent ordering
            return [self._format_task_output(task) 
                   for task in sorted(self._tasks.values(), key=lambda x: x['id'])]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful clearing
            
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
            # Reset ID counter for efficiency
            self._next_id = 1
            return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format internal task representation for external consumption.
        
        Args:
            task (Dict): Internal task dictionary
            
        Returns:
            Dict: Formatted task with required fields only
            
        Note:
            This is an internal method for maintaining consistent output format.
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the system.
        
        Returns:
            int: Total number of tasks
            
        Note:
            This utility method provides quick access to task count for UI purposes.
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
            
        Note:
            This utility method helps with progress tracking.
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task['is_finished'])


def main():
    """
    Demonstration of TaskManager functionality with comprehensive examples.
    
    This function showcases all the main features of the TaskManager class
    including error handling and edge cases.
    """
    print("=== TaskManager Demo ===\n")
    
    # Initialize task manager
    tm = TaskManager()
    
    try:
        # Demonstrate adding tasks
        print("1. Adding tasks:")
        task1_id = tm.add("Buy groceries", "Get milk, bread, eggs, and fruits")
        task2_id = tm.add("Complete project", "Finish the final report and presentation")
        task3_id = tm.add("Exercise", "30 minutes cardio workout")
        print(f"Added task {task1_id}: Buy groceries")
        print(f"Added task {task2_id}: Complete project")
        print(f"Added task {task3_id}: Exercise")
        
        # Demonstrate getting all tasks
        print(f"\n2. All tasks ({tm.get_task_count()} total):")
        for task in tm.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate finishing a task
        print(f"\n3. Completing task {task1_id}:")
        if tm.finish(task1_id):
            print("Task marked as completed successfully")
        
        # Demonstrate searching
        print("\n4. Searching for 'project':")
        search_results = tm.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Show completion statistics
        print(f"\n5. Progress: {tm.get_completed_count()}/{tm.get_task_count()} tasks completed")
        
        # Demonstrate removing a task
        print(f"\n6. Removing task {task2_id}:")
        if tm.remove(task2_id):
            print("Task removed successfully")
        
        print(f"\nRemaining tasks ({tm.get_task_count()} total):")
        for task in tm.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate error handling
        print("\n7. Error handling examples:")
        try:
            tm.add("", "Invalid task")
        except ValueError as e:
            print(f"  Caught expected error: {e}")
        
        try:
            tm.remove(-1)
        except ValueError as e:
            print(f"  Caught expected error: {e}")
        
        # Demonstrate clearing all tasks
        print("\n8. Clearing all tasks:")
        if tm.clear_all():
            print("All tasks cleared successfully")
            print(f"Tasks remaining: {tm.get_task_count()}")
        
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
