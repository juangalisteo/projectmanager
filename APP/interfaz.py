"""Project Manager · ventana para crear proyectos nuevos a partir de PLANTILLA.

La lógica está en creador.py; aquí solo está la ventana. Mismo estilo que VideoFetch y
StreamFetch: fondo grafito, un único color de acento y pasos numerados.

Project:   Project Manager v1.1.0
Author:    Juan Bautista Galisteo Marqués (@juangalisteo)
"""
import colorsys
import os
import re
import subprocess
import sys
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox

sys.dont_write_bytecode = True  # no __pycache__ folders next to the program
APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP))
import creador  # noqa: E402

APP_VERSION = creador.VERSION

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # sharp text on scaled displays
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ProjectManager.App")
    except Exception:
        pass

# ── Palette: graphite with a single signal colour (gold, like the style manual) ──
BG = "#0B0B0C"
SURFACE = "#121214"
FIELD = "#18181B"
RAISED = "#202024"
BORDER = "#26262B"
TEXT = "#F4F4F5"
MUTED = "#A1A1AA"
FAINT = "#5E5E66"
ACCENT = "#C7A15B"
ACCENT_HOVER = "#D9B977"
ACCENT_PRESS = "#A88544"
ACCENT_SOFT = "#2A2214"
BORDER_STRONG = "#3A3A41"
SUCCESS = "#34D399"
DANGER = "#F87171"

SCALE = 1.0
UI_ZOOM = 0.8
F = {}

TYPE_KEYS = ["DOCUMENTO", "PROYECTO", "GENERAL"]
TYPE_HINTS = {
    "DOCUMENTO": "Libros, manuales, investigaciones y documentación.",
    "PROYECTO": "Software, aplicaciones, páginas web y desarrollo.",
    "GENERAL": "Cualquier otro trabajo, con lo mínimo para empezar.",
}


def px(value):
    return int(round(value * SCALE))


def pick_family(*names):
    available = set(tkfont.families())
    for name in names:
        if name in available:
            return name
    return "TkDefaultFont"


def setup_fonts(root):
    global SCALE
    root.tk.call("tk", "scaling", float(root.tk.call("tk", "scaling")) * UI_ZOOM)
    SCALE = root.winfo_fpixels("1i") / 96
    ui = pick_family("Segoe UI Variable Text", "Segoe UI", "Inter", "DejaVu Sans")
    display = pick_family("Segoe UI Variable Display", "Segoe UI", "Inter", "DejaVu Sans")
    semi = pick_family("Segoe UI Semibold", "Segoe UI Variable Text Semibold", "Inter SemiBold")
    mono = pick_family("Cascadia Mono", "Consolas", "DejaVu Sans Mono")

    def strong(size):
        if semi != "TkDefaultFont":
            return tkfont.Font(root, family=semi, size=size)
        return tkfont.Font(root, family=ui, size=size, weight="bold")

    F["title"] = tkfont.Font(root, family=display, size=28, weight="bold")
    F["lead"] = tkfont.Font(root, family=ui, size=11)
    F["body"] = tkfont.Font(root, family=ui, size=10)
    F["input"] = tkfont.Font(root, family=ui, size=11)
    F["small"] = tkfont.Font(root, family=ui, size=9)
    F["brand"] = strong(12)
    F["button"] = strong(10)
    F["chip"] = strong(9)
    F["mono"] = tkfont.Font(root, family=mono, size=9)
    F["eyebrow"] = tkfont.Font(root, family=mono, size=8)


def fit_panels(widget):
    """Sizes every Panel to its content, innermost first."""
    for child in widget.winfo_children():
        fit_panels(child)
    if isinstance(widget, Panel):
        widget.update_idletasks()
        widget._fit()


def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
              x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return canvas.create_polygon(points, smooth=True, **kw)


# ── Components ────────────────────────────────────────────────────────────
class Button(tk.Canvas):
    """Flat button with rounded corners, hover and disabled state."""

    KINDS = {
        "primary": dict(bg=ACCENT, hover=ACCENT_HOVER, press=ACCENT_PRESS, fg=BG, border=None,
                        off_bg="#1C1C20", off_fg="#55555C"),
        "secondary": dict(bg=FIELD, hover=RAISED, press="#2A2A2F", fg=TEXT, border=BORDER,
                          off_bg=FIELD, off_fg=FAINT),
        "ghost": dict(bg=None, hover=FIELD, press=RAISED, fg=MUTED, border=None, off_bg=None, off_fg=FAINT),
    }

    def __init__(self, parent, text, command, kind="secondary", height=40, padx=18):
        self.parent_bg = parent["bg"]
        super().__init__(parent, bg=self.parent_bg, highlightthickness=0, bd=0, cursor="hand2")
        self.text, self.command, self.kind = text, command, self.KINDS[kind]
        self.h, self.padx = px(height), px(padx)
        self.state, self.hover, self.pressed = "normal", False, False
        self.min_w = 0  # never shrinks, so «Copiado ✓» does not move the layout
        self.bind("<Enter>", lambda e: self._set(hover=True))
        self.bind("<Leave>", lambda e: self._set(hover=False, pressed=False))
        self.bind("<ButtonPress-1>", lambda e: self._set(pressed=True))
        self.bind("<ButtonRelease-1>", self._release)
        self._draw()

    def _set(self, **values):
        for key, value in values.items():
            setattr(self, key, value)
        self._draw()

    def _release(self, event):
        fire = self.pressed and self.hover and self.state == "normal"
        self._set(pressed=False)
        if fire and self.command:
            self.command()

    def _draw(self):
        k = self.kind
        self.delete("all")
        w = max(self.min_w, F["button"].measure(self.text) + 2 * self.padx)
        self.min_w = w
        tk.Canvas.configure(self, width=w, height=self.h)
        if self.state == "disabled":
            bg, fg = k["off_bg"], k["off_fg"]
        elif self.pressed and self.hover:
            bg, fg = k["press"], k["fg"] if k is not self.KINDS["ghost"] else TEXT
        elif self.hover:
            bg, fg = k["hover"], k["fg"] if k is not self.KINDS["ghost"] else TEXT
        else:
            bg, fg = k["bg"], k["fg"]
        bg = bg or self.parent_bg
        outline = k["border"] if k["border"] and self.state != "disabled" and not self.hover else bg
        rounded_rect(self, 1, 1, w - 1, self.h - 1, px(9), fill=bg, outline=outline)
        self.create_text(w / 2, self.h / 2, text=self.text, fill=fg, font=F["button"])

    def set_text(self, text):
        self.text = text
        self._draw()

    def set_state(self, state):
        self.state = state
        tk.Canvas.configure(self, cursor="hand2" if state == "normal" else "arrow")
        self._draw()


