# 04_STYLE_MANUAL · Manual de estilo, maquetación e imágenes

Las normas de redacción, diseño y composición con las que se producen los documentos de este proyecto (bloques 01 a 10), más el estilo de imágenes e infografías (bloques 11 a 16): paleta, letras, grosores, piezas, composición, formatos y cómo generar imágenes con IA.

## Qué hay aquí

| Archivo | Para qué sirve |
| --- | --- |
| `00_MANUAL_DE_ESTILO.pdf` | El manual para leer o adjuntar a la IA |
| `01_MANUAL_DE_ESTILO.md` | Su editable: el PDF se genera desde aquí |
| `02_PROMPTS/01_APLICAR_MANUAL.md` | Prompt para producir un documento con el manual |
| `02_PROMPTS/02_REVISION_ENTREGA.md` | Prompt para revisar un PDF ya hecho, en un chat nuevo |
| `02_PROMPTS/03_CREAR_IMAGEN_SVG.md` | Prompt para dibujar una imagen con el estilo, en SVG (camino exacto) |
| `02_PROMPTS/04_GENERADOR_IMAGENES.md` | Prompt maestro para un generador de imágenes (ChatGPT, Gemini, Midjourney…) |
| `02_PROMPTS/05_REVISION_IMAGEN.md` | Prompt para revisar una imagen ya hecha, en un chat nuevo |
| `03_SOURCE/01_PALETTE.py` | Calcula la paleta completa a partir de un color |
| `03_SOURCE/02_BUILD_MANUAL.py` | Generador del PDF del manual |
| `03_SOURCE/03_FONTS/` | Fuentes Inter (licencia OFL) y FreeSerif Bold (GNU FreeFont, licencia GPL con excepción de fuentes) |
| `03_SOURCE/04_IMAGES/` | Imágenes del manual: fotografías, lámina modelo, composición de ejemplo y recortes |
| `03_SOURCE/05_IMAGE_KIT/` | Kit de imágenes en SVG: piezas base, lienzos de los seis formatos y composición de ejemplo |

La ficha del proyecto, las reglas de escritura y las normas de nombres están en `00_CONFIG/`, en la raíz del proyecto.

## Producir un documento

Con la app de escritorio y acceso a la carpeta, basta con decírselo a Claude en el chat del proyecto:

```text
Vamos a producir el documento. Aplica 04_STYLE_MANUAL\02_PROMPTS\01_APLICAR_MANUAL.md
con el manual de 04_STYLE_MANUAL y el color de la ficha. El material está en 01_MATERIALS.
```

Sin acceso a la carpeta: adjunta el PDF del manual, `00_CONFIG/00_PROJECT_CONFIG.json`, `00_CONFIG/01_WRITING_RULES.md` y el material, y pega el contenido de `02_PROMPTS/01_APLICAR_MANUAL.md`.

## Crear una imagen

Para una lámina, una infografía o cualquier imagen con texto o datos (camino exacto, recomendado):

```text
Vamos a crear una imagen. Aplica 04_STYLE_MANUAL\02_PROMPTS\03_CREAR_IMAGEN_SVG.md
con el estilo de los bloques 11 a 16 del manual. El material está en 01_MATERIALS.
```

Para un motivo muy detallado o una ilustración sin texto, copia `02_PROMPTS/04_GENERADOR_IMAGENES.md` en tu generador de imágenes, rellena los huecos y adjunta `03_SOURCE/04_IMAGES/03_STYLE_EXAMPLE.png` como referencia. Los textos se ponen después, en Inter.

Antes de dar una imagen por buena, revísala en un chat nuevo con `02_PROMPTS/05_REVISION_IMAGEN.md`.

## El kit de imágenes

| Archivo | Qué es |
| --- | --- |
| `05_IMAGE_KIT/01_BASE_PIECES_VECTOR.svg` | Todas las piezas del bloque 12, con sus medidas, listas para copiar |
| `05_IMAGE_KIT/02_BASE_SHEET_NORMAL_VECTOR.svg` … `07_BASE_SHEET_16X9_VECTOR.svg` | Lienzo de cada formato con marco, volutas y guías, vacío |
| `05_IMAGE_KIT/08_STYLE_EXAMPLE_VECTOR.svg` | Composición completa de ejemplo hecha solo con las piezas |

Los SVG del kit llevan el texto editable: para verlos bien hay que tener instaladas Inter y FreeSerif Bold (están en `03_SOURCE/03_FONTS/`).

## Paleta y PDF

Desde esta carpeta, con Python 3:

```text
python 03_SOURCE/01_PALETTE.py "#2E7D6B"
python 03_SOURCE/01_PALETTE.py "#2E7D6B" --write ../00_CONFIG/00_PROJECT_CONFIG.json
python 03_SOURCE/02_BUILD_MANUAL.py        (necesita: pip install reportlab)
```

Project Manager ya calcula la paleta al crear el proyecto y la guarda en la ficha; el script sirve si cambias de color más adelante.
