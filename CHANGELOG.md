# Changelog · Project Manager

Cambios importantes, de la versión más nueva a la más antigua. Versiones según [Semantic Versioning](https://semver.org/lang/es/).

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
