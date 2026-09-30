from dto.add_task_request import AddTaskRequest
from dto.add_task_response import AddTaskResponse
from entity.task import Task
from interfaces.task_repository import TaskRepository


class AddTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def __call__(self, request: AddTaskRequest) -> AddTaskResponse:
        """Obtain a unique ID via repo.next_id(), construct a Task, persist it via repo.add(),
        and return an AddTaskResponse containing the new Task."""
        task = Task(description=request.description, id=self.repo.next_id())
        self.repo.add(task)
        return AddTaskResponse(task)
