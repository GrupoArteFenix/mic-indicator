# 🎙 Mic Indicator - Grupo Arte Fénix

Indicador de micrófono para XFCE con reconocimiento de voz integrado.
Funciona en Ubuntu, Linux Mint, Fedora y Arch Linux.

## Estados

| Icono | Estado | Descripción |
|-------|--------|-------------|
| ⚫ Gris | Apagado | Micrófono muteado, sin consumo |
| 🔴 Rojo | Standby | Todo listo, micrófono muteado |
| 🟢 Verde | Transcribiendo | Dictado activo, pega texto donde esté el cursor |
| 🔵 Celeste | Solo audio | Para videollamadas, OBS, grabaciones |

## Características

- Icono en la barra de tareas con 4 estados claramente diferenciados
- Círculo blanco de fondo visible en cualquier color de escritorio
- Reconocimiento de voz offline en español con Vosk
- Pega el texto en cualquier aplicación (LibreOffice, navegador, terminal...)
- Opción de iniciar automáticamente con el equipo
- Disponible en el menú de aplicaciones
- Compatible con Ubuntu, Linux Mint, Fedora y Arch Linux

## Instalación
```bash
git clone https://github.com/GrupoArteFenix/mic-indicator.git
cd mic-indicator
chmod +x instalar.sh
sudo ./instalar.sh
```

El instalador detecta tu sistema automáticamente y descarga
todo lo necesario incluyendo el modelo de voz en español.

## Uso

- **Clic en el icono** → abre el menú de control
- **⚫ Apagado** → micrófono muteado, sin consumo de recursos
- **🔴 Standby** → entorno preparado, micrófono muteado
- **🟢 Transcribir** → habla y el texto aparece donde esté el cursor
- **🔵 Solo audio** → micrófono activo para videollamadas y grabaciones
- **✅ Iniciar con el equipo** → activa o desactiva el autostart

## Compatibilidad

- Ubuntu / Linux Mint
- Fedora
- Arch Linux / Manjaro

## Apoya el proyecto

💛 [GitHub Sponsors](https://github.com/sponsors/GrupoArteFenix)

## Licencia

MIT - Grupo Arte Fénix  
🔥 [github.com/GrupoArteFenix](https://github.com/GrupoArteFenix)
