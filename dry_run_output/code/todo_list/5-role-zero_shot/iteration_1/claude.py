
from datetime import datetime
from typing import List, Dict, Optional, Union, Any
import re

class TaskManager:
    """
    Task Manager class for managing a todo list application.
    
    This class provides functionality to add, remove, search, finish, 
    get all tasks, and clear all tasks in a todo list.
    
    Attributes:
        _tasks (dict): Dictionary storing tasks with task ID as key
        _next_id (int): Counter for assigning unique task IDs
    """
    
    def __init__(self):
        """Initialize an empty task manager with a task dictionary and ID counter."""
        self._tasks = {}  # Using dictionary for O(1) lookups by ID
        self._next_id = 1  # Start IDs from 1
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Description of the task
        
        Returns:
            int: Unique ID of the added task
            
        Raises:
            ValueError: If task_name or task_description is empty
        """
        # Input validation
        if not task_name or not isinstance(task_name, str):
            raise ValueError("Task name cannot be empty and must be a string")
        if not task_description or not isinstance(task_description, str):
            raise ValueError("Task description cannot be empty and must be a string")
        
        # Create task with unique ID
        task_id = self._next_id
        self._tasks[task_id] = {
            'id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'is_finished': False,
            'created_at': datetime.now()
        }
        self._next_id += 1
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        
        Args:
            task_id (int): Unique ID of the task to remove
        
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        
        return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): Search term to match against task names or descriptions
        
        Returns:
            list[dict]: List of matching tasks with their details
            
        Raises:
            ValueError: If task_term is empty
        """
        # Input validation
        if not task_term or not isinstance(task_term, str):
            raise ValueError("Search term cannot be empty and must be a string")
        
        # Case-insensitive search
        results = []
        pattern = re.compile(re.escape(task_term), re.IGNORECASE)
        
        for task in self._tasks.values():
            if (pattern.search(task['task_name']) or 
                pattern.search(task['task_description'])):
                results.append(self._format_task_output(task))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): Unique ID of the task to mark as completed
        
        Returns:
            bool: True if task was successfully marked as completed, False otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        # Check if task exists
        if task_id in self._tasks:
            # Only update if not already finished
            if not self._tasks[task_id]['is_finished']:
                self._tasks[task_id]['is_finished'] = True
                self._tasks[task_id]['completed_at'] = datetime.now()
                return True
            return True  # Task was already finished
        
        return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            list[dict]: List of all tasks with their details
        """
        return [self._format_task_output(task) for task in self._tasks.values()]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks.
        
        Returns:
            bool: True if all tasks were successfully deleted
        """
        self._tasks.clear()
        return True
    
    def _format_task_output(self, task: Dict) -> Dict:
        """
        Format task output to match the required format.
        
        Args:
            task (dict): Task dictionary with all details
            
        Returns:
            dict: Task with required format (id, task_name, task_description, is_finished)
        """
        return {
            'id': task['id'],
            'task_name': task['task_name'],
            'task_description': task['task_description'],
            'is_finished': task['is_finished']
        }
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Get a task by its ID.
        
        Args:
            task_id (int): Unique ID of the task to retrieve
            
        Returns:
            dict or None: Task details if found, None otherwise
            
        Raises:
            ValueError: If task_id is not a positive integer
        """
        # Input validation
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
            
        if task_id in self._tasks:
            return self._format_task_output(self._tasks[task_id])
        
        return None


def demo_task_manager():
    """Demonstrate the functionality of the TaskManager class."""
    
    # Create a new task manager
    task_manager = TaskManager()
    
    # Add tasks
    task1_id = task_manager.add("Buy groceries", "Milk, eggs, bread")
    task2_id = task_manager.add("Call doctor", "Schedule annual checkup")
    task3_id = task_manager.add("Finish report", "Complete quarterly sales report")
    
    print("All tasks after adding:")
    for task in task_manager.get_all():
        print(task)
    
    # Mark a task as completed
    task_manager.finish(task1_id)
    print(f"\nTask {task1_id} marked as completed.")
    
    # Search for tasks
    print("\nSearch results for 'report':")
    for task in task_manager.search("report"):
        print(task)
    
    # Remove a task
    task_manager.remove(task2_id)
    print(f"\nTask {task2_id} removed.")
    
    # Get all tasks after modifications
    print("\nAll tasks after modifications:")
    for task in task_manager.get_all():
        print(task)
    
    # Clear all tasks
    task_manager.clear_all()
    print("\nAll tasks cleared.")
    print("Tasks remaining:", len(task_manager.get_all()))

if __name__ == "__main__":
    demo_task_manager()
