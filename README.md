---
title: ASCII Art Converter PRO
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---

# 🎨 ASCII Art Converter PRO

Convierte imágenes a arte ASCII en alta resolución (PNG) o formato vectorial escalable (SVG).

## ✨ Características

- **Múltiples formatos de salida**: PNG de alta resolución, SVG vectorial escalable, TXT
- **Fuente personalizada IcoMoon**: Usa glifos personalizados para crear arte único
- **Preview en vivo**: Actualización automática al cambiar parámetros
- **Sistema de capas**: Para fotografías con degradados complejos
- **Modo aleatorio**: Ideal para logos, tipografías y siluetas
- **Alta resolución**: Escala hasta 10x para impresión y gran formato
- **Invertir colores**: Blanco sobre negro o negro sobre blanco

## 🚀 Uso

1. **Sube tu imagen** (formatos: JPG, PNG, etc.)
2. **Selecciona el formato de salida**:
   - PNG: Para redes sociales, web o impresión
   - SVG: Escalable infinitamente (compatible con Illustrator)
   - TXT: Texto plano
3. **Ajusta los parámetros**:
   - Ancho y contraste
   - Escala de resolución
   - Caracteres ASCII personalizados
4. **Presets de caracteres**:
   - IcoMoon: `abcdefghijk` (glifos personalizados)
   - Flores: `❀✿@#*+○◉●◎`
   - Bloques: `█▓▒░`
   - Clásico: `@%#*+=-:.`

## 🎯 Modos de conversión

### Modo Normal
Convierte la imagen pixel a pixel usando la rampa de caracteres seleccionada.

### Modo Aleatorio
Rellena las zonas oscuras con caracteres aleatorios. Ideal para logos y siluetas en blanco y negro.

### Sistema de Capas
Divide la imagen en múltiples capas de luminosidad para mayor detalle en fotografías.

## 🖨️ Recomendaciones

**Para impresión/gran formato:**
- Usa PNG con escala 5-10x
- O mejor: SVG (escalable sin pérdida de calidad)

**Para web/redes sociales:**
- PNG escala 2-3x

## 📋 Tecnologías

- **Gradio**: Interfaz web interactiva
- **Pillow (PIL)**: Procesamiento de imágenes
- **Python**: Backend

## 🎨 Fuente IcoMoon

La fuente IcoMoon incluida permite usar glifos personalizados asignados a las letras `abcdefghijk`. Los SVGs generados incluyen la fuente embebida en base64 para compatibilidad con Adobe Illustrator y otros programas de diseño vectorial.

---

Desarrollado con ❤️ para crear arte ASCII de alta calidad
