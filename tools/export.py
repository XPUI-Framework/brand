"""Writes every SVG in assets/ and candidates/ from the two alphabets."""

from pathlib import Path

from glyphs import BOLD, LIGHT
from mark import INK, PAPER, Drawing, compose, rects, svg

ROOT = Path(__file__).resolve().parent.parent

MARK = Drawing(size=32, glyphs=BOLD, gap=2, solid=True, frame=2)
MARK_16 = Drawing(size=16, glyphs=LIGHT, gap=2, solid=True, frame=1)

CANDIDATES = {
    "a-solid": MARK_16,
    "a-outline": Drawing(size=16, glyphs=LIGHT, gap=2, solid=False, frame=1),
    "b-solid": MARK,
    "b-outline": Drawing(size=32, glyphs=BOLD, gap=2, solid=False, frame=2),
}


def favicon() -> str:
    """mark-16 on its own paper ground, swapping the two when the OS is dark."""
    style = (f".p{{fill:{PAPER}}}.i{{fill:{INK}}}"
             f"@media (prefers-color-scheme:dark){{.p{{fill:{INK}}}.i{{fill:{PAPER}}}}}")
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
            f'<style>{style}</style><rect class="p" width="16" height="16"/>'
            f'<g class="i">{rects(compose(MARK_16))}</g></svg>\n')


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text)


def main() -> None:
    for name, drawing in (("mark", MARK), ("mark-16", MARK_16)):
        grid = compose(drawing)
        write(f"assets/{name}.svg", svg(grid, INK))
        write(f"assets/{name}-inverted.svg", svg(grid, PAPER))
    write("assets/favicon.svg", favicon())
    for name, drawing in CANDIDATES.items():
        write(f"candidates/{name}.svg", svg(compose(drawing), INK))


if __name__ == "__main__":
    main()
