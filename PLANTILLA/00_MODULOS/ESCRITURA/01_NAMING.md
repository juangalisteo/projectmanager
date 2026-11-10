# NORMAS DE NOMENCLATURA

**Versión:** 1.1.0
**Fecha:** 06/11/2026
**Autor:** Juan Bautista Galisteo Marqués

---

## OBJETIVO

Estas normas fijan cómo se nombran las carpetas y los archivos de cualquier proyecto: los que crea Project Manager y los que se organizan a mano.

El objetivo es que cualquier persona (o IA) entienda la estructura de un vistazo, que todo salga ordenado en el explorador y que no haya nombres repetidos ni archivos sueltos.

---

## 01. MAYÚSCULAS

Los nombres de carpetas y archivos se escriben siempre en **MAYÚSCULAS**.

La **extensión** del archivo va siempre en **minúsculas** (ver norma 10).

### Correcto

    00_MASTER
    01_AVATAR
    02_INTRO

    00_BRAND_LOGO.png
    01_BRAND_ICON_VECTOR.svg

### Incorrecto

    00_Master
    01_avatar
    00_BRAND_LOGO.PNG

---

## 02. SEPARADOR

El separador entre palabras es siempre el guion bajo:

    _

### Correcto

    00_INTRO_MAIN
    01_SOUND_EFFECTS

### Incorrecto

    00 INTRO MAIN
    00-INTRO-MAIN
    00_Intro_Main

---

## 03. NUMERACIÓN

Toda carpeta y todo archivo de dentro del proyecto lleva un número de **dos dígitos al principio**.

El número marca el **orden** dentro de su nivel.

    00_NOMBRE
    01_NOMBRE
    02_NOMBRE
    ...
    99_NOMBRE

### Números reservados

    00 = BASE del nivel (configuración, documento principal, maestro)
    99 = ARCHIVE del nivel (cosas antiguas que no se usan pero se guardan)

Los números del `01` al `98` son para el contenido normal.

Se pueden dejar huecos (`01`, `05`, `10`…) si se prevé meter elementos en medio más adelante.

La **carpeta raíz** del proyecto no lleva número: es el nombre del proyecto (`MI_PROYECTO`).

Lo que llega de fuera (un PDF descargado, las fotos de una cámara) se renombra al guardarlo en el proyecto.

REGLA:

    NÚMERO   = DOS DÍGITOS
    POSICIÓN = SIEMPRE AL PRINCIPIO
    00       = BASE
    99       = ARCHIVE
    RAÍZ     = SIN NÚMERO

---

## 04. IDIOMA

Las **categorías estructurales** (nombres de carpetas y tipos de archivo) se escriben en **INGLÉS**.

    MASTER     BRAND      ASSETS     AUDIO
    VIDEO      IMAGE      SFX        DESIGN
    TEMPLATES  PROJECT    EXPORT     CONFIG
    DOCS       REPORTS    WORK       ARCHIVE
    SOURCES    MATERIALS

Los **títulos y nombres propios** (temas de vídeos, nombres de canales, libros…) pueden ir en su idioma original, siempre sin tildes ni Ñ.

### Correcto

    02_WORK/01_PROJECT_NAME
    00_BRAND/01_LOGO
    02_WORK/01_HISTORIA_DE_ROMA.md

### Incorrecto

    02_TRABAJOS
    00_MARCA/01_LOGOTIPO

---

## 05. CARACTERES

Solo se usan:

    A-Z
    0-9
    _

Se evitan:

    Espacios
    Tildes (Á É Í Ó Ú)
    Ñ (se escribe N: ESPANA, MONTANA)
    Signos: ¿ ? ¡ ! , ; : ( ) & % # @ ' "

### Correcto

    02_INTRO_MAIN

### Incorrecto

    02_INTRO_PRINCÍPAL
    02_INTRO_MAIN!
    02 INTRO MAIN

**Motivo:** los espacios, tildes y signos dan problemas en programas, terminal, GitHub y al subir archivos a la web.

---

## 06. NOMBRES

Los nombres deben ser:

- **Cortos:** máximo 3–4 palabras.
- **Claros:** se entiende qué hay dentro sin abrirlo.
- **Únicos:** no puede haber dos nombres iguales en el mismo nivel.
- **Consistentes:** una misma cosa se llama siempre igual en todo el proyecto.

### Correcto

    01_AUDIO
    02_VIDEO
    03_IMAGE

### Evitar

    01_ARCHIVOS_DE_AUDIO_UTILIZADOS
    02_TODOS_LOS_VIDEOS
    03_FINAL_FINAL_BUENO

---

## 07. VERSIONES

Cuando un mismo archivo tiene varias versiones, el número del principio **no cambia** y la versión se añade **al final** con `_V` y dos dígitos.

    00_WORDMARK_LOGO_V01.png
    00_WORDMARK_LOGO_V02.png
    00_WORDMARK_LOGO_V03.png

Así todas las versiones salen juntas y se ve cuál es la última.

### Incorrecto

    00_WORDMARK_LOGO.png
    01_WORDMARK_LOGO.png      ← parece otro elemento distinto
    00_WORDMARK_LOGO_FINAL.png

Las versiones viejas que ya no se usan van a la carpeta `99_ARCHIVE` de ese nivel.

---

## 08. VARIANTES

