import unittest

from dto.add_task_request import AddTaskRequest
from dto.task_operation_request import TaskOperationRequest
from persistence.in_memory_task_repository import InMemoryTaskRepository
from use_cases.add_task import AddTaskUseCase
from use_cases.complete_task import CompleteTaskUseCase
from use_cases.delete_task import DeleteTaskUseCase
from use_cases.list_tasks import ListTasksUseCase


class UseCaseTests(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryTaskRepository()
        self.add = AddTaskUseCase(self.repo)
        self.complete = CompleteTaskUseCase(self.repo)
        self.delete = DeleteTaskUseCase(self.repo)
        self.list = ListTasksUseCase(self.repo)

    def test_add_assigns_increasing_ids(self):
        first = self.add(AddTaskRequest("first")).task
        second = self.add(AddTaskRequest("second")).task
        self.assertEqual(1, first.id)
        self.assertEqual(2, second.id)

    def test_list_returns_all_tasks(self):
        self.add(AddTaskRequest("first"))
        self.add(AddTaskRequest("second"))
        self.assertEqual(["first", "second"], [t.description for t in self.list().tasks])

    def test_complete_marks_task_done(self):
        task = self.add(AddTaskRequest("first")).task
        response = self.complete(TaskOperationRequest(task.id))
        self.assertTrue(response.success)
        self.assertTrue(self.repo.get_by_id(task.id).completed)

    def test_complete_missing_task_fails(self):
        response = self.complete(TaskOperationRequest(99))
        self.assertFalse(response.success)
        self.assertEqual("no task found", response.description)

    def test_delete_removes_task(self):
        task = self.add(AddTaskRequest("first")).task
        response = self.delete(TaskOperationRequest(task.id))
        self.assertTrue(response.success)
        self.assertEqual([], self.list().tasks)

    def test_delete_missing_task_fails(self):
        response = self.delete(TaskOperationRequest(99))
        self.assertFalse(response.success)


if __name__ == "__main__":
    unittest.main()
