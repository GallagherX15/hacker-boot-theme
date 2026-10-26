# 🔧 Solución de Errores Comunes en GRUB

Al personalizar el cargador de arranque GRUB y configurar Dual Boot en Arch Linux, es habitual encontrarse con ciertos comportamientos imprevistos o configuraciones por defecto molestas. A continuación se detallan las soluciones correspondientes a cada caso:

---

## 1. 👥 En el menú de inicio aparecen varias opciones idénticas de "Arch Linux"

### Causa:
Si el sistema genera imágenes **UKI** (Unified Kernel Images, por ejemplo cuando `mkinitcpio` compila binarios autónomos en `/boot/EFI/Linux/arch-linux.efi`), el script de GRUB `/etc/grub.d/15_uki` detecta automáticamente dichos archivos y genera una entrada de inicio independiente para cada uno.

Simultáneamente, el script tradicional `/etc/grub.d/10_linux` busca los núcleos convencionales ubicados en `/boot/vmlinuz-linux`.

**Consecuencia:** El menú muestra entradas repetidas ("Arch Linux", "Arch Linux (fallback)", etc.) que apuntan a la misma instalación.

### Solución:
Desactiva la ejecución del script `15_uki` retirándole los permisos de ejecución:
```bash
sudo chmod -x /etc/grub.d/15_uki
```
Posteriormente, regenera el archivo de configuración de GRUB:
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```
Con esto, las entradas duplicadas desaparecerán y el menú conservará únicamente una entrada limpia para Arch Linux y otra para Windows Boot Manager.

---

## 2. 📺 La pantalla de GRUB se visualiza con baja resolución (640x480 o pixelada)

### Causa:
Por defecto, GRUB inicia en un modo de compatibilidad VGA estándar a menos que se defina explícitamente la resolución nativa de la pantalla.

### Solución:
Edita el archivo de configuración general `/etc/default/grub`:
```bash
sudo nano /etc/default/grub
```
Localiza la variable `GRUB_GFXMODE` y establécela en resolución Full HD:
```bash
GRUB_GFXMODE="1920x1080,auto"
GRUB_GFXPAYLOAD_LINUX="keep"
```
Guarda los cambios (`Ctrl+O`, `Enter`, `Ctrl+X`) y aplica la configuración:
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## 3. 🚫 Error "Verification Failed: (0x1A) Security Violation" o fallo de verificación

### Causa:
Este error se presenta cuando Secure Boot está habilitado en la BIOS pero el binario de GRUB (`grubx64.efi`) o el kernel (`vmlinuz-linux`) no han sido firmados con los certificados autorizados en la placa madre mediante `sbctl`.

### Solución:
Si estás utilizando `sbctl` con tus propios certificados registrados, no requieres utilizar `shim`. Simplemente firma directamente los ejecutables correspondientes:
```bash
# Revisa qué binarios carecen de firma
sudo sbctl verify

# Firma los componentes requeridos con el parámetro -s (para mantener la persistencia)
sudo sbctl sign -s /boot/EFI/arch/grubx64.efi
sudo sbctl sign -s /boot/vmlinuz-linux
```

---

## 4. 🔒 Bloqueo de cuenta de usuario por intentos fallidos de sudo (`pam_faillock`)

### Causa:
Si se ejecutan scripts o instrucciones en la terminal que redirigen la entrada estándar de manera errónea al invocar `sudo` (por ejemplo usando bloques heredoc complejos con pipes interactivos), el sistema puede interpretar el flujo de datos como intentos incorrectos de contraseña.

Al alcanzar tres intentos fallidos consecutivos, el módulo de seguridad de Arch Linux (`pam_faillock`) **bloquea temporalmente el acceso del usuario** indicando: `sudo: 3 incorrect password attempts`.

### Solución:
1. Puedes restaurar el acceso de inmediato ejecutando el siguiente comando (con tu usuario habitual, sin sudo):
   ```bash
   faillock --reset
   ```
2. Al ejecutar scripts de Python o automatizaciones con privilegios elevados, evita redirigir contraseñas por tuberías en scripts interactivos. Guarda el código en un archivo temporal (por ejemplo `/tmp/script.py`) y ejecútalo directamente:
   ```bash
   sudo python3 /tmp/script.py
   ```
