
"""
Console-based Todo List Application
A high-quality, maintainable task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from datetime import datetime


class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Task name/title
        description (str): Detailed task description
        is_finished (bool): Completion status
        created_at (datetime): Task creation timestamp
    """
    
    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name/title
            description: Detailed task description
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format.
        
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
    Manages todo list operations with thread-safe implementation.
    
    This class provides a complete interface for managing tasks including
    adding, removing, searching, and updating tasks. It uses efficient
    data structures for optimal performance and includes comprehensive
    error handling and validation.
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._lock = threading.RLock()  # Thread-safe operations
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name: The task name to validate
            
        Raises:
            ValueError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:
            raise ValueError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description: The task description to validate
            
        Raises:
            ValueError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace only")
        if len(task_description.strip()) > 500:
            raise ValueError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id: The task ID to validate
            
        Raises:
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
            task_name: Name/title of the task
            task_description: Detailed description of the task
            
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
            # Create new task with unique ID
            task_id = self._next_id
            task = Task(task_id, task_name.strip(), task_description.strip())
            
            # Store task and increment ID counter
            self._tasks[task_id] = task
            self._next_id += 1
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False if task not found
            
        Raises:
            ValueError: If task ID is invalid
            TypeError: If task_id is not an integer
        """
        # Validate input
        self._validate_task_id(task_id)
        
        with self._lock:
            # Check if task exists and remove it
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: Term to search for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            ValueError: If search term is invalid
            TypeError: If task_term is not a string
        """
        # Validate input
        self._validate_search_term(task_term)
        
        search_term_lower = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            # Search through all tasks for matching terms
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort results by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was successfully marked as finished, False if task not found
            
        Raises:
            ValueError: If task ID is invalid
            TypeError: If task_id is not an integer
        """
        # Validate input
        self._validate_task_id(task_id)
        
        with self._lock:
            # Check if task exists and mark as finished
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks from the todo list.
        
        Returns:
            List of dictionaries containing all task information,
            sorted by task ID
        """
        with self._lock:
            # Convert all tasks to dictionary format and sort by ID
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            True indicating successful clearing of all tasks
        """
        with self._lock:
            # Clear all tasks and reset ID counter
            self._tasks.clear()
            self._next_id = 1
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


class TodoApp:
    """
    Console-based todo list application interface.
    
    Provides a user-friendly command-line interface for interacting
    with the TaskManager system.
    """
    
    def __init__(self) -> None:
        """Initialize the todo application."""
        self.task_manager = TaskManager()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           TODO LIST MANAGER")
        print("="*50)
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Mark Task as Finished")
        print("5. Show All Tasks")
        print("6. Clear All Tasks")
        print("7. Show Statistics")
        print("8. Exit")
        print("="*50)
    
    def display_task(self, task: Dict) -> None:
        """
        Display a single task in formatted output.
        
        Args:
            task: Dictionary containing task information
        """
        status = "✓ DONE" if task['is_finished'] else "○ PENDING"
        print(f"[{task['id']}] {task['task_name']} - {status}")
        print(f"    Description: {task['task_description']}")
        print("-" * 40)
    
    def display_tasks(self, tasks: List[Dict]) -> None:
        """
        Display multiple tasks in formatted output.
        
        Args:
            tasks: List of task dictionaries to display
        """
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"\nFound {len(tasks)} task(s):")
        print("-" * 40)
        for task in tasks:
            self.display_task(task)
    
    def safe_input(self, prompt: str) -> str:
        """
        Get user input with error handling.
        
        Args:
            prompt: Prompt message to display
            
        Returns:
            User input string
        """
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return ""
    
    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to Todo List Manager!")
        
        while True:
            try:
                self.display_menu()
                choice = self.safe_input("Enter your choice (1-8): ")
                
                if choice == '1':
                    self._handle_add_task()
                elif choice == '2':
                    self._handle_remove_task()
                elif choice == '3':
                    self._handle_search_tasks()
                elif choice == '4':
                    self._handle_finish_task()
                elif choice == '5':
                    self._handle_show_all_tasks()
                elif choice == '6':
                    self._handle_clear_all_tasks()
                elif choice == '7':
                    self._handle_show_statistics()
                elif choice == '8':
                    print("Thank you for using Todo List Manager!")
                    break
                else:
                    print("Invalid choice. Please enter a number from 1-8.")
                    
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")
    
    def _handle_add_task(self) -> None:
        """Handle adding a new task."""
        try:
            name = self.safe_input("Enter task name: ")
            if not name:
                return
                
            description = self.safe_input("Enter task description: ")
            if not description:
                return
                
            task_id = self.task_manager.add(name, description)
            print(f"✓ Task added successfully with ID: {task_id}")
            
        except (ValueError, TypeError) as e:
            print(f"Error adding task: {e}")
    
    def _handle_remove_task(self) -> None:
        """Handle removing a task."""
        try:
            task_id_str = self.safe_input("Enter task ID to remove: ")
            if not task_id_str:
                return
                
            task_id = int(task_id_str)
            if self.task_manager.remove(task_id):
                print(f"✓ Task {task_id} removed successfully.")
            else:
                print(f"Task with ID {task_id} not found.")
                
        except ValueError:
            print("Error: Please enter a valid task ID (positive integer).")
        except Exception as e:
            print(f"Error removing task: {e}")
    
    def _handle_search_tasks(self) -> None:
        """Handle searching for tasks."""
        try:
            search_term = self.safe_input("Enter search term: ")
            if not search_term:
                return
                
            results = self.task_manager.search(search_term)
            self.display_tasks(results)
            
        except (ValueError, TypeError) as e:
            print(f"Error searching tasks: {e}")
    
    def _handle_finish_task(self) -> None:
        """Handle marking a task as finished."""
        try:
            task_id_str = self.safe_input("Enter task ID to mark as finished: ")
            if not task_id_str:
                return
                
            task_id = int(task_id_str)
            if self.task_manager.finish(task_id):
                print(f"✓ Task {task_id} marked as finished.")
            else:
                print(f"Task with ID {task_id} not found.")
                
        except ValueError:
            print("Error: Please enter a valid task ID (positive integer).")
        except Exception as e:
            print(f"Error finishing task: {e}")
    
    def _handle_show_all_tasks(self) -> None:
        """Handle displaying all tasks."""
        try:
            all_tasks = self.task_manager.get_all()
            self.display_tasks(all_tasks)
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
    
    def _handle_clear_all_tasks(self) -> None:
        """Handle clearing all tasks."""
        try:
            confirm = self.safe_input("Are you sure you want to delete all tasks? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                self.task_manager.clear_all()
                print("✓ All tasks cleared successfully.")
            else:
                print("Operation cancelled.")
        except Exception as e:
            print(f"Error clearing tasks: {e}")
    
    def _handle_show_statistics(self) -> None:
        """Handle displaying task statistics."""
        try:
            total_tasks = self.task_manager.get_task_count()
            completed_tasks = self.task_manager.get_completed_count()
            pending_tasks = total_tasks - completed_tasks
            
            print(f"\n📊 Task Statistics:")
            print(f"Total Tasks: {total_tasks}")
            print(f"Completed: {completed_tasks}")
            print(f"Pending: {pending_tasks}")
            
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100
                print(f"Completion Rate: {completion_rate:.1f}%")
                
        except Exception as e:
            print(f"Error retrieving statistics: {e}")


def main() -> None:
    """Main entry point of the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
