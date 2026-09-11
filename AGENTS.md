# `brand`

## What this is

The XPUI mark and every file made from it. `assets/` is generated and copied into other
repositories; `docs/manual.md` says which file goes where and the rules of use.
**Nothing in `assets/` or `docs/images/` is edited by hand** — change `tools/` and rebuild.

## The gate

```bash
./build-and-test.sh
```

```text
the masters are two tones on the grid · every coordinate is an integer · each inverted file is its master's geometry · the rasters are ink and paper at their sizes · documented paths resolve
```

It regenerates everything first, so a green run proves the committed files are what the tools
make. Read the real exit code.

## Style that bites here

- **Two tones.** Ink `#1A1A1A` and paper `#F2F2EE`, in `tools/mark.py` and nowhere else.
- **The letters are holes.** The masters stay transparent; only the rasters are opaque.
- **Integer coordinates.** A pixel is a `<rect>` on the grid, or the mark is not pixel art.
- **A screenshot shows real files.** `tools/examples.py` points every image at `assets/`.

## Git

Never stage, never commit, never push without being asked, each time. No assistant
self-attribution in a commit message. Never rewrite a commit that exists.
