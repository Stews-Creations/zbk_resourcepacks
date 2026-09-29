"""Validate Core machine JSON, texture dependencies, and shared Death Machine poses."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'zombies_build_kit/assets/zbk'
atlas = json.loads((ROOT / 'zombies_build_kit/assets/minecraft/atlases/items.json').read_text())
assert {'type': 'minecraft:directory', 'source': 'item/guns/special', 'prefix': 'item/guns/special/'} in atlas['sources'], 'Machine textures must be registered in the item atlas, not merely present on disk.'
for pack in ('zombies_build_kit', 'zombies_build_kit_vivecraft_overlay'):
    model = json.loads((ROOT / pack / 'assets/zbk/models/item/guns/special/death_machine.json').read_text())
    assert model['parent'] == 'zbk:item/guns/special/death_machine_geometry'
    assert model['display']
geometry = json.loads((ASSETS / 'models/item/guns/special/death_machine_geometry.json').read_text())
assert geometry['elements']
for texture in geometry['textures'].values():
    if texture.startswith('#'):
        continue
    assert (ASSETS / f'textures/{texture[4:]}.png').is_file()
print('Passed: Death Machine atlas registration, textures, and shared geometry.')

# Cabinet models must not replace bottle item definitions.
assert {'type': 'minecraft:directory', 'source': 'item/map_elements/perks', 'prefix': 'item/map_elements/perks/'} in atlas['sources']
for name in ('juggernog','stamina_up','speed_cola','double_tap','quick_revive','mule_kick','wunderfizz'):
    item = json.loads((ASSETS / f'items/map_elements/perks/{name}.json').read_text())
    assert item['model']['model'] == f'zbk:item/map_elements/perks/{name}'
    model = json.loads((ASSETS / f'models/item/map_elements/perks/{name}.json').read_text())
    assert model['elements'] and model['display']['fixed']
    for value in model['textures'].values():
        if value.startswith('#'):
            assert value[1:] in model['textures'], f'{name}: unresolved texture {value}'
            continue
        assert (ASSETS / f'textures/{value[4:]}.png').is_file(), value
        # Other sizes lower the mipmap level of every sprite in the item atlas.
        size = Image.open(ASSETS / f'textures/{value[4:]}.png').size
        assert all(16 <= side <= 1024 and side & (side - 1) == 0 for side in size), f'{value}: {size}'
    assert model['textures']['2'] == 'zbk:item/map_elements/perks/perk_materials'
    assert all(face['texture'][1:] in model['textures'] for element in model['elements'] for face in element['faces'].values())
    assert len(model['elements']) <= 320, f'{name}: {len(model["elements"])} cubes'
    if name != 'wunderfizz':
        bottle = json.loads((ASSETS / f'items/perks/{name}.json').read_text())
        assert bottle['model']['model'] == f'zbk:item/perks/{name}'
print('Passed: seven cabinet models, atlas registration, power-of-two textures, cube budgets, and separate bottle IDs.')

wunderfizz = json.loads((ASSETS / 'models/item/map_elements/perks/wunderfizz.json').read_text())
assert all(isinstance(element.get('shade'), bool) for element in wunderfizz['elements'])
assert any(element['shade'] is False for element in wunderfizz['elements']), 'Smoothed contours must retain disabled directional shading.'
print('Passed: Wunderfizz preserves explicit shading on its smooth contours.')
