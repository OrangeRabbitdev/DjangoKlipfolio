#!/bin/bash
set -e  # Salir si hay un error

# Directorios y archivos
CHROMIUM_DIR="chromium"
CHROMIUM_BINARY="$CHROMIUM_DIR/chrome"
CHROMIUM_URL="https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1052319/chrome-linux.zip"
ZIP_FILE="chromium.zip"
CHROMEDRIVER_DIR="chromedriver"
CHROMEDRIVER_BINARY="$CHROMEDRIVER_DIR/chromedriver"
CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip"

# ✅ 1. Instalar Chromium si no está presente
if [ -f "$CHROMIUM_BINARY" ]; then
    echo "✅ Chromium ya está instalado."
else
    echo "🔽 Descargando Chromium..."
    wget -q "$CHROMIUM_URL" -O "$ZIP_FILE"

    if [ ! -s "$ZIP_FILE" ]; then
        echo "❌ Error: La descarga de Chromium falló."
        exit 1
    fi

    echo "📦 Extrayendo Chromium..."
    mkdir -p "$CHROMIUM_DIR"
    unzip -q "$ZIP_FILE" -d "$CHROMIUM_DIR"

    mv "$CHROMIUM_DIR/chrome-linux"/* "$CHROMIUM_DIR/"
    rm -rf "$CHROMIUM_DIR/chrome-linux"
    rm "$ZIP_FILE"

    chmod +x "$CHROMIUM_BINARY"
    echo "✅ Chromium instalado en $CHROMIUM_BINARY"
fi

# ✅ 2. Instalar ChromeDriver compatible (versión 108)
if [ -f "$CHROMEDRIVER_BINARY" ]; then
    echo "✅ ChromeDriver ya está instalado."
else
    echo "🔽 Descargando ChromeDriver versión 108..."
    wget -q "$CHROMEDRIVER_URL" -O "chromedriver.zip"

    if [ ! -s "chromedriver.zip" ]; then
        echo "❌ Error: La descarga de ChromeDriver falló."
        exit 1
    fi

    echo "📦 Extrayendo ChromeDriver..."
    mkdir -p "$CHROMEDRIVER_DIR"
    unzip -q "chromedriver.zip" -d "$CHROMEDRIVER_DIR"
    rm "chromedriver.zip"

    chmod +x "$CHROMEDRIVER_BINARY"
    echo "✅ ChromeDriver instalado en $CHROMEDRIVER_BINARY"
fi

# ✅ 3. Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
sudo pip3 install -r requirements.txt

echo "✅ Build completado correctamente."
