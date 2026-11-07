# Changelog · Project Manager

Cambios importantes, de la versión más nueva a la más antigua. Versiones según [Semantic Versioning](https://semver.org/lang/es/).

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
