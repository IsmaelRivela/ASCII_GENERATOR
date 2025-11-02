from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import gradio as gr
import io
import random
import xml.etree.ElementTree as ET
import os
import base64
import tempfile

# Constantes de paths
BASE_DIR = os.path.dirname(__file__)
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
PRESETS_DIR = os.path.join(BASE_DIR, 'presets')
TULIPANA_PATH = os.path.join(FONTS_DIR, 'tulipana_gliph.ttf')
RUSHMORE_PATH = os.path.join(FONTS_DIR, 'Rushmore-Gliphs.ttf')

# Crear carpeta de presets si no existe
if not os.path.exists(PRESETS_DIR):
    os.makedirs(PRESETS_DIR)

# Diccionario de fuentes disponibles
FUENTES_DISPONIBLES = {
    "Tulipana": {
        "path": TULIPANA_PATH,
        "nombre": "TulipanaGliph",
        "caracteres_default": "abcdefghijklmno"
    },
    "Rushmore": {
        "path": RUSHMORE_PATH,
        "nombre": "RushmoreGliphs",
        "caracteres_default": "abcdefghijklmno"
    }
}

def generar_archivo_parametros(params_dict, output_dir=None):
    """Genera un archivo .txt con todos los parámetros usados"""
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"parametros_ascii_art_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("PARÁMETROS DE GENERACIÓN - ASCII ART CONVERTER PRO\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        f.write("--- CONFIGURACIÓN BÁSICA ---\n")
        f.write(f"Fuente seleccionada: {params_dict.get('fuente', 'N/A')}\n")
        f.write(f"Caracteres ASCII: {params_dict.get('caracteres', 'N/A')}\n")
        f.write(f"Modo de salida: {params_dict.get('modo_salida', 'N/A')}\n")
        f.write(f"Ancho (caracteres): {params_dict.get('ancho', 'N/A')}\n")
        f.write(f"Contraste: {params_dict.get('contraste', 'N/A')}\n")
        f.write(f"Ratio vertical: {params_dict.get('ratio', 'N/A')}\n\n")
        
        f.write("--- PARÁMETROS VISUALES ---\n")
        f.write(f"Escala de resolución: {params_dict.get('escala_resolucion', 'N/A')}x\n")
        f.write(f"Tamaño de fuente base: {params_dict.get('font_size', 'N/A')}px\n")
        f.write(f"Altura de línea: {params_dict.get('line_height', 'N/A')}\n")
        f.write(f"Solapamiento: {params_dict.get('solapamiento', 'N/A')}%\n")
        f.write(f"Super denso (2x): {'Sí' if params_dict.get('super_denso') else 'No'}\n\n")
        
        f.write("--- COLORES Y EFECTOS ---\n")
        f.write(f"Invertir colores: {'Sí' if params_dict.get('invertir_colores') else 'No'}\n")
        f.write(f"Invertir orden caracteres: {'Sí' if params_dict.get('invertir') else 'No'}\n")
        f.write(f"Color de caracteres: {params_dict.get('color_caracteres', 'N/A')}\n")
        f.write(f"Fondo transparente: {'Sí' if params_dict.get('fondo_transparente') else 'No'}\n\n")
        
        f.write("--- MODOS ESPECIALES ---\n")
        f.write(f"Modo aleatorio: {'Sí' if params_dict.get('modo_aleatorio') else 'No'}\n")
        if params_dict.get('modo_aleatorio'):
            f.write(f"  └─ Umbral de negro: {params_dict.get('umbral_negro', 'N/A')}\n")
        f.write(f"Sistema de capas: {'Sí' if params_dict.get('usar_capas') else 'No'}\n")
        if params_dict.get('usar_capas'):
            f.write(f"  └─ Número de capas: {params_dict.get('num_capas', 'N/A')}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("Para reproducir estos resultados, usa exactamente estos valores.\n")
        f.write("=" * 60 + "\n")
    
    return filepath

def guardar_preset(nombre, params_dict):
    """Guarda un preset de configuración"""
    import json
    filepath = os.path.join(PRESETS_DIR, f"{nombre}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(params_dict, f, indent=2, ensure_ascii=False)
    return filepath

def cargar_preset(nombre):
    """Carga un preset de configuración"""
    import json
    filepath = os.path.join(PRESETS_DIR, f"{nombre}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def listar_presets():
    """Lista todos los presets disponibles"""
    if not os.path.exists(PRESETS_DIR):
        return []
    presets = [f.replace('.json', '') for f in os.listdir(PRESETS_DIR) if f.endswith('.json')]
    return sorted(presets)

def eliminar_preset(nombre):
    """Elimina un preset"""
    filepath = os.path.join(PRESETS_DIR, f"{nombre}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def generar_svg(pixels, ancho_real, altura, caracteres, font_size, line_height, 
            char_width_ratio, modo_aleatorio, umbral_negro, usar_capas, 
            num_capas, invertir_colores, fuente_seleccionada="Tulipana"):
    """Genera SVG vectorial con Tulipana Gliph, omitiendo caracteres de fondo blanco"""
    char_width = font_size * char_width_ratio
    char_height = font_size * line_height

    svg_width = int(ancho_real * char_width) + 40
    svg_height = int(altura * char_height) + 40

    # Embeber la fuente seleccionada en base64 para compatibilidad con Illustrator
    font_face_css = ''
    font_info = FUENTES_DISPONIBLES.get(fuente_seleccionada, FUENTES_DISPONIBLES["Tulipana"])
    font_path = font_info["path"]
    font_name = font_info["nombre"]
    
    try:
        if os.path.exists(font_path):
            with open(font_path, 'rb') as f:
                font_b64 = base64.b64encode(f.read()).decode('ascii')
            font_face_css = f"@font-face {{font-family: '{font_name}'; src: url('data:font/truetype;base64,{font_b64}') format('truetype');}}"
    except Exception:
        font_face_css = ''

    # SVG sin fondo (transparente) - solo renderizamos los caracteres
    svg_lines = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        f'<defs><style type="text/css">{font_face_css} text {{ font-family: "{font_name}", monospace; font-size: {font_size}px; }}</style></defs>',
        f'<g font-family="{font_name}, monospace" font-size="{font_size}px">'
    ]

    char_list = list(caracteres.strip())
    
    # Umbral para considerar un pixel como "blanco" (fondo que no debe renderizarse)
    UMBRAL_BLANCO = 240  # Pixels > 240 se consideran fondo blanco y se omiten

    y_pos = 20
    for y in range(altura):
        x_pos = 20
        for x in range(ancho_real):
            idx = y * ancho_real + x
            if idx < len(pixels):
                pixel = pixels[idx]
                
                # OMITIR pixels blancos/cercanos al blanco (fondo)
                if pixel > UMBRAL_BLANCO:
                    x_pos += char_width
                    continue

                # Generar escala de grises completa basada en el valor del pixel
                # Mapear pixel (0-255) a un caracter de la lista
                char_idx = int((pixel / 255) * (len(caracteres) - 1))
                char = caracteres[char_idx]
                
                # Generar color en escala de grises basado en el pixel
                # Invertir si es necesario (negro sobre blanco vs blanco sobre negro)
                if invertir_colores:
                    color_val = pixel  # Más claro = más blanco
                else:
                    color_val = 255 - pixel  # Más oscuro = más negro
                
                color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
                
                # Escapar caracteres especiales XML
                char_escaped = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Solo agregar al SVG si no es un espacio y no es fondo blanco
                if char.strip():  # Omitir espacios
                    svg_lines.append(f'<text x="{x_pos}" y="{y_pos}" fill="{color}">{char_escaped}</text>')

            x_pos += char_width
        y_pos += char_height

    svg_lines.append('</g>')
    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)

def procesar_imagen(imagen, caracteres, ancho, contraste, ratio, invertir, 
             solapamiento, font_size, line_height, super_denso, modo_salida,
             usar_capas, num_capas, modo_aleatorio, umbral_negro, 
             escala_resolucion, invertir_colores, color_caracteres="auto", 
             fondo_transparente=False, fuente_seleccionada="Tulipana"):
    if imagen is None:
        return None, "Por favor, sube una imagen primero", None, None

    if not caracteres or caracteres.strip() == "":
        caracteres = "@%#*+=-:. "

    # Crear diccionario de parámetros para exportar
    params_dict = {
        'fuente': fuente_seleccionada,
        'caracteres': caracteres,
        'modo_salida': modo_salida,
        'ancho': ancho,
        'contraste': contraste,
        'ratio': ratio,
        'escala_resolucion': escala_resolucion,
        'font_size': font_size,
        'line_height': line_height,
        'solapamiento': solapamiento,
        'super_denso': super_denso,
        'invertir_colores': invertir_colores,
        'invertir': invertir,
        'color_caracteres': color_caracteres,
        'fondo_transparente': fondo_transparente,
        'modo_aleatorio': modo_aleatorio,
        'umbral_negro': umbral_negro,
        'usar_capas': usar_capas,
        'num_capas': num_capas
    }

    try:
        if invertir and not modo_aleatorio:
            caracteres = caracteres[::-1]

        img = imagen.copy()
        aspecto = img.height / img.width

        ancho_real = ancho * 2 if super_denso else ancho
        altura = int(ancho_real * aspecto * ratio)

        img = img.resize((ancho_real, altura))
        img = img.convert('L')
        img = img.filter(ImageFilter.SHARPEN)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contraste)

        pixels = list(img.getdata())

        char_list = list(caracteres.strip())

        if modo_salida == "Preview (Texto)":
            ascii_lines = []
            for y in range(min(altura, 50)):  # Limitar preview
                line = ""
                for x in range(ancho_real):
                    idx = y * ancho_real + x
                    if idx < len(pixels):
                        pixel = pixels[idx]

                        if modo_aleatorio:
                            if pixel < umbral_negro:
                                line += random.choice(char_list)
                            else:
                                line += " "
                        else:
                            char_idx = int((pixel / 255) * (len(caracteres) - 1))
                            line += caracteres[char_idx]
                ascii_lines.append(line)

            texto_preview = '\n'.join(ascii_lines)
            # No generar archivo de parámetros para preview
            return texto_preview, f"Preview generado ({len(ascii_lines)} líneas)", None, None

        elif modo_salida == "Imagen PNG (Alta Resolución)":
            # Aplicar escala de resolución (limitar para evitar MemoryError)
            escala_effectiva = min(max(1, escala_resolucion), 8)
            char_width = font_size * 0.6 * escala_effectiva
            char_height = font_size * line_height * escala_effectiva
            font_size_scaled = int(font_size * escala_effectiva)

            if solapamiento > 0:
                char_width = char_width * (1 - solapamiento / 100)

            img_width = int(ancho_real * char_width) + 40
            img_height = int(altura * char_height) + 40

            # Protección: si la imagen es demasiado grande, reducir escala
            MAX_DIM = 10000
            if img_width > MAX_DIM or img_height > MAX_DIM:
                factor = max(img_width / MAX_DIM, img_height / MAX_DIM)
                escala_effectiva = max(1, escala_effectiva / factor)
                char_width = font_size * 0.6 * escala_effectiva
                char_height = font_size * line_height * escala_effectiva
                font_size_scaled = int(max(4, font_size * escala_effectiva))
                img_width = int(ancho_real * char_width) + 40
                img_height = int(altura * char_height) + 40

            # Color de fondo según invertir_colores y transparencia
            if fondo_transparente:
                bg_color = (255, 255, 255, 0)  # Transparente
                png_img = Image.new('RGBA', (img_width, img_height), bg_color)
            else:
                bg_color = (255, 255, 255) if not invertir_colores else (0, 0, 0)
                png_img = Image.new('RGB', (img_width, img_height), bg_color)
            draw = ImageDraw.Draw(png_img)

            # Cargar fuente seleccionada
            font_used = None
            font = None
            font_info = FUENTES_DISPONIBLES.get(fuente_seleccionada, FUENTES_DISPONIBLES["Tulipana"])
            font_path = font_info["path"]
            
            try:
                # Cargar la fuente seleccionada
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size_scaled)
                    font_used = f"{fuente_seleccionada} ({os.path.basename(font_path)})"
                else:
                    font = ImageFont.load_default()
                    font_used = "default"
            except Exception as e:
                font = ImageFont.load_default()
                font_used = f"default (error: {str(e)})"

            if modo_aleatorio:
                y_pos = 20
                for y in range(altura):
                    x_pos = 20
                    for x in range(ancho_real):
                        idx = y * ancho_real + x
                        if idx < len(pixels):
                            pixel = pixels[idx]

                        if pixel < umbral_negro:
                            char = random.choice(char_list)
                            # Color personalizado o por defecto (negro sobre blanco, o viceversa si invertido)
                            if color_caracteres != "auto":
                                color_fijo = tuple(int(color_caracteres.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                            else:
                                color_fijo = (0, 0, 0) if not invertir_colores else (255, 255, 255)
                            draw.text((x_pos, y_pos), char, font=font, fill=color_fijo)

                        x_pos += char_width
                    y_pos += char_height

                # Generar archivo de parámetros
                params_file = generar_archivo_parametros(params_dict)
                status_msg = f"PNG generado {img_width}x{img_height}px (Escala: {escala_resolucion}x) (fuente: {font_used})"
                return png_img, status_msg, None, params_file

            elif usar_capas and num_capas > 1:
                for capa in range(num_capas):
                    rango_inicio = int((capa / num_capas) * 255)
                    rango_fin = int(((capa + 1) / num_capas) * 255)

                    y_pos = 20
                    for y in range(altura):
                        x_pos = 20
                        for x in range(ancho_real):
                            idx = y * ancho_real + x
                            if idx < len(pixels):
                                pixel = pixels[idx]

                            if rango_inicio <= pixel < rango_fin:
                                pos_en_rango = (pixel - rango_inicio) / max(1, (rango_fin - rango_inicio))
                                char_idx = int(pos_en_rango * (len(caracteres) - 1))
                                char = caracteres[char_idx]

                                # Color personalizado o por defecto (negro sobre blanco, o viceversa si invertido)
                                if color_caracteres != "auto":
                                    color_fijo = tuple(int(color_caracteres.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                                else:
                                    color_fijo = (0, 0, 0) if not invertir_colores else (255, 255, 255)
                                draw.text((x_pos, y_pos), char, font=font, fill=color_fijo)

                            x_pos += char_width
                        y_pos += char_height

                # Generar archivo de parámetros
                params_file = generar_archivo_parametros(params_dict)
                status_msg = f"PNG generado {img_width}x{img_height}px ({num_capas} capas, Escala: {escala_resolucion}x) (fuente: {font_used})"
                return png_img, status_msg, None, params_file
            else:
                y_pos = 20
                for y in range(altura):
                    x_pos = 20
                    for x in range(ancho_real):
                        idx = y * ancho_real + x
                        if idx < len(pixels):
                            pixel = pixels[idx]
                            char_idx = int((pixel / 255) * (len(caracteres) - 1))
                            char = caracteres[char_idx]

                            color_val = 255 if not invertir_colores else 0
                            if invertir_colores:
                                color_val = pixel
                            else:
                                color_val = 255 - pixel

                            draw.text((x_pos, y_pos), char, font=font, fill=(color_val, color_val, color_val))
                        x_pos += char_width
                    y_pos += char_height

                # Generar archivo de parámetros
                params_file = generar_archivo_parametros(params_dict)
                status_msg = f"PNG generado {img_width}x{img_height}px (Escala: {escala_resolucion}x) (fuente: {font_used})"
                return png_img, status_msg, None, params_file

        elif modo_salida == "Vector SVG (Escalable)":
            svg_content = generar_svg(
                pixels, ancho_real, altura, caracteres, font_size, 
                line_height, 0.6, modo_aleatorio, umbral_negro,
                usar_capas, num_capas, invertir_colores, fuente_seleccionada
            )

            # Generar archivo de parámetros
            params_file = generar_archivo_parametros(params_dict)
            return None, f"SVG generado ({ancho_real}x{altura} caracteres) - Escalable infinitamente", svg_content, params_file

        elif modo_salida == "Texto completo (TXT)":
            ascii_lines = []
            for y in range(altura):
                line = ""
                for x in range(ancho_real):
                    idx = y * ancho_real + x
                    if idx < len(pixels):
                        pixel = pixels[idx]

                        if modo_aleatorio:
                            if pixel < umbral_negro:
                                line += random.choice(char_list)
                            else:
                                line += " "
                        else:
                            char_idx = int((pixel / 255) * (len(caracteres) - 1))
                            line += caracteres[char_idx]
                ascii_lines.append(line)

            texto_completo = '\n'.join(ascii_lines)
            # Generar archivo de parámetros
            params_file = generar_archivo_parametros(params_dict)
            return texto_completo, f"Texto generado {len(ascii_lines)} líneas", None, params_file

    except Exception as e:
        return None, f"Error: {str(e)}", None, None

def crear_interfaz():
    # Tema personalizado blanco y negro minimalista
    custom_theme = gr.themes.Base(
        primary_hue=gr.themes.colors.slate,
        secondary_hue=gr.themes.colors.gray,
        neutral_hue=gr.themes.colors.slate,
        font=gr.themes.GoogleFont("Inter"),
    ).set(
        body_background_fill='#FFFFFF',
        body_text_color='#1a1a1a',
        button_primary_background_fill='#000000',
        button_primary_background_fill_hover='#2a2a2a',
        button_primary_text_color='#FFFFFF',
        button_secondary_background_fill='#F5F5F5',
        button_secondary_background_fill_hover='#E5E5E5',
        button_secondary_text_color='#1a1a1a',
        block_background_fill='#FAFAFA',
        block_border_color='#E0E0E0',
        block_label_text_color='#1a1a1a',
        block_title_text_color='#000000',
        input_background_fill='#FFFFFF',
        input_border_color='#D0D0D0',
        slider_color='#000000',
    )
    
    # CSS personalizado para hacer sticky el preview
    custom_css = """
    .preview-container {
        position: sticky !important;
        top: 20px !important;
        max-height: calc(100vh - 40px) !important;
        overflow-y: auto !important;
    }
    
    .main-title {
        font-weight: 700 !important;
        color: #000000 !important;
        font-size: 2em !important;
        margin-bottom: 0.5em !important;
        letter-spacing: -0.02em !important;
    }
    
    .subtitle {
        color: #4a4a4a !important;
        font-size: 1.1em !important;
        margin-bottom: 2em !important;
    }
    
    .section-header {
        font-weight: 600 !important;
        color: #000000 !important;
        border-bottom: 2px solid #000000 !important;
        padding-bottom: 0.5em !important;
        margin-top: 1.5em !important;
        margin-bottom: 1em !important;
    }
    """
    
    with gr.Blocks(title="ASCII Art Converter PRO", theme=custom_theme, css=custom_css) as demo:
        gr.Markdown("# ASCII Art Converter PRO", elem_classes="main-title")
        gr.Markdown("Genera arte ASCII en **alta resolución** (PNG) o **formato vectorial** (SVG) para cualquier tamaño", elem_classes="subtitle")

        # Variable para SVG download
        svg_output = gr.State()

        with gr.Row():
            with gr.Column(scale=1):
                imagen_input = gr.Image(
                    label="Sube tu imagen",
                    type="pil",
                    height=300
                )

                gr.Markdown("### Configuración", elem_classes="section-header")

                caracteres_input = gr.Textbox(
                    label="Caracteres ASCII",
                    value="abcdefghijklmno",
                    placeholder="Usa: abcdefghijklmno"
                )

                fuente_selector = gr.Radio(
                    label="Seleccionar fuente",
                    choices=["Tulipana", "Rushmore"],
                    value="Tulipana",
                    info="Cambia entre las fuentes disponibles"
                )

                modo_salida = gr.Radio(
                    label="Formato de salida",
                    choices=[
                        "Imagen PNG (Alta Resolución)", 
                        "Vector SVG (Escalable)",
                        "Texto completo (TXT)"
                    ],
                    value="Imagen PNG (Alta Resolución)"
                )

                with gr.Row():
                    invertir_colores_check = gr.Checkbox(
                        label="Invertir colores",
                        value=False,
                        info="Blanco sobre negro ↔ Negro sobre blanco"
                    )
                    preview_live_check = gr.Checkbox(
                        label="Preview en vivo",
                        value=False,
                        info="Actualiza automáticamente (puede ser lento)"
                    )
                
                with gr.Row():
                    color_picker = gr.ColorPicker(
                        label="Color de caracteres",
                        value="#000000",
                        info="Elige el color de los caracteres (o deja auto)"
                    )
                    fondo_transparente_check = gr.Checkbox(
                        label="Fondo transparente",
                        value=False,
                        info="PNG con fondo transparente (solo PNG)"
                    )

                with gr.Accordion("Parámetros básicos", open=True):
                    ancho_slider = gr.Slider(
                        label="Ancho (caracteres)",
                        minimum=30,
                        maximum=300,
                        value=100,
                        step=10
                    )

                    contraste_slider = gr.Slider(
                        label="Contraste",
                        minimum=0.5,
                        maximum=3.0,
                        value=1.5,
                        step=0.1
                    )

                    ratio_slider = gr.Slider(
                        label="Ratio vertical",
                        minimum=0.3,
                        maximum=1.0,
                        value=0.55,
                        step=0.05
                    )

                    escala_resolucion = gr.Slider(
                        label="Escala de resolución (PNG)",
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1,
                        info="1x=normal, 5x=print, 10x=gran formato"
                    )

                with gr.Accordion("Modo aleatorio (logos/siluetas)", open=False):
                    modo_aleatorio_check = gr.Checkbox(
                        label="Activar modo aleatorio",
                        value=False,
                        info="Rellena zonas oscuras con caracteres random"
                    )

                    umbral_negro_slider = gr.Slider(
                        label="Umbral de negro",
                        minimum=0,
                        maximum=255,
                        value=128,
                        step=5
                    )

                with gr.Accordion("Sistema de capas (fotografías)", open=False):
                    usar_capas_check = gr.Checkbox(
                        label="Activar sistema de capas",
                        value=False
                    )

                    num_capas_slider = gr.Slider(
                        label="Número de capas",
                        minimum=2,
                        maximum=10,
                        value=4,
                        step=1
                    )

                with gr.Accordion("Parámetros avanzados", open=False):
                    solapamiento_slider = gr.Slider(
                        label="Solapamiento (%)",
                        minimum=0,
                        maximum=60,
                        value=20,
                        step=5
                    )

                    font_size_slider = gr.Slider(
                        label="Tamaño de fuente base (px)",
                        minimum=4,
                        maximum=20,
                        value=8,
                        step=1,
                        info="Se multiplica por la escala"
                    )

                    line_height_slider = gr.Slider(
                        label="Altura de línea",
                        minimum=0.3,
                        maximum=1.5,
                        value=0.6,
                        step=0.05
                    )

                    invertir_check = gr.Checkbox(
                        label="Invertir orden de caracteres",
                        value=False
                    )

                    super_denso_check = gr.Checkbox(
                        label="Super denso (2x resolución)",
                        value=False
                    )
            
                procesar_btn = gr.Button("Generar ASCII Art", variant="primary", size="lg")

                gr.Markdown("### Presets de caracteres", elem_classes="section-header")
                gr.Markdown("**Para ambas fuentes (Tulipana & Rushmore)**")
                with gr.Row():
                    preset_tulipana = gr.Button("Tulipana", size="sm")
                    preset_flores = gr.Button("Flores", size="sm")
                    preset_bloques = gr.Button("Bloques", size="sm")
                    preset_clasico = gr.Button("Clásico", size="sm")

                gr.Markdown("### Gestión de Presets Personalizados", elem_classes="section-header")
                with gr.Row():
                    nombre_preset_input = gr.Textbox(
                        label="Nombre del preset",
                        placeholder="Ej: mi_configuracion_favorita",
                        scale=2
                    )
                    guardar_preset_btn = gr.Button("Guardar", size="sm", scale=1)
                
                presets_dropdown = gr.Dropdown(
                    label="Cargar preset guardado",
                    choices=listar_presets(),
                    interactive=True
                )
                
                with gr.Row():
                    cargar_preset_btn = gr.Button("Cargar Preset", size="sm")
                    eliminar_preset_btn = gr.Button("Eliminar Preset", size="sm", variant="stop")
                    actualizar_lista_btn = gr.Button("Actualizar Lista", size="sm")

            with gr.Column(scale=1, elem_classes="preview-container"):
                gr.Markdown("### 🖼️ Preview / Resultado", elem_classes="section-header")

                output_preview = gr.Image(
                    label="Resultado PNG",
                    type="pil",
                    height=500
                )

                svg_download = gr.File(
                    label="Descargar SVG",
                    visible=False
                )

                params_download = gr.File(
                    label="Descargar Parámetros (.txt)",
                    visible=True
                )

                status_text = gr.Textbox(
                    label="Estado",
                    value="Esperando imagen...",
                    interactive=False
                )

            def cambiar_vista(modo):
                # Simplificado: solo controlar visibilidad de PNG y SVG
                if modo == "Imagen PNG (Alta Resolución)":
                    return gr.update(visible=True), gr.update(visible=False)
                elif modo == "Vector SVG (Escalable)":
                    return gr.update(visible=False), gr.update(visible=True)
                else:
                    return gr.update(visible=False), gr.update(visible=False)

            modo_salida.change(
                fn=cambiar_vista,
                inputs=[modo_salida],
                outputs=[output_preview, svg_download]
            )

        def procesar_wrapper(img, chars, fuente, ancho, contraste, ratio, invertir, 
                           solap, font, lh, denso, modo, usar_capas, num_capas,
                           modo_aleatorio, umbral_negro, escala, invertir_colores, color_chars, fondo_transp):
            resultado, status, svg_data, params_file = procesar_imagen(
                img, chars, ancho, contraste, ratio, invertir, 
                solap, font, lh, denso, modo, usar_capas, num_capas,
                modo_aleatorio, umbral_negro, escala, invertir_colores, color_chars, fondo_transp, fuente
            )
            # Debemos devolver siempre 5 valores: output_preview, svg_download, params_download, status, svg_output
            if modo == "Imagen PNG (Alta Resolución)":
                return gr.update(value=resultado, visible=True), gr.update(visible=False), params_file, status, svg_data

            elif modo == "Vector SVG (Escalable)":
                # Guardar SVG como archivo en temp dir multiplataforma para descarga
                if svg_data:
                    tmp = tempfile.gettempdir()
                    svg_path = os.path.join(tmp, 'ascii_art.svg')
                    with open(svg_path, "w", encoding="utf-8") as f:
                        f.write(svg_data)
                    return gr.update(visible=False), gr.update(value=svg_path, visible=True), params_file, status, svg_data
                return gr.update(visible=False), gr.update(visible=False), params_file, status, None

            else:
                # Texto completo
                return gr.update(value=resultado, visible=False), gr.update(visible=False), params_file, status, svg_data

        # Procesar con botón
        procesar_btn.click(
            fn=procesar_wrapper,
            inputs=[
                imagen_input, caracteres_input, fuente_selector, ancho_slider, contraste_slider, 
                ratio_slider, invertir_check, solapamiento_slider, font_size_slider, 
                line_height_slider, super_denso_check, modo_salida, usar_capas_check, 
                num_capas_slider, modo_aleatorio_check, umbral_negro_slider,
                escala_resolucion, invertir_colores_check, color_picker, fondo_transparente_check
            ],
            outputs=[output_preview, svg_download, params_download, status_text, svg_output]
        )

        # Preview en vivo (opcional)
        def preview_live_wrapper(preview_enabled, img, chars, fuente, ancho, contraste, ratio, invertir, 
                                 solap, font, lh, denso, modo, usar_capas, num_capas, modo_aleatorio, umbral, escala, invertir_colores, color_chars, fondo_transp):
            if preview_enabled and img is not None:
                resultado, status, svg_data, params_file = procesar_imagen(
                    img, chars, ancho, contraste, ratio, invertir, solap, font, lh, denso,
                    modo, usar_capas, num_capas, modo_aleatorio, umbral, escala, invertir_colores, color_chars, fondo_transp, fuente
                )
                if modo == "Imagen PNG (Alta Resolución)":
                    return resultado, gr.update(visible=False), params_file, status, svg_data

                if modo == "Vector SVG (Escalable)":
                    if svg_data:
                        tmp = tempfile.gettempdir()
                        svg_path = os.path.join(tmp, 'ascii_art_preview.svg')
                        with open(svg_path, "w", encoding="utf-8") as f:
                            f.write(svg_data)
                        return gr.update(visible=False), gr.update(value=svg_path, visible=True), params_file, status, svg_data
                    return gr.update(visible=False), gr.update(visible=False), params_file, status, None

                # Texto completo
                return resultado, gr.update(visible=False), params_file, status, svg_data

            return gr.update(), gr.update(), None, "Preview en vivo desactivado", None

        # Conectar inputs relevantes al preview en vivo
        live_inputs = [
            preview_live_check, imagen_input, caracteres_input, fuente_selector, ancho_slider, contraste_slider,
            ratio_slider, invertir_check, solapamiento_slider, font_size_slider, line_height_slider,
            super_denso_check, modo_salida, usar_capas_check, num_capas_slider, modo_aleatorio_check,
            umbral_negro_slider, escala_resolucion, invertir_colores_check, color_picker, fondo_transparente_check
        ]

        # Registrar cambios: cuando cualquiera cambie, si preview_live_check está activado, actualizar
        for comp in [imagen_input, caracteres_input, fuente_selector, ancho_slider, contraste_slider, ratio_slider, invertir_check,
                     solapamiento_slider, font_size_slider, line_height_slider, super_denso_check, modo_salida,
                     usar_capas_check, num_capas_slider, modo_aleatorio_check, umbral_negro_slider, escala_resolucion,
                     invertir_colores_check, color_picker, fondo_transparente_check]:
            comp.change(
                fn=preview_live_wrapper,
                inputs=live_inputs,
                outputs=[output_preview, svg_download, params_download, status_text, svg_output]
            )

        # Función para cambiar caracteres automáticamente según la fuente
        def cambiar_fuente(fuente_seleccionada):
            font_info = FUENTES_DISPONIBLES.get(fuente_seleccionada, FUENTES_DISPONIBLES["Tulipana"])
            return font_info["caracteres_default"]

        # Conectar cambio de fuente
        fuente_selector.change(
            fn=cambiar_fuente,
            inputs=[fuente_selector],
            outputs=[caracteres_input]
        )

        # Presets - Caracteres personalizados
        preset_tulipana.click(
            fn=lambda: "abcdefghijklmno",
            outputs=caracteres_input
        )

        preset_flores.click(
            fn=lambda: "❀✿@#*+○◉●◎",
            outputs=caracteres_input
        )

        preset_bloques.click(
            fn=lambda: "█▓▒░ ",
            outputs=caracteres_input
        )

        preset_clasico.click(
            fn=lambda: "@%#*+=-:. ",
            outputs=caracteres_input
        )

        # Gestión de presets personalizados
        def guardar_preset_handler(nombre, chars, fuente, ancho, contraste, ratio, invertir,
                                   solap, font, lh, denso, usar_capas, num_capas, modo_aleatorio,
                                   umbral, escala, invertir_colores, color_chars, fondo_transp):
            if not nombre or nombre.strip() == "":
                return "❌ Error: Debes especificar un nombre para el preset", gr.update()
            
            params = {
                'caracteres': chars,
                'fuente': fuente,
                'ancho': ancho,
                'contraste': contraste,
                'ratio': ratio,
                'invertir': invertir,
                'solapamiento': solap,
                'font_size': font,
                'line_height': lh,
                'super_denso': denso,
                'usar_capas': usar_capas,
                'num_capas': num_capas,
                'modo_aleatorio': modo_aleatorio,
                'umbral_negro': umbral,
                'escala_resolucion': escala,
                'invertir_colores': invertir_colores,
                'color_caracteres': color_chars,
                'fondo_transparente': fondo_transp
            }
            
            try:
                guardar_preset(nombre, params)
                return f"✅ Preset '{nombre}' guardado correctamente", gr.update(choices=listar_presets())
            except Exception as e:
                return f"❌ Error al guardar preset: {str(e)}", gr.update()

        def cargar_preset_handler(nombre):
            if not nombre:
                return [None] * 18 + ["❌ Selecciona un preset primero"]
            
            params = cargar_preset(nombre)
            if params:
                return [
                    params.get('caracteres', ''),
                    params.get('fuente', 'Tulipana'),
                    params.get('ancho', 100),
                    params.get('contraste', 1.5),
                    params.get('ratio', 0.55),
                    params.get('invertir', False),
                    params.get('solapamiento', 20),
                    params.get('font_size', 8),
                    params.get('line_height', 0.6),
                    params.get('super_denso', False),
                    params.get('usar_capas', False),
                    params.get('num_capas', 4),
                    params.get('modo_aleatorio', False),
                    params.get('umbral_negro', 128),
                    params.get('escala_resolucion', 3),
                    params.get('invertir_colores', False),
                    params.get('color_caracteres', 'auto'),
                    params.get('fondo_transparente', False),
                    f"✅ Preset '{nombre}' cargado correctamente"
                ]
            return [None] * 18 + [f"❌ No se pudo cargar el preset '{nombre}'"]

        def eliminar_preset_handler(nombre):
            if not nombre:
                return "❌ Selecciona un preset primero", gr.update()
            
            if eliminar_preset(nombre):
                return f"✅ Preset '{nombre}' eliminado", gr.update(choices=listar_presets(), value=None)
            return f"❌ No se pudo eliminar el preset '{nombre}'", gr.update()

        def actualizar_lista_handler():
            return gr.update(choices=listar_presets())

        # Conectar botones de presets
        guardar_preset_btn.click(
            fn=guardar_preset_handler,
            inputs=[
                nombre_preset_input, caracteres_input, fuente_selector, ancho_slider,
                contraste_slider, ratio_slider, invertir_check, solapamiento_slider,
                font_size_slider, line_height_slider, super_denso_check, usar_capas_check,
                num_capas_slider, modo_aleatorio_check, umbral_negro_slider, escala_resolucion,
                invertir_colores_check, color_picker, fondo_transparente_check
            ],
            outputs=[status_text, presets_dropdown]
        )

        cargar_preset_btn.click(
            fn=cargar_preset_handler,
            inputs=[presets_dropdown],
            outputs=[
                caracteres_input, fuente_selector, ancho_slider, contraste_slider,
                ratio_slider, invertir_check, solapamiento_slider, font_size_slider,
                line_height_slider, super_denso_check, usar_capas_check, num_capas_slider,
                modo_aleatorio_check, umbral_negro_slider, escala_resolucion,
                invertir_colores_check, color_picker, fondo_transparente_check, status_text
            ]
        )

        eliminar_preset_btn.click(
            fn=eliminar_preset_handler,
            inputs=[presets_dropdown],
            outputs=[status_text, presets_dropdown]
        )

        actualizar_lista_btn.click(
            fn=actualizar_lista_handler,
            outputs=[presets_dropdown]
        )

        gr.Markdown("""
        ---
        
        ### Tips de uso
        
        **Fuentes disponibles**
        - **Tulipana:** Fuente original del proyecto
        - **Rushmore:** Nueva fuente con estilo diferente
        - Al cambiar fuente se actualizan automáticamente los caracteres por defecto
        
        **Para impresión/gran formato**
        - PNG con escala 5-10x
        - SVG (escalable sin pérdida)
        
        **Para web/redes sociales**
        - PNG escala 2-3x
        
        **Modos especiales**
        - **Aleatorio:** Logos, tipografías, siluetas en blanco y negro
        - **Capas:** Fotografías y degradados complejos
        
        **Otras funciones**
        - **Invertir colores:** Útil para fondos blancos o impresión
        - **Preview en vivo:** Actualiza automáticamente al cambiar valores (puede ser lento con imágenes grandes)
        """)

        return demo


if __name__ == "__main__":
    demo = crear_interfaz()
    demo.launch()