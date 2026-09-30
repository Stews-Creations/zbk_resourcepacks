"""Package the released resource packs and inspect the result.

Usage: python .github/scripts/package_packs.py --output dist [--tag v1.0.0]

Writes one ZIP per released pack from the files tracked in this repository,
with pack.mcmeta at the ZIP root. The pack version comes from --tag: the
packaged pack.mcmeta and VERSION carry that version in place of the ${version}
placeholder that the tracked pack.mcmeta files use. Without --tag the ZIPs are
development builds versioned 0.0.0-dev.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]

# Released pack -> a path prefix that must be present in its ZIP.
PACKS = {
    "zombies_build_kit": "assets/zbk/",
    "zombies_build_kit_vivecraft_overlay": "assets/zbk/",
}
GENERATED_FILES = {"VERSION"}
LICENSE_DOCUMENTS = {"LICENSES/LICENSE.md", "LICENSES/NOTICE", "LICENSES/MEDIA_PERMISSION.md"}
LOCAL_ONLY = {"AGENTS.md", "AGENTS.override.md", "CLAUDE.md", "GEMINI.md", ".codex", ".claude", ".agents"}
VERSION_PLACEHOLDER = "${version}"
DEV_VERSION = "0.0.0-dev"


def release_version(tag):
    if tag is None:
        return DEV_VERSION
    match = re.fullmatch(r"v(\d+\.\d+\.\d+)", tag)
    if not match:
        raise SystemExit(f"Release tag {tag} must use vMAJOR.MINOR.PATCH")
    return match.group(1)


def tracked_files(pack):
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--", pack], cwd=ROOT, check=True, capture_output=True
    ).stdout.decode("utf-8")
    return sorted(name for name in listing.split("\0") if name)


def stamped_metadata(pack, version):
    raw = (ROOT / pack / "pack.mcmeta").read_text(encoding="utf-8")
    if VERSION_PLACEHOLDER not in raw:
        raise SystemExit(f"{pack}/pack.mcmeta must carry {VERSION_PLACEHOLDER} instead of a fixed version")
    stamped = raw.replace(VERSION_PLACEHOLDER, version)
    if json.loads(stamped)["zbk"]["version"] != version:
        raise SystemExit(f"{pack}/pack.mcmeta zbk.version must be {VERSION_PLACEHOLDER}")
    return stamped


def package(pack, archive_path, version):
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for name in tracked_files(pack):
            relative = Path(name).relative_to(pack).as_posix()
            if relative in GENERATED_FILES:
                raise SystemExit(f"{name} is written at packaging time; do not track it")
            if LOCAL_ONLY & set(Path(relative).parts):
                continue
            if relative == "pack.mcmeta":
                archive.writestr("pack.mcmeta", stamped_metadata(pack, version))
            else:
                archive.write(ROOT / name, relative)
        archive.writestr("VERSION", version + "\n")


def inspect(pack, archive_path, version):
    with ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise SystemExit(f"{archive_path.name} is damaged")
        names = set(archive.namelist())
        packaged_version = archive.read("VERSION").decode("utf-8").strip() if "VERSION" in names else None
        metadata = archive.read("pack.mcmeta").decode("utf-8") if "pack.mcmeta" in names else ""

    if packaged_version != version or VERSION_PLACEHOLDER in metadata:
        raise SystemExit(f"{archive_path.name} has no stamped pack metadata at its root")
    if json.loads(metadata)["zbk"]["version"] != version:
        raise SystemExit(f"{archive_path.name} pack.mcmeta version does not match {version}")
    if not any(name.startswith(PACKS[pack]) for name in names):
        raise SystemExit(f"{archive_path.name} has no Core assets under {PACKS[pack]}")
    missing = LICENSE_DOCUMENTS - names
    if missing:
        raise SystemExit(f"{archive_path.name} is missing {sorted(missing)}")
    leaked = [name for name in names if LOCAL_ONLY & set(Path(name).parts)]
    if leaked:
        raise SystemExit(f"{archive_path.name} contains local-only files: {sorted(leaked)[:5]}")
    return len(names)


def main():
    parser = argparse.ArgumentParser(description="Package the released resource packs.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tag", help="Release tag, such as v1.0.0; omit for a 0.0.0-dev build")
    args = parser.parse_args()

    version = release_version(args.tag)
    args.output.mkdir(parents=True, exist_ok=True)
    for pack in PACKS:
        archive_path = args.output / (f"{pack}-{args.tag}.zip" if args.tag else f"{pack}.zip")
        package(pack, archive_path, version)
        count = inspect(pack, archive_path, version)
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        print(f"{digest}  {archive_path.name}  ({count} files, version {version})")


if __name__ == "__main__":
    sys.exit(main())
