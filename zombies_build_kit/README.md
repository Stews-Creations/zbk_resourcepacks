# Zombies Build Kit Base resource pack

This resource pack supplies shared Zombies Build Kit item models, textures, HUD fonts, gameplay audio, generated shared models, and reusable Panzer presentation assets. It requires the matching ZBK base pack datapack.

The base pack assets live under `assets/zbk/`. Use `zbk:` for the base pack item models, fonts, textures, and sounds. The matching datapack keeps its `zombies:` gameplay function and dialog IDs.

The base pack also overrides Minecraft HUD sprites to hide the vanilla hearts, hunger icons, and experience bar behind the ZBK HUD. These transparent sprites cover normal and special heart variants and belong in the base pack so every map gets the same HUD behavior.

Magenta stained glass panes use the empty `zbk:block/invisible` model as invisible collision blocks for Build Kit mechanics. The override lives in the base pack so map datapacks can use the same block consistently.

The base pack also supplies the zombie and zombified piglin textures used by shared enemies, plus the supplied Richtofen mannequin skin at `assets/minecraft/textures/entity/player/richtofen.png`. The base pack mannequin profiles reference the zombie and Richtofen textures by their vanilla resource paths, so keep these files in the base pack for every map.

The base pack sound events include round and game cues, dog and teleporter effects, menu music, and four-character gameplay callouts. These play with the base pack alone. The reusable radio includes all ten tracks through `zbk:radio`, with audio files under `assets/zbk/sounds/radio/`; it requires no map add-on. Individual tracks also have `zbk:radio.<track>` events. Map resource packs may supply their own location music and Easter egg audio.

## Death Machine model

The Death Machine uses the updated six-barrel geometry through `models/item/guns/special/death_machine_geometry.json`. Both the base model and Vivecraft overlay inherit this geometry while retaining their own held-item transforms. The item atlas registers its texture directory. This weapon belongs to the base pack and requires no map resource pack.

## Perk machine models

The seven cabinet models use item IDs `zbk:map_elements/perks/<perk>` and geometry under `models/item/map_elements/perks/`. These are separate from the `zbk:perks/<perk>` bottle items. The matching datapack supplies placement, barrier collision, purchases, and deletion, while old block machines remain supported.

The runtime JSON and textures are exported from Blockbench projects. Authoring projects and export scripts are not distributed.

The authoring projects trace each cabinet in image coordinates, with the left of the artwork at low X. Minecraft draws a north face with the left of its texture at high X, so the exporter mirrors every cabinet across X=8. Raised panels, signs, and lettering then sit over the matching cabinet artwork. Fixed display transforms are measured on the mirrored source before simplification, so placement stays centered on the footprint.

The exporter simplifies all seven cabinets:

- Adjacent contour slices merge into slabs that enclose their source slices. A slab's outline varies by at most 0.25 model units, or 0.4 units on parts without artwork. Curves are deliberately stepped to reduce rendering cost.
- Slab UVs follow the source projection. Slices merge only while the artwork stays within about 2.5 texels of its traced position; otherwise they remain separate.
- A traced outline can end in a bottom slice that covers only part of the width. The exporter widens that slice to the one resting on it, so cabinets and bases have level, complete bottoms. Rounded corners are unchanged.
- Quick Revive's sloped lid gets smooth covers at the lid's own angle, with the lid badge lying flat on them. The stepped lid stays underneath as the solid body. This uses the free element rotation angles of Minecraft 26.2.
- The Wunderfizz orb becomes cuboids that share its center and reach its surface with every corner, so it steps evenly toward all sides. Its front and back keep the projected artwork, and the side of each step repeats the artwork along its own edge. Faces of different orb cuboids can share a plane, where they show the same texels.
- Every cuboid grows by 0.01 units with matching UVs, so neighboring cuboids overlap instead of leaving pixel-wide cracks along shared edges.
- Faces fully covered by opaque, unrotated closed cuboids are removed, and elements with no remaining faces are dropped. Partially exposed faces, rotated details, separated hardware, and per-element shading remain.
- Mule Kick's side fins extend inward into the cabinet shell, including its tapered lower section, so both plates remain attached.

| Cabinet | Cuboids | Faces |
| --- | --- | --- |
| Juggernog | 48 | 241 |
| Stamin-Up | 141 | 648 |
| Speed Cola | 92 | 444 |
| Double Tap | 98 | 464 |
| Quick Revive | 116 | 589 |
| Mule Kick | 133 | 641 |
| Der Wunderfizz | 271 | 1341 |

