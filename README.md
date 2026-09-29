# Zombies Build Kit resource packs

This repository contains the installable base resource pack, its optional Vivecraft overlay, and source references for map-specific assets. The base pack supplies shared ZBK item models, textures, HUD fonts, gameplay audio, and generated shared models. Released map worlds bundle the required base and map resource assets.

## Install

### Play a released ZBK map

Download the map's world file and follow its installation instructions. The world file includes its required resource pack content, so players do not need to download any resource packs separately. The optional Vivecraft overlay is a separate download for players who want its held-weapon transforms.

### Build your own world

1. Download `zombies_build_kit-v<version>.zip` from the [latest resource pack release](https://github.com/Stews-Creations/zbk_resourcepacks/releases/latest), plus the matching [base datapack](https://github.com/Stews-Creations/zbk_datapacks). Put the resource pack ZIP in `.minecraft/resourcepacks` and the datapack in the world's `datapacks` folder.
2. If you use Vivecraft, also download `zombies_build_kit_vivecraft_overlay-v<version>.zip` from the same release and enable it above the base pack.
3. If you are making a map, include its required map assets with the world you distribute. The map pack folders in this repository are source references, not separate GitHub release downloads.

Both release ZIPs place `pack.mcmeta` and `LICENSES/` at the ZIP root. The `LICENSES/` folder contains the license, notice, and media permission documents. Enable the base resource pack in Minecraft; enable the optional overlay above it. Keep the datapack, resource pack, and overlay on matching versions.

## Supported combinations

| World | Resource pack stack, highest priority first |
| --- | --- |
| Custom map world | Base pack Vivecraft overlay (optional), the base pack |
| Nacht der Untoten world bundle | Base pack Vivecraft overlay (optional), Nacht, the base pack |
| Der Eisendrache world bundle | DE Vivecraft overlay (optional), the base pack Vivecraft overlay (optional), DE, the base pack |

The map rows show resource priority inside a bundled world, not extra downloads for players. The DE pack intentionally overrides Minecraft's native inventory background with the original quest inventory board. The base pack's Minecraft HUD overrides hide vanilla hearts, hunger icons, and the experience bar so they do not overlap the ZBK HUD.

## Override the base pack sounds

A map resource pack can replace any base pack audio file listed below. Put the replacement `.ogg` at the same path under `assets/zbk/sounds/` in the map pack, then place that pack above the base pack. For example, to replace `round/start.ogg`, use `assets/zbk/sounds/round/start.ogg`. Keep the file name and directory path exact. The base pack sound event continues to work without editing `sounds.json`.

The 544 paths below are relative to `assets/zbk/sounds/` in the base pack. Expand a category to see every file in it.

<details><summary>buildables (1 file)</summary>

```text
buildables/zmb_building.ogg
```

</details>

<details><summary>drops (6 files)</summary>

```text
drops/carpenter.ogg
drops/double_points.ogg
drops/fire_sale.ogg
drops/insta_kill.ogg
drops/max_ammo.ogg
drops/nuke.ogg
```

</details>

<details><summary>environment (1 file)</summary>

```text
environment/explosions/explode_barrel.ogg
```

</details>

<details><summary>game (5 files)</summary>

```text
game/cash.ogg
game/disco.ogg
game/game_over.ogg
game/over_announcer.ogg
game/start.ogg
```

</details>

<details><summary>grenade (2 files)</summary>

```text
grenade/explode.ogg
grenade/throw.ogg
```

</details>

<details><summary>guns (86 files)</summary>

```text
guns/bo3/205_brecci_1.ogg
guns/bo3/205_brecci_silenced.ogg
guns/bo3/48_dredge_1.ogg
guns/bo3/48_dredge_silenced.ogg
guns/bo3/argus_1.ogg
guns/bo3/argus_action.ogg
guns/bo3/argus_fast.ogg
guns/bo3/argus_shot.ogg
guns/bo3/argus_silenced.ogg
guns/bo3/argus_silenced_fast.ogg
guns/bo3/argus_silenced_shot.ogg
guns/bo3/brm_1.ogg
guns/bo3/brm_silenced.ogg
guns/bo3/dingo_1.ogg
guns/bo3/dingo_silenced.ogg
guns/bo3/drakon_1.ogg
guns/bo3/drakon_silenced.ogg
guns/bo3/gorgon_1.ogg
guns/bo3/gorgon_silenced.ogg
guns/bo3/haymaker12_1.ogg
guns/bo3/haymaker12_silenced.ogg
guns/bo3/hvk30_1.ogg
guns/bo3/hvk30_silenced.ogg
guns/bo3/icr1_1.ogg
guns/bo3/icr1_silenced.ogg
guns/bo3/kn44_silenced.ogg
guns/bo3/krm262_1.ogg
guns/bo3/krm262_action.ogg
guns/bo3/krm262_fast.ogg
guns/bo3/krm262_shot.ogg
guns/bo3/krm262_silenced.ogg
guns/bo3/krm262_silenced_fast.ogg
guns/bo3/krm262_silenced_shot.ogg
guns/bo3/kuda_1.ogg
guns/bo3/kuda_silenced.ogg
guns/bo3/lcar9_1.ogg
guns/bo3/lcar9_silenced.ogg
guns/bo3/locus_1.ogg
guns/bo3/locus_bolt.ogg
guns/bo3/locus_fast.ogg
guns/bo3/locus_shot.ogg
guns/bo3/locus_silenced.ogg
guns/bo3/locus_silenced_fast.ogg
guns/bo3/locus_silenced_shot.ogg
guns/bo3/m8a7_1.ogg
guns/bo3/m8a7_silenced.ogg
guns/bo3/man_o_war_1.ogg
guns/bo3/man_o_war_silenced.ogg
guns/bo3/mr6_1.ogg
guns/bo3/mr6_silenced.ogg
guns/bo3/p06_1.ogg
guns/bo3/p06_silenced.ogg
guns/bo3/pharo_1.ogg
guns/bo3/pharo_silenced.ogg
guns/bo3/razorback_1.ogg
guns/bo3/razorback_silenced.ogg
guns/bo3/rk5_1.ogg
guns/bo3/rk5_silenced.ogg
guns/bo3/rpk_1.ogg
guns/bo3/rpk_2.ogg
guns/bo3/rpk_3.ogg
guns/bo3/sheiva_1.ogg
guns/bo3/sheiva_silenced.ogg
guns/bo3/svg100_1.ogg
guns/bo3/svg100_bolt.ogg
guns/bo3/svg100_fast.ogg
guns/bo3/svg100_shot.ogg
guns/bo3/svg100_silenced.ogg
guns/bo3/svg100_silenced_fast.ogg
guns/bo3/svg100_silenced_shot.ogg
guns/bo3/vesper_1.ogg
guns/bo3/vesper_silenced.ogg
guns/bo3/vmp_1.ogg
guns/bo3/vmp_silenced.ogg
guns/bo3/weevil_1.ogg
guns/bo3/weevil_silenced.ogg
guns/bo3/xm53_1.ogg
guns/bo3/xr2_1.ogg
guns/bo3/xr2_silenced.ogg
guns/death_machine.ogg
guns/enemy_hit.ogg
guns/grenade.ogg
guns/kn44_1.ogg
guns/light_machine_gun.ogg
guns/raygun.ogg
guns/sheiva.ogg
```

</details>

<details><summary>jump_pads (10 files)</summary>

```text
jump_pads/flinger_activate.ogg
jump_pads/flinger_fly.ogg
jump_pads/flinger_land.ogg
jump_pads/landing_pad_activated.ogg
jump_pads/landing_pad_activated_sound.ogg
jump_pads/landing_pad_activation_required.ogg
jump_pads/launch_activate.ogg
jump_pads/launch_fly.ogg
jump_pads/launch_land.ogg
jump_pads/launch_pad_on.ogg
```

</details>

<details><summary>mob (15 files)</summary>

```text
mob/dog/dog_dead.ogg
mob/dog/dog_spawn.ogg
mob/panzer/death.ogg
mob/panzer/electric_throw.ogg
mob/panzer/flamethrower_burst.ogg
mob/panzer/flamethrower_loop.ogg
mob/panzer/footstep_1.ogg
mob/panzer/footstep_2.ogg
mob/panzer/footstep_3.ogg
mob/panzer/footstep_4.ogg
mob/panzer/landing.ogg
mob/panzer/landing_flame.ogg
mob/panzer/melee.ogg
mob/panzer/panzer_spawn.ogg
mob/panzer/spawn.ogg
```

</details>

<details><summary>music (1 file)</summary>

```text
music/main_menu.ogg
```

</details>

<details><summary>mystery_box (9 files)</summary>

```text
mystery_box/bye_bye.ogg
mystery_box/close.ogg
mystery_box/land.ogg
mystery_box/laugh.ogg
mystery_box/music.ogg
mystery_box/open.ogg
mystery_box/poof.ogg
mystery_box/rotate.ogg
mystery_box/woosh.ogg
```

</details>

<details><summary>pack_a_punch (1 file)</summary>

```text
pack_a_punch/pack_a_punch.ogg
```

</details>

<details><summary>perks (7 files)</summary>

```text
perks/double_tap.ogg
perks/juggernog.ogg
perks/mule_kick.ogg
perks/perk_buy.ogg
perks/quick_revive.ogg
perks/speed_cola.ogg
perks/stamina_up.ogg
```

</details>

<details><summary>radio (10 files)</summary>

```text
radio/all_mixed_up.ogg
radio/areia.ogg
radio/dog_fire.ogg
radio/dusk.ogg
radio/first_fight.ogg
radio/konigratzer_marsch.ogg
radio/russian_theme.ogg
radio/stag_push.ogg
radio/true_crime_track_4.ogg
radio/wtf.ogg
```

</details>

<details><summary>reload (114 files)</summary>

```text
reload/205_brecci_empty.ogg
reload/205_brecci_empty_fast.ogg
reload/205_brecci_partial.ogg
reload/205_brecci_partial_fast.ogg
reload/48_dredge_empty.ogg
reload/48_dredge_empty_fast.ogg
reload/48_dredge_partial.ogg
reload/48_dredge_partial_fast.ogg
reload/argus_empty.ogg
reload/argus_empty_fast.ogg
reload/argus_partial.ogg
reload/argus_partial_fast.ogg
reload/brm_empty.ogg
reload/brm_empty_fast.ogg
reload/brm_partial.ogg
reload/brm_partial_fast.ogg
reload/dingo_empty.ogg
reload/dingo_empty_fast.ogg
reload/dingo_partial.ogg
reload/dingo_partial_fast.ogg
reload/drakon_empty.ogg
reload/drakon_empty_fast.ogg
reload/drakon_partial.ogg
reload/drakon_partial_fast.ogg
reload/gorgon_empty.ogg
reload/gorgon_empty_fast.ogg
reload/gorgon_partial.ogg
reload/gorgon_partial_fast.ogg
reload/haymaker12_empty.ogg
reload/haymaker12_empty_fast.ogg
reload/haymaker12_partial.ogg
reload/haymaker12_partial_fast.ogg
reload/hvk30_empty.ogg
reload/hvk30_empty_fast.ogg
reload/hvk30_partial.ogg
reload/hvk30_partial_fast.ogg
reload/icr1_empty.ogg
reload/icr1_empty_fast.ogg
reload/icr1_partial.ogg
reload/icr1_partial_fast.ogg
reload/kn44_empty.ogg
reload/kn44_empty_fast.ogg
reload/kn44_partial.ogg
reload/kn44_partial_fast.ogg
reload/krm262_empty.ogg
reload/krm262_empty_fast.ogg
reload/krm262_partial.ogg
reload/krm262_partial_fast.ogg
reload/krm262_shell.ogg
reload/krm262_shell_fast.ogg
reload/kuda_empty.ogg
reload/kuda_empty_fast.ogg
reload/kuda_partial.ogg
reload/kuda_partial_fast.ogg
reload/lcar9_empty.ogg
reload/lcar9_empty_fast.ogg
reload/lcar9_partial.ogg
reload/lcar9_partial_fast.ogg
reload/locus_empty.ogg
reload/locus_empty_fast.ogg
reload/locus_partial.ogg
reload/locus_partial_fast.ogg
reload/m8a7_empty.ogg
reload/m8a7_empty_fast.ogg
reload/m8a7_partial.ogg
reload/m8a7_partial_fast.ogg
reload/man_o_war_empty.ogg
reload/man_o_war_empty_fast.ogg
reload/man_o_war_partial.ogg
reload/man_o_war_partial_fast.ogg
reload/mr6_empty.ogg
reload/mr6_empty_fast.ogg
reload/mr6_partial.ogg
reload/mr6_partial_fast.ogg
reload/pharo_empty.ogg
reload/pharo_empty_fast.ogg
reload/pharo_partial.ogg
reload/pharo_partial_fast.ogg
reload/ray_gun_empty.ogg
reload/ray_gun_empty_fast.ogg
reload/ray_gun_partial.ogg
reload/ray_gun_partial_fast.ogg
reload/rk5_empty.ogg
reload/rk5_empty_fast.ogg
reload/rk5_partial.ogg
reload/rk5_partial_fast.ogg
reload/rpk_empty.ogg
reload/rpk_empty_fast.ogg
reload/rpk_partial.ogg
reload/rpk_partial_fast.ogg
reload/sheiva_empty.ogg
reload/sheiva_empty_fast.ogg
reload/sheiva_partial.ogg
reload/sheiva_partial_fast.ogg
reload/svg100_empty.ogg
reload/svg100_empty_fast.ogg
reload/svg100_partial.ogg
reload/svg100_partial_fast.ogg
reload/vesper_empty.ogg
reload/vesper_empty_fast.ogg
reload/vesper_partial.ogg
reload/vesper_partial_fast.ogg
reload/vmp_empty.ogg
reload/vmp_empty_fast.ogg
reload/vmp_partial.ogg
reload/vmp_partial_fast.ogg
reload/weevil_empty.ogg
reload/weevil_empty_fast.ogg
reload/weevil_partial.ogg
reload/weevil_partial_fast.ogg
reload/xm53_empty.ogg
reload/xm53_empty_fast.ogg
reload/xm53_partial.ogg
reload/xm53_partial_fast.ogg
```

</details>

<details><summary>rocket_shield (2 files)</summary>

```text
rocket_shield/break.ogg
rocket_shield/impact.ogg
```

</details>

<details><summary>round (2 files)</summary>

```text
round/end.ogg
round/start.ogg
```

</details>

<details><summary>round_change (7 files)</summary>

```text
round_change/fetch_me_their_souls.ogg
round_change/mus_doground_end.ogg
round_change/mus_zombie_dog_start.ogg
round_change/round_change_1.ogg
round_change/round_change_2.ogg
round_change/round_change_3.ogg
round_change/round_change_4.ogg
```

</details>

<details><summary>special_equipment (1 file)</summary>

```text
special_equipment/monkey_bomb.ogg
```

</details>

<details><summary>teleporter (4 files)</summary>

```text
teleporter/teleporter_available.ogg
teleporter/teleporter_buy.ogg
teleporter/teleporter_recharging.ogg
teleporter/teleporter_success.ogg
```

</details>

<details><summary>traps (5 files)</summary>

```text
traps/amb_sparks_r.ogg
traps/available.ogg
traps/big.ogg
traps/flip.ogg
traps/start.ogg
```

</details>

<details><summary>voice_lines (251 files)</summary>

```text
voice_lines/dempsy/box_gun/vox_cast_plr_0_box_ar_1.ogg
voice_lines/dempsy/box_gun/vox_cast_plr_0_box_ar_3.ogg
voice_lines/dempsy/box_gun/vox_cast_plr_0_box_mg_1.ogg
voice_lines/dempsy/box_gun/vox_cast_plr_0_box_raygun_4.ogg
voice_lines/dempsy/box_gun/vox_cast_plr_0_box_shotgun_0.ogg
voice_lines/dempsy/carpenter/vox_cast_plr_0_powerup_carpenter_0.ogg
voice_lines/dempsy/carpenter/vox_cast_plr_0_powerup_carpenter_3.ogg
voice_lines/dempsy/carpenter/vox_cast_plr_0_powerup_carpenter_4.ogg
voice_lines/dempsy/crawler_kill/vox_cast_plr_0_crawler_kill_0.ogg
voice_lines/dempsy/crawler_kill/vox_cast_plr_0_crawler_kill_2.ogg
voice_lines/dempsy/crawler_kill/vox_cast_plr_0_crawler_kill_4.ogg
voice_lines/dempsy/dog/vox_cast_plr_0_spawn_hellhound_0.ogg
voice_lines/dempsy/dog/vox_cast_plr_0_spawn_hellhound_1.ogg
voice_lines/dempsy/dog/vox_cast_plr_0_spawn_hellhound_4.ogg
voice_lines/dempsy/double_points/vox_cast_plr_0_powerup_double_1.ogg
voice_lines/dempsy/double_points/vox_cast_plr_0_powerup_double_2.ogg
voice_lines/dempsy/double_points/vox_cast_plr_0_powerup_double_4.ogg
voice_lines/dempsy/downed/vox_cast_plr_0_revive_down_0.ogg
voice_lines/dempsy/downed/vox_cast_plr_0_revive_down_3.ogg
voice_lines/dempsy/downed/vox_cast_plr_0_revive_down_4.ogg
voice_lines/dempsy/fire_sale/vox_cast_plr_0_powerup_firesale_2.ogg
voice_lines/dempsy/fire_sale/vox_cast_plr_0_powerup_firesale_4.ogg
voice_lines/dempsy/fire_sale/vox_cast_plr_0_powerup_firesale_4_s.ogg
voice_lines/dempsy/headshot/vox_cast_plr_0_kill_headshot_1.ogg
voice_lines/dempsy/headshot/vox_cast_plr_0_kill_headshot_2.ogg
voice_lines/dempsy/headshot/vox_cast_plr_0_kill_headshot_4.ogg
voice_lines/dempsy/headshot/vox_cast_plr_0_kill_headshot_6.ogg
voice_lines/dempsy/insta_kill/vox_cast_plr_0_powerup_insta_2.ogg
voice_lines/dempsy/insta_kill/vox_cast_plr_0_powerup_insta_3.ogg
voice_lines/dempsy/insta_kill/vox_cast_plr_0_powerup_insta_4.ogg
voice_lines/dempsy/kill/vox_cast_plr_0_kill_damaged_0.ogg
voice_lines/dempsy/kill/vox_cast_plr_0_kill_damaged_1.ogg
voice_lines/dempsy/kill/vox_cast_plr_0_kill_damaged_3.ogg
voice_lines/dempsy/kill/vox_cast_plr_0_kill_demongate_0.ogg
voice_lines/dempsy/max_ammo/vox_cast_plr_0_powerup_ammo_0.ogg
voice_lines/dempsy/max_ammo/vox_cast_plr_0_powerup_ammo_1.ogg
voice_lines/dempsy/max_ammo/vox_cast_plr_0_powerup_ammo_2.ogg
voice_lines/dempsy/no_ammo/vox_cast_plr_0_ammo_out_1.ogg
voice_lines/dempsy/no_ammo/vox_cast_plr_0_ammo_out_2.ogg
voice_lines/dempsy/no_ammo/vox_cast_plr_0_ammo_out_3.ogg
voice_lines/dempsy/nuke/vox_cast_plr_0_powerup_nuke_0.ogg
voice_lines/dempsy/nuke/vox_cast_plr_0_powerup_nuke_2.ogg
voice_lines/dempsy/nuke/vox_cast_plr_0_powerup_nuke_4.ogg
voice_lines/dempsy/perk_pickup/vox_cast_plr_0_perk_generic_6.ogg
voice_lines/dempsy/perk_pickup/vox_cast_plr_0_perk_generic_8.ogg
voice_lines/dempsy/perk_pickup/vox_cast_plr_0_perk_generic_9.ogg
voice_lines/dempsy/rebuild_barrier/vox_cast_plr_0_rebuild_boards_0.ogg
voice_lines/dempsy/rebuild_barrier/vox_cast_plr_0_rebuild_boards_2.ogg
voice_lines/dempsy/rebuild_barrier/vox_cast_plr_0_rebuild_boards_4_s.ogg
voice_lines/dempsy/revive_other/vox_cast_plr_0_revive_support_0.ogg
voice_lines/dempsy/revive_other/vox_cast_plr_0_revive_support_1.ogg
voice_lines/dempsy/revive_other/vox_cast_plr_0_revive_support_2.ogg
voice_lines/dempsy/revived/vox_cast_plr_0_revive_thanks_0.ogg
voice_lines/dempsy/revived/vox_cast_plr_0_revive_thanks_1.ogg
voice_lines/dempsy/revived/vox_cast_plr_0_revive_thanks_2.ogg
voice_lines/dempsy/take_damage/vox_cast_plr_0_attacked_zombie_2.ogg
voice_lines/dempsy/take_damage/vox_cast_plr_0_attacked_zombie_3.ogg
voice_lines/dempsy/take_damage/vox_cast_plr_0_attacked_zombie_9.ogg
voice_lines/dempsy/wall_buy/vox_cast_plr_0_generic_wall_buy_0.ogg
voice_lines/dempsy/wall_buy/vox_cast_plr_0_generic_wall_buy_1.ogg
voice_lines/dempsy/wall_buy/vox_cast_plr_0_generic_wall_buy_3.ogg
voice_lines/nicholai/box_gun/vox_cast_plr_1_box_ar_0.ogg
voice_lines/nicholai/box_gun/vox_cast_plr_1_box_ar_1.ogg
voice_lines/nicholai/box_gun/vox_cast_plr_1_box_ar_2.ogg
voice_lines/nicholai/box_gun/vox_cast_plr_1_box_raygun_2.ogg
voice_lines/nicholai/box_gun/vox_cast_plr_1_box_shotgun_0.ogg
voice_lines/nicholai/carpenter/vox_cast_plr_1_powerup_carpenter_1.ogg
voice_lines/nicholai/carpenter/vox_cast_plr_1_powerup_carpenter_2.ogg
voice_lines/nicholai/carpenter/vox_cast_plr_1_powerup_carpenter_3.ogg
voice_lines/nicholai/crawler_kill/vox_cast_plr_1_crawler_kill_1.ogg
voice_lines/nicholai/crawler_kill/vox_cast_plr_1_crawler_kill_2.ogg
voice_lines/nicholai/crawler_kill/vox_cast_plr_1_crawler_kill_3.ogg
voice_lines/nicholai/crawler_kill/vox_cast_plr_1_crawler_kill_4.ogg
voice_lines/nicholai/dog/vox_cast_plr_1_spawn_hellhound_0.ogg
voice_lines/nicholai/dog/vox_cast_plr_1_spawn_hellhound_2.ogg
voice_lines/nicholai/dog/vox_cast_plr_1_spawn_hellhound_4.ogg
voice_lines/nicholai/double_points/vox_cast_plr_1_powerup_double_0.ogg
voice_lines/nicholai/double_points/vox_cast_plr_1_powerup_double_1.ogg
voice_lines/nicholai/double_points/vox_cast_plr_1_powerup_double_3.ogg
voice_lines/nicholai/downed/vox_cast_plr_1_revive_down_2.ogg
voice_lines/nicholai/downed/vox_cast_plr_1_revive_down_3.ogg
voice_lines/nicholai/downed/vox_cast_plr_1_revive_down_4.ogg
voice_lines/nicholai/fire_sale/vox_cast_plr_1_powerup_firesale_1.ogg
voice_lines/nicholai/fire_sale/vox_cast_plr_1_powerup_firesale_3.ogg
voice_lines/nicholai/fire_sale/vox_cast_plr_1_powerup_firesale_4.ogg
voice_lines/nicholai/headshot/vox_cast_plr_1_kill_headshot_1.ogg
voice_lines/nicholai/headshot/vox_cast_plr_1_kill_headshot_4.ogg
voice_lines/nicholai/headshot/vox_cast_plr_1_kill_headshot_6.ogg
voice_lines/nicholai/headshot/vox_cast_plr_1_kill_headshot_8.ogg
voice_lines/nicholai/insta_kill/vox_cast_plr_1_powerup_insta_0.ogg
voice_lines/nicholai/insta_kill/vox_cast_plr_1_powerup_insta_2.ogg
voice_lines/nicholai/insta_kill/vox_cast_plr_1_powerup_insta_3.ogg
voice_lines/nicholai/kill/vox_cast_plr_1_kill_damaged_0.ogg
voice_lines/nicholai/kill/vox_cast_plr_1_kill_damaged_1.ogg
voice_lines/nicholai/kill/vox_cast_plr_1_kill_damaged_3.ogg
voice_lines/nicholai/max_ammo/vox_cast_plr_1_powerup_ammo_0.ogg
voice_lines/nicholai/max_ammo/vox_cast_plr_1_powerup_ammo_3.ogg
voice_lines/nicholai/max_ammo/vox_cast_plr_1_powerup_ammo_4.ogg
voice_lines/nicholai/no_ammo/vox_cast_plr_1_ammo_out_0.ogg
voice_lines/nicholai/no_ammo/vox_cast_plr_1_ammo_out_1.ogg
voice_lines/nicholai/no_ammo/vox_cast_plr_1_ammo_out_4.ogg
voice_lines/nicholai/nuke/vox_cast_plr_1_powerup_nuke_0.ogg
voice_lines/nicholai/nuke/vox_cast_plr_1_powerup_nuke_1.ogg
voice_lines/nicholai/nuke/vox_cast_plr_1_powerup_nuke_4.ogg
voice_lines/nicholai/perk_pickup/vox_cast_plr_1_perk_generic_2.ogg
voice_lines/nicholai/perk_pickup/vox_cast_plr_1_perk_generic_3.ogg
voice_lines/nicholai/perk_pickup/vox_cast_plr_1_perk_generic_4.ogg
voice_lines/nicholai/perk_pickup/vox_cast_plr_1_perk_generic_9.ogg
voice_lines/nicholai/rebuild_barrier/vox_cast_plr_1_rebuild_boards_0.ogg
voice_lines/nicholai/rebuild_barrier/vox_cast_plr_1_rebuild_boards_1.ogg
voice_lines/nicholai/rebuild_barrier/vox_cast_plr_1_rebuild_boards_2.ogg
voice_lines/nicholai/revive_other/vox_cast_plr_1_revive_support_0.ogg
voice_lines/nicholai/revive_other/vox_cast_plr_1_revive_support_1.ogg
voice_lines/nicholai/revive_other/vox_cast_plr_1_revive_support_3.ogg
voice_lines/nicholai/revived/vox_cast_plr_1_revive_thanks_0.ogg
voice_lines/nicholai/revived/vox_cast_plr_1_revive_thanks_2.ogg
voice_lines/nicholai/revived/vox_cast_plr_1_revive_thanks_4.ogg
voice_lines/nicholai/take_damage/vox_cast_plr_1_attacked_zombie_0.ogg
voice_lines/nicholai/take_damage/vox_cast_plr_1_attacked_zombie_1.ogg
voice_lines/nicholai/take_damage/vox_cast_plr_1_attacked_zombie_2.ogg
voice_lines/nicholai/take_damage/vox_cast_plr_1_attacked_zombie_8.ogg
voice_lines/nicholai/wall_buy/vox_cast_plr_1_generic_wall_buy_0.ogg
voice_lines/nicholai/wall_buy/vox_cast_plr_1_generic_wall_buy_2.ogg
voice_lines/nicholai/wall_buy/vox_cast_plr_1_generic_wall_buy_4.ogg
voice_lines/rictophen/box_gun/vox_cast_plr_2_box_ar_1.ogg
voice_lines/rictophen/box_gun/vox_cast_plr_2_box_ar_2.ogg
voice_lines/rictophen/box_gun/vox_cast_plr_2_box_ar_4.ogg
voice_lines/rictophen/box_gun/vox_cast_plr_2_box_mg_0.ogg
voice_lines/rictophen/box_gun/vox_cast_plr_2_box_mg_2.ogg
voice_lines/rictophen/carpenter/vox_cast_plr_2_powerup_carpenter_1.ogg
voice_lines/rictophen/carpenter/vox_cast_plr_2_powerup_carpenter_3.ogg
voice_lines/rictophen/carpenter/vox_cast_plr_2_powerup_carpenter_4.ogg
voice_lines/rictophen/crawler_kill/vox_cast_plr_2_crawler_kill_1.ogg
voice_lines/rictophen/crawler_kill/vox_cast_plr_2_crawler_kill_3.ogg
voice_lines/rictophen/crawler_kill/vox_cast_plr_2_crawler_kill_4.ogg
voice_lines/rictophen/dog/vox_cast_plr_2_spawn_hellhound_1.ogg
voice_lines/rictophen/dog/vox_cast_plr_2_spawn_hellhound_2.ogg
voice_lines/rictophen/dog/vox_cast_plr_2_spawn_hellhound_4.ogg
voice_lines/rictophen/double_points/vox_cast_plr_2_powerup_double_0.ogg
voice_lines/rictophen/double_points/vox_cast_plr_2_powerup_double_3.ogg
voice_lines/rictophen/double_points/vox_cast_plr_2_powerup_double_4.ogg
voice_lines/rictophen/downed/vox_cast_plr_2_revive_down_0.ogg
voice_lines/rictophen/downed/vox_cast_plr_2_revive_down_3.ogg
voice_lines/rictophen/downed/vox_cast_plr_2_revive_down_4.ogg
voice_lines/rictophen/fire_sale/vox_cast_plr_2_powerup_firesale_2.ogg
voice_lines/rictophen/fire_sale/vox_cast_plr_2_powerup_firesale_3.ogg
voice_lines/rictophen/fire_sale/vox_cast_plr_2_powerup_firesale_4.ogg
voice_lines/rictophen/headshot/vox_cast_plr_2_kill_headshot_1.ogg
voice_lines/rictophen/headshot/vox_cast_plr_2_kill_headshot_4.ogg
voice_lines/rictophen/headshot/vox_cast_plr_2_kill_headshot_6.ogg
voice_lines/rictophen/headshot/vox_cast_plr_2_kill_headshot_7.ogg
voice_lines/rictophen/insta_kill/vox_cast_plr_2_powerup_insta_1.ogg
voice_lines/rictophen/insta_kill/vox_cast_plr_2_powerup_insta_2.ogg
voice_lines/rictophen/insta_kill/vox_cast_plr_2_powerup_insta_3.ogg
voice_lines/rictophen/kill/vox_cast_plr_2_kill_damaged_0.ogg
voice_lines/rictophen/kill/vox_cast_plr_2_kill_damaged_1.ogg
voice_lines/rictophen/kill/vox_cast_plr_2_kill_damaged_2.ogg
voice_lines/rictophen/max_ammo/vox_cast_plr_2_powerup_ammo_1.ogg
voice_lines/rictophen/max_ammo/vox_cast_plr_2_powerup_ammo_3.ogg
voice_lines/rictophen/max_ammo/vox_cast_plr_2_powerup_ammo_4.ogg
voice_lines/rictophen/no_ammo/vox_cast_plr_2_ammo_out_0.ogg
voice_lines/rictophen/no_ammo/vox_cast_plr_2_ammo_out_2.ogg
voice_lines/rictophen/no_ammo/vox_cast_plr_2_ammo_out_3.ogg
voice_lines/rictophen/nuke/vox_cast_plr_2_powerup_nuke_0.ogg
voice_lines/rictophen/nuke/vox_cast_plr_2_powerup_nuke_2.ogg
voice_lines/rictophen/nuke/vox_cast_plr_2_powerup_nuke_3.ogg
voice_lines/rictophen/nuke/vox_cast_plr_2_powerup_nuke_4.ogg
voice_lines/rictophen/perk_pickup/vox_cast_plr_2_perk_generic_3.ogg
voice_lines/rictophen/perk_pickup/vox_cast_plr_2_perk_generic_5.ogg
voice_lines/rictophen/perk_pickup/vox_cast_plr_2_perk_generic_7.ogg
voice_lines/rictophen/perk_pickup/vox_cast_plr_2_perk_generic_9.ogg
voice_lines/rictophen/rebuild_barrier/vox_cast_plr_2_rebuild_boards_0.ogg
voice_lines/rictophen/rebuild_barrier/vox_cast_plr_2_rebuild_boards_2.ogg
voice_lines/rictophen/rebuild_barrier/vox_cast_plr_2_rebuild_boards_3.ogg
voice_lines/rictophen/rebuild_barrier/vox_cast_plr_2_rebuild_boards_4.ogg
voice_lines/rictophen/revive_other/vox_cast_plr_2_revive_support_2.ogg
voice_lines/rictophen/revive_other/vox_cast_plr_2_revive_support_3.ogg
voice_lines/rictophen/revive_other/vox_cast_plr_2_revive_support_4.ogg
voice_lines/rictophen/revived/vox_cast_plr_2_revive_thanks_0.ogg
voice_lines/rictophen/revived/vox_cast_plr_2_revive_thanks_1.ogg
voice_lines/rictophen/revived/vox_cast_plr_2_revive_thanks_4.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_0.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_1.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_2.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_4.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_7.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_8.ogg
voice_lines/rictophen/take_damage/vox_cast_plr_2_attacked_zombie_9.ogg
voice_lines/rictophen/wall_buy/vox_cast_plr_2_generic_wall_buy_0.ogg
voice_lines/rictophen/wall_buy/vox_cast_plr_2_generic_wall_buy_4.ogg
voice_lines/rictophen/wall_buy/vox_cast_plr_2_generic_wall_buy_7.ogg
voice_lines/takeo/box_gun/vox_cast_plr_3_box_ar_0.ogg
voice_lines/takeo/box_gun/vox_cast_plr_3_box_ar_4.ogg
voice_lines/takeo/box_gun/vox_cast_plr_3_box_mg_0.ogg
voice_lines/takeo/box_gun/vox_cast_plr_3_box_mg_3.ogg
voice_lines/takeo/box_gun/vox_cast_plr_3_box_shotgun_0.ogg
voice_lines/takeo/carpenter/vox_cast_plr_3_powerup_carpenter_1.ogg
voice_lines/takeo/carpenter/vox_cast_plr_3_powerup_carpenter_3.ogg
voice_lines/takeo/carpenter/vox_cast_plr_3_powerup_carpenter_4.ogg
voice_lines/takeo/crawler_kill/vox_cast_plr_3_crawler_kill_1.ogg
voice_lines/takeo/crawler_kill/vox_cast_plr_3_crawler_kill_3.ogg
voice_lines/takeo/crawler_kill/vox_cast_plr_3_crawler_kill_4.ogg
voice_lines/takeo/dog/vox_cast_plr_3_spawn_hellhound_0.ogg
voice_lines/takeo/dog/vox_cast_plr_3_spawn_hellhound_3.ogg
voice_lines/takeo/dog/vox_cast_plr_3_spawn_hellhound_4.ogg
voice_lines/takeo/double_points/vox_cast_plr_3_powerup_double_0.ogg
voice_lines/takeo/double_points/vox_cast_plr_3_powerup_double_1.ogg
voice_lines/takeo/double_points/vox_cast_plr_3_powerup_double_4.ogg
voice_lines/takeo/downed/vox_cast_plr_3_revive_down_1.ogg
voice_lines/takeo/downed/vox_cast_plr_3_revive_down_3.ogg
voice_lines/takeo/downed/vox_cast_plr_3_revive_down_4.ogg
voice_lines/takeo/fire_sale/vox_cast_plr_3_powerup_firesale_3.ogg
voice_lines/takeo/fire_sale/vox_cast_plr_3_powerup_firesale_4.ogg
voice_lines/takeo/fire_sale/vox_cast_plr_3_powerup_firesale_5.ogg
voice_lines/takeo/headshot/vox_cast_plr_3_kill_headshot_1.ogg
voice_lines/takeo/headshot/vox_cast_plr_3_kill_headshot_3.ogg
voice_lines/takeo/headshot/vox_cast_plr_3_kill_headshot_4.ogg
voice_lines/takeo/headshot/vox_cast_plr_3_kill_headshot_7.ogg
voice_lines/takeo/insta_kill/vox_cast_plr_3_powerup_insta_0.ogg
voice_lines/takeo/insta_kill/vox_cast_plr_3_powerup_insta_2.ogg
voice_lines/takeo/insta_kill/vox_cast_plr_3_powerup_insta_4.ogg
voice_lines/takeo/kill/vox_cast_plr_3_kill_damaged_1.ogg
voice_lines/takeo/kill/vox_cast_plr_3_kill_damaged_2.ogg
voice_lines/takeo/kill/vox_cast_plr_3_kill_damaged_3.ogg
voice_lines/takeo/max_ammo/vox_cast_plr_3_powerup_ammo_0.ogg
voice_lines/takeo/max_ammo/vox_cast_plr_3_powerup_ammo_1.ogg
voice_lines/takeo/max_ammo/vox_cast_plr_3_powerup_ammo_3.ogg
voice_lines/takeo/no_ammo/vox_cast_plr_3_ammo_out_0.ogg
voice_lines/takeo/no_ammo/vox_cast_plr_3_ammo_out_3.ogg
voice_lines/takeo/no_ammo/vox_cast_plr_3_ammo_out_4.ogg
voice_lines/takeo/nuke/vox_cast_plr_3_powerup_nuke_0.ogg
voice_lines/takeo/nuke/vox_cast_plr_3_powerup_nuke_1.ogg
voice_lines/takeo/nuke/vox_cast_plr_3_powerup_nuke_3.ogg
voice_lines/takeo/perk_pickup/vox_cast_plr_3_perk_generic_1.ogg
voice_lines/takeo/perk_pickup/vox_cast_plr_3_perk_generic_3.ogg
voice_lines/takeo/perk_pickup/vox_cast_plr_3_perk_generic_6.ogg
voice_lines/takeo/rebuild_barrier/vox_cast_plr_3_rebuild_boards_1.ogg
voice_lines/takeo/rebuild_barrier/vox_cast_plr_3_rebuild_boards_2.ogg
voice_lines/takeo/rebuild_barrier/vox_cast_plr_3_rebuild_boards_4.ogg
voice_lines/takeo/revive_other/vox_cast_plr_3_revive_support_1.ogg
voice_lines/takeo/revive_other/vox_cast_plr_3_revive_support_2.ogg
voice_lines/takeo/revive_other/vox_cast_plr_3_revive_support_4.ogg
voice_lines/takeo/revived/vox_cast_plr_3_revive_thanks_0.ogg
voice_lines/takeo/revived/vox_cast_plr_3_revive_thanks_2.ogg
voice_lines/takeo/revived/vox_cast_plr_3_revive_thanks_4.ogg
voice_lines/takeo/take_damage/vox_cast_plr_3_attacked_zombie_2.ogg
voice_lines/takeo/take_damage/vox_cast_plr_3_attacked_zombie_3.ogg
voice_lines/takeo/take_damage/vox_cast_plr_3_attacked_zombie_7.ogg
voice_lines/takeo/wall_buy/vox_cast_plr_3_generic_wall_buy_1.ogg
voice_lines/takeo/wall_buy/vox_cast_plr_3_generic_wall_buy_6.ogg
voice_lines/takeo/wall_buy/vox_cast_plr_3_generic_wall_buy_9.ogg
```

</details>

<details><summary>wonderfizz (4 files)</summary>

```text
wonderfizz/rand_perk_mach_leave.ogg
wonderfizz/rand_perk_mach_loop.ogg
wonderfizz/rand_perk_mach_start.ogg
wonderfizz/rand_perk_mach_stop.ogg
```

</details>

The base pack sound catalog is [`assets/zbk/sounds.json`](zombies_build_kit/assets/zbk/sounds.json). Change it only when you need different sound-event behavior; replacing individual `.ogg` files does not require a catalog change.

## Pack contents

| Folder | Use |
| --- | --- |
| [`zombies_build_kit`](zombies_build_kit/README.md) | Released base pack runtime resource pack |
| [`zombies_build_kit_vivecraft_overlay`](zombies_build_kit_vivecraft_overlay/README.md) | Released optional base pack Vivecraft overlay |
| [`zbk_nacht_der_untoten`](zbk_nacht_der_untoten/README.md) | Nacht source reference for world bundles; no separate release asset |
| [`zbk_der_eisendrache`](zbk_der_eisendrache/README.md) | Der Eisendrache source reference for world bundles; no separate release asset |
| [`zbk_der_eisendrache_vivecraft_overlay`](zbk_der_eisendrache_vivecraft_overlay/README.md) | DE Vivecraft source reference; no separate release asset |

## License and credit

Keep the packaged `LICENSES/` folder with each pack when distributing it. ZBK assets use the repository's noncommercial asset license and media permission. Third-party notices are preserved in each installable pack. See [licensing and attribution](LICENSES/LICENSE.md).
