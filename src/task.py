from datetime import datetime

class Task:
    def __init__(self, name :str, date : str, priority : int, difficulty : int, est_time : float):
        self.name = name
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.priority = priority
        self.difficulty = difficulty
        self.est_time = est_time

class Calendar:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.name] = task
    
    def get_task_proximity(self, task1, task2):
        return abs((task1.date - task2.date).days)
    
    def calculate_load(self):
        # Placeholder for load calculation based on tasks
        pass