Perk textures live in `textures/item/map_elements/perks/` and are registered in the item atlas. Each cabinet has one artwork texture, `<perk>_1.png`, cropped to the texels its model uses. Juggernog also keeps its small palette, `juggernog_0.png`. All seven cabinets share one material atlas, `perk_materials.png`. Every texture has power-of-two sides of at most 1024 pixels, which keeps mipmapping available for the whole item atlas. Texels outside the traced artwork take the color of the nearest traced texel, so slab edges and mipmaps do not pick up the blank background.

Wunderfizz's frame and base use dark aged metal with muted brushed-steel trim from the shared material atlas. Its orb artwork, blue badge, and brass platform retain their original materials. Its curved surfaces keep the source model's disabled directional face shading.

Reload resources with F3+T after updating the pack.

## Install

1. For your own world, install the matching base datapack and download the base resource pack ZIP from the [repository releases](https://github.com/Stews-Creations/zbk_resourcepacks/releases/latest). Enable the resource pack in Minecraft.
2. For Vivecraft, download the optional base pack Vivecraft overlay from the same release and enable it above the base pack.

Released ZBK map worlds include their required base pack and map resource assets, so players need only the world download. Map pack folders in this repository are references for world authors.

Refresh resources with F3+T after changing files.

## Pack metadata and licensing

`VERSION` and the `zbk.version` metadata field identify this resource pack as version 1.0.0. Minecraft's 26.2 resource format metadata remains at format 88.0. ZBK custom assets use the project license and media permission. The release ZIP keeps these documents and third-party notices in `LICENSES/`.

## Supported guns

Gun models cover the BO3 arsenal, Ray Gun, and Death Machine. Retired generic gun item definitions, models, and textures are not included. Shared audio required by supported weapons remains in the base pack.

## Model organization

Model paths below are relative to `assets/zbk/models/`.

| Folder | Contents |
| --- | --- |
| `item/guns/` | `pistols`, `submachine_guns`, `assault_rifles`, `shotguns`, `light_machine_guns`, `sniper_rifles`, and `launchers`; Ray Gun in `wonder_weapons`, Death Machine and its shared geometry in `special` |
| `wall/guns/` | Wall-buy gun models grouped by the same weapon types |
| `item/special_equipment/` | Grenade, Monkey Bomb variants, Trip Mine variants, and Rocket Shield parts, charges, and HUD models |
| `item/powerups/` | Powerup drops and their HUD models |
| `item/perks/` | Perk item models |
| `item/melee/` | Knife, Bowie Knife, and puncher |
| `item/map_elements/` | Workbench, wall-gun marker, and Pack-a-Punch parts |
| `props/` | Floating vehicles and explosive barrel |
| `block/` | Invisible collision-block model |

Item definitions under `assets/zbk/items/` follow the same categories, without the model-only `item/` prefix. For example, `zbk:guns/pistols/mr6` selects `zbk:item/guns/pistols/mr6`, and `zbk:wall/guns/pistols/mr6` selects its wall model. Rocket Shield charge variants use `special_equipment/rocket_shield/shield_1` through `shield_3`. The shared `empty` definition stays at the root. Generated enemy assets retain their exporter-owned paths under `assets/animated_java/`.

Install the matching datapack with these item IDs. Previously saved items using old IDs must be recreated; reload resources with F3+T and rebuild placed displays through their owning system.

Custom model overrides must use these categorized paths. The base pack Vivecraft overlay mirrors the held-gun paths so its transforms apply to the same models.

## Texture organization

Textures under `assets/zbk/textures/item/` match the model categories: `guns/<type>/`, `special_equipment/`, `powerups/`, `perks/`, `melee/`, and `map_elements/`. Held and wall-buy guns share the same gun textures. Perk bottles live alongside their perk textures; equipment layers, Rocket Shield charges, and Pack-a-Punch materials stay together in their respective subfolders.

Death Machine textures, including the exported `death_machine_0.png`, live in `item/guns/special/`. Its exporter and item-atlas entry use that directory. Fonts and HUD imagery remain under `textures/font/`, shared enemy materials under `textures/entity/`, and vanilla overrides at their required Minecraft paths. Sound paths are unchanged. Custom texture overrides must mirror the categorized texture paths.
