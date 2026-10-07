"""Frases con la personalidad de la Tía Pancha."""
import random

GREETING = "¡Hola, corazón! Aquí está tu Tía Pancha. Llámame cuando me necesites."

INTRODUCTION = (
    "¡Hola! Soy la Tía Pancha, tu asistente de voz. "
    "Puedes llamarme Tía Pancha, Auntie Pancha, o simplemente Tía. "
    "Puedo abrir programas, buscar cosas en internet, decirte la hora, "
    "poner temporizadores y hasta contarte un chiste. ¿En qué te ayudo, mi cielo?"
)

HELP = (
    "Puedo abrir el navegador, el bloc de notas, la calculadora, Paint o el explorador de archivos; "
    "buscar en Google o en YouTube; decirte la hora y la fecha; subir o bajar el volumen; "
    "tomar capturas de pantalla; poner temporizadores y contarte chistes. "
    "Solo di «Tía Pancha» y lo que necesites."
)

FALLBACKS = [
    "Ay, corazón, eso todavía no lo sé hacer. Pregúntame qué puedo hacer.",
    "Mmm, no te entendí bien, mi cielo. ¿Me lo repites?",
    "Uy, esa no me la sé. Pero puedo abrirte programas o buscar algo en internet.",
]

NOT_HEARD = [
    "¿Mi cielo? No te escuché nada.",
    "Aquí sigo, corazón, pero no te oí.",
]

NOT_UNDERSTOOD = [
    "No te entendí bien, corazón. ¿Me lo repites?",
    "Perdón, mi cielo, se me fue. ¿Qué me decías?",
]

ERROR = "Ay, algo me salió mal haciendo eso. Inténtalo otra vez, corazón."

NO_INTERNET = "No tengo conexión a internet, corazón. Así no te puedo entender."

NO_MIC = "No encuentro un micrófono. Puedes escribirme abajo mientras tanto."


def pick(options: list[str]) -> str:
    return random.choice(options)
