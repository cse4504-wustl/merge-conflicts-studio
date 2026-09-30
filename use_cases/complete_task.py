from dto.task_operation_request import TaskOperationRequest
from dto.task_operation_response import TaskOperationResponse
from interfaces.task_repository import TaskRepository


class CompleteTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def __call__(self, request: TaskOperationRequest) -> TaskOperationResponse:
        """Retrieve the task via repo.get_by_id(), set completed=True, persist via repo.update().
        Return TaskOperationResponse with success=True and the task description if found, or success=False and description="no task found" otherwise."""
        task = self.repo.get_by_id(request.task_id)
        if task is None:
            return TaskOperationResponse(success=False, description="no task found")

        task.completed = True
        self.repo.update(task)
        return TaskOperationResponse(success=True, description=task.description)
