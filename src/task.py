from datetime import datetime

from Dashboard.src.stress import Metric

class Task:
    def __init__(self, name :str, date : str, priority : Metric, difficulty : Metric, est_time : float):
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
        total_tasks = len(self.tasks)
        avg_difficulty = sum(task.difficulty for task in self.tasks.values()) / total_tasks if total_tasks > 0 else 0
        avg_proximity = sum(self.get_task_proximity(task1, task2) for task1 in self.tasks.values() for task2 in self.tasks.values()) / (total_tasks * (total_tasks - 1)) if total_tasks > 1 else 0
        if total_tasks < 3 and 
        pass
