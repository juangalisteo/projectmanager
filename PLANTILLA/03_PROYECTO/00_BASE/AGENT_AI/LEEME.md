# LEEME — Mapa de `AGENT_AI/` · [PROYECTO]

> Qué es cada archivo y qué pasa con él cuando su tarea termina. Lo mantiene el asesor. Actualizado: [FECHA].
> **No muevas ni cambies de nombre estos archivos a mano:** los agentes los buscan por su ruta exacta.

## La norma

1. Mientras un documento se usa, está en su sitio (`TRABAJO/` o la carpeta del agente).
2. Cuando su tarea termina, se archiva en `TRABAJO/99_ARCHIVE/` o, si ya no sirve, se borra.
3. Antes de borrar nada, el agente da la lista al propietario y espera su aprobación.

## Cómo empezar cada chat

| Chat | Qué haces |
| --- | --- |
| **Asesor** (app de escritorio de Claude, con acceso a la carpeta) | Copia **entero** `00_INICIO_CHAT.md` (en la raíz) y pégalo como primer mensaje, o adjúntalo tal cual. También lo copia el botón «Prompt · IA» de Project Manager. Es la forma recomendada. |
| **Ejecutor** (Claude Code, abierto en esta carpeta) | No necesita prompt de arranque: carga `CLAUDE.md` solo, que trae `AGENTS.md` y sus reglas. Le pegas el prompt que te prepara el asesor. |
[[SI CODEX]]
| **Codex** (ChatGPT, abierto en esta carpeta) | Igual que el ejecutor: lee `AGENTS.md` solo, y ahí se le dice que lea `AGENT_AI/CODEX/AGENT.md`. Le pegas el prompt del asesor. |
[[FIN]]
| **Asesor sin acceso a la carpeta** (Claude en el navegador o en el móvil) | Adjunta `AGENTS.md`, `00_CONFIG/01_WRITING_RULES.md`, `00_CONFIG/00_PROJECT_CONFIG.json`, `AGENT_AI/TRABAJO/PLAN.md` y `AGENT_AI/ESTADO.md`, y pega el mensaje de abajo. |

Mensaje para el asesor sin acceso a la carpeta:

```text
Hola. Eres el asesor del proyecto [PROYECTO]. Te adjunto las reglas, las
reglas de escritura, la ficha, el plan y el estado. Léelos enteros y
aplica las reglas de escritura en todo lo que me entregues. Si en la ficha
faltan datos, pregúntamelos juntos con tu recomendación; si no, dime en
tres líneas dónde estamos y cuál es el siguiente paso. Como no puedes
escribir en mi carpeta, cuando cambies un archivo dámelo completo para
descargarlo, y al final de cada tarea dame también el ESTADO.md
actualizado. Antes de cambiar nada, explícame qué vas a cambiar y espera
a que te diga que sí. Respóndeme en español y con palabras sencillas, y
dame siempre tu recomendación.
```

**Si mueves o renombras la carpeta:** cambia la ruta de `00_INICIO_CHAT.md` y el campo `proyecto.ruta` de `00_CONFIG/00_PROJECT_CONFIG.json`.

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
