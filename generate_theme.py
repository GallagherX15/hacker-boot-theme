#!/usr/bin/env python3
"""
HACKER GRUB THEME GENERATOR
Genera un background.png personalizado para tu menú de GRUB con estilo hacker/cyberpunk rojo.
Evita el típico bug de arte ASCII torcido calculando el bounding box del bloque completo.
"""

import sys
import os
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageFont

def get_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        # Fallback a tipografías comunes del sistema si no está JetBrains Mono
        fallbacks = [
            "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Bold.ttf",
            "/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        ]
        for fb in fallbacks:
            if os.path.exists(fb):
                return ImageFont.truetype(fb, size)
        print(f"[!] Aviso: No se encontró la fuente '{font_path}', usando fuente por defecto.")
        return ImageFont.load_default()

def generate_banner_lines(text, font_style="bloody"):
    """Genera líneas ASCII usando la matriz interna bloody o herramientas externas (toilet/figlet)"""
    text_clean = text.strip().upper()

    if font_style == "bloody":
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from assets.ascii_templates.bloody_alphabet import render_bloody_text
            lines = render_bloody_text(text_clean, letter_spacing="  ")
            if any(l.strip() for l in lines):
                return lines
        except Exception as e:
            pass

    if font_style in ["mono12", "mono9", "future", "smblock"]:
        try:
            res = subprocess.check_output(['toilet', '-f', font_style, '-w', '120', text_clean], stderr=subprocess.DEVNULL)
            lines = [l for l in res.decode('utf-8', errors='ignore').splitlines() if l.strip()]
            if lines:
                return lines
        except Exception:
            pass

    try:
        res = subprocess.check_output(['figlet', '-f', 'slant', text_clean], stderr=subprocess.DEVNULL)
        lines = [l for l in res.decode('utf-8', errors='ignore').splitlines() if l.strip()]
        if lines:
            return lines
    except Exception:
        pass

    # Fallback básico si no hay figlet/toilet
    return [
        f"  ██████╗  █████╗ ██╗     ██╗      █████╗  ██████╗ ██╗  ██╗███████╗██████╗  ",
        f" ██╔════╝ ██╔══██╗██║     ██║     ██╔══██╗██╔════╝ ██║  ██║██╔════╝██╔══██╗ ",
        f" ██║  ███╗███████║██║     ██║     ███████║██║  ███╗███████║█████╗  ██████╔╝ ",
        f" ██║   ██║██╔══██║██║     ██║     ██╔══██║██║   ██║██╔══██║██╔══╝  ██╔══██╗ ",
        f" ╚██████╔╝██║  ██║███████╗███████╗██║  ██║╚██████╔╝██║  ██║███████╗██║  ██║ ",
        f"  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ "
    ]

def build_background(
    output_path="background.png",
    skull_path=None,
    nickname="GALLAGHERX",
    subtitle="[ GALLAGHER BOOT ]",
    style="bloody",
    banner_font_size=13,
    font_path="/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Bold.ttf",
    scanlines=True,
    width=1920,
    height=1080
):
    print(f"[*] Creando fondo Cyberpunk Red ({width}x{height}) con estilo '{style}'...")
    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Calavera centrada
    skull_y = 35
    sh = 0
    if skull_path and os.path.exists(skull_path):
        try:
            skull = Image.open(skull_path)
            sw, sh = skull.size
            skull_x = (width - sw) // 2
            if skull.mode in ('RGBA', 'LA'):
                img.paste(skull, (skull_x, skull_y), skull)
            else:
                img.paste(skull, (skull_x, skull_y))
            print(f"[+] Calavera colocada en x={skull_x}, y={skull_y} (tamaño: {sw}x{sh})")
        except Exception as e:
            print(f"[!] No se pudo cargar la imagen de la calavera ({e}), continuando sin ella.")
            sh = 100

    # 2. Tipografías
    font_banner = get_font(font_path, banner_font_size)
    font_sub = get_font(font_path, 18)
    font_div = get_font(font_path, 13)
    font_hint = get_font(font_path, 13)

    # 3. Banner ASCII con centrado de BLOQUE COMPLETO
    banner_lines = generate_banner_lines(nickname, font_style=style)
    
    # Calcular el ancho máximo del bloque completo
    max_line_width = 0
    for line in banner_lines:
        bbox = draw.textbbox((0, 0), line, font=font_banner)
        lw = bbox[2] - bbox[0]
        if lw > max_line_width:
            max_line_width = lw

    bx = (width - max_line_width) // 2
    by = skull_y + sh + 15

    for line in banner_lines:
        draw.text((bx, by), line, fill=(255, 45, 45), font=font_banner)
        by += banner_font_size + 3

    by += 15

    # 4. Subtítulo (ej. [ GALLAGHER BOOT ])
    sub_text = subtitle.strip()
    if sub_text:
        bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
        lw = bbox[2] - bbox[0]
        draw.text(((width - lw) // 2, by), sub_text, fill=(245, 35, 35), font=font_sub)
        by += 26

    # 5. Línea divisoria
    div = "─" * 68
    bbox = draw.textbbox((0, 0), div, font=font_div)
    lw = bbox[2] - bbox[0]
    draw.text(((width - lw) // 2, by), div, fill=(130, 15, 15), font=font_div)
    by += 20

    # 6. Prompt de selección
    prompt = ">> SELECT HOST OS TO INITIATE SEQUENCE <<"
    bbox = draw.textbbox((0, 0), prompt, font=font_hint)
    lw = bbox[2] - bbox[0]
    draw.text(((width - lw) // 2, by), prompt, fill=(210, 30, 30), font=font_hint)

    # 7. Efecto CRT Scanlines (líneas sutiles horizontales de monitor retro)
    if scanlines:
        for scan_y in range(0, height, 4):
            draw.line([(0, scan_y), (1920, scan_y)], fill=(5, 0, 0))

    # Guardar
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"[✓] Fondo generado con éxito en: {output_path}")

def interactive_mode():
    print("=" * 60)
    print("  CYBERPUNK RED GRUB THEME - GENERADOR VIBE CODING")
    print("=" * 60)
    print("Vamos a armar tu imagen de fondo en 10 segundos.\n")

    nickname = input("1. Tu Nick / Nombre para el banner (default: GALLAGHERX): ").strip()
    if not nickname:
        nickname = "GALLAGHERX"

    print("\nEstilos de fuente ASCII disponibles:")
    print("  [1] bloody  (Letras sangrantes/góticas con goteo - Recomendado)")
    print("  [2] mono12  (Bloques limpios y sólidos)")
    print("  [3] future  (Estilo futurista)")
    style_choice = input("Elegí estilo [1/2/3] (default: 1): ").strip()
    style_map = {"1": "bloody", "2": "mono12", "3": "future"}
    selected_style = style_map.get(style_choice, "bloody")

    custom_sub = input(f"\n2. Subtítulo debajo del banner (default: [{nickname} BOOT]): ").strip()
    if not custom_sub:
        custom_sub = f"[{nickname} BOOT]"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_skull = os.path.join(script_dir, "assets", "skull_red.png")
    
    skull_choice = input(f"\n3. Ruta de calavera/logo (Enter para usar la que viene incluida): ").strip()
    if not skull_choice:
        skull_choice = default_skull

    out_file = os.path.join(script_dir, "grub", "background.png")

    build_background(
        output_path=out_file,
        skull_path=skull_choice,
        nickname=nickname,
        subtitle=custom_sub,
        style=selected_style
    )
    print("\nListo! El nuevo 'background.png' quedó guardado en la carpeta 'grub/'.")
    print("Ahora podés correr './install.sh' para aplicarlo al sistema.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de fondos para GRUB estilo Hacker")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interactivo con preguntas")
    parser.add_argument("--name", "-n", default="GALLAGHERX", help="Nombre a mostrar en ASCII")
    parser.add_argument("--subtitle", "-s", default="[ GALLAGHER BOOT ]", help="Texto del subtítulo")
    parser.add_argument("--style", choices=["bloody", "mono12", "future", "smblock"], default="bloody", help="Estilo del banner ASCII")
    parser.add_argument("--skull", default=None, help="Ruta de la imagen de calavera")
    parser.add_argument("--out", "-o", default="grub/background.png", help="Ruta de salida")
    parser.add_argument("--no-scanlines", action="store_true", help="Desactivar efecto scanlines CRT")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skull_path = args.skull if args.skull else os.path.join(script_dir, "assets", "skull_red.png")
        build_background(
            output_path=args.out,
            skull_path=skull_path,
            nickname=args.name,
            subtitle=args.subtitle,
            style=args.style,
            scanlines=not args.no_scanlines
        )
