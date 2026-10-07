"""Presentación, ayuda, hora, fecha y charla básica."""
import random
from datetime import datetime

from core import persona
from skills.base import SkillContext, skill

DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
          "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


@skill(
    "presentarse",
    patterns=[r"\b(?:presentate|quien eres|como te llamas|que eres|cual es tu nombre)\b"],
    phrases=["presentate", "quien eres"],
    priority=10,
)
def introduce(ctx: SkillContext) -> str:
    return persona.INTRODUCTION


@skill(
    "ayuda",
    patterns=[r"\bque (?:puedes|sabes) hacer\b", r"\bayuda(?:me)?\b", r"\bcomandos\b"],
    phrases=["que puedes hacer"],
    priority=10,
)
def help_(ctx: SkillContext) -> str:
    return persona.HELP


@skill(
    "hora",
    patterns=[r"\bque hora\b", r"\bla hora\b"],
    phrases=["que hora es"],
    priority=10,
)
def tell_time(ctx: SkillContext) -> str:
    now = datetime.now()
    hour12 = now.hour % 12 or 12
    if now.hour < 6:
        period = "de la madrugada"
    elif now.hour < 12:
        period = "de la mañana"
    elif now.hour < 20:
        period = "de la tarde"
    else:
        period = "de la noche"
    prefix = "Es la" if hour12 == 1 else "Son las"
    return f"{prefix} {hour12}:{now.minute:02d} {period}."


@skill(
    "fecha",
    patterns=[r"\bque (?:dia|fecha)\b", r"\bfecha de hoy\b", r"\ba cuanto estamos\b"],
    phrases=["que dia es hoy"],
    priority=10,
)
def tell_date(ctx: SkillContext) -> str:
    now = datetime.now()
    return f"Hoy es {DAYS[now.weekday()]} {now.day} de {MONTHS[now.month - 1]} de {now.year}."


@skill(
    "como_estas",
    patterns=[r"\bcomo (?:estas|te va|te sientes)\b"],
    phrases=["como estas"],
    priority=5,
)
def how_are_you(ctx: SkillContext) -> str:
    return random.choice([
        "¡Muy bien, corazón! Gracias por preguntar. ¿Y tú cómo estás?",
        "Aquí andamos, con mucha energía para ayudarte.",
    ])


@skill(
    "gracias",
    patterns=[r"\bgracias\b"],
    priority=5,
)
def thanks(ctx: SkillContext) -> str:
    return random.choice(["De nada, mi cielo.", "Para eso estoy, corazón.", "Con mucho gusto."])


@skill(
    "saludo",
    patterns=[r"^(?:hola|buenos dias|buenas tardes|buenas noches|buenas|que onda|que tal)\b"],
    priority=0,
)
def greet(ctx: SkillContext) -> str:
    return random.choice([
        "¡Hola, corazón! ¿En qué te ayudo?",
        "¡Quihubo, mi cielo! ¿Qué necesitas?",
    ])
