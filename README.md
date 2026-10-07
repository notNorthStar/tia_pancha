# Tía Pancha 🎙️

Asistente de voz de escritorio (tipo Alexa) en Python, para la materia de Advanced User Interfaces.

## Cómo usarla

1. Di **"Tía Pancha"**, **"Auntie Pancha"**, **"Tía"** o **"Auntie"**, presiona **Hablar con la Tía** o usa **Ctrl + Espacio**.
2. Pide algo. También puedes decirlo todo junto: *"Tía Pancha, abre el bloc de notas"*.
3. Si no quieres hablar, puedes escribirle en la caja de texto.

| Ejemplo | Acción |
|---|---|
| "Preséntate" / "¿Qué puedes hacer?" | Presentación / ayuda |
| "Abre el navegador / bloc de notas / calculadora / Paint / explorador" | Abre la aplicación |
| "Abre YouTube / Gmail / GitHub…" | Abre el sitio |
| "Busca *recetas de mole* en Google" | Búsqueda en Google |
| "Pon *Bad Bunny* en YouTube" | Búsqueda en YouTube |
| "¿Qué hora es?" / "¿Qué día es hoy?" | Hora / fecha |
| "Sube / baja el volumen", "Silencio" | Volumen del sistema |
| "Toma una captura de pantalla" | Guarda en `Imágenes/Tia Pancha` |
| "Pon un temporizador de 5 minutos" | Avisa con voz al terminar |
| "Cuéntame un chiste" | Chiste |
| "Adiós" | Cierra la app |

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Requiere internet: el reconocimiento de voz usa Google y la voz usa edge-tts. Si la voz no tiene conexión, cae a la voz de Windows.

## Arquitectura

```
main.py              → arranca la UI
config.py            → wake words, voz, tiempos
core/assistant.py    → máquina de estados (REPOSO → ESCUCHANDO → PROCESANDO → HABLANDO) en un hilo
core/wake_word.py    → detecta el nombre al inicio de la frase (con coincidencia difusa)
core/stt.py          → voz a texto (SpeechRecognition + Google)
core/tts.py          → texto a voz (edge-tts, respaldo pyttsx3)
core/intent_parser.py→ texto → acción (regex con datos + coincidencia difusa)
skills/              → una acción por función, registrada con @skill
ui/                  → ventana CustomTkinter y orbe animado
```

La UI y el asistente solo se comunican mediante una cola de eventos, así la ventana nunca se congela.

### Agregar una acción nueva

```python
# skills/mi_modulo.py  (e importarlo en skills/__init__.py)
from skills.base import SkillContext, skill

@skill("saludo_profe", patterns=[r"\bsaluda al profe\b"], phrases=["saluda al profe"], priority=10)
def greet_teacher(ctx: SkillContext) -> str:
    return "¡Buenas, profe! Póngale diez a este equipo."
```
