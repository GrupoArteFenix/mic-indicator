#!/bin/bash
# ============================================================
#  Instalador del Indicador de Micrófono - Arte Fénix
# ============================================================
set -e

INSTALL_DIR="/usr/local/bin"
SHARE_DIR="/usr/local/share/mic-indicator"
AUTOSTART_DIR="/etc/xdg/autostart"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================================"
echo "  Instalador Indicador de Micrófono - Arte Fénix"
echo "======================================================"

# 1. Dependencias
echo ""
echo "▶ Instalando dependencias..."
sudo apt install -y librsvg2-bin python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-appindicator3-0.1

# 2. Crear directorio de iconos
echo ""
echo "▶ Creando iconos..."
sudo mkdir -p "$SHARE_DIR"
sudo python3 "$SCRIPT_DIR/crear-iconos.py"

# 3. Instalar script principal
echo ""
echo "▶ Instalando script principal..."
sudo cp "$SCRIPT_DIR/mic-indicator.py" "$INSTALL_DIR/mic-indicator"
sudo chmod +x "$INSTALL_DIR/mic-indicator"

# 4. Autostart para TODOS los usuarios (xdg/autostart)
echo ""
echo "▶ Configurando autostart para todos los usuarios..."
sudo tee "$AUTOSTART_DIR/mic-indicator.desktop" > /dev/null << 'EOF'
[Desktop Entry]
Type=Application
Name=Indicador de Micrófono
Comment=Control de micrófono para XFCE
Exec=/usr/local/bin/mic-indicator
Icon=audio-input-microphone
Terminal=false
Categories=AudioVideo;Audio;
X-GNOME-Autostart-enabled=true
EOF

echo ""
echo "======================================================"
echo "  ✅ Instalación completada"
echo "======================================================"
echo ""
echo "  Para iniciar ahora sin reiniciar:"
echo "  mic-indicator &"
echo ""
echo "  En el próximo inicio de sesión arrancará solo."
echo "======================================================"
