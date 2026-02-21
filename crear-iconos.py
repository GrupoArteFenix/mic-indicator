#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los iconos SVG/PNG para el indicador de micrófono
"""

import os
import subprocess

ICON_DIR = "/usr/local/share/mic-indicator"

ICONOS = {
    "mic_gris":    "#808080",
    "mic_rojo":    "#e53935",
    "mic_verde":   "#43a047",
    "mic_celeste": "#1e88e5",
}

SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <!-- Cuerpo del micrófono -->
  <rect x="9" y="2" width="6" height="11" rx="3" fill="{color}"/>
  <!-- Arco exterior -->
  <path d="M5 11a7 7 0 0 0 14 0" stroke="{color}" stroke-width="2"
        fill="none" stroke-linecap="round"/>
  <!-- Palo -->
  <line x1="12" y1="18" x2="12" y2="22" stroke="{color}" stroke-width="2"
        stroke-linecap="round"/>
  <!-- Base -->
  <line x1="8" y1="22" x2="16" y2="22" stroke="{color}" stroke-width="2"
        stroke-linecap="round"/>
</svg>
"""

def crear_iconos():
    os.makedirs(ICON_DIR, exist_ok=True)

    for nombre, color in ICONOS.items():
        svg_path = f"{ICON_DIR}/{nombre}.svg"
        png_path = f"{ICON_DIR}/{nombre}.png"

        # Escribir SVG
        with open(svg_path, "w") as f:
            f.write(SVG_TEMPLATE.format(color=color))

        # Convertir a PNG con rsvg-convert o inkscape
        resultado = subprocess.run(
            ["rsvg-convert", "-w", "24", "-h", "24", "-o", png_path, svg_path],
            capture_output=True
        )
        if resultado.returncode != 0:
            # Intentar con inkscape
            subprocess.run(
                ["inkscape", "--export-type=png",
                 f"--export-filename={png_path}",
                 f"--export-width=24", svg_path],
                capture_output=True
            )

        print(f"✓ {nombre}.png creado")

    print(f"\nIconos en: {ICON_DIR}")

if __name__ == "__main__":
    crear_iconos()
