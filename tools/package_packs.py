"""Package each installable Core, map, and Vivecraft resource pack."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
PACKS = (
    "zombies_build_kit",
    "zombies_build_kit_vivecraft_overlay",
    "zbk_nacht_der_untoten",
    "zbk_der_eisendrache",
    "zbk_der_eisendrache_vivecraft_overlay",
)
RUNTIME_ASSET_SUFFIXES = {
    ".json",
    ".mcmeta",
    ".ogg",
    ".otf",
    ".png",
    ".properties",
    ".ttf",
    ".vsh",
    ".fsh",
}
ROOT_FILES = {
    "pack.mcmeta",
    "pack.png",
    "README.md",
    "LICENSE.md",
    "MEDIA_PERMISSION.md",
    "NOTICE",
    "VERSION",
}


def package(pack_name: str) -> tuple[Path, int, int]:
    pack = ROOT / pack_name
    if not (pack / "pack.mcmeta").is_file():
        raise FileNotFoundError(f"Missing resource pack metadata: {pack / 'pack.mcmeta'}")
    output = OUTPUT / f"{pack_name}.zip"
    included = 0
    skipped_assets = 0
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(pack.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(pack)
            if any(part.startswith(".") for part in relative.parts):
                continue
            if relative.parts[0] == "assets":
                if path.suffix.lower() not in RUNTIME_ASSET_SUFFIXES:
                    skipped_assets += 1
                    continue
            elif relative.parts[0] == "LICENSES":
                pass
            elif len(relative.parts) == 1 and relative.name in ROOT_FILES:
                pass
            else:
                continue
            archive.write(path, relative.as_posix())
            included += 1
    return output, included, skipped_assets


if __name__ == "__main__":
    for name in PACKS:
        output, included, skipped = package(name)
        print(f"{output.relative_to(ROOT)} ({included} files; skipped {skipped} non-runtime assets)")
