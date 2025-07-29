
"""
High-Quality Todo List Application

A console-based todo list application implementing the TaskManager class
with comprehensive task management functionality following ISO/IEC 25010 standards.
"""

import uuid
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Name/title of the task
        description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
        created_at (datetime): Timestamp when task was created
    """
    id: int
    name: str
    description: str
    is_finished: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Union[int, str, bool]]:
        """
        Convert task to dictionary format for external consumption.
        
        Returns:
            dict: Task data in dictionary format
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    A comprehensive task management system for console-based todo list operations.
    
    This class provides functionality to add, remove, search, finish, retrieve,
    and clear tasks while maintaining data integrity and performance.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses dictionary for O(1) lookups and maintains a counter for unique IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
    
    def _validate_string_input(self, value: str, field_name: str) -> None:
        """
        Validate string inputs for non-empty content.
        
        Args:
            value (str): String to validate
            field_name (str): Name of the field for error messaging
            
        Raises:
            ValueError: If string is empty, None, or contains only whitespace
        """
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty or contain only whitespace")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID for type and positive value.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists in the storage.
        
        Args:
            task_id (int): ID of the task to check
            
        Returns:
            bool: True if task exists, False otherwise
        """
        return task_id in self._tasks
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name/title of the task (cannot be empty)
            task_description (str): Detailed description (cannot be empty)
            
        Returns:
            int: Unique ID assigned to the newly created task
            
        Raises:
            ValueError: If task_name or task_description is empty or whitespace-only
            TypeError: If inputs are not strings
        """
        # Validate inputs
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
            
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")
        
        # Create and store new task
        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description.strip()
        )
        
        self._tasks[task_id] = new_task
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        self._validate_task_id(task_id)
        
        if self._task_exists(task_id):
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict[str, Union[int, str, bool]]]:
        """
        Search for tasks containing the specified term in name or description.
        
        Performs case-insensitive search across task names and descriptions.
        
        Args:
            task_term (str): Search term to look for in tasks
            
        Returns:
            list[dict]: List of matching tasks in dictionary format
            
        Raises:
            ValueError: If search term is empty or contains only whitespace
            TypeError: If search term is not a string
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
            
        self._validate_string_input(task_term, "Search term")
        
        search_term_lower = task_term.strip().lower()
        matching_tasks = []
        
        for task in self._tasks.values():
            # Case-insensitive search in both name and description
            if (search_term_lower in task.name.lower() or 
                search_term_lower in task.description.lower()):
                matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): Unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, 
                  False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        self._validate_task_id(task_id)
        
        if self._task_exists(task_id):
            self._tasks[task_id].is_finished = True
            return True
        
        return False
    
    def get_all(self) -> List[Dict[str, Union[int, str, bool]]]:
        """
        Retrieve all tasks from the todo list.
        
        Returns:
            list[dict]: List of all tasks in dictionary format, sorted by ID
        """
        all_tasks = [task.to_dict() for task in self._tasks.values()]
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful operation
        """
        self._tasks.clear()
        self._next_id = 1
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the system.
        
        Returns:
            int: Total number of tasks
        """
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        return sum(1 for task in self._tasks.values() if task.is_finished)
    
    def get_pending_count(self) -> int:
        """
        Get the number of pending (incomplete) tasks.
        
        Returns:
            int: Number of pending tasks
        """
        return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function showcases the basic operations of the todo list application.
    """
    # Initialize the task manager
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===\n")
    
    try:
        # Add some sample tasks
        print("1. Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Purchase milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added task {task1_id}: Buy groceries")
        print(f"Added task {task2_id}: Complete project")
        print(f"Added task {task3_id}: Exercise")
        
        # Display all tasks
        print("\n2. All tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print("\n3. Marking task as finished...")
        if task_manager.finish(task1_id):
            print(f"Task {task1_id} marked as completed!")
        
        # Search for tasks
        print("\n4. Searching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\n5. Statistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed: {task_manager.get_completed_count()}")
        print(f"  Pending: {task_manager.get_pending_count()}")
        
        # Remove a task
        print(f"\n6. Removing task {task3_id}...")
        if task_manager.remove(task3_id):
            print("Task removed successfully!")
        
        # Final state
        print("\n7. Final task list:")
        final_tasks = task_manager.get_all()
        for task in final_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
    
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
