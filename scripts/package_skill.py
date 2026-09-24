#!/usr/bin/env python3
"""Build dist/young-tutor.zip for upload in Claude (Customize > Skills).

The ZIP has the skill folder at its root:

    young-tutor/
        SKILL.md
        references/...
"""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "plugins" / "young-tutor" / "skills" / "young-tutor"
OUT = ROOT / "dist" / "young-tutor.zip"
IGNORE = {".DS_Store", "__pycache__"}


def skill_files():
    """Return the files of the skill, sorted, as (path on disk, path in ZIP)."""
    files = []
    for path in sorted(SKILL_DIR.rglob("*")):
        if path.is_file() and not IGNORE.intersection(path.parts):
            arcname = f"{SKILL_DIR.name}/{path.relative_to(SKILL_DIR).as_posix()}"
            files.append((path, arcname))
    return files


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, arcname in skill_files():
            # Fixed time stamp, so that the same files give the same ZIP.
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
    sys.exit(0)
