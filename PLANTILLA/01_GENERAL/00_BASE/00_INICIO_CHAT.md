# Cómo empezar un chat sobre [PROYECTO]

Copia el prompt y pégalo como **primer mensaje** de un chat nuevo. Copia solo lo que hay dentro del recuadro.

---

## A. Con la app de escritorio de Claude (puede abrir esta carpeta)

Es la forma recomendada: Claude lee y escribe directamente en la carpeta.

```text
Hola. Vas a trabajar conmigo en el proyecto [PROYECTO].

1. Pídeme acceso a la carpeta del proyecto (una sola petición):
   [RUTA]

2. Lee enteros, en este orden:
   - AGENTS.md: las reglas del proyecto.
   - 00_CONFIG\01_WRITING_RULES.md: cómo escribir. Aplícalas en todo
     texto que me entregues, al redactar y en una segunda lectura.
   - 00_CONFIG\02_NAMING.md: normas de nombres. Síguelas cada vez que
     crees o renombres una carpeta o un archivo.
   - AGENT_AI\ESTADO.md: dónde lo dejamos y qué sigue.

3. Si todavía no sé bien qué quiero hacer, ayúdame a definirlo con
   preguntas cortas y dame tu recomendación. Guarda lo que decidamos en
   AGENT_AI\ESTADO.md.

4. Después te digo qué hacemos hoy.

Cómo quiero que trabajes conmigo:
- Respóndeme siempre en español y con palabras sencillas.
- Si hay que cambiar un archivo, guárdalo completo en la carpeta o dámelo
  completo para descargar; nunca trozos para editar.
- Dame siempre tu recomendación cuando haya que decidir algo.
- Al cerrar cada tarea con cambios, actualiza AGENT_AI\ESTADO.md y
  avísame en una frase.
```

---

## B. Sin acceso a la carpeta (Claude en el navegador o en el móvil)

Adjunta `AGENTS.md`, `00_CONFIG/01_WRITING_RULES.md` y `AGENT_AI/ESTADO.md`, y pega este prompt:

```text
Hola. Vas a trabajar conmigo en el proyecto [PROYECTO]. Te adjunto las
reglas (AGENTS.md), las reglas de escritura (01_WRITING_RULES.md) y el
estado (ESTADO.md). Léelos enteros antes de responder y aplica las reglas
de escritura en todo lo que me entregues. Como no puedes escribir en mi
carpeta, cuando cambies un archivo dámelo completo para descargarlo y
sustituirlo, y al final de cada tarea dame también el ESTADO.md
actualizado. Respóndeme en español y con palabras sencillas, y dame
siempre tu recomendación.
```
[[SI CODEX]]

---

## C. Con Codex (ChatGPT), abierto en esta carpeta

Codex carga `AGENTS.md` solo. Para arrancar una sesión:

```text
Lee AGENT_AI/CODEX/AGENT.md, 00_CONFIG/01_WRITING_RULES.md y
AGENT_AI/ESTADO.md. Confirma en 3 líneas dónde estamos y cuál es el
siguiente paso. No hagas nada más.
```
[[FIN]]

---

**Si mueves o renombras la carpeta:** cambia la ruta de este archivo (`[RUTA]`) y la del `README.md`.
