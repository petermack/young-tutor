#!/usr/bin/env python3
"""Check the young-tutor skill and plugin files. Exit 1 if a check fails."""

import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_skill import OUT, ROOT, SKILL_DIR, skill_files  # noqa: E402

errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def rel(path):
    return path.relative_to(ROOT).as_posix()


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{rel(path)}: not valid JSON ({exc})")
        return {}


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


# SKILL.md
skill_md = SKILL_DIR / "SKILL.md"
text = skill_md.read_text(encoding="utf-8")
meta = frontmatter(text)
check(meta is not None, "SKILL.md: no YAML frontmatter")
meta = meta or {}
name = meta.get("name", "")
description = meta.get("description", "")
check(re.fullmatch(r"[a-z0-9-]{1,64}", name), f"SKILL.md: bad name {name!r}")
check(name == SKILL_DIR.name, f"SKILL.md: name {name!r} is not the folder name {SKILL_DIR.name!r}")
check(0 < len(description) <= 200, f"SKILL.md: description has {len(description)} characters (1 to 200)")
check("<" not in description and ">" not in description, "SKILL.md: description has < or >")
check(len(text.splitlines()) <= 500, "SKILL.md: more than 500 lines")

# Every reference file exists and SKILL.md uses it.
refs_dir = SKILL_DIR / "references"
named = set(re.findall(r"references/([\w.-]+\.md)", text))
for ref in sorted(named):
    check((refs_dir / ref).is_file(), f"SKILL.md: references/{ref} does not exist")
for path in sorted(refs_dir.glob("*.md")):
    check(path.name in named, f"{rel(path)}: SKILL.md does not use this file")
    for other in re.findall(r"`([\w.-]+\.md)`", path.read_text(encoding="utf-8")):
        check((refs_dir / other).is_file(), f"{rel(path)}: {other} does not exist")

# JSON examples in the skill are valid.
for path in sorted(SKILL_DIR.rglob("*.md")):
    for block in re.findall(r"```json\n(.*?)```", path.read_text(encoding="utf-8"), re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}: JSON example is not valid ({exc})")

# Plugin and marketplace manifests.
market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
entries = {p.get("name"): p for p in market.get("plugins", [])}
check(name in entries, f"marketplace.json: no plugin named {name!r}")
if name in entries:
    source = ROOT / entries[name].get("source", "")
    manifest = source / ".claude-plugin" / "plugin.json"
    check(manifest.is_file(), f"marketplace.json: {rel(manifest)} does not exist")
    if manifest.is_file():
        plugin = load_json(manifest)
        check(plugin.get("name") == name, "plugin.json: name is not the skill name")
        check(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")), "plugin.json: bad version")
    check((source / "skills" / name / "SKILL.md").is_file(), "plugin: skill is not in skills/<name>/")

# Learner data stays out of Git.
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
check("learner/" in gitignore, ".gitignore: no line 'learner/'")

# The ZIP for upload agrees with the skill files.
if not OUT.is_file():
    errors.append(f"{rel(OUT)} does not exist. Run: python3 scripts/package_skill.py")
else:
    with zipfile.ZipFile(OUT) as zf:
        in_zip = {n: zf.read(n) for n in zf.namelist()}
    on_disk = {arcname: path.read_bytes() for path, arcname in skill_files()}
    check(in_zip == on_disk, f"{rel(OUT)} is out of date. Run: python3 scripts/package_skill.py")

if errors:
    print("FAIL")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print(f"OK: {name} ({len(description)}-character description)")
