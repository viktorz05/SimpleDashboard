QUESTIONS = [
    "¿Te has sentido nervioso o estresado?",
    "¿Has sentido que no puedes controlar tus preocupaciones?",
    "¿Te has sentido sobrecargado de tareas? ",
    "¿Te has sentido incapaz de manejar tus responsabilidades? ",
    "¿Te has sentido frustrado por situaciones fuera de tu control? "
]

def get_stress_level(responses):
    score = sum(responses)
    if score <= 5:
        return "Bajo"
    elif score <= 10:
        return "Moderado"
    else:
        return "Alto"