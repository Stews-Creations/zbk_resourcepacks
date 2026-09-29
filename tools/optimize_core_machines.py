"""Runtime simplification for the reviewed perk cabinet exports.

Authoring elements/names are inputs only. Contour slices become enclosing slabs
whose UVs follow the source projection, so artwork stays where it was traced.
Stepped inclines gain smooth covers at their own angle, which Minecraft 26.2
accepts for element rotation. Geometry is mirrored into Minecraft's north-face UV orientation, seams overlap
slightly, and faces are removed only behind opaque, closed cuboids.
Dependencies: numpy and Pillow.
"""
from collections import defaultdict
from copy import deepcopy
import math
import re

import numpy as np
from PIL import Image

EPS = 1e-7
CONTOUR_TOLERANCE = .25  # Largest silhouette step, in model units.
PLAIN_TOLERANCE = 1.6  # Multiplier for parts without artwork.
ORB_LEVELS = 8  # Depth steps between the orb's centre and its front.
ORB_STEPS = 16  # Outline steps between the orb's centre and its rim.
ORB_EDGE = .05  # Width of the artwork band on the side of an orb step, in UV units.
BOTTOM_GAP = 1  # A lowest slice this much narrower than the one above is a tracing gap.
# Stepped inclines that receive a smooth cover, and the parts that rest on them.
SLOPES = {'sloping_control_deck': ('lid_badge',)}
SLOPE_LIFT = .03  # Clearance of a cover above the steps it hides.
SLOPE_EDGE = .05  # Width of the artwork band on the ends of a cover, in UV units.
DECAL_DEPTH = .15  # Thickness of a part laid onto an incline.
SEAM_OVERLAP = .01  # Growth per side; abutting cuboids overlap instead of cracking.
ART_UV_TOLERANCE = .04  # About 2.5 texels of a 1024-pixel texture.
TEXTURE_LIMIT = 1024
DIRECTIONS = {'west': (0, -1), 'east': (0, 1), 'down': (1, -1),
              'up': (1, 1), 'north': (2, -1), 'south': (2, 1)}
# Position axes behind each face's U and V in the authoring projection.
UV_AXES = {'north': (0, 1), 'south': (0, 1), 'east': (2, 1), 'west': (2, 1),
           'up': (0, 2), 'down': (0, 2)}


def samples(element, direction):
    """Authoring (position, uv) pairs for U and V; V runs down the Y axis."""
    a, b = element['from'], element['to']
    u0, v0, u1, v1 = element['faces'][direction]['uv']
    pu, pv = UV_AXES[direction]
    if pv == 1:
        return [(a[pu], u0), (b[pu], u1)], [(b[1], v0), (a[1], v1)]
    return [(a[pu], u0), (b[pu], u1)], [(a[2], v0), (b[2], v1)]


def fit(points):
    """Least-squares line through (position, uv) and its largest residual."""
    p = np.array(points, float)
    if np.ptp(p[:, 0]) < EPS:
        return None
    slope, offset = np.polyfit(p[:, 0], p[:, 1], 1)
    return slope, offset, float(np.abs(slope * p[:, 0] + offset - p[:, 1]).max())


def mergeable(elements):
    first = elements[0]
    return all(not e.get('rotation') and e.get('shade', True) == first.get('shade', True)
               and e['faces'].keys() == first['faces'].keys()
               and all({k: v for k, v in f.items() if k != 'uv'} ==
                       {k: v for k, v in first['faces'][d].items() if k != 'uv'}
                       and not f.get('rotation') for d, f in e['faces'].items())
               for e in elements)


