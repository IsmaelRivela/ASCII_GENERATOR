# 📋 Guía de Presets y Parámetros - ASCII Art Converter PRO

## 🎯 Nuevas Funcionalidades Implementadas

### 1. 📄 Generación Automática de Archivo de Parámetros

Cada vez que generas una imagen ASCII Art (PNG, SVG o TXT), **se crea automáticamente un archivo .txt** con todos los parámetros utilizados.

#### ✨ Características:
- **Descarga automática**: El archivo aparece en el botón "📄 Descargar Parámetros (.txt)"
- **Información completa**: Incluye TODOS los valores usados para generar la imagen
- **Formato legible**: Texto claro y organizado por secciones
- **Timestamp**: Fecha y hora de generación

#### 📝 Contenido del archivo:
```
==============================================================
PARÁMETROS DE GENERACIÓN - ASCII ART CONVERTER PRO
==============================================================

Fecha y hora: 27/10/2025 15:30:45

--- CONFIGURACIÓN BÁSICA ---
Fuente seleccionada: Tulipana
Caracteres ASCII: abcdefghijklmno
Modo de salida: Imagen PNG (Alta Resolución)
Ancho (caracteres): 100
Contraste: 1.5
Ratio vertical: 0.55

--- PARÁMETROS VISUALES ---
Escala de resolución: 3x
Tamaño de fuente base: 8px
Altura de línea: 0.6
Solapamiento: 20%
Super denso (2x): No

--- COLORES Y EFECTOS ---
Invertir colores: No
Invertir orden caracteres: No
Color de caracteres: auto
Fondo transparente: No

--- MODOS ESPECIALES ---
Modo aleatorio: No
Sistema de capas: No

==============================================================
Para reproducir estos resultados, usa exactamente estos valores.
==============================================================
```

#### 🎯 Usos prácticos:
- **Reproducir resultados**: Sabes exactamente qué configuración usaste
- **Compartir configuraciones**: Envía el archivo a otros usuarios
- **Documentación**: Mantén registro de tus configuraciones favoritas
- **Aprendizaje**: Compara parámetros de diferentes imágenes

---

### 2. 💾 Sistema de Presets Personalizados

Ahora puedes **guardar, cargar y gestionar** tus configuraciones favoritas.

#### 🔧 Componentes del Sistema:

##### A. Guardar un Preset
1. Configura todos los parámetros como desees (fuente, caracteres, contraste, etc.)
2. Escribe un nombre en el campo "Nombre del preset"
3. Haz clic en "💾 Guardar"
4. ¡Listo! Tu configuración queda guardada

**Ejemplo de nombres de presets:**
- `foto_retrato_byn`
- `logo_empresa_alta_calidad`
- `poster_vintage`
- `arte_minimalista`

##### B. Cargar un Preset
1. Selecciona un preset del menú desplegable
2. Haz clic en "📂 Cargar Preset"
3. Todos los parámetros se aplicarán automáticamente

##### C. Eliminar un Preset
1. Selecciona el preset que quieres eliminar
2. Haz clic en "🗑️ Eliminar Preset"
3. Confirma la eliminación

##### D. Actualizar Lista
- Si has guardado presets desde otra sesión
- Haz clic en "🔄 Actualizar Lista"

#### 📁 Almacenamiento:
- Los presets se guardan en la carpeta `presets/` del proyecto
- Formato JSON legible y editable
- Portables: puedes copiar los archivos .json entre instalaciones

---

## 🎨 Flujo de Trabajo Recomendado

### Para Proyectos Repetitivos:
1. **Primera vez**: Experimenta con los parámetros hasta obtener el resultado deseado
2. **Guardar**: Guarda la configuración como preset (ej: "logo_cliente_ABC")
3. **Exportar parámetros**: Descarga el archivo .txt para tus registros
4. **Próximas veces**: Solo carga el preset y procesa la nueva imagen

### Para Exploración Creativa:
1. **Experimenta**: Prueba diferentes combinaciones
2. **Guarda lo que funciona**: Crea presets para cada estilo que te guste
3. **Documenta**: Los archivos .txt te ayudan a recordar qué funcionó

### Para Trabajo en Equipo:
1. **Estandariza**: Crea presets para cada tipo de proyecto
2. **Comparte**: Distribuye los archivos .json del folder `presets/`
3. **Referencia**: Usa los archivos .txt para documentación

---

## 🗂️ Estructura de Archivos

