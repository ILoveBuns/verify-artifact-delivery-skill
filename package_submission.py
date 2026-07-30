#!/usr/bin/env python3
"""Build a minimal competition ZIP containing only runtime skill files."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / "skills"
OUTPUT = ROOT / "dist" / "benchflow-skill-lift-submission.zip"
EXCLUDED_PARTS = {"agents", "evals", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc"}


def include(path: Path) -> bool:
    relative = path.relative_to(SKILLS)
    return (
        path.is_file()
        and not EXCLUDED_PARTS.intersection(relative.parts)
        and path.suffix not in EXCLUDED_SUFFIXES
    )


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(SKILLS.rglob("*")):
        if include(path):
            archive.write(path, Path("skills") / path.relative_to(SKILLS))

print(OUTPUT)
