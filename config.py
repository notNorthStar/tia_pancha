"""Configuración central de la Tía Pancha."""
from pathlib import Path

ASSISTANT_NAME = "Tía Pancha"

# --- Voz e idioma ---
LANGUAGE = "es-MX"                 # Idioma para el reconocimiento de Google
VOICE = "es-MX-DaliaNeural"        # Voz neural de edge-tts
VOICE_RATE = "+0%"                 # Velocidad de habla (ej. "+10%", "-5%")

# --- Wake word ---
# Nombres completos (se comparan con coincidencia difusa contra las 2 primeras palabras).
# Incluye variantes fonéticas de cómo Google suele transcribir "Auntie" en español.
WAKE_NAMES_FULL = [
    "tia pancha",
    "auntie pancha",
    "aunty pancha",
    "anti pancha",
    "ante pancha",
    "andy pancha",
    "onti pancha",
]
# Nombres cortos (deben ser exactamente la primera palabra de la frase).
WAKE_NAMES_SHORT = {"tia", "tita", "auntie", "aunty", "anti", "onti"}
# Muletillas que se ignoran antes del nombre ("oye tía", "hey auntie"...).
WAKE_FILLERS = {"oye", "hey", "ey", "hola", "ok", "okay", "oiga", "eh"}
WAKE_FUZZY_THRESHOLD = 80

# --- Reconocimiento de intenciones ---
INTENT_FUZZY_THRESHOLD = 75

# --- Micrófono (segundos) ---
AMBIENT_CALIBRATION = 1.0          # Calibración inicial del ruido ambiente
WAKE_LISTEN_TIMEOUT = 1            # Cada cuánto revisa botón / texto mientras espera
WAKE_PHRASE_LIMIT = 6              # Duración máxima de una frase en reposo
COMMAND_LISTEN_TIMEOUT = 6         # Cuánto espera a que empieces a hablar tras activarla
COMMAND_PHRASE_LIMIT = 10          # Duración máxima de una petición
PAUSE_THRESHOLD = 0.7              # Silencio que marca el fin de la frase

# --- Acciones ---
SCREENSHOT_DIR = Path.home() / "Pictures" / "Tia Pancha"
