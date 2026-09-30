from datetime import date


class Task:
    def __init__(self, description: str, id: int, completed: bool = None, created_date: date = None):
        self.description = description
        self.id = id
        self.completed = False if completed is None else completed
        self.created_date = date.today() if created_date is None else created_date
