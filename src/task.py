from datetime import datetime
from itertools import combinations
from stress import QMetric

class Task:
    def __init__(self, name :str, date : str, priority : QMetric, difficulty : QMetric, est_time : float, s_time : str | None, e_time : str | None):
        self.name = name
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.priority = priority
        self.difficulty = difficulty
        self.est_time = est_time
        self.start_time = datetime.strptime(s_time, "%H:%M").time() if s_time else None
        self.end_time =  datetime.strptime(e_time, "%H:%M").time() if e_time else None
    
    @property
    def time_block(self) -> str:
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}"
        return ""

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
