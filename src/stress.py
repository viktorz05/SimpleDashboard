from enum import Enum, auto
QUESTIONS = [
    "¿Te has sentido nervioso o estresado?",
    "¿Has sentido que no puedes controlar tus preocupaciones?",
    "¿Te has sentido sobrecargado de tareas? ",
    "¿Te has sentido incapaz de manejar tus responsabilidades? ",
    "¿Te has sentido frustrado por situaciones fuera de tu control? "
]

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