# 🔴 GallagherX Cyberpunk Red GRUB Theme & Secure Boot Dual Boot Guide

> **"Hice este repositorio porque estuve varias horas batallando para que el anticheat Vanguard (League of Legends / Valorant) me dejara jugar en Windows 11 teniendo Arch Linux en Dual Boot, y de paso creé un tema de GRUB estilo hacker con calavera roja y tipografía sangrante que quedó excelente."**

![GRUB Theme Preview](assets/previews/preview.png)

---

## ⚡ ¿Qué incluye este repositorio?

1. **Tema de GRUB Cyberpunk Red**: Fondo a 1080p con calavera ASCII simétrica, banner con efecto de sangre gótica/goteo, scanlines retro estilo monitor CRT y barra de progreso roja personalizada.
2. **Guía de Secure Boot con `sbctl`**: Cómo activar Secure Boot de verdad para **Vanguard (LoL / Valorant)** sin romper el arranque de Linux y sin trucos raros que dejan de funcionar con cada actualización del kernel.
3. **Generador "Vibe Coding"**: Un script en Python interactivo (`generate_theme.py`) para poner tu propio nick o cambiar el logo en 10 segundos sin tocar código.
4. **Modo Manual**: Para quienes prefieren la terminal y quieren entender cada archivo haciéndolo paso a paso.
5. **Solución a los errores comunes**: Entradas duplicadas en el menú de inicio, calaveras torcidas en ASCII y problemas de resolución.

---

## 🎮 Parte 1: El problema de Vanguard y Secure Boot

Si tienes Dual Boot (Windows 11 + Arch Linux) y quisiste abrir League of Legends o Valorant, seguro te apareció el error:
`VAN9003: Vanguard requires Secure Boot to be enabled`.

El problema: si activas Secure Boot en la BIOS directamente, Arch Linux no inicia porque los binarios de Linux no están firmados por las claves de fábrica de Microsoft.

La solución definitiva es usar **`sbctl`** para crear tus propios certificados UEFI y firmar GRUB y el Kernel.

### ⚠️ Los 2 errores principales a evitar:
1. **Ejecutar `sbctl enroll-keys` sin el parámetro `-m`**: Si olvidas el `-m`, borras las claves de Microsoft de tu placa madre y **Windows no volverá a iniciar**. Siempre debe usarse con `-m` (`sbctl enroll-keys -m`).
2. **No limpiar las claves en la BIOS primero**: Si tu placa está en *User Mode*, la terminal mostrará el error `Setup Mode is disabled`. Tienes que entrar a la BIOS y seleccionar la opción para borrar las claves (*Clear Secure Boot Keys*).

> 👉 **[Consulta la guía completa paso a paso de Secure Boot aquí](docs/SECURE_BOOT_DUALBOOT_GUIDE.md)** con todos los comandos y detalles.

---

## 🚀 Parte 2: Instalación del Tema de GRUB

Puedes instalarlo de dos maneras: la rápida (**Modo Vibe Coding**) o la manual paso a paso (**Modo Manual**).

### 🛠️ Opción A: Modo "Vibe Coding" (Automático e Interactivo)

Si no te quieres complicar y prefieres personalizar el banner con tu nombre mediante un generador automático:

1. **Clona el repositorio e instala las dependencias:**
   ```bash
   git clone https://github.com/TU_USUARIO/hacker-boot-theme.git
   cd hacker-boot-theme
   sudo pacman -S python-pillow ttf-jetbrains-mono-nerd
   ```

2. **Genera tu fondo personalizado:**
   ```bash
   ./generate_theme.py
   ```
   El script te preguntará:
   * Tu Nick o Nombre para el banner ASCII (ejemplo: `GALLAGHERX`, `NEO`, `CYBER`).
   * El estilo de fuente (sangrante gótico `bloody`, bloque limpio `mono12`, etc.).
   * El texto del subtítulo (ejemplo: `[ GALLAGHER BOOT ]`).
   * Si quieres usar la calavera roja que viene incluida o una imagen propia.

3. **Instálalo en el sistema con un solo comando:**
   ```bash
   sudo ./install.sh
   ```
   El instalador:
   * Copia el tema a `/boot/grub/themes/gallagherx`.
   * Realiza un respaldo seguro de tu archivo `/etc/default/grub`.
   * Configura la resolución a 1080p y activa el tema.
   * Ejecuta `grub-mkconfig` automáticamente.

---

### 💻 Opción B: Modo Manual (Paso a paso)

Si prefieres realizar todo el proceso manualmente:

1. **Instala las fuentes necesarias:**
   ```bash
   sudo pacman -S ttf-jetbrains-mono-nerd
   ```

