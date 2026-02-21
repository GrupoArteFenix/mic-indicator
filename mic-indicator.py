#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indicador de micrófono para XFCE - Arte Fénix
Estados: Gris → Rojo → Verde → Celeste → Gris
Con banner Arte Fénix, botón de donación y cierre suave (queda en gris)
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import os
import signal
import sys
import webbrowser

# ── Rutas ────────────────────────────────────────────────────────────────────
NERD_DICTATION_DIR = "/home/equipo_fenix/nerd-dictation"
VENV_PYTHON        = f"{NERD_DICTATION_DIR}/venv/bin/python3"
NERD_DICTATION_BIN = f"{NERD_DICTATION_DIR}/nerd-dictation"
MODEL_DIR          = f"{NERD_DICTATION_DIR}/model"
ICON_DIR           = "/usr/local/share/mic-indicator"
PID_FILE           = "/tmp/mic-indicator-dictation.pid"

# ── URLs ──────────────────────────────────────────────────────────────────────
URL_GITHUB      = "https://github.com/GrupoArteFenix"
URL_SPONSORS    = "https://github.com/sponsors/GrupoArteFenix"
URL_REPO        = "https://github.com/GrupoArteFenix/mic-indicator"

# ── Estados ───────────────────────────────────────────────────────────────────
ESTADO_GRIS    = 0
ESTADO_ROJO    = 1
ESTADO_VERDE   = 2
ESTADO_CELESTE = 3

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
    subprocess.run(
        [VENV_PYTHON, NERD_DICTATION_BIN, "end"],
        cwd=NERD_DICTATION_DIR,
        capture_output=True,
    )
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

        self.indicator = AppIndicator3.Indicator.new(
            "mic-indicator",
            ICONOS[ESTADO_GRIS],
            AppIndicator3.IndicatorCategory.HARDWARE,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("Micrófono")

        self.menu = Gtk.Menu()
        self._construir_menu()
        self.indicator.set_menu(self.menu)

        mutear_micro()

    def _construir_menu(self):
        for child in self.menu.get_children():
            self.menu.remove(child)

        # ── Banner Arte Fénix ─────────────────────────────────────────────
        banner = Gtk.MenuItem(label="🔥 Grupo Arte Fénix")
        banner.connect("activate", lambda w: webbrowser.open(URL_GITHUB))
        self.menu.append(banner)

        subtitulo = Gtk.MenuItem(label="    Apps · Libros · Multimedia")
        subtitulo.set_sensitive(False)
        self.menu.append(subtitulo)

        self.menu.append(Gtk.SeparatorMenuItem())

        # ── Estado actual ─────────────────────────────────────────────────
        estado_label = Gtk.MenuItem(label=f"🎙  Estado: {NOMBRES[self.estado]}")
        estado_label.set_sensitive(False)
        self.menu.append(estado_label)

        self.menu.append(Gtk.SeparatorMenuItem())

        # ── Botones de estado ─────────────────────────────────────────────
        estados = [
            (ESTADO_GRIS,    "⚫  Apagado"),
            (ESTADO_ROJO,    "🔴  Standby"),
            (ESTADO_VERDE,   "🟢  Transcribir"),
            (ESTADO_CELESTE, "🔵  Solo audio"),
        ]

        for estado, etiqueta in estados:
            item = Gtk.MenuItem(label=etiqueta)
            if estado == self.estado:
                item.set_sensitive(False)
            else:
                item.connect("activate", self._cambiar_estado, estado)
            self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # ── Donación ──────────────────────────────────────────────────────
        donar = Gtk.MenuItem(label="💛  Apoya este proyecto")
        donar.connect("activate", lambda w: webbrowser.open(URL_SPONSORS))
        self.menu.append(donar)

        repo = Gtk.MenuItem(label="📦  Ver en GitHub")
        repo.connect("activate", lambda w: webbrowser.open(URL_REPO))
        self.menu.append(repo)

        self.menu.append(Gtk.SeparatorMenuItem())

        # ── Cerrar suave (queda en gris) ──────────────────────────────────
        cerrar = Gtk.MenuItem(label="⏸  Desactivar micrófono")
        cerrar.connect("activate", self._desactivar)
        self.menu.append(cerrar)

        self.menu.show_all()

    def _cambiar_estado(self, widget, nuevo_estado):
        estado_anterior = self.estado

        if estado_anterior == ESTADO_VERDE:
            parar_dictado()

        if nuevo_estado == ESTADO_GRIS:
            mutear_micro()
        elif nuevo_estado == ESTADO_ROJO:
            mutear_micro()
        elif nuevo_estado == ESTADO_VERDE:
            desmutear_micro()
            iniciar_dictado()
        elif nuevo_estado == ESTADO_CELESTE:
            desmutear_micro()

        self.estado = nuevo_estado
        self.indicator.set_icon_full(ICONOS[nuevo_estado], NOMBRES[nuevo_estado])
        self.indicator.set_title(f"Micrófono: {NOMBRES[nuevo_estado]}")
        self._construir_menu()

    def _desactivar(self, widget):
        """Cierre suave: para todo y vuelve a gris, el proceso sigue vivo."""
        if self.estado == ESTADO_VERDE:
            parar_dictado()
        mutear_micro()
        self.estado = ESTADO_GRIS
        self.indicator.set_icon_full(ICONOS[ESTADO_GRIS], NOMBRES[ESTADO_GRIS])
        self.indicator.set_title("Micrófono: Apagado")
        self._construir_menu()


def main():
    signal.signal(signal.SIGTERM, lambda *a: None)
    signal.signal(signal.SIGINT,  lambda *a: None)

    app = MicIndicator()
    Gtk.main()


if __name__ == "__main__":
    main()
