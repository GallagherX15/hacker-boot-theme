# 💀 Guía de Arte ASCII para Bootloaders: Cómo crearlos, encontrarlos y evitar errores

Tunear el bootloader con arte ASCII (calaveras, logos cyberpunk, espadas o banners con tu nickname) le da un aspecto increíble a tu máquina. Pero si alguna vez intentaste poner arte ASCII en una imagen con un script o editor, seguro te topaste con dos problemas clásicos:
1. **La calavera o el dibujo te queda torcido / chueco.**
2. **Las letras del banner se juntan y quedan como un bloque ilegible de caracteres raros.**

Acá te explico por qué pasa esto y cómo resolverlo fácilmente.

---

## 🔍 Dónde buscar y cómo generar Arte ASCII

Hay dos tipos de arte ASCII que vas a necesitar:

### 1. Banners de Texto (Tu Nickname / Nombre)
Para convertir texto normal a letras gigantes ASCII:
* **Web (Recomendado):** Entrá a [TAAG (Text to ASCII Art Generator)](https://patorjk.com/software/taag/).
  * Fuentes recomendadas con estética hacker:
    * `Bloody` (letras góticas con efecto de goteo de sangre).
    * `Slant` (inclinada clásica de la demoscene).
    * `Mono12` / `Block` (bloques sólidos limpios).
    * `Graffiti` / `Doom` / `Cyberlarge`.
* **Desde la Terminal (Linux):**
  Instalá `toilet` y `figlet`:
  ```bash
  sudo pacman -S figlet toilet
  ```
  Probá diferentes estilos:
  ```bash
  toilet -f mono12 -w 120 "TUNOMBRE"
  toilet -f future -w 120 "TUNOMBRE"
  figlet -f slant "TUNOMBRE"
  ```

### 2. Dibujos e Íconos (Calaveras, Logos, etc.)
* **[ASCII Art Archive](https://www.asciiart.eu/)**: El catálogo más grande de arte ASCII libre (categorías: skulls, dragons, cyber, gaming).
* **Convertir cualquier imagen PNG a ASCII:**
  Podés usar herramientas CLI como `chafa` o `jp2a`:
  ```bash
  sudo pacman -S chafa
  chafa --format=symbols --size=60x30 mi_imagen.png
  ```

---

## ⚠️ El Error de la "Calavera Torcida" (Y por qué se desalinea)

### ¿Qué causa el error?
Muchos scripts para generar fondos hacen lo siguiente:
```python
# ❌ ERROR COMÚN: Centrar línea por línea independientemente
for line in ascii_art_lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    line_width = bbox[2] - bbox[0]
    draw.text(((1920 - line_width) // 2, y), line, fill=color)
    y += line_height
```

**Por qué esto rompe todo:**
En el arte ASCII, las líneas tienen diferentes cantidades de espacios al principio (` `) y al final.
Si centrás cada línea de forma individual según su propio ancho visible, el ojo izquierdo de la calavera se va a correr 20 píxeles para un lado, la mandíbula para el otro y los cuernos van a quedar desparejos.

### ✅ La Solución: Centrar el BLOQUE COMPLETO
Tenés que calcular el ancho máximo de la línea más ancha del bloque, y usar **el mismo punto X de inicio para todas las líneas**:

```python
# ✔️ FORMA CORRECTA: Anclar todo el bloque a un mismo X
max_block_width = 0
for line in ascii_art_lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    w = bbox[2] - bbox[0]
    if w > max_block_width:
        max_block_width = w

# X de inicio único para todo el bloque
start_x = (1920 - max_block_width) // 2

for line in ascii_art_lines:
    draw.text((start_x, y), line, fill=color, font=font)
    y += line_height
```
De esta manera, la simetría original de la calavera se mantiene intacta al 100%.

---

## ⚠️ El Error de las Letras Pegadas (Como pasó con `GHERX`)

Si usás fuentes con caracteres sombreados densos como `░`, `▒`, `▓` y `█` (muy común en la fuente *Bloody* o *Dripping*):
* Si las letras no tienen un margen uniforme de 1 o 2 espacios entre sí, los caracteres de una letra se tocan con los de la siguiente.
* Al renderizarse en pantalla, el ojo humano no puede distinguir dónde termina la `G` y dónde empieza la `H`, quedando un manchón rojo incomprensible.

### ✅ La Solución:
Cuando definas o copies letras ASCII compuestas, asegurate de que cada matriz de letra tenga el mismo ancho y agregale siempre un espacio separador uniforme:

```python
# Cada letra es una lista de 6 líneas con padding garantizado
G = ["  ▄████  ", " ██▒ ▀█▒ ", "▒██░▄▄▄░ ", "░▓█  ██▓░", "░▒▓███▀▒ ", " ░▒   ▒  "]
A = [" ▄▄▄     ", "▒████▄   ", "▒██  ▀█▄ ", "░██▄▄▄▄██", " ▓█   ▓██", " ▒▒   ▓▒█"]
# ...
# Al concatenar, dejamos siempre 1 espacio de separación
for row in range(6):
    banner_lines[row] += letra[row] + "  "
```

---

## 📐 La Regla de Oro: Tipografía Monospace Obligatoria

El arte ASCII depende de que **cada carácter ocupe exactamente el mismo ancho de píxeles**. 
* Si usás una tipografía proporcional (Arial, Roboto, Inter, etc.), los espacios ocupan 4px y las letras 12px, por lo que las columnas se descuajeringan por completo.
* Usá **siempre** fuentes monoespaciadas. La mejor recomendación para este tema es **JetBrains Mono Nerd Font** (`JetBrainsMonoNerdFontMono-Bold.ttf`).
