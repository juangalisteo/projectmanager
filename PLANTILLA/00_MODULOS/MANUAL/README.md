# 04_STYLE_MANUAL · Manual de estilo y maquetación

Las normas de redacción, diseño y composición con las que se producen los documentos de este proyecto: Inter fija, el color principal de la ficha y una identidad común.

## Qué hay aquí

| Archivo | Para qué sirve |
| --- | --- |
| `00_MANUAL_DE_ESTILO.pdf` | El manual para leer o adjuntar a la IA |
| `01_MANUAL_DE_ESTILO.md` | Su editable: el PDF se genera desde aquí |
| `02_PROMPTS/01_APLICAR_MANUAL.md` | Prompt para producir un documento con el manual |
| `02_PROMPTS/02_REVISION_ENTREGA.md` | Prompt para revisar un PDF ya hecho, en un chat nuevo |
| `03_SOURCE/01_PALETTE.py` | Calcula la paleta completa a partir de un color |
| `03_SOURCE/02_BUILD_MANUAL.py` | Generador del PDF del manual |
| `03_SOURCE/03_FONTS/`, `03_SOURCE/04_IMAGES/` | Fuentes Inter (licencia OFL) e imágenes del manual |

La ficha del proyecto, las reglas de escritura y las normas de nombres están en `00_CONFIG/`, en la raíz del proyecto.

## Producir un documento

Con la app de escritorio y acceso a la carpeta, basta con decírselo a Claude en el chat del proyecto:

```text
Vamos a producir el documento. Aplica 04_STYLE_MANUAL\02_PROMPTS\01_APLICAR_MANUAL.md
con el manual de 04_STYLE_MANUAL y el color de la ficha. El material está en 01_MATERIALS.
```

Sin acceso a la carpeta: adjunta el PDF del manual, `00_CONFIG/00_PROJECT_CONFIG.json`, `00_CONFIG/01_WRITING_RULES.md` y el material, y pega el contenido de `02_PROMPTS/01_APLICAR_MANUAL.md`.

## Paleta y PDF

Desde esta carpeta, con Python 3:

```text
python 03_SOURCE/01_PALETTE.py "#2E7D6B"
python 03_SOURCE/01_PALETTE.py "#2E7D6B" --write ../00_CONFIG/00_PROJECT_CONFIG.json
python 03_SOURCE/02_BUILD_MANUAL.py        (necesita: pip install reportlab)
```

Project Manager ya calcula la paleta al crear el proyecto y la guarda en la ficha; el script sirve si cambias de color más adelante.
