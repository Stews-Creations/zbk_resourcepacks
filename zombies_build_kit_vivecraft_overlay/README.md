# Zombies Build Kit Vivecraft Overlay

This optional resource pack supplies Vivecraft-specific held-item transforms for shared Zombies Build Kit weapon models. It depends on the base resource pack and matching datapack.

The overlay overrides the base pack item models in the `zbk:` asset namespace.

## Installation

Download this optional overlay from the [resource pack release](https://github.com/Stews-Creations/zbk_resourcepacks/releases/latest) and enable it above `Zombies Build Kit Base`. Map authors can include map-specific Vivecraft assets in their world bundles. Refresh resources with F3+T after changing files.

This overlay contains shared weapon overrides only. The map-specific bow transforms are owned by the DE Vivecraft overlay. `VERSION` and the `zbk.version` metadata field identify this pack as version 1.0.0; Minecraft's 26.2 resource format remains at 88.0.

## Supported guns

Gun models cover the BO3 arsenal, Ray Gun, and Death Machine. Retired generic gun item definitions, models, and textures are not included. Shared audio required by supported weapons remains in the base pack.

Held-gun overrides mirror the base pack's `assets/zbk/models/item/guns/<type>/` folders. Ray Gun lives in `wonder_weapons/`; Death Machine lives in `special/` and inherits base pack's shared geometry. Item definitions mirror the base pack's categorized IDs under `assets/zbk/items/guns/`. See the [base pack model layout](../zombies_build_kit/README.md#model-organization) when adding or overriding a model.
