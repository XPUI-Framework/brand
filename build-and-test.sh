#!/bin/sh
# Rebuilds everything generated, then proves it. Read the exit code.
set -eu
cd "$(dirname "$0")"
for tool in python3 rsvg-convert magick; do
  command -v "$tool" >/dev/null || { echo "missing: $tool"; exit 1; }
done
echo "·· the SVGs";        python3 tools/export.py
echo "·· the rasters";     tools/rasters.sh
echo "·· the screenshots"; python3 tools/screenshots.py
echo "·· the checks";      tools/check.sh
