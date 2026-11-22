# Changelog · Project Manager

Cambios importantes, de la versión más nueva a la más antigua. Versiones según [Semantic Versioning](https://semver.org/lang/es/).

## [1.3.0] · 2026-11-22

### Añadido

- **Manual «general + imágenes»** (`PLANTILLA/00_MODULOS/MANUAL_IMAGENES`): el manual general entero, sin cambios, más seis bloques sobre imágenes e infografías sacados de la lámina modelo: fundamentos (paleta y uso de cada color, letras con su escala y espaciado, siete grosores de línea, cortes y aire, plumilla y luz), catálogo de piezas con cotas (marco con volutas, cuatro tipos de círculo, rótulos, adornos, construcción, formas y piezas de infografía), composición sobre el eje y seis formatos (normal, 9:16, A4, 4:5, 1:1 y 16:9), infografías, método para crear un elemento nuevo y cómo generar imágenes con IA. PDF de 70 páginas, 52 figuras y 20 tablas.
- La página final de ese manual lleva la escuadra, el compás y la G dibujados con el estilo de imágenes, y la frase «Una idea simple / da forma a tu realidad.» (decisión del propietario). El manual general mantiene su libro y su frase.
- Prompts nuevos en ese manual: crear una imagen en SVG, prompt maestro para un generador de imágenes y revisión de una imagen. Kit de imágenes en SVG (piezas base, lienzos de los seis formatos y una composición de ejemplo) y la fuente FreeSerif Bold para las capitales.
- Botón **★** en «03 · Color principal», a la izquierda de «Color», con el aspecto del botón de ChatGPT. En rojo (por defecto), el Documento sale con el manual general; en verde, con el de «general + imágenes». Cada proyecto lleva un solo manual. La ficha lo apunta en `documento.manual_version`. Desde la consola: `--imagenes`.
- 19 pruebas automáticas: cuatro nuevas (manual general, manual con imágenes, la parte general idéntica en los dos manuales y color solo en Documento).

### Cambiado

- **«03 · Color principal» solo funciona con Documento.** Con Proyecto o General se queda en gris y no se puede pulsar, y el proyecto sale con la paleta predeterminada.
- El generador del manual (`02_BUILD_MANUAL.py`) es el mismo para las dos versiones: dibuja las figuras de imágenes y, si hay muchos bloques, sigue el índice en una segunda página. El PDF del manual general sale igual que antes.
- Textos más cortos en la sección 03: con Proyecto y General pone «Solo con Documento»; con Documento, «Pulsa ↻ para elegir un color aleatorio.» (el cuadro de color se sigue pudiendo pulsar). Al pulsar la ★, la línea de estado dice solo qué manual saldrá.
- En la plantilla de Documento, `AGENTS.md` y `README.md` nombran los prompts de imágenes solo si el proyecto lleva ese manual (bloques `[[SI IMAGENES]]`).

## [1.2.0] · 2026-11-10

### Añadido

- Botón **«Actualizar ruta»**, arriba a la derecha de «01 · Nombre del proyecto», del tamaño del botón de ChatGPT y con el aspecto de «Examinar». Si mueves o cambias de nombre la carpeta de un proyecto, eliges la carpeta en su sitio nuevo y Project Manager escribe la ruta nueva en `00_INICIO_CHAT.md`, en `README.md` y en la ficha (`proyecto.ruta` y `proyecto.carpeta`). Si la ruta ya estaba bien o la carpeta no es un proyecto de Project Manager, avisa y no toca nada.
- También desde la consola: `python APP\creador.py --actualizar-ruta "C:\nueva\ruta\MI_PROYECTO"`.
- 15 pruebas automáticas: dos nuevas para «Actualizar ruta» (los tres tipos, con un proyecto movido y renombrado, y los casos en que no debe tocar nada).

## [1.1.0] · 2026-11-09

### Cambiado

- `00_INICIO_CHAT.md` lleva ahora **solo el prompt de arranque**, sin títulos, recuadros ni explicaciones. Se copia o se adjunta entero en un chat nuevo y Claude sabe qué hacer: pide acceso a la carpeta, lee las reglas y el estado, dice en tres líneas dónde estamos y espera. Antes mezclaba una guía con cuatro prompts y el chat no sabía cuál seguir.
- El prompt dice también cómo trabajar con el propietario: explicar los cambios y esperar su sí, entregar archivos completos y marcar los archivos antiguos que haya que borrar.
- Se quitan los prompts de arranque de Codex y del ejecutor (Claude Code): los dos cargan sus reglas solos al abrir la carpeta (`AGENTS.md` y `CLAUDE.md`).
- El prompt para usar Claude sin acceso a la carpeta, con la lista de archivos que hay que adjuntar, pasa al `README.md` de General y Documento, y a `AGENT_AI/LEEME.md` en Proyecto (que no se sube a GitHub).
- El botón «Prompt · IA» copia `00_INICIO_CHAT.md` entero.
- 13 pruebas automáticas: una nueva comprueba que el prompt de arranque de los tres tipos es solo el mensaje, con la ruta y sin Codex.

## [1.0.0] · 2026-11-07

Primera versión publicada.

### Ventana

- Cinco pasos: nombre del proyecto, tipo, color principal, asistentes y carpeta de destino.
- Campo de nombre con el texto y el borde en el color de la aplicación y una × para borrarlo.
- Color principal con dos modos, «Color» y «Predeterminado». Selector propio, oscuro (cuadrado de saturación y brillo, barra de tono y código), botón ↻ que elige un color al azar que siempre da una paleta legible y muestra en vivo de la paleta (fondo, texto, acento, recuadros y bordes).
- Interruptor ChatGPT (verde = activado, rojo = desactivado) para añadir Codex. Claude va siempre.
- Botón «Prompt · IA» que copia el prompt de inicio, con la ruta del proyecto ya escrita.
- «Ver actividad»: registro de lo que hace el programa, con barra de desplazamiento fina e icono de copiar. Si hay un error, se abre solo.
- Icono nítido a todos los tamaños (de 16 a 256 px) en la barra de título y en la de tareas.

### Tipos de proyecto

- **General:** README, prompt de inicio, reglas para la IA, reglas de escritura, normas de nombres, estado y la carpeta `01_WORK`. Con ChatGPT, una bitácora por agente.
- **Documento:** lo de General más la ficha con la paleta, el plan, la bitácora de Claude, las carpetas `01_MATERIALS`, `02_WORK` y `03_EXPORT` y el manual de estilo con su generador de PDF.
- **Proyecto:** asesor (app de escritorio) y ejecutor (Claude Code) separados, con `.gitignore`, `CHANGELOG.md`, `CLAUDE.md`, guía de prompts, `docs/`, `tests/` y la licencia GPL-3.0 (`LICENSE`) ya creada.

### Plantilla y creador

- Plantilla genérica con etiquetas (`[PROYECTO]`, `[RUTA]`, `[COLOR]`…) y bloques condicionales (`[[SI …]]`, `[[NO …]]`).
- Paleta de 13 tonos calculada a partir de un solo color, con el contraste comprobado.
- Módulos compartidos: normas de nombres 1.1.0, reglas de escritura (guía de Wikipedia sobre los rasgos del texto escrito por IA) y Manual de estilo y maquetación 1.0.
- El proyecto se crea en una carpeta temporal y solo recibe su nombre al final. Si falta una parte de la plantilla, el mensaje dice cuál y no se crea nada.
- 12 pruebas automáticas (`tests/`).