class Panel(tk.Canvas):
    """Container with a rounded background and thin border. Children go in .inner."""

    def __init__(self, parent, bg=SURFACE, border=BORDER, radius=16, pad=24, shrink=False):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0, width=1, height=1)
        self.fill, self.border, self.radius, self.pad = bg, border, px(radius), px(pad)
        self.shrink = shrink  # True: as wide as its content (not stretched)
        self.inner = tk.Frame(self, bg=bg)
        self.window = self.create_window(self.pad, self.pad, window=self.inner, anchor="nw")
        self.bind("<Configure>", self._redraw)
        self.inner.bind("<Configure>", self._fit)

    def _fit(self, event=None):
        # The height is set from the content's requested size. It must also be called
        # before the window opens (see fit_panels): Tk does not show a window item
        # that lies outside its canvas, so a 1 px canvas would never grow by itself.
        tk.Canvas.configure(self, height=self.inner.winfo_reqheight() + 2 * self.pad)
        if self.shrink:
            tk.Canvas.configure(self, width=self.inner.winfo_reqwidth() + 2 * self.pad)

    def _redraw(self, event):
        self.delete("shape")
        rounded_rect(self, 1, 1, event.width - 1, event.height - 1, self.radius,
                     fill=self.fill, outline=self.border, tags="shape")
        self.tag_lower("shape")
        if not self.shrink:
            self.itemconfigure(self.window, width=max(1, event.width - 2 * self.pad))

    def set_border(self, color):
        self.border = color
        self.itemconfigure("shape", outline=color)


class NameField(tk.Frame):
    """Name box like VideoFetch: text in the accent colour, accent border while typing
    and a small × to clear it."""

    def __init__(self, parent, variable, on_return):
        super().__init__(parent, bg=parent["bg"])
        self.variable = variable
        self.panel = Panel(self, bg=FIELD, border=BORDER, radius=10, pad=3)
        self.panel.pack(fill="x")
        row = tk.Frame(self.panel.inner, bg=FIELD)
        row.pack(fill="x")
        self.entry = tk.Entry(row, textvariable=variable, font=F["input"], bg=FIELD, fg=ACCENT,
                              disabledbackground=FIELD, disabledforeground=ACCENT_PRESS,
                              insertbackground=ACCENT, insertwidth=px(2), relief="flat", bd=0,
                              highlightthickness=0, selectbackground=ACCENT_SOFT, selectforeground=TEXT)
        self.entry.pack(side="left", fill="x", expand=True, padx=(px(8), 0), pady=px(4))
        self.clear = tk.Label(row, text="×", width=2, font=F["brand"], fg=FAINT, bg=FIELD, cursor="hand2")
        self.clear.pack(side="right", padx=(px(2), px(4)))
        self.clear.bind("<Enter>", lambda e: self.clear.configure(fg=ACCENT))
        self.clear.bind("<Leave>", lambda e: self.clear.configure(fg=FAINT))
        self.clear.bind("<Button-1>", self._clear)
        self.entry.bind("<FocusIn>", lambda e: self.panel.set_border(ACCENT))
        self.entry.bind("<FocusOut>", lambda e: self.panel.set_border(BORDER))
        self.entry.bind("<Return>", on_return)
        variable.trace_add("write", lambda *a: self._refresh())
        self._refresh()

    def _refresh(self):
        # The × is only shown when something is typed.
        self.clear.configure(text="×" if self.variable.get() else "")

    def _clear(self, event=None):
        if str(self.entry["state"]) == "normal":
            self.variable.set("")
            self.entry.focus_set()


class IconButton(tk.Canvas):
    """Tiny drawn button without text, copied from VideoFetch: "copy" (two sheets).
    Grey; accent colour on hover; a green ✓ for a moment when clicked."""

    def __init__(self, parent, kind, command, confirm=True, size=18):
        size = px(size)
        super().__init__(parent, width=size, height=size, bg=parent["bg"], highlightthickness=0, bd=0,
                         cursor="hand2")
        self.kind, self.command, self.confirm = kind, command, confirm
        self.size, self.color, self.done, self.state = size, FAINT, False, "normal"
        self.bind("<Enter>", lambda e: self._paint(ACCENT if self.state == "normal" else FAINT))
        self.bind("<Leave>", lambda e: self._paint(FAINT))
        self.bind("<Button-1>", self._click)
        self._draw()

    def _paint(self, color):
        self.color = color
        self._draw()

    def _draw(self):
        self.delete("all")
        s, w = self.size, max(1, px(1.4))
        color = self.color if self.state == "normal" else BORDER_STRONG
        if self.done:
            self.create_line(s * .2, s * .55, s * .42, s * .76, s * .82, s * .28, fill=SUCCESS, width=px(2))
        elif self.kind == "copy":
            self.create_rectangle(s * .35, s * .15, s * .85, s * .65, outline=color, width=w)
            self.create_rectangle(s * .15, s * .35, s * .65, s * .85, outline=color, width=w, fill=self["bg"])
        elif self.kind == "random":
            # circular arrow (reload): an open circle with an arrow head at its end
            w = max(2, px(1.8))
            self.create_arc(s * .18, s * .18, s * .82, s * .82, start=60, extent=290, style="arc",
                            outline=color, width=w)
            self.create_polygon(s * .58, s * .05, s * .86, s * .22, s * .56, s * .36, fill=color, outline=color)

    def _click(self, event):
        if self.state != "normal":
            return
        self.command()
        if self.confirm:
            self.done = True
            self._draw()
            self.after(1200, self._reset)

    def _reset(self):
        if not self.winfo_exists():
            return
        self.done = False
        self._draw()

    def set_state(self, state):
        self.state = state
        self.configure(cursor="hand2" if state == "normal" else "arrow")
        self._draw()


