#!/bin/bash
# ============================================================
#  Instalador del Indicador de Micrófono - Arte Fénix
#  Compatible con: Ubuntu/Mint (apt) · Fedora (dnf) · Arch (pacman)
# ============================================================
set -e

INSTALL_DIR="/usr/local/bin"
SHARE_DIR="/usr/local/share/mic-indicator"
AUTOSTART_DIR="/etc/xdg/autostart"
APPS_DIR="/usr/share/applications"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================================"
echo "  Indicador de Micrófono - Grupo Arte Fénix"
echo "  https://github.com/GrupoArteFenix/mic-indicator"
echo "======================================================"

# ── Detectar gestor de paquetes ───────────────────────────────────────────────
echo ""
echo "▶ Detectando sistema..."

if command -v apt &> /dev/null; then
    DISTRO="debian"
    echo "  Sistema: Ubuntu / Linux Mint / Debian"
elif command -v dnf &> /dev/null; then
    DISTRO="fedora"
    echo "  Sistema: Fedora / RHEL"
elif command -v pacman &> /dev/null; then
    DISTRO="arch"
    echo "  Sistema: Arch Linux / Manjaro"
else
    echo "  ❌ No se reconoce el gestor de paquetes."
    exit 1
fi

# ── Instalar dependencias ─────────────────────────────────────────────────────
echo ""
echo "▶ Instalando dependencias..."

if [ "$DISTRO" = "debian" ]; then
    sudo apt install -y librsvg2-bin python3-gi python3-gi-cairo \
        gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 python3-venv sox xdotool

elif [ "$DISTRO" = "fedora" ]; then
    sudo dnf install -y librsvg2-tools python3-gobject gtk3 \
        libappindicator-gtk3 python3 sox xdotool

elif [ "$DISTRO" = "arch" ]; then
    sudo pacman -Sy --noconfirm librsvg python-gobject gtk3 \
        libappindicator-gtk3 python sox xdotool
fi

# ── Crear directorio de iconos ────────────────────────────────────────────────
echo ""
echo "▶ Creando iconos..."
sudo mkdir -p "$SHARE_DIR"
sudo python3 "$SCRIPT_DIR/crear-iconos.py"

# ── Copiar logo si existe ─────────────────────────────────────────────────────
if [ -f "$SCRIPT_DIR/Arte-Fenix-App.png" ]; then
    sudo cp "$SCRIPT_DIR/Arte-Fenix-App.png" "$SHARE_DIR/logo.png"
    echo "✓ Logo copiado"
fi

# ── Instalar script principal ─────────────────────────────────────────────────
echo ""
echo "▶ Instalando script principal..."
sudo cp "$SCRIPT_DIR/mic-indicator.py" "$INSTALL_DIR/mic-indicator"
sudo chmod +x "$INSTALL_DIR/mic-indicator"
chmod +x "$SCRIPT_DIR/instalar.sh"

# ── Entrada en menú de aplicaciones ──────────────────────────────────────────
echo ""
echo "▶ Añadiendo al menú de aplicaciones..."
sudo tee "$APPS_DIR/mic-indicator.desktop" > /dev/null << 'EOF'
[Desktop Entry]
Type=Application
Name=Indicador de Micrófono
Name[es]=Indicador de Micrófono
Comment=Control de micrófono con reconocimiento de voz
Comment[es]=Control de micrófono con reconocimiento de voz
Exec=/usr/local/bin/mic-indicator
Icon=audio-input-microphone
Terminal=false
Categories=AudioVideo;Audio;Utility;
Keywords=microfono;voz;dictado;transcripcion;
EOF

# ── Autostart para todos los usuarios ────────────────────────────────────────
echo ""
echo "▶ Configurando autostart..."
sudo mkdir -p "$AUTOSTART_DIR"
sudo tee "$AUTOSTART_DIR/mic-indicator.desktop" > /dev/null << 'EOF'
[Desktop Entry]
Type=Application
Name=Indicador de Micrófono
Comment=Control de micrófono con reconocimiento de voz - Arte Fénix
Exec=/usr/local/bin/mic-indicator
Icon=audio-input-microphone
Terminal=false
Categories=AudioVideo;Audio;Utility;
X-GNOME-Autostart-enabled=true
EOF

echo ""
echo "======================================================"
echo "  ✅ Instalación completada"
echo "======================================================"
echo ""
echo "  Inicia ahora:"
echo "  mic-indicator &"
echo ""
echo "  También disponible en el menú de aplicaciones."
echo "  Arrancará automáticamente con el equipo."
echo "  Puedes cambiarlo desde el menú del indicador."
echo ""
echo "  🔥 Grupo Arte Fénix"
echo "  https://github.com/GrupoArteFenix"
echo "======================================================"
