"""Volumen y capturas de pantalla."""
from datetime import datetime

import pyautogui

import config
from skills.base import SkillContext, skill

VOLUME_STEPS = 5  # cada pulsación de tecla multimedia = 2 %


@skill(
    "subir_volumen",
    patterns=[r"\b(?:sube|subele|subir|aumenta|aumentale|mas)\b.*\bvolumen\b",
              r"\bvolumen\b.*\b(?:arriba|mas alto)\b"],
    phrases=["sube el volumen"],
    priority=10,
)
def volume_up(ctx: SkillContext) -> str:
    pyautogui.press("volumeup", presses=VOLUME_STEPS)
    return "Ya le subí, corazón."


@skill(
    "bajar_volumen",
    patterns=[r"\b(?:baja|bajale|bajar|disminuye|reduce|menos)\b.*\bvolumen\b",
              r"\bvolumen\b.*\b(?:abajo|mas bajo)\b"],
    phrases=["baja el volumen"],
    priority=10,
)
def volume_down(ctx: SkillContext) -> str:
    pyautogui.press("volumedown", presses=VOLUME_STEPS)
    return "Ya le bajé."


@skill(
    "silenciar",
    patterns=[r"\b(?:silencio|silencia|mutea|mute|quita el sonido|activa el sonido)\b"],
    phrases=["silencia la computadora"],
    priority=10,
)
def mute(ctx: SkillContext) -> None:
    pyautogui.press("volumemute")
    return None  # si silenciamos, no tiene sentido responder en voz alta


@skill(
    "captura_pantalla",
    patterns=[r"\b(?:captura|screenshot|pantallazo|foto de (?:la )?pantalla)\b"],
    phrases=["toma una captura de pantalla"],
    priority=10,
)
def screenshot(ctx: SkillContext) -> str:
    config.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = config.SCREENSHOT_DIR / f"captura_{datetime.now():%Y%m%d_%H%M%S}.png"
    pyautogui.screenshot(str(path))
    return "Listo, guardé la captura en tu carpeta de Imágenes, en Tía Pancha."
