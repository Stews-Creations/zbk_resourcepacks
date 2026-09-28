# Zombies Build Kit Resource Packs

This repository contains the installable Core resource pack, optional map resource packs, and optional Vivecraft overlays. Core supplies shared ZBK item models, textures, HUD fonts, gameplay audio, and generated shared models. Map packs supply only their map assets and require the matching Core datapack and resource pack.

## Install and package

1. Copy each selected pack folder into `.minecraft/resourcepacks`, or ZIP each folder's contents so `pack.mcmeta` is at the ZIP root.
2. For a map, place its pack above Core. Enable Vivecraft overlays above the corresponding base packs.

## Supported combinations

| World | Resource pack stack, highest priority first |
| --- | --- |
| Core only | Core Vivecraft overlay (optional), Core |
| Nacht der Untoten | Core Vivecraft overlay (optional), Nacht, Core |
| Der Eisendrache | DE Vivecraft overlay (optional), Core Vivecraft overlay (optional), DE, Core |

Install only the matching map pack for a world. The DE pack intentionally overrides Minecraft's native inventory background with the original quest inventory board. The Core pack also owns its documented required Minecraft overrides.

## Pack contents

| Folder | Use |
| --- | --- |
| [`zombies_build_kit`](zombies_build_kit/README.md) | Shared runtime assets used by Core |
| [`zombies_build_kit_vivecraft_overlay`](zombies_build_kit_vivecraft_overlay/README.md) | Optional Vivecraft held-weapon transforms for Core |
| [`zbk_nacht_der_untoten`](zbk_nacht_der_untoten/README.md) | Nacht der Untoten audio and map assets |
| [`zbk_der_eisendrache`](zbk_der_eisendrache/README.md) | Der Eisendrache audio, models, textures, fonts, and inventory screen |
| [`zbk_der_eisendrache_vivecraft_overlay`](zbk_der_eisendrache_vivecraft_overlay/README.md) | Optional Vivecraft bow transforms for Der Eisendrache |

All installable packs use ZBK pack version 1.0.0 and retain Minecraft Java 26.2 resource format 88.0. Keep the license and attribution files with each pack when distributing it. ZBK assets use the repository's noncommercial asset license and media permission. Third-party notices are preserved in each installable pack. See [licensing and attribution](LICENSE.md).
