"""Convierte texto en una intención (skill) con sus datos (slots)."""
from dataclasses import dataclass

from rapidfuzz import fuzz

import config
import skills  # noqa: F401  (importarlo registra todas las acciones)
from core.text_utils import normalize
from skills.base import REGISTRY, Skill


@dataclass
class Intent:
    skill: Skill
    slots: dict[str, str]
    text: str


def parse(text: str) -> Intent | None:
    norm = normalize(text)
    if not norm:
        return None

    ordered = sorted(REGISTRY, key=lambda s: -s.priority)

    # 1) Patrones regex: precisos y capaces de extraer datos ("busca {q} en youtube")
    for skill in ordered:
        for pattern in skill.patterns:
            match = pattern.search(norm)
            if match:
                slots = {k: v for k, v in match.groupdict().items() if v}
                return Intent(skill, slots, norm)

    # 2) Coincidencia difusa contra frases de ejemplo: tolera errores de transcripción
    best_skill, best_score = None, 0.0
    for skill in ordered:
        for phrase in skill.phrases:
            score = fuzz.ratio(norm, phrase)
            if score > best_score:
                best_skill, best_score = skill, score

    if best_skill and best_score >= config.INTENT_FUZZY_THRESHOLD:
        return Intent(best_skill, {}, norm)
    return None
