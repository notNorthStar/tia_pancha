"""Voz a texto con SpeechRecognition + Google (online)."""
from contextlib import contextmanager

import speech_recognition as sr

import config


class NetworkError(Exception):
    """No se pudo contactar al servicio de reconocimiento."""


class SpeechToText:
    def __init__(self, language: str = config.LANGUAGE):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = config.PAUSE_THRESHOLD
        self.source = None

    @contextmanager
    def open(self):
        """Mantiene el micrófono abierto durante toda la vida del asistente."""
        with sr.Microphone() as source:
            self.source = source
            self.recognizer.adjust_for_ambient_noise(source, duration=config.AMBIENT_CALIBRATION)
            try:
                yield self
            finally:
                self.source = None

    def listen(self, timeout: float, phrase_time_limit: float) -> sr.AudioData | None:
        """Graba una frase. Devuelve None si nadie empezó a hablar antes del timeout."""
        try:
            return self.recognizer.listen(
                self.source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return None

    def transcribe(self, audio: sr.AudioData) -> str | None:
        """Devuelve el texto reconocido, o None si no se entendió nada."""
        try:
            return self.recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return None
        except sr.RequestError as exc:
            raise NetworkError(str(exc)) from exc
