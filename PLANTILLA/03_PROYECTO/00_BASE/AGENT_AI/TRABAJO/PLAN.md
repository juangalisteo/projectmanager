# PLAN · [PROYECTO]

> Documento principal del proyecto. Lo lee primero cualquier chat nuevo.
> Actualizado: [FECHA].

---

## Cómo trabajamos

- **Asesor (app de escritorio de Claude):** diseña, explica decisiones, revisa resúmenes y prepara los prompts para el ejecutor según `00_CONFIG/03_PROMPTS_GUIDE.md`. Lee todo el proyecto, pero no toca código ni Git. Escribe solo en este archivo, en `IDEAS_FUTURAS.md`, en `AGENT_AI/ESTADO.md` y en `AGENT_AI/LEEME.md`, y avisa en una frase de cada cambio.
- **Ejecutor (Claude Code[[SI CODEX]] o Codex[[FIN]]):** ejecuta un paso por chat nuevo, sobre los archivos, según el prompt del asesor.
- **Propietario ([AUTOR]):** aprueba cada fase y decide todo lo que es de producto.
- **Ciclo:** el asesor prepara el prompt → el ejecutor lo hace en un chat nuevo → resumen de 3 o 4 líneas → el asesor lo revisa y prepara el siguiente.
- Al ejecutor no se le pegan documentos: se le indica la ruta. Al asesor se le pega solo el resumen final, salvo que haya que decidir sobre un informe.
- **Modelos:** antes de cada prompt, una línea visible con el modelo y el esfuerzo: «Opus alto», «Opus medio» o «Sonnet».
- El asesor no manda un prompt nuevo mientras el ejecutor sigue trabajando y no ha pasado su resumen.
- **Idioma:** todo en español y con palabras sencillas. Los archivos que cambian se entregan completos.

## Objetivo

Pendiente. Qué debe conseguir el programa y cómo sabremos que la primera versión está terminada. Sale de la ficha (`00_CONFIG/00_PROJECT_CONFIG.json`).

## Decisiones tomadas

Cada decisión con su fecha, quién la tomó y por qué. Las que parecen mejorables pero son así a propósito también van en `AGENTS.md` §9.

- [FECHA] · Proyecto creado con Project Manager.
- [FECHA] · Licencia GPL-3.0 (decisión fija del propietario para todos sus programas).

## Fases

| Fase | Qué | Estado |
| --- | --- | --- |
| A | Ficha completa y diseño: qué hace, para quién, tecnología y estructura de carpetas del código | pendiente |
| B | Arranque: `git init`, `.gitignore` revisado, primer commit y repositorio en GitHub (privado) | pendiente |
| C | Primera versión que funcione, en lotes pequeños con sus pruebas | pendiente |
| D | Documentación: README, CHANGELOG y capturas en `docs/` | pendiente |
| E | Publicación de la versión `v1.0.0` en GitHub, con la licencia GPL-3.0 (`LICENSE`) | pendiente |

## Preguntas pendientes

Ninguna todavía.

## Último resumen recibido

Ninguno todavía.
