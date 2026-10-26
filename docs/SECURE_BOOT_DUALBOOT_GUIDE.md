# 🛡️ Guía Completa: Secure Boot en Dual Boot (Arch Linux + Windows 11) para Vanguard (LoL / Valorant)

Si estás aquí, probablemente te ocurrió lo mismo que a mí: querías jugar League of Legends o Valorant en Windows 11, pero el sistema antitrampas **Vanguard** mostró un mensaje exigiendo tener **Secure Boot** activado obligatoriamente. El problema es que en un entorno Dual Boot con Arch Linux, activar Secure Boot desde la BIOS suele impedir el arranque de Linux o generar errores de verificación (`Verification Failed` / `Security Violation`).

En esta guía se explica cómo dejar **Secure Boot 100% activo y funcional**, usando tus propios certificados UEFI mediante `sbctl`, sin dañar el arranque de Windows y manteniendo tu menú de GRUB personalizado.

---

## ⚠️ El Error Principal a Evitar

Muchos tutoriales en internet indican simplemente:
> *"Ejecuta `sbctl enroll-keys`"*

**NO LO HAGAS SIN PRECAUCIÓN.**
1. Si ejecutas `sbctl enroll-keys` sin el parámetro `-m`, borrarás las claves oficiales de Microsoft de la placa madre. **Resultado:** Windows 11 no podrá iniciar o dispositivos con Option ROMs de fábrica (tarjetas gráficas, tarjetas Wi-Fi) pueden presentar problemas.
2. Si tu BIOS se encuentra en **User Mode**, `sbctl` arrojará el siguiente error:
   ```text
   ✗ Setup Mode is disabled. Please enter firmware setup to enable it.
   ```

A continuación se detalla el procedimiento correcto para configurarlo con éxito al primer intento.

---

## 📋 Requisitos Previos

Instala `sbctl` en Arch Linux:
```bash
sudo pacman -S sbctl
```

Verifica el estado actual de Secure Boot:
```bash
sudo sbctl status
```
Presta atención a dos valores clave:
* `Installed:` (indicará `✗ sbctl is not installed` si es la primera vez que se ejecuta).
* `Setup Mode:` (si indica `✗ Disabled`, es necesario ingresar a la BIOS).

---

## 🛠️ Paso 1: Configurar la UEFI/BIOS en "Setup Mode"

Para que Linux pueda registrar certificados en la placa madre, la BIOS debe estar en modo de configuración (**Setup Mode**).

1. Reinicia el equipo e ingresa a la BIOS (habitualmente mediante las teclas `F10`, `F2`, `F12` o `Supr/Del`).
2. Dirígete a la pestaña **Security** o **Boot Options** -> **Secure Boot Configuration**.
3. Busca la opción correspondiente para limpiar las claves existentes:
   * **Clear Secure Boot Keys** (o *Delete All Secure Boot Variables* / *Reset to Setup Mode*).
   * En ciertas placas base (como ASUS o MSI), cambia el tipo de sistema operativo a **Custom** y accede a **Key Management -> Clear Keys**.
4. Guarda los cambios (`F10`) e inicia nuevamente en **Arch Linux**.

> [!NOTE]
> Al limpiar las variables de fábrica no se borra ninguna información del disco. La placa madre simplemente entra en "Setup Mode", lo que significa que Secure Boot queda suspendido temporalmente a la espera de nuevos certificados autorizados.

Verifica en la terminal de Linux:
```bash
sudo sbctl status
```
Ahora el campo `Setup Mode` debe aparecer como **Enabled** (o `✓`).

---

## 🔑 Paso 2: Crear tus Propias Claves

Genera tus certificados criptográficos locales:
```bash
sudo sbctl create-keys
```
Este comando generará tus claves privadas y certificados en el directorio `/usr/share/secureboot/keys/`.

---

## 📝 Paso 3: Firmar el Bootloader y el Kernel (ANTES de registrar las claves)

Antes de guardar las claves en la UEFI, **es imprescindible firmar los archivos `.efi` de Linux**. De lo contrario, al reiniciar el equipo con Secure Boot habilitado, la BIOS bloqueará el arranque de Arch Linux por no contar con una firma válida.

1. Revisa qué archivos requieren firma:
   ```bash
   sudo sbctl verify
   ```
   Aparecerán marcados en rojo (`✗`) todos los ejecutables EFI sin firmar.

2. Firma el binario de GRUB (el parámetro `-s` guarda la regla en la base de datos para firmas automáticas futuras):
   ```bash
   # Verifica la ruta exacta de tu grubx64.efi (normalmente en /boot/EFI/arch/ o /boot/EFI/BOOT/)
   sudo sbctl sign -s /boot/EFI/arch/grubx64.efi
   ```

3. Firma el kernel o las imágenes UKI (Unified Kernel Images):
   ```bash
   # Si utilizas el kernel tradicional:
   sudo sbctl sign -s /boot/vmlinuz-linux

   # Si utilizas UKIs (por ejemplo generadas en /boot/EFI/Linux/):
   sudo sbctl sign -s /boot/EFI/Linux/arch-linux.efi
   sudo sbctl sign -s /boot/EFI/Linux/arch-linux-fallback.efi
   ```

4. Comprueba que todos los archivos aparezcan firmados:
   ```bash
   sudo sbctl verify
   ```
   Todos los binarios deben figurar con el indicador verde `✓ is signed`.

---

## 🚀 Paso 4: Registrar las Claves en la UEFI (COMANDO FUNDAMENTAL)

En este paso se utiliza el parámetro `-m`. Este indicador le indica a `sbctl`: *"Registra mis certificados locales de Arch Linux, pero **conserva e incluye también los certificados oficiales de Microsoft UEFI CA**"*.

```bash
sudo sbctl enroll-keys -m
```

Si el proceso fue exitoso, el sistema responderá:
```text
✓ Enrolled keys to the EFI variables!
```

---

## 🔒 Paso 5: Habilitar Secure Boot y Comprobar el Funcionamiento

1. Reinicia el equipo e ingresa nuevamente a la BIOS.
2. Asegúrate de que **Secure Boot** se encuentre en estado **Enabled** (en varias placas se activa automáticamente al registrar las claves).
3. Guarda los cambios e inicia en Arch Linux.
4. Abre una terminal y confirma el estado:
   ```bash
   sudo sbctl status
   ```
   Deberás observar:
   * `Installed: ✓ sbctl is installed`
   * `Setup Mode: ✓ Disabled`
   * `Secure Boot: ✓ Enabled`

5. Ahora reinicia e inicia en **Windows 11**:
   * Abre League of Legends o Valorant.
   * El anticheat Vanguard funcionará con total normalidad sin solicitar Secure Boot.
   * **Dual Boot operando al 100% con seguridad activada en ambos sistemas.**

---

## 🔄 ¿Qué sucede al actualizar el Kernel en el futuro?

El paquete `sbctl` instala un hook automático para el gestor `pacman`. Cada vez que ejecutes `sudo pacman -Syu` y se descargue una nueva versión del paquete `linux` o `grub`, el hook firmará automáticamente el nuevo kernel antes de reiniciar el equipo, manteniendo la compatibilidad sin intervención manual.
