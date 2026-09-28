# ZBK Resource Packs

Implementation is not available yet.

## Responsibility

This repository will own reusable visual and audio assets for Zombies Build Kit. It is planned to provide a base resource pack and an optional VR overlay so users can select the VR presentation independently.

## Dependencies

The base pack must match the core datapack's asset identifiers. The optional VR overlay is layered above the base pack and reuses its shared assets. Exact client compatibility and packaging dependencies remain to be verified during migration.

## Source and outputs

Required runtime textures, sounds, fonts, models, and item definitions belong in source control, along with portable maintained generators. Blockbench authoring projects and workspaces are excluded. Record external provenance and regeneration limitations where source is intentionally absent. Packaged release archives, temporary exports, and local tooling state are excluded. Map-specific audio, artwork, and models are outside the core scope even when they occupy shared namespaces.

## License and credit

Free noncommercial use, modification, and sharing are allowed with credit to
[MiniStew](https://www.youtube.com/@MiniStew). Monetized videos and streams are
allowed under the [media permission](MEDIA_PERMISSION.md). Selling covered ZBK
content or maps containing it, or charging for server access, is not covered
by that permission. See [licensing and attribution](LICENSE.md) for the code
and asset licenses, their scope, and redistribution requirements.
