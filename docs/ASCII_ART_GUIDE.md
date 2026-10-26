# 💀 Guía de Arte ASCII para Bootloaders: Creación, Búsqueda y Alineación Geométrica

Personalizar el cargador de arranque con arte ASCII (calaveras, emblemas cyberpunk o tipografías con tu nombre) le da una estética única al equipo. No obstante, al intentar plasmar arte ASCII en una imagen mediante scripts o herramientas gráficas, suelen ocurrir dos fallos comunes:
1. **La calavera o el dibujo queda torcido o desalineado.**
2. **Las letras del banner se juntan y forman un bloque ilegible de símbolos.**

A continuación se detalla por qué suceden estos fenómenos y cómo resolverlos de manera precisa.

---

## 🔍 Dónde buscar y cómo generar Arte ASCII

Existen dos categorías principales de arte ASCII:

### 1. Banners de Texto (Nombres y Títulos)
Para convertir texto convencional en letras estilizadas de gran tamaño:
* **Generador en línea recomendado:** Utiliza [TAAG (Text to ASCII Art Generator)](https://patorjk.com/software/taag/).
  * Fuentes recomendadas con estética cyberpunk/hacker:
    * `Bloody` (letras con efecto gótico de goteo).
    * `Slant` (diseño inclinado clásico de terminal).
    * `Mono12` / `Block` (bloques sólidos limpios y de alta visibilidad).
    * `Future` / `Cyberlarge`.
* **Desde la terminal en Linux:**
  Instala los paquetes `toilet` y `figlet`:
  ```bash
  sudo pacman -S figlet toilet
  ```
  Puedes probar diferentes fuentes directamente:
  ```bash
  toilet -f mono12 -w 120 "TUNOMBRE"
  toilet -f future -w 120 "TUNOMBRE"
  figlet -f slant "TUNOMBRE"
  ```

### 2. Ilustraciones e Íconos (Calaveras, Logos y Gráficos)
* **[ASCII Art Archive](https://www.asciiart.eu/)**: Catálogo extenso de arte en texto libre (secciones recomendadas: skulls, dragons, cyber, gaming).
* **Conversión de imágenes a texto:**
  Herramientas como `chafa` permiten transformar archivos PNG o JPG en secuencias ASCII/ANSI:
  ```bash
  sudo pacman -S chafa
  chafa --format=symbols --size=60x30 mi_imagen.png
  ```

---

## ⚠️ El Problema del Dibujo Torcido (Y por qué se pierde la simetría)

### Origen del fallo:
Muchos scripts cometen el error de centrar el texto línea por línea:
```python
# ❌ ERROR COMÚN: Centrar cada línea de forma individual
for line in ascii_art_lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    line_width = bbox[2] - bbox[0]
    draw.text(((1920 - line_width) // 2, y), line, fill=color)
    y += line_height
```

**Por qué esto deforma la imagen:**
En el arte ASCII, las líneas contienen cantidades variables de espacios en blanco al inicio (` `).
Si se calcula el centro de cada línea en función de su propio ancho visible, las líneas más cortas se desplazarán hacia el centro relativo y las más largas hacia los extremos. Como resultado, elementos simétricos (ojos, mandíbula, alas) quedan completamente descuadrados.

### ✅ La Solución Correcta: Centrado del BLOQUE COMPLETO
Se debe calcular el ancho máximo considerando la línea más extensa del bloque y fijar **la misma coordenada X de inicio para todas las líneas**:

```python
# ✔️ MÉTODO CORRECTO: Usar un punto X de anclaje uniforme
max_block_width = 0
for line in ascii_art_lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    w = bbox[2] - bbox[0]
    if w > max_block_width:
        max_block_width = w

# Coordenada X única para todo el conjunto
start_x = (1920 - max_block_width) // 2

for line in ascii_art_lines:
    draw.text((start_x, y), line, fill=color, font=font)
    y += line_height
```
Con este enfoque, la geometría y proporciones originales se conservan intactas al 100%.

---

## ⚠️ El Problema de Caracteres Amontonados (Colisión tipográfica)

Al utilizar tipografías que emplean caracteres densos de semitono o bloque (`░`, `▒`, `▓`, `█`):
* Si las matrices de cada letra no cuentan con un margen lateral de 1 o 2 espacios, los bordes de caracteres adyacentes colisionan.
* Al renderizarse en la pantalla de inicio, las letras pierden su silueta y el texto se vuelve incomprensible.

### ✅ La Solución:
Al componer palabras con matrices ASCII, es indispensable garantizar que cada carácter cuente con dimensiones proporcionales y un margen uniforme constante:

```python
# Definición de letras con matriz uniforme y padding
G = ["  ▄████  ", " ██▒ ▀█▒ ", "▒██░▄▄▄░ ", "░▓█  ██▓░", "░▒▓███▀▒ ", " ░▒   ▒  "]
A = [" ▄▄▄     ", "▒████▄   ", "▒██  ▀█▄ ", "░██▄▄▄▄██", " ▓█   ▓██", " ▒▒   ▓▒█"]

# Al concatenar caracteres, se agrega una separación fija
for row in range(6):
    banner_lines[row] += letra[row] + "  "
```

---

## 📐 Regla Obligatoria: Fuente Monospace

Todo arte ASCII requiere estrictamente una **tipografía monoespaciada** (Monospace).
* En una fuente proporcional (como Arial o Roboto), un espacio ocupa mucho menos ancho que un carácter alfabético, lo que destruye la alineación de columnas.
* Se recomienda utilizar fuentes profesionales como **JetBrains Mono Nerd Font** (`JetBrainsMonoNerdFontMono-Bold.ttf`) para máxima nitidez y compatibilidad.
