# Cómo empezar un chat sobre [PROYECTO]

Copia el prompt y pégalo como **primer mensaje** de un chat nuevo. Copia solo lo que hay dentro del recuadro.

---

## A. Con la app de escritorio de Claude (puede abrir esta carpeta)

Es la forma recomendada: Claude lee y escribe directamente en la carpeta.

```text
Hola. Vas a trabajar conmigo en el documento [PROYECTO].

1. Pídeme acceso a la carpeta del proyecto (una sola petición):
   [RUTA]

2. Lee enteros, en este orden:
   - AGENTS.md: las reglas del proyecto.
   - 00_CONFIG\01_WRITING_RULES.md: cómo escribir. Aplícalas en todo
     texto que me entregues, al redactar y en una segunda lectura.
   - 00_CONFIG\02_NAMING.md: normas de nombres. Síguelas cada vez que
     crees o renombres una carpeta o un archivo.
   - 00_CONFIG\00_PROJECT_CONFIG.json: la ficha del documento.
   - AGENT_AI\TRABAJO\PLAN.md: objetivo, decisiones y fases.
   - AGENT_AI\ESTADO.md: dónde lo dejamos y qué sigue.
   Cuando toque producir el documento, lee también
   04_STYLE_MANUAL\00_MANUAL_DE_ESTILO.pdf y
   04_STYLE_MANUAL\02_PROMPTS\01_APLICAR_MANUAL.md, y aplícalos.

3. Si en la ficha faltan datos (tema, objetivo, público, tipo de trabajo,
   alcance, entregables, formato o color), pregúntamelos todos juntos y
   dame tu recomendación para cada uno. Guárdalos en la ficha.

4. Después te digo qué hacemos hoy.

Tu papel:
- Haces el trabajo completo: investigas, redactas, compones y revisas.
- Mis originales de 01_MATERIALS no se tocan: trabajas en 02_WORK y lo
  terminado va a 03_EXPORT.
- Al cerrar cada tarea con cambios, actualizas AGENT_AI\ESTADO.md y, si
  hay una decisión nueva, AGENT_AI\TRABAJO\PLAN.md. Avísame en una frase.

Cómo quiero que trabajes conmigo:
- Respóndeme siempre en español y con palabras sencillas.
- Si hay que cambiar un archivo, guárdalo completo en la carpeta o dámelo
  completo para descargar; nunca trozos para editar.
- Dame siempre tu recomendación cuando haya que decidir algo.
```

---

## B. Sin acceso a la carpeta (Claude en el navegador o en el móvil)

Adjunta estos archivos, en este orden, y pega el prompt:

1. `AGENTS.md`
2. `00_CONFIG/01_WRITING_RULES.md`
3. `00_CONFIG/00_PROJECT_CONFIG.json`
4. `AGENT_AI/TRABAJO/PLAN.md`
5. `AGENT_AI/ESTADO.md`
6. `04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf`, solo si hoy toca producir el documento
7. Los archivos de `01_MATERIALS` que necesites hoy

```text
Hola. Vas a trabajar conmigo en el documento [PROYECTO]. Te adjunto las
reglas, las reglas de escritura, la ficha, el plan y el estado. Léelos
enteros antes de responder y aplica las reglas de escritura en todo lo que
me entregues. Si en la ficha faltan datos, pregúntamelos juntos con tu
recomendación. Como no puedes escribir en mi carpeta, cuando cambies un
archivo dámelo completo para descargarlo y sustituirlo, y al final de cada
tarea dame también el ESTADO.md actualizado. Respóndeme en español y con
palabras sencillas, y dame siempre tu recomendación.
```
[[SI CODEX]]

---

## C. Con Codex (ChatGPT), abierto en esta carpeta

Codex carga `AGENTS.md` solo. Para arrancar una sesión:

```text
Lee AGENT_AI/CODEX/AGENT.md, 00_CONFIG/01_WRITING_RULES.md,
AGENT_AI/TRABAJO/PLAN.md y AGENT_AI/ESTADO.md. Confirma en 3 líneas dónde
estamos y cuál es el siguiente paso. No hagas nada más.
```
[[FIN]]

---

**Si mueves o renombras la carpeta:** cambia la ruta de este archivo (`[RUTA]`), la del `README.md` y el campo `proyecto.ruta` de `00_CONFIG/00_PROJECT_CONFIG.json`.
