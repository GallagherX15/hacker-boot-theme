# 🛡️ Guía Definitiva: Secure Boot en Dual Boot (Arch Linux + Windows 11) para Vanguard (LoL / Valorant)

Si llegaste acá, probablemente te pasó lo mismo que a mí: querías jugar al League of Legends o al Valorant en Windows 11, pero el anticheat **Vanguard** te tiró un cartel diciendo que necesitás tener **Secure Boot** activado sí o sí. El problema es que si tenés Dual Boot con Arch Linux, activar Secure Boot desde la BIOS suele romper el arranque de Linux o dar error de firma (`Verification Failed` / `Security Violation`).

En esta guía te explico cómo dejar **Secure Boot 100% activo**, con tus propias claves UEFI usando `sbctl`, sin romper Windows y manteniendo tu GRUB tuneado.

---

## ⚠️ El Error #1 que comete todo el mundo

La mayoría de tutoriales te dicen:
> *"Corré `sbctl enroll-keys`"*

**NO LO HAGAS A CIEGAS.**
1. Si corrés `sbctl enroll-keys` sin el flag `-m`, vas a borrar las claves de Microsoft de tu placa madre. **Resultado:** Windows 11 no va a arrancar o la placa de video / Wi-Fi con Option ROMs de fábrica pueden dejar de responder.
2. Si tu BIOS está en **User Mode**, `sbctl` te va a tirar el error:
   ```text
   ✗ Setup Mode is disabled. Please enter firmware setup to enable it.
   ```

A continuación tenés el paso a paso exacto para hacerlo bien a la primera.

---

## 📋 Requisitos Previos

Instalá `sbctl` en Arch Linux:
```bash
sudo pacman -S sbctl
```

Verificá el estado actual de tu arranque seguro:
```bash
sudo sbctl status
```
Fijate en dos valores clave:
* `Installed:` (debe decir `✗ sbctl is not installed` o similar si es la primera vez)
* `Setup Mode:` (si dice `✗ Disabled`, tenemos que ir a la BIOS)

---

## 🛠️ Paso 1: Poner la UEFI/BIOS en "Setup Mode"

Para que Linux pueda registrar claves en la placa madre, la BIOS tiene que estar en modo de configuración (**Setup Mode**).

1. Reiniciá la PC y entrá a la BIOS (generalmente con `F10`, `F2` o `Del`).
2. Buscá la pestaña **Security** o **Boot Options** -> **Secure Boot Configuration**.
3. Vas a encontrar una opción llamada:
   * **Clear Secure Boot Keys** (o *Delete All Secure Boot Variables* / *Reset to Setup Mode*).
   * En algunas placas (como ASUS o MSI), ponés el tipo de SO en **Custom** y seleccionás **Key Management -> Clear Keys**.
4. Guardá los cambios (`F10`) y volvé a iniciar en **Arch Linux**.

> [!NOTE]
> Al borrar las claves no rompés nada. La máquina entra en "Setup Mode", lo que significa que el Secure Boot está apagado temporalmente esperando que alguien le cargue claves nuevas.

Verificá en Linux:
```bash
sudo sbctl status
```
Ahora `Setup Mode` debería mostrarse como **Enabled** (o `✓`).

---

## 🔑 Paso 2: Crear tus propias Claves

Generá tus certificados locales con:
```bash
sudo sbctl create-keys
```
Esto crea tus certificados criptográficos privados en `/usr/share/secureboot/keys/`.

---

## 📝 Paso 3: Firmar el Bootloader y el Kernel (ANTES de activar)

Antes de guardar las claves en la UEFI, **tenés que firmar los archivos `.efi` de Linux**, porque si no lo hacés, cuando reinicies la PC la BIOS va a bloquear a Arch Linux por no estar firmado.

1. Chequeá qué archivos necesitan firma:
   ```bash
   sudo sbctl verify
   ```
   Te va a listar en rojo (`✗`) todos los ejecutables EFI que no tienen firma.

2. Firmá el binario de GRUB (el flag `-s` guarda la regla para que se firme solo en el futuro):
   ```bash
   # Fijate dónde está tu grubx64.efi (suele estar en /boot/EFI/arch/ o /boot/EFI/BOOT/)
   sudo sbctl sign -s /boot/EFI/arch/grubx64.efi
   ```

3. Firmá el kernel o los UKI (Unified Kernel Images):
   ```bash
   # Si usás kernel tradicional:
   sudo sbctl sign -s /boot/vmlinuz-linux

   # Si usás UKIs (ej. mkinitcpio con UKI en /boot/EFI/Linux/):
   sudo sbctl sign -s /boot/EFI/Linux/arch-linux.efi
   sudo sbctl sign -s /boot/EFI/Linux/arch-linux-fallback.efi
   ```

4. Verificá que todo esté en verde:
   ```bash
   sudo sbctl verify
   ```
   Todos los binarios deben decir `✓ is signed`.

---

## 🚀 Paso 4: Enrolar las Claves a la UEFI (EL COMANDO CLAVE)

Acá es donde usamos el flag `-m`. Este flag le dice a `sbctl`: *"Guardá mis claves personalizadas para Arch Linux, pero **conservá también las claves oficiales de Microsoft UEFI CA**"*.

```bash
sudo sbctl enroll-keys -m
```

Si todo salió bien, te va a decir:
```text
✓ Enrolled keys to the EFI variables!
```

---

## 🔒 Paso 5: Activar Secure Boot y Probar

1. Reiniciá tu PC y entrá a la BIOS.
2. Asegurate de que **Secure Boot** esté en **Enabled** (en muchas placas se activa automáticamente al enrolar claves).
3. Guardá y arrancá en Arch Linux.
4. Abrí una terminal y verificá:
   ```bash
   sudo sbctl status
   ```
   Deberías ver:
   * `Installed: ✓ sbctl is installed`
   * `Setup Mode: ✓ Disabled`
   * `Secure Boot: ✓ Enabled`

5. Ahora reiniciá en **Windows 11**:
   * Abrí League of Legends o Valorant.
   * El Vanguard ya no te va a joder con el cartel de Secure Boot.
   * **Dual Boot funcionando al 100% con seguridad activa.**

---

## 🔄 ¿Qué pasa cuando se actualiza el Kernel?

`sbctl` incluye un hook automático para Pacman. Cada vez que hacés un `sudo pacman -Syu` y se descarga una versión nueva de `linux` o `grub`, el hook se ejecuta y firma automáticamente el kernel nuevo antes de que reinicies la máquina. ¡Te olvidás para siempre!