class SlimScrollbar(tk.Canvas):
    """Thin scrollbar for a text box, copied from VideoFetch.
    It appears on its own when there are more lines than fit. It can be dragged or clicked."""

    def __init__(self, parent, target):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0, width=px(12), height=1,
                         cursor="hand2")
        self.target, self.span, self.grab, self.hover = target, (0.0, 1.0), None, False
        target.configure(yscrollcommand=self.set)
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))
        self.bind("<Button-1>", self._press)
        self.bind("<B1-Motion>", self._drag)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, "grab", None))

    def set(self, first, last):
        self.span = (float(first), float(last))
        if self.span[0] <= 0 and self.span[1] >= 1:
            if self.winfo_manager():
                self.pack_forget()
        elif not self.winfo_manager():
            self.pack(side="right", fill="y", padx=(0, px(4)), pady=px(6), before=self.target)
        self._draw()

    def _hover(self, value):
        self.hover = value
        self._draw()

    def _draw(self):
        self.delete("all")
        h, w = self.winfo_height(), px(12)
        top, bottom = self.span[0] * h, self.span[1] * h
        color = ACCENT if self.hover or self.grab is not None else BORDER_STRONG
        rounded_rect(self, px(3), top + px(2), w - px(3), max(top + px(20), bottom - px(2)), px(3),
                     fill=color, outline=color)

    def _press(self, event):
        h = max(1, self.winfo_height())
        top, bottom = self.span[0] * h, self.span[1] * h
        # Click on the thumb: drag it. Click elsewhere: jump to that point.
        self.grab = event.y - top if top <= event.y <= bottom else (bottom - top) / 2
        self._drag(event)

    def _drag(self, event):
        h = max(1, self.winfo_height())
        self.target.yview_moveto((event.y - (self.grab or 0)) / h)
        self._draw()


class PaletteStrip(tk.Canvas):
    """Row of colour samples with their name below: a live preview of the palette."""

    ITEMS = [("background", "Fondo"), ("text", "Texto"), ("accent", "Acento"),
             ("accent_surface", "Recuadros"), ("border", "Bordes")]

    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0)
        self.box, self.gap = px(30), px(10)
        self.cell = max(self.box, max(F["small"].measure(t) for _, t in self.ITEMS)) + self.gap
        tk.Canvas.configure(self, width=self.cell * len(self.ITEMS), height=self.box + px(22))

    def show(self, colors):
        self.delete("all")
        for i, (key, text) in enumerate(self.ITEMS):
            cx = i * self.cell + self.cell / 2
            fill = colors[key] if colors else FIELD
            rounded_rect(self, cx - self.box / 2, 1, cx + self.box / 2, self.box, px(8), fill=fill, outline=BORDER)
            self.create_text(cx, self.box + px(12), text=text, fill=MUTED if colors else FAINT, font=F["small"])


