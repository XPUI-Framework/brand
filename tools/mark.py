"""Composes the mark on a pixel grid and writes it as SVG."""

from dataclasses import dataclass

INK = "#1A1A1A"
PAPER = "#F2F2EE"
LINES = ("XP", "UI")


@dataclass(frozen=True)
class Drawing:
    size: int
    glyphs: dict
    gap: int
    solid: bool
    frame: int


def compose(drawing: Drawing) -> list[list[bool]]:
    """True where the pixel is ink."""
    size = drawing.size
    glyph = len(next(iter(drawing.glyphs.values())))
    origin = (size - (2 * glyph + drawing.gap)) // 2
    grid = [[drawing.solid] * size for _ in range(size)]
    if not drawing.solid:
        for i in range(size):
            for t in range(drawing.frame):
                for x, y in ((i, t), (i, size - 1 - t), (t, i), (size - 1 - t, i)):
                    grid[y][x] = True
    for row, line in enumerate(LINES):
        for col, letter in enumerate(line):
            left = origin + col * (glyph + drawing.gap)
            top = origin + row * (glyph + drawing.gap)
            for y, pixels in enumerate(drawing.glyphs[letter]):
                for x, pixel in enumerate(pixels):
                    if pixel == "X":
                        grid[top + y][left + x] = not drawing.solid
    return grid


def rects(grid: list[list[bool]]) -> str:
    """One <rect> per horizontal run of ink, every coordinate an integer."""
    out = []
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            start = x
            while x < len(row) and row[x]:
                x += 1
            out.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1"/>')
    return "".join(out)


def svg(grid: list[list[bool]], fill: str) -> str:
    size = len(grid)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'shape-rendering="crispEdges" fill="{fill}">{rects(grid)}</svg>\n')
