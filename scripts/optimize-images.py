#!/usr/bin/env python3
"""Optimize website images with free local tools: ImageMagick + cwebp.

Usage:
  python3 scripts/optimize-images.py input_dir output_dir [--max-width 1920] [--quality 82]

Outputs:
  - resized original-format image for jpg/png/webp inputs
  - webp version for jpg/png inputs
  - copied svg/gif/avif files
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

RASTER = {".jpg", ".jpeg", ".png", ".webp"}
COPY_ONLY = {".svg", ".gif", ".avif"}


def require(cmd: str) -> None:
    if shutil.which(cmd) is None:
        raise SystemExit(f"Missing required command: {cmd}")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def relative_output(src: Path, input_dir: Path, output_dir: Path) -> Path:
    return output_dir / src.relative_to(input_dir)


def optimize_raster(src: Path, dest: Path, max_width: int, quality: int) -> list[Path]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    created: list[Path] = []

    magick_cmd = [
        "magick",
        str(src),
        "-auto-orient",
        "-strip",
        "-resize",
        f"{max_width}x{max_width}>",
    ]

    if ext in {".jpg", ".jpeg"}:
        magick_cmd += ["-sampling-factor", "4:2:0", "-quality", str(quality)]
    elif ext == ".png":
        magick_cmd += ["-define", "png:compression-level=9"]
    elif ext == ".webp":
        magick_cmd += ["-quality", str(quality)]

    run(magick_cmd + [str(dest)])
    created.append(dest)

    if ext in {".jpg", ".jpeg", ".png"}:
        webp_dest = dest.with_suffix(".webp")
        run(["cwebp", "-quiet", "-q", str(quality), str(dest), "-o", str(webp_dest)])
        created.append(webp_dest)

    return created


def copy_asset(src: Path, dest: Path) -> list[Path]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return [dest]


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize images for static websites.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--max-width", type=int, default=1920)
    parser.add_argument("--quality", type=int, default=82)
    args = parser.parse_args()

    require("magick")
    require("cwebp")

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")
    if input_dir == output_dir:
        raise SystemExit("Input and output directories must be different")

    files = [p for p in input_dir.rglob("*") if p.is_file()]
    created: list[Path] = []
    skipped: list[Path] = []

    for src in files:
        ext = src.suffix.lower()
        dest = relative_output(src, input_dir, output_dir)
        if ext in RASTER:
            created.extend(optimize_raster(src, dest, args.max_width, args.quality))
        elif ext in COPY_ONLY:
            created.extend(copy_asset(src, dest))
        else:
            skipped.append(src)

    total_bytes = sum(p.stat().st_size for p in created if p.exists())
    print(f"optimized_files={len(created)}")
    print(f"skipped_files={len(skipped)}")
    print(f"output_dir={output_dir}")
    print(f"output_bytes={total_bytes}")
    if skipped:
        print("skipped:")
        for path in skipped:
            print(f"- {path.relative_to(input_dir)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