class ColorPicker(tk.Toplevel):
    """Modern colour picker in the app's dark style (replaces the old Windows dialog).
    Big square = saturation (left → right) and brightness (top → bottom); bar = hue."""

    def __init__(self, root, initial, on_ok):
        super().__init__(root)
        self.withdraw()
        self.title("Color principal")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(root)
        self.on_ok, self.initial = on_ok, initial
        r, g, b = (int(initial[i:i + 2], 16) / 255 for i in (1, 3, 5))
        self.h, self.s, self.v = colorsys.rgb_to_hsv(r, g, b)
        self.size, self.bar = px(240), px(18)
        self.m = px(10)  # margin so the markers are never cut at the edges
        self.hex = tk.StringVar()

        frame = tk.Frame(self, bg=BG)
        frame.pack(padx=px(24), pady=px(22))
        label(frame, "Elige el color principal", "brand").grid(row=0, column=0, columnspan=3, sticky="w")
        label(frame, "Arrastra en el cuadro y en la barra, o escribe el código.", "small", MUTED).grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(px(2), px(16)))

        self.sv = tk.Canvas(frame, width=self.size + 2 * self.m, height=self.size + 2 * self.m, bg=BG,
                            highlightthickness=0, cursor="crosshair")
        self.sv.grid(row=2, column=0)
        self.sv_img = tk.PhotoImage(width=self.size, height=self.size)
        self.sv.create_image(self.m, self.m, image=self.sv_img, anchor="nw")
        self.hue = tk.Canvas(frame, width=self.bar, height=self.size + 2 * self.m, bg=BG, highlightthickness=0,
                             cursor="sb_v_double_arrow")
        self.hue.grid(row=2, column=1, padx=(px(2), 0))
        self.hue_img = tk.PhotoImage(width=self.bar, height=self.size)
        self.hue.create_image(0, self.m, image=self.hue_img, anchor="nw")
        self._draw_hue_bar()

        side = tk.Frame(frame, bg=BG)
        side.grid(row=2, column=2, sticky="n", padx=(px(20), 0), pady=(self.m, 0))
        eyebrow(side, "", "Nuevo").pack(anchor="w")
        self.new_box = tk.Canvas(side, width=px(110), height=px(56), bg=BG, highlightthickness=0)
        self.new_box.pack(anchor="w", pady=(px(4), px(12)))
        eyebrow(side, "", "Actual").pack(anchor="w")
        old_box = tk.Canvas(side, width=px(110), height=px(32), bg=BG, highlightthickness=0, cursor="hand2")
        old_box.pack(anchor="w", pady=(px(4), px(16)))
        rounded_rect(old_box, 1, 1, px(109), px(31), px(8), fill=initial, outline=BORDER)
        old_box.bind("<Button-1>", lambda e: self.set_hex(initial))
        eyebrow(side, "", "Código").pack(anchor="w")
        box = Panel(side, bg=FIELD, border=BORDER, radius=10, pad=10, shrink=True)
        box.pack(anchor="w", pady=(px(4), 0))
        self.entry = tk.Entry(box.inner, textvariable=self.hex, width=10, font=F["mono"], bg=FIELD, fg=ACCENT,
                              insertbackground=ACCENT, relief="flat", bd=0, highlightthickness=0)
        self.entry.pack()
        self.entry.bind("<KeyRelease>", lambda e: self._typed())

        buttons = tk.Frame(frame, bg=BG)
        buttons.grid(row=3, column=0, columnspan=3, sticky="e", pady=(px(20), 0))
        Button(buttons, "Cancelar", self.destroy, kind="ghost", height=40, padx=16).pack(side="left")
        Button(buttons, "Aceptar", self.accept, kind="primary", height=40, padx=24).pack(side="left",
                                                                                         padx=(px(10), 0))

        for widget, handler in ((self.sv, self._on_sv), (self.hue, self._on_hue)):
            widget.bind("<Button-1>", handler)
            widget.bind("<B1-Motion>", handler)
        self.bind("<Return>", lambda e: self.accept())
        self.bind("<Escape>", lambda e: self.destroy())

        self._draw_sv()
        self._refresh(update_entry=True)
        fit_panels(self)
        self.update_idletasks()
        x = root.winfo_rootx() + (root.winfo_width() - self.winfo_reqwidth()) // 2
        y = root.winfo_rooty() + (root.winfo_height() - self.winfo_reqheight()) // 3
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.deiconify()
        dark_title_bar(self)
        self.grab_set()
        self.entry.focus_set()

    # ── drawing ──
    def _draw_hue_bar(self):
        rows = []
        for y in range(self.size):
            r, g, b = colorsys.hsv_to_rgb(y / self.size, 1, 1)
            c = f"#{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"
            rows.append("{" + " ".join([c] * self.bar) + "}")
        self.hue_img.put(" ".join(rows))

    def _draw_sv(self):
        # pure colour of the hue; each pixel mixes it with white (saturation) and black (brightness)
        hr, hg, hb = colorsys.hsv_to_rgb(self.h, 1, 1)
        n = self.size - 1
        rows = []
        for y in range(self.size):
            v = 1 - y / n
            line = []
            for x in range(self.size):
                s = x / n
                line.append("#%02X%02X%02X" % (round(v * (1 - s + s * hr) * 255),
                                               round(v * (1 - s + s * hg) * 255),
                                               round(v * (1 - s + s * hb) * 255)))
            rows.append("{" + " ".join(line) + "}")
        self.sv_img.put(" ".join(rows))

    def _refresh(self, update_entry=False):
        n = self.size - 1
        self.sv.delete("marker")
        x, y = self.m + self.s * n, self.m + (1 - self.v) * n
        r = px(7)
        self.sv.create_oval(x - r, y - r, x + r, y + r, outline=BG, width=px(4), tags="marker")
        self.sv.create_oval(x - r, y - r, x + r, y + r, outline="#FFFFFF", width=px(2), tags="marker")
        self.hue.delete("marker")
        hy = self.m + self.h * self.size
        self.hue.create_rectangle(1, hy - px(3), self.bar - 1, hy + px(3), outline="#FFFFFF", width=px(2),
                                  tags="marker")
        color = self.color()
        self.new_box.delete("all")
        rounded_rect(self.new_box, 1, 1, px(109), px(55), px(10), fill=color, outline=BORDER)
        if update_entry:
            self.hex.set(color)
            self.entry.xview_moveto(0)  # always show the whole code, with its #

    def color(self):
        r, g, b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        return f"#{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"

    # ── events ──
    def _on_sv(self, event):
        n = self.size - 1
        self.s = min(max((event.x - self.m) / n, 0), 1)
        self.v = 1 - min(max((event.y - self.m) / n, 0), 1)
        self._refresh(update_entry=True)

    def _on_hue(self, event):
        self.h = min(max((event.y - self.m) / self.size, 0), 0.9999)
        self._refresh(update_entry=True)
        if not getattr(self, "_pending", False):  # redraw the square at most once per frame
            self._pending = True
            self.after(16, self._redraw_square)

    def _redraw_square(self):
        self._pending = False
        if self.winfo_exists():
            self._draw_sv()

    def _typed(self):
        if re.fullmatch(r"#?[0-9A-Fa-f]{6}", self.hex.get().strip()):
            self.set_hex(self.hex.get(), keep_entry=True)

    def set_hex(self, value, keep_entry=False):
        value = value.strip().lstrip("#")
        r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
        h, self.s, self.v = colorsys.rgb_to_hsv(r, g, b)
        if self.s > 0:  # a grey has no hue: keep the current one
            self.h = h
        self._draw_sv()
        self._refresh(update_entry=not keep_entry)

    def accept(self):
        self.on_ok(self.color())
        self.destroy()


