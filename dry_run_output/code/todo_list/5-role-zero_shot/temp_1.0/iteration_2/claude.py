
"""
TODO List Application

A console-based todo list application implementing ISO/IEC 25010 quality standards.
Provides functionality to manage tasks with CRUD operations and search capabilities.
"""

from typing import List, Dict, Optional
import logging
from datetime import datetime


class TaskManager:
    """
    A task management system that provides CRUD operations for todo list items.
    
    This class implements an in-memory task storage system with efficient operations
    for adding, removing, searching, and managing task completion status.
    
    Attributes:
        _tasks (Dict[int, Dict]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
        self._logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the TaskManager."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): The task name to validate
            
        Raises:
            ValueError: If task name is empty or not a string
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
            task_description (str): The task description to validate
            
        Raises:
            TypeError: If task description is not a string
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            TypeError: If task ID is not an integer
            ValueError: If task ID is negative or zero
            KeyError: If task ID does not exist
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
    
    def _validate_search_term(self, task_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            task_term (str): The search term to validate
            
        Raises:
            TypeError: If search term is not a string
            ValueError: If search term is empty
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")
    
    def _create_task_dict(self, task_id: int, task_name: str, task_description: str, 
                         is_finished: bool = False) -> Dict:
        """
        Create a standardized task dictionary.
        
        Args:
            task_id (int): Unique task identifier
            task_name (str): Name of the task
            task_description (str): Description of the task
            is_finished (bool): Completion status of the task
            
        Returns:
            Dict: Formatted task dictionary with metadata
        """
        return {
            'id': task_id,
            'task_name': task_name.strip(),
            'task_description': task_description.strip(),
            'is_finished': is_finished,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (cannot be empty)
            task_description (str): Description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task_name is empty or whitespace only
            TypeError: If inputs are not strings
        """
        try:
            self._validate_task_name(task_name)
            self._validate_task_description(task_description)
            
            task_id = self._next_id
            self._tasks[task_id] = self._create_task_dict(
                task_id, task_name, task_description
            )
            self._next_id += 1
            
            self._logger.info(f"Task created successfully with ID: {task_id}")
            return task_id
            
        except (ValueError, TypeError) as e:
            self._logger.error(f"Failed to add task: {e}")
            raise
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            KeyError: If task with given ID does not exist
        """
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            self._logger.info(f"Task with ID {task_id} removed successfully")
            return True
            
        except (TypeError, ValueError, KeyError) as e:
            self._logger.error(f"Failed to remove task {task_id}: {e}")
            raise
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Uses efficient string matching to find tasks containing the search term
        in either their name or description fields.
        
        Args:
            task_term (str): Search term to match against task name/description
            
        Returns:
            List[Dict]: List of matching tasks with all their details
            
        Raises:
            ValueError: If task_term is empty or whitespace only
            TypeError: If task_term is not a string
        """
        try:
            self._validate_search_term(task_term)
            
            search_term_lower = task_term.strip().lower()
            matching_tasks = []
            
            for task in self._tasks.values():
                task_name_lower = task['task_name'].lower()
                task_desc_lower = task['task_description'].lower()
                
                if (search_term_lower in task_name_lower or 
                    search_term_lower in task_desc_lower):
                    matching_tasks.append(task.copy())
            
            self._logger.info(f"Search for '{task_term}' returned {len(matching_tasks)} results")
            return matching_tasks
            
        except (ValueError, TypeError) as e:
            self._logger.error(f"Search failed: {e}")
            raise
    
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
            KeyError: If task with given ID does not exist
        """
        try:
            self._validate_task_id(task_id)
            
            self._tasks[task_id]['is_finished'] = True
            self._tasks[task_id]['updated_at'] = datetime.now().isoformat()
            
            self._logger.info(f"Task with ID {task_id} marked as finished")
            return True
            
        except (TypeError, ValueError, KeyError) as e:
            self._logger.error(f"Failed to finish task {task_id}: {e}")
            raise
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks from the todo list.
        
        Returns tasks in the order they were created, with all task details
        including metadata.
        
        Returns:
            List[Dict]: List of all tasks with their complete information
        """
        tasks_list = list(self._tasks.values())
        self._logger.info(f"Retrieved {len(tasks_list)} tasks")
        return tasks_list
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        This operation clears all stored tasks and resets the ID counter,
        effectively returning the system to its initial state.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        task_count = len(self._tasks)
        self._tasks.clear()
        self._next_id = 1
        
        self._logger.info(f"Cleared {task_count} tasks from the system")
        return True
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID.
        
        Args:
            task_id (int): Unique identifier of the task
            
        Returns:
            Optional[Dict]: Task dictionary if found, None otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        try:
            if not isinstance(task_id, int):
                raise TypeError("Task ID must be an integer")
            if task_id <= 0:
                raise ValueError("Task ID must be a positive integer")
            
            return self._tasks.get(task_id, None)
            
        except (TypeError, ValueError) as e:
            self._logger.error(f"Failed to get task {task_id}: {e}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the current tasks.
        
        Returns:
            Dict: Statistics including total tasks, completed tasks, and pending tasks
        """
        total_tasks = len(self._tasks)
        completed_tasks = sum(1 for task in self._tasks.values() if task['is_finished'])
        pending_tasks = total_tasks - completed_tasks
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }


def main():
    """
    Demonstration function showing TaskManager usage.
    
    This function provides examples of all TaskManager operations and
    demonstrates proper error handling.
    """
    # Initialize the task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("=== Adding Tasks ===")
        task1_id = task_manager.add("Buy groceries", "Buy milk, eggs, and bread from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added task 1 with ID: {task1_id}")
        print(f"Added task 2 with ID: {task2_id}")
        print(f"Added task 3 with ID: {task3_id}")
        
        # Display all tasks
        print("\n=== All Tasks ===")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\n=== Finishing Task {task1_id} ===")
        task_manager.finish(task1_id)
        print(f"Task {task1_id} marked as completed")
        
        # Search for tasks
        print("\n=== Searching Tasks ===")
        search_results = task_manager.search("project")
        print(f"Tasks containing 'project': {len(search_results)} found")
        for task in search_results:
            print(f"  - {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print("\n=== Task Statistics ===")
        stats = task_manager.get_statistics()
        print(f"Total tasks: {stats['total_tasks']}")
        print(f"Completed: {stats['completed_tasks']}")
        print(f"Pending: {stats['pending_tasks']}")
        print(f"Completion rate: {stats['completion_rate']:.1f}%")
        
        # Demonstrate error handling
        print("\n=== Error Handling Demo ===")
        try:
            task_manager.add("", "This should fail")
        except ValueError as e:
            print(f"Caught expected error: {e}")
        
        try:
            task_manager.remove(999)
        except KeyError as e:
            print(f"Caught expected error: {e}")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
