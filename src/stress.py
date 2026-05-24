from enum import Enum, auto

class QMetric(Enum):
    ALTO = "ALTO", "#F54927"
    MEDIO = "MEDIO", "#F5B027"
    BAJO = "BAJO", "#27F5B0"
    
    def __init__(self, label, color):
        self.label = label
        self.color = color

def get_stress_level(responses) -> tuple[int, QMetric]:
    score = sum(responses)
    if score <= 6:
        return score, QMetric.BAJO 
    elif score <= 13:
        return score, QMetric.MEDIO
    else:
        return score, QMetric.ALTO