# ZBK Der Eisendrache resource pack

This optional map resource pack supplies Der Eisendrache models, textures, sound events, audio, fonts, and the map inventory screen override under the `zbk_der_eisendrache` namespace. It requires the matching ZBK base pack and Der Eisendrache datapacks and resource pack.

## Installation

Enable `ZBK Der Eisendrache` above `Zombies Build Kit Base`. For Vivecraft, enable `ZBK Der Eisendrache Vivecraft Overlay` above this pack and the base pack Vivecraft overlay. Keep unrelated map packs disabled for the world. Refresh client resources with F3+T after replacing packs.

The inventory screen texture intentionally replaces Minecraft's native inventory background while this map pack is enabled. The original resource pack already used this screen artwork as a global override. Reusable Panzer presentation textures and sounds are supplied by the base pack under their shared `zombies:` identifiers; this map pack owns the DE-specific encounter behavior.

## Contents and license

Models, item definitions, and textures are grouped by purpose within `assets/zbk_der_eisendrache/`:

| Category | Paths |
| --- | --- |
| Pack-a-Punch | Models and textures in `item/map_elements/pack_a_punch/`; item definitions in `map_elements/pack_a_punch/` |
| Fuse and powerups | Models and textures in `item/powerups/`; fuse item definitions in `powerups/` |
| Tram and rocket | Models and item definitions in `props/tram/` and `props/rocket/` |
| Equipment | Grenade textures in `item/special_equipment/grenade/` |
| Quest board | Models in `quest/hud/<quest>/` and textures in `item/quest/hud/<quest>/`; item definitions stay in `quest/hud/` |
| HUD | Ammo modifier textures in `font/hud/ammo_mods/`; damage overlay in `font/hud/`; item GUI textures in `item/gui/` |

Bow models, arrows, ritual boxes, and quest mechanisms retain their existing `quest/bows/` subfolders. The Vivecraft overlay uses those same bow item IDs. The intro video font is `font/intro_cutscene/video.json`, referenced as `zbk_der_eisendrache:intro_cutscene/video`; its frames live in `textures/font/intro_cutscene/video/`. The vanilla inventory override retains its required Minecraft path.

Each bow model directory keeps `idle.json` beside a `draw/` folder containing its numbered draw poses, including the `right_hand/` and Vivecraft variants. Quest HUD model and texture groups are `electric/`, `fire/`, `void/`, `wolf/`, `ragnarok/`, and `shared/`.

Audio files are grouped by action: `sounds/dragon/` contains `feeding/`, `fire/`, `idle/`, and `lifecycle/`; `sounds/tram/` contains `motor/`, `controls/`, and `announcements/`. Electric bow audio lives under `sounds/quest/bows/electric/`, grouped into `runes/`, `weather_vane/`, `fires/`, `ritual/`, `upgrades/`, and `storm/`. The sound catalog maps the existing event IDs to these files, so gameplay sound calls remain the same. Item definition IDs also remain unchanged by these model, texture, and audio groupings.

Install the matching datapack when updating these resource paths. Existing items with the previous fuse, Pack-a-Punch, tram, or rocket item IDs need to be recreated; rebuild placed displays through their owning systems and refresh resources with F3+T.

## License

The pack restores the original Der Eisendrache namespace assets and the map-specific assets previously stored under the shared `zombies` namespace. ZBK custom assets use the project license and media permission included here. Third-party notices are preserved in `LICENSES/`.