def slab(elements, axis, art=('#1',), tolerance=CONTOUR_TOLERANCE):
    """One cuboid enclosing adjacent slices, or None when artwork would move."""
    if not mergeable(elements):
        return None
    result = deepcopy(elements[len(elements) // 2])
    for a in range(3):
        low = [e['from'][a] for e in elements]
        high = [e['to'][a] for e in elements]
        if a != axis and (max(low) - min(low) > tolerance + EPS or max(high) - min(high) > tolerance + EPS):
            return None
        # Enclose every source slice. Averaging retracts tapered slices from
        # their adjoining shell and trim, which opens gaps.
        result['from'][a], result['to'][a] = min(low), max(high)
    ordered = sorted(elements, key=lambda e: e['from'][axis])
    north = result['faces'].get('north')
    linked = [d for d in result['faces'] if d != 'north' and north and
              all(e['faces'][d] == e['faces']['north'] for e in elements)]
    for direction, face in result['faces'].items():
        if direction in linked:
            continue
        # Faces across the stack are exposed on its end slices only.
        source = elements
        if DIRECTIONS[direction][0] == axis:
            source = [ordered[-1] if DIRECTIONS[direction][1] > 0 else ordered[0]]
        pairs = [samples(e, direction) for e in source]
        lines = [fit([p for pair in pairs for p in pair[i]]) for i in range(2)]
        limit = ART_UV_TOLERANCE if face['texture'] in art else None
        if any(line is None or (limit is not None and line[2] > limit) for line in lines):
            if limit is not None:
                return None
            continue  # Flat materials keep the middle slice's sample.
        if any(line[2] > .5 for line in lines):
            continue
        pu, pv = UV_AXES[direction]
        (su, ou, _), (sv, ov, _) = lines
        a, b = result['from'], result['to']
        v = (b[1], a[1]) if pv == 1 else (a[2], b[2])
        uv = [su * a[pu] + ou, sv * v[0] + ov, su * b[pu] + ou, sv * v[1] + ov]
        if limit is not None and (min(uv) < -limit or max(uv) > 16 + limit):
            return None
        face['uv'] = [min(16, max(0, value)) for value in uv]
    for direction in linked:
        result['faces'][direction] = deepcopy(result['faces']['north'])
    return result


def chains(elements, axis, art=('#1',), tolerance=CONTOUR_TOLERANCE):
    """Group touching slices along one axis; unrelated parts stay apart."""
    others = [a for a in range(3) if a != axis]
    result = []
    for e in sorted(elements, key=lambda e: e['from'][axis]):
        for chain in result:
            last = chain[-1]
            if (abs(last['to'][axis] - e['from'][axis]) < 1e-6 and
                    all(last['from'][a] < e['to'][a] - EPS and e['from'][a] < last['to'][a] - EPS for a in others)
                    and slab(chain + [e], axis, art, tolerance)):
                chain.append(e)
                break
        else:
            result.append([e])
    return result


def stack(elements, axis, art=('#1',), tolerance=CONTOUR_TOLERANCE):
    """Merge chains of touching slices along one axis."""
    return [slab(chain, axis, art, tolerance) if len(chain) > 1 else chain[0]
            for chain in chains(elements, axis, art, tolerance)]


def incline(steps, decals, art=('#1',), tolerance=CONTOUR_TOLERANCE):
    """Cover a stepped incline with smooth plates and lay its decals onto it.

    Steps alone show their artwork as stripes, and a part traced onto the
    incline from the front stands upright on it. The steps stay underneath as
    the solid body, recessed beneath the covers. Each cover reaches below the
    inner corners of its steps, so it is closed from every side. Returns None
    unless the step fronts follow one straight line.
    """
    line = fit([(e['to'][1], e['from'][2]) for e in steps])
    if line is None or line[2] > .05 or line[0] < EPS:
        return None
    run, offset = line[:2]
    angle = -math.degrees(math.atan2(1, run))

    def plate(part, bottom, top):
        """A cuboid along the incline between two heights above its surface."""
        a, b = part['from'], part['to']
        front = run * a[1] + offset
        u0, v0, u1, v1 = part['faces']['north']['uv']
        edge = SLOPE_EDGE if v1 > v0 else -SLOPE_EDGE
        faces = {'up': [u0, v1, u1, v0], 'north': [u0, v1 - edge, u1, v1], 'south': [u0, v0, u1, v0 + edge]}
        result = {'from': [a[0], a[1] + bottom, front],
                  'to': [b[0], a[1] + top, front + math.hypot(b[1] - a[1], run * (b[1] - a[1]))],
                  'shade': part.get('shade', True),
                  'rotation': {'origin': [8, a[1], front], 'axis': 'x', 'angle': angle},
                  'faces': {d: {**part['faces']['north'], 'uv': uv} for d, uv in faces.items()}}
        for direction in ('east', 'west'):
            if direction in part['faces']:
                result['faces'][direction] = deepcopy(part['faces'][direction])
        return result

    groups = chains(steps, 1, art, tolerance)
    rise = max(max(e['to'][1] for e in chain) - min(e['from'][1] for e in chain) for chain in groups)
    sunk = run * rise / math.hypot(1, run) + .05
    result = []
    for chain in groups:
        body = slab(chain, 1, art, tolerance) if len(chain) > 1 else deepcopy(chain[0])
        body['from'][2] = max(e['from'][2] for e in chain)
        cover = plate(body, -sunk, SLOPE_LIFT)
        # An incline wider than the part beneath it shows its underside.
        cover['faces']['down'] = deepcopy(cover['faces']['up'])
        result.append(cover)
        # The cover encloses the front of its steps.
        del body['faces']['north']
        result.append(body)
    for group in decals:
        for chain in chains(group, 1, art, tolerance):
            part = slab(chain, 1, art, tolerance) if len(chain) > 1 else chain[0]
            result.append(plate(part, 0, SLOPE_LIFT + DECAL_DEPTH))
    return result


def orb(elements, art=('#1',), levels=ORB_LEVELS, steps=ORB_STEPS):
    """Rebuild the orb's column grid as cuboids sharing its centre.

    Each cuboid reaches the orb's surface with all eight corners, so one
    cuboid shapes every octant and the orb steps evenly toward its front,
    back, top, bottom and sides. Steps straddle the true surface; the deepest
    cuboid keeps the full depth so the front still meets its badge. Cuboids
    that another one contains are left out.

    Fronts and backs keep the projected artwork, and the side of each step
    repeats the artwork along its own edge. Faces of different cuboids can
    share a plane; they show the same texels there. Returns None unless the
    columns describe a sphere.
    """
    centre = [sum((e['from'][a] + e['to'][a]) / 2 for e in elements) / len(elements) for a in range(3)]
    radius = max(e['to'][2] - centre[2] for e in elements)
    lines = [fit([p for e in elements for p in samples(e, 'north')[i]]) for i in range(2)]
    if any(line is None or line[2] > ART_UV_TOLERANCE for line in lines):
        return None
    for e in elements:
        across = sum(((e['from'][a] + e['to'][a]) / 2 - centre[a]) ** 2 for a in range(2))
        if abs(e['to'][2] - centre[2] - math.sqrt(max(0, radius ** 2 - across))) > .05 * radius:
            return None
    area = [extent(e['faces']['north']['uv'][i] for e in elements)
            for i, extent in enumerate((min, min, max, max))]
    (su, ou, _), (sv, ov, _) = lines
    grid, rise = radius / steps, radius / levels

    def outline(level):
        """Half-height in grid steps for each half-width of one level's disc."""
        reach = radius ** 2 - (level * rise - rise / 2) ** 2
        return [int(math.sqrt(max(0, reach - (i * grid - grid / 2) ** 2)) / grid + .5) for i in range(1, steps + 2)]

    result = []
    for level in range(1, levels + 1):
        heights, deeper = outline(level), outline(level + 1) if level < levels else [0] * (steps + 1)
        for i in range(1, steps + 1):
            j = heights[i - 1]
            # Keep the widest cuboid of each height unless a deeper one holds it.
            if j < 1 or heights[i] == j or deeper[i - 1] >= j:
                continue
            half = [i * grid, j * grid, level * rise]
            part = deepcopy(elements[0])
            part['from'] = [c - h for c, h in zip(centre, half)]
            part['to'] = [c + h for c, h in zip(centre, half)]
            a, b = part['from'], part['to']
            u0, u1, v0, v1 = su * a[0] + ou, su * b[0] + ou, sv * b[1] + ov, sv * a[1] + ov
            inward = [ORB_EDGE if value < (area[k % 2] + area[k % 2 + 2]) / 2 else -ORB_EDGE
                      for k, value in enumerate((u0, v0, u1, v1))]
            uvs = {'north': [u0, v0, u1, v1], 'south': [u0, v0, u1, v1],
                   'west': [u0, v0, u0 + inward[0], v1], 'east': [u1 + inward[2], v0, u1, v1],
                   'up': [u0, v0, u1, v0 + inward[1]], 'down': [u0, v1 + inward[3], u1, v1]}
            for direction, face in part['faces'].items():
                face['uv'] = [min(area[k % 2 + 2], max(area[k % 2], value))
                              for k, value in enumerate(uvs[direction])]
            result.append(part)
    return result


def simplify(elements, names, art=('#1',), tolerance=CONTOUR_TOLERANCE):
    groups = defaultdict(list)
    for i, name in enumerate(names):
        groups[re.sub(r'_\d+(?:_\d+)?$', '', name)].append(i)
    resting = {decal for name, decals in SLOPES.items() if name in groups for decal in decals}
    replacements, removed = {}, set()
    for name, indices in groups.items():
        if name in resting:
            continue  # Placed together with its incline.
        parts = [elements[i] for i in indices if not elements[i].get('rotation')]
        if len(parts) < 2:
            continue
        kept = [i for i in indices if not elements[i].get('rotation')]
        plain = not any(f['texture'] in art for e in parts for f in e['faces'].values())
        step = tolerance * (PLAIN_TOLERANCE if plain else 1)
        merged = None
        if name == 'orb_shell':
            merged = orb(parts, art)
        elif name in SLOPES:
            decals = [[elements[i] for i in groups.get(decal, [])] for decal in SLOPES[name]]
            merged = incline(parts, decals, art, step)
            if merged is not None:
                removed.update(i for decal in SLOPES[name] for i in groups.get(decal, []))
        if merged is None:
            # One pass only: merging slabs again would compound their steps.
            merged = min((stack(parts, axis, art, step) for axis in range(3)), key=len)
            if len(merged) >= len(parts):
                continue
        replacements[kept[0]] = merged
        removed.update(kept[1:])
    return [part for i, e in enumerate(elements) if i in replacements or i not in removed
            for part in replacements.get(i, [e])]


def mirror(elements):
    """Flip the model across X=8 into Minecraft's face orientation.

    The authoring projection puts a north face's first U at its low X edge;
    Minecraft puts it at the high X edge. Without the flip every face shows its
    artwork reversed in place, so raised panels and lettering split between
    slices land on the wrong side of the cabinet artwork behind them.
    """
    for e in elements:
        e['from'][0], e['to'][0] = 16 - e['to'][0], 16 - e['from'][0]
        rotation = e.get('rotation')
        if rotation:
            rotation['origin'][0] = 16 - rotation['origin'][0]
            if rotation['axis'] != 'x':
                rotation['angle'] = -rotation['angle']
        faces = e['faces']
        for direction in ('south', 'up', 'down'):
            if direction in faces:
                u0, v0, u1, v1 = faces[direction]['uv']
                faces[direction]['uv'] = [u1, v0, u0, v1]
        east, west = faces.pop('east', None), faces.pop('west', None)
        if west:
            faces['east'] = west
        if east:
            faces['west'] = east


def overlap(elements, amount=SEAM_OVERLAP):
    """Grow every cuboid slightly and extend its UVs by the same distance.

    Faces that only share part of an edge can leave pixel-wide cracks. Growing
    all cuboids equally keeps coplanar faces coplanar and joins their seams.
    """
    for e in elements:
        size = [b - a for a, b in zip(e['from'], e['to'])]
        for direction, face in e['faces'].items():
            if face.get('rotation'):
                continue
            pu, pv = UV_AXES[direction]
            u0, v0, u1, v1 = face['uv']
            du, dv = (u1 - u0) / size[pu] * amount, (v1 - v0) / size[pv] * amount
            face['uv'] = [min(16, max(0, value)) for value in (u0 - du, v0 - dv, u1 + du, v1 + dv)]
        e['from'] = [value - amount for value in e['from']]
        e['to'] = [value + amount for value in e['to']]


def covered(rect, blockers):
    """Exact rectangle-union coverage, retaining partially exposed faces."""
    pending = [rect]
    for x0, y0, x1, y1 in blockers:
        remaining = []
        for a, b, c, d in pending:
            l, t, r, u = max(a, x0), max(b, y0), min(c, x1), min(d, y1)
            if r <= l + EPS or u <= t + EPS:
                remaining.append((a, b, c, d))
                continue
            if l > a + EPS: remaining.append((a, b, l, d))
            if r < c - EPS: remaining.append((r, b, c, d))
            if t > b + EPS: remaining.append((l, b, r, t))
            if u < d - EPS: remaining.append((l, u, r, d))
        pending = remaining
        if not pending:
            return True
    return False


def cull(model, assets):
    elements = model['elements']
    alpha = {}
    for key, value in model['textures'].items():
        if not value.startswith('#'):
            namespace, path = value.split(':')
            alpha['#' + key] = Image.open(assets.parent / namespace / 'textures' / (path + '.png')).convert('RGBA').getchannel('A')
    def opaque(e):
        if e.get('rotation') or set(e['faces']) != set(DIRECTIONS):
            return False
        for face in e['faces'].values():
            image = alpha.get(face['texture'])
            if image is None: return False
            u0, v0, u1, v1 = face['uv']
            # Include adjacent texels so transparent texture boundaries cannot occlude.
            bounds = (max(0, math.floor(min(u0, u1) * image.width / 16) - 1),
                      max(0, math.floor(min(v0, v1) * image.height / 16) - 1),
                      min(image.width, math.ceil(max(u0, u1) * image.width / 16) + 1),
                      min(image.height, math.ceil(max(v0, v1) * image.height / 16) + 1))
            if bounds[2] <= bounds[0] or bounds[3] <= bounds[1] or image.crop(bounds).getextrema()[0] < 255:
                return False
        return True
    low = np.array([e['from'] for e in elements])
    high = np.array([e['to'] for e in elements])
    solids = np.array([opaque(e) for e in elements]) & np.all(high > low + EPS, axis=1)
    result = deepcopy(elements)
    for i, e in enumerate(elements):
        if e.get('rotation'): continue
        for direction in e['faces']:
            axis, sign = DIRECTIONS[direction]
            a, b = [j for j in range(3) if j != axis]
            plane = high[i, axis] if sign > 0 else low[i, axis]
            mask = solids.copy()
            if sign > 0:
                mask &= (low[:, axis] <= plane + EPS) & (high[:, axis] > plane + EPS)
            else:
                mask &= (low[:, axis] < plane - EPS) & (high[:, axis] >= plane - EPS)
            mask &= (low[:, a] < high[i, a] - EPS) & (high[:, a] > low[i, a] + EPS)
            mask &= (low[:, b] < high[i, b] - EPS) & (high[:, b] > low[i, b] + EPS)
            mask[i] = False
            ids = np.flatnonzero(mask)
            blockers = [(low[j, a], low[j, b], high[j, a], high[j, b]) for j in ids]
            if covered((low[i, a], low[i, b], high[i, a], high[i, b]), blockers):
                del result[i]['faces'][direction]
    model['elements'] = [e for e in result if e['faces']]


def level_bottoms(elements, names):
    """Widen a stack's lowest slice to the slice resting on it.

    Outlines traced from a photograph end in a slanted bottom edge, so their
    last slice covers only part of the width and leaves a corner missing
    beneath the rest. Rounded corners narrow gradually and are left alone.
    """
    groups = defaultdict(list)
    for e, name in zip(elements, names):
        if not e.get('rotation'):
            groups[re.sub(r'_\d+(?:_\d+)?$', '', name)].append(e)

    def touching(e, other):
        return all(e['from'][a] < other['to'][a] - EPS and other['from'][a] < e['to'][a] - EPS for a in (0, 2))

    for parts in groups.values():
        for e in parts:
            above = [o for o in parts if abs(o['from'][1] - e['to'][1]) < 1e-6 and touching(e, o)]
            if len(above) != 1 or any(abs(o['to'][1] - e['from'][1]) < 1e-6 and touching(e, o) for o in parts):
                continue
            low, high = above[0]['from'][0], above[0]['to'][0]
            if (low > e['from'][0] + EPS or high < e['to'][0] - EPS
                    or max(e['from'][0] - low, high - e['to'][0]) < BOTTOM_GAP):
                continue
            for direction, face in e['faces'].items():
                if UV_AXES[direction][0] == 0 and not face.get('rotation'):
                    u0, v0, u1, v1 = face['uv']
                    scale = (u1 - u0) / (e['to'][0] - e['from'][0])
                    face['uv'] = [min(16, max(0, u0 - scale * (e['from'][0] - low))), v0,
                                  min(16, max(0, u1 + scale * (high - e['to'][0]))), v1]
            e['from'][0], e['to'][0] = low, high


def connect_mule_kick_fins(elements, names):
    """Extend only the inner edges of the reviewed Mule Kick fins into its shell.

    The original reference tracing leaves air between these separate profiles.
    Use all cabinet slices crossed by each fin, including the tapered bottom.
    Outer silhouette, height, depth, textures and element count stay unchanged.
    """
    cabinet = [e for e, n in zip(elements, names) if n.startswith('green_cabinet_')]
    if not cabinet or not any(n.startswith('left_side_fin_') for n in names):
        return
    for e, name in zip(elements, names):
        if not name.startswith(('left_side_fin_', 'right_side_fin_')):
            continue
        neighbors = [c for c in cabinet if c['from'][1] < e['to'][1] - EPS
                     and c['to'][1] > e['from'][1] + EPS]
        if not neighbors:
            raise ValueError(f'Mule Kick fin has no adjoining cabinet: {name}')
        if name.startswith('left_'):
            e['to'][0] = max(e['to'][0], max(c['from'][0] for c in neighbors) + .02)
        else:
            e['from'][0] = min(e['from'][0], min(c['to'][0] for c in neighbors) - .02)


def pack_texture(image, rects, limit=TEXTURE_LIMIT, crop=True):
    """Fit a texture to power-of-two dimensions around the texels a model uses.

    `rects` are the source faces' UV rectangles. Unused texels take the colour
    of the nearest used ones, so enclosing slabs and mipmaps never sample the
    blank background around the artwork. Returns the image and the UV mapping
    (scale_u, offset_u, scale_v, offset_v) into it.
    """
    image = image.convert('RGBA')
    width, height = image.size
    box = (0, 0, width, height)
    if crop:
        pixels = np.array(image, float)
        used = np.zeros((height, width), bool)
        for u0, v0, u1, v1 in rects:
            x0, x1 = sorted((u0 / 16 * width, u1 / 16 * width))
            y0, y1 = sorted((v0 / 16 * height, v1 / 16 * height))
            used[max(0, math.floor(y0)):math.ceil(y1), max(0, math.floor(x0)):math.ceil(x1)] = True
        ys, xs = np.nonzero(used)
        margin = 24
        box = (max(0, xs.min() - margin), max(0, ys.min() - margin),
               min(width, xs.max() + 1 + margin), min(height, ys.max() + 1 + margin))
        pixels = pixels[box[1]:box[3], box[0]:box[2]]
        used = used[box[1]:box[3], box[0]:box[2]]
        source = pixels.copy()
        traced = used.copy()
        pixels[~used] = 0
        for _ in range(4 * margin):
            if used.all():
                break
            total = np.zeros_like(pixels)
            count = np.zeros(used.shape)
            padded = np.pad(pixels, ((1, 1), (1, 1), (0, 0)))
            known = np.pad(used, 1)
            for dy in range(3):
                for dx in range(3):
                    total += padded[dy:dy + used.shape[0], dx:dx + used.shape[1]]
                    count += known[dy:dy + used.shape[0], dx:dx + used.shape[1]]
            grown = ~used & (count > 0)
            pixels[grown] = total[grown] / count[grown][:, None]
            used |= grown
        pixels[~used] = source[~used]
        pixels[~traced, 3] = 255
        image = Image.fromarray(pixels.round().astype(np.uint8))
    size = tuple(min(limit, 1 << max(4, math.ceil(math.log2(value)))) for value in image.size)
    if size != image.size:
        image = image.resize(size, Image.LANCZOS)
    if image.getchannel('A').getextrema()[0] == 255:
        image = image.convert('RGB')
    return image, (width / (box[2] - box[0]), -16 * box[0] / (box[2] - box[0]),
                   height / (box[3] - box[1]), -16 * box[1] / (box[3] - box[1]))


def optimize(model, names, assets, art=('#1',)):
    before = (len(model['elements']), sum(len(e['faces']) for e in model['elements']))
    level_bottoms(model['elements'], names)
    connect_mule_kick_fins(model['elements'], names)
    model['elements'] = simplify(model['elements'], names, art)
    mirror(model['elements'])
    overlap(model['elements'])
    cull(model, assets)
    after = (len(model['elements']), sum(len(e['faces']) for e in model['elements']))
    return before, after
