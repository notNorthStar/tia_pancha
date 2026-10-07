"""Tía Pancha — asistente de voz. Ejecutar con: python main.py"""
import logging
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import customtkinter as ctk  # noqa: E402

from ui.main_window import MainWindow  # noqa: E402


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    ctk.set_appearance_mode("dark")
    MainWindow().mainloop()


if __name__ == "__main__":
    main()
