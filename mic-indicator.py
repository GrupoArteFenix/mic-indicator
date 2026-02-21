#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indicador de micrófono para XFCE - Arte Fénix
Estados: Gris → Rojo → Verde → Celeste → Gris
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import os
import signal
import sys

# ── Rutas ────────────────────────────────────────────────────────────────────
NERD_DICTATION_DIR = "/home/equipo_fenix/nerd-dictation"
VENV_PYTHON        = f"{NERD_DICTATION_DIR}/venv/bin/python3"
NERD_DICTATION_BIN = f"{NERD_DICTATION_DIR}/nerd-dictation"
MODEL_DIR          = f"{NERD_DICTATION_DIR}/model"
ICON_DIR           = "/usr/local/share/mic-indicator"
PID_FILE           = "/tmp/mic-indicator-dictation.pid"

# ── Estados ───────────────────────────────────────────────────────────────────
ESTADO_GRIS    = 0   # Apagado
ESTADO_ROJO    = 1   # Standby (venv activo, micro muteado)
ESTADO_VERDE   = 2   # Transcripción activa
ESTADO_CELESTE = 3   # Solo audio activo

NOMBRES = {
    ESTADO_GRIS:    "Apagado",
    ESTADO_ROJO:    "Standby",
    ESTADO_VERDE:   "Transcribiendo",
    ESTADO_CELESTE: "Solo audio",
}

ICONOS = {
    ESTADO_GRIS:    f"{ICON_DIR}/mic_gris.png",
    ESTADO_ROJO:    f"{ICON_DIR}/mic_rojo.png",
    ESTADO_VERDE:   f"{ICON_DIR}/mic_verde.png",
    ESTADO_CELESTE: f"{ICON_DIR}/mic_celeste.png",
}

# ── Fuente del micrófono USB ──────────────────────────────────────────────────
MIC_SOURCE = "alsa_input.usb-GeneralPlus_USB_Audio_Device-00.mono-fallback"

# ─────────────────────────────────────────────────────────────────────────────

def mutear_micro():
    subprocess.run(["pactl", "set-source-mute", MIC_SOURCE, "1"],
                   capture_output=True)

def desmutear_micro():
    subprocess.run(["pactl", "set-source-mute", MIC_SOURCE, "0"],
                   capture_output=True)

def iniciar_dictado():
    proc = subprocess.Popen(
        [VENV_PYTHON, NERD_DICTATION_BIN, "begin",
         f"--vosk-model-dir={MODEL_DIR}"],
        cwd=NERD_DICTATION_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))

def parar_dictado():
    # Intentar parada limpia con el comando end
    subprocess.run(
        [VENV_PYTHON, NERD_DICTATION_BIN, "end"],
        cwd=NERD_DICTATION_DIR,
        capture_output=True,
    )
    # Si quedó el PID, matar el proceso
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, ValueError):
            pass
        os.remove(PID_FILE)

# ─────────────────────────────────────────────────────────────────────────────

class MicIndicator:
    def __init__(self):
        self.estado = ESTADO_GRIS
        self.dictado_proceso = None

        # Crear el indicador
        self.indicator = AppIndicator3.Indicator.new(
            "mic-indicator",
            ICONOS[ESTADO_GRIS],
            AppIndicator3.IndicatorCategory.HARDWARE,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("Micrófono")

        # Menú
        self.menu = Gtk.Menu()
        self._construir_menu()
        self.indicator.set_menu(self.menu)

        # Estado inicial: todo muteado
        mutear_micro()

    def _construir_menu(self):
        # Limpiar menú anterior
        for child in self.menu.get_children():
            self.menu.remove(child)

        # Título informativo
        titulo = Gtk.MenuItem(label=f"🎙 Micrófono — {NOMBRES[self.estado]}")
        titulo.set_sensitive(False)
        self.menu.append(titulo)

        separador = Gtk.SeparatorMenuItem()
        self.menu.append(separador)

        # Botones de estado
        estados = [
            (ESTADO_GRIS,    "⚫  Apagado"),
            (ESTADO_ROJO,    "🔴  Standby"),
            (ESTADO_VERDE,   "🟢  Transcribir"),
            (ESTADO_CELESTE, "🔵  Solo audio"),
        ]

        for estado, etiqueta in estados:
            item = Gtk.MenuItem(label=etiqueta)
            if estado == self.estado:
                item.set_sensitive(False)  # Estado actual no clickable
            else:
                item.connect("activate", self._cambiar_estado, estado)
            self.menu.append(item)

        sep2 = Gtk.SeparatorMenuItem()
        self.menu.append(sep2)

        # Salir
        salir = Gtk.MenuItem(label="✖  Salir")
        salir.connect("activate", self._salir)
        self.menu.append(salir)

        self.menu.show_all()

    def _cambiar_estado(self, widget, nuevo_estado):
        estado_anterior = self.estado

        # ── Acciones de SALIDA del estado anterior ────────────────────────
        if estado_anterior == ESTADO_VERDE:
            parar_dictado()

        # ── Acciones de ENTRADA al nuevo estado ───────────────────────────
        if nuevo_estado == ESTADO_GRIS:
            mutear_micro()

        elif nuevo_estado == ESTADO_ROJO:
            mutear_micro()
            # venv ya está embebido en VENV_PYTHON, nada más que hacer

        elif nuevo_estado == ESTADO_VERDE:
            desmutear_micro()
            iniciar_dictado()

        elif nuevo_estado == ESTADO_CELESTE:
            desmutear_micro()

        # ── Actualizar estado e icono ──────────────────────────────────────
        self.estado = nuevo_estado
        self.indicator.set_icon_full(ICONOS[nuevo_estado], NOMBRES[nuevo_estado])
        self.indicator.set_title(f"Micrófono: {NOMBRES[nuevo_estado]}")
        self._construir_menu()

    def _salir(self, widget):
        parar_dictado()
        mutear_micro()
        Gtk.main_quit()


def main():
    # Manejo de señales para salida limpia
    signal.signal(signal.SIGTERM, lambda *a: Gtk.main_quit())
    signal.signal(signal.SIGINT,  lambda *a: Gtk.main_quit())

    app = MicIndicator()
    Gtk.main()


if __name__ == "__main__":
    main()
