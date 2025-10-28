# 🚀 Instrucciones para Deploy en Hugging Face Spaces

## Pasos para subir tu aplicación:

### 1. Crear cuenta en Hugging Face
- Ve a https://huggingface.co/join
- Crea una cuenta gratuita

### 2. Crear un nuevo Space
- Ve a https://huggingface.co/spaces
- Click en "Create new Space"
- Elige un nombre para tu Space (ej: `ascii-art-converter`)
- Selecciona "Gradio" como SDK
- Elige "Public" o "Private" según prefieras
- Click en "Create Space"

### 3. Subir los archivos

**Opción A: Usando la interfaz web**
1. En tu Space recién creado, click en "Files" → "Add file" → "Upload files"
2. Arrastra y suelta estos archivos:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - La carpeta `fonts/` completa (con `icomoon.ttf` dentro)

**Opción B: Usando Git (recomendado)**
```bash
# Clona el repositorio de tu Space
git clone https://huggingface.co/spaces/TU_USUARIO/TU_SPACE_NAME
cd TU_SPACE_NAME

# Copia los archivos necesarios
cp /ruta/a/ascii_public_v2/app.py .
cp /ruta/a/ascii_public_v2/requirements.txt .
cp /ruta/a/ascii_public_v2/README.md .
cp -r /ruta/a/ascii_public_v2/fonts .

# Commit y push
git add .
git commit -m "Initial commit: ASCII Art Converter PRO"
git push
```

### 4. Esperar el build
- Hugging Face automáticamente detectará el `requirements.txt`
- Instalará las dependencias (Gradio y Pillow)
- Iniciará tu aplicación
- El proceso tarda 2-5 minutos

### 5. ¡Listo!
Tu aplicación estará disponible en:
`https://huggingface.co/spaces/TU_USUARIO/TU_SPACE_NAME`

## 📋 Archivos necesarios (ya están listos):

✅ `app.py` - Aplicación principal
✅ `requirements.txt` - Dependencias (Gradio, Pillow)
✅ `README.md` - Documentación del proyecto
✅ `fonts/icomoon.ttf` - Fuente personalizada
✅ `.gitignore` - Archivos a excluir

## ⚙️ Configuración opcional

Si quieres personalizar más tu Space, puedes crear un archivo `README.md` en la raíz con metadatos:

```yaml
---
title: ASCII Art Converter PRO
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---
```

## 🔧 Solución de problemas

### Si la aplicación no inicia:
1. Verifica los logs en la pestaña "Logs" de tu Space
2. Asegúrate de que `fonts/icomoon.ttf` esté en la carpeta correcta
3. Verifica que las versiones en `requirements.txt` sean compatibles

### Si los glifos no se muestran:
- Asegúrate de que la carpeta `fonts/` esté en la raíz del proyecto
- Verifica que `icomoon.ttf` se haya subido correctamente

## 📊 Recursos de Hugging Face Spaces

**Gratis:**
- 2 vCPU cores
- 16 GB RAM
- 50 GB Storage

**Suficiente para esta aplicación** ✅

## 🎯 Próximos pasos

Después del deploy, puedes:
- Compartir el link público de tu Space
- Embedder el Space en tu sitio web
- Crear una API para uso programático
- Añadir más presets de caracteres
- Implementar más modos de conversión

---

¿Necesitas ayuda? Consulta la documentación oficial:
https://huggingface.co/docs/hub/spaces