Si un elemento tiene **variantes** (no versiones, sino formas distintas del mismo elemento), cada variante lleva su propio número y una palabra que la describe.

    00_WORDMARK_LOGO.png
    01_WORDMARK_HORIZONTAL.png
    02_WORDMARK_STACKED.png
    03_WORDMARK_VECTOR.svg

REGLA:

    VARIANTE = NÚMERO NUEVO + NOMBRE DESCRIPTIVO
    VERSIÓN  = MISMO NÚMERO + _V01, _V02...

---

## 09. CARPETAS DE ORGANIZACIÓN (opcional)

Fuera de los proyectos, las carpetas que **agrupan** proyectos en tu organización personal (por ejemplo, las carpetas de una marca) pueden usar el separador visual `¦`:

    IDENTIFICADOR ¦ NOMBRE

    00 ¦ DOCS
    01 ¦ SOCIAL
    02 ¦ DESIGN

Reglas de esta excepción:

- Solo se usa en esas carpetas de agrupación. **Nunca dentro de un proyecto.**
- Es la única excepción a «sin espacios» y «sin signos».
- Una carpeta que vaya a abrirse en la terminal o a subirse a GitHub no la usa.

---

## 10. EXTENSIONES

La extensión va siempre en **minúsculas** y es la estándar de cada tipo:

    .md   .txt  .pdf  .json .csv
    .png  .jpg  .svg
    .mp4  .mov  .wav  .mp3
    .psd  .ai   .prproj

---

## 11. FECHAS

Si un nombre necesita fecha, se escribe así (año-mes-día, sin separadores):

    AAAAMMDD

Ejemplo:

    03_REPORT_20261030.md

Así los archivos se ordenan solos por fecha.

---

## 12. EXCEPCIONES

### Nombres estándar

Se dejan tal cual, sin número, porque los programas y las webs los buscan con ese nombre:

    README.md      → presentación de una carpeta o proyecto
    AGENTS.md      → reglas para agentes de IA
    CLAUDE.md      → instrucciones que carga Claude Code al abrir la carpeta
    CHANGELOG.md   → historial de versiones
    LICENSE        → licencia
    .gitignore     → configuración de Git

### Sistema de trabajo con IA

Nombres fijos e iguales en todos los proyectos, porque los agentes y los prompts los buscan por su nombre exacto:

    00_INICIO_CHAT.md   → prompt para empezar un chat (lleva 00 por ser la base)
    AGENT_AI/           → memoria del trabajo con la IA, y todo lo que hay dentro:
                          ESTADO.md, LEEME.md, TRABAJO/ (PLAN.md, IDEAS_FUTURAS.md),
                          CLAUDE/ y CODEX/ (AGENT.md, BITACORA.md, PUENTE.md, REPORTS/)

Los archivos que se creen dentro de `REPORTS/` sí siguen la norma 11: `AAAAMMDD_TEMA.md`.

### Código

En los proyectos con código (programas, aplicaciones, webs), **el código y sus carpetas** siguen el estándar de su lenguaje y de sus herramientas, normalmente en minúsculas y sin número: `src/`, `docs/`, `tests/`, `index.html`, `main.py`. Así funcionan sin problemas en la terminal, en GitHub y en cada programa.

Lo que no es código dentro de esos proyectos (documentos, imágenes de trabajo, recursos de diseño) sigue estas normas.

---

## EJEMPLO DE ESTRUCTURA

Un proyecto de tipo Documento creado con Project Manager:

    MI_DOCUMENTO/
    ├── README.md
    ├── 00_INICIO_CHAT.md
    ├── AGENTS.md
    ├── 00_CONFIG/
    │   ├── 00_PROJECT_CONFIG.json
    │   └── 01_WRITING_RULES.md
    ├── AGENT_AI/
    │   └── ESTADO.md
    ├── 01_MATERIALS/
    │   ├── 01_INFORME_ANUAL_2025.pdf
    │   └── 02_ENTREVISTA_NOTAS.md
    ├── 02_WORK/
    │   ├── 01_CAPITULO_INTRO_V01.md
    │   ├── 01_CAPITULO_INTRO_V02.md
    │   └── 99_ARCHIVE/
    └── 03_EXPORT/
        └── 01_MI_DOCUMENTO_20261106.pdf

---

# RESUMEN

    MAYÚSCULAS        = SÍ (extensión en minúsculas)
    SEPARADOR         = _
    NUMERACIÓN        = DOS DÍGITOS, SIEMPRE AL PRINCIPIO
    00                = BASE DEL NIVEL
    99                = ARCHIVE DEL NIVEL
    RAÍZ DEL PROYECTO = SIN NÚMERO
    IDIOMA            = INGLÉS ESTRUCTURAL / TÍTULOS EN SU IDIOMA
    CARACTERES        = A-Z / 0-9 / _
    ESPACIOS/TILDES/Ñ = NO (Ñ → N)
    VERSIÓN           = _V01 AL FINAL
    VARIANTE          = NÚMERO NUEVO
    FECHA             = AAAAMMDD
    ¦                 = SOLO CARPETAS DE ORGANIZACIÓN, NUNCA DENTRO DE UN PROYECTO
    EXCEPCIONES       = NOMBRES ESTÁNDAR, SISTEMA DE IA (AGENT_AI) Y CÓDIGO

---

© 2026 · Juan Bautista Galisteo Marqués