class Chip(tk.Canvas):
    """Pill-shaped label."""

    def __init__(self, parent, text, fg=MUTED, font=None):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0)
        font = font or F["chip"]
        w, h = font.measure(text) + px(22), px(26)
        tk.Canvas.configure(self, width=w, height=h)
        rounded_rect(self, 1, 1, w - 1, h - 1, h / 2, fill=parent["bg"], outline=BORDER)
        self.create_text(w / 2, h / 2, text=text, fill=fg, font=font)


class Segmented(tk.Canvas):
    """Segmented selector: the chosen option is highlighted in the accent colour."""

    def __init__(self, parent, options, index=0, command=None, gap=0):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0, cursor="hand2")
        self.options, self.index, self.command, self.hovered = options, index, command, None
        self.font, self.inset, self.h, self.radius = F["button"], px(4), px(40), px(11)
        self.gap = px(gap)  # gap > 0: separate buttons instead of one joined bar
        widest = max(self.font.measure(o) for o in options) + px(34)
        self.widths = [widest] * len(options)
        self.w = sum(self.widths) + 2 * self.inset + self.gap * (len(options) - 1)
        tk.Canvas.configure(self, width=self.w, height=self.h)
        self.bind("<Motion>", lambda e: self._hover(self._hit(e.x)))
        self.bind("<Leave>", lambda e: self._hover(None))
        self.bind("<Button-1>", self._click)
        self._draw()

    def _hit(self, x):
        left = self.inset
        for i, width in enumerate(self.widths):
            if left <= x < left + width:
                return i
            left += width + self.gap
        return None

    def _hover(self, index):
        if index != self.hovered:
            self.hovered = index
            self._draw()

    def _click(self, event):
        index = self._hit(event.x)
        if index is not None and index != self.index:
            self.index = index
            self._draw()
            if self.command:
                self.command(index)

    def _draw(self):
        self.delete("all")
        if not self.gap:
            rounded_rect(self, 1, 1, self.w - 1, self.h - 1, self.radius, fill=FIELD, outline=BORDER)
        left = self.inset
        for i, (text, width) in enumerate(zip(self.options, self.widths)):
            if i == self.index:
                rounded_rect(self, left, self.inset, left + width, self.h - self.inset, self.radius - px(3),
                             fill=ACCENT, outline=ACCENT)
                color = BG
            else:
                if self.gap:  # each option is its own button
                    rounded_rect(self, left, self.inset, left + width, self.h - self.inset, self.radius - px(3),
                                 fill=FIELD, outline=BORDER)
                color = TEXT if i == self.hovered else MUTED
            self.create_text(left + width / 2, self.h / 2, text=text, fill=color, font=self.font)
            left += width + self.gap


class Toggle(tk.Canvas):
    """Small on/off button, as in VideoFetch: translucent red when off, green when on."""

    OFF = dict(fill="#2A1315", outline="#5C1F24", text="#F87171", hover="#FCA5A5")
    ON = dict(fill="#0E2A20", outline="#34D399", text="#34D399", hover="#6EE7B7")

    def __init__(self, parent, text, value=False, command=None):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0, cursor="hand2")
        self.text, self.value, self.command = text, value, command
        self.state, self.hover = "normal", False
        self.font = F["chip"]
        self.w, self.h = self.font.measure(text) + px(26), px(28)
        tk.Canvas.configure(self, width=self.w, height=self.h)
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<Button-1>", self._click)
        self._draw()

    def _set_hover(self, value):
        self.hover = value
        self._draw()

    def _click(self, event):
        if self.state != "normal":
            return
        self.value = not self.value
        self._draw()
        if self.command:
            self.command(self.value)

    def _draw(self):
        self.delete("all")
        if self.state == "disabled":
            fill, outline, color = FIELD, BORDER, FAINT
        else:
            look = self.ON if self.value else self.OFF
            fill, outline = look["fill"], look["outline"]
            color = look["hover"] if self.hover else look["text"]
        rounded_rect(self, 1, 1, self.w - 1, self.h - 1, px(8), fill=fill, outline=outline)
        self.create_text(self.w / 2, self.h / 2, text=self.text, fill=color, font=self.font)


def make_logo(parent):
    """Gold square with a 2×2 grid: the system's grid icon."""
    size = px(38)
    c = tk.Canvas(parent, width=size, height=size, bg=parent["bg"], highlightthickness=0, bd=0)
    rounded_rect(c, 0, 0, size, size, px(10), fill=ACCENT, outline=ACCENT)
    s, g = size * 0.24, size * 0.09  # same proportions as projectmanager.ico
    for ix in range(2):
        for iy in range(2):
            x = size / 2 - s - g / 2 + ix * (s + g)
            y = size / 2 - s - g / 2 + iy * (s + g)
            rounded_rect(c, x, y, x + s, y + s, px(2.5), fill=BG, outline=BG)
    return c


def window_icon(root):
    ico = APP / "projectmanager.ico"
    if sys.platform == "win32" and ico.exists():
        try:
            root.iconbitmap(str(ico))
            root.iconbitmap(default=str(ico))
            root.after(50, lambda: taskbar_icon(root, ico))
            return
        except tk.TclError:
            pass
    icon = tk.PhotoImage(width=32, height=32)
    icon.put(ACCENT, to=(0, 0, 32, 32))
    for x0, y0 in ((8, 8), (17, 8), (8, 17), (17, 17)):
        icon.put(BG, to=(x0, y0, x0 + 7, y0 + 7))
    root.iconphoto(True, icon)
    root._icon = icon


