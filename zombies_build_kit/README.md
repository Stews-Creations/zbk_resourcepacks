# Zombies Build Kit Core Resource Pack

This resource pack supplies shared Zombies Build Kit item models, textures, HUD fonts, gameplay audio, generated shared models, and reusable Panzer presentation assets. It requires the matching ZBK Core datapack.

Core assets live under `assets/zbk/`. Use `zbk:` for Core item models, fonts, textures, and sounds. The matching datapack keeps its `zombies:` gameplay function and dialog IDs.

Core also overrides Minecraft HUD sprites to hide the vanilla hearts, hunger icons, and experience bar behind the ZBK HUD. These transparent sprites cover normal and special heart variants and belong in the base pack so every map gets the same HUD behavior.

Core sound events include round and game cues, dog and teleporter effects, menu music, and four-character gameplay callouts. These play with Core alone. Map resource packs may supply their own location music, radio tracks, and Easter egg audio.

## Perk machine models

The seven cabinet models use item IDs `zbk:map_elements/perks/<perk>` and geometry under `models/item/map_elements/perks/`. These are separate from the `zbk:perks/<perk>` bottle items. The matching datapack supplies placement, barrier collision, purchases, and deletion, while old block machines remain supported.

`tools/export_core_machines.py` in the resource-pack repository exports the runtime JSON and textures from supplied Blockbench projects. Authoring projects are not distributed. Exporting requires Python with NumPy and Pillow; run `python tools/test_optimize_core_machines.py` and `python tools/validate_core_machines.py` from the resource-pack repository after export.

The authoring projects trace each cabinet in image coordinates, with the left of the artwork at low X. Minecraft draws a north face with the left of its texture at high X, so the exporter mirrors every cabinet across X=8. Raised panels, signs, and lettering then sit over the matching cabinet artwork. Fixed display transforms are measured on the mirrored source before simplification, so placement stays centered on the footprint.

The exporter applies `tools/optimize_core_machines.py` to all seven cabinets:

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

1. For your own world, install the matching Core datapack and download the Core resource pack ZIP from the [repository releases](https://github.com/Stews-Creations/zbk_resourcepacks/releases/latest). Enable the resource pack in Minecraft.
2. For Vivecraft, download the optional Core Vivecraft overlay from the same release and enable it above Core.

Released ZBK map worlds include their required Core and map resource assets, so players need only the world download. Map pack folders in this repository are references for world authors.

Refresh resources with F3+T after changing files.

## Pack metadata and licensing

`VERSION` and the `zbk.version` metadata field identify this resource pack as version 1.0.0. Minecraft's 26.2 resource format metadata remains at format 88.0. ZBK custom assets use the project license and media permission. The release ZIP keeps these documents and third-party notices in `LICENSES/`.
