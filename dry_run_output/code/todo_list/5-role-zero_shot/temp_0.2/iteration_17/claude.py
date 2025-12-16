
"""
High-Quality Todo List Application

A console-based todo list application implementing the TaskManager class
with comprehensive task management functionality following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import re
from datetime import datetime


class TaskManager:
    """
    A comprehensive task management system for handling todo list operations.
    
    This class provides functionality to add, remove, search, finish, and manage
    tasks in an efficient and maintainable way. All tasks are stored in-memory
    with optimized data structures for fast operations.
    
    Attributes:
        _tasks (Dict[int, Dict]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
        _name_index (Dict[str, set]): Index for fast name-based searches
        _description_index (Dict[str, set]): Index for fast description-based searches
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage and indexes."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1
        # Search indexes for O(1) lookups
        self._name_index: Dict[str, set] = {}
        self._description_index: Dict[str, set] = {}
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): The task name to validate
            
        Raises:
            TypeError: If task_name is not a string
            ValueError: If task_name is empty or contains only whitespace
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or contain only whitespace")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            TypeError: If task_description is not a string
            ValueError: If task_description is empty or contains only whitespace
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or contain only whitespace")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_search_term(self, task_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            task_term (str): The search term to validate
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty or contain only whitespace")
    
    def _update_search_indexes(self, task_id: int, task_name: str, task_description: str) -> None:
        """
        Update search indexes for efficient searching.
        
        Args:
            task_id (int): The task ID
            task_name (str): The task name
            task_description (str): The task description
        """
        # Index by individual words for better search capability
        name_words = re.findall(r'\w+', task_name.lower())
        desc_words = re.findall(r'\w+', task_description.lower())
        
        for word in name_words:
            if word not in self._name_index:
                self._name_index[word] = set()
            self._name_index[word].add(task_id)
        
        for word in desc_words:
            if word not in self._description_index:
                self._description_index[word] = set()
            self._description_index[word].add(task_id)
    
    def _remove_from_search_indexes(self, task_id: int, task_name: str, task_description: str) -> None:
        """
        Remove task from search indexes.
        
        Args:
            task_id (int): The task ID to remove
            task_name (str): The task name
            task_description (str): The task description
        """
        name_words = re.findall(r'\w+', task_name.lower())
        desc_words = re.findall(r'\w+', task_description.lower())
        
        for word in name_words:
            if word in self._name_index:
                self._name_index[word].discard(task_id)
                if not self._name_index[word]:
                    del self._name_index[word]
        
        for word in desc_words:
            if word in self._description_index:
                self._description_index[word].discard(task_id)
                if not self._description_index[word]:
                    del self._description_index[word]
    
    def _format_task(self, task_id: int, task_data: Dict) -> Dict:
        """
        Format task data for external consumption.
        
        Args:
            task_id (int): The task ID
            task_data (Dict): Internal task data
            
        Returns:
            Dict: Formatted task data with id, task_name, task_description, is_finished
        """
        return {
            'id': task_id,
            'task_name': task_data['name'],
            'task_description': task_data['description'],
            'is_finished': task_data['is_finished']
        }
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name of the task (must not be empty)
            task_description (str): The description of the task (must not be empty)
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            TypeError: If inputs are not strings
            ValueError: If inputs are empty or contain only whitespace
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        task_id = self._next_id
        self._next_id += 1
        
        # Store task with metadata
        self._tasks[task_id] = {
            'name': task_name.strip(),
            'description': task_description.strip(),
            'is_finished': False,
            'created_at': datetime.now(),
            'finished_at': None
        }
        
        # Update search indexes for efficient searching
        self._update_search_indexes(task_id, task_name, task_description)
        
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The ID of the task to remove (must be positive)
            
        Returns:
            bool: True if the task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)
        
        if task_id not in self._tasks:
            return False
        
        # Remove from search indexes before deleting
        task_data = self._tasks[task_id]
        self._remove_from_search_indexes(task_id, task_data['name'], task_data['description'])
        
        # Remove the task
        del self._tasks[task_id]
        return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using partial matching.
        
        Args:
            task_term (str): The search term (must not be empty)
            
        Returns:
            List[Dict]: List of matching tasks with format:
                       [{'id': int, 'task_name': str, 'task_description': str, 'is_finished': bool}]
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("groceries")
            >>> print(len(results))
            1
        """
        self._validate_search_term(task_term)
        
        search_words = re.findall(r'\w+', task_term.lower())
        matching_task_ids = set()
        
        # Search in both name and description indexes
        for word in search_words:
            # Partial matching for more flexible search
            for indexed_word in self._name_index:
                if word in indexed_word:
                    matching_task_ids.update(self._name_index[indexed_word])
            
            for indexed_word in self._description_index:
                if word in indexed_word:
                    matching_task_ids.update(self._description_index[indexed_word])
        
        # Also perform direct substring search for exact phrase matching
        term_lower = task_term.lower()
        for task_id, task_data in self._tasks.items():
            if (term_lower in task_data['name'].lower() or 
                term_lower in task_data['description'].lower()):
                matching_task_ids.add(task_id)
        
        # Format and return results sorted by ID
        results = []
        for task_id in sorted(matching_task_ids):
            if task_id in self._tasks:  # Safety check
                results.append(self._format_task(task_id, self._tasks[task_id]))
        
        return results
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The ID of the task to mark as finished (must be positive)
            
        Returns:
            bool: True if the task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)
        
        if task_id not in self._tasks:
            return False
        
        self._tasks[task_id]['is_finished'] = True
        self._tasks[task_id]['finished_at'] = datetime.now()
        return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of all tasks with format:
                       [{'id': int, 'task_name': str, 'task_description': str, 'is_finished': bool}]
                       Sorted by task ID in ascending order
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> print(len(all_tasks))
            2
        """
        results = []
        for task_id in sorted(self._tasks.keys()):
            results.append(self._format_task(task_id, self._tasks[task_id]))
        return results
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful clearing
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> success = tm.clear_all()
            >>> print(success)
            True
            >>> print(len(tm.get_all()))
            0
        """
        self._tasks.clear()
        self._name_index.clear()
        self._description_index.clear()
        self._next_id = 1
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: The total number of tasks in the system
        """
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: The number of completed tasks
        """
        return sum(1 for task in self._tasks.values() if task['is_finished'])
    
    def get_pending_count(self) -> int:
        """
        Get the number of pending (not completed) tasks.
        
        Returns:
            int: The number of pending tasks
        """
        return sum(1 for task in self._tasks.values() if not task['is_finished'])


def main():
    """
    Console interface for the Todo List application.
    
    Provides a simple command-line interface for interacting with the TaskManager.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, stats, quit")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print("Goodbye!")
                break
            
            elif command == 'add':
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except (TypeError, ValueError) as e:
                    print(f"Error: {e}")
            
            elif command == 'remove':
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'search':
                term = input("Enter search term: ").strip()
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"Found {len(results)} task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No tasks found")
                except (TypeError, ValueError) as e:
                    print(f"Error: {e}")
            
            elif command == 'finish':
                try:
                    task_id = int(input("Enter task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'list':
                tasks = task_manager.get_all()
                if tasks:
                    print(f"All tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == 'clear':
                confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
                if confirm == 'y' or confirm == 'yes':
                    task_manager.clear_all()
                    print("All tasks cleared")
                else:
                    print("Operation cancelled")
            
            elif command == 'stats':
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = task_manager.get_pending_count()
                print(f"Statistics:")
                print(f"  Total tasks: {total}")
                print(f"  Completed: {completed}")
                print(f"  Pending: {pending}")
            
            else:
                print("Unknown command. Available commands: add, remove, search, finish, list, clear, stats, quit")
            
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
