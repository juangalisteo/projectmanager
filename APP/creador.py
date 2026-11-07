"""Project Manager · crea la carpeta de un proyecto nuevo a partir de PLANTILLA.

La ventana (interfaz.py) usa este archivo. También se puede usar desde la consola:

    python APP/creador.py --nombre "Mi proyecto" --tipo DOCUMENTO --destino "C:\\ruta" --color "#2E7D6B"

Qué hace:
1. Convierte el nombre en un nombre de carpeta según las normas (MAYÚSCULAS, _, sin tildes).
2. Copia las partes de PLANTILLA que corresponden al tipo de proyecto.
3. Cambia las etiquetas ([PROYECTO], [RUTA], [COLOR]…) por sus valores y quita los
   bloques [[SI …]] … [[FIN]] que no tocan.
4. Escribe la ficha 00_CONFIG/00_PROJECT_CONFIG.json con la paleta calculada.
5. Comprueba que no queda ninguna etiqueta sin rellenar.

Lo crea todo primero en una carpeta temporal y solo al final le pone su nombre: si algo
falla, no queda una carpeta a medias.

Project:   Project Manager v1.0.0
Author:    Juan Bautista Galisteo Marqués (@juangalisteo)
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import random
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ folders next to the program

APP = Path(__file__).resolve().parent
ROOT = APP.parent
PLANTILLA = ROOT / "PLANTILLA"
SETTINGS = APP / "projectmanager_ajustes.json"
VERSION = "1.0.0"

TIPOS = {
    "DOCUMENTO": "Documento",
    "PROYECTO": "Proyecto",
    "GENERAL": "General",
}
ORIGINAL_COLOR = "#C7A15B"
ORIGINAL_COLORS = {
    "background": "#FAFAF7", "surface": "#FFFFFF", "text": "#22343D", "muted": "#596771",
    "accent": "#C7A15B", "accent_text": "#7B5A26", "accent_surface": "#F3E9D6", "border": "#DADFE1",
    "row": "#F3F5F6", "gradient_strong": "#EAD5AC", "gradient_soft": "#F5ECD9", "grid_line": "#EDF0F1",
    "accent_on_dark": "#C7A15B",
}

# Qué parte de PLANTILLA se copia, a dónde, si lleva etiquetas y para qué proyectos.
# (origen, destino, procesar_etiquetas, condición)
PIEZAS = [
    # General: the minimum (rules, state and a work folder). With ChatGPT, one log per agent.
    ("01_GENERAL/00_BASE", "", True, lambda o: o.tipo == "GENERAL"),
    ("01_GENERAL/01_CODEX", "", True, lambda o: o.tipo == "GENERAL" and o.codex),
    # Documento: plan, Claude's log, work folders and the style manual.
    ("02_DOCUMENTO/00_BASE", "", True, lambda o: o.tipo == "DOCUMENTO"),
    ("02_DOCUMENTO/01_CODEX", "", True, lambda o: o.tipo == "DOCUMENTO" and o.codex),
    ("00_MODULOS/MANUAL", "04_STYLE_MANUAL", False, lambda o: o.tipo == "DOCUMENTO"),
    # Writing rules and naming rules, copied as they are (all types)
    ("00_MODULOS/ESCRITURA/02_WRITING_RULES.md", "00_CONFIG/01_WRITING_RULES.md", False,
     lambda o: True),
    ("00_MODULOS/ESCRITURA/01_NAMING.md", "00_CONFIG/02_NAMING.md", False, lambda o: True),
    # Proyecto: advisor (desktop app) + executor (Claude Code), with Git, tests and the GPL-3.0 licence.
    ("03_PROYECTO/00_BASE", "", True, lambda o: o.tipo == "PROYECTO"),
    ("03_PROYECTO/01_CODEX", "", True, lambda o: o.tipo == "PROYECTO" and o.codex),
    ("03_PROYECTO/02_LICENSE/LICENSE", "LICENSE", False, lambda o: o.tipo == "PROYECTO"),
]
# Empty folders that each type creates (an empty folder cannot travel inside PLANTILLA with Git).
CARPETAS_VACIAS = {
    "GENERAL": ["01_WORK"],
    "DOCUMENTO": ["01_MATERIALS", "02_WORK", "03_EXPORT"],
    "PROYECTO": ["docs", "tests", "AGENT_AI/CLAUDE/REPORTS"],
}
CARPETAS_VACIAS_CODEX = {"PROYECTO": ["AGENT_AI/CODEX/REPORTS"]}
# Types that get the project card 00_CONFIG/00_PROJECT_CONFIG.json (colour and palette).
CON_FICHA = {"DOCUMENTO", "PROYECTO"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".gitignore", ".cmd", ".csv", ""}
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "00_TEMP")
TAG_RE = re.compile(r"\[(PROYECTO|CARPETA|RUTA|TIPO|COLOR|FECHA|FECHA_ISO|AUTOR|GITHUB)\]")
BLOCK_RE = re.compile(r"\[\[(SI|NO) ([A-Z|]+)\]\]((?:(?!\[\[(?:SI|NO) ).)*?)\[\[FIN\]\]", re.S)


class ErrorProyecto(Exception):
    """Error con un mensaje para mostrar tal cual al usuario."""


@dataclass
class Opciones:
    nombre: str
    tipo: str
    destino: Path
    color: str | None = None          # None = identidad original
    codex: bool = False
    autor: str = ""
    github: str = ""
    fecha: datetime.date = field(default_factory=datetime.date.today)


@dataclass
class Resultado:
    ruta: Path
    archivos: int
    carpeta: str


# ── Ajustes guardados ─────────────────────────────────────────────────────
def cargar_ajustes() -> dict:
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def guardar_ajustes(**valores) -> None:
    try:
        datos = cargar_ajustes()
        datos.update(valores)
        SETTINGS.write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception:
        pass


# ── Nombres y valores ─────────────────────────────────────────────────────
def nombre_carpeta(nombre: str) -> str:
    """«Mi proyecto» → «MI_PROYECTO» (norma de nombres: A-Z, 0-9 y _)."""
    texto = nombre.strip().replace("ñ", "n").replace("Ñ", "N")
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^A-Za-z0-9]+", "_", texto).strip("_").upper()
    return re.sub(r"_+", "_", texto)


def color_valido(color: str) -> str:
    color = color.strip().upper()
    if not color.startswith("#"):
        color = "#" + color
    if not re.fullmatch(r"#[0-9A-F]{6}", color):
        raise ErrorProyecto(f"El color «{color}» no es válido. Escríbelo como #RRGGBB, por ejemplo #2E7D6B.")
    return color


def fecha_texto(fecha: datetime.date) -> str:
    return fecha.strftime("%d/%m/%Y")


_PALETA = None


def cargar_paleta():
    """The palette calculator of the style manual (loaded once)."""
    global _PALETA
    if _PALETA is None:
        ruta = PLANTILLA / "00_MODULOS" / "MANUAL" / "03_SOURCE" / "01_PALETTE.py"
        spec = importlib.util.spec_from_file_location("palette", ruta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        _PALETA = modulo
    return _PALETA


def paleta(color: str | None) -> dict:
    """Full palette for a colour; None = the default (original) palette."""
    return dict(ORIGINAL_COLORS) if color is None else cargar_paleta().palette(color_valido(color))


def paleta_legible(colores: dict) -> bool:
    """True if every text/background pair of the palette passes its contrast check."""
    m = cargar_paleta()
    return (m.contrast(colores["accent"], colores["background"]) >= 3
            and all(m.contrast(colores[a], colores[b]) >= minimo for _, a, b, minimo in m.CHECKS))


def color_aleatorio(rng: random.Random | None = None) -> str:
    """A random main colour that always gives a readable palette:
    any hue, lively but not neon, neither too light nor too dark."""
    rng = rng or random.Random()
    m = cargar_paleta()
    for _ in range(80):
        candidato = m.tone(rng.uniform(0, 360), rng.uniform(40, 70), rng.uniform(42, 60))
        if paleta_legible(m.palette(candidato)):
            return candidato
    return "#2E7D6B"


def valores(o: Opciones, carpeta: str, ruta: Path) -> dict:
    return {
        "PROYECTO": o.nombre.strip(),
        "CARPETA": carpeta,
        "RUTA": str(ruta),
        "TIPO": TIPOS[o.tipo],
        "COLOR": o.color or f"{ORIGINAL_COLOR} (predeterminado)",
        "FECHA": fecha_texto(o.fecha),
        "FECHA_ISO": o.fecha.isoformat(),
        "AUTOR": o.autor or "el propietario",
        "GITHUB": o.github or "",
    }


# ── Plantilla ─────────────────────────────────────────────────────────────
def activas(o: Opciones) -> set[str]:
    claves = {o.tipo}
    if o.codex:
        claves.add("CODEX")
    return claves


def resolver_bloques(texto: str, claves: set[str]) -> str:
    """Quita o deja los bloques [[SI A|B]] … [[FIN]] y [[NO A]] … [[FIN]].
    Un marcador solo en su línea se lleva también su salto de línea."""
    texto = re.sub(r"(?m)^[ \t]*(\[\[(?:SI|NO) [A-Z|]+\]\]|\[\[FIN\]\])[ \t]*\n", r"\1", texto)
    while True:
        nuevo = BLOCK_RE.sub(lambda m: m[3] if ((m[1] == "SI") == bool(set(m[2].split("|")) & claves)) else "", texto)
        if nuevo == texto:
            break
        texto = nuevo
    if "[[" in texto and re.search(r"\[\[(SI|NO|FIN)", texto):
        raise ErrorProyecto("La plantilla tiene un bloque [[SI …]] sin su [[FIN]].")
    return texto


def procesar(texto: str, mapa: dict, claves: set[str]) -> str:
    texto = resolver_bloques(texto, claves)
    texto = re.sub(r"\n{3,}", "\n\n", texto)  # sin líneas en blanco dobles al quitar bloques
    return TAG_RE.sub(lambda m: mapa[m[1]], texto)


def ficha(o: Opciones, carpeta: str, ruta: Path) -> dict:
    if o.color:
        colores = cargar_paleta().palette(o.color)
        modo = "un_color"
    else:
        colores = dict(ORIGINAL_COLORS)
        modo = "identidad_original"
    datos = {
        "schema_version": "1.0.0",
        "_uso": "Ficha del proyecto. Claude pregunta los campos vacíos (null) al empezar. Si mueves la carpeta, cambia proyecto.ruta.",
        "ficha": {
            "tema": None, "objetivo": None, "publico": None, "tipo_de_trabajo": None,
            "alcance": {"incluye": [], "excluye": []}, "entregables": [], "formato": None,
            "color_principal": colores["accent"],
        },
        "proyecto": {
            "nombre_visible": o.nombre.strip(), "carpeta": carpeta, "ruta": str(ruta),
            "tipo": o.tipo, "responsable": o.autor or None, "github": o.github or None,
            "idioma": "es-ES", "creado": o.fecha.isoformat(),
            "creado_con": f"Project Manager v{VERSION}",
            **({"licencia": "GPL-3.0"} if o.tipo == "PROYECTO" else {}),
        },
        "modulos": {
            "escritura": True,
            "documentos_maquetados": o.tipo == "DOCUMENTO",
            "agentes": ["CLAUDE"] + (["CODEX"] if o.codex else []),
        },
        "identity": {
            "font_family": "Inter", "font_is_fixed": True,
            "primary_color": colores["accent"], "palette_mode": modo, "colors": colores,
        },
    }
    if o.tipo == "DOCUMENTO":
        datos["documento"] = {
            "composicion": {
                "portada": None,
                "_portada_valores": "fotografia_del_tema | simbolo_rotulado | cifra_protagonista | directa_al_contenido",
                "indice": None,
                "cierre": None,
                "_cierre_valores": "ideas_clave | conclusiones | proximos_pasos | nota_de_uso",
                "pagina_final": {"imagen": None, "frase": [None, None]},
                "simbolos": [],
            },
            "cabecera": {"nombre": o.nombre.strip().upper(), "icono": "grid", "logo_path": None},
            "manual": "04_STYLE_MANUAL/00_MANUAL_DE_ESTILO.pdf",
        }
    datos["estado"] = {"decisiones": [], "pendientes": ["Completar la ficha"], "ultima_revision": None}
    return datos


def comprobar_restos(carpeta: Path, procesados: list[Path]) -> None:
    restos = []
    for ruta in procesados:
        texto = ruta.read_text(encoding="utf-8")
        if TAG_RE.search(texto) or re.search(r"\[\[(SI|NO|FIN)", texto):
            restos.append(str(ruta.relative_to(carpeta)))
    if restos:
        raise ErrorProyecto("Quedan etiquetas sin rellenar en: " + ", ".join(restos))


# ── Crear ─────────────────────────────────────────────────────────────────
def crear_proyecto(o: Opciones) -> Resultado:
    o.tipo = o.tipo.upper()
    if o.tipo not in TIPOS:
        raise ErrorProyecto("Elige un tipo de proyecto: Documento, Programa o General.")
    if not o.nombre.strip():
        raise ErrorProyecto("Escribe el nombre del proyecto.")
    carpeta = nombre_carpeta(o.nombre)
    if not carpeta:
        raise ErrorProyecto("El nombre tiene que llevar al menos una letra o un número.")
    if o.color:
        o.color = color_valido(o.color)
    destino = Path(o.destino).expanduser()
    if not str(o.destino).strip() or not destino.is_dir():
        raise ErrorProyecto("Elige una carpeta de destino que exista.")
    if not PLANTILLA.is_dir():
        raise ErrorProyecto(f"No encuentro la carpeta PLANTILLA en {ROOT}.")
    faltan = [origen for origen, _, _, condicion in PIEZAS if condicion(o) and not (PLANTILLA / origen).exists()]
    if faltan:
        raise ErrorProyecto("Falta en PLANTILLA: " + ", ".join(faltan).replace("/", "\\")
                            + ". Si has movido o renombrado esas carpetas, déjalas como estaban.")
    final = destino / carpeta
    if final.exists():
        raise ErrorProyecto(f"Ya existe una carpeta llamada {carpeta} en el destino. Cambia el nombre o el destino.")

    temporal = destino / f".{carpeta}_CREANDO"
    if temporal.exists():
        shutil.rmtree(temporal)
    mapa = valores(o, carpeta, final)
    claves = activas(o)
    procesados = []
    try:
        for origen, dentro, con_etiquetas, condicion in PIEZAS:
            if not condicion(o):
                continue
            base = PLANTILLA / origen
            if base.is_file():  # a single file, copied as it is
                (temporal / dentro).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(base, temporal / dentro)
                continue
            shutil.copytree(base, temporal / dentro, dirs_exist_ok=True, ignore=IGNORE)
            if not con_etiquetas:
                continue
            for archivo in base.rglob("*"):
                if archivo.is_file() and archivo.suffix.lower() in TEXT_SUFFIXES and "__pycache__" not in archivo.parts:
                    copia = temporal / dentro / archivo.relative_to(base)
                    texto = archivo.read_text(encoding="utf-8")
                    copia.write_text(procesar(texto, mapa, claves), encoding="utf-8", newline="\n")
                    procesados.append(copia)
        for vacia in CARPETAS_VACIAS.get(o.tipo, []) + (CARPETAS_VACIAS_CODEX.get(o.tipo, []) if o.codex else []):
            (temporal / vacia).mkdir(parents=True, exist_ok=True)
        if o.tipo in CON_FICHA:
            config = temporal / "00_CONFIG" / "00_PROJECT_CONFIG.json"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text(json.dumps(ficha(o, carpeta, final), indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")
        comprobar_restos(temporal, procesados)
        temporal.rename(final)
    except ErrorProyecto:
        shutil.rmtree(temporal, ignore_errors=True)
        raise
    except Exception as exc:
        shutil.rmtree(temporal, ignore_errors=True)
        raise ErrorProyecto(f"No se ha podido crear el proyecto: {exc}") from exc
    archivos = sum(1 for p in final.rglob("*") if p.is_file())
    return Resultado(final, archivos, carpeta)


def main(argv=None) -> int:
    ajustes = cargar_ajustes()
    ap = argparse.ArgumentParser(description="Crea un proyecto nuevo a partir de PLANTILLA.")
    ap.add_argument("--nombre", required=True)
    ap.add_argument("--tipo", required=True, choices=list(TIPOS) + [t.lower() for t in TIPOS])
    ap.add_argument("--destino", required=True)
    ap.add_argument("--color", help="#RRGGBB; sin color = identidad original")
    ap.add_argument("--codex", action="store_true")
    ap.add_argument("--autor", default=ajustes.get("autor", ""))
    ap.add_argument("--github", default=ajustes.get("github", ""))
    a = ap.parse_args(argv)
    try:
        r = crear_proyecto(Opciones(a.nombre, a.tipo, Path(a.destino), a.color, a.codex, autor=a.autor, github=a.github))
    except ErrorProyecto as exc:
        print(f"Error: {exc}")
        return 1
    print(f"Proyecto creado: {r.ruta} ({r.archivos} archivos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
