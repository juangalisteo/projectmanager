# AGENT.md — Reglas propias de Claude · [PROYECTO]

Las reglas comunes están en `AGENTS.md` (raíz) y no se repiten aquí.

## Carga

- `CLAUDE.md` (raíz) importa `AGENTS.md` y este archivo. Claude Code los carga solo al abrir la carpeta.
- En la app de escritorio, el prompt A de `00_INICIO_CHAT.md` dice qué leer al empezar.

## Archivos propios

- **Bitácora:** `AGENT_AI/CLAUDE/BITACORA.md`. Entrada al final, con este formato:
  `## AAAA-MM-DD HH:MM — título`, y debajo: tarea, archivos modificados, resultado, decisiones y pendientes.
- **Puente:** `AGENT_AI/CLAUDE/PUENTE.md`, para el propietario u otro asistente.
- **Informes:** `AGENT_AI/CLAUDE/REPORTS/AAAAMMDD_TEMA.md`.

## Documentos vivos

- Cada línea de trabajo tiene un único documento vivo en `AGENT_AI/TRABAJO/`; el prompt lo nombra. Se edita en su sitio; no se crea otro para lo mismo.
- La salida en bruto de los comandos no se guarda en archivos aparte: solo los resultados relevantes, dentro del documento vivo.
- Las copias grandes o los archivos temporales que se creen durante una tarea se borran al terminarla.
