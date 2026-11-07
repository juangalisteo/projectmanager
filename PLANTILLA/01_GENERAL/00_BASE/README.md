# [PROYECTO]

| Dato | Valor |
| --- | --- |
| Tipo | [TIPO] |
| Carpeta | `[RUTA]` |
| Color principal | `[COLOR]` |
| Creado | [FECHA], con Project Manager |
| Autor | [AUTOR] |

> **Si mueves o renombras esta carpeta**, cambia la ruta en la tabla de arriba y en `00_INICIO_CHAT.md`. Claude usa esa ruta para pedir acceso.

## Para empezar

1. Abre `00_INICIO_CHAT.md`.
2. Copia el prompt y pégalo como primer mensaje en un chat nuevo de Claude.
3. Claude pide acceso a esta carpeta, lee las reglas y el estado, y te pregunta qué hacemos.

## Qué hay en la carpeta

```
[CARPETA]/
├── README.md            este archivo
├── 00_INICIO_CHAT.md    prompt para empezar un chat
├── AGENTS.md            reglas para la IA
├── 00_CONFIG/
│   ├── 01_WRITING_RULES.md   reglas de escritura (sin marcas de texto de IA)
│   └── 02_NAMING.md          normas de nombres de carpetas y archivos
├── AGENT_AI/
[[NO CODEX]]
│   └── ESTADO.md        dónde estamos, qué falta e ideas para más adelante
[[FIN]]
[[SI CODEX]]
│   ├── ESTADO.md        dónde estamos, qué falta e ideas para más adelante
│   ├── CLAUDE/          bitácora de Claude
│   └── CODEX/           reglas y bitácora de Codex (ChatGPT)
[[FIN]]
└── 01_WORK/             aquí se trabaja
```

## Cómo se trabaja

- **La memoria del proyecto está en archivos, no en el chat.** `AGENT_AI/ESTADO.md` dice dónde se quedó el trabajo y qué sigue. Un chat nuevo lo lee y continúa.
- **Todo el trabajo va en `01_WORK`.** Si el proyecto crece, se ordena por dentro con carpetas numeradas (`01_NOMBRE`, `02_NOMBRE`…).
- **Un chat, una tarea.** Al terminar, la IA actualiza el estado y te dice qué ha cambiado y qué no ha podido comprobar.
