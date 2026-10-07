"""Orquestador: máquina de estados que corre en su propio hilo."""
import logging
import queue
import threading
import time
import winsound
from typing import Any, Callable

import config
from core import persona
from core.intent_parser import parse
from core.state import State
from core.stt import NetworkError, SpeechToText
from core.tts import TextToSpeech
from core.wake_word import detect
from skills.base import SkillContext

log = logging.getLogger(__name__)

# emit(tipo, dato) -> la UI recibe: ("state", State), ("user", str), ("tia", str), ("error", str), ("quit", None)
Emitter = Callable[[str, Any], None]


class Assistant:
    def __init__(self, emit: Emitter):
        self._emit = emit
        self._activate = threading.Event()
        self._stop = threading.Event()
        self._inbox: queue.Queue[tuple[str, str]] = queue.Queue()
        self._shutdown_requested = False
        self._offline_warned = False
        self._thread = threading.Thread(target=self._run, name="TiaPancha", daemon=True)
        self.stt: SpeechToText | None = None
        self.tts: TextToSpeech | None = None

    # ---------- API pública (segura para llamar desde la UI u otros hilos) ----------

    def start(self) -> None:
        self._thread.start()

    def activate(self) -> None:
        """Equivale a decir "Tía Pancha" (botón / atajo de teclado)."""
        self._activate.set()

    def submit_text(self, text: str) -> None:
        """Petición escrita: se procesa sin necesidad de decir el nombre."""
        self._inbox.put(("text", text))

    def notify(self, text: str) -> None:
        """Mensaje que la tía debe decir por iniciativa propia (ej. un temporizador)."""
        self._inbox.put(("notify", text))

    def request_shutdown(self) -> None:
        self._shutdown_requested = True

    def stop(self) -> None:
        self._stop.set()

    # ---------- Ciclo principal ----------

    def _run(self) -> None:
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        try:
            with self.stt.open():
                self._say(persona.GREETING)
                self._loop(with_mic=True)
        except OSError as exc:  # PyAudio no encontró micrófono
            log.error("Micrófono no disponible: %s", exc)
            self._emit("error", persona.NO_MIC)
            self._loop(with_mic=False)

    def _loop(self, with_mic: bool) -> None:
        while not self._stop.is_set():
            self._process_inbox()
            if self._stop.is_set():
                break
            if self._activate.is_set():
                self._activate.clear()
                if with_mic:
                    self._command_turn()
                else:
                    self._say(persona.NO_MIC)
                continue
            if with_mic:
                self._wait_for_wake_word()
            else:
                time.sleep(0.1)

    def _process_inbox(self) -> None:
        while not self._inbox.empty():
            kind, text = self._inbox.get_nowait()
            if kind == "text":
                self._handle(text)
            elif kind == "notify":
                self._say(text)

    def _wait_for_wake_word(self) -> None:
        audio = self.stt.listen(config.WAKE_LISTEN_TIMEOUT, config.WAKE_PHRASE_LIMIT)
        if audio is None:
            return
        text = self._transcribe(audio)
        if not text:
            return

        woke, request = detect(text)
        if not woke:
            log.debug("Ignorado (sin nombre): %s", text)
            return

        self._emit("user", text)
        if request:
            self._handle(request)
        else:
            self._command_turn()

    def _command_turn(self) -> None:
        """Escucha una petición después de activarse por nombre o botón."""
        self._set_state(State.LISTENING)
        winsound.Beep(880, 120)
        audio = self.stt.listen(config.COMMAND_LISTEN_TIMEOUT, config.COMMAND_PHRASE_LIMIT)
        winsound.Beep(660, 90)

        if audio is None:
            self._say(persona.pick(persona.NOT_HEARD))
            return

        self._set_state(State.PROCESSING)
        text = self._transcribe(audio)
        if text is None:
            self._say(persona.pick(persona.NOT_UNDERSTOOD))
            return

        self._emit("user", text)
        self._handle(text)

    def _handle(self, text: str) -> None:
        self._set_state(State.PROCESSING)
        intent = parse(text)
        if intent is None:
            reply = persona.pick(persona.FALLBACKS)
        else:
            log.info("Intención: %s %s", intent.skill.name, intent.slots)
            try:
                reply = intent.skill.handler(SkillContext(intent.text, intent.slots, self))
            except Exception:
                log.exception("Error ejecutando %s", intent.skill.name)
                reply = persona.ERROR

        if reply:
            self._say(reply)
        else:
            self._set_state(State.IDLE)

        if self._shutdown_requested:
            self._stop.set()
            self._emit("quit", None)

    # ---------- Utilidades ----------

    def _transcribe(self, audio) -> str | None:
        try:
            text = self.stt.transcribe(audio)
        except NetworkError as exc:
            log.warning("Sin conexión: %s", exc)
            if not self._offline_warned:
                self._offline_warned = True
                self._emit("error", persona.NO_INTERNET)
            self._set_state(State.IDLE)
            time.sleep(3)
            return None
        self._offline_warned = False
        return text

    def _say(self, text: str) -> None:
        self._emit("tia", text)
        self._set_state(State.SPEAKING)
        self.tts.speak(text)
        self._set_state(State.IDLE)

    def _set_state(self, state: State) -> None:
        self._emit("state", state)
