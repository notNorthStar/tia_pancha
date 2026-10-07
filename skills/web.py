"""Navegador, búsquedas y sitios web."""
import webbrowser
from urllib.parse import quote_plus

from skills.base import SkillContext, skill

SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "gmail": "https://mail.google.com",
    "correo": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "github": "https://github.com",
    "wikipedia": "https://es.wikipedia.org",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
}


@skill(
    "buscar_youtube",
    patterns=[r"\b(?:pon|ponme|reproduce|reproduceme|busca|buscame|buscar)\s+(?P<q>.+?)\s+en youtube\b"],
    priority=30,
)
def search_youtube(ctx: SkillContext) -> str:
    query = ctx.slots["q"]
    webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(query)}")
    return f"Te busqué {query} en YouTube."


@skill(
    "buscar_google",
    patterns=[r"\b(?:busca|buscame|buscar|investiga|googlea)\s+(?:en (?:google|internet)\s+)?"
              r"(?P<q>.+?)(?:\s+en (?:google|internet))?$"],
    priority=20,
)
def search_google(ctx: SkillContext) -> str:
    query = ctx.slots["q"]
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
    return f"Esto encontré sobre {query}, corazón."


@skill(
    "abrir_sitio",
    patterns=[r"\b(?:abre|abrir|abreme|entra a|ve a|llevame a)\s+(?:el |la |mi )?"
              r"(?P<site>" + "|".join(SITES) + r")\b"],
    priority=15,
)
def open_site(ctx: SkillContext) -> str:
    site = ctx.slots["site"]
    webbrowser.open(SITES[site])
    return f"Ahí tienes {site.capitalize()}."


@skill(
    "abrir_navegador",
    patterns=[r"\b(?:abre|abrir|abreme|inicia)\b.*\b(?:navegador|chrome|edge|firefox|internet)\b"],
    phrases=["abre el navegador", "abre chrome", "abre internet"],
    priority=10,
)
def open_browser(ctx: SkillContext) -> str:
    webbrowser.open("https://www.google.com")
    return "Listo, ya te abrí el navegador."
