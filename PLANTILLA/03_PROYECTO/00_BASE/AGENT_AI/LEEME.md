# LEEME — Mapa de `AGENT_AI/` · [PROYECTO]

> Qué es cada archivo y qué pasa con él cuando su tarea termina. Lo mantiene el asesor. Actualizado: [FECHA].
> **No muevas ni cambies de nombre estos archivos a mano:** los agentes los buscan por su ruta exacta.

## La norma

1. Mientras un documento se usa, está en su sitio (`TRABAJO/` o la carpeta del agente).
2. Cuando su tarea termina, se archiva en `TRABAJO/99_ARCHIVE/` o, si ya no sirve, se borra.
3. Antes de borrar nada, el agente da la lista al propietario y espera su aprobación.

## Lo que abres tú

| Archivo | Qué es | Se archiva cuando… |
| --- | --- | --- |
| `TRABAJO/PLAN.md` | El archivo principal: cómo trabajamos, decisiones, fases y preguntas pendientes | Termina el proyecto |
| `ESTADO.md` | Foto del momento: qué se acaba de hacer y qué sigue | Nunca: siempre está al día |
| `TRABAJO/IDEAS_FUTURAS.md` | Mejoras aparcadas para más adelante | Se hacen o se descartan |

## Lo que usan los agentes

| Archivo | Qué es |
| --- | --- |
| `CLAUDE/AGENT.md` | Reglas propias de Claude |
| `CLAUDE/BITACORA.md` | Historia de lo que ha hecho Claude |
| `CLAUDE/PUENTE.md` | Resultado completo de la última tarea, para pasarlo a otro chat |
| `CLAUDE/REPORTS/` | Informes largos de Claude |
[[SI CODEX]]
| `CODEX/…` | Lo mismo para Codex |
[[FIN]]

## Terminado o archivado

Todavía nada.
