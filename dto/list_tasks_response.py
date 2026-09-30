from typing import List

from entity.task import Task


class ListTasksResponse:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
