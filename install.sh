#!/usr/bin/env bash
#
# CYBERPUNK RED GRUB THEME - INSTALADOR AUTOMÁTICO
# Instala el tema en /boot/grub/themes/gallagherx y regenera la configuración.
#

set -e

THEME_NAME="gallagherx"
TARGET_DIR="/boot/grub/themes/${THEME_NAME}"
GRUB_DEFAULT="/etc/default/grub"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "      CYBERPUNK RED GRUB THEME - INSTALADOR"
echo "=========================================================="
echo ""

# 1. Verificar permisos de root
if [ "$EUID" -ne 0 ]; then
    echo "[!] Este script necesita permisos de root para escribir en /boot y /etc."
    echo "[*] Ejecutando nuevamente con sudo..."
    exec sudo bash "$0" "$@"
fi

# 2. Verificar dependencias recomendadas
echo "[*] Verificando dependencias..."
MISSING_PKGS=""
if ! pacman -Qi ttf-jetbrains-mono-nerd &>/dev/null && ! pacman -Qi ttf-jetbrains-mono &>/dev/null; then
    MISSING_PKGS="${MISSING_PKGS} ttf-jetbrains-mono-nerd"
fi

if [ -n "$MISSING_PKGS" ]; then
    echo "[i] Te recomendamos instalar las fuentes tipográficas:"
    echo "    sudo pacman -S --needed ${MISSING_PKGS}"
    echo ""
fi

# 3. Copiar archivos del tema
echo "[*] Creando directorio ${TARGET_DIR}..."
mkdir -p "${TARGET_DIR}"

echo "[*] Copiando archivos de tema..."
cp -r "${SCRIPT_DIR}/grub/"* "${TARGET_DIR}/"

# Asegurar permisos correctos
chmod 755 "${TARGET_DIR}"
chmod 644 "${TARGET_DIR}"/*

echo "[+] Tema copiado correctamente a ${TARGET_DIR}."

# 4. Modificar /etc/default/grub de manera segura
if [ -f "$GRUB_DEFAULT" ]; then
    # Crear backup si no existe uno previo
    if [ ! -f "${GRUB_DEFAULT}.bak" ]; then
        echo "[*] Creando backup en ${GRUB_DEFAULT}.bak..."
        cp "$GRUB_DEFAULT" "${GRUB_DEFAULT}.bak"
    fi

    echo "[*] Configurando ${GRUB_DEFAULT}..."

    # Configurar GRUB_THEME
    if grep -q "^GRUB_THEME=" "$GRUB_DEFAULT"; then
        sed -i "s|^GRUB_THEME=.*|GRUB_THEME=\"${TARGET_DIR}/theme.txt\"|" "$GRUB_DEFAULT"
    elif grep -q "^#GRUB_THEME=" "$GRUB_DEFAULT"; then
        sed -i "s|^#GRUB_THEME=.*|GRUB_THEME=\"${TARGET_DIR}/theme.txt\"|" "$GRUB_DEFAULT"
    else
        echo "GRUB_THEME=\"${TARGET_DIR}/theme.txt\"" >> "$GRUB_DEFAULT"
    fi

    # Configurar resolución 1080p
    if grep -q "^GRUB_GFXMODE=" "$GRUB_DEFAULT"; then
        sed -i 's|^GRUB_GFXMODE=.*|GRUB_GFXMODE="1920x1080,auto"|' "$GRUB_DEFAULT"
    elif grep -q "^#GRUB_GFXMODE=" "$GRUB_DEFAULT"; then
        sed -i 's|^#GRUB_GFXMODE=.*|GRUB_GFXMODE="1920x1080,auto"|' "$GRUB_DEFAULT"
    else
        echo 'GRUB_GFXMODE="1920x1080,auto"' >> "$GRUB_DEFAULT"
    fi

    echo "[+] ${GRUB_DEFAULT} actualizado."
else
    echo "[!] Advertencia: No se encontró ${GRUB_DEFAULT}. Asegúrate de configurar GRUB_THEME manualmente."
fi

# 5. Detección de duplicados por UKI (/etc/grub.d/15_uki)
if [ -x "/etc/grub.d/15_uki" ]; then
    echo ""
    echo "[i] DETECCIÓN DE ENTRADAS DUPLICADAS:"
    echo "    Se detectó que '/etc/grub.d/15_uki' está activo."
    echo "    Si en tu menú de GRUB te aparecen dos o tres 'Arch Linux' iguales,"
    echo "    es porque 15_uki duplica las entradas de UKI. Puedes desactivarlo con:"
    echo "    sudo chmod -x /etc/grub.d/15_uki"
    echo ""
fi

# 6. Regenerar grub.cfg
echo "[*] Actualizando grub.cfg..."
if [ -d "/boot/grub" ]; then
    grub-mkconfig -o /boot/grub/grub.cfg
    echo ""
    echo "=========================================================="
    echo "  [✓] TEMA INSTALADO Y CONFIGURADO CON ÉXITO!"
    echo "  Reinicia tu PC para disfrutar del nuevo bootloader."
    echo "=========================================================="
else
    echo "[!] No se encontró /boot/grub. Si usas otra ruta, ejecuta grub-mkconfig manualmente."
fi
