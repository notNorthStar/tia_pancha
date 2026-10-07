"""Orbe animado que refleja el estado de la asistente."""
import math
import random
import tkinter as tk

from core.state import State
from ui.theme import STATE_COLORS

RGB = tuple[float, float, float]
WHITE: RGB = (255, 255, 255)


def _hex_to_rgb(color: str) -> RGB:
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def _rgb_to_hex(rgb: RGB) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c))) for c in rgb)


def _mix(a: RGB, b: RGB, t: float) -> RGB:
    return tuple(x + (y - x) * t for x, y in zip(a, b))


class Orb(tk.Canvas):
    FPS = 30

    def __init__(self, master, size: int, bg: str):
        super().__init__(master, width=size, height=size, bg=bg, highlightthickness=0, bd=0)
        self.center = size / 2
        self.base_radius = size * 0.22
        self._bg = _hex_to_rgb(bg)
        self._state = State.IDLE
        self._color = _hex_to_rgb(STATE_COLORS[State.IDLE])
        self._target = self._color
        self._t = 0.0
        self._level = 0.0          # "volumen" simulado al hablar
        self._ripples: list[float] = []
        self._next_ripple = 0.0
        self._tick()

    def set_state(self, state: State) -> None:
        self._state = state
        self._target = _hex_to_rgb(STATE_COLORS[state])

    # ---------- animación ----------

    def _tick(self) -> None:
        dt = 1 / self.FPS
        self._t += dt
        self._color = _mix(self._color, self._target, 0.12)  # transición suave de color

        self.delete("all")
        radius = self._radius()
        self._draw_glow(radius)
        if self._state is State.LISTENING:
            self._draw_ripples(radius, dt)
        else:
            self._ripples.clear()
        self._draw_sphere(radius)
        if self._state is State.PROCESSING:
            self._draw_spinner(radius)

        self.after(int(1000 / self.FPS), self._tick)

    def _radius(self) -> float:
        t, r = self._t, self.base_radius
        if self._state is State.IDLE:
            return r + 3 * math.sin(t * 2 * math.pi / 3)           # respiración lenta
        if self._state is State.LISTENING:
            return r + 5 + 4 * math.sin(t * 2 * math.pi * 1.2)     # pulso atento
        if self._state is State.PROCESSING:
            return r * 0.94 + 2 * math.sin(t * 4)
        # SPEAKING: imita la amplitud de una voz
        target = abs(0.6 * math.sin(t * 9) + 0.4 * math.sin(t * 13.7)) * random.uniform(0.6, 1.0)
        self._level += (target - self._level) * 0.35
        return r + 14 * self._level

    def _circle(self, radius: float, dx: float = 0, dy: float = 0, **kwargs) -> None:
        cx, cy = self.center + dx, self.center + dy
        self.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, **kwargs)

    def _draw_glow(self, radius: float) -> None:
        for i in range(8, 0, -1):
            color = _rgb_to_hex(_mix(self._color, self._bg, 0.55 + i * 0.055))
            self._circle(radius + i * 6, fill=color, outline="")

    def _draw_sphere(self, radius: float) -> None:
        # Capas cada vez más claras desplazadas hacia arriba-izquierda = efecto 3D
        layers = 14
        for k in range(layers):
            f = k / layers
            color = _rgb_to_hex(_mix(self._color, WHITE, f * 0.55))
            self._circle(radius * (1 - f * 0.75), dx=-radius * 0.22 * f, dy=-radius * 0.28 * f,
                         fill=color, outline="")

    def _draw_ripples(self, radius: float, dt: float) -> None:
        if self._t >= self._next_ripple:
            self._ripples.append(0.0)
            self._next_ripple = self._t + 0.6
        lifetime = 1.4
        self._ripples = [age + dt for age in self._ripples if age + dt < lifetime]
        for age in self._ripples:
            progress = age / lifetime
            color = _rgb_to_hex(_mix(self._color, self._bg, progress))
            self._circle(radius + 8 + progress * 70, outline=color, width=2)

    def _draw_spinner(self, radius: float) -> None:
        r = radius + 16
        c = self.center
        color = _rgb_to_hex(_mix(self._color, WHITE, 0.3))
        start = -self._t * 360 * 1.1
        for offset in (0, 180):
            self.create_arc(c - r, c - r, c + r, c + r, start=start + offset, extent=70,
                            style="arc", outline=color, width=4)
