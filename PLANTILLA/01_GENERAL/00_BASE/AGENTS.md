# AGENTS.md — Reglas para la IA · [PROYECTO]

Valen para cualquier agente que trabaje en este proyecto: Claude[[SI CODEX]], Codex (ChatGPT)[[FIN]] u otros. Aquí solo hay reglas permanentes; el estado del trabajo está en `AGENT_AI/ESTADO.md`.
[[SI CODEX]]

Codex tiene además sus reglas propias en `AGENT_AI/CODEX/AGENT.md`, que no repiten estas.
[[FIN]]

## 1. Idioma y trato

- Respuestas siempre en **español**, con palabras sencillas: en el chat y en los archivos.
- Cuando haya que decidir algo, el agente da su recomendación y explica por qué en una o dos frases.
- Si un archivo cambia, se entrega completo (guardado en la carpeta o para descargar), nunca en trozos para pegar.

## 2. Carpetas

- `01_WORK/` es donde se trabaja. Si crece, se ordena por dentro con carpetas numeradas.
- Antes de borrar o sustituir algo, se dice qué es y se espera la confirmación del propietario.
- Solo se crea un archivo nuevo cuando la tarea lo pide. No se dejan archivos sueltos que nadie sepa qué son.

## 3. Nombres de carpetas y archivos

Las normas completas, con ejemplos, están en `00_CONFIG/02_NAMING.md`. Se siguen siempre que se crea o se renombra una carpeta o un archivo. Lo esencial:


- **MAYÚSCULAS**, con la extensión en minúsculas: `01_GUION.md`, `02_PORTADA.png`.
- Palabras separadas con `_`. Sin espacios, tildes ni signos; la Ñ se escribe N.
- Un número de dos dígitos al principio: `01_`, `02_`… El `00` es la base del nivel y el `99` el archivo de cosas antiguas (`99_ARCHIVE`). Lo que llega de fuera se renombra al guardarlo.
- Las categorías van en inglés (`WORK`, `EXPORT`, `DESIGN`…); los títulos, en su idioma.
- Versiones: mismo número y `_V01`, `_V02` al final. Fechas: `AAAAMMDD`.
- Sin número, por ser estándar: `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE` y `.gitignore`.
- Tampoco se cambian los nombres del sistema de trabajo con IA: `00_INICIO_CHAT.md` y todo lo que hay en `AGENT_AI/`.

## 4. Escritura y comprobación

- Todo texto que se entregue (documentos, guiones, resúmenes, correos, READMEs) aplica `00_CONFIG/01_WRITING_RULES.md`: al redactar y en una segunda lectura completa antes de entregar. Son las reglas para escribir con voz natural y sin las marcas típicas de los textos generados con IA.
- Los datos, citas y enlaces se comprueban; lo que no se ha podido comprobar se dice.
- Todo se revisa en su soporte final (el PDF, el vídeo, la web…) antes de darlo por terminado.

## 5. Al cerrar una tarea

- `AGENT_AI/ESTADO.md` se actualiza al cerrar cada tarea con cambios: qué se hizo, qué está pendiente y cuál es el siguiente paso. Las ideas que no tocan ahora van a su apartado «Ideas para más adelante».
[[SI CODEX]]
- Cada agente apunta lo que hizo en su bitácora (`AGENT_AI/CLAUDE/BITACORA.md` o `AGENT_AI/CODEX/BITACORA.md`): una entrada corta al final, nunca se borra ni se reescribe. Así los dos agentes no pisan el mismo archivo.
[[FIN]]
- Las preguntas sencillas no necesitan cierre.
