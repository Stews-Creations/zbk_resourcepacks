"""Validate supported ZBK Core, map, and Vivecraft resource-pack combinations."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = "zombies_build_kit"
CORE_VR = "zombies_build_kit_vivecraft_overlay"
NACHT = "zbk_nacht_der_untoten"
DE = "zbk_der_eisendrache"
DE_VR = "zbk_der_eisendrache_vivecraft_overlay"
PACK_NAMES = (CORE, CORE_VR, NACHT, DE, DE_VR)
COMBINATIONS = {
    "Core only": (CORE,),
    "Core + Nacht": (NACHT, CORE),
    "Core + Nacht + Vivecraft": (CORE_VR, NACHT, CORE),
    "Core + Der Eisendrache": (DE, CORE),
    "Core + Der Eisendrache + Vivecraft": (DE_VR, CORE_VR, DE, CORE),
}
OLD_NAMESPACES = ("zbk_map_1", "zbk_map_2")
MAP_NAMESPACES = ("zbk_nacht_der_untoten", "zbk_der_eisendrache")
MINECRAFT_OVERRIDES = (
    "atlases/blocks.json",
    "font/default.json",
    "items/carved_pumpkin.json",
    "lang/en_us.json",
    "sounds/empty.ogg",
    "textures/gui/sprites/hud/hotbar.png",
    "textures/gui/sprites/hud/hotbar_selection.png",
    "textures/gui/sprites/hud/hotbar_offhand_left.png",
    "textures/gui/sprites/hud/hotbar_offhand_right.png",
)


def parse_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON: {path.relative_to(ROOT)} ({exc})")
        return None


def relative_path(pack: Path, namespace: str, category: str, identifier: str, suffix: str) -> Path:
    name = identifier if Path(identifier).suffix else identifier + suffix
    return pack / "assets" / namespace / category / name


def find_asset(pack_roots: tuple[Path, ...], namespace: str, category: str, identifier: str, suffix: str) -> Path | None:
    return next((path for pack in pack_roots
                 if (path := relative_path(pack, namespace, category, identifier, suffix)).is_file()), None)


def validate_pack_metadata(pack: Path, errors: list[str]) -> None:
    metadata_path = pack / "pack.mcmeta"
    if not metadata_path.is_file():
        errors.append(f"Missing {pack.name}/pack.mcmeta")
        return
    data = parse_json(metadata_path, errors)
    if not isinstance(data, dict):
        return
    description = data.get("pack", {}).get("description")
    if not description:
        errors.append(f"Missing pack description in {pack.name}/pack.mcmeta")
    bounds = (data.get("pack", {}).get("min_format"), data.get("pack", {}).get("max_format"))
    if bounds != ([88, 0], [88, 0]):
        errors.append(f"Unexpected Minecraft 26.2 resource format bounds in {pack.name}/pack.mcmeta: {bounds}")
    version = data.get("zbk", {}).get("version")
    version_file = pack / "VERSION"
    if version != "1.0.0" or not version_file.is_file() or version_file.read_text(encoding="ascii").strip() != version:
        errors.append(f"{pack.name} must declare matching ZBK version 1.0.0 in pack.mcmeta and VERSION")


def custom_namespaces(pack_roots: tuple[Path, ...]) -> set[str]:
    return {p.name for pack in pack_roots for p in (pack / "assets").iterdir() if p.is_dir() and p.name not in {"minecraft"}}


def validate_combination(label: str, pack_names: tuple[str, ...], errors: list[str]) -> int:
    packs = tuple(ROOT / name for name in pack_names)
    seen_namespaces: dict[str, str] = {}
    for pack in packs:
        if not pack.is_dir():
            errors.append(f"{label}: missing pack folder {pack.name}")
            continue
        for ns_dir in (pack / "assets").iterdir() if (pack / "assets").is_dir() else ():
            if ns_dir.is_dir() and ns_dir.name != "minecraft":
                seen_namespaces.setdefault(ns_dir.name, pack.name)
        for path in pack.rglob("*"):
            if not path.is_file():
                continue
            try:
                raw = path.read_bytes()
            except OSError as exc:
                errors.append(f"Cannot read {path.relative_to(ROOT)} ({exc})")
                continue
            if path.suffix.lower() in {".json", ".mcmeta"}:
                parse_json(path, errors)
            if path.suffix.lower() in {".json", ".mcmeta", ".properties", ".txt"}:
                text = raw.decode("utf-8-sig", errors="ignore")
                for old_namespace in OLD_NAMESPACES:
                    if old_namespace in text:
                        errors.append(f"Removed legacy namespace {old_namespace} remains in {path.relative_to(ROOT)}")

    namespaces = custom_namespaces(packs)
    for pack in packs:
        assets = pack / "assets"
        for path in assets.rglob("*.json"):
            data = parse_json(path, errors)
            if data is None:
                continue
            source = path.relative_to(ROOT).as_posix()

            def walk(node, key=None, inside_textures=False):
                if isinstance(node, dict):
                    if node.get("type") == "reference" and isinstance(node.get("id"), str):
                        ns, sep, identifier = node["id"].partition(":")
                        if sep and ns in namespaces and not find_asset(packs, ns, "font", identifier, ".json"):
                            errors.append(f"{label}: missing font {node['id']} in {source}")
                    for child_key, value in node.items():
                        walk(value, child_key, inside_textures or child_key == "textures")
                elif isinstance(node, list):
                    for value in node:
                        walk(value, key, inside_textures)
                elif isinstance(node, str) and ":" in node:
                    namespace, _, identifier = node.partition(":")
                    if namespace not in namespaces:
                        return
                    if key in {"model", "parent"} and not find_asset(packs, namespace, "models", identifier, ".json"):
                        errors.append(f"{label}: missing model {node} in {source}")
                    elif (key == "file" or inside_textures) and not find_asset(packs, namespace, "textures", identifier, ".png"):
                        errors.append(f"{label}: missing texture {node} in {source}")

            walk(data)

        for path in (assets / "minecraft").rglob("*") if (assets / "minecraft").is_dir() else ():
            if path.is_file() and path.suffix.lower() in {".json", ".mcmeta"}:
                data = parse_json(path, errors)
                if data is not None:
                    walk(data)

    # Check custom sound-event and clip references across every enabled pack.
    event_sets: dict[str, set[str]] = {}
    sound_jsons: list[tuple[Path, dict]] = []
    for pack in packs:
        assets = pack / "assets"
        for path in assets.glob("*/sounds.json"):
            namespace = path.parent.name
            data = parse_json(path, errors)
            if isinstance(data, dict):
                event_sets.setdefault(namespace, set()).update(data)
                sound_jsons.append((path, data))
    for path, events in sound_jsons:
        namespace = path.parent.name
        source = path.relative_to(ROOT).as_posix()
        def check_sound(node):
            if isinstance(node, dict):
                nested = node.get("type") == "event"
                name = node.get("name")
                if isinstance(name, str):
                    target_ns, sep, identifier = name.partition(":")
                    target_ns = target_ns if sep else namespace
                    if nested:
                        if target_ns in namespaces and identifier not in event_sets.get(target_ns, set()):
                            errors.append(f"{label}: missing nested sound event {name} in {source}")
                    elif target_ns in namespaces and not find_asset(packs, target_ns, "sounds", identifier, ".ogg"):
                        errors.append(f"{label}: missing sound clip {name} in {source}")
                for key, value in node.items():
                    if key != "name":
                        check_sound(value)
            elif isinstance(node, list):
                for item in node:
                    check_sound(item)
            elif isinstance(node, str):
                target_ns, sep, identifier = node.partition(":")
                target_ns = target_ns if sep else namespace
                if target_ns in namespaces and not find_asset(packs, target_ns, "sounds", identifier, ".ogg"):
                    errors.append(f"{label}: missing sound clip {node} in {source}")
        check_sound(events)

    # Only Core owns these required Minecraft overrides. The map pack adds only its documented inventory board.
    if CORE in pack_names:
        core = ROOT / CORE / "assets" / "minecraft"
        for rel in MINECRAFT_OVERRIDES:
            if not (core / rel).is_file():
                errors.append(f"Missing required Core Minecraft override assets/minecraft/{rel}")
    if label == "Core only":
        for path in (ROOT / CORE / "assets").rglob("*"):
            if path.is_file() and path.suffix.lower() in {".json", ".mcmeta", ".properties", ".txt"}:
                text = path.read_text(encoding="utf-8-sig", errors="ignore")
                if any(ns in text for ns in MAP_NAMESPACES + OLD_NAMESPACES):
                    errors.append(f"Core has a map dependency in {path.relative_to(ROOT)}")
    return sum(1 for pack in packs for path in (pack / "assets").rglob("*.json"))


def validate(datapacks: dict[str, Path | None]) -> int:
    errors: list[str] = []
    for name in PACK_NAMES:
        validate_pack_metadata(ROOT / name, errors)
    counts = {}
    for label, combo in COMBINATIONS.items():
        counts[label] = validate_combination(label, combo, errors)
    core_datapack = datapacks.get("core")
    if core_datapack:
        if not core_datapack.is_dir():
            errors.append(f"Core datapack path does not exist: {core_datapack}")
        else:
            from_core = set()
            text_files = [p for p in core_datapack.rglob("*") if p.is_file() and p.suffix.lower() in {".mcfunction", ".json", ".mcmeta", ".txt"}]
            for path in text_files:
                text = path.read_text(encoding="utf-8-sig", errors="ignore")
                if any(ns in text for ns in MAP_NAMESPACES + OLD_NAMESPACES):
                    errors.append(f"Core datapack has a map dependency: {path}")
                from_core.update(re.findall(r'item_model\s*[:=]\s*[\'\"]zombies:([a-z0-9_./-]+)', text))
                from_core.update(re.findall(r'"minecraft:item_model"\s*:\s*"zombies:([a-z0-9_./-]+)"', text))
            for identifier in sorted(from_core):
                if not (ROOT / CORE / "assets/zombies/items" / f"{identifier}.json").is_file():
                    errors.append(f"Core datapack item_model is missing: zombies:{identifier}")
    print("Checked supported combinations: " + ", ".join(f"{name} ({count} asset JSON files)" for name, count in counts.items()))
    if errors:
        print("Validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Pack metadata, resource references, and supported pack combinations resolve.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datapack", "--core-datapack", dest="core_datapack", type=Path, help="Optional Core datapack path for Core-only ID and dependency checks.")
    args = parser.parse_args()
    return validate({"core": args.core_datapack.resolve() if args.core_datapack else None})


if __name__ == "__main__":
    raise SystemExit(main())
