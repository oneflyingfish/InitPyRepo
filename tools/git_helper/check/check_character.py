from pathlib import Path
import os


def check_only_assic(files):
    ok = True

    if isinstance(files, str):
        files = [files]

    for f in files:
        if not os.path.exists(f):
            continue
        txt = Path(f).read_text(encoding="utf-8")
        for nr, line in enumerate(txt.splitlines(), 1):
            if any(ord(ch) > 255 for ch in line):
                print(f"{f}:{nr} contains illegal characters, remove them please.")
                ok = False
    return ok
