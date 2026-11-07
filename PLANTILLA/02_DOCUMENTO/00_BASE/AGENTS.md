# AGENTS.md — Reglas para la IA · [PROYECTO]

Valen para cualquier agente que trabaje en este documento: Claude[[SI CODEX]], Codex (ChatGPT)[[FIN]] u otros. Aquí solo hay reglas permanentes; el estado del trabajo está en `AGENT_AI/ESTADO.md` y las decisiones, en `AGENT_AI/TRABAJO/PLAN.md`.
[[SI CODEX]]

Codex tiene además sus reglas propias en `AGENT_AI/CODEX/AGENT.md`, que no repiten estas.
[[FIN]]

## 1. Idioma y trato

- Respuestas siempre en **español**, con palabras sencillas: en el chat y en los archivos.
- Cuando haya que decidir algo, el agente da su recomendación y explica por qué en una o dos frases.
- Si un archivo cambia, se entrega completo (guardado en la carpeta o para descargar), nunca en trozos para pegar.

## 2. Carpetas

- `01_MATERIALS/` guarda los originales del propietario: se leen, no se modifican, no se mueven y no se borran.
- `02_WORK/` es donde se trabaja: borradores, versiones y material en curso.
- `03_EXPORT/` recibe solo lo terminado y revisado.
- `04_STYLE_MANUAL/` es el manual de estilo; no se modifica salvo que el propietario lo pida.
- Antes de borrar o sustituir algo, se dice qué es y se espera la confirmación del propietario.
- Solo se crea un archivo nuevo cuando la tarea lo pide. No se dejan archivos sueltos que nadie sepa qué son.

## 3. Nombres de carpetas y archivos

Las normas completas, con ejemplos, están en `00_CONFIG/02_NAMING.md`. Se siguen siempre que se crea o se renombra una carpeta o un archivo. Lo esencial:

- **MAYÚSCULAS**, con la extensión en minúsculas: `01_CAPITULO_INTRO.md`, `02_PORTADA.png`.
- Palabras separadas con `_`. Sin espacios, tildes ni signos; la Ñ se escribe N.
- Un número de dos dígitos al principio: `01_`, `02_`… El `00` es la base del nivel y el `99` el archivo de cosas antiguas (`99_ARCHIVE`). Lo que llega de fuera se renombra al guardarlo.
- Las categorías van en inglés (`WORK`, `EXPORT`, `DESIGN`…); los títulos, en su idioma.
- Versiones: mismo número y `_V01`, `_V02` al final. Fechas: `AAAAMMDD`.
- Sin número, por ser estándar: `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE` y `.gitignore`.
- Tampoco se cambian los nombres del sistema de trabajo con IA: `00_INICIO_CHAT.md` y todo lo que hay en `AGENT_AI/`.

## 4. Escritura y composición

- Todo texto que se entregue aplica `00_CONFIG/01_WRITING_RULES.md`: al redactar y en una segunda lectura completa antes de entregar. Son las reglas para escribir con voz natural y sin las marcas típicas de los textos generados con IA.
- Los datos, citas y enlaces se comprueban en fuentes adecuadas al tema; lo que no se ha podido comprobar se dice.
- El documento maquetado sigue `04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf` con el color de la ficha (`00_CONFIG/00_PROJECT_CONFIG.json`). El modo de aplicarlo está en `04_STYLE_MANUAL/02_PROMPTS/01_APLICAR_MANUAL.md`.

## 5. Comprobación

- El PDF exportado se revisa página por página antes de darlo por terminado.
- Se corrige y se vuelve a comprobar hasta que no queden defectos visibles.
- Para una revisión independiente, se usa `04_STYLE_MANUAL/02_PROMPTS/02_REVISION_ENTREGA.md` en un chat nuevo.

## 6. Al cerrar una tarea

- `AGENT_AI/ESTADO.md` se actualiza al cerrar cada tarea con cambios: qué se hizo, qué está pendiente y cuál es el siguiente paso.
- Si hay una decisión nueva o cambia una fase, se apunta en `AGENT_AI/TRABAJO/PLAN.md`.
- Cada agente apunta lo que hizo en su bitácora (`AGENT_AI/CLAUDE/BITACORA.md`[[SI CODEX]] o `AGENT_AI/CODEX/BITACORA.md`[[FIN]]): una entrada corta al final, solo si hubo cambios o decisiones. Nunca se borra ni se reescribe.
- Las preguntas sencillas no necesitan cierre.
