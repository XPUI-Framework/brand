#!/bin/sh
# Every PNG and the ICO in assets/, opaque, from the SVG masters: ink on paper, and
# each mark again as paper on ink.
set -eu
cd "$(dirname "$0")/../assets"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
nodate="-define png:exclude-chunks=date,time"

# $1 master, $2 size in pixels, $3 output
on_paper() {
  rsvg-convert -w "$2" -h "$2" "$1" -o "$tmp/render.png"
  magick "$tmp/render.png" -background "#F2F2EE" -alpha remove -alpha off $nodate "$3"
}

# The inverted master on an ink ground: the white square with black letters.
on_ink() {
  rsvg-convert -w "$2" -h "$2" "$1" -o "$tmp/render.png"
  magick "$tmp/render.png" -background "#1A1A1A" -alpha remove -alpha off $nodate "$3"
}

on_paper mark-16.svg 16 mark-16.png
on_paper mark.svg 32 mark-32.png
on_paper mark.svg 512 mark-512.png

on_ink mark-16-inverted.svg 16 mark-16-inverted.png
on_ink mark-inverted.svg 32 mark-32-inverted.png
on_ink mark-inverted.svg 512 mark-512-inverted.png

on_paper mark-16.svg 48 "$tmp/48.png"
magick mark-16.png mark-32.png "$tmp/48.png" $nodate favicon.ico

on_paper mark.svg 160 "$tmp/touch.png"
magick -size 180x180 xc:"#1A1A1A" "$tmp/touch.png" -gravity center -composite $nodate apple-touch-icon.png

on_paper mark.svg 384 "$tmp/social.png"
magick -size 1280x640 xc:"#F2F2EE" "$tmp/social.png" -gravity center -composite $nodate social-1280x640.png
