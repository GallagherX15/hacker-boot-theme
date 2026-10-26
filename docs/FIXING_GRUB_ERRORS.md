# 🔧 Solución de Errores Comunes en GRUB

Al tunear GRUB y configurar Dual Boot en Arch Linux, es muy común encontrarse con algunos comportamientos raros o errores molestos. Acá tenés la solución a cada uno:

---

## 1. 👥 En el menú de booteo aparecen varios "Arch Linux" con el mismo nombre

### ¿Por qué pasa?
Si tu sistema genera **UKIs** (Unified Kernel Images, por ejemplo cuando `mkinitcpio` crea binarios `.efi` en `/boot/EFI/Linux/arch-linux.efi`), el script de GRUB `/etc/grub.d/15_uki` busca automáticamente esos archivos y crea una entrada de booteo para cada uno.

Al mismo tiempo, el script estándar `/etc/grub.d/10_linux` busca los kernels clásicos en `/boot/vmlinuz-linux`.

**Consecuencia:** Tenés dos o tres opciones que dicen exactamente lo mismo ("Arch Linux", "Arch Linux (fallback)", etc.) en la lista de arranque.

### Solución:
Desactivá la ejecución del script `15_uki` quitándole los permisos de ejecución:
```bash
sudo chmod -x /etc/grub.d/15_uki
```
Luego regenerá la configuración de GRUB:
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```
Listo, las entradas duplicadas desaparecen y te queda una sola entrada limpia para Arch Linux y una para Windows Boot Manager.

---

## 2. 📺 La pantalla de GRUB se ve pixelada o en baja resolución (640x480)

### ¿Por qué pasa?
Por defecto, GRUB arranca en modo VGA estándar de baja resolución a menos que le indiques explícitamente la resolución nativa de tu monitor.

### Solución:
Editá el archivo `/etc/default/grub`:
```bash
sudo nano /etc/default/grub
```
Buscá la línea `GRUB_GFXMODE` y configurala a 1080p nativo:
```bash
GRUB_GFXMODE="1920x1080,auto"
GRUB_GFXPAYLOAD_LINUX="keep"
```
Guardá los cambios (`Ctrl+O`, `Enter`, `Ctrl+X`) y ejecutá:
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## 3. 🚫 Error "Verification Failed: (0x1A) Security Violation" o "shim_lock"

### ¿Por qué pasa?
Ocurre cuando Secure Boot está activado en la BIOS pero el binario de GRUB (`grubx64.efi`) o el kernel (`vmlinuz-linux`) no están firmados con tus claves de `sbctl`, o cuando intentás usar un `shim` viejo que tiene hashes desactualizados.

### Solución:
No necesitás usar `shim` si tenés tus propias claves enroladas en la placa madre con `sbctl`.
Simplemente firmá directamente el binario de GRUB que usa tu placa madre:
```bash
# Buscá los binarios sin firmar
sudo sbctl verify

# Firmalos todos con el flag -s (para que persista)
sudo sbctl sign -s /boot/EFI/arch/grubx64.efi
sudo sbctl sign -s /boot/vmlinuz-linux
```

---

## 4. 🔒 Bloqueo de cuenta por intentos fallidos de sudo (`pam_faillock`)

### ¿Por qué pasa?
Si ejecutás scripts que piden contraseña de root o hacés pipes raros en bash (como `echo "..." | sudo -S python - << 'EOF'`), el bloque heredoc (`<< 'EOF'`) puede comerse la entrada estándar antes de que `sudo` lea la contraseña. 

Si esto pasa 3 veces, la seguridad de Arch Linux (`pam_faillock`) **bloquea temporalmente tu usuario** por seguridad ("sudo: 3 incorrect password attempts").

### Solución:
1. No te desesperes, podés desbloquear tu usuario inmediatamente corriendo (sin sudo, como tu usuario normal si aún tenés sesión abierta):
   ```bash
   faillock --reset
   ```
2. Si vas a correr scripts de Python con sudo, nunca uses heredocs con `sudo -S`. Guardá el script en un archivo temporal (ej. `/tmp/script.py`) y ejecutalo:
   ```bash
   sudo python3 /tmp/script.py
   ```
   O simplemente ejecutá el comando normal con `sudo` interactivo.
