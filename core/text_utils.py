import re
import unicodedata


def normalize(text: str) -> str:
    """Minúsculas, sin acentos, sin signos de puntuación y con espacios simples."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
