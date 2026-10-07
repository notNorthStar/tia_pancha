"""Registro de acciones. Cada acción se registra sola con el decorador @skill."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from core.text_utils import normalize

if TYPE_CHECKING:
    from core.assistant import Assistant


@dataclass
class SkillContext:
    text: str                 # petición normalizada (minúsculas, sin acentos)
    slots: dict[str, str]     # datos extraídos por el patrón, ej. {"q": "gatos"}
    assistant: Assistant


Handler = Callable[[SkillContext], "str | None"]


@dataclass
class Skill:
    name: str
    handler: Handler
    patterns: list[re.Pattern]   # se prueban primero (sobre texto normalizado)
    phrases: list[str]           # ejemplos para la coincidencia difusa
    priority: int = 0            # mayor prioridad = se evalúa antes


REGISTRY: list[Skill] = []


def register(name: str, handler: Handler, patterns=(), phrases=(), priority: int = 0) -> None:
    REGISTRY.append(Skill(
        name=name,
        handler=handler,
        patterns=[re.compile(p) for p in patterns],
        phrases=[normalize(p) for p in phrases],
        priority=priority,
    ))


def skill(name: str, patterns=(), phrases=(), priority: int = 0):
    """Decorador para registrar una acción.

    @skill("hora", patterns=[r"\\bque hora\\b"], phrases=["que hora es"])
    def tell_time(ctx): return "Son las..."
    """
    def decorator(fn: Handler) -> Handler:
        register(name, fn, patterns, phrases, priority)
        return fn
    return decorator
