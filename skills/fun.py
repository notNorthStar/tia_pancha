"""Chistes, temporizadores y despedida."""
import random
import threading

from skills.base import SkillContext, skill

JOKES = [
    "¿Qué le dice una iguana a su hermana gemela? ¡Somos iguanitas!",
    "¿Por qué el libro de matemáticas está triste? Porque tiene muchos problemas.",
    "¿Cuál es el café más peligroso del mundo? El ex-preso.",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
    "¿Qué le dijo un techo a otro techo? Techo de menos.",
    "¿Cómo se despiden los químicos? Ácido un placer.",
    "Mamá, mamá, en la escuela me dicen distraído. Niño, tu casa es la de enfrente.",
]

NUMBER_WORDS = {
    "un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "quince": 15,
    "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
}
UNIT_SECONDS = {"segundo": 1, "minuto": 60, "hora": 3600}

TIMER_WORDS = r"\b(?:temporizador|alarma|timer|cronometro|avisame|recuerdame)\b"


@skill(
    "chiste",
    patterns=[r"\bchiste\b", r"\bhazme reir\b"],
    phrases=["cuentame un chiste"],
    priority=10,
)
def joke(ctx: SkillContext) -> str:
    return random.choice(JOKES)


@skill(
    "temporizador",
    patterns=[
        TIMER_WORDS + r".*?\b(?P<half>media hora)\b",
        TIMER_WORDS + r".*?\b(?P<n>\d+|" + "|".join(NUMBER_WORDS) + r")\s+(?P<unit>segundo|minuto|hora)s?\b",
        TIMER_WORDS,
    ],
    priority=10,
)
def timer(ctx: SkillContext) -> str:
    if "half" in ctx.slots:
        amount, unit = 30, "minuto"
    elif "n" in ctx.slots:
        raw = ctx.slots["n"]
        amount = int(raw) if raw.isdigit() else NUMBER_WORDS[raw]
        unit = ctx.slots["unit"]
    else:
        return "¿De cuánto tiempo, corazón? Dime, por ejemplo: pon un temporizador de 5 minutos."

    label = f"{'un' if amount == 1 else amount} {unit}{'' if amount == 1 else 's'}"
    t = threading.Timer(
        amount * UNIT_SECONDS[unit],
        ctx.assistant.notify,
        args=[f"¡Tiempo, corazón! Ya pasaron {label}."],
    )
    t.daemon = True
    t.start()
    return f"Va, te aviso en {label}."


@skill(
    "despedida",
    patterns=[r"\b(?:adios|apagate|hasta luego|bye|nos vemos|cierrate|descansa)\b"],
    phrases=["adios tia"],
    priority=10,
)
def goodbye(ctx: SkillContext) -> str:
    ctx.assistant.request_shutdown()
    return "¡Adiós, corazón! Cuídate mucho."
