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

`00_INICIO_CHAT.md` es el prompt de arranque: lleva solo el mensaje, sin explicaciones.

1. Abre un chat nuevo en la app de escritorio de Claude.
2. Copia **entero** `00_INICIO_CHAT.md` y pégalo como primer mensaje, o adjúntalo tal cual. También lo copia el botón «Prompt · IA» de Project Manager.
3. Claude pide acceso a esta carpeta, lee las reglas, la ficha, el plan y el estado, y te pregunta los datos que falten o te dice dónde estamos.

### Si usas Claude sin acceso a la carpeta (navegador o móvil)

Adjunta estos archivos, en este orden:

1. `AGENTS.md`
2. `00_CONFIG/01_WRITING_RULES.md`
3. `00_CONFIG/00_PROJECT_CONFIG.json`
4. `AGENT_AI/TRABAJO/PLAN.md`
5. `AGENT_AI/ESTADO.md`
6. `04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf`, solo si hoy toca producir el documento
7. Los archivos de `01_MATERIALS` que necesites hoy

Y pega este mensaje:

```text
Hola. Vas a trabajar conmigo en el documento [PROYECTO]. Te adjunto las
reglas, las reglas de escritura, la ficha, el plan y el estado. Léelos
enteros y aplica las reglas de escritura en todo lo que me entregues. Si
en la ficha faltan datos, pregúntamelos juntos con tu recomendación; si
no, dime en tres líneas dónde estamos y cuál es el siguiente paso. Como no
puedes escribir en mi carpeta, cuando cambies un archivo dámelo completo
para descargarlo, y al final de cada tarea dame también el ESTADO.md
actualizado. Antes de cambiar nada, explícame qué vas a cambiar y espera
a que te diga que sí. Respóndeme en español y con palabras sencillas, y
dame siempre tu recomendación.
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