def taskbar_icon(root, ico):
    """Gives Windows the .ico frame of the exact size it needs (title bar and taskbar),
    so it does not stretch a smaller one and look blurry. Same as VideoFetch."""
    if sys.platform != "win32" or not ico.exists():
        return
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        user32.LoadImageW.restype = wintypes.HANDLE
        user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
                                      ctypes.c_int, ctypes.c_int, wintypes.UINT]
        user32.SendMessageW.restype = ctypes.c_ssize_t
        user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        user32.GetParent.restype = wintypes.HWND
        user32.GetParent.argtypes = [wintypes.HWND]
        root.update_idletasks()
        hwnd = user32.GetParent(root.winfo_id()) or root.winfo_id()
        image_icon, load_from_file, wm_seticon = 1, 0x10, 0x80
        for kind, metric in ((1, 11), (0, 49)):  # ICON_BIG / SM_CXICON, ICON_SMALL / SM_CXSMICON
            size = user32.GetSystemMetrics(metric)
            handle = user32.LoadImageW(None, str(ico), image_icon, size, size, load_from_file)
            if handle:
                user32.SendMessageW(hwnd, wm_seticon, kind, handle)
                root._taskbar_icons = getattr(root, "_taskbar_icons", []) + [handle]
    except Exception:
        pass


