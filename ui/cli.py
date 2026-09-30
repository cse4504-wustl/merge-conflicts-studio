from dto.add_task_request import AddTaskRequest
from dto.task_operation_request import TaskOperationRequest
from persistence.in_memory_task_repository import InMemoryTaskRepository
from use_cases.add_task import AddTaskUseCase
from use_cases.complete_task import CompleteTaskUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.list_tasks import ListTasksUseCase


class TaskCLI:
    def __init__(self):
        repo = InMemoryTaskRepository()
        self.add_task = AddTaskUseCase(repo)
        self.complete_task = CompleteTaskUseCase(repo)
        self.delete_task = DeleteTaskUseCase(repo)
        self.list_tasks = ListTasksUseCase(repo)

    def run(self):
        while True:
            self._print_menu()
            choice = input("Choice: ").strip()

            if choice == "1":
                self._handle_add()
            elif choice == "2":
                self._handle_list()
            elif choice == "3":
                self._handle_complete()
            elif choice == "4":
                self._handle_delete()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def _print_menu(self):
        print()
        print("=== Task Manager ===")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")

    # ------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------
    def _handle_add(self):
        description = input("Enter task description: ").strip()
        if not description:
            print("Description cannot be empty.")
            return

        response = self.add_task(AddTaskRequest(description))
        print("Task added successfully!")

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------
    def _handle_list(self):
        response = self.list_tasks()
        if not response.tasks:
            print("No tasks yet.")
            return

        for task in response.tasks:
            status = "Done" if task.completed else "Pending"
            print(f"ID: {task.id} | Description: {task.description} | Status: {status} | Created: {task.created_date}")

    # ------------------------------------------------------------------
    # Complete
    # ------------------------------------------------------------------
    def _handle_complete(self):
        task_id = self._read_task_id()
        if task_id is None:
            return

        response = self.complete_task(TaskOperationRequest(task_id))
        if response.success:
            print(f"Completed: {response.description}")
        else:
            print(f"Could not complete task {task_id}: {response.description}")

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------
    def _handle_delete(self):
        task_id = self._read_task_id()
        if task_id is None:
            return

        response = self.delete_task(TaskOperationRequest(task_id))
        if response.success:
            print(f"Deleted: {response.description}")
        else:
            print(f"Could not delete task {task_id}: {response.description}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _read_task_id(self):
        raw = input("Enter task ID: ").strip()
        if not raw.isdigit():
            print("Task ID must be a number.")
            return None
        return int(raw)
