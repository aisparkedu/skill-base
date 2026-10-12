#!/usr/bin/env python3
"""Normalize an image to a fixed canvas without stretching or cropping."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_hex_color(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("background must be a 6-digit hex color")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("background must be hexadecimal") from exc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Contain an image on a fixed-size canvas, preserving aspect ratio."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument(
        "--background", type=parse_hex_color, default=parse_hex_color("F8F1E5")
    )
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        parser.error("width and height must be positive")

    with Image.open(args.input) as source:
        source = source.convert("RGBA")
        scale = min(args.width / source.width, args.height / source.height)
        size = (
            max(1, round(source.width * scale)),
            max(1, round(source.height * scale)),
        )
        resized = source.resize(size, Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (args.width, args.height), (*args.background, 255))
        position = ((args.width - size[0]) // 2, (args.height - size[1]) // 2)
        canvas.alpha_composite(resized, position)

        args.output.parent.mkdir(parents=True, exist_ok=True)
        canvas.convert("RGB").save(args.output, format="PNG", optimize=True)

    print(f"Saved {args.output} ({args.width}x{args.height})")


if __name__ == "__main__":
    main()
