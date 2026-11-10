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

`00_INICIO_CHAT.md` es el prompt de arranque: lleva solo el mensaje, sin explicaciones.

1. Abre un chat nuevo en la app de escritorio de Claude.
2. Copia **entero** `00_INICIO_CHAT.md` y pégalo como primer mensaje, o adjúntalo tal cual. También lo copia el botón «Prompt · IA» de Project Manager.
3. Claude pide acceso a esta carpeta, lee las reglas y el estado, te dice dónde estamos y espera a que le digas qué hacemos.

### Si usas Claude sin acceso a la carpeta (navegador o móvil)

Adjunta `AGENTS.md`, `00_CONFIG/01_WRITING_RULES.md` y `AGENT_AI/ESTADO.md`, y pega este mensaje:

```text
Hola. Vas a trabajar conmigo en el proyecto [PROYECTO]. Te adjunto las
reglas (AGENTS.md), las reglas de escritura (01_WRITING_RULES.md) y el
estado (ESTADO.md). Léelos enteros y dime en tres líneas dónde estamos y
cuál es el siguiente paso. Como no puedes escribir en mi carpeta, cuando
cambies un archivo dámelo completo para descargarlo, y al final de cada
tarea dame también el ESTADO.md actualizado. Antes de cambiar nada,
explícame qué vas a cambiar y espera a que te diga que sí. Respóndeme en
español y con palabras sencillas, y dame siempre tu recomendación.
```
[[SI CODEX]]

### Con Codex (ChatGPT)

No necesita prompt de arranque: al abrirlo en esta carpeta lee `AGENTS.md` solo, y ahí se le dice que lea sus reglas (`AGENT_AI/CODEX/AGENT.md`).
[[FIN]]

## Qué hay en la carpeta

```
[CARPETA]/
├── README.md            este archivo
├── 00_INICIO_CHAT.md    prompt de arranque para un chat nuevo
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
