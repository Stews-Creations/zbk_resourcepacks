"""Export native single-item models from a supplied directory of Blockbench projects.

Usage: python tools/export_core_machines.py PATH_TO_MODELS
Authoring projects are inputs only; runtime packs contain JSON and PNG files.
"""
import argparse
import base64
from copy import deepcopy
import hashlib
import io
import json
import math
import itertools
from pathlib import Path
from PIL import Image
from optimize_core_machines import mirror, optimize, pack_texture

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'zombies_build_kit/assets/zbk'
NAMES = ['death_machine', 'juggernog', 'stamina_up', 'speed_cola', 'double_tap', 'quick_revive', 'mule_kick', 'wunderfizz']
# Every cabinet embeds the same material atlas; the pack stores it once.
SHARED = {'perk_materials_hd.png': 'item/map_elements/perks/perk_materials'}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def export(source):
    shared, written = {}, set()
    for name in NAMES:
        slug = 'stamin_up' if name == 'stamina_up' else name
        data = json.loads((source / f'{slug}.bbmodel').read_text(encoding='utf-8'))
        target = f'item/guns/special/{name}' if name == 'death_machine' else f'item/map_elements/perks/{name}'
        path = ASSETS / f'models/{target}.json'
        poses = json.loads(path.read_text()).get('display', {}) if path.exists() else {}
        textures, elements, mappings = {}, [], {}
        cubes = [cube for cube in data['elements'] if cube.get('export') is not False]
        used = {face['texture'] for cube in cubes for face in cube['faces'].values() if face.get('texture') is not None}
        for index in sorted(used):
            texture = data['textures'][index]
            content = base64.b64decode(texture['source'].split(',', 1)[1])
            asset = f'item/guns/special/{name}_{index}' if name == 'death_machine' else f'item/map_elements/perks/{name}_{index}'
            if name != 'death_machine':
                width = texture.get('uv_width', data['resolution']['width'])
                height = texture.get('uv_height', data['resolution']['height'])
                rects = [[v * 16 / (width if i % 2 == 0 else height) for i, v in enumerate(face['uv'])]
                         for cube in cubes for face in cube['faces'].values() if face.get('texture') == index]
                asset = SHARED.get(texture['name'], asset)
                image, mappings[index] = pack_texture(Image.open(io.BytesIO(content)), rects, crop=texture['name'] not in SHARED)
                if shared.setdefault(asset, hashlib.sha256(content).digest()) != hashlib.sha256(content).digest():
                    raise ValueError(f'{name}: {texture["name"]} differs from the shared copy')
                content = io.BytesIO()
                image.save(content, 'PNG', optimize=True)
                content = content.getvalue()
            png = ASSETS / f'textures/{asset}.png'
            png.parent.mkdir(parents=True, exist_ok=True)
            png.write_bytes(content)
            written.add(png)
            textures[str(index)] = f'zbk:{asset}'
        for cube in data['elements']:
            if cube.get('export') is False:
                continue
            element = {key: cube[key] for key in ('from', 'to')}
            # Fine contour slices rely on disabled face shading to read as a
            # continuous curved surface rather than alternating dark ridges.
            if 'shade' in cube:
                element['shade'] = bool(cube['shade'])
            if any(value < -16 or value > 32 for key in ('from', 'to') for value in cube[key]):
                raise ValueError(f'{name}: out-of-bounds cube')
            rotation = cube.get('rotation', [0, 0, 0])
            axes = [i for i, value in enumerate(rotation) if value]
            if axes:
                if len(axes) != 1 or rotation[axes[0]] not in (-45, -22.5, 22.5, 45):
                    raise ValueError(f'{name}: unsupported native rotation')
                element['rotation'] = {'origin': cube['origin'], 'axis': 'xyz'[axes[0]], 'angle': rotation[axes[0]]}
                if cube.get('rescale'):
                    element['rotation']['rescale'] = True
            element['faces'] = {}
            for direction, face in cube['faces'].items():
                index = face.get('texture')
                if index is None:
                    continue
                texture = data['textures'][index]
                width = texture.get('uv_width', data['resolution']['width'])
                height = texture.get('uv_height', data['resolution']['height'])
                exported = {'uv': [v * 16 / (width if i % 2 == 0 else height) for i, v in enumerate(face['uv'])], 'texture': f'#{index}'}
                if index in mappings:
                    su, ou, sv, ov = mappings[index]
                    exported['uv'] = [v * (su if i % 2 == 0 else sv) + (ou if i % 2 == 0 else ov) for i, v in enumerate(exported['uv'])]
                if face.get('rotation'):
                    exported['rotation'] = face['rotation']
                element['faces'][direction] = exported
            elements.append(element)
        textures['particle'] = '#' + min(textures)
        model = {'credit': 'ZBK reference-based machine model', 'textures': textures, 'elements': elements}
        if name != 'death_machine':
            # Center the actual rotated footprint and put its lowest point on the floor.
            # Measure the source in its runtime orientation, before simplification.
            placed = deepcopy(elements)
            mirror(placed)
            points = []
            for element in placed:
                for corner in itertools.product(*zip(element['from'], element['to'])):
                    point = list(corner)
                    rotation = element.get('rotation')
                    if rotation:
                        axis = 'xyz'.index(rotation['axis'])
                        a, b = (axis + 1) % 3, (axis + 2) % 3
                        origin = rotation['origin']
                        angle = math.radians(rotation['angle'])
                        x, y = point[a] - origin[a], point[b] - origin[b]
                        point[a] = origin[a] + x * math.cos(angle) - y * math.sin(angle)
                        point[b] = origin[b] + x * math.sin(angle) + y * math.cos(angle)
                    points.append(point)
            low = [min(p[i] for p in points) for i in range(3)]
            high = [max(p[i] for p in points) for i in range(3)]
            poses = {'fixed': {'translation': [8 - (low[0] + high[0]) / 2, 8 - low[1], 8 - (low[2] + high[2]) / 2]}}
        model['display'] = poses
        if name != 'death_machine':
            names = [cube['name'] for cube in cubes]
            art = {f'#{index}' for index in used if index and data['textures'][index]['name'] not in SHARED}
            before, after = optimize(model, names, ASSETS, art)
            print(f'{name}: elements {before[0]} -> {after[0]}, faces {before[1]} -> {after[1]}')
        write(path, model)
        item = f'guns/special/{name}' if name == 'death_machine' else f'map_elements/perks/{name}'
        write(ASSETS / f'items/{item}.json', {'model': {'type': 'minecraft:model', 'model': f'zbk:{target}'}})
        if name == 'death_machine':
            overlay = ROOT / f'zombies_build_kit_vivecraft_overlay/assets/zbk/models/{target}.json'
            vr_poses = json.loads(overlay.read_text()).get('display', {})
            # Inherit geometry through a separate model to avoid a self-parent override.
            geometry = {key: value for key, value in model.items() if key != 'display'}
            write(ASSETS / 'models/item/guns/special/death_machine_geometry.json', geometry)
            write(path, {'parent': 'zbk:item/guns/special/death_machine_geometry', 'display': poses})
            write(overlay, {'parent': 'zbk:item/guns/special/death_machine_geometry', 'display': vr_poses})
        print(f'{name}: {len(model["elements"])} cubes in one model')
    # Earlier exports wrote one material atlas per cabinet.
    for png in (ASSETS / 'textures/item/map_elements/perks').glob('*.png'):
        if png not in written:
            png.unlink()
            print(f'removed stale {png.name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    export(parser.parse_args().source)
