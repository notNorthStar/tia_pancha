"""Texto a voz: edge-tts (voz neural, online) con pyttsx3 como respaldo offline."""
import asyncio
import logging
import os
import tempfile
import time

import edge_tts
import pygame

import config

log = logging.getLogger(__name__)


class TextToSpeech:
    def __init__(self, voice: str = config.VOICE, rate: str = config.VOICE_RATE):
        self.voice = voice
        self.rate = rate
        pygame.mixer.init()
        self._tmpdir = tempfile.mkdtemp(prefix="tia_pancha_")
        self._counter = 0
        self._offline_engine = None

    def speak(self, text: str) -> None:
        try:
            self._speak_online(text)
        except Exception as exc:  # sin internet, servicio caído, etc.
            log.warning("edge-tts falló (%s); usando voz de Windows", exc)
            self._speak_offline(text)

    def _speak_online(self, text: str) -> None:
        # Se alternan dos archivos porque Windows bloquea el que pygame tiene cargado.
        self._counter += 1
        path = os.path.join(self._tmpdir, f"voz_{self._counter % 2}.mp3")
        asyncio.run(edge_tts.Communicate(text, self.voice, rate=self.rate).save(path))

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        pygame.mixer.music.unload()

    def _speak_offline(self, text: str) -> None:
        if self._offline_engine is None:
            import pyttsx3

            self._offline_engine = pyttsx3.init()
            for voice in self._offline_engine.getProperty("voices"):
                if "spanish" in voice.name.lower() or "es-" in voice.id.lower():
                    self._offline_engine.setProperty("voice", voice.id)
                    break
        self._offline_engine.say(text)
        self._offline_engine.runAndWait()
