"""Ventana principal: orbe, historial de conversación, botón y caja de texto."""
import queue

import customtkinter as ctk

from core.assistant import Assistant
from core.state import State
from ui import theme
from ui.orb import Orb


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=theme.BG)
        self.title("Tía Pancha")
        self.geometry("430x620+80+20")
        self.minsize(380, 560)

        self._events: queue.Queue = queue.Queue()
        self._state = State.IDLE
        self._build()

        # El asistente vive en otro hilo y se comunica con la UI solo a través de la cola
        self.assistant = Assistant(emit=lambda kind, data: self._events.put((kind, data)))
        self.bind("<Control-space>", lambda _e: self._on_activate())
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(40, self._poll_events)
        self.assistant.start()

    # ---------- construcción ----------

    def _build(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(16, 0))
        ctk.CTkLabel(header, text="Tía Pancha", text_color=theme.TEXT,
                     font=(theme.FONT, 28, "bold")).pack()
        ctk.CTkLabel(header, text="Tu asistente de confianza", text_color=theme.MUTED,
                     font=(theme.FONT, 13)).pack()

        self.orb = Orb(self, size=210, bg=theme.BG)
        self.orb.pack()

        self.status = ctk.CTkLabel(self, text=theme.STATUS_TEXT[State.IDLE],
                                   text_color=theme.MUTED, font=(theme.FONT, 14))
        self.status.pack(pady=(0, 10))

        self.chat = ctk.CTkScrollableFrame(self, fg_color=theme.CARD, corner_radius=16)
        self.chat.pack(fill="both", expand=True, padx=18)

        input_row = ctk.CTkFrame(self, fg_color="transparent")
        input_row.pack(fill="x", padx=18, pady=(12, 0))
        self.entry = ctk.CTkEntry(input_row, placeholder_text="Escríbele a la tía…", height=40,
                                  corner_radius=20, fg_color=theme.CARD, border_width=0,
                                  text_color=theme.TEXT, font=(theme.FONT, 13))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self._on_send())
        ctk.CTkButton(input_row, text="Enviar", width=80, height=40, corner_radius=20,
                      fg_color=theme.USER_BUBBLE, hover_color=theme.TIA_BUBBLE,
                      font=(theme.FONT, 13, "bold"), command=self._on_send).pack(side="left", padx=(8, 0))

        self.mic_button = ctk.CTkButton(self, text="Hablar con la Tía", height=54, corner_radius=27,
                                        fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
                                        font=(theme.FONT, 16, "bold"), command=self._on_activate)
        self.mic_button.pack(fill="x", padx=18, pady=(12, 4))
        ctk.CTkLabel(self, text="Atajo: Ctrl + Espacio", text_color=theme.MUTED,
                     font=(theme.FONT, 11)).pack(pady=(0, 12))

    def _add_message(self, text: str, from_user: bool, color: str | None = None) -> None:
        row = ctk.CTkFrame(self.chat, fg_color="transparent")
        row.pack(fill="x", pady=4, padx=4)
        bubble = ctk.CTkLabel(
            row, text=text, wraplength=280, justify="left", anchor="w",
            fg_color=theme.USER_BUBBLE if from_user else theme.TIA_BUBBLE,
            text_color=color or theme.TEXT, corner_radius=14,
            font=(theme.FONT, 13), padx=12, pady=8,
        )
        bubble.pack(side="right" if from_user else "left")
        self.after(30, lambda: self.chat._parent_canvas.yview_moveto(1.0))

    # ---------- eventos de la UI ----------

    def _on_activate(self) -> None:
        if self._state is State.IDLE:
            self.status.configure(text="Ahí voy…", text_color=theme.TEXT)
            self.assistant.activate()

    def _on_send(self) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._add_message(text, from_user=True)
        self.assistant.submit_text(text)

    def _on_close(self) -> None:
        self.assistant.stop()
        self.destroy()

    # ---------- eventos del asistente ----------

    def _poll_events(self) -> None:
        while not self._events.empty():
            kind, data = self._events.get_nowait()
            if kind == "state":
                self._apply_state(data)
            elif kind == "user":
                self._add_message(data, from_user=True)
            elif kind == "tia":
                self._add_message(data, from_user=False)
            elif kind == "error":
                self.status.configure(text=data, text_color=theme.ERROR)
                self._add_message(data, from_user=False, color=theme.ERROR)
            elif kind == "quit":
                self.after(400, self._on_close)
                return
        self.after(40, self._poll_events)

    def _apply_state(self, state: State) -> None:
        self._state = state
        self.orb.set_state(state)
        self.status.configure(text=theme.STATUS_TEXT[state], text_color=theme.MUTED)
        self.mic_button.configure(state="normal" if state is State.IDLE else "disabled")
