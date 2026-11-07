# AGENTS.md — Reglas para agentes de IA · [PROYECTO]

Valen para cualquier agente: Claude (app o Claude Code)[[SI CODEX]], Codex (ChatGPT)[[FIN]] u otros. Aquí solo hay reglas permanentes. El estado del trabajo no va aquí: ver §8.

Cada agente tiene además sus reglas propias, que no repiten estas:

- Claude: `AGENT_AI/CLAUDE/AGENT.md` (lo carga `CLAUDE.md`).
[[SI CODEX]]
- Codex: lee `AGENT_AI/CODEX/AGENT.md` al empezar.
[[FIN]]

## 1. Idioma y trato

- Todos los agentes responden en **español**, con palabras sencillas: en el chat, los informes, la bitácora y los resúmenes.
- Cuando haya que decidir algo, el agente da su recomendación y explica por qué en una o dos frases.
- Si un archivo cambia, se entrega completo (guardado en la carpeta o para descargar), nunca en trozos para pegar.
- El código (funciones, clases, variables, comentarios) va en inglés, según el estándar del lenguaje. Todo lo que ve el usuario del programa va en español.

## 2. Protección del trabajo

- Sin autorización expresa en la tarea, no se modifican código, arquitectura, configuración, pruebas ni dependencias, y no se hace commit, push, pull, merge, reset ni tags.
- Si una tarea autoriza cambios, se mantienen dentro de lo pedido y se lista cada archivo modificado.
- Antes de borrar o sustituir algo, se dice qué es y se espera la confirmación del propietario.

## 3. Nombres de carpetas y archivos

Las normas completas están en `00_CONFIG/02_NAMING.md`. En este proyecto:

- **El código y sus carpetas** siguen el estándar de su lenguaje y de sus herramientas, normalmente en minúsculas y sin número: `src/`, `docs/`, `tests/`, `main.py`, `index.html`.
- **Lo que no es código** (documentos, imágenes de trabajo, recursos de diseño) sigue las normas: MAYÚSCULAS, `_`, número de dos dígitos al principio y extensión en minúsculas.
- Sin número, por ser estándar: `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE` y `.gitignore`.
- No se cambian los nombres del sistema de trabajo con IA: `00_INICIO_CHAT.md` y todo lo que hay en `AGENT_AI/`.

## 4. Escritura

Todo texto que se entregue (README, CHANGELOG, mensajes de la interfaz, informes, resúmenes) aplica `00_CONFIG/01_WRITING_RULES.md`: al redactar y en una segunda lectura antes de entregar. Los datos y enlaces se comprueban; lo que no se ha podido comprobar se dice.

## 5. Comprobación

- Cambio acotado: pruebas del ámbito tocado y comprobación de que el código compila. Si se tocó un JSON, se valida.
- Suite completa de pruebas solo al cerrar una fase, si el cambio afecta a mucho código o si el propietario la pide. Una sola vez, guardando el resultado.
- Nada se da por terminado sin haberlo probado. Lo que el agente no puede probar (por ejemplo, una ventana en Windows) se dice y lo prueba el propietario.

## 6. Publicación

- La licencia es **GPL-3.0** y está en `LICENSE`. No se cambia ni se sustituye por otra, y el archivo no se edita: es el texto oficial.
- El repositorio empieza privado. Se hace público solo cuando el propietario lo decide.
- Cada versión publicada tiene su entrada en `CHANGELOG.md` y su etiqueta (`v1.0.0`…), según Semantic Versioning.

## 7. Documentación de cierre

- **Estado** (`AGENT_AI/ESTADO.md`): se actualiza al cerrar cada tarea con cambios. Qué se hizo, qué está pendiente y cuál es el siguiente paso.
- **Bitácora** (`AGENT_AI/<AGENTE>/BITACORA.md`): una entrada de 15 líneas como máximo, solo si la tarea produjo cambios, hallazgos o decisiones. Solo se añade al final; nunca se borra ni se reescribe.
- **Puente** (`AGENT_AI/<AGENTE>/PUENTE.md`): solo cuando el propietario lo pida o al cerrar un lote. Se regenera desde cero con el resultado completo, para pasarlo a otro asistente.
- **Informes**: un resultado largo va a `AGENT_AI/<AGENTE>/REPORTS/AAAAMMDD_TEMA.md`.
- Las preguntas sencillas no necesitan cierre. Si el prompt del propietario dice otra cosa, manda el propietario.

## 8. Privacidad y dónde está cada cosa

- `AGENT_AI/`, `00_CONFIG/` y `00_INICIO_CHAT.md` son privados: nunca se suben a Git (están en `.gitignore`). Si detectas uno de ellos en Git, avisa sin tocar Git.
- Lo que ya no sirve se borra, con la lista aprobada antes por el propietario. No se dejan archivos sueltos que nadie sepa qué son.

```text
AGENT_AI/
  LEEME.md             mapa de AGENT_AI: qué es cada archivo
  ESTADO.md            estado actual y siguiente paso (léelo al empezar)
  TRABAJO/
    PLAN.md            cómo trabajamos, decisiones, fases
    IDEAS_FUTURAS.md   mejoras aparcadas, para no mezclarlas con lo actual
  CLAUDE/              AGENT.md, BITACORA.md, PUENTE.md, REPORTS/
[[SI CODEX]]
  CODEX/               AGENT.md, BITACORA.md, PUENTE.md, REPORTS/
[[FIN]]
```

- Ficha del proyecto: `00_CONFIG/00_PROJECT_CONFIG.json`.
- Cómo redactar prompts para el ejecutor: `00_CONFIG/03_PROMPTS_GUIDE.md`.
- Historia: la bitácora de cada agente. Se busca lo concreto; no se lee entera.

## 9. Decisiones intencionadas del proyecto

Cosas que parecen mejorables pero son así a propósito. No se cambian ni se proponen como mejora sin preguntar antes al propietario. Se apuntan aquí a medida que aparezcan, con su motivo.

- La licencia es GPL-3.0 (`LICENSE`), siempre, en todos los proyectos del propietario.
