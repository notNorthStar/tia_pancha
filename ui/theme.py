from core.state import State

BG = "#14121f"
CARD = "#1e1b2e"
TEXT = "#ede9fe"
MUTED = "#a19cb8"
ERROR = "#f87171"
ACCENT = "#8b5cf6"
ACCENT_HOVER = "#7c3aed"
USER_BUBBLE = "#2e2a45"
TIA_BUBBLE = "#4c1d95"

FONT = "Segoe UI"

# Color del orbe en cada estado
STATE_COLORS = {
    State.IDLE: "#8b5cf6",        # morado: en reposo
    State.LISTENING: "#22d3ee",   # cian: escuchando
    State.PROCESSING: "#f59e0b",  # ámbar: pensando
    State.SPEAKING: "#ec4899",    # rosa: hablando
}

STATUS_TEXT = {
    State.IDLE: "Di «Tía Pancha» o presiona el botón",
    State.LISTENING: "Te escucho…",
    State.PROCESSING: "Déjame pensar…",
    State.SPEAKING: "Hablando…",
}
