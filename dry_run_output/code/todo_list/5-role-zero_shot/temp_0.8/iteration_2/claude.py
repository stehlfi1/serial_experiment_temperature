
"""
High-Quality Todo List Application
Implements a console-based task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import time


class Task:
    """
    Represents a single task with all its attributes.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Task name/title
        description (str): Detailed description of the task
        is_finished (bool): Completion status
        created_at (float): Timestamp when task was created
    """
    
    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id (int): Unique identifier for the task
            name (str): Task name
            description (str): Task description
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False
        self.created_at = time.time()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external representation.
        
        Returns:
            Dict: Task data in dictionary format
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages todo list operations with high performance and reliability.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and managing task completion status.
    """
    
    def __init__(self) -> None:
        """Initialize the task manager with empty task storage."""
        self._tasks: Dict[int, Task] = {}  # Primary storage: O(1) lookups
        self._next_id: int = 1  # Auto-incrementing ID counter
        self._id_pool: List[int] = []  # Reusable IDs for efficiency
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): Task name to validate
            
        Raises:
            ValueError: If task name is empty or invalid
            TypeError: If task name is not a string
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): Task description to validate
            
        Raises:
            ValueError: If task description is empty or invalid
            TypeError: If task description is not a string
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task ID is not an integer
            ValueError: If task ID is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _get_next_id(self) -> int:
        """
        Get the next available task ID efficiently.
        
        Returns:
            int: Next available task ID
        """
        if self._id_pool:
            return self._id_pool.pop()
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def _return_id(self, task_id: int) -> None:
        """
        Return an ID to the pool for reuse.
        
        Args:
            task_id (int): ID to return to the pool
        """
        self._id_pool.append(task_id)
        self._id_pool.sort(reverse=True)  # Keep pool sorted for consistent behavior
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task name or description is empty
            TypeError: If inputs are not strings
            
        Time Complexity: O(1)
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        # Sanitize inputs
        task_name = task_name.strip()
        task_description = task_description.strip()
        
        task_id = self._get_next_id()
        task = Task(task_id, task_name, task_description)
        self._tasks[task_id] = task
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Time Complexity: O(1)
        """
        self._validate_task_id(task_id)
        
        if task_id not in self._tasks:
            return False
        
        del self._tasks[task_id]
        self._return_id(task_id)
        return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): Search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search term is not a string
            ValueError: If search term is empty
            
        Time Complexity: O(n) where n is the number of tasks
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")
        
        search_term = task_term.strip().lower()
        matching_tasks = []
        
        for task in self._tasks.values():
            if (search_term in task.name.lower() or 
                search_term in task.description.lower()):
                matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent results
        matching_tasks.sort(key=lambda x: x['id'])
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Time Complexity: O(1)
        """
        self._validate_task_id(task_id)
        
        if task_id not in self._tasks:
            return False
        
        self._tasks[task_id].is_finished = True
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Time Complexity: O(n log n) where n is the number of tasks (due to sorting)
        """
        all_tasks = [task.to_dict() for task in self._tasks.values()]
        # Sort by task ID for consistent ordering
        all_tasks.sort(key=lambda x: x['id'])
        return all_tasks
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful operation
            
        Time Complexity: O(1)
        """
        self._tasks.clear()
        self._id_pool.clear()
        self._next_id = 1
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks currently stored
            
        Time Complexity: O(1)
        """
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
            
        Time Complexity: O(n) where n is the number of tasks
        """
        return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    """
    # Create task manager instance
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===\n")
    
    # Add some tasks
    print("1. Adding tasks...")
    task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
    task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
    task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
    
    print(f"Added task with ID: {task1_id}")
    print(f"Added task with ID: {task2_id}")
    print(f"Added task with ID: {task3_id}")
    
    # Display all tasks
    print("\n2. All tasks:")
    tasks = task_manager.get_all()
    for task in tasks:
        status = "✓" if task['is_finished'] else "○"
        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
    
    # Mark a task as finished
    print("\n3. Marking task as finished...")
    success = task_manager.finish(task2_id)
    print(f"Task {task2_id} marked as finished: {success}")
    
    # Search for tasks
    print("\n4. Searching for 'project'...")
    search_results = task_manager.search("project")
    for task in search_results:
        status = "✓" if task['is_finished'] else "○"
        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
    
    # Remove a task
    print("\n5. Removing task...")
    success = task_manager.remove(task1_id)
    print(f"Task {task1_id} removed: {success}")
    
    # Display final state
    print("\n6. Final task list:")
    tasks = task_manager.get_all()
    for task in tasks:
        status = "✓" if task['is_finished'] else "○"
        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
    
    print(f"\nTotal tasks: {task_manager.get_task_count()}")
    print(f"Completed tasks: {task_manager.get_completed_count()}")


if __name__ == "__main__":
    main()
