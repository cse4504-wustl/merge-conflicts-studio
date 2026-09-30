from typing import List, Optional

from entity.task import Task


class InMemoryTaskRepository:
    def __init__(self):
        self._tasks: List[Task] = []

    def get_all(self) -> List[Task]:
        return list(self._tasks)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def add(self, task: Task) -> None:
        self._tasks.append(task)

    def update(self, task: Task) -> None:
        for index, existing in enumerate(self._tasks):
            if existing.id == task.id:
                self._tasks[index] = task
                return

    def remove(self, task_id: int) -> None:
        self._tasks = [task for task in self._tasks if task.id != task_id]

    def next_id(self) -> int:
        return max([task.id for task in self._tasks], default=0) + 1
