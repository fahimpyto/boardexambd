"""Stage only the public website files into dist/ for deployment.

The source tree contains build tooling, design files and a large PDF source.
Cloudflare should only receive the files that are actually part of the site.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from seo_config import ALL_PAGES

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

PUBLIC_DIRS = ("assets", "md", "ssc-26-routine")
PUBLIC_FILES = ("sitemap.xml", "robots.txt", "llms.txt")

MAX_FILE_SIZE = 25 * 1024 * 1024  # Cloudflare Workers static asset limit
MAX_FILES = 20_000


def copy_file(source: Path, target: Path) -> None:
    if not source.is_file():
        raise SystemExit(f"Missing public file: {source.relative_to(ROOT)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    for page in ALL_PAGES:
        copy_file(ROOT / page["file"], DIST / page["file"])

    for name in PUBLIC_DIRS:
        source = ROOT / name
        if not source.is_dir():
            raise SystemExit(f"Missing public directory: {name}")
        shutil.copytree(source, DIST / name)

    for name in PUBLIC_FILES:
        copy_file(ROOT / name, DIST / name)

    files = [path for path in DIST.rglob("*") if path.is_file()]
    oversized = [path for path in files if path.stat().st_size > MAX_FILE_SIZE]
    if oversized:
        details = "\n".join(
            f"  {path.relative_to(DIST)} ({path.stat().st_size / 1024 / 1024:.1f} MB)"
            for path in oversized
        )
        raise SystemExit(f"Files exceed Cloudflare's 25 MiB limit:\n{details}")
    if len(files) > MAX_FILES:
        raise SystemExit(f"Deployment has {len(files)} files; Cloudflare's limit is {MAX_FILES}")

    total = sum(path.stat().st_size for path in files)
    print(
        f"Staged {len(ALL_PAGES)} pages, {len(files)} files, "
        f"{total / 1024 / 1024:.1f} MB into dist/"
    )


if __name__ == "__main__":
    main()
