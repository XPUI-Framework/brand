"""The pages the manual's screenshots are taken from. Every mark on them is a file in assets/."""

from dataclasses import dataclass
from pathlib import Path

ASSETS = (Path(__file__).resolve().parent.parent / "assets").as_uri()

BASE_CSS = """
body { margin: 0; padding: 24px; font: 13px/1.4 ui-monospace, Menlo, monospace; background: #F2F2EE; color: #1A1A1A; }
img { display: block; }
.row { display: flex; align-items: end; gap: 28px; padding: 20px; }
.ink { background: #1A1A1A; color: #F2F2EE; }
figure { margin: 0; display: flex; flex-direction: column; align-items: center; gap: 6px; }
figcaption { font-size: 11px; white-space: nowrap; }
.pixelated { image-rendering: pixelated; }
"""


@dataclass(frozen=True)
class Example:
    name: str
    width: int
    height: int
    body: str
    css: str = ""
    schemes: tuple = ("light",)


def mark(file: str, size: int, cls: str = "") -> str:
    return f'<img class="{cls}" src="{ASSETS}/{file}" width="{size}" height="{size}" alt="">'


def figure(content: str, caption: str) -> str:
    return f"<figure>{content}<figcaption>{caption}</figcaption></figure>"


def themed(size: int) -> str:
    """The README pattern: the inverted mark when the reader's theme is dark."""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{ASSETS}/mark-inverted.svg">'
            f'{mark("mark.svg", size)}</picture>')


def sizes() -> Example:
    def row(suffix: str, cls: str) -> str:
        cells = [figure(mark(f"mark-16{suffix}.svg", 16), "16 · mark-16")]
        cells += [figure(mark(f"mark{suffix}.svg", s), f"{s} · mark") for s in (32, 64, 96, 128)]
        return f'<div class="row {cls}">{"".join(cells)}</div>'
    return Example("sizes", 600, 420, row("", "") + row("-inverted", "ink"))


def pixels() -> Example:
    return Example("pixels", 700, 340, '<div class="row">'
                   + figure(mark("mark-16.svg", 256, "pixelated"), "mark-16 · 16 grid · 1px strokes · shown at 16×")
                   + figure(mark("mark.svg", 256, "pixelated"), "mark · 32 grid · 2px strokes · shown at 8×")
                   + "</div>")


def inversion() -> Example:
    return Example("inversion", 520, 290, '<div style="display:flex">'
                   + f'<div class="row" style="padding:40px">{figure(mark("mark.svg", 192), "mark.svg on paper")}</div>'
                   + f'<div class="row ink" style="padding:40px">{figure(mark("mark-inverted.svg", 192), "mark-inverted.svg on ink")}</div>'
                   + "</div>")


def clear_space() -> Example:
    box = ('<div style="padding:32px;outline:1px dashed #1A1A1A;position:relative">'
           f'{mark("mark.svg", 128)}'
           '<span style="position:absolute;top:8px;left:50%;transform:translateX(-50%)">¼</span>'
           '<span style="position:absolute;left:10px;top:50%;transform:translateY(-50%)">¼</span></div>')
    return Example("clear-space", 300, 270, f'<div class="row">{figure(box, "a quarter of the width on every side")}</div>')


def misuse() -> Example:
    master = (Path(__file__).resolve().parent.parent / "assets/mark.svg").read_text()
    red = master.replace("#1A1A1A", "#D0392B").replace("<svg ", '<svg width="96" height="96" ', 1)
    stretched = master.replace("<svg ", '<svg width="128" height="72" preserveAspectRatio="none" ', 1)
    tiles = [
        (stretched, "don't stretch it"),
        (red, "don't recolour it"),
        (f'<img src="{ASSETS}/mark.svg" width="96" height="96" style="filter:drop-shadow(4px 4px 3px #1A1A1A)" alt="">', "no shadows, no effects"),
        (f'<img src="{ASSETS}/mark.svg" width="96" height="96" style="transform:perspective(300px) rotateY(-30deg) rotateZ(-8deg)" alt="">', "no perspective, no rotation"),
        (f'<img src="{ASSETS}/mark-32.png" width="96" height="96" style="image-rendering:auto;filter:blur(0.6px)" alt="">', "don't smooth-scale a PNG"),
        ('<div style="width:96px;height:96px;background:#1A1A1A;color:#F2F2EE;font:700 30px/1 Helvetica,sans-serif;'
         'display:grid;place-content:center;text-align:center">XP<br>UI</div>', "don't reset it in a font"),
        (f'<div style="padding:12px;background:#8A8A8A">{mark("mark.svg", 72)}</div>', "not on a mid-tone"),
        (f'<div style="width:96px;height:96px;background:#F2F2EE;display:grid;place-content:center;outline:1px solid #1A1A1A">'
         f'<div style="background:#fff;padding:6px">{mark("mark.svg", 64)}</div></div>', "no baked white box"),
    ]
    cells = "".join(f'<figure style="width:136px;height:150px;justify-content:end">{t}<figcaption style="white-space:normal;text-align:center">{c}</figcaption></figure>'
                    for t, c in tiles)
    return Example("misuse", 720, 440, f'<div class="row" style="flex-wrap:wrap;gap:24px 20px">{cells}</div>')


