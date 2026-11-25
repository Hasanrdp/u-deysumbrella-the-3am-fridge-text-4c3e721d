#!/usr/bin/env python3
"""The 3AM Fridge Text — u-deysumbrella-the-3am-fridge-text-4c3e721d.

A smart fridge texts its owner at 3am. One line, 119 characters, written
to /output/entry.txt. The line is pinned below by its exact byte count and
SHA-256, and the program verifies the file it wrote against both before
it reports success, so a changed or truncated output can never slip out
as the entry.
"""

import hashlib
import os

LINE = "You open me at 3am like the answer is in here. It isn't. It's in your bed. I checked. I'm a fridge, I check everything."
EXPECTED_SHA256 = "5558c9f9951ad58b5f95b5fbf4ab03329ed72a83db5193d7b89f6ad69f74e6d2"
EXPECTED_BYTES = 119
MAX_CHARS = 140


def choose_output_dir():
    """The grader provides /output; a local trial falls back to ./output."""
    for candidate in ("/output", "output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise SystemExit("no writable output directory for entry.txt")


def verify(path, data):
    """Read the written file back and hold it to the pinned bytes, hash,
    character count and exact text. Any mismatch aborts the run."""
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("read-back bytes differ from the pinned line")
    if len(back) != EXPECTED_BYTES:
        raise SystemExit(f"byte count {len(back)} != pinned {EXPECTED_BYTES}")
    digest = hashlib.sha256(back).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"sha256 {digest} != pinned {EXPECTED_SHA256}")
    text = back.decode("utf-8")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise SystemExit(f"character count {len(text)} outside 1..{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("entry is only whitespace")
    return text


def main():
    out_dir = choose_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    text = verify(path, data)
    print(f"wrote {path}: {len(text)} chars, "
          f"sha256 {EXPECTED_SHA256[:12]}...")


if __name__ == "__main__":
    main()
