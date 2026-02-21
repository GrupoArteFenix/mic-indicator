#!/bin/bash
# ============================================================
#  Instalador del Indicador de Micrófono - Arte Fénix
#  Compatible con: Ubuntu/Mint (apt) · Fedora (dnf) · Arch (pacman)
# ============================================================
set -e

INSTALL_DIR="/usr/local/bin"
SHARE_DIR="/usr/local/share/mic-indicator"
AUTOSTART_DIR="/etc/xdg/autostart"
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
    echo "     Instala manualmente: python3-gi, gir appindicator3, librsvg"
    exit 1
fi

# ── Instalar dependencias según distro ───────────────────────────────────────
echo ""
echo "▶ Instalando dependencias..."

if [ "$DISTRO" = "debian" ]; then
    sudo apt install -y \
        librsvg2-bin \
        python3-gi \
        python3-gi-cairo \
        gir1.2-gtk-3.0 \
        gir1.2-appindicator3-0.1 \
        python3-venv \
        sox \
        xdotool

elif [ "$DISTRO" = "fedora" ]; then
    sudo dnf install -y \
        librsvg2-tools \
        python3-gobject \
        gtk3 \
        libappindicator-gtk3 \
        python3 \
        sox \
        xdotool

elif [ "$DISTRO" = "arch" ]; then
    sudo pacman -Sy --noconfirm \
        librsvg \
        python-gobject \
        gtk3 \
        libappindicator-gtk3 \
        python \
        sox \
        xdotool
fi

# ── Crear directorio de iconos ────────────────────────────────────────────────
echo ""
echo "▶ Creando iconos..."
sudo mkdir -p "$SHARE_DIR"
sudo python3 "$SCRIPT_DIR/crear-iconos.py"

# ── Instalar script principal ─────────────────────────────────────────────────
echo ""
echo "▶ Instalando script principal..."
sudo cp "$SCRIPT_DIR/mic-indicator.py" "$INSTALL_DIR/mic-indicator"
sudo chmod +x "$INSTALL_DIR/mic-indicator"

# ── Autostart para todos los usuarios ────────────────────────────────────────
echo ""
echo "▶ Configurando autostart para todos los usuarios..."
sudo mkdir -p "$AUTOSTART_DIR"
sudo tee "$AUTOSTART_DIR/mic-indicator.desktop" > /dev/null << 'EOF'
[Desktop Entry]
Type=Application
Name=Indicador de Micrófono
Name[es]=Indicador de Micrófono
Comment=Control de micrófono con reconocimiento de voz - Arte Fénix
Comment[es]=Control de micrófono con reconocimiento de voz - Arte Fénix
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
echo "  En el próximo inicio de sesión arrancará solo."
echo ""
echo "  🔥 Grupo Arte Fénix"
echo "  https://github.com/GrupoArteFenix"
echo "======================================================"
