# 🎨 Guía de Nuevas Funcionalidades - ASCII Art Converter PRO

## ✨ Actualizaciones Recientes

### 1. Colores Por Defecto Invertidos

**Antes:** Blanco sobre negro (difícil de imprimir)  
**Ahora:** Negro sobre blanco (ideal para impresión y documentos)

- ✅ **Por defecto**: Caracteres NEGROS sobre fondo BLANCO
- ✅ **Con "Invertir colores" activo**: Caracteres BLANCOS sobre fondo NEGRO

### 2. Selector de Color Personalizado 🎨

Ahora puedes elegir cualquier color para tus caracteres:

**Ejemplos de colores:**
- `#000000` - Negro (por defecto)
- `#FF0000` - Rojo
- `#00FF00` - Verde
- `#0000FF` - Azul
- `#FF00FF` - Magenta
- `#00FFFF` - Cyan
- `#FFD700` - Dorado

**Casos de uso:**
- Logo empresarial con colores de marca
- Arte decorativo con colores vibrantes
- Diseño temático (ej: verde para naturaleza)

### 3. Fondo Transparente 🔲

Genera PNG con canal alpha (transparencia) para:

**Casos de uso:**
- Superponer sobre otras imágenes
- Logotipos con fondo transparente
- Composiciones en diseño gráfico
- Memes y overlays

**Importante:** 
- Solo disponible en modo PNG
- No aplica a SVG ni TXT
- El PNG generado será RGBA (4 canales) en lugar de RGB (3 canales)

## 🎯 Ejemplos de Configuración

### Ejemplo 1: Logo Negro Clásico
```
Color: #000000 (negro)
Fondo transparente: ✅ Activado
Invertir colores: ❌ Desactivado
Resultado: Logo negro sobre transparente
```

### Ejemplo 2: Arte Rojo Vibrante
```
Color: #FF0000 (rojo)
Fondo transparente: ❌ Desactivado
Invertir colores: ❌ Desactivado
Resultado: Caracteres rojos sobre fondo blanco
```

### Ejemplo 3: Estilo Neón (Blanco sobre Negro)
```
Color: #FFFFFF (blanco)
Fondo transparente: ❌ Desactivado
Invertir colores: ✅ Activado
Resultado: Caracteres blancos sobre fondo negro
```

### Ejemplo 4: Logo Corporativo Transparente
```
Color: #1E90FF (azul corporativo)
Fondo transparente: ✅ Activado
Invertir colores: ❌ Desactivado
Preset: IcoMoon
Resultado: Glifos personalizados azules sobre transparente
```

## 💡 Tips y Recomendaciones

### Para Impresión
- Usa color negro (`#000000`)
- Desactiva fondo transparente
- Escala de resolución: 5-10x
- Formato: PNG o SVG

### Para Web/Redes Sociales
- Fondo transparente para superposición
- Colores vibrantes para destacar
- Escala de resolución: 2-3x
- Formato: PNG

### Para Logos
- Fondo transparente siempre
- Color corporativo personalizado
- Preset: IcoMoon para glifos únicos
- Formato: SVG para escalabilidad

### Para Arte/Posters
- Colores personalizados según tema
- Fondo blanco o transparente
- Alta resolución (5-10x)
- Sistema de capas para más detalle

## 🔧 Controles en la Interfaz

### Ubicación de los nuevos controles:

1. **🎨 Color de caracteres** - Debajo de "Invertir colores"
   - Click para abrir selector de color
   - Escribe valor hex directo (ej: #FF0000)

2. **🔲 Fondo transparente** - Al lado del selector de color
   - Checkbox simple on/off
   - Solo afecta PNG

3. **🔄 Invertir colores** - Existente, ahora con nuevo comportamiento
   - Intercambia fondo blanco ↔ negro
   - Ajusta color de caracteres automáticamente si no es personalizado

## ⚙️ Compatibilidad

- **PNG**: ✅ Todas las funcionalidades
- **SVG**: ⚠️ Color personalizado aplicado al embed base64
- **TXT**: ❌ No aplica color ni transparencia (solo texto)

## 🚀 Prueba Rápida

Para probar las nuevas funcionalidades:

```bash
python app.py
```

1. Sube una imagen
2. Selecciona preset "IcoMoon"
3. Cambia el color a `#FF0000` (rojo)
4. Activa "Fondo transparente"
5. Genera y descarga

¡Verás tus glifos personalizados en rojo sobre fondo transparente!

---

**Fecha de actualización:** Octubre 2025  
**Versión:** 2.0 - Color + Transparencia
