#!/usr/bin/env python3
"""One-line office joke entry for make.fun.

Writes exactly one line to /output/entry.txt (UTF-8, 1-200 chars,
no trailing newline). Deterministic, Python 3 stdlib only.
Output directory fallback chain:
MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> temp dir.
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY = (
    "I tap my badge at the office door every morning and it still says "
    "access denied, which is the most honest performance feedback I've "
    "ever received."
)

def validate(entry):
    """Gate: reject empty / whitespace-only / >200-char entries."""
    if not isinstance(entry, str) or not entry.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if entry != entry.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if len(entry) > 200:
        raise ValueError(f"entry too long: {len(entry)} > 200 characters")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    return entry


def _candidates():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        yield Path(env)
    yield Path("/output")
    yield Path(__file__).resolve().parent / "output"
    yield Path(tempfile.gettempdir())


def main():
    entry = validate(ENTRY)
    for directory in _candidates():
        try:
            directory.mkdir(parents=True, exist_ok=True)
            target = directory / "entry.txt"
            with open(target, "w", encoding="utf-8", newline="") as f:
                f.write(entry)
            print(f"wrote {target} ({len(entry)} chars)")
            return 0
        except OSError:
            continue
    print("error: no writable output directory", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
