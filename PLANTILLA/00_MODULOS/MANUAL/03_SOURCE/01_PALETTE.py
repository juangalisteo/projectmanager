"""Paleta del sistema editorial a partir de UN color principal.

Uso desde la carpeta del manual (04_STYLE_MANUAL en cada proyecto):

    python 03_SOURCE/01_PALETTE.py "#2E7D6B"
    python 03_SOURCE/01_PALETTE.py "#2E7D6B" --write ../00_CONFIG/00_PROJECT_CONFIG.json

Sin --write muestra los colores y los contrastes. Con --write guarda los colores
en el bloque identity.colors del JSON indicado.

Método: se imita la idea de las paletas tonales de Material (un mismo tono de
color en una escala de luminosidad de 0 a 100) usando la luminosidad L* de
CIELAB como «tono». No es la librería oficial de Google (HCT); es una
aproximación sin dependencias. La asignación de cada tono a una función
(tinta, acento de texto, superficie...) es una decisión editorial propia.
"""
from __future__ import annotations
import json, math, sys, argparse
from pathlib import Path


def hex_to_rgb(h: str):
    h = h.strip().lstrip('#')
    if len(h) != 6:
        raise ValueError(f'Color no válido: {h}. Usa el formato #RRGGBB.')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#' + ''.join(f'{round(max(0, min(1, c)) * 255):02X}' for c in rgb)


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delin(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


_WP = (0.95047, 1.0, 1.08883)


def rgb_to_lab(rgb):
    r, g, b = (_lin(c) for c in rgb)
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = (f(v / w) for v, w in zip((x, y, z), _WP))
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lab_to_rgb(L, a, b):
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200
    inv = lambda t: t ** 3 if t ** 3 > 216 / 24389 else (116 * t - 16) / (24389 / 27)
    x, y, z = (inv(t) * w for t, w in zip((fx, fy, fz), _WP))
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bl = 0.0557 * x - 0.2040 * y + 1.0570 * z
    return tuple(_delin(c) if c > 0 else c for c in (r, g, bl))


def lch(hexcolor):
    L, a, b = rgb_to_lab(hex_to_rgb(hexcolor))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def _in_gamut(rgb):
    return all(-1e-4 <= c <= 1 + 1e-4 for c in rgb)


def tone(hue, chroma, L):
    """Color con el tono de color `hue`, la luminosidad L* y la mayor saturación
    posible hasta `chroma` sin salir del espacio sRGB."""
    if L <= 0:
        return '#000000'
    if L >= 100:
        return '#FFFFFF'
    lo, hi = 0.0, chroma
    h = math.radians(hue)
    for _ in range(30):
        mid = (lo + hi) / 2
        if _in_gamut(lab_to_rgb(L, mid * math.cos(h), mid * math.sin(h))):
            lo = mid
        else:
            hi = mid
    return rgb_to_hex(lab_to_rgb(L, lo * math.cos(h), lo * math.sin(h)))


def luminance(hexcolor):
    r, g, b = (_lin(c) for c in hex_to_rgb(hexcolor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c1, c2):
    a, b = sorted((luminance(c1), luminance(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def palette(seed: str) -> dict:
    """Devuelve las funciones de color del sistema a partir del color elegido."""
    seed = rgb_to_hex(hex_to_rgb(seed))
    L, C, H = lch(seed)
    background = tone(H, 2.2, 98.2)
    colors = {
        'background': background,
        'surface': '#FFFFFF',
        'text': tone(H, min(C, 12), 21),
        'muted': tone(H, min(C, 9), 43),
        'accent': seed,
        'accent_surface': tone(H, min(C, 13), 92.5),
        'border': tone(H, min(C, 3), 88),
        'row': tone(H, min(C, 1.6), 96.5),
        'gradient_strong': tone(H, min(C, 24), 86),
        'gradient_soft': tone(H, min(C, 12), 93.5),
        'grid_line': tone(H, min(C, 1.5), 94.5),
    }
    # Acento de texto: el tono más claro (desde 40 hacia abajo) que cumple 4,5:1
    # sobre el fondo y sobre la superficie de acento. Material usa el tono 40
    # para «primary» en el tema claro; aquí se baja si el contraste no llega.
    for t in [x / 2 for x in range(80, 10, -1)]:
        cand = tone(H, C, t)
        if contrast(cand, background) >= 4.5 and contrast(cand, colors['accent_surface']) >= 4.5:
            colors['accent_text'] = cand
            break
    # Acento sobre fondo oscuro: el tono más oscuro (desde 70 hacia arriba) que cumple 4,5:1 sobre la tinta.
    for t in range(70, 100):
        cand = tone(H, C, t)
        if contrast(cand, colors['text']) >= 4.5:
            colors['accent_on_dark'] = cand
            break
    return colors


CHECKS = [
    ('Cuerpo / fondo', 'text', 'background', 4.5),
    ('Cuerpo / superficie', 'text', 'surface', 4.5),
    ('Cuerpo / fila alterna', 'text', 'row', 4.5),
    ('Cuerpo / superficie de acento', 'text', 'accent_surface', 4.5),
    ('Apoyo / fondo', 'muted', 'background', 4.5),
    ('Apoyo / superficie', 'muted', 'surface', 4.5),
    ('Acento de texto / fondo', 'accent_text', 'background', 4.5),
    ('Acento de texto / sup. de acento', 'accent_text', 'accent_surface', 4.5),
    ('Blanco / tinta (tarjeta oscura)', 'surface', 'text', 4.5),
    ('Acento / tinta (tarjeta oscura)', 'accent_on_dark', 'text', 4.5),
]
# Avisos: no bloquean, pero cambian el uso permitido del color.
NOTICES = [
    ('Acento gráfico sobre fondo', 'accent', 'background', 3.0,
     'Por debajo de 3:1 el acento gráfico solo decora (rellenos grandes, filetes). '
     'Las líneas, iconos o flechas que transmiten información usan el acento de texto.'),
]


def report(colors):
    rows = []
    for name, fg, bg, need in CHECKS:
        r = contrast(colors[fg], colors[bg])
        rows.append({'par': name, 'texto': colors[fg], 'fondo': colors[bg],
                     'contraste': round(r, 2), 'minimo': need, 'cumple': r >= need})
    return rows


def main():
    ap = argparse.ArgumentParser(description='Paleta editorial a partir de un color principal.')
    ap.add_argument('color', help='Color principal en formato #RRGGBB')
    ap.add_argument('--write', type=Path, help='JSON de configuración donde guardar identity.colors')
    a = ap.parse_args()
    colors = palette(a.color)
    print(json.dumps(colors, indent=2, ensure_ascii=False))
    print()
    for r in report(colors):
        mark = 'OK ' if r['cumple'] else 'NO '
        print(f"{mark} {r['contraste']:>5.2f}:1 (mín. {r['minimo']}) {r['par']}  {r['texto']} / {r['fondo']}")
    for name, fg, bg, need, msg in NOTICES:
        r = contrast(colors[fg], colors[bg])
        print(f"{'OK ' if r >= need else 'AVISO'} {r:>5.2f}:1 (ref. {need}) {name}  {colors[fg]} / {colors[bg]}")
        if r < need:
            print('      ' + msg)
    if any(not r['cumple'] for r in report(colors)):
        print('\nAtención: algún par de texto no cumple. Elige otro color o cambia ese uso.')
    if a.write:
        cfg = json.loads(a.write.read_text(encoding='utf-8'))
        cfg.setdefault('identity', {})['colors'] = colors
        cfg['identity']['primary_color'] = colors['accent']
        a.write.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'\nGuardado en {a.write}')


if __name__ == '__main__':
    main()