IN_USE_CSS = """
body { background: #ffffff; color: #1f2328; font-family: system-ui, sans-serif; }
.tab { display: flex; align-items: center; gap: 8px; width: 280px; padding: 8px 12px; border-radius: 8px 8px 0 0; background: #e8e8e8; font-size: 12px; }
.bar { height: 6px; background: #e8e8e8; margin-bottom: 20px; width: 560px; }
.header { display: flex; align-items: center; justify-content: space-between; width: 520px; padding: 12px 20px; border-bottom: 1px solid #d0d7de; margin-bottom: 24px; font: 13px ui-monospace, Menlo, monospace; }
.avatars { display: flex; align-items: end; gap: 20px; }
.avatars img { border-radius: 12%; outline: 1px solid #d0d7de; }
.card { display: flex; align-items: center; gap: 8px; font-size: 14px; }
.card img { border-radius: 4px; }
@media (prefers-color-scheme: dark) {
  body { background: #0d1117; color: #e6edf3; }
  .tab, .bar { background: #2b2b2b; }
  .header { border-color: #30363d; }
  .avatars img { outline-color: #30363d; }
}
"""


def in_use() -> Example:
    body = (f'<div class="tab"><img src="{ASSETS}/favicon.svg" width="16" height="16" alt="">XPUI · xpui.rs</div><div class="bar"></div>'
            f'<div class="header">{themed(32)}<span>docs&nbsp;&nbsp;github&nbsp;&nbsp;system</span></div>'
            f'<div class="avatars">{mark("mark-512.png", 96)}{mark("mark-512.png", 40)}{mark("mark-512.png", 20)}'
            f'<div class="card">{mark("mark-512.png", 20)}<b>XPUI-Framework</b>/xpui-framework</div></div>')
    return Example("in-use", 620, 280, body, IN_USE_CSS, ("light", "dark"))


README_CSS = """
body { background: #ffffff; color: #1f2328; font: 14px/1.5 -apple-system, system-ui, sans-serif; padding: 32px; }
.badges { display: flex; gap: 4px; margin-bottom: 16px; }
.badge { font: 11px/20px Verdana, sans-serif; color: #fff; display: flex; border-radius: 3px; overflow: hidden; }
.badge b { background: #555; padding: 0 6px; font-weight: normal; } .badge i { font-style: normal; padding: 0 6px; }
h1 { font: 600 32px/1.25 ui-monospace, Menlo, monospace; margin: 12px 0 16px; padding-bottom: 8px; border-bottom: 1px solid #d1d9e0; }
.alert { border-left: 4px solid #9a6700; padding: 8px 16px; } .alert b { color: #9a6700; display: block; margin-bottom: 4px; }
@media (prefers-color-scheme: dark) {
  body { background: #0d1117; color: #f0f6fc; }
  h1 { border-color: #3d444d; }
  .alert { border-color: #d29922; } .alert b { color: #d29922; }
}
"""


def readme() -> Example:
    body = ('<div class="badges"><span class="badge"><b>CI</b><i style="background:#4c1">passing</i></span>'
            '<span class="badge"><b>license</b><i style="background:#007ec6">MIT</i></span></div>'
            f'{themed(64)}<h1>xpui</h1>'
            '<div class="alert"><b>⚠ Warning</b>Under heavy development. Not production-ready. '
            'The API can break without notice. Use at your own risk.</div>')
    return Example("readme", 640, 330, body, README_CSS, ("light", "dark"))


EXAMPLES = [sizes(), pixels(), inversion(), clear_space(), misuse(), in_use(), readme()]


def page(example: Example) -> str:
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<style>{BASE_CSS}{example.css}</style></head><body>{example.body}</body></html>')
