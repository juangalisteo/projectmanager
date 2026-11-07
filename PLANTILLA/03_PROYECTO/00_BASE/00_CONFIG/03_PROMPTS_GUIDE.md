# GUÍA DE PROMPTS · [PROYECTO]

Cómo pedir tareas a un agente de IA en este proyecto: qué se pone en cada prompt y qué no. La idea viene del trabajo con agentes en proyectos anteriores y se resume en una frase:

**PROMPT = SOLO LO NUEVO DE ESTA TAREA.**

Las reglas permanentes ya están en `AGENTS.md` y en el `AGENT.md` de cada agente; el estado, en `AGENT_AI/ESTADO.md`; las decisiones, en `AGENT_AI/TRABAJO/PLAN.md`. Repetirlas en cada prompt gasta contexto y esconde la tarea real.

---

## 1. Qué lleva un prompt

| Parte | Qué escribir | ¿Siempre? |
| --- | --- | --- |
| Tarea | Un nombre corto: «P2 — Pantalla de ajustes» | Sí |
| Referencia | El documento o apartado relacionado, por su ruta | Si existe |
| Objetivo | Qué debe conseguir, en una o dos frases | Sí |
| Alcance | Qué archivos o partes puede tocar | Sí |
| Preservar | Solo lo delicado de esta tarea | Si hace falta |
| Criterio de cierre | Qué tiene que ser cierto para darla por terminada | Sí |

## 2. Qué no se repite

No hace falta escribir en cada prompt «responde en español», «no hagas commit», «actualiza la bitácora», «no toques otros archivos» ni «lee AGENTS.md»: ya lo dicen las reglas. Tampoco se pide leer la bitácora entera; se busca lo concreto cuando hay una duda histórica.

Sí conviene decir cuándo se quiere el `PUENTE.md` (por ejemplo, al cerrar un lote), porque por defecto no se genera.

## 3. Plantillas

### Arranque de sesión

```text
Lee AGENT_AI/ESTADO.md. Confirma en 3 líneas: línea activa, último
resultado y siguiente paso. No hagas nada más.
```

### Tarea

```text
[NOMBRE]
Referencia: [documento §]
Objetivo:
Alcance:
Preservar:
Criterio de cierre:
```

### Auditoría (solo lectura)

```text
[NOMBRE]
Alcance de lectura: [lista cerrada de archivos o carpetas]
Preguntas:
Salida: AGENT_AI/<AGENTE>/REPORTS/AAAAMMDD_TEMA.md
Las dudas van como preguntas abiertas en el informe.
```

### Decisión

```text
Decisión [Pn]: [opción elegida + matiz].
Regístrala en AGENT_AI/TRABAJO/PLAN.md («Decisiones») y en ESTADO.md.
Continúa con [paso] / no continúes.
```

### Retomar tras una parada

```text
Retoma [lote] detenido en [paso]. Nueva información: [...].
Repite solo la comprobación [x].
```

### Cierre de lote

```text
Cierra [lote]: revisión final, comprobación [focal | completa, una vez],
commit "[mensaje]" (sí/no), push (sí/no), PUENTE.md (sí/no).
```

No todos los apartados son obligatorios. Si una tarea se define bien con menos, se usa menos.

## 4. Tareas grandes

Una tarea grande se parte en pasos, y cada prompt avanza uno:

```text
ENTENDER → DISEÑAR → APROBAR → HACER (bloque 1) → COMPROBAR → HACER (bloque 2) → COMPROBAR → CERRAR
```

No se empieza a hacer mientras haya decisiones abiertas. **Un prompt, una responsabilidad**: no se mezclan en el mismo prompt una auditoría, un rediseño y una implementación.

## 5. Modelo y esfuerzo

El asesor indica el modelo **fuera** del prompt, en una línea visible justo antes: «Opus alto», «Opus medio» o «Sonnet». Sonnet para tareas sencillas y acotadas; Opus para tareas delicadas, que tocan mucho o cambian cómo funciona algo, o si Sonnet ya falló.

## 6. Prueba antes de enviar

Antes de añadir algo al prompt: ¿el agente lo necesita de verdad para **esta** tarea? Si no, fuera. Si ya está en un documento del proyecto, se nombra la ruta en vez de copiarlo.