```
ascii_public_v2/
├── app.py
├── fonts/
│   ├── tulipana_gliph.ttf
│   └── Rushmore-Gliphs.ttf
├── presets/                        ← NUEVA CARPETA
│   ├── mi_preset_1.json
│   ├── mi_preset_2.json
│   └── ...
└── [otros archivos]
```

---

## 💡 Tips y Trucos

### Para Guardar Presets:
- ✅ Usa nombres descriptivos: `retrato_suave_escala5x`
- ✅ Incluye información clave en el nombre: `logo_rushmore_negro`
- ❌ Evita caracteres especiales en los nombres
- ✅ Puedes tener tantos presets como quieras

### Para Archivos de Parámetros:
- 📌 Guárdalos junto con tus imágenes finales
- 📌 Úsalos como referencia para proyectos similares
- 📌 Incluye el .txt cuando compartas tu trabajo
- 📌 Compara parámetros entre diferentes resultados

### Organización Sugerida:
```
Mis_Proyectos/
├── Proyecto_A/
│   ├── imagen_original.jpg
│   ├── ascii_resultado.png
│   └── parametros_ascii_art_20251027_153045.txt
├── Proyecto_B/
│   ├── logo.png
│   ├── ascii_logo.svg
│   └── parametros_ascii_art_20251027_154512.txt
└── Presets_Compartidos/
    ├── preset_logos.json
    ├── preset_fotos.json
    └── preset_posters.json
```

---

## 🔄 Migración y Backup

### Respaldar tus Presets:
```powershell
# Copiar toda la carpeta de presets
Copy-Item -Path "presets" -Destination "C:\Backup\mis_presets_ascii" -Recurse
```

### Restaurar Presets:
```powershell
# Copiar presets de backup
Copy-Item -Path "C:\Backup\mis_presets_ascii\*" -Destination "presets\" -Force
```

### Compartir un Preset Específico:
1. Localiza el archivo en `presets/nombre_preset.json`
2. Envíalo a otro usuario
3. El receptor lo coloca en su carpeta `presets/`
4. Haz clic en "🔄 Actualizar Lista"

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Workflow de Fotografía
```
1. Carga una foto de retrato
2. Ajusta: fuente=Tulipana, contraste=2.0, escala=5x
3. Guarda preset como "retrato_alta_calidad"
4. Descarga la imagen PNG y el archivo de parámetros
5. Para la próxima foto: carga el preset y procesa
```

### Ejemplo 2: Serie de Logos
```
1. Configura: fuente=Rushmore, modo_aleatorio=Sí, umbral=100
2. Guarda preset como "logos_rushmore_random"
3. Procesa cada logo con el mismo preset
4. Mantén consistencia en toda la serie
```

### Ejemplo 3: Comparación de Estilos
```
1. Crea preset "estilo_minimalista" (pocos caracteres, alto contraste)
2. Crea preset "estilo_detallado" (muchos caracteres, capas)
3. Crea preset "estilo_vintage" (colores invertidos, fuente específica)
4. Carga la misma imagen y prueba los 3 presets
5. Compara los resultados
```

---

## ❓ Preguntas Frecuentes

**P: ¿Cuántos presets puedo guardar?**  
R: Ilimitados. Solo están limitados por el espacio en disco.

**P: ¿Los presets incluyen la imagen original?**  
R: No, solo los parámetros de configuración. Debes cargar tu propia imagen.

**P: ¿Puedo editar los archivos .json manualmente?**  
R: Sí, pero ten cuidado con la sintaxis JSON. Es mejor usar la interfaz.

**P: ¿El archivo de parámetros .txt se genera siempre?**  
R: Sí, excepto para el "Preview (Texto)" que es solo visualización.

**P: ¿Puedo usar presets entre diferentes versiones de la app?**  
R: Sí, siempre que los parámetros sean compatibles.

**P: ¿Dónde se guardan los archivos .txt de parámetros?**  
R: En la carpeta temporal del sistema. Descárgalos inmediatamente para conservarlos.

---

## 🚀 Próximos Pasos

1. **Experimenta** con diferentes configuraciones
2. **Guarda** tus favoritas como presets
3. **Documenta** descargando los archivos de parámetros
4. **Comparte** tus presets con otros usuarios
5. **Optimiza** tu flujo de trabajo

---

**¡Disfruta de tus nuevas herramientas de productividad!** 🎨✨

*Última actualización: 27 de octubre de 2025*