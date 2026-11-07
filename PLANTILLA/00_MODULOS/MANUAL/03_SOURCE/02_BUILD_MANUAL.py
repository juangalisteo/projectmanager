"""Generador del MANUAL DE ESTILO Y MAQUETACIÓN.

Desde la carpeta del manual (04_STYLE_MANUAL en cada proyecto):

    python 03_SOURCE/02_BUILD_MANUAL.py

Lee 01_MANUAL_DE_ESTILO.md y 03_SOURCE/00_MANUAL_CONFIG.json y escribe
00_MANUAL_DE_ESTILO.pdf. Necesita Python 3 y reportlab
(pip install reportlab). No descarga nada ni usa servicios externos.
"""
from pathlib import Path
import json, re, html, argparse, importlib.util, math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CFG = json.loads((HERE / '00_MANUAL_CONFIG.json').read_text(encoding='utf-8'))
LAY = CFG['layout']
spec = importlib.util.spec_from_file_location('palette', HERE / '01_PALETTE.py')
PAL = importlib.util.module_from_spec(spec); spec.loader.exec_module(PAL)

for n, f in [('R', 'Inter-Regular.ttf'), ('M', 'Inter-Medium.ttf'), ('S', 'Inter-SemiBold.ttf'), ('B', 'Inter-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(HERE / '03_FONTS' / f)))
pdfmetrics.registerFontFamily('R', normal='R', bold='B', italic='R', boldItalic='B')
pdfmetrics.registerFontFamily('M', normal='M', bold='B', italic='M', boldItalic='B')
pdfmetrics.registerFontFamily('S', normal='S', bold='B', italic='S', boldItalic='B')

W, H = 595.276, 841.89
M = LAY['margin_mm'] * 72 / 25.4
CW = W - 2 * M
BOTTOM = H - 52
COL = CFG['identity']['colors']
C = {k: HexColor(v) for k, v in COL.items()}
INK, GOLD, ACC, SOFT, MUTED, BORDER = C['text'], C['accent'], C['accent_text'], C['accent_surface'], C['muted'], C['border']
WHITE = white
NEUTRAL = C['row']
GOLD_DARK = C['accent_on_dark']
IMG = HERE / '04_IMAGES'
PHOTO = IMG / '00_STUDIO_PHOTO.png'
COVER = ROOT / CFG['cover']['image_path']
BLOCK_ICONS = ['layers', 'document', 'palette', 'heading', 'layout', 'table', 'card', 'image', 'flow', 'eye']
CALLOUT_ICON = {'nota': 'info', 'definicion': 'book', 'advertencia': 'warning', 'ejemplo': 'bulb', 'comprobar': 'check'}


# ---------------------------------------------------------------- contenido
def parse(md):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    blocks = []
    for line in md.splitlines():
        m = re.match(r'^## (\d{2}) / (.+)$', line)
        if m:
            blocks.append({'code': m[1], 'name': m[2].strip(), 'opening': None, 'intro': [], 'sections': []}); continue
        if not blocks:
            continue
        b = blocks[-1]
        if line.startswith('!apertura '):
            b['opening'] = [x.strip() for x in line[10:].split('||')]; continue
        m = re.match(r'^### (\d+)\. (.+)$', line)
        if m:
            b['sections'].append({'num': int(m[1]), 'title': m[2].strip(), 'head': None, 'lines': []}); continue
        if line.startswith('= ') and b['sections'] and b['sections'][-1]['head'] is None:
            b['sections'][-1]['head'] = [x.strip() for x in line[2:].split('|')]; continue
        (b['sections'][-1]['lines'] if b['sections'] else b['intro']).append(line)
    return blocks


def number_refs(md):
    figs, tabs = {}, {}
    for line in re.sub(r'<!--.*?-->', '', md, flags=re.S).splitlines():
        for kind, key in re.findall(r'^(?:@@\w+|Tabla:)\s+\{(fig|tab):([\w-]+)\}', line):
            d = figs if kind == 'fig' else tabs
            if key in d:
                raise ValueError(f'Etiqueta repetida: {kind}:{key}')
            d[key] = len(d) + 1
    return figs, tabs


RAW = (ROOT / CFG['document']['content']).read_text(encoding='utf-8')
FIGS, TABS = number_refs(RAW)
for _kind, _d in (('fig', FIGS), ('tab', TABS)):
    for _k in _d:
        if len(re.findall(r'\{' + _kind + ':' + _k + r'\}', RAW)) < 2:
            raise ValueError(f'{_kind}:{_k} no se cita en el texto. Toda figura y tabla se cita.')


def resolve(text):
    def rep(m):
        d = FIGS if m[1] == 'fig' else TABS
        if m[2] not in d:
            raise ValueError(f'Referencia sin destino: {m[0]}')
        return ('figura ' if m[1] == 'fig' else 'tabla ') + str(d[m[2]])
    return re.sub(r'\{(fig|tab):([\w-]+)\}', rep, text)


BLOCKS = parse(RAW)
DEBUG = False


def markup(t):
    t = html.escape(resolve(t)).replace('\n', '<br/>')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', lambda m: f'<font name="M" size="8.8" color="{COL["accent_text"]}">{m[1]}</font>', t)
    return t


def bind(text):
    """Une las dos últimas palabras para que ningún párrafo acabe con una palabra sola."""
    if len(text.split()) < 5:
        return text.strip()  # en textos de pocas palabras la unión rompería palabras largas
    return re.sub(r'(\S+)\s+(\S+)$', lambda m: m[1] + ' ' + m[2], text.strip())


# ---------------------------------------------------------------- página
class Book:
    def __init__(self, path, pages=None):
        self.c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
        self.c.setTitle(CFG['document']['pdf_title']); self.c.setAuthor(CFG['document']['author'])
        self.c.setSubject('Normas de redacción, diseño y maquetación de documentos')
        self.c._doc.Catalog.Lang = PDFString(CFG['document']['language'])
        self.page = 0; self.y = 0; self.pages = pages or {}; self.found = {}; self.log = []
        self.pending = []; self.in_table = False; self.flushing = False

    # primitivas (del generador original)
    def rect(self, x, t, w, h, fill=WHITE, stroke=None, r=10, shadow=False, width=.6):
        c = self.c
        if shadow:
            for j in range(5, 0, -1):
                c.saveState(); c.setFillColor(INK); c.setFillAlpha(.014 * j)
                c.roundRect(x - j * .4, H - t - h - j * 1.4, w + j * .8, h + j * .4, r + j * .8, fill=1, stroke=0); c.restoreState()
        c.saveState()
        if fill is not None: c.setFillColor(fill)
        if stroke: c.setStrokeColor(stroke); c.setLineWidth(width)
        c.roundRect(x, H - t - h, w, h, r, fill=1 if fill is not None else 0, stroke=bool(stroke)); c.restoreState()

    def line(self, x, t, xx, tt, color=BORDER, width=.6, dash=None):
        c = self.c; c.saveState(); c.setStrokeColor(color); c.setLineWidth(width); c.setLineCap(1)
        if dash: c.setDash(*dash)
        c.line(x, H - t, xx, H - tt); c.restoreState()

    def txt(self, x, t, text, size=10, font='R', color=INK, align='left'):
        c = self.c; c.setFillColor(color); c.setFont(font, size)
        f = c.drawString if align == 'left' else c.drawRightString if align == 'right' else c.drawCentredString
        f(x, H - t - size * .8, text)

    def para(self, x, t, text, w=CW, size=10.5, lead=15, color=INK, font='R', align=None, keep=True):
        alignment = align if align is not None else (4 if font == 'R' and w >= CW * .6 else 0)
        sty = ParagraphStyle('p', fontName=font, fontSize=size, leading=lead, textColor=color, alignment=alignment,
                             allowWidows=0, allowOrphans=0, splitLongWords=True)
        p = Paragraph(markup(bind(text) if keep else text), sty); _, h = p.wrap(w, 3000); p.drawOn(self.c, x, H - t - h)
        return h

    def height(self, text, w=CW, size=10.5, lead=15, font='R'):
        p = Paragraph(markup(bind(text)), ParagraphStyle('h', fontName=font, fontSize=size, leading=lead))
        return p.wrap(w, 3000)[1]

    def circle(self, x, t, r, fill, stroke=None, width=1):
        c = self.c; c.saveState()
        if fill is not None: c.setFillColor(fill)
        if stroke: c.setStrokeColor(stroke); c.setLineWidth(width)
        c.circle(x, H - t, r, fill=1 if fill is not None else 0, stroke=bool(stroke)); c.restoreState()

    def arrow(self, x, t, xx, tt, color=INK, width=1.2, head=5):
        self.line(x, t, xx, tt, color, width)
        a = math.atan2(-(tt - t), xx - x); c = self.c
        p = c.beginPath(); p.moveTo(xx, H - tt)
        p.lineTo(xx - head * math.cos(a - .45), H - tt - head * math.sin(a - .45))
        p.lineTo(xx - head * math.cos(a + .45), H - tt - head * math.sin(a + .45)); p.close()
        c.saveState(); c.setFillColor(color); c.drawPath(p, fill=1, stroke=0); c.restoreState()

    def icon(self, kind, x, t, s=20, color=ACC):
        c = self.c; c.saveState(); c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(s * .065); c.setLineCap(1); c.setLineJoin(1)
        def l(a, b, d, e): c.line(x + a * s, H - (t + b * s), x + d * s, H - (t + e * s))
        def rr(a, b, w, h, r=.08): c.roundRect(x + a * s, H - t - (b + h) * s, w * s, h * s, r * s, fill=0, stroke=1)
        def ci(a, b, r, fill=0): c.circle(x + a * s, H - (t + b * s), r * s, stroke=1 - fill, fill=fill)
        def poly(pts, close=True):
            p = c.beginPath(); p.moveTo(x + pts[0][0] * s, H - (t + pts[0][1] * s))
            for a, b in pts[1:]: p.lineTo(x + a * s, H - (t + b * s))
            if close: p.close()
            c.drawPath(p, stroke=1, fill=0)
        if kind == 'grid':
            for a, b in [(.12, .12), (.58, .12), (.12, .58), (.58, .58)]: rr(a, b, .3, .3, .065)
        elif kind == 'layers':
            for off in [0, .23, .46]: poly([(.1, .27 + off), (.5, .08 + off), (.9, .27 + off), (.5, .46 + off)])
        elif kind == 'document':
            rr(.22, .08, .56, .84)
            for yy in [.35, .5, .65]: l(.34, yy, .66, yy)
        elif kind == 'palette':
            for a, b in [(.23, .25), (.72, .25), (.23, .72), (.72, .72)]: ci(a, b, .15)
        elif kind == 'flow':
            rr(.03, .15, .3, .24, .04); rr(.67, .15, .3, .24, .04); rr(.35, .67, .3, .24, .04); l(.33, .27, .67, .27); l(.5, .27, .5, .67)
        elif kind == 'check': l(.18, .52, .41, .75); l(.41, .75, .86, .22)
        elif kind == 'arrow': l(.1, .5, .9, .5); l(.64, .23, .9, .5); l(.64, .77, .9, .5)
        elif kind == 'quote':
            rr(.12, .18, .27, .39, .05); rr(.6, .18, .27, .39, .05); l(.39, .57, .25, .82); l(.87, .57, .73, .82)
        elif kind == 'eye':
            p = c.beginPath(); p.moveTo(x + .05 * s, H - (t + .5 * s))
            p.curveTo(x + .3 * s, H - (t + .08 * s), x + .7 * s, H - (t + .08 * s), x + .95 * s, H - (t + .5 * s))
            p.curveTo(x + .7 * s, H - (t + .92 * s), x + .3 * s, H - (t + .92 * s), x + .05 * s, H - (t + .5 * s))
            c.drawPath(p, stroke=1, fill=0); ci(.5, .5, .13)
        elif kind == 'info':
            ci(.5, .5, .42); l(.5, .45, .5, .72); ci(.5, .3, .035, 1)
        elif kind == 'warning':
            poly([(.5, .1), (.92, .86), (.08, .86)]); l(.5, .38, .5, .6); ci(.5, .73, .035, 1)
        elif kind == 'book':
            poly([(.5, .25), (.5, .85), (.08, .78), (.08, .18)]); poly([(.5, .25), (.92, .18), (.92, .78), (.5, .85)])
        elif kind == 'bulb':
            ci(.5, .4, .28); l(.38, .72, .62, .72); l(.41, .84, .59, .84); l(.4, .64, .4, .72); l(.6, .64, .6, .72)
        elif kind == 'heading':
            l(.12, .22, .88, .22); l(.12, .45, .7, .45); l(.12, .65, .55, .65); l(.12, .82, .45, .82)
        elif kind == 'layout':
            rr(.12, .08, .76, .84); l(.5, .2, .5, .8); l(.22, .2, .78, .2)
        elif kind == 'table':
            rr(.08, .16, .84, .68); l(.08, .38, .92, .38); l(.08, .6, .92, .6); l(.4, .16, .4, .84)
        elif kind == 'card':
            rr(.06, .2, .4, .6, .1); rr(.54, .2, .4, .6, .1); l(.14, .34, .26, .34); l(.62, .34, .74, .34)
        elif kind == 'image':
            rr(.08, .16, .84, .68, .1); poly([(.16, .74), (.4, .46), (.58, .64), (.68, .54), (.84, .74)], False); ci(.68, .34, .07)
        elif kind == 'link':
            rr(.08, .36, .46, .28, .14); rr(.46, .36, .46, .28, .14)
        elif kind == 'search':
            ci(.42, .42, .26); l(.62, .62, .88, .88)
        else:
            rr(.1, .1, .8, .8, .18); l(.3, .5, .7, .5); l(.5, .3, .5, .7)
        c.restoreState()

    def glow_grid(self, strong=False, glow=True):
        c = self.c
        if glow:
            c.saveState(); p = c.beginPath(); p.rect(0, 0, W, H); c.clipPath(p, stroke=0)
            c.radialGradient(W + 20, H - 35, 340, [C['gradient_strong'] if strong else C['gradient_soft'], WHITE], positions=[0, 1])
            c.restoreState()
        step = LAY['grid_step_pt']
        for xx in range(0, int(W) + 1, step): self.line(xx, 0, xx, H, C['grid_line'], .24)
        for yy in range(0, int(H) + 1, step): self.line(0, yy, W, yy, C['grid_line'], .24)

    def page_start(self, grid=False, strong=False, glow=None, right=None):
        if self.page: self.c.showPage()
        self.page += 1; self.y = LAY['content_top_pt']
        self.c.setFillColor(WHITE); self.c.rect(0, 0, W, H, fill=1, stroke=0)
        if grid: self.glow_grid(strong, glow if glow is not None else True)
        hd = CFG['header']
        self.rect(M, 25, 24, 24, INK, r=7)
        if hd.get('logo_path'):
            self.c.drawImage(str(ROOT / hd['logo_path']), M + 3, H - 46, 18, 18, preserveAspectRatio=True, anchor='c', mask='auto')
        else:
            self.icon(hd.get('icon', 'grid'), M + 5, 30, 14, GOLD)
        self.txt(M + 32, 32, hd['name'].upper(), 9.2, 'S')
        self.txt(W - M, 34, right or hd['right_label'], 7.4, 'S', ACC, 'right')
        self.line(M, LAY['header_rule_top_pt'], W - M, LAY['header_rule_top_pt'])
        self.line(M, H - LAY['footer_rule_from_bottom_pt'], W - M, H - LAY['footer_rule_from_bottom_pt'])
        self.txt(W - M, H - 24, f'{self.page:02d}', 8, 'S', INK, 'right')
        if self.pending and not self.in_table and not self.flushing:
            self.flushing = True
            while self.pending: place_figure(self, *self.pending.pop(0))
            self.flushing = False

    def space(self):
        return BOTTOM - self.y

    def ensure(self, h):
        if self.y + h > BOTTOM:
            self.page_start(); return True
        return False

    def label(self, text, x=M, t=None, color=ACC):
        t = self.y if t is None else t
        self.line(x, t + 5, x + 15, t + 5, color, 1.4)
        self.txt(x + 21, t, text.upper(), 8, 'S', color)

    def title(self, first, second, t, size=28):
        a = self.para(M, t, first, CW, size, size * 1.08, INK, 'B', keep=False)
        b = self.para(M, t + a, second, CW, size, size * 1.08, ACC, 'B', keep=False)
        return t + a + b

    def caption(self, kind, n, text, x=M, w=CW, t=None):
        t = self.y if t is None else t
        word = 'Figura' if kind == 'fig' else 'Tabla'
        return self.para(x, t, f'**{word} {n}.** {text}', w, 8.5, 11.5, MUTED, 'M', align=0)

    def caption_h(self, text, w=CW):
        return self.height(f'**Figura 00.** {text}', w, 8.5, 11.5, 'M')

    def photo(self, x, t, w, h, overlay=False, focus_x=.5, focus_y=.5, image=PHOTO, r=12):
        c = self.c; c.saveState(); p = c.beginPath(); p.roundRect(x, H - t - h, w, h, r); c.clipPath(p, stroke=0)
        iw, ih = ImageReader(str(image)).getSize(); scale = max(w / iw, h / ih); dw, dh = iw * scale, ih * scale
        c.drawImage(str(image), x + (w - dw) * focus_x, H - t - h + (h - dh) * (1 - focus_y), dw, dh, mask='auto')
        if overlay: c.setFillColor(INK); c.setFillAlpha(.78); c.rect(x, H - t - h, w, h, fill=1, stroke=0)
        c.restoreState()

    def pill(self, x, t, label, fill=WHITE, ink=INK, icon=None, size=8.2, shadow=True):
        w = pdfmetrics.stringWidth(label, 'S', size) + 24 + (17 if icon else 0)
        self.rect(x, t, w, 25, fill, BORDER, r=9, shadow=shadow)
        if icon: self.icon(icon, x + 8, t + 7, 11, ACC)
        self.txt(x + 10 + (17 if icon else 0), t + 8, label, size, 'S', ink)
        return w

    def callout(self, kind, title, body, x=M, w=CW):
        h = max(58, self.height(body, w - 52, 9.8, 14) + 37)
        if self.ensure(h + 12): pass
        t = self.y
        self.rect(x, t, w, h, SOFT if kind == 'comprobar' else NEUTRAL, r=10)
        self.line(x, t + 10, x, t + h - 10, GOLD, 2.2)
        self.icon(CALLOUT_ICON.get(kind, 'info'), x + 13, t + 14, 15, ACC)
        self.txt(x + 39, t + 14, title.upper(), 7.8, 'S', ACC)
        self.para(x + 39, t + 29, body, w - 52, 9.8, 14, INK, 'R', align=0)
        self.y += h + 12

    def quote(self, text, who):
        h1 = self.height('«' + text + '»', CW - 40, 12.5, 18, 'M'); h = h1 + 30
        self.ensure(h + 14); t = self.y
        self.line(M + 4, t + 2, M + 4, t + h - 4, GOLD, 2.4)
        self.para(M + 22, t, '«' + text + '»', CW - 40, 12.5, 18, INK, 'M', align=0)
        self.txt(M + 22, t + h1 + 9, '— ' + who, 8.5, 'M', MUTED)
        self.y += h + 14

    def bullet(self, text):
        h = self.height(text, CW - 18); self.ensure(h + 6)
        self.circle(M + 4, self.y + 7.5, 2.1, GOLD)
        self.para(M + 16, self.y, text, CW - 16, 10.5, 15, align=0); self.y += h + 5

    def numbered(self, number, text):
        h = self.height(text, CW - 30, 10.3, 14.8); height = max(h, 19) + 10
        self.ensure(height)
        self.circle(M + 9, self.y + 9, 9, INK); self.txt(M + 9, self.y + 5, number, 7, 'S', WHITE, 'center')
        self.para(M + 30, self.y + 1, text, CW - 30, 10.3, 14.8, align=0); self.y += height

    # ---------------------------------------------------------- tablas
    def table(self, rows, number, caption, cell_fns=None, numeric=None, widths=None):
        head, body = rows[0], rows[1:]
        ncol = len(head)
        is_num = numeric or [all(re.fullmatch(r'[-−]?[\d.]+(,\d+)?(:1)?', r[k].strip()) for r in body) for k in range(ncol)]
        widths = widths or col_widths(rows, is_num)
        fsz, lead, pad = 9.4, 13.2, 9
        def row_h(r, font='R'):
            return max(self.height(v if not (cell_fns and cell_fns.get(k)) else 'x', widths[k] - 2 * pad, fsz, lead, 'S' if font == 'S' or k == 0 else 'R') for k, v in enumerate(r)) + 2 * pad
        hh = max(self.height(v, widths[k] - 2 * pad, 8.8, 11.6, 'S') for k, v in enumerate(head)) + 2 * pad
        hs = [max(24, row_h(r)) for r in body]
        cap = f'{caption}'
        caph = self.height(f'**Tabla 0.** {cap}', CW, 8.5, 11.5, 'M') + 7
        # plan de páginas: nunca una fila sola en una página
        def plan(start_y):
            breaks, y, first = [], start_y + caph + hh, 0
            for i, h in enumerate(hs):
                if y + h > BOTTOM:
                    breaks.append(i); y = LAY['content_top_pt'] + caph + hh
                y += h
            for j, bi in enumerate(breaks):
                nxt = breaks[j + 1] if j + 1 < len(breaks) else len(hs)
                if nxt - bi == 1 and bi > 1: breaks[j] = bi - 1
                if bi < 2: breaks[j] = max(bi, 0)
            return breaks
        if self.y + caph + hh + sum(hs[:2]) > BOTTOM: self.page_start()
        breaks = plan(self.y)
        if breaks and breaks[0] < 2:
            self.page_start(); breaks = plan(self.y)
        self.in_table = True
        def draw_head(cont):
            self.caption('tab', number, cap + (' (continuación)' if cont else ''))
            self.y += caph
            self.rect(M, self.y, CW, hh, SOFT, r=6); x = M
            for k, v in enumerate(head):
                hv = self.height(v, widths[k] - 2 * pad, 8.8, 11.6, 'S')
                self.para(x + pad, self.y + (hh - hv) / 2, v, widths[k] - 2 * pad, 8.8, 11.6, INK, 'S', align=1, keep=False); x += widths[k]
            self.y += hh
        draw_head(False)
        for i, r in enumerate(body):
            if i in breaks:
                self.page_start(); draw_head(True)
            h = hs[i]
            if i % 2 == 0: self.rect(M, self.y, CW, h, NEUTRAL, r=3)
            x = M
            for k, v in enumerate(r):
                if cell_fns and cell_fns.get(k):
                    cell_fns[k](self, x, self.y, widths[k], h, v)
                elif is_num[k]:
                    decimal_cell(self, x, self.y, widths[k], h, v, [rr[k] for rr in body])
                else:
                    hv = self.height(v, widths[k] - 2 * pad, fsz, lead, 'S' if k == 0 else 'R')
                    self.para(x + pad, self.y + (h - hv) / 2, v, widths[k] - 2 * pad, fsz, lead, INK, 'S' if k == 0 else 'R', align=0)
                x += widths[k]
            self.line(M, self.y + h, W - M, self.y + h, BORDER, .4)
            self.y += h
        self.in_table = False
        self.y += 16


def col_widths(rows, is_num):
    ncol = len(rows[0]); pad = 18
    nat = [max(pdfmetrics.stringWidth(re.sub(r'[*`]', '', r[k]), 'S' if k == 0 else 'R', 9.4) for r in rows) + pad for k in range(ncol)]
    longest_word = [max(pdfmetrics.stringWidth(wd, 'S', 9.4) for r in rows for wd in (r[k].split() or [''])) + pad + 6 for k in range(ncol)]
    if sum(nat) <= CW:
        extra = CW - sum(nat); textual = [k for k in range(ncol) if not is_num[k]] or list(range(ncol))
        tot = sum(nat[k] for k in textual)
        return [nat[k] + (extra * nat[k] / tot if k in textual else 0) for k in range(ncol)]
    short = [k for k in range(ncol) if nat[k] <= CW * .2 or is_num[k]]
    fixed = sum(nat[k] for k in short)
    longs = [k for k in range(ncol) if k not in short]
    weights = {k: math.sqrt(nat[k]) for k in longs}
    rest = CW - fixed; tw = sum(weights.values())
    w = [nat[k] if k in short else max(longest_word[k], rest * weights[k] / tw) for k in range(ncol)]
    # si sobra ancho, se recorta de la columna más ancha sin bajar de su palabra más larga
    for _ in range(200):
        over = sum(w) - CW
        if over <= .5: break
        k = max(range(ncol), key=lambda j: w[j] - longest_word[j])
        w[k] -= min(over, max(0, w[k] - longest_word[k]))
    return [x * CW / sum(w) for x in w]


def decimal_cell(b, x, t, w, h, v, column):
    """Alinea una cifra por la coma decimal; las de la misma columna comparten el eje."""
    def split(s):
        s = s.strip(); suf = ':1' if s.endswith(':1') else ''
        s = s[:-2] if suf else s
        a, _, d = s.partition(','); return a, (',' + d if d else ''), suf
    fr = max(pdfmetrics.stringWidth(split(s)[1] + split(s)[2], 'M', 9.4) for s in column)
    axis = x + w - 12 - fr
    a, d, suf = split(v)
    b.txt(axis, t + (h - 9.4) / 2 + 1, a, 9.4, 'M', INK, 'right')
    b.txt(axis, t + (h - 9.4) / 2 + 1, d + suf, 9.4, 'M', INK)


# ---------------------------------------------------------------- piezas
def cover(b):
    cv = CFG['cover']
    b.page_start(grid=True, strong=True, right=CFG['header']['cover_right_label'])
    b.pill(M, 91, cv['category_label'], SOFT, ACC)
    first, second = CFG['document']['title_lines']
    b.txt(M, 142, first, 54, 'B'); b.txt(M, 204, second, 54, 'B', ACC)
    b.para(M, 290, cv['subtitle'], CW, 16, 22, align=0)
    b.label(cv['visual_label'], t=344)
    b.photo(M, 363, CW, 331, image=COVER)
    nsec = sum(len(x['sections']) for x in BLOCKS)
    metrics = ((str(len(BLOCKS)), 'bloques de consulta'), (str(nsec), 'apartados con su comprobación'), (str(len(FIGS)), 'figuras de ejemplo'))
    gap = 12; width = (CW - 2 * gap) / 3
    for i, (value, lab) in enumerate(metrics):
        x = M + i * (width + gap); b.rect(x, 715, width, 67, WHITE, BORDER, 11)
        b.txt(x + 14, 728, value, 24, 'B'); b.txt(x + 14, 760, lab, 8.1, 'M', MUTED)


def index_page(b):
    b.page_start(grid=True)
    b.c.bookmarkPage('indice'); b.c.addOutlineEntry('Índice', 'indice', 0)
    b.txt(M, 80, 'Índice', 34, 'B')
    b.txt(M, 126, f"Versión {CFG['document']['version']} · {CFG['document']['date']}", 9, 'M', MUTED)
    gap, pitch = 12, 19
    width = (CW - gap) / 2; top = 150
    for i in range(0, len(BLOCKS), 2):
        pair = BLOCKS[i:i + 2]
        height = 46 + max(len(g['sections']) for g in pair) * pitch
        for column, g in enumerate(pair):
            x = M + column * (width + gap); bi = BLOCKS.index(g)
            b.rect(x, top, width, height, WHITE, BORDER, 11)
            b.rect(x + 12, top + 11, 24, 24, SOFT, r=7); b.icon(BLOCK_ICONS[bi], x + 16.5, top + 15.5, 15, ACC)
            b.para(x + 45, top + 16, f"{g['code']} / {g['name']}", width - 56, 10, 12, INK, 'B', keep=False)
            bp = b.pages.get(('b', g['code']))
            if bp: b.c.linkRect('', f"b{g['code']}", (x + 4, H - top - 38, x + width - 4, H - top - 6), relative=0, thickness=0)
            for s in g['sections']:
                y = top + 42 + (s['num'] - 1) * pitch
                th = b.height(s['title'], width - 58, 8.9, 10.4, 'M')
                if th > pitch:
                    raise ValueError(f"Título demasiado largo para el índice: {s['title']}")
                b.txt(x + 12, y + 5.5, f"{s['num']}.", 8.8, 'S', ACC)
                b.para(x + 27, y + (pitch - th) / 2, s['title'], width - 58, 8.9, 10.4, INK, 'M', keep=False)
                pg = b.pages.get(('s', g['code'], s['num']))
                if pg:
                    b.txt(x + width - 12, y + 5.5, f'{pg:02d}', 8.8, 'S', MUTED, 'right')
                    b.c.linkRect('', f"s{g['code']}_{s['num']}", (x + 6, H - y - pitch, x + width - 6, H - y), relative=0, thickness=0)
        top += height + gap
    if top > BOTTOM: raise ValueError('El índice no cabe en una página.')


def opening_cards(b, texts):
    w = (CW - 14) / 2
    labels = ['QUÉ SE TRATA', 'POR QUÉ IMPORTA', 'QUÉ NECESITA EL LECTOR']
    h0 = b.height(texts[0], w - 28, 10, 14.2, 'M') + 44
    h1 = b.height(texts[1], w - 28, 10, 14.2, 'M') + b.height(texts[2], w - 28, 10, 14.2, 'M') + 72
    h = max(h0, h1); t = b.y
    b.rect(M, t, w, h, NEUTRAL, r=11)
    b.txt(M + 14, t + 14, labels[0], 7.8, 'S', ACC)
    b.para(M + 14, t + 32, texts[0], w - 28, 10, 14.2, INK, 'M', align=0)
    x = M + w + 14; b.rect(x, t, w, h, INK, r=11)
    b.txt(x + 14, t + 14, labels[1], 7.8, 'S', GOLD_DARK)
    hh = b.para(x + 14, t + 32, texts[1], w - 28, 10, 14.2, WHITE, 'M', align=0)
    b.txt(x + 14, t + 44 + hh, labels[2], 7.8, 'S', GOLD_DARK)
    b.para(x + 14, t + 62 + hh, texts[2], w - 28, 10, 14.2, WHITE, 'M', align=0)
    b.y = t + h + 20


def section_head(b, block, s, opening=False):
    flush_pending(b)
    bi = BLOCKS.index(block)
    heading = f"{s['num']}. {s['title']}"
    first, second = s['head'] or (s['title'], '')
    if opening:
        b.page_start(grid=True)
        b.c.bookmarkPage(f"b{block['code']}")
        b.c.addOutlineEntry(f"{block['code']} / {block['name']}", f"b{block['code']}", 0, closed=True)
        b.found[('b', block['code'])] = b.page
        b.txt(M, LAY['block_top_pt'], f"{block['code']} / {block['name'].upper()}", 8, 'B', MUTED)
        top = LAY['section_label_top_pt']
    else:
        need = 16 + 70 + 60
        if DEBUG: print('apartado', block['code'], s['num'], 'pág', b.page, 'espacio', round(b.space()))
        if b.space() < max(LAY['min_space_to_share_page_pt'], need) or b.page in b.block_pages_full:
            b.page_start(); top = LAY['section_label_top_pt']
        else:
            b.y += 22; top = b.y
    b.c.bookmarkHorizontal(f"s{block['code']}_{s['num']}", 0, H - top + 20)
    b.c.addOutlineEntry(heading, f"s{block['code']}_{s['num']}", 1)
    b.found[('s', block['code'], s['num'])] = b.page
    b.label(heading, t=top)
    b.y = b.title(first, second, top + 16) + LAY['title_after_pt']


def render_lines(b, lines):
    i = 0
    while i < len(lines):
        t = lines[i].strip()
        if not t: i += 1; continue
        if t.startswith('Tabla:'):
            m = re.match(r'Tabla:\s+\{tab:([\w-]+)\}\s*(.*)', t); key, cap = m[1], m[2]
            i += 1
            while i < len(lines) and not lines[i].strip(): i += 1
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', x) for x in row): rows.append(row)
                i += 1
            b.table(rows, TABS[key], cap); continue
        if t.startswith('|'):
            raise ValueError('Tabla sin título «Tabla: {tab:clave} ...»: ' + t[:40])
        if t.startswith('@@closing_page'):
            first, second = [x.strip() for x in t[len('@@closing_page'):].split('|')]
            closing_page(b, first, second); i += 1; continue
        if t.startswith('@@callout_grid'):
            m = re.match(r'@@callout_grid\s+\{fig:([\w-]+)\}\s*(.*)', t); i += 1; items = []
            while i < len(lines) and len(items) < 5 and (not lines[i].strip() or lines[i].strip().startswith('!!')):
                if lines[i].strip():
                    mm = re.match(r'!!(\w+)\s+(.+?)\s*\|\s*(.+)', lines[i].strip()); items.append((mm[1], mm[2], mm[3]))
                i += 1
            v_callout_grid(b, m[1], m[2], items); continue
        if t.startswith('@@'):
            m = re.match(r'@@(\w+)\s+\{(fig|tab):([\w-]+)\}\s*(.*)', t)
            VISUALS[m[1]](b, m[2], m[3], m[4]); i += 1; continue
        if t.startswith('!!'):
            m = re.match(r'!!(\w+)\s+(.+?)\s*\|\s*(.+)', t); b.callout(m[1], m[2], m[3]); i += 1; continue
        if t.startswith('>> '):
            text, who = [x.strip() for x in t[3:].split('||')]; b.quote(text, who); i += 1; continue
        if t.startswith('#### '):
            nxt = next((x for x in lines[i + 1:] if x.strip()), '')
            need = 26 + (b.height(nxt, CW) if nxt and not nxt.startswith(('@@', '|', 'Tabla:', '!!')) else 60)
            b.ensure(need + 8); b.y += 6; b.label(t[5:]); b.y += 22; i += 1; continue
        m = re.match(r'^(\d+)\.\s+(.+)', t)
        if m: b.numbered(*m.groups()); i += 1; continue
        if t.startswith('- '): b.bullet(t[2:]); i += 1; continue
        ls = [t]; i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('|', '- ', '#', '@@', '!!', '>>', 'Tabla:')):
            ls.append(lines[i].strip()); i += 1
        text = ' '.join(ls); h = b.height(text)
        if b.y + h > BOTTOM:
            # se parte el párrafo por líneas para no dejar huecos
            split_paragraph(b, text)
        else:
            b.para(M, b.y, text); b.y += h + 8


def split_paragraph(b, text):
    sty = ParagraphStyle('p', fontName='R', fontSize=10.5, leading=15, textColor=INK, alignment=4, allowWidows=0, allowOrphans=0)
    p = Paragraph(markup(bind(text)), sty); p.wrap(CW, 3000)
    avail = BOTTOM - b.y
    if avail < 15 * 2:
        b.page_start(); h = b.para(M, b.y, text); b.y += h + 8; return
    parts = p.split(CW, avail)
    if len(parts) < 2:
        b.page_start(); h = b.para(M, b.y, text); b.y += h + 8; return
    for k, part in enumerate(parts):
        if k: b.page_start()
        _, h = part.wrap(CW, 3000); part.drawOn(b.c, M, H - b.y - h); b.y += h + (8 if k == len(parts) - 1 else 0)


def figure(b, key, caption, h, draw, gap_after=14):
    """Coloca la figura con su pie. Si no cabe y queda espacio útil, el texto
    siguiente sube a ocupar el hueco y la figura abre la página siguiente."""
    ch = b.caption_h(caption)
    item = (key, caption, h, draw, gap_after)
    if b.pending or b.y + h + 8 + ch > BOTTOM:
        if b.space() >= 110 and not b.flushing:
            b.pending.append(item); return
        b.page_start()
        if item in b.pending: return
    place_figure(b, *item)


def place_figure(b, key, caption, h, draw, gap_after=14):
    ch = b.caption_h(caption)
    if b.y + h + 8 + ch > BOTTOM and not b.flushing: b.page_start()
    t = b.y; draw(t)
    b.y = t + h + 8
    b.caption('fig', FIGS[key], caption); b.y += ch + gap_after


def flush_pending(b):
    while b.pending:
        item = b.pending[0]; ch = b.caption_h(item[1])
        if b.y + item[2] + 8 + ch > BOTTOM:
            b.page_start()  # la propia apertura de página coloca las pendientes
        else:
            b.pending.pop(0); place_figure(b, *item)


# ---------------------------------------------------------------- visuales
def v_use_flow(b, kind, key, cap):
    def draw(t):
        rows = [('TODOS LOS PROYECTOS', [('Prompt de escritura', 'en instrucciones', 'document'), ('Prompt de arranque', 'se pega al empezar', 'layers'), ('Ficha inicial', 'ocho datos', 'check')]),
                ('SI HAY UN DOCUMENTO', [('Manual + configuración', 'se adjuntan', 'book'), ('Prompt de aplicación', 'se pega', 'layers'), ('Documento y revisión', 'PDF comprobado', 'eye')])]
        bw = (CW - 110 - 2 * 22) / 3
        for r, (lab, steps) in enumerate(rows):
            y = t + r * 78
            b.txt(M, y + 25, lab, 7.4, 'S', ACC if r == 0 else INK)
            for k, (a, s, ic) in enumerate(steps):
                x = M + 110 + k * (bw + 22); dark = (r == 1 and k == 2)
                b.rect(x, y, bw, 62, INK if dark else SOFT, r=10)
                b.icon(ic, x + 12, y + 11, 15, GOLD_DARK if dark else ACC)
                b.txt(x + 12, y + 33, a, 8.8, 'S', WHITE if dark else INK)
                b.txt(x + 12, y + 46, s, 7.8, 'M', HexColor('#D9DEE0') if dark else MUTED)
                if k < 2: b.arrow(x + bw + 3, y + 31, x + bw + 19, y + 31, ACC, 1.1, 4)
        x3 = M + 110 + 2 * (bw + 22) + bw / 2; x1 = M + 110 + bw / 2
        b.line(x3, t + 62, x3, t + 70, ACC, 1); b.line(x3, t + 70, x1, t + 70, ACC, 1); b.arrow(x1, t + 70, x1, t + 77, ACC, 1, 3.5)
    figure(b, key, cap, 140, draw)


def v_config_sheet(b, kind, key, cap):
    fields = [('Tema', 'De qué trata el documento'), ('Objetivo', 'Qué debe conseguir el lector'), ('Público', 'Quién lo lee y qué sabe ya'),
              ('Tipo de trabajo', 'Cuaderno, informe, ficha...'), ('Alcance', 'Qué incluye y qué no'), ('Entregables', 'Archivos y formatos finales'),
              ('Formato', 'A4 vertical u otro soporte'), ('Color principal', 'Un hexadecimal o «identidad original»')]
    def draw(t):
        gap = 10; w = (CW - 3 * gap) / 4
        for i, (a, d) in enumerate(fields):
            x = M + (i % 4) * (w + gap); y = t + (i // 4) * 70; dark = i == 7
            b.rect(x, y, w, 60, INK if dark else WHITE, None if dark else BORDER, 10)
            b.txt(x + 12, y + 11, f'{i + 1:02d}', 7.6, 'S', GOLD_DARK if dark else ACC)
            b.txt(x + 12, y + 25, a, 9.6, 'B', WHITE if dark else INK)
            b.para(x + 12, y + 39, d, w - 20, 7.8, 10, HexColor('#D9DEE0') if dark else MUTED, 'M', align=0, keep=False)
    figure(b, key, cap, 130, draw)


def v_tonal_scale(b, kind, key, cap):
    L, Cc, Hh = PAL.lch(COL['accent'])
    tones = [0, 10, 21, 30, 40, 50, 60, 70, 80, 86, 92, 98, 100]
    roles = {21: 'Tinta*', 40: 'Acento de texto', 86: 'Degradado', 92: 'Superficie', 98: 'Fondo'}
    def draw(t):
        w = CW / len(tones)
        for i, tn in enumerate(tones):
            col = PAL.tone(Hh, Cc, tn); x = M + i * w
            b.rect(x + 1.5, t, w - 3, 52, HexColor(col), BORDER if tn > 90 else None, 6)
            b.txt(x + w / 2, t + 58, str(tn), 8, 'S', INK, 'center')
            if tn in roles:
                b.line(x + w / 2, t + 72, x + w / 2, t + 80, ACC, .8)
                b.para(x - 6, t + 83, roles[tn], w + 12, 7.4, 9, ACC, 'S', align=1, keep=False)
        b.txt(M, t + 112, '* En la identidad original la tinta es azul pizarra; en una paleta de un solo color, la tinta sale de este tono con poca saturación.', 7.6, 'M', MUTED)
    figure(b, key, cap, 120, draw)


def mini_palette(b, x, t, w, cols, name, seed):
    """Cuatro colores principales en grande y, debajo, los tonos de apoyo en pequeño."""
    b.txt(x, t, name, 9.5, 'B'); b.txt(x + w, t + 1, seed, 8, 'S', MUTED, 'right')
    main = [('Fondo', 'background'), ('Tinta', 'text'), ('Acento', 'accent'), ('Acento de texto', 'accent_text')]
    sw = (w - 3 * 6) / 4
    for i, (lab, k) in enumerate(main):
        xx = x + i * (sw + 6); yy = t + 18
        b.rect(xx, yy, sw, 46, HexColor(cols[k]), BORDER, 7)
        b.txt(xx, yy + 51, lab, 7.6, 'S'); b.txt(xx, yy + 61, cols[k], 7.2, 'M', MUTED)
    b.txt(x, t + 98, 'TONOS DE APOYO', 6.8, 'S', ACC)
    support = [('Apoyo', 'muted'), ('Superficie', 'accent_surface'), ('Separador', 'border'), ('Fila', 'row'), ('Degradado', 'gradient_strong')]
    ss = (w - 4 * 6) / 5
    for i, (lab, k) in enumerate(support):
        xx = x + i * (ss + 6); yy = t + 108
        b.rect(xx, yy, ss, 12, HexColor(cols[k]), BORDER, 3)
        b.txt(xx, yy + 16, lab, 6.6, 'S'); b.txt(xx, yy + 24, cols[k], 6, 'M', MUTED)
    y = t + 142; b.rect(x, y, w, 46, HexColor(cols['background']), BORDER, 9)
    b.c.saveState(); b.c.setFillColor(HexColor(cols['text'])); b.c.setFont('B', 12); b.c.drawString(x + 12, H - y - 20, 'Un color elegido,')
    b.c.setFillColor(HexColor(cols['accent_text'])); b.c.drawString(x + 12, H - y - 34, 'todas sus funciones.'); b.c.restoreState()
    b.rect(x + w - 64, y + 8, 52, 30, HexColor(cols['text']), r=7); b.line(x + w - 56, y + 18, x + w - 40, y + 18, HexColor(cols['accent_on_dark']), 2)


def v_palette_demo(b, kind, key, cap):
    green = PAL.palette('#2E7D6B')
    def draw(t):
        w = (CW - 24) / 2
        mini_palette(b, M, t, w, COL, 'Identidad original', COL['accent'])
        mini_palette(b, M + w + 24, t, w, green, 'Paleta desde un color', '#2E7D6B')
    figure(b, key, cap, 188, draw)


def mini_page(b, x, t, w, grid=True, strong=False):
    h = w * 297 / 210; s = w / W
    b.rect(x, t, w, h, WHITE, BORDER, 4, shadow=True)
    c = b.c; c.saveState(); p = c.beginPath(); p.roundRect(x, H - t - h, w, h, 4); c.clipPath(p, stroke=0)
    if grid:
        c.radialGradient(x + w + 3, H - t - 6, 340 * s, [C['gradient_strong'] if strong else C['gradient_soft'], WHITE], positions=[0, 1])
        st = LAY['grid_step_pt'] * s
        k = 0
        while k * st < w: b.line(x + k * st, t, x + k * st, t + h, C['grid_line'], .2); k += 1
        k = 0
        while k * st < h: b.line(x, t + k * st, x + w, t + k * st, C['grid_line'], .2); k += 1
    c.restoreState()
    m = M * s
    b.rect(x + m, t + 25 * s, 24 * s, 24 * s, INK, r=2)
    b.line(x + m + 30 * s, t + 37 * s, x + m + 110 * s, t + 37 * s, INK, 1.2)
    b.line(x + w - m - 70 * s, t + 37 * s, x + w - m, t + 37 * s, GOLD, 1)
    b.line(x + m, t + 60 * s, x + w - m, t + 60 * s, BORDER, .4)
    b.line(x + m, t + h - 34 * s, x + w - m, t + h - 34 * s, BORDER, .4)
    b.txt(x + w - m, t + h - 26 * s, '07', 4, 'S', INK, 'right')
    return h, s, m


def v_cover_variants(b, kind, key, cap):
    names = [('CUADERNO DIDÁCTICO', 'Ciudades del', 'río Éufrates.'), ('INFORME', 'Resultados', 'del trimestre.'), ('FICHA DE CONSULTA', 'Tamaños de', 'imagen.')]
    def draw(t):
        gap = 30; w = 132; x0 = M + (CW - 3 * w - 2 * gap) / 2
        for i, (cat, a, z) in enumerate(names):
            x = x0 + i * (w + gap); h, s, m = mini_page(b, x, t, w, True, True)
            pw = pdfmetrics.stringWidth(cat, 'S', 4.6) + 10
            b.rect(x + m, t + 26, pw, 9, SOFT, r=3); b.txt(x + m + 5, t + 28.5, cat, 4.6, 'S', ACC)
            b.txt(x + m, t + 40, a, 13, 'B'); b.txt(x + m, t + 55, z, 13, 'B', ACC)
            if i == 0:
                b.photo(x + m, t + 80, w - 2 * m, 72, image=PHOTO, r=5)
                for k in range(3): b.rect(x + m + k * (w - 2 * m) / 3 + 1, t + 158, (w - 2 * m) / 3 - 3, 13, WHITE, BORDER, 3)
            elif i == 1:
                b.txt(x + m, t + 80, '+18 %', 26, 'B')
                b.txt(x + m, t + 110, 'Ventas frente al trimestre anterior', 6, 'M', MUTED)
                for k, hv in enumerate([24, 35, 30, 46]):
                    b.rect(x + m + k * 22, t + 172 - hv, 14, hv, GOLD if k == 3 else SOFT, r=2)
            else:
                for k in range(5):
                    y = t + 80 + k * 16; b.rect(x + m, y, w - 2 * m, 12, NEUTRAL if k % 2 == 0 else WHITE, r=2)
                    b.line(x + m + 6, y + 6, x + m + 40, y + 6, INK, 1.2); b.line(x + w - m - 30, y + 6, x + w - m - 6, y + 6, ACC, 1.2)
            b.txt(x, t + h + 8, ['Fotografía del tema', 'Cifra protagonista', 'Directa al contenido'][i], 8, 'S', ACC)
    figure(b, key, cap, 132 * 297 / 210 + 22, draw)


def v_fixed_adjustable(b, kind, key, cap):
    data = [('SE MANTIENE', ['Inter en cuatro pesos', 'Cuadrícula y degradado', 'Títulos y aperturas en dos colores', 'Cabecera, pie y numeración', 'Componentes y sus medidas'], NEUTRAL),
            ('SE AJUSTA', ['Paleta, si hay color propio', 'Imagen y composición de portada', 'Páginas y componentes necesarios', 'Intensidad del degradado', 'Tipo de cierre'], INK)]
    def draw(t):
        w = (CW - 34) / 2
        for j, (title, lines, fill) in enumerate(data):
            x = M + j * (w + 34); b.rect(x, t, w, 128, fill, r=10); fg = WHITE if j else INK
            b.txt(x + 14, t + 14, title, 8, 'S', GOLD_DARK if j else ACC)
            for k, tx in enumerate(lines): b.icon('check', x + 13, t + 34 + k * 18, 11, GOLD_DARK if j else ACC); b.txt(x + 32, t + 35 + k * 18, tx, 9, 'M', fg)
        b.icon('arrow', M + w + 8, t + 55, 18, ACC)
    figure(b, key, cap, 128, draw)


def v_type_specimen(b, kind, key, cap):
    def draw(t):
        b.rect(M, t, CW, 168, NEUTRAL, r=12)
        b.txt(M + 18, t + 16, 'INTER · REGULAR · MEDIUM · SEMIBOLD · BOLD', 7.4, 'S', ACC)
        b.txt(M + 18, t + 40, 'Aa', 64, 'B')
        rows = [('B', 'Bold', 'Títulos que orientan'), ('S', 'SemiBold', 'Rótulos y cabeceras de tabla'), ('M', 'Medium', 'Etiquetas y apoyos breves'), ('R', 'Regular', 'El cuerpo desarrolla la idea')]
        for k, (f, n, sample) in enumerate(rows):
            y = t + 36 + k * 21
            b.txt(M + 140, y + 3, n, 7.6, 'S', MUTED); b.txt(M + 205, y, sample, 13.5, f)
        b.line(M + 18, t + 125, W - M - 18, t + 125)
        b.para(M + 18, t + 136, 'Tamaño, peso y espacio construyen la jerarquía. El color solo acentúa un fragmento con significado.', CW - 36, 9.6, 13.5, align=0)
    figure(b, key, cap, 168, draw)


def v_identity_anatomy(b, kind, key, cap):
    def draw(t):
        w = 172; h, s, m = mini_page(b, M, t, w, True, False)
        b.txt(M + m, t + 70 * s, '01 / BLOQUE', 3.4, 'B', MUTED)
        b.line(M + m, t + 88 * s, M + m + 8, t + 88 * s, ACC, .8); b.txt(M + m + 11, t + 85.5 * s, '1. APARTADO', 4, 'S', ACC)
        b.txt(M + m, t + 103 * s, 'Título del apartado', 9.5, 'B'); b.txt(M + m, t + 103 * s + 11, 'en dos colores.', 9.5, 'B', ACC)
        for k in range(12): b.line(M + m, t + 103 * s + 30 + k * 7, M + w - m, t + 103 * s + 30 + k * 7, HexColor('#C9CED1'), 1.6)
        notes = [(30, 'Cabecera: icono, nombre del proyecto y documento con versión', 37), (60, 'Filete de cabecera a 60 pt del borde', 60),
                 (8, 'Degradado radial desde la esquina superior derecha', 20), (85, 'Etiqueta del apartado a 85 pt; título a 101 pt', 88),
                 (140, 'Cuadrícula decorativa cada 21 pt, detrás del contenido', 300), (245, 'Lectura: caja de 182 mm con márgenes de 14 mm', 230),
                 (H / 1 - 34, 'Pie: filete a 34 pt del borde y número de página', H - 30)]
        for k, (_, text, py) in enumerate(notes):
            ty = t + 12 + k * 33
            ax = M + w - 6 if k != 5 else M + w - m - 4
            ay = t + py * s
            b.line(ax, ay, M + w + 34, ty + 5, ACC, .6); b.circle(ax, ay, 2, GOLD)
            b.circle(M + w + 34, ty + 5, 1.6, ACC)
            b.para(M + w + 42, ty, text, CW - w - 42, 9.2, 12.6, INK, 'M', align=0, keep=False)
    figure(b, key, cap, 172 * 297 / 210, draw)


def v_title_examples(b, kind, key, cap):
    rows = [(True, 'La portada dice de qué trata', 'antes de decorar.', 'Cada línea se lee sola y la segunda completa la primera.'),
            (False, 'La portada dice de', 'qué trata antes de decorar.', 'El corte separa «de qué»: la primera línea queda colgando.')]
    def draw(t):
        for k, (ok, a, z, note) in enumerate(rows):
            y = t + k * 76; b.rect(M, y, CW, 66, WHITE, BORDER, 10)
            b.txt(M + 16, y + 13, a, 17, 'B'); b.txt(M + 16, y + 34, z, 17, 'B', ACC)
            x = M + CW - 178
            b.rect(x, y + 12, 164, 42, NEUTRAL if ok else SOFT, r=7)
            b.icon('check' if ok else 'warning', x + 9, y + 20, 11, ACC)
            b.txt(x + 26, y + 20, 'CORTE CON SENTIDO' if ok else 'CORTE QUE SEPARA', 6.8, 'S', ACC)
            b.para(x + 9, y + 33, note, 148, 7.2, 9, INK, 'M', align=0, keep=False)
    figure(b, key, cap, 142, draw)


def v_heading_levels(b, kind, key, cap):
    def draw(t):
        b.rect(M, t, CW, 156, WHITE, BORDER, 12); x = M + 18
        b.txt(x, t + 16, '04 / ENCABEZADOS Y DESARROLLO', 8, 'B', MUTED)
        b.line(x, t + 37, x + 15, t + 37, ACC, 1.4); b.txt(x + 21, t + 32, '1. JERARQUÍA Y NUMERACIÓN', 8, 'S', ACC)
        b.txt(x, t + 50, 'Tres niveles bastan', 19, 'B'); b.txt(x, t + 71, 'para casi cualquier documento.', 19, 'B', ACC)
        b.line(x, t + 109, x + 15, t + 109, ACC, 1.4); b.txt(x + 21, t + 104, 'CONSERVAR LA IDENTIDAD', 8, 'S', ACC)
        for k in range(2): b.line(x, t + 127 + k * 9, x + 300 - k * 80, t + 127 + k * 9, HexColor('#C9CED1'), 2)
        tags = [(t + 19, 'Bloque · «01 / Nombre»'), (t + 35, 'Apartado · «1. Nombre», reinicia en cada bloque'), (t + 66, 'Título en dos colores'), (t + 107, 'Subtítulo · filete y mayúsculas, sin número')]
        for y, txt in tags:
            b.line(M + 330, y + 3, M + 344, y + 3, BORDER, .6); b.para(M + 348, y - 3, txt, CW - 360, 8, 10.5, INK, 'M', align=0, keep=False)
    figure(b, key, cap, 156, draw)


def v_grid_page(b, kind, key, cap):
    labels = ['Seis columnas de lectura', 'Tres y tres: comparación', 'Dos para imagen, cuatro para texto']
    def draw(t):
        gap = 22; w = (CW - 2 * gap) / 3
        for i in range(3):
            x = M + i * (w + gap); h, s, m = mini_page(b, x, t, w, False)
            cw = w - 2 * m; g = 14 * s; colw = (cw - 5 * g) / 6
            for k in range(6): b.rect(x + m + k * (colw + g), t + 66 * s, colw, h - 66 * s - 40 * s, HexColor('#FBEFEF') if False else NEUTRAL, r=1)
            y0 = t + 80 * s
            if i == 0:
                for k in range(16): b.line(x + m, y0 + k * 7, x + w - m, y0 + k * 7, HexColor('#9AA5AB'), 1.4)
            elif i == 1:
                for k in range(3):
                    for j in range(2):
                        b.rect(x + m + j * (cw / 2 + g / 2), y0 + k * 40, cw / 2 - g / 2, 34, WHITE, ACC, 3, width=.5)
            else:
                b.photo(x + m, y0, 2 * colw + g, 80, image=PHOTO, r=3, focus_x=.3)
                for k in range(10): b.line(x + m + 2 * (colw + g), y0 + 3 + k * 7, x + w - m, y0 + 3 + k * 7, HexColor('#9AA5AB'), 1.4)
            b.txt(x, t + h + 8, labels[i], 8, 'S', ACC)
    figure(b, key, cap, (CW - 44) / 3 * 297 / 210 + 20, draw)


def v_spacing_scale(b, kind, key, cap):
    items = [(6, 'Entre etiqueta y título', 'Etiqueta y título se leen como una unidad'), (8, 'Entre párrafos', '8–12 pt; el párrafo es la unidad de lectura'),
             (12, 'Entre tarjetas y recuadros', '12–16 pt; componentes del mismo grupo'), (18, 'Título → texto; texto → figura', '16–20 pt; separa niveles sin desconectar'),
             (22, 'Entre apartados en la misma página', '22–32 pt; el cambio de tema se ve')]
    def draw(t):
        for k, (v, a, d) in enumerate(items):
            y = t + k * 30
            b.rect(M, y + 4, v * 3, 16, GOLD if k == 3 else SOFT, r=3)
            b.txt(M + 104, y + 7, f'{v} pt', 9.5, 'B')
            b.txt(M + 150, y + 3, a, 9.4, 'S'); b.txt(M + 150, y + 15, d, 8.2, 'M', MUTED)
    figure(b, key, cap, 148, draw)


def v_widow_fix(b, kind, key, cap):
    bad = 'La revisión se hace sobre el archivo exportado y no sobre el editor, porque solo el PDF muestra la página tal como la recibe el lector final.'
    good = 'La revisión se hace sobre el archivo exportado y no sobre el editor, porque solo el PDF muestra la página tal como la verá el lector.'
    def lone_width():
        for w in range(150, 240):
            sty = ParagraphStyle('w', fontName='R', fontSize=10, leading=14, alignment=4)
            p = Paragraph(bad, sty); p.wrap(w, 999)
            last = p.blPara.lines[-1]
            words = last[1] if isinstance(last, tuple) else last.words
            if len([x for x in words if str(x).strip()]) == 1: return w
        return 200
    wd = lone_width()
    def draw(t):
        bw = (CW - 24) / 2
        for k, (text, title, keep) in enumerate([(bad, 'PALABRA AISLADA', False), (good, 'FRASE AJUSTADA', True)]):
            x = M + k * (bw + 24); b.rect(x, t, bw, 120, NEUTRAL if k == 0 else SOFT, r=10)
            b.icon('warning' if k == 0 else 'check', x + 14, t + 13, 12, ACC); b.txt(x + 32, t + 14, title, 7.8, 'S', ACC)
            hh = b.para(x + 14, t + 36, text, wd, 10, 14, INK, 'R', align=4, keep=keep)
            if k == 0:
                b.line(x + 14, t + 36 + hh + 2, x + 60, t + 36 + hh + 2, GOLD, 1.6)
    figure(b, key, cap, 120, draw)


def v_gap_fix(b, kind, key, cap):
    def draw(t):
        w = 150; gap = 60; x0 = M + (CW - 2 * w - gap) / 2
        for k in range(2):
            x = x0 + k * (w + gap); h, s, m = mini_page(b, x, t, w, False)
            y = t + 70 * s
            for j in range(7): b.line(x + m, y + j * 6, x + w - m, y + j * 6, HexColor('#9AA5AB'), 1.3)
            y += 50
            if k == 0:
                b.rect(x + m, y, w - 2 * m, h - (y - t) - 40 * s, None, ACC, 3, width=.7)
                b.para(x + m + 6, y + 40, 'Media página vacía: el apartado siguiente empezaba en página nueva', w - 2 * m - 12, 7.2, 9.4, ACC, 'S', align=1, keep=False)
            else:
                b.line(x + m, y, x + m + 6, y, ACC, 1); b.line(x + m, y + 8, x + m + 60, y + 8, INK, 2.4); b.line(x + m, y + 16, x + m + 44, y + 16, ACC, 2.4)
                for j in range(5): b.line(x + m, y + 30 + j * 6, x + w - m, y + 30 + j * 6, HexColor('#9AA5AB'), 1.3)
                b.rect(x + m, y + 66, w - 2 * m, 50, SOFT, r=3); b.txt(x + w / 2, y + 87, 'Esquema del apartado', 6.5, 'S', ACC, 'center')
                for j in range(4): b.line(x + m, y + 126 + j * 6, x + w - m, y + 126 + j * 6, HexColor('#9AA5AB'), 1.3)
            b.txt(x, t + h + 8, 'Antes' if k == 0 else 'Recompuesta', 8, 'S', ACC)
        b.arrow(x0 + w + 12, t + 100, x0 + w + gap - 12, t + 100, ACC, 1.2)
    figure(b, key, cap, 150 * 297 / 210 + 20, draw)


def v_table_anatomy(b, kind, key, cap):
    def draw(t):
        tw = 300; x = M; widths = [34, 150, 58, 58]
        b.rect(x, t, tw, 30, SOFT, r=6)
        for k, (hd, cx) in enumerate(zip(['Nº', 'Concepto', 'Ancho (mm)', 'Peso (kg)'], [17, 109, 213, 271])):
            b.txt(x + cx, t + 11, hd, 8.4, 'S', INK, 'center')
        data = [('1', 'Columna de número', '12,5', '0,40'), ('2', 'Columna de texto', '96,0', '1,25'), ('3', 'Columna de cifra', '18,0', '12,80'), ('4', 'Fila alterna', '7,5', '0,05')]
        for i, row in enumerate(data):
            y = t + 30 + i * 26
            if i % 2 == 0: b.rect(x, y, tw, 26, NEUTRAL, r=3)
            b.txt(x + 17, y + 9, row[0], 9, 'M', INK, 'center'); b.txt(x + 43, y + 9, row[1], 9, 'S')
            for j, ax in [(2, 222), (3, 280)]:
                a, d = row[j].split(','); b.txt(x + ax, y + 9, a, 9, 'M', INK, 'right'); b.txt(x + ax, y + 9, ',' + d, 9, 'M')
            b.line(x, y + 26, x + tw, y + 26, BORDER, .4)
        notes = [(t + 15, 'Cabecera centrada en superficie de acento; unidades entre paréntesis'), (t + 43, 'Texto alineado a la izquierda con 9 pt de margen interior'),
                 (t + 69, 'Cifras alineadas por la coma, con los mismos decimales'), (t + 95, 'Filas alternas con sombreado suave'), (t + 134, 'Separador horizontal de 0,4 pt; sin líneas verticales')]
        for y, txt in notes:
            b.line(x + tw + 6, y, x + tw + 20, y, ACC, .6); b.circle(x + tw + 6, y, 1.8, GOLD)
            b.para(x + tw + 26, y - 6, txt, CW - tw - 26, 8.4, 11, INK, 'M', align=0, keep=False)
    figure(b, key, cap, 150, draw)


PAIR_NAMES = {
    'Cuerpo / fondo': 'Texto principal sobre la página',
    'Cuerpo / superficie': 'Texto principal sobre tarjeta blanca',
    'Cuerpo / fila alterna': 'Texto principal sobre fila de tabla',
    'Cuerpo / superficie de acento': 'Texto principal sobre cabecera de tabla',
    'Apoyo / fondo': 'Texto de apoyo sobre la página',
    'Apoyo / superficie': 'Texto de apoyo sobre tarjeta blanca',
    'Acento de texto / fondo': 'Acento de texto sobre la página',
    'Acento de texto / sup. de acento': 'Acento de texto sobre cabecera de tabla',
    'Blanco / tinta (tarjeta oscura)': 'Texto blanco sobre tarjeta oscura',
    'Acento / tinta (tarjeta oscura)': 'Acento sobre tarjeta oscura',
}


def swatch_cell(bk, x, t, w, h, v):
    bk.rect(x + 9, t + (h - 10) / 2, 10, 10, HexColor(v), BORDER, 2)
    bk.txt(x + 23, t + (h - 8) / 2 + 1, v, 7.8, 'M', INK)


def center_cell(bk, x, t, w, h, v):
    bk.txt(x + w / 2, t + (h - 9.4) / 2 + 1, v, 9.4, 'M', INK, 'center')


def v_contrast_table(b, kind, key, cap):
    """Contraste de cada combinación de texto y fondo de la paleta del documento."""
    rows = [['Nº', 'Combinación', 'Texto', 'Fondo', 'Contraste', 'Mínimo', 'Se lee bien']]
    for n, r in enumerate(PAL.report(COL), 1):
        rows.append([str(n), PAIR_NAMES.get(r['par'], r['par']), r['texto'], r['fondo'],
                     f"{r['contraste']:.2f}".replace('.', ','), f"{r['minimo']:.1f}".replace('.', ','), 'Sí' if r['cumple'] else 'No'])
    ws = [30, 176, 66, 66, 64, 54, 0]; ws[-1] = CW - sum(ws)
    b.table(rows, TABS[key], cap, cell_fns={0: center_cell, 2: swatch_cell, 3: swatch_cell, 6: center_cell},
            numeric=[False, False, False, False, True, True, False], widths=ws)


def v_measures_table(b, kind, key, cap):
    """Medidas del perfil A4 en puntos y milímetros (1 pt = 0,3528 mm)."""
    mm = lambda pt: pt * 25.4 / 72
    data = [
        ('Margen lateral', M, 'Izquierda y derecha de todas las páginas'),
        ('Caja de texto', CW, 'Ancho útil entre márgenes'),
        ('Calle entre columnas', LAY['gutter_pt'], 'Separación de la retícula de seis columnas'),
        ('Columna de la retícula', (CW - 5 * LAY['gutter_pt']) / 6, 'Una de las seis columnas'),
        ('Paso de la cuadrícula', LAY['grid_step_pt'], 'Fondo decorativo'),
        ('Filete de cabecera', LAY['header_rule_top_pt'], 'Distancia desde el borde superior'),
        ('Inicio del contenido', LAY['content_top_pt'], 'Páginas de continuación'),
        ('Etiqueta de bloque', LAY['block_top_pt'], 'Aperturas de bloque'),
        ('Etiqueta de apartado', LAY['section_label_top_pt'], 'Inicio de apartado'),
        ('Título de apartado', LAY['title_top_pt'], 'Primera línea del título'),
        ('Filete del pie', LAY['footer_rule_from_bottom_pt'], 'Distancia desde el borde inferior'),
        ('Cuerpo de texto', LAY['body_pt'], 'Inter Regular, lectura continua'),
        ('Interlineado del cuerpo', LAY['body_leading_pt'], 'Entre líneas de un párrafo'),
        ('Título de apartado (tamaño)', LAY['title_pt'], 'Inter Bold en dos colores'),
        ('Título de portada', 54.0, 'Inter Bold en dos líneas'),
        ('Pie de figura', 8.5, 'Inter Medium, color de apoyo'),
        ('Espacio entre párrafos', 8.0, 'Separación mínima'),
        ('Espacio entre tarjetas', 12.0, 'Componentes del mismo grupo'),
        ('Espacio antes de un apartado', 22.0, 'Cuando comparte página'),
        ('Margen interior de celda', 9.0, 'Tablas'),
        ('Altura mínima de fila', 24.0, 'Tablas'),
        ('Margen interior de tarjeta', 14.0, 'Tarjetas y recuadros'),
        ('Radio de esquina de fotografía', LAY['photo_radius_pt'], 'Fotografías'),
        ('Radio de esquina de tarjeta', LAY['card_radius_pt'], 'Tarjetas y recuadros'),
        ('Diámetro del círculo de paso', 18.0, 'Pasos numerados'),
        ('Icono junto al texto', 13.0, 'Recuadros y etiquetas'),
        ('Grosor del filete de acento', 1.4, 'Etiquetas y subtítulos'),
        ('Grosor del separador de tabla', 0.4, 'Líneas entre filas'),
    ]
    rows = [['Nº', 'Elemento', 'Medida (pt)', 'Medida (mm)', 'Dónde se usa']]
    for n, (name, pt, use) in enumerate(data, 1):
        rows.append([str(n), name, f"{pt:.2f}".replace('.', ','), f"{mm(pt):.2f}".replace('.', ','), use])
    ws = [30, 170, 70, 70, 0]; ws[-1] = CW - sum(ws)
    b.table(rows, TABS[key], cap, cell_fns={0: center_cell}, numeric=[False, False, True, True, False], widths=ws)


def v_callout_grid(b, key, cap, items):
    w = (CW - 14) / 2
    full_last = len(items) % 2 == 1
    hs = [max(46, b.height(z, (CW if (full_last and k == len(items) - 1) else w) - 50, 9, 12.6) + 33) for k, (_, _, z) in enumerate(items)]
    rows = [max(hs[k:k + 2]) for k in range(0, len(items), 2)]
    def draw(t):
        y = t
        for r, rh in enumerate(rows):
            for j, (kind, a, z) in enumerate(items[2 * r:2 * r + 2]):
                full = len(items[2 * r:2 * r + 2]) == 1
                x = M + j * (w + 14); ww = CW if full else w
                b.rect(x, y, ww, rh, SOFT if kind == 'comprobar' else NEUTRAL, r=10)
                b.line(x, y + 10, x, y + rh - 10, GOLD, 2.2)
                b.icon(CALLOUT_ICON.get(kind, 'info'), x + 13, y + 11, 13, ACC)
                b.txt(x + 37, y + 11, a.upper(), 7.4, 'S', ACC)
                b.para(x + 37, y + 25, z, ww - 50, 9, 12.6, INK, 'R', align=0)
            y += rh + 10
    figure(b, key, cap, sum(rows) + 10 * (len(rows) - 1), draw)


def card_block(b, x, t, w, h, title, body, dark=False):
    b.rect(x, t, w, h, INK if dark else WHITE, None if dark else BORDER, 10)
    b.line(x + 14, t + 12, x + 31, t + 12, GOLD_DARK if dark else GOLD, 2)
    hh = b.para(x + 14, t + 20, title, w - 28, 11, 14, WHITE if dark else INK, 'B', align=0, keep=False)
    b.para(x + 14, t + 26 + hh, body, w - 28, 9.4, 13, HexColor('#E4E8EA') if dark else INK, 'R', align=0)


def v_cards_demo(b, kind, key, cap):
    two = [('¿Cuándo va una tabla?', 'Cuando varios elementos comparten atributos y el lector necesita compararlos en filas y columnas.'),
           ('¿Cuándo van tarjetas?', 'Cuando son pocas ideas con explicación propia que se leen por separado y no comparten columnas.')]
    three = [('Informe', 'Conclusiones con su dato.'), ('Cuaderno', 'Ideas clave y ejemplos.', True), ('Ficha', 'Consulta rápida.')]
    def draw(t):
        w = (CW - 14) / 2
        for k, (a, z) in enumerate(two): card_block(b, M + k * (w + 14), t, w, 80, a, z)
        b.txt(M, t + 92, 'DOS POR FILA · EXPLICACIÓN DE TRES O MÁS LÍNEAS', 7.2, 'S', ACC)
        w3 = (CW - 28) / 3
        for k, item in enumerate(three): card_block(b, M + k * (w3 + 14), t + 112, w3, 64, item[0], item[1], len(item) > 2)
        b.txt(M, t + 186, 'TRES POR FILA · TÍTULOS CORTOS · UNA TARJETA OSCURA PARA LA OPCIÓN DESTACADA', 7.2, 'S', ACC)
    figure(b, key, cap, 196, draw)


def v_photo_labels(b, kind, key, cap):
    def draw(t):
        h = 300; b.photo(M, t, CW, h, focus_y=.45)
        pts = [(.69, .24, 'Tablero de referencias', 'image', -165, -4), (.76, .52, 'Composición en pantalla', 'layout', 10, 46), (.50, .74, 'Pruebas de página impresas', 'document', -210, 28)]
        for fx, fy, lab, ic, dx, dy in pts:
            px, py = M + fx * CW, t + fy * h
            b.circle(px, py, 4.5, WHITE, GOLD, 1.6)
            wpill = pdfmetrics.stringWidth(lab, 'S', 8.2) + 41
            lx = min(max(px + dx, M + 10), M + CW - wpill - 10); ly = py + dy
            b.line(px, py, lx + (wpill if lx < px else 0), ly + 12, WHITE, 1)
            b.pill(lx, ly, lab, icon=ic)
    figure(b, key, cap, 300, draw)


def v_crop_demo(b, kind, key, cap):
    specs = [('3:2 · todo el ancho', 3 / 2, .5), ('4:5 · junto a texto', 4 / 5, .3), ('1:1 · miniatura', 1, .32)]
    def draw(t):
        h = 150; x = M; gap = 18
        ws = [h * r for _, r, _ in specs]; scale = min(1, (CW - 2 * gap) / sum(ws)); h2 = h * scale
        for lab, r, fx in specs:
            w = h2 * r; b.photo(x, t, w, h2, focus_x=fx); b.txt(x, t + h2 + 8, lab, 8, 'S', ACC); x += w + gap
    figure(b, key, cap, 150 * min(1, (CW - 36) / (150 * (1.5 + .8 + 1))) + 22, draw)


def box(b, x, t, w, h, text, dark=False, pill=False):
    b.rect(x, t, w, h, INK if dark else SOFT, None, h / 2 if pill else 8)
    th = b.height(text, w - 12, 8.5, 10.5, 'S')
    b.para(x + 6, t + (h - th) / 2, text, w - 12, 8.5, 10.5, WHITE if dark else INK, 'S', align=1, keep=False)


def v_flow_diagram(b, kind, key, cap):
    def draw(t):
        y = t + 30; bh = 44; bw = 62; dw = 82; g = (CW - 5 * bw - dw) / 6
        xs = []; x = M
        steps = [('Completar la ficha', True, True), ('Investigar el tema', False, False), ('Redactar', False, False), ('Componer páginas', False, False)]
        for lab, dark, pill in steps:
            box(b, x, y, bw, bh, lab, dark, pill); xs.append(x); x += bw + g
        dx = x; cy = y + bh / 2
        c = b.c; p = c.beginPath(); p.moveTo(dx, H - cy); p.lineTo(dx + dw / 2, H - (cy - 34)); p.lineTo(dx + dw, H - cy); p.lineTo(dx + dw / 2, H - (cy + 34)); p.close()
        c.saveState(); c.setFillColor(WHITE); c.setStrokeColor(ACC); c.setLineWidth(1.2); c.drawPath(p, fill=1, stroke=1); c.restoreState()
        b.para(dx + 12, cy - 11, '¿Supera la revisión?', dw - 24, 8, 10, INK, 'S', align=1, keep=False)
        ex = dx + dw + g; box(b, ex, y, bw, bh, 'Entregar', True, True)
        for k in range(3): b.arrow(xs[k] + bw + 2, cy, xs[k + 1] - 3, cy, INK, 1.2)
        b.arrow(xs[3] + bw + 2, cy, dx - 3, cy, INK, 1.2)
        b.arrow(dx + dw + 2, cy, ex - 3, cy, INK, 1.2); b.txt(dx + dw + g / 2, cy - 15, 'Sí', 8.4, 'B', ACC, 'center')
        # vuelta: No
        bx = dx + dw / 2; by = cy + 34
        b.line(bx, by, bx, by + 30, INK, 1.2); b.line(bx, by + 30, xs[3] + bw / 2, by + 30, INK, 1.2)
        b.arrow(xs[3] + bw / 2, by + 30, xs[3] + bw / 2, y + bh + 3, INK, 1.2)
        b.txt(bx + 8, by + 6, 'No', 8.4, 'B', ACC)
        b.txt((xs[3] + bw / 2 + bx) / 2, by + 35, 'Corregir y volver a exportar', 7.6, 'M', MUTED, 'center')
        # leyenda
        ly = t + 140; lx = M
        for lab, kind2 in [('Inicio o final', 'pill'), ('Paso', 'box'), ('Decisión con salidas rotuladas', 'dia')]:
            if kind2 == 'pill': b.rect(lx, ly, 22, 11, INK, r=5.5)
            elif kind2 == 'box': b.rect(lx, ly, 22, 11, SOFT, r=3)
            else:
                p = c.beginPath(); p.moveTo(lx, H - ly - 5.5); p.lineTo(lx + 11, H - ly); p.lineTo(lx + 22, H - ly - 5.5); p.lineTo(lx + 11, H - ly - 11); p.close()
                c.saveState(); c.setStrokeColor(ACC); c.setFillColor(WHITE); c.drawPath(p, fill=1, stroke=1); c.restoreState()
            b.txt(lx + 28, ly + 1.5, lab, 7.8, 'M', MUTED); lx += 40 + pdfmetrics.stringWidth(lab, 'M', 7.8) + 18
    figure(b, key, cap, 154, draw)


def v_hierarchy_diagram(b, kind, key, cap):
    kids = [('README.md', 'Cómo empezar'), ('00_MANUAL .pdf', 'Para consultar'), ('01_MANUAL .md', 'Editable'), ('02_PROMPTS', 'Se copian o consultan'), ('03_SOURCE', 'Generador y recursos')]
    def draw(t):
        rw = 250; box(b, M + (CW - rw) / 2, t, rw, 34, '04_STYLE_MANUAL', True)
        n = len(kids); g = 8; w = (CW - (n - 1) * g) / n; ytop = t + 70
        b.line(M + CW / 2, t + 34, M + CW / 2, t + 52, INK, 1.1)
        b.line(M + w / 2, t + 52, M + CW - w / 2, t + 52, INK, 1.1)
        for k, (a, z) in enumerate(kids):
            x = M + k * (w + g); b.arrow(x + w / 2, t + 52, x + w / 2, ytop - 2, INK, 1.1, 4)
            b.rect(x, ytop, w, 52, WHITE, BORDER, 8); b.para(x + 6, ytop + 10, a, w - 12, 8.4, 10.5, INK, 'B', align=1, keep=False)
            b.para(x + 6, ytop + 32, z, w - 12, 7.4, 9, MUTED, 'M', align=1, keep=False)
        sub = {3: ['Aplicar manual', 'Revisión'], 4: ['Configuración', 'Paleta', 'Generador', 'Fuentes Inter', 'Imágenes']}
        for k, items in sub.items():
            x = M + k * (w + g); b.line(x + w / 2, ytop + 52, x + w / 2, ytop + 62, INK, .9)
            for j, it in enumerate(items):
                yy = ytop + 64 + j * 15; b.rect(x + 4, yy, w - 8, 12, NEUTRAL, r=4); b.txt(x + w / 2, yy + 2.5, it, 6.8, 'M', INK, 'center')
    figure(b, key, cap, 212, draw)


def v_timeline(b, kind, key, cap):
    ev = [('30/10/2026', 'Normas de nomenclatura 1.0'), ('01/11/2026', 'Paleta y fotografía de estudio'), ('04/11/2026', 'Fotografía de portada'), ('05/11/2026', 'Sistema editorial 1.1'), ('06/11/2026', 'Manual de estilo 1.0')]
    def draw(t):
        y = t + 46; b.line(M, y, M + CW, y, INK, 1.6); n = len(ev); step = CW / n
        for k, (d, txt) in enumerate(ev):
            x = M + step * k + step / 2; last = k == n - 1
            b.circle(x, y, 6, INK if last else WHITE, ACC, 1.6)
            b.txt(x, t + 16, d, 8.4, 'B', ACC, 'center')
            b.para(x - step / 2 + 6, y + 16, txt, step - 12, 8.6, 11, INK, 'M', align=1, keep=False)
        b.arrow(M + CW - 12, y, M + CW + 2, y, INK, 1.6)
    figure(b, key, cap, 96, draw)


def v_concept_map(b, kind, key, cap):
    nodes = [('Jerarquía', 'ordena', -170, -62), ('Retícula', 'alinea', 170, -62), ('Contraste', 'hace legible', -190, 40), ('Ejemplos', 'aclaran', 190, 40), ('Revisión', 'comprueba', 0, 88)]
    def draw(t):
        cx, cy = M + CW / 2, t + 100
        for name, rel, dx, dy in nodes:
            nx, ny = cx + dx, cy + dy
            b.line(cx, cy, nx, ny, ACC, 1.1)
            mx, my = (cx + nx) / 2, (cy + ny) / 2
            wl = pdfmetrics.stringWidth(rel, 'M', 7.6) + 10
            b.rect(mx - wl / 2, my - 6, wl, 12, WHITE, BORDER, 5); b.txt(mx, my - 3.5, rel, 7.6, 'M', ACC, 'center')
        for name, rel, dx, dy in nodes:
            nx, ny = cx + dx, cy + dy; w = 92
            b.rect(nx - w / 2, ny - 15, w, 30, SOFT, r=15); b.txt(nx, ny - 5, name, 9, 'S', INK, 'center')
        b.rect(cx - 70, cy - 20, 140, 40, INK, r=20); b.txt(cx, cy - 6, 'Documento legible', 10, 'B', WHITE, 'center')
    figure(b, key, cap, 206, draw)


def v_icon_sheet(b, kind, key, cap):
    items = [('info', 'Nota', 'Información complementaria'), ('book', 'Definición', 'Término y su significado'), ('warning', 'Advertencia', 'Riesgo o error frecuente'),
             ('bulb', 'Ejemplo', 'Caso que aplica la regla'), ('check', 'Comprobación', 'Lo que se revisa'), ('document', 'Documento', 'Bloque de portada e índice'),
             ('palette', 'Color', 'Identidad y paleta'), ('table', 'Tabla', 'Datos y cifras'), ('image', 'Imagen', 'Fotografías y pies'),
             ('flow', 'Diagrama', 'Relaciones y procesos'), ('eye', 'Revisión', 'Comprobar la exportación'), ('layers', 'Sistema', 'Configuración y módulos')]
    def draw(t):
        g = 10; w = (CW - 3 * g) / 4
        for k, (ic, a, z) in enumerate(items):
            x = M + (k % 4) * (w + g); y = t + (k // 4) * 54
            b.rect(x, y, w, 46, WHITE, BORDER, 9); b.rect(x + 9, y + 10, 26, 26, SOFT, r=7); b.icon(ic, x + 14, y + 15, 16, ACC)
            b.txt(x + 44, y + 11, a, 9, 'B'); b.para(x + 44, y + 24, z, w - 50, 7.4, 9.2, MUTED, 'M', align=0, keep=False)
    figure(b, key, cap, 154, draw)


def v_review_flow(b, kind, key, cap):
    labels = [('Exportar', 'PDF real', 'document'), ('Pasada 1', 'Composición', 'layout'), ('Pasada 2', 'Lectura', 'eye'), ('Corregir', 'Y reexportar', 'check'), ('Entregar', 'Con pendientes', 'layers')]
    def draw(t):
        n = len(labels); g = 12; w = (CW - (n - 1) * g) / n
        for i, (a, z, ic) in enumerate(labels):
            x = M + i * (w + g); dark = i == 2
            b.rect(x, t, w, 70, INK if dark else SOFT, r=11); b.icon(ic, x + 12, t + 11, 18, GOLD_DARK if dark else ACC)
            b.txt(x + 12, t + 38, a, 9, 'B', WHITE if dark else INK); b.txt(x + 12, t + 52, z, 7.8, 'M', HexColor('#D9DEE0') if dark else MUTED)
            if i < n - 1: b.icon('arrow', x + w + 1, t + 30, 10, ACC)
        b.line(M + 3 * (w + g) + w / 2, t + 70, M + 3 * (w + g) + w / 2, t + 84, ACC, .9, (2, 2))
        b.line(M + 1 * (w + g) + w / 2, t + 84, M + 3 * (w + g) + w / 2, t + 84, ACC, .9, (2, 2))
        b.arrow(M + 1 * (w + g) + w / 2, t + 84, M + 1 * (w + g) + w / 2, t + 73, ACC, .9, 4)
        b.txt(M + 2 * (w + g) + w / 2, t + 88, 'si la corrección cambia la composición', 7.4, 'M', MUTED, 'center')
    figure(b, key, cap, 100, draw)


# ---------------------------------------------------------------- símbolos
def poly_path(b, pts, x, t, s, fill=None, stroke=None, width=1, close=True):
    c = b.c; p = c.beginPath(); p.moveTo(x + pts[0][0] * s, H - (t + pts[0][1] * s))
    for a, z in pts[1:]: p.lineTo(x + a * s, H - (t + z * s))
    if close: p.close()
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(width); c.setLineJoin(1); c.setLineCap(1)
    c.drawPath(p, fill=1 if fill is not None else 0, stroke=1 if stroke is not None else 0); c.restoreState()


def symbol(b, kind, x, t, s):
    """Dibuja un símbolo de ejemplo dentro de un cuadrado de lado s (formas neutras, sin tema concreto)."""
    w = max(1, min(s * .028, 2.2))
    if kind == 'circulo':
        b.circle(x + .5 * s, t + .5 * s, s * .36, SOFT, ACC, w)
        b.circle(x + .5 * s, t + .5 * s, s * .08, GOLD)
    elif kind == 'triangulo':
        poly_path(b, [(.5, .12), (.9, .86), (.1, .86)], x, t, s, SOFT, ACC, w)
    elif kind == 'cuadrado':
        poly_path(b, [(.16, .16), (.84, .16), (.84, .84), (.16, .84)], x, t, s, SOFT, ACC, w)
        b.line(x + .16 * s, t + .5 * s, x + .84 * s, t + .5 * s, ACC, w * .7)
        b.line(x + .5 * s, t + .16 * s, x + .5 * s, t + .84 * s, ACC, w * .7)
    elif kind == 'estrella':
        pts = []
        for k in range(10):
            a = math.radians(-90 + k * 36); r = .4 if k % 2 == 0 else .17
            pts.append((.5 + math.cos(a) * r, .53 + math.sin(a) * r))
        poly_path(b, pts, x, t, s, SOFT, ACC, w)
    elif kind == 'emblema':
        # emblema de ejemplo: círculo con un triángulo inscrito y un punto central
        b.circle(x + .5 * s, t + .52 * s, s * .42, SOFT, ACC, w)
        poly_path(b, [(.5, .16), (.84, .74), (.16, .74)], x, t, s, None, INK, s * .035)
        b.circle(x + .5 * s, t + .55 * s, s * .06, GOLD)
    elif kind == 'libro':
        # libro abierto con la retícula en sus páginas y rayos de luz
        poly_path(b, [(.5, .5), (.08, .42), (.08, .86), (.5, .94)], x, t, s, WHITE, INK, w * 1.4)
        poly_path(b, [(.5, .5), (.92, .42), (.92, .86), (.5, .94)], x, t, s, WHITE, INK, w * 1.4)
        for k in range(4):
            f = .5 + k * .1
            b.line(x + .14 * s, t + (f + .0) * s, x + .44 * s, t + (f + .06) * s, BORDER, w)
            b.line(x + .56 * s, t + (f + .06) * s, x + .86 * s, t + f * s, BORDER, w)
        b.line(x + .5 * s, t + .5 * s, x + .5 * s, t + .94 * s, INK, w)
        for ang in range(-60, 61, 20):
            a = math.radians(ang - 90)
            b.line(x + .5 * s + math.cos(a) * .14 * s, t + .32 * s + math.sin(a) * .14 * s,
                   x + .5 * s + math.cos(a) * .26 * s, t + .32 * s + math.sin(a) * .26 * s, GOLD, w * 1.2)


def v_symbol_cover(b, kind, key, cap):
    def draw(t):
        w = 190; h, s, m = mini_page(b, M, t, w, True, True)
        cat = 'TEMA · SUBTEMA · ÁMBITO'
        b.rect(M + m, t + 24, pdfmetrics.stringWidth(cat, 'S', 4.4) + 10, 9, SOFT, r=3); b.txt(M + m + 5, t + 26.5, cat, 4.4, 'S', ACC)
        b.txt(M + m, t + 41, 'Título del', 21, 'B'); b.txt(M + m, t + 63, 'documento.', 21, 'B', ACC)
        b.txt(M + m, t + 92, 'Una frase que explica el asunto', 6.4, 'R')
        ss = 112; sx = M + (w - ss) / 2; sy = t + 108; symbol(b, 'emblema', sx, sy, ss)
        b.txt(M + m, sy + 30, 'PARTE A', 4.6, 'S'); b.line(M + m, sy + 37, sx + 30, sy + 37, ACC, .4); b.txt(M + m, sy + 40, 'Significado', 4.2, 'M', ACC)
        b.txt(M + w - m, sy + 76, 'PARTE B', 4.6, 'S', INK, 'right'); b.line(sx + 90, sy + 83, M + w - m, sy + 83, ACC, .4); b.txt(M + w - m, sy + 86, 'Significado', 4.2, 'M', ACC, 'right')
        b.txt(M + m, t + h - 40, 'Una frase de cierre', 6.6, 'B', ACC); b.txt(M + m, t + h - 31, 'en dos líneas y dos colores.', 6.6, 'B')
        notes = [(t + 26, 'Píldora con las materias del documento'), (t + 52, 'Título en dos líneas y dos colores'), (t + 94, 'Frase que explica el asunto'),
                 (sy + 40, 'Símbolo del tema dibujado, centrado y grande'), (sy + 84, 'Etiquetas: nombre de la parte y su significado'), (t + h - 34, 'Frase simbólica al pie, en dos colores')]
        for k, (py, text) in enumerate(notes):
            ty = t + 10 + k * 44
            b.circle(M + w - 4, py, 2, GOLD); b.line(M + w - 4, py, M + w + 30, ty + 5, ACC, .6); b.circle(M + w + 30, ty + 5, 1.6, ACC)
            b.para(M + w + 38, ty, text, CW - w - 38, 9.2, 12.6, INK, 'M', align=0, keep=False)
    figure(b, key, cap, 190 * 297 / 210, draw)


def v_closing_example(b, kind, key, cap):
    def draw(t):
        gap = 40; w = 150; x0 = M + (CW - 2 * w - gap) / 2
        items = [('libro', 'Una frase breve', 'que condensa el documento.', 'Imagen simbólica y frase'),
                 ('flow', 'Del encargo', 'a un documento útil.', 'Estructura del documento y frase')]
        for k, (kind2, a, z, lab) in enumerate(items):
            x = x0 + k * (w + gap); h, s, m = mini_page(b, x, t, w, True, False)
            if kind2 == 'libro':
                symbol(b, 'libro', x + (w - 92) / 2, t + 52, 92)
            else:
                yy = t + 70
                for j, tx in enumerate(['Ficha', 'Redacción', 'Revisión']):
                    bx = x + m + j * ((w - 2 * m) / 3); bw = (w - 2 * m) / 3 - 6
                    b.rect(bx, yy, bw, 30, INK if j == 2 else SOFT, r=5); b.txt(bx + bw / 2, yy + 12, tx, 5.6, 'S', WHITE if j == 2 else INK, 'center')
                    if j < 2: b.arrow(bx + bw + .5, yy + 15, bx + bw + 5.5, yy + 15, ACC, .7, 2.5)
                b.rect(x + m + 20, yy + 44, w - 2 * m - 40, 26, WHITE, BORDER, 5); b.txt(x + w / 2, yy + 54, 'Documento útil', 5.6, 'B', INK, 'center')
                b.arrow(x + w / 2, yy + 31, x + w / 2, yy + 43, ACC, .7, 2.5)
            b.txt(x + w / 2, t + 158, a, 7.4, 'B', ACC, 'center'); b.txt(x + w / 2, t + 168, z, 7.4, 'B', INK, 'center')
            b.txt(x, t + h + 8, lab, 8, 'S', ACC)
    figure(b, key, cap, 150 * 297 / 210 + 20, draw)


def v_symbol_sheet(b, kind, key, cap):
    items = [('circulo', 'Símbolo A', 'Significado'), ('triangulo', 'Símbolo B', 'Significado'),
             ('cuadrado', 'Símbolo C', 'Significado'), ('estrella', 'Símbolo D', 'Significado')]
    def draw(t):
        g = 10; w = (CW - 3 * g) / 4
        for k, (sym, a, z) in enumerate(items):
            x = M + k * (w + g); b.rect(x, t, w, 110, WHITE, BORDER, 10)
            symbol(b, sym, x + (w - 50) / 2, t + 12, 50)
            b.txt(x + w / 2, t + 74, a, 10.5, 'B', INK, 'center'); b.txt(x + w / 2, t + 90, z, 8.6, 'M', MUTED, 'center')
    figure(b, key, cap, 110, draw)


def v_symbol_cards(b, kind, key, cap):
    cards = [('circulo', 'Símbolo A', 'Describe la figura tal como se ve: su forma, sus partes y de dónde procede.',
              'Da la lectura del símbolo y nombra la fuente o el autor que la propone.', 'Traduce el significado a una situación cotidiana que el lector reconoce.'),
             ('triangulo', 'Símbolo B', 'Describe la figura tal como se ve: su forma, sus partes y de dónde procede.',
              'Da la lectura del símbolo y nombra la fuente o el autor que la propone.', 'Traduce el significado a una situación cotidiana que el lector reconoce.')]
    labels = ['QUÉ ES', 'QUÉ SIGNIFICA', 'EJEMPLO']
    def card_h(c):
        return max(116, 30 + sum(b.height(v, CW - 150, 9.2, 13) + 20 for v in c[2:]))
    def draw(t):
        y = t
        for c in cards:
            h = card_h(c); b.rect(M, y, CW, h, WHITE, BORDER, 10)
            b.rect(M + 12, y + 12, 96, 96, SOFT, r=9); symbol(b, c[0], M + 22, y + 22, 76)
            x = M + 124; b.txt(x, y + 13, c[1], 12, 'B'); yy = y + 32
            for lab, v in zip(labels, c[2:]):
                b.txt(x, yy, lab, 7, 'S', ACC); yy += 10; yy += b.para(x, yy, v, CW - 140, 9.2, 13, INK, 'R', align=0) + 8
            y += h + 10
    figure(b, key, cap, sum(card_h(c) for c in cards) + 10, draw)


def closing_page(b, first, second):
    """Última página del documento: imagen simbólica centrada y frase de cierre en dos colores."""
    flush_pending(b)
    b.page_start(grid=True)
    b.c.bookmarkPage('cierre'); b.c.addOutlineEntry('Cierre', 'cierre', 0)
    s = 250; symbol(b, 'libro', M + (CW - s) / 2, 230, s)
    b.txt(M + CW / 2, 520, first, 22, 'B', ACC, 'center')
    b.txt(M + CW / 2, 548, second, 22, 'B', INK, 'center')
    b.line(M + CW / 2 - 20, 594, M + CW / 2 + 20, 594, GOLD, 1.6)


VISUALS = {'symbol_cover': v_symbol_cover, 'measures_table': v_measures_table, 'closing_example': v_closing_example, 'symbol_sheet': v_symbol_sheet, 'symbol_cards': v_symbol_cards, 'use_flow': v_use_flow, 'config_sheet': v_config_sheet, 'tonal_scale': v_tonal_scale, 'palette_demo': v_palette_demo,
           'cover_variants': v_cover_variants, 'fixed_adjustable': v_fixed_adjustable, 'type_specimen': v_type_specimen,
           'identity_anatomy': v_identity_anatomy, 'title_examples': v_title_examples, 'heading_levels': v_heading_levels,
           'grid_page': v_grid_page, 'spacing_scale': v_spacing_scale, 'widow_fix': v_widow_fix, 'gap_fix': v_gap_fix,
           'table_anatomy': v_table_anatomy, 'contrast_table': v_contrast_table, 'cards_demo': v_cards_demo,
           'photo_labels': v_photo_labels, 'crop_demo': v_crop_demo, 'flow_diagram': v_flow_diagram,
           'hierarchy_diagram': v_hierarchy_diagram, 'timeline_diagram': v_timeline, 'concept_map': v_concept_map,
           'icon_sheet': v_icon_sheet, 'review_flow': v_review_flow}


# ---------------------------------------------------------------- montaje
def render(path, pages=None):
    b = Book(path, pages); b.block_pages_full = set()
    cover(b); index_page(b)
    for block in BLOCKS:
        if not block['opening']: raise ValueError(f"Falta !apertura en el bloque {block['code']}")
        for k, s in enumerate(block['sections']):
            section_head(b, block, s, opening=k == 0)
            if k == 0:
                opening_cards(b, block['opening'])
                render_lines(b, block['intro'])
            render_lines(b, s['lines'])
    flush_pending(b)
    b.c.showOutline(); b.c.save(); return b


def main():
    ap = argparse.ArgumentParser(description='Regenera el PDF del Manual de estilo y maquetación.')
    ap.add_argument('--output', type=Path, help='PDF alternativo para revisión; por defecto sustituye el PDF del manual.')
    a = ap.parse_args()
    out = a.output or (ROOT / CFG['document']['output'])
    tmp = HERE / '00_TEMP'; tmp.mkdir(exist_ok=True)
    first = render(tmp / '00_LAYOUT_PASS.pdf')
    final = render(out, first.found)
    if final.found != first.found:
        final = render(out, final.found)
    records = {'pages': final.page, 'figures': len(FIGS), 'tables': len(TABS),
               'sections': {f'{k[1]}.{k[2]}' if k[0] == 's' else f'bloque {k[1]}': v for k, v in final.found.items()}}
    (tmp / '01_LAYOUT_RECORDS.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    (tmp / '00_LAYOUT_PASS.pdf').unlink(missing_ok=True)
    print(json.dumps({'output': str(out), 'pages': final.page, 'figures': len(FIGS), 'tables': len(TABS)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
