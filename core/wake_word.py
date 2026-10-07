"""Detección del nombre de la asistente dentro de una frase transcrita."""
from rapidfuzz import fuzz

import config
from core.text_utils import normalize


def detect(text: str) -> tuple[bool, str]:
    """Indica si la frase empieza con el nombre de la tía.

    Devuelve (activada, resto_de_la_frase). Así "Tía Pancha, abre el bloc de notas"
    activa a la asistente y entrega "abre el bloc de notas" como petición.
    """
    words = normalize(text).split()
    while words and words[0] in config.WAKE_FILLERS:
        words.pop(0)
    if not words:
        return False, ""

    # Nombre completo: tolera errores de transcripción ("tía plancha", "tía pancho"...)
    if len(words) >= 2:
        pair = " ".join(words[:2])
        for name in config.WAKE_NAMES_FULL:
            if fuzz.ratio(pair, name) >= config.WAKE_FUZZY_THRESHOLD:
                return True, " ".join(words[2:])

    if words[0] in config.WAKE_NAMES_SHORT:
        return True, " ".join(words[1:])

    return False, ""
