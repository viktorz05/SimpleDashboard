from datetime import datetime
from itertools import combinations
from stress import QMetric

class Task:
    def __init__(self, name :str, date : str, priority : QMetric, difficulty : QMetric, est_time : float):
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
        pairs = list(combinations(self.tasks.values(), 2))
        avg_proximity = sum(self.get_task_proximity(task1, task2) for task1, task2 in pairs) / len(pairs) if pairs else 0
        avg_difficulty = sum(task.difficulty.value for task in self.tasks.values()) / total_tasks if total_tasks > 0 else 0
        if total_tasks < 3 and avg_difficulty < 5 and avg_proximity > 7:
            return QMetric.BAJO
        elif total_tasks < 5 and avg_difficulty < 7 and avg_proximity > 3:
            return QMetric.MEDIO
        else:
            return QMetric.ALTO 
