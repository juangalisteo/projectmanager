# [PROYECTO]

| Dato | Valor |
| --- | --- |
| Tipo | [TIPO] |
| Carpeta | `[RUTA]` |
| Color principal | `[COLOR]` |
| Creado | [FECHA], con Project Manager |
| Autor | [AUTOR] |

> **Si mueves o renombras esta carpeta**, cambia la ruta en tres sitios: la tabla de arriba, `00_INICIO_CHAT.md` y el campo `proyecto.ruta` de `00_CONFIG/00_PROJECT_CONFIG.json`. Claude usa esa ruta para pedir acceso.

## Para empezar

1. Abre `00_INICIO_CHAT.md`.
2. Copia el prompt y pégalo como primer mensaje en un chat nuevo de Claude.
3. Claude pide acceso a esta carpeta, lee las reglas, la ficha, el plan y el estado, y te pregunta los datos que falten.

## Qué hay en la carpeta

```
[CARPETA]/
├── README.md            este archivo
├── 00_INICIO_CHAT.md    prompts para empezar un chat
├── AGENTS.md            reglas para la IA
├── 00_CONFIG/
│   ├── 00_PROJECT_CONFIG.json   ficha del documento y paleta de color
│   ├── 01_WRITING_RULES.md      reglas de escritura (sin marcas de texto de IA)
│   └── 02_NAMING.md             normas de nombres de carpetas y archivos
├── AGENT_AI/
│   ├── ESTADO.md        dónde estamos y qué sigue
│   ├── TRABAJO/
│   │   └── PLAN.md      objetivo, decisiones, índice y fases
[[NO CODEX]]
│   └── CLAUDE/          bitácora de Claude
[[FIN]]
[[SI CODEX]]
│   ├── CLAUDE/          bitácora de Claude
│   └── CODEX/           reglas y bitácora de Codex (ChatGPT)
[[FIN]]
├── 01_MATERIALS/        tus materiales: documentos, apuntes, PDF, imágenes
├── 02_WORK/             borradores y archivos en curso
├── 03_EXPORT/           lo terminado, listo para usar o enviar
└── 04_STYLE_MANUAL/     manual de estilo, su PDF y el generador
```

## Cómo se trabaja

- **La memoria del proyecto está en archivos, no en el chat.** `AGENT_AI/TRABAJO/PLAN.md` guarda las decisiones y las fases; `AGENT_AI/ESTADO.md` dice dónde se quedó el trabajo y qué sigue. Un chat nuevo los lee y continúa.
- **Los originales no se tocan.** Lo que hay en `01_MATERIALS` se lee; se trabaja en `02_WORK` y lo terminado va a `03_EXPORT`.
- **Los documentos siguen el manual.** Cuando toca producir el documento, Claude aplica `04_STYLE_MANUAL` con el color de la ficha.
- **Un chat, una tarea.** Al terminar, la IA actualiza el estado y te dice qué ha cambiado y qué no ha podido comprobar.
