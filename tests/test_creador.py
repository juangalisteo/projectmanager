"""Pruebas de creador.py. Se ejecutan con:  python -m unittest discover tests"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "APP"))
import creador  # noqa: E402

LEFTOVER = re.compile(r"\[(PROYECTO|CARPETA|RUTA|TIPO|COLOR|FECHA|FECHA_ISO|AUTOR|GITHUB)\]|\[\[(SI|NO|FIN)")


def make(tmp, **kw):
    base = dict(nombre="Proyecto de prueba", tipo="DOCUMENTO", destino=Path(tmp), autor="Autor", github="@autor")
    base.update(kw)
    return creador.crear_proyecto(creador.Opciones(**base))


def text_files(folder):
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json", ".txt", ".gitignore", ""}:
            yield path


class NameTests(unittest.TestCase):
    def test_folder_name(self):
        self.assertEqual(creador.nombre_carpeta("Mis apuntes técnicos"), "MIS_APUNTES_TECNICOS")
        self.assertEqual(creador.nombre_carpeta("  España: año 2026!  "), "ESPANA_ANO_2026")
        self.assertEqual(creador.nombre_carpeta("???"), "")

    def test_color(self):
        self.assertEqual(creador.color_valido("2e7d6b"), "#2E7D6B")
        with self.assertRaises(creador.ErrorProyecto):
            creador.color_valido("verde")

    def test_random_colour(self):
        """Random colours are valid and always give a readable palette."""
        import random
        rng = random.Random(42)
        for _ in range(200):
            color = creador.color_aleatorio(rng)
            self.assertEqual(creador.color_valido(color), color)
            self.assertTrue(creador.paleta_legible(creador.paleta(color)), color)
        self.assertEqual(creador.paleta(None)["accent"], creador.ORIGINAL_COLOR)

    def test_blocks(self):
        text = "A\n[[SI DOCUMENTO]]\nB\n[[FIN]]\nC [[SI PROGRAMA]]x[[FIN]]\n[[NO PROGRAMA]]\nD\n[[FIN]]\n"
        self.assertEqual(creador.resolver_bloques(text, {"DOCUMENTO"}), "A\nB\nC \nD\n")
        self.assertEqual(creador.resolver_bloques(text, {"PROGRAMA"}), "A\nC x\n")


class CreateTests(unittest.TestCase):
    def check_clean(self, folder):
        for path in text_files(folder):
            if "04_STYLE_MANUAL" in path.parts or path.name in {"LICENSE", "01_WRITING_RULES.md", "02_NAMING.md", "02_WRITING_RULES.md",
                                                                 "03_AI_PATTERNS.md", "01_NAMING.md"}:
                continue  # copied as they are: they talk about placeholders on purpose
            self.assertIsNone(LEFTOVER.search(path.read_text(encoding="utf-8")), path)

    def test_document(self):
        """Documento: rules, card, plan, Claude's log, work folders and the style manual."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, color="#2E7D6B")
            files = sorted(p.relative_to(r.ruta).as_posix() for p in r.ruta.rglob("*")
                           if p.is_file() and "04_STYLE_MANUAL" not in p.parts)
            self.assertEqual(files, ["00_CONFIG/00_PROJECT_CONFIG.json", "00_CONFIG/01_WRITING_RULES.md",
                                     "00_CONFIG/02_NAMING.md", "00_INICIO_CHAT.md", "AGENTS.md",
                                     "AGENT_AI/CLAUDE/BITACORA.md", "AGENT_AI/ESTADO.md",
                                     "AGENT_AI/TRABAJO/PLAN.md", "README.md"])
            for folder in ["01_MATERIALS", "02_WORK", "03_EXPORT"]:
                self.assertTrue((r.ruta / folder).is_dir(), folder)
            for rel in ["README.md", "00_MANUAL_DE_ESTILO.pdf", "01_MANUAL_DE_ESTILO.md",
                        "02_PROMPTS/01_APLICAR_MANUAL.md", "03_SOURCE/02_BUILD_MANUAL.py"]:
                self.assertTrue((r.ruta / "04_STYLE_MANUAL" / rel).exists(), rel)
            self.assertFalse((r.ruta / "AGENT_AI/CODEX").exists())
            config = json.loads((r.ruta / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
            self.assertEqual(config["identity"]["colors"]["accent"], "#2E7D6B")
            self.assertEqual(config["proyecto"]["ruta"], str(r.ruta))
            self.assertTrue((r.ruta / config["documento"]["manual"]).exists())
            self.assertIn(str(r.ruta), (r.ruta / "00_INICIO_CHAT.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_document_general_manual(self):
        """Star off (default): the project gets the general manual, without the images part."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp)
            manual = r.ruta / "04_STYLE_MANUAL"
            self.assertNotIn("## 11 / Imágenes", (manual / "01_MANUAL_DE_ESTILO.md").read_text(encoding="utf-8"))
            self.assertFalse((manual / "02_PROMPTS/03_CREAR_IMAGEN_SVG.md").exists())
            self.assertFalse((manual / "03_SOURCE/05_IMAGE_KIT").exists())
            config = json.loads((r.ruta / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
            self.assertEqual(config["documento"]["manual_version"], "general")
            self.assertFalse(config["modulos"]["imagenes"])
            self.assertNotIn("03_CREAR_IMAGEN_SVG", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))

    def test_document_images_manual(self):
        """Star on: one manual, the «general + images» version, with its prompts, fonts and image kit."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, color="#2E7D6B", imagenes=True)
            manual = r.ruta / "04_STYLE_MANUAL"
            text = (manual / "01_MANUAL_DE_ESTILO.md").read_text(encoding="utf-8")
            self.assertIn("## 11 / Imágenes", text)
            self.assertIn("## 16 / Imágenes: generar con IA", text)
            for rel in ["00_MANUAL_DE_ESTILO.pdf", "02_PROMPTS/01_APLICAR_MANUAL.md", "02_PROMPTS/02_REVISION_ENTREGA.md",
                        "02_PROMPTS/03_CREAR_IMAGEN_SVG.md", "02_PROMPTS/04_GENERADOR_IMAGENES.md",
                        "02_PROMPTS/05_REVISION_IMAGEN.md", "03_SOURCE/01_PALETTE.py", "03_SOURCE/02_BUILD_MANUAL.py",
                        "03_SOURCE/03_FONTS/FreeSerifBold.ttf", "03_SOURCE/03_FONTS/Inter-Bold.ttf",
                        "03_SOURCE/04_IMAGES/02_STYLE_MODEL.png", "03_SOURCE/05_IMAGE_KIT/01_BASE_PIECES_VECTOR.svg",
                        "03_SOURCE/05_IMAGE_KIT/07_BASE_SHEET_16X9_VECTOR.svg"]:
                self.assertTrue((manual / rel).exists(), rel)
            self.assertEqual(len(list(manual.glob("*.pdf"))), 1)  # one manual only
            config = json.loads((r.ruta / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
            self.assertEqual(config["documento"]["manual_version"], "general_imagenes")
            self.assertTrue(config["modulos"]["imagenes"])
            self.assertEqual(config["identity"]["colors"]["accent"], "#2E7D6B")
            self.assertIn("03_CREAR_IMAGEN_SVG", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_images_manual_keeps_general(self):
        """The «general + images» manual starts with the whole general manual, unchanged."""
        modules = creador.PLANTILLA / "00_MODULOS"
        general = (modules / "MANUAL/01_MANUAL_DE_ESTILO.md").read_text(encoding="utf-8").rstrip()
        images = (modules / "MANUAL_IMAGENES/01_MANUAL_DE_ESTILO.md").read_text(encoding="utf-8")
        closing = general.splitlines()[-1]
        self.assertTrue(closing.startswith("@@closing_page"))
        self.assertTrue(images.startswith(general[: -len(closing)].rstrip()))
        # each manual has its own final page; the images one ends with the square, compass and G
        self.assertTrue(images.rstrip().splitlines()[-1].startswith("@@closing_page"))
        self.assertTrue(images.rstrip().endswith("| escuadra"))
        # the same generator builds both manuals
        self.assertEqual((modules / "MANUAL/03_SOURCE/02_BUILD_MANUAL.py").read_bytes(),
                         (modules / "MANUAL_IMAGENES/03_SOURCE/02_BUILD_MANUAL.py").read_bytes())

    def test_colour_only_for_document(self):
        """Proyecto and General ignore the colour and the star: default palette, no style manual."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, tipo="PROYECTO", color="#2E7D6B", imagenes=True)
            config = json.loads((r.ruta / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
            self.assertEqual(config["identity"]["palette_mode"], "identidad_original")
            self.assertEqual(config["identity"]["primary_color"], creador.ORIGINAL_COLOR)
            self.assertFalse(config["modulos"]["imagenes"])
            self.assertFalse((r.ruta / "04_STYLE_MANUAL").exists())
            g = make(tmp, nombre="General de prueba", tipo="GENERAL", color="#2E7D6B", imagenes=True)
            self.assertFalse((g.ruta / "04_STYLE_MANUAL").exists())
            self.assertNotIn("#2E7D6B", "".join(p.read_text(encoding="utf-8") for p in text_files(g.ruta)))

    def test_document_with_chatgpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, codex=True)
            for rel in ["AGENT_AI/CODEX/AGENT.md", "AGENT_AI/CODEX/BITACORA.md", "AGENT_AI/CLAUDE/BITACORA.md"]:
                self.assertTrue((r.ruta / rel).exists(), rel)
            self.assertIn("Codex", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_proyecto(self):
        """Proyecto: advisor + executor, Git files, tests and the GPL-3.0 licence."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, tipo="PROYECTO")
            files = sorted(p.relative_to(r.ruta).as_posix() for p in r.ruta.rglob("*") if p.is_file())
            self.assertEqual(files, [".gitignore", "00_CONFIG/00_PROJECT_CONFIG.json", "00_CONFIG/01_WRITING_RULES.md",
                                     "00_CONFIG/02_NAMING.md", "00_CONFIG/03_PROMPTS_GUIDE.md", "00_INICIO_CHAT.md",
                                     "AGENTS.md", "AGENT_AI/CLAUDE/AGENT.md", "AGENT_AI/CLAUDE/BITACORA.md",
                                     "AGENT_AI/CLAUDE/PUENTE.md", "AGENT_AI/ESTADO.md", "AGENT_AI/LEEME.md",
                                     "AGENT_AI/TRABAJO/IDEAS_FUTURAS.md", "AGENT_AI/TRABAJO/PLAN.md",
                                     "CHANGELOG.md", "CLAUDE.md", "LICENSE", "README.md"])
            for folder in ["docs", "tests", "AGENT_AI/CLAUDE/REPORTS"]:
                self.assertTrue((r.ruta / folder).is_dir(), folder)
            self.assertIn("GNU GENERAL PUBLIC LICENSE", (r.ruta / "LICENSE").read_text(encoding="utf-8"))
            self.assertIn("Version 3", (r.ruta / "LICENSE").read_text(encoding="utf-8"))
            for private in ["AGENT_AI/", "00_CONFIG/", "00_INICIO_CHAT.md"]:
                self.assertIn(private, (r.ruta / ".gitignore").read_text(encoding="utf-8"))
            config = json.loads((r.ruta / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
            self.assertEqual(config["proyecto"]["licencia"], "GPL-3.0")
            self.assertEqual(config["identity"]["palette_mode"], "identidad_original")
            self.assertNotIn("Codex", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_proyecto_with_chatgpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, tipo="PROYECTO", codex=True)
            for rel in ["AGENT_AI/CODEX/AGENT.md", "AGENT_AI/CODEX/BITACORA.md", "AGENT_AI/CODEX/PUENTE.md"]:
                self.assertTrue((r.ruta / rel).exists(), rel)
            self.assertTrue((r.ruta / "AGENT_AI/CODEX/REPORTS").is_dir())
            self.assertIn("Codex", (r.ruta / "AGENT_AI/LEEME.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_general(self):
        """General is the minimum: exactly these files and the empty work folder."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, tipo="GENERAL")
            files = sorted(p.relative_to(r.ruta).as_posix() for p in r.ruta.rglob("*") if p.is_file())
            self.assertEqual(files, ["00_CONFIG/01_WRITING_RULES.md", "00_CONFIG/02_NAMING.md", "00_INICIO_CHAT.md", "AGENTS.md",
                                     "AGENT_AI/ESTADO.md", "README.md"])
            self.assertTrue((r.ruta / "01_WORK").is_dir())
            self.assertIn("01_WRITING_RULES.md", (r.ruta / "00_INICIO_CHAT.md").read_text(encoding="utf-8"))
            self.assertNotIn("Codex", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn(str(r.ruta), (r.ruta / "00_INICIO_CHAT.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_general_with_chatgpt(self):
        """With ChatGPT on, General adds one log per agent and Codex's own rules."""
        with tempfile.TemporaryDirectory() as tmp:
            r = make(tmp, tipo="GENERAL", codex=True)
            for rel in ["AGENT_AI/CLAUDE/BITACORA.md", "AGENT_AI/CODEX/AGENT.md", "AGENT_AI/CODEX/BITACORA.md"]:
                self.assertTrue((r.ruta / rel).exists(), rel)
            self.assertIn("Codex", (r.ruta / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("Con Codex", (r.ruta / "README.md").read_text(encoding="utf-8"))
            self.check_clean(r.ruta)

    def test_start_prompt(self):
        """00_INICIO_CHAT.md is only the start prompt: no headings, no boxes, no guide, no Codex.
        It is the same with ChatGPT on or off, and it carries the project's path."""
        for tipo in creador.TIPOS:
            prompts = []
            for codex in (False, True):
                with tempfile.TemporaryDirectory() as tmp:
                    r = make(tmp, tipo=tipo, codex=codex)
                    text = (r.ruta / "00_INICIO_CHAT.md").read_text(encoding="utf-8")
                    self.assertTrue(text.startswith("Hola."), tipo)
                    self.assertIn(str(r.ruta), text)
                    self.assertIn("Pídeme acceso a la carpeta", text)
                    self.assertIn("Qué hacer ahora", text)
                    self.assertIn("Antes de cambiar nada", text)
                    for banned in ("```", "Codex", "ChatGPT", "Copia el prompt", "\n#"):
                        self.assertNotIn(banned, text, f"{tipo}: {banned}")
                    prompts.append(text.replace(str(r.ruta), "RUTA"))
            self.assertEqual(prompts[0], prompts[1], tipo)

    def test_update_route(self):
        """«Actualizar ruta»: after moving (and renaming) a project, its new path is written in the
        prompt, the README and the card, and the old one is gone. A second run changes nothing."""
        import shutil
        for tipo in creador.TIPOS:
            with tempfile.TemporaryDirectory() as tmp:
                r = make(tmp, tipo=tipo, codex=True)
                old = str(r.ruta)
                moved = Path(tmp) / "OTRO_SITIO" / "NUEVO_NOMBRE"
                moved.parent.mkdir()
                shutil.move(old, moved)
                result = creador.actualizar_ruta(moved)
                new = str(moved.resolve())
                self.assertEqual(result.viejas, [old], tipo)
                self.assertIn("00_INICIO_CHAT.md", result.archivos)
                for name in ["00_INICIO_CHAT.md", "README.md"]:
                    text = (moved / name).read_text(encoding="utf-8")
                    self.assertNotIn(old, text, f"{tipo}: {name}")
                self.assertIn(new, (moved / "00_INICIO_CHAT.md").read_text(encoding="utf-8"))
                if tipo != "PROYECTO":  # the Proyecto README is the GitHub page: it has no path
                    self.assertIn(new, (moved / "README.md").read_text(encoding="utf-8"))
                if tipo in creador.CON_FICHA:
                    config = json.loads((moved / "00_CONFIG/00_PROJECT_CONFIG.json").read_text(encoding="utf-8"))
                    self.assertEqual(config["proyecto"]["ruta"], new)
                    self.assertEqual(config["proyecto"]["carpeta"], "NUEVO_NOMBRE")
                self.assertEqual(creador.actualizar_ruta(moved).archivos, [], tipo)  # already up to date
                self.check_clean(moved)

    def test_update_route_errors(self):
        """A folder that is not a Project Manager project, or does not exist, is not touched."""
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / "CARPETA_CUALQUIERA"
            other.mkdir()
            (other / "README.md").write_text("Hola", encoding="utf-8")
            with self.assertRaises(creador.ErrorProyecto):
                creador.actualizar_ruta(other)
            self.assertEqual((other / "README.md").read_text(encoding="utf-8"), "Hola")
            with self.assertRaises(creador.ErrorProyecto):
                creador.actualizar_ruta(Path(tmp) / "NO_EXISTE")

    def test_errors_leave_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            make(tmp)
            with self.assertRaises(creador.ErrorProyecto):
                make(tmp)  # same name again
            with self.assertRaises(creador.ErrorProyecto):
                make(tmp, nombre="Otro", color="rojo")
            with self.assertRaises(creador.ErrorProyecto):
                make(tmp, destino=Path(tmp) / "no_existe")
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["PROYECTO_DE_PRUEBA"])

    def test_missing_template_part(self):
        """If a PLANTILLA folder was renamed, the message says which one, and nothing is created."""
        original = creador.PIEZAS
        creador.PIEZAS = original + [("99_NO_EXISTE", "", False, lambda o: True)]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(creador.ErrorProyecto) as ctx:
                    make(tmp)
                self.assertIn("99_NO_EXISTE", str(ctx.exception))
                self.assertEqual(list(Path(tmp).iterdir()), [])
        finally:
            creador.PIEZAS = original


if __name__ == "__main__":
    unittest.main()
