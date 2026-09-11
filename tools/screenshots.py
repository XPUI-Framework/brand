"""Renders tools/examples.py into docs/images/ with a headless Chromium."""

import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from examples import EXAMPLES, page

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "images"
SCHEME = {"dark": 0, "light": 1}


def chromium() -> str | None:
    candidates = [os.environ.get("CHROME", "")]
    candidates += glob.glob(os.path.expanduser(
        "~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"))
    candidates += glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"))
    candidates += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    candidates += [shutil.which(n) or "" for n in ("chromium", "google-chrome", "chrome-headless-shell")]
    return next((c for c in candidates if c and os.access(c, os.X_OK)), None)


def main() -> int:
    browser = chromium()
    if not browser:
        print("skipped: no Chromium found; set CHROME to one")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for example in EXAMPLES:
            html = Path(tmp) / f"{example.name}.html"
            html.write_text(page(example))
            for scheme in example.schemes:
                suffix = "" if len(example.schemes) == 1 else f"-{scheme}"
                target = OUT / f"{example.name}{suffix}.png"
                subprocess.run([browser, "--headless", "--disable-gpu", "--hide-scrollbars",
                                "--force-device-scale-factor=2",
                                f"--window-size={example.width},{example.height}",
                                f"--blink-settings=preferredColorScheme={SCHEME[scheme]}",
                                f"--screenshot={target}", html.as_uri()],
                               check=True, capture_output=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
