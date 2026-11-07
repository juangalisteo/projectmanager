# AGENT.md — Reglas propias de Codex · [PROYECTO]

Las reglas comunes están en `AGENTS.md` (raíz) y no se repiten aquí.

## Carga

- Codex carga `AGENTS.md` automáticamente, pero no tiene imports: lee este archivo al empezar cada sesión.

## Papel

- Hace de ejecutor, como Claude Code: un paso por chat, según el prompt del asesor.
- No escribe en `AGENT_AI/CLAUDE/`: es la carpeta de Claude.

## Archivos propios

- **Bitácora:** `AGENT_AI/CODEX/BITACORA.md`. Entrada al final con el formato `## AAAA-MM-DD HH:MM — título` y debajo: tarea, archivos modificados, resultado, decisiones y pendientes. Si crece mucho, se busca lo concreto; no se lee entera.
- **Puente:** `AGENT_AI/CODEX/PUENTE.md`, el documento con el que el propietario pasa el resultado de Codex al asesor. Cuando toca generarlo, se borra lo anterior y se escribe desde cero con el resultado completo, de modo que el otro asistente pueda trabajar sin el chat.
- **Informes:** `AGENT_AI/CODEX/REPORTS/AAAAMMDD_TEMA.md`.
