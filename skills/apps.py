"""Abrir programas de Windows."""
import random
import subprocess

from skills.base import SkillContext, register

OPEN_VERB = r"\b(abre|abrir|abreme|inicia|ejecuta|lanza|pon)\b.*"

# (nombre, patrón del programa, comando, cómo lo nombra la tía, frases de ejemplo)
APPS = [
    ("bloc_de_notas", r"\b(bloc|block|blog|blop) de notas\b|\bnotepad\b|\bnotas\b",
     ["notepad.exe"], "el bloc de notas", ["abre el bloc de notas", "abre notepad"]),
    ("calculadora", r"\bcalculadora\b",
     ["calc.exe"], "la calculadora", ["abre la calculadora"]),
    ("explorador", r"\bexplorador\b|\bmis archivos\b|\bmis documentos\b",
     ["explorer.exe"], "el explorador de archivos", ["abre el explorador de archivos"]),
    ("paint", r"\bpaint\b",
     ["mspaint.exe"], "Paint", ["abre paint"]),
]

REPLIES = [
    "Listo, ya te abrí {}.",
    "Ahí está {}, corazón.",
    "Abriendo {}.",
]


def _launcher(command: list[str], label: str):
    def handler(ctx: SkillContext) -> str:
        subprocess.Popen(command)
        return random.choice(REPLIES).format(label)
    return handler


for name, app_pattern, command, label, phrases in APPS:
    register(
        name,
        _launcher(command, label),
        patterns=[OPEN_VERB + f"(?:{app_pattern})"],
        phrases=phrases,
        priority=10,
    )
