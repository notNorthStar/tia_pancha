from enum import Enum, auto


class State(Enum):
    """Estados de la máquina de estados del asistente."""
    IDLE = auto()        # Reposo: solo espera su nombre o el botón
    LISTENING = auto()   # Grabando la petición
    PROCESSING = auto()  # Transcribiendo / interpretando / ejecutando
    SPEAKING = auto()    # Respondiendo en voz alta