def dark_title_bar(root):
    """Dark title bar in the same colour as the window (Windows 10/11)."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        dwm = ctypes.windll.dwmapi
        dark = ctypes.c_int(1)
        for attribute in (20, 19):
            if dwm.DwmSetWindowAttribute(hwnd, attribute, ctypes.byref(dark), ctypes.sizeof(dark)) == 0:
                break
        r, g, b = (int(BG[i:i + 2], 16) for i in (1, 3, 5))
        color = ctypes.c_int(r | (g << 8) | (b << 16))
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(color), ctypes.sizeof(color))
    except Exception:
        pass


def label(parent, text="", font="body", fg=TEXT, **kw):
    return tk.Label(parent, text=text, font=F[font], fg=fg, bg=parent["bg"], **kw)


def eyebrow(parent, number, text):
    return label(parent, f"{number} — {text.upper()}" if number else text.upper(), "eyebrow", FAINT)


def open_folder(path):
    try:
        if sys.platform == "win32":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception:
        pass


def first_prompt(project):
    """The start prompt: 00_INICIO_CHAT.md holds only the prompt, so it is copied whole."""
    try:
        return (Path(project) / "00_INICIO_CHAT.md").read_text(encoding="utf-8").strip()
    except Exception:
        return ""


# ── Application ───────────────────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        setup_fonts(root)
        root.title("Project Manager")
        root.configure(bg=BG)
        window_icon(root)
        dark_title_bar(root)
        settings = creador.cargar_ajustes()
        self.settings = settings
        self.name = tk.StringVar()
        self.type_hint = tk.StringVar(value=TYPE_HINTS["DOCUMENTO"])
        self.color = tk.StringVar(value=settings.get("color", "#2E7D6B"))
        self.color_hint = tk.StringVar()
        self.destination = tk.StringVar(value=settings.get("destino", ""))
        self.status = tk.StringVar(value="Todo listo · Escribe el nombre del proyecto")
        self.type_index = 0
        self.use_original = bool(settings.get("identidad_original", False))
        self.last_project = None
        self.color.trace_add("write", lambda *a: self.update_color())
        self.build_ui()
        self.update_color()
        self.update_destination()
        self.fit_window()

    def build_ui(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, padx=px(36), pady=(px(28), px(30)))

        header = tk.Frame(frame, bg=BG)
        header.pack(fill="x")
        make_logo(header).pack(side="left")
        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left", padx=(px(12), 0))
        label(brand, "Project Manager", "brand").pack(anchor="w")
        label(brand, "Proyectos para trabajar con IA", "small", MUTED).pack(anchor="w")
        Chip(header, f"v{APP_VERSION}", font=F["mono"]).pack(side="right")

        label(frame, "Proyecto nuevo, listo para trabajar", "title").pack(anchor="w", pady=(px(34), px(6)))
        label(frame, "Elige nombre y destino · La carpeta saldrá con reglas, prompts y agentes de IA.",
              "lead", MUTED).pack(anchor="w", pady=(0, px(28)))

        card = Panel(frame)
        card.pack(fill="x")
        body = card.inner

        def divider():
            tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=px(18))

        def row(number, title, hint_var):
            line = tk.Frame(body, bg=SURFACE)
            line.pack(fill="x")
            text = tk.Frame(line, bg=SURFACE)
            text.pack(side="left", fill="x", expand=True)
            eyebrow(text, number, title).pack(anchor="w")
            label(text, textvariable=hint_var, font="body", fg=MUTED, wraplength=px(430),
                  justify="left").pack(anchor="w", pady=(px(4), 0))
            return line

        # 01 · Name
        eyebrow(body, "01", "Nombre del proyecto").pack(anchor="w", pady=(0, px(10)))
        # Same name box as VideoFetch: accent text and border, × to clear
        self.name_field = NameField(body, self.name, lambda e: self.create())
        self.name_field.pack(fill="x")
        self.entry = self.name_field.entry
        divider()

        # 02 · Type
        line = row("02", "Tipo", self.type_hint)
        Segmented(line, ["Documento", "Proyecto", "General"], command=self.on_type).pack(side="right")
        divider()

        # 03 · Colour
        line = row("03", "Color principal", self.color_hint)
        controls = tk.Frame(line, bg=SURFACE)
        controls.pack(side="right")
        self.color_mode = Segmented(controls, ["Color", "Predeterminado"],
                                    index=1 if self.use_original else 0, command=self.on_color_mode, gap=10)
        self.color_mode.pack(side="right")
        self.color_row = tk.Frame(body, bg=SURFACE)
        self.color_row.pack(fill="x", pady=(px(14), 0))
        # ↻ random colour (only in «Color» mode), the colour box (click = choose) and its code
        self.random_button = IconButton(self.color_row, "random", self.random_color, confirm=False, size=22)
        self.swatch = tk.Canvas(self.color_row, width=px(44), height=px(44), bg=SURFACE, highlightthickness=0,
                                cursor="hand2")
        self.swatch.pack(side="left")
        self.swatch.bind("<Button-1>", lambda e: self.pick_color())
        self.hexbox = Panel(self.color_row, bg=FIELD, border=BORDER, radius=10, pad=10, shrink=True)
        self.hexbox.pack(side="left", padx=(px(10), 0))
        self.hex_entry = tk.Entry(self.hexbox.inner, textvariable=self.color, width=9, font=F["mono"], bg=FIELD,
                                  fg=TEXT, disabledbackground=FIELD, disabledforeground=FAINT,
                                  insertbackground=ACCENT, relief="flat", bd=0, highlightthickness=0)
        self.hex_entry.pack()
        self.default_hex = tk.StringVar(value=creador.ORIGINAL_COLOR)
        self.palette_strip = PaletteStrip(self.color_row)
        self.palette_strip.pack(side="right")
        divider()

        # 04 · Assistants
        hint = tk.StringVar(value="Claude va siempre. Añade otro en caso de trabajar con él.")
        line = row("04", "Asistentes", hint)
        agents = tk.Frame(line, bg=SURFACE)
        agents.pack(side="right")
        self.codex = Toggle(agents, "ChatGPT", bool(self.settings.get("codex", False)))
        self.codex.pack(side="left")
        divider()

        # 05 · Destination
        self.destination_hint = tk.StringVar()
        line = row("05", "Carpeta de destino", self.destination_hint)
        Button(line, "Examinar", self.pick_destination).pack(side="right")

        # Status and actions
        status = tk.Frame(frame, bg=BG)
        status.pack(fill="x", pady=(px(22), px(14)))
        self.dot = tk.Canvas(status, width=px(10), height=px(10), bg=BG, highlightthickness=0)
        self.dot.pack(side="left", padx=(px(2), px(10)))
        self.set_dot(FAINT)
        label(status, textvariable=self.status, font="body", anchor="w", wraplength=px(760),
              justify="left").pack(side="left", fill="x", expand=True)
        tk.Frame(frame, bg=FIELD, height=px(4)).pack(fill="x")

        actions = tk.Frame(frame, bg=BG)
        actions.pack(fill="x", pady=(px(24), 0))
        # «Ver actividad», as in VideoFetch: shows what the program has done, with a copy icon
        self.details_button = Button(actions, "Ver actividad", self.toggle_details, kind="ghost",
                                     height=40, padx=14)
        self.details_button.pack(side="left")
        self.open_button = Button(actions, "Abrir carpeta", self.open_last, kind="ghost", height=40, padx=14)
        self.open_button.pack(side="left", padx=(px(4), 0))
        self.open_button.set_state("disabled")
        self.create_button = Button(actions, "Crear proyecto", self.create, kind="primary", height=48, padx=30)
        self.create_button.pack(side="right")
        self.copy_button = Button(actions, "Prompt · IA", self.copy_prompt, height=48)
        self.copy_button.pack(side="right", padx=(0, px(12)))
        self.copy_button.set_state("disabled")

        self.details = Panel(frame, bg=FIELD, radius=12, pad=12)
        self.log = tk.Text(self.details.inner, height=7, wrap="word", state="disabled", font=F["mono"],
                           bg=FIELD, fg=MUTED, relief="flat", bd=0, highlightthickness=0,
                           selectbackground=ACCENT_SOFT, padx=px(4), pady=px(2))
        self.log.pack(fill="both", expand=True)
        SlimScrollbar(self.details.inner, self.log)
        self.copy_icon = IconButton(self.details.inner, "copy", self.copy_log)
        self.copy_icon.place(relx=1.0, x=-px(18), y=px(2), anchor="ne")
        self.write_log(f"Project Manager v{APP_VERSION} · listo.")

    def fit_window(self):
        self.root.update_idletasks()
        fit_panels(self.root)
        self.root.update_idletasks()
        width = max(px(900), self.root.winfo_reqwidth())
        height = self.root.winfo_reqheight()
        x = max(0, (self.root.winfo_screenwidth() - width) // 2)
        y = max(0, (self.root.winfo_screenheight() - height) // 2 - px(30))
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(px(820), height)

    def grow_if_needed(self):
        """A long status message can take two lines: make the window taller if needed."""
        self.root.update_idletasks()
        need = self.root.winfo_reqheight()
        if need > self.root.winfo_height():
            self.root.geometry(f"{self.root.winfo_width()}x{need}")
            self.root.minsize(px(820), need)

    def toggle_details(self):
        if self.details.winfo_manager():
            self.details.pack_forget()
            self.details_button.set_text("Ver actividad")
        else:
            self.details.pack(fill="x", pady=(px(14), 0))
            self.details_button.set_text("Ocultar actividad")
        # The window takes exactly the height it needs, opened or closed.
        self.root.update_idletasks()
        fit_panels(self.details)
        self.root.update_idletasks()
        need = min(self.root.winfo_reqheight(), self.root.winfo_screenheight() - px(90))
        self.root.minsize(px(820), need)
        self.root.geometry(f"{self.root.winfo_width()}x{need}")

    def show_details(self):
        if not self.details.winfo_manager():
            self.toggle_details()

    def write_log(self, text):
        import datetime
        self.log.configure(state="normal")
        self.log.insert("end", f"{datetime.datetime.now():%H:%M:%S}  {text}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def copy_log(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log.get("1.0", "end-1c"))

    # ── Updates ──
    def set_dot(self, color):
        self.dot.delete("all")
        self.dot.create_oval(1, 1, px(9), px(9), fill=color, outline=color)

    def on_type(self, index):
        self.type_index = index
        self.type_hint.set(TYPE_HINTS[TYPE_KEYS[index]])

    def on_color_mode(self, index):
        self.use_original = index == 1
        self.update_color()

    def update_color(self):
        colors = None
        if self.use_original:
            value, ok = creador.ORIGINAL_COLOR, True
            colors = creador.paleta(None)
            self.color_hint.set("Dorado, azul pizarra y blanco roto: la paleta del sistema.")
        else:
            try:
                value, ok = creador.color_valido(self.color.get()), True
                colors = creador.paleta(value)
                self.color_hint.set("Pulsa ↻ para elegir un color aleatorio, o el cuadro para elegirlo tú.")
            except Exception:
                value, ok = "", False
                self.color_hint.set("Escribe el color como #RRGGBB o pulsa el cuadro para elegirlo.")
        self.swatch.delete("all")
        size = px(44)
        rounded_rect(self.swatch, 1, 1, size - 1, size - 1, px(10), fill=value if ok else FIELD, outline=BORDER)
        self.palette_strip.show(colors)
        # «Predeterminado» fixes the palette: no random button, no editing
        editable = not self.use_original
        self.hex_entry.configure(state="normal" if editable else "disabled",
                                 textvariable=self.color if editable else self.default_hex)
        self.swatch.configure(cursor="hand2" if editable else "arrow")
        if editable and not self.random_button.winfo_manager():
            self.random_button.pack(side="left", padx=(0, px(12)), before=self.swatch)
        elif not editable and self.random_button.winfo_manager():
            self.random_button.pack_forget()

    def random_color(self):
        self.color.set(creador.color_aleatorio())
        self.write_log(f"Color al azar: {self.color.get()}.")

    def update_destination(self):
        value = self.destination.get()
        self.destination_hint.set(value if value else "Elige dónde se creará la carpeta del proyecto")

    # ── Actions ──
    def pick_color(self):
        if self.use_original:
            return
        try:
            start = creador.color_valido(self.color.get())
        except creador.ErrorProyecto:
            start = "#2E7D6B"
        ColorPicker(self.root, start, self.color.set)

    def pick_destination(self):
        start = self.destination.get() or str(Path.home())
        chosen = filedialog.askdirectory(initialdir=start, title="Carpeta donde se creará el proyecto")
        if chosen:
            self.destination.set(str(Path(chosen)))
            self.update_destination()

    def create(self):
        options = creador.Opciones(
            nombre=self.name.get(),
            tipo=TYPE_KEYS[self.type_index],
            destino=Path(self.destination.get()) if self.destination.get() else Path(""),
            color=None if self.use_original else self.color.get(),
            codex=self.codex.value,
            autor=self.settings.get("autor", ""),
            github=self.settings.get("github", ""),
        )
        if not self.destination.get():
            self.fail("Elige una carpeta de destino que exista.")
            return
        self.create_button.set_state("disabled")
        self.status.set("Creando el proyecto…")
        self.write_log(f"Creando «{options.nombre.strip()}» · tipo {options.tipo.capitalize()} · "
                       f"{'identidad original' if options.color is None else 'color ' + str(options.color)} · "
                       f"{'Claude y ChatGPT' if options.codex else 'Claude'} · destino {options.destino}")
        self.set_dot(ACCENT)
        self.root.update_idletasks()
        try:
            result = creador.crear_proyecto(options)
        except creador.ErrorProyecto as exc:
            self.fail(str(exc))
            return
        finally:
            self.create_button.set_state("normal")
        creador.guardar_ajustes(destino=self.destination.get(), color=self.color.get(),
                                identidad_original=self.use_original,
                                codex=self.codex.value)
        self.last_project = result.ruta
        self.open_button.set_state("normal")
        self.copy_button.set_state("normal")
        self.set_dot(SUCCESS)
        self.status.set("Proyecto creado · Copia el prompt para iniciar el proyecto y comenzar.")
        self.write_log(f"Proyecto creado: {result.ruta} · {result.archivos} archivos.")
        self.grow_if_needed()
        open_folder(result.ruta)

    def fail(self, message):
        self.set_dot(DANGER)
        self.status.set(message)
        self.write_log("Error: " + message)
        self.show_details()  # the error is in the activity, with its copy icon
        self.grow_if_needed()

    def open_last(self):
        if self.last_project:
            open_folder(self.last_project)

    def copy_prompt(self):
        text = first_prompt(self.last_project) if self.last_project else ""
        if not text:
            messagebox.showinfo("Project Manager", "No encuentro el prompt. Ábrelo en 00_INICIO_CHAT.md.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.set_dot(SUCCESS)
        self.status.set("Prompt de inicio copiado. Pégalo como primer mensaje en un chat nuevo de Claude.")
        self.write_log("Prompt de inicio copiado al portapapeles.")


ERROR_LOG = APP / "projectmanager_errores.log"


def log_error(*exc):
    """If something fails, it is written to APP\\projectmanager_errores.log."""
    try:
        import datetime
        import traceback
        with ERROR_LOG.open("a", encoding="utf-8") as file:
            file.write(f"\n--- {datetime.datetime.now():%Y-%m-%d %H:%M:%S} · v{APP_VERSION} ---\n")
            file.write("".join(traceback.format_exception(*exc)))
    except Exception:
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.report_callback_exception = log_error
    try:
        App(root)
    except Exception:
        log_error(*sys.exc_info())
        raise
    root.mainloop()
