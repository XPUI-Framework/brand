#!/bin/sh
# Proves assets/ and the documentation: two tones, the grid, and every path they name.
set -u
cd "$(dirname "$0")/.."
INK="#1A1A1A"
PAPER="#F2F2EE"
failed=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

pass() { echo "ok      $1"; }
fail() { echo "FAILED  $1"; printf '%s\n' "$2" | sed 's/^/        /'; failed=1; }

colours() { magick "$1" -alpha off -unique-colors txt: | tail -n +2 | awk '{print $3}' | sort | tr '\n' ' '; }

# With shape-rendering stripped, an off-grid edge anti-aliases and shows up as a third colour.
two_tones() {
  out=""
  for pair in "mark.svg $PAPER" "mark-16.svg $PAPER" "mark-inverted.svg $INK" "mark-16-inverted.svg $INK"; do
    set -- $pair
    sed 's/ *shape-rendering="[^"]*"//g' "assets/$1" > "$tmp/aa.svg"
    rsvg-convert -w 512 -h 512 -b "$2" "$tmp/aa.svg" -o "$tmp/aa.png"
    got=$(colours "$tmp/aa.png")
    [ "$got" = "$INK $PAPER " ] || out="$out$1: $got
"
  done
  [ -z "$out" ] && pass "the masters are two tones on the grid" || fail "the masters are two tones on the grid" "$out"
}

integer_coordinates() {
  out=$(grep -oE '(x|y|width|height)="[0-9.]+"' assets/*.svg candidates/*.svg | grep -E '"[0-9]+\.[0-9]+"')
  [ -z "$out" ] && pass "every coordinate is an integer" || fail "every coordinate is an integer" "$out"
}

same_geometry() {
  out=""
  for m in mark mark-16; do
    strip='s/ fill="#[0-9A-F]*"//'
    [ "$(sed "$strip" "assets/$m.svg")" = "$(sed "$strip" "assets/$m-inverted.svg")" ] || out="$out$m-inverted.svg differs from $m.svg
"
  done
  [ -z "$out" ] && pass "each inverted file is its master's geometry" || fail "each inverted file is its master's geometry" "$out"
}

rasters() {
  out=""
  for spec in "mark-16.png 16x16" "mark-32.png 32x32" "mark-512.png 512x512" \
              "apple-touch-icon.png 180x180" "social-1280x640.png 1280x640"; do
    set -- $spec
    size=$(magick identify -format '%wx%h' "assets/$1")
    got=$(colours "assets/$1")
    [ "$size" = "$2" ] || out="$out$1: $size, not $2
"
    [ "$got" = "$INK $PAPER " ] || out="$out$1: $got
"
  done
  frames=$(magick identify -format '%wx%h ' assets/favicon.ico)
  [ "$frames" = "16x16 32x32 48x48 " ] || out="${out}favicon.ico: $frames
"
  [ -z "$out" ] && pass "the rasters are ink and paper at their sizes" || fail "the rasters are ink and paper at their sizes" "$out"
}

# The text outside code fences and inline code: an example is not a link.
prose() { awk '/^```/ { fenced = !fenced; next } !fenced' "$1" | sed 's/`[^`]*`//g'; }

# Markdown links and HTML src/srcset, relative to the file that names them.
documented_paths() {
  out=""
  for doc in README.md docs/manual.md candidates/README.md; do
    dir=$(dirname "$doc")
    for target in $(prose "$doc" | grep -oE '\]\([^)#]+|(src|srcset)="[^"]+"' | sed -E 's/^\]\(//; s/^(src|srcset)="//; s/"$//' | grep -vE '^(https?:|mailto:)'); do
      [ -e "$dir/$target" ] || out="$out$doc: $target
"
    done
  done
  [ -z "$out" ] && pass "documented paths resolve" || fail "documented paths resolve" "$out"
}

two_tones
integer_coordinates
same_geometry
rasters
documented_paths
exit $failed