2. **Crea la carpeta del tema y copia los archivos:**
   ```bash
   sudo mkdir -p /boot/grub/themes/gallagherx
   sudo cp -r grub/* /boot/grub/themes/gallagherx/
   ```

3. **Edita `/etc/default/grub`:**
   ```bash
   sudo nano /etc/default/grub
   ```
   Asegúrate de configurar estas dos líneas:
   ```bash
   GRUB_THEME="/boot/grub/themes/gallagherx/theme.txt"
   GRUB_GFXMODE="1920x1080,auto"
   ```

4. **Regenera el archivo de configuración de GRUB:**
   ```bash
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   ```
   Reinicia el equipo y ya tendrás el nuevo menú activo.

---

## 💀 Parte 3: ¿Cómo crear o cambiar el Arte ASCII?

En este tema no utilizamos una imagen estática genérica. El banner y los elementos están construidos con matrices ASCII en alta fidelidad y efecto CRT.

Si quieres buscar o crear tus propios diseños en ASCII:
* **Generadores de texto:** Puedes usar [TAAG (Text to ASCII Art Generator)](https://patorjk.com/software/taag/) con fuentes como `Bloody`, `Slant` o `Mono12`.
* **Colecciones de dibujos e íconos:** Revisa [ASCII Art Archive](https://www.asciiart.eu/) (calaveras, dragones, espadas, etc.).

### 🚨 El problema de la "Calavera Torcida"
Si alguna vez intentaste programar un script para centrar arte ASCII y el dibujo quedó chueco o deformado, se debe a que **centraste cada línea de forma individual**. 

Como cada línea de un dibujo ASCII tiene una cantidad distinta de espacios en blanco al inicio, centrar línea por línea desalinea la figura por completo. **La solución correcta consiste en calcular el ancho máximo de todo el bloque y comenzar todas las líneas exactamente en la misma posición X.**

> 👉 **[Consulta la Guía de Arte ASCII y Centrado Matemático aquí](docs/ASCII_ART_GUIDE.md)** para ver el código en Python exacto y cómo evitar que las letras se amontonen.

---

## 🔧 Solución de Errores Comunes

* **¿Aparecen dos o tres opciones iguales de "Arch Linux" en el menú de inicio?**  
  Esto sucede cuando el sistema genera UKIs (Unified Kernel Images). El script `15_uki` de GRUB crea entradas duplicadas.  
  Se soluciona ejecutando:  
  `sudo chmod -x /etc/grub.d/15_uki && sudo grub-mkconfig -o /boot/grub/grub.cfg`.
* **¿El menú de GRUB se ve gigante y pixelado en baja resolución?**  
  La pantalla está iniciando en modo VGA por defecto. Agrega `GRUB_GFXMODE="1920x1080,auto"` en `/etc/default/grub`.
* **¿Se bloqueó tu usuario por intentos fallidos de contraseña (`pam_faillock`)?**  
  Puedes desbloquearlo de inmediato ejecutando en la terminal: `faillock --reset`.

> 👉 **[Revisa la guía completa de solución de errores aquí](docs/FIXING_GRUB_ERRORS.md)**.

---

## 📂 Estructura del Repositorio

```text
├── assets/
│   ├── ascii_templates/   # Diccionarios de fuentes ASCII y plantillas de calaveras
│   ├── previews/          # Capturas de pantalla reales del menú
│   └── skull_red.png      # Calavera en alta definición roja
├── docs/
│   ├── ASCII_ART_GUIDE.md           # Cómo armar y centrar arte ASCII sin deformarlo
│   ├── FIXING_GRUB_ERRORS.md        # Solución a entradas duplicadas, UKIs y resolución
│   └── SECURE_BOOT_DUALBOOT_GUIDE.md# Guía paso a paso sbctl + Vanguard + Windows 11
├── generate_theme.py      # Generador interactivo de fondos en Python (Modo Vibe Coding)
├── grub/
│   ├── background.png     # Fondo generado listo para usar (1920x1080)
│   ├── jetbrains_*.pf2    # Fuentes convertidas para el renderizador de GRUB
│   ├── select_*.png       # Texturas de la caja de selección roja
│   └── theme.txt          # Archivo de configuración oficial del tema
├── install.sh             # Script instalador automático con respaldo
├── LICENSE                # Licencia MIT
└── README.md
```

---

## ⭐ Créditos y Contribuciones

Desarrollado para la comunidad de Arch Linux y para quienes disfrutan de los videojuegos en Dual Boot sin renunciar a su sistema operativo principal. Si este proyecto te fue de utilidad, considera dejarle una estrella ⭐ al repositorio en GitHub. ¡Las sugerencias y contribuciones son siempre bienvenidas!
