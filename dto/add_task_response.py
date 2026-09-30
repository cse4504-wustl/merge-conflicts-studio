from entity.task import Task


class AddTaskResponse:
    def __init__(self, task: Task):
        self.task = task
