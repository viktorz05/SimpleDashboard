from enum import Enum, auto


class QMetric(Enum):
    ALTO = 10
    MEDIO = 5
    BAJO = 0

def get_stress_level(responses):
    score = sum(responses)
    if score < 6:
        return QMetric.BAJO 
    elif score < 14:
        return QMetric.MEDIO
    else:
        return QMetric.ALTO