from dto.list_tasks_response import ListTasksResponse
from interfaces.task_repository import TaskRepository


class ListTasksUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def __call__(self) -> ListTasksResponse:
        """Retrieve all tasks via repo.get_all() and return them in a ListTasksResponse."""
        return ListTasksResponse(self.repo.get_all())
