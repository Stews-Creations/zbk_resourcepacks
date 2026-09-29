"""Geometry, artwork and texture safety regressions; run directly with Python."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from optimize_core_machines import (ART_UV_TOLERANCE, CONTOUR_TOLERANCE, DIRECTIONS, ORB_LEVELS,
                                    SEAM_OVERLAP, connect_mule_kick_fins, covered, cull, level_bottoms, mirror,
                                    overlap, pack_texture, simplify, slab)


def box(a, b, texture='#0'):
    return {'from': list(a), 'to': list(b), 'shade': False,
            'faces': {d: {'texture': texture, 'uv': [0, 0, 16, 16]} for d in DIRECTIONS}}


def projected(a, b):
    """A slice whose front artwork follows u = x, v = 16 - y."""
    e = box(a, b)
    e['faces']['north'] = {'texture': '#1', 'uv': [a[0], 16 - b[1], b[0], 16 - a[1]]}
    return e


class OptimizationTests(unittest.TestCase):
    def run_cull(self, elements):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)/'assets/zbk'
            (assets/'textures').mkdir(parents=True)
            Image.new('RGBA', (16,16), (255,255,255,255)).save(assets/'textures/solid.png')
            Image.new('RGBA', (16,16), (255,255,255,0)).save(assets/'textures/clear.png')
            model = {'textures': {'0':'zbk:solid', '1':'zbk:clear'}, 'elements':elements}
            cull(model, assets)
            return model['elements']

    def test_union_and_gap(self):
        self.assertTrue(covered((0,0,2,2), [(0,0,1,2), (1,0,2,2)]))
        self.assertFalse(covered((0,0,2,2), [(0,0,.99,2), (1,0,2,2)]))

    def test_shared_faces_only(self):
        result = self.run_cull([box((0,0,0),(1,1,1)), box((1,0,0),(2,1,1))])
        self.assertEqual(sum(len(e['faces']) for e in result), 10)
        self.assertNotIn('east', result[0]['faces'])
        self.assertNotIn('west', result[1]['faces'])

    def test_partial_face_remains(self):
        result = self.run_cull([box((0,0,0),(1,1,1)), box((1,0,0),(2,.5,1))])
        self.assertIn('east', result[0]['faces'])

    def test_transparent_and_rotated_do_not_occlude(self):
        for blocker in (box((1,0,0),(2,1,1),'#1'), box((1,0,0),(2,1,1))):
            if blocker['faces']['west']['texture'] == '#0':
                blocker['rotation'] = {'axis':'y','angle':45,'origin':[1,0,0]}
            result = self.run_cull([box((0,0,0),(1,1,1)),blocker])
            self.assertIn('east', result[0]['faces'])

    def test_buried_element_removed(self):
        result = self.run_cull([box((0,0,0),(3,3,3)), box((1,1,1),(2,2,2))])
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]['faces']), 6)

    def test_contour_slabs_enclose_source_and_keep_shading(self):
        elements = [projected((2-.002*i,i*.02,1),(9+.002*i,(i+1)*.02,5)) for i in range(200)]
        result = simplify(deepcopy(elements), [f'hood_{i}' for i in range(200)])
        self.assertLess(len(result), len(elements) / 20)
        self.assertTrue(all(e['shade'] is False for e in result))
        for source in elements:
            self.assertTrue(any(all(e['from'][a] <= source['from'][a] and
                                    e['to'][a] >= source['to'][a] for a in range(3)) for e in result))
        for e in result:
            self.assertLessEqual(max(s['to'][0] for s in elements if e['from'][1] <= s['from'][1] < e['to'][1])
                                 - min(s['to'][0] for s in elements if e['from'][1] <= s['from'][1] < e['to'][1]),
                                 CONTOUR_TOLERANCE + 1e-6)

    def test_artwork_follows_its_projection(self):
        elements = [projected((2-.002*i,i*.02,1),(9+.002*i,(i+1)*.02,5)) for i in range(200)]
        for e in simplify(deepcopy(elements), [f'hood_{i}' for i in range(200)]):
            u0, v0, u1, v1 = e['faces']['north']['uv']
            for actual, expected in ((u0,e['from'][0]), (u1,e['to'][0]), (v0,16-e['to'][1]), (v1,16-e['from'][1])):
                self.assertAlmostEqual(actual, expected, delta=ART_UV_TOLERANCE)

    def test_shifted_artwork_cannot_merge(self):
        es = [projected((0,0,0),(4,1,1)), projected((0,1,0),(4,2,1))]
        self.assertIsNotNone(slab(es, 1))
        es[1]['faces']['north']['uv'][0] += .5
        self.assertIsNone(slab(es, 1))
        self.assertEqual(simplify(deepcopy(es), ['sign_0','sign_1']), es)

    def test_hardware_preserved(self):
        elements = [box((0,i,0),(1,i+.5,1)) for i in range(40)]
        self.assertEqual(simplify(deepcopy(elements), [f'bolt_{i}' for i in range(40)]), elements)

    def test_rotated_parts_preserved(self):
        elements = [box((0,i,0),(1,i+1,1)) for i in range(4)]
        for e in elements:
            e['rotation'] = {'axis':'y','angle':22.5,'origin':[0,0,0]}
        self.assertEqual(simplify(deepcopy(elements), [f'ring_{i}' for i in range(4)]), elements)

    def test_interleaved_chains_merge_separately(self):
        elements, names = [], []
        for i in range(10):
            for knob, x in enumerate((0, 3)):
                elements.append(box((x,i*.1,0),(x+1,(i+1)*.1,1)))
                names.append(f'knob_{knob*10+i}')
        result = simplify(deepcopy(elements), names)
        self.assertEqual(sorted((e['from'], e['to']) for e in result),
                         [([0,0,0],[1,1.0,1]), ([3,0,0],[4,1.0,1])])

    def test_side_fins_connect_across_tapered_shell(self):
        es = [box((1,0,3),(9,1,12)), box((2,1,3),(8,2,12)),
              box((0,0,4),(.8,2,11)), box((9.2,0,4),(10,2,11))]
        original = deepcopy(es)
        connect_mule_kick_fins(es, ['green_cabinet_0','green_cabinet_1',
                                   'left_side_fin_0','right_side_fin_0'])
        self.assertEqual(es[2]['to'][0], 2.02)
        self.assertEqual(es[3]['from'][0], 7.98)
        self.assertEqual(len(es), len(original))
        self.assertEqual(es[2]['from'], original[2]['from'])
        self.assertEqual(es[3]['to'], original[3]['to'])
        for e, before in zip(es, original):
            self.assertEqual(e['faces'], before['faces'])
            for k in ('from','to'):
                self.assertEqual(e[k][1:], before[k][1:])

    def test_mirror_puts_artwork_on_its_traced_side(self):
        # Traced at the image's left edge: low X and low U in the authoring model.
        panel = projected((1,0,0),(3,2,1))
        panel['faces']['east']['uv'] = [1,2,3,4]
        panel['faces']['west']['uv'] = [5,6,7,8]
        panel['faces']['up']['uv'] = [1,0,3,1]
        original = deepcopy(panel)
        mirror([panel])
        # Minecraft shows a north face's first U at high X, the viewer's left.
        self.assertEqual((panel['from'][0], panel['to'][0]), (13, 15))
        self.assertEqual(panel['faces']['north'], original['faces']['north'])
        self.assertEqual(panel['faces']['east'], original['faces']['west'])
        self.assertEqual(panel['faces']['west'], original['faces']['east'])
        self.assertEqual(panel['faces']['up']['uv'], [3,0,1,1])
        self.assertEqual(panel['from'][1:], original['from'][1:])

    def test_mirror_reverses_rotation(self):
        for axis, angle in (('x',22.5), ('y',-22.5), ('z',-45)):
            e = box((1,0,0),(3,2,1))
            e['rotation'] = {'axis':axis,'angle':45 if axis == 'z' else 22.5,'origin':[2,1,0]}
            mirror([e])
            self.assertEqual(e['rotation'], {'axis':axis,'angle':angle,'origin':[14,1,0]})

    def test_overlap_joins_seams_without_moving_artwork(self):
        es = [projected((2,1,0),(6,2,1)), projected((3,2,0),(5,3,1))]
        overlap(es)
        self.assertGreater(es[0]['to'][1], es[1]['from'][1])
        for e in es:
            u0, v0, u1, v1 = e['faces']['north']['uv']
            self.assertAlmostEqual(u0, e['from'][0])
            self.assertAlmostEqual(u1, e['to'][0])
            self.assertAlmostEqual(v0, 16 - e['to'][1])
            self.assertAlmostEqual(v1, 16 - e['from'][1])
        self.assertAlmostEqual(es[0]['to'][1], 2 + SEAM_OVERLAP)
        result = self.run_cull([box((0,0,0),(1,1,1)), box((1,0,0),(2,1,1))])
        overlap(result)
        self.assertEqual(sum(len(e['faces']) for e in result), 10)

    def orb(self):
        elements, names = [], []
        for y in range(96):
            for x in range(96):
                q = (x-47.5)**2 + (y-47.5)**2
                if q >= 48**2:
                    continue
                depth = (48**2 - q)**.5 / 12
                e = box((4+x/12,4+y/12,8-depth), (4+(x+1)/12,4+(y+1)/12,8+depth), '#1')
                for face in e['faces'].values():
                    face['uv'] = [x/6,16-(y+1)/6,(x+1)/6,16-y/6]
                elements.append(e)
                names.append(f'orb_shell_{x}_{y}')
        return elements, names

    def test_orb_budget_extent_and_artwork(self):
        elements, names = self.orb()
        result = simplify(deepcopy(elements), names)
        self.assertLessEqual(len(result), 80)
        self.assertTrue(all(e['shade'] is False for e in result))
        self.assertEqual(len({e['from'][2] for e in result}), ORB_LEVELS)
        for axis in (0,1,2):
            self.assertAlmostEqual(min(e['from'][axis] for e in result), min(e['from'][axis] for e in elements), places=2)
            self.assertAlmostEqual(max(e['to'][axis] for e in result), max(e['to'][axis] for e in elements), places=2)
        for e in result:
            # Every cuboid shares the orb's centre and stays near its surface.
            for axis, centre in enumerate((8,8,8)):
                self.assertAlmostEqual((e['from'][axis]+e['to'][axis])/2, centre)
            corner = sum((e['to'][axis]-centre)**2 for axis, centre in enumerate((8,8,8)))**.5
            self.assertLess(abs(corner-4), .5)
            u0, v0, u1, v1 = e['faces']['north']['uv']
            self.assertAlmostEqual(u0, (e['from'][0]-4)*2, delta=ART_UV_TOLERANCE)
            self.assertAlmostEqual(v1, 16-(e['from'][1]-4)*2, delta=ART_UV_TOLERANCE)
            for face in e['faces'].values():
                self.assertTrue(all(0 <= value <= 16 for value in face['uv']))
        for e in result:
            self.assertFalse(any(o is not e and all(o['from'][a] <= e['from'][a] and o['to'][a] >= e['to'][a]
                                                    for a in range(3)) for o in result))

    def test_columns_that_are_not_a_sphere_stay_stacked(self):
        elements, names = self.orb()
        for e in elements:
            e['from'][2], e['to'][2] = 7, 9
        self.assertTrue(all(e['from'][2] == 7 for e in simplify(deepcopy(elements), names)))

    def test_partial_bottom_slice_is_widened(self):
        es = [projected((5,1,0),(9,1.2,1)), projected((2,1.2,0),(10,1.4,1)), projected((2.1,1.4,0),(9.9,1.6,1))]
        level_bottoms(es, ['base_2','base_1','base_0'])
        self.assertEqual((es[0]['from'][0], es[0]['to'][0]), (2, 10))
        self.assertAlmostEqual(es[0]['faces']['north']['uv'][0], 2)
        self.assertAlmostEqual(es[0]['faces']['north']['uv'][2], 10)
        self.assertEqual((es[1]['from'][0], es[2]['from'][0]), (2, 2.1))

    def test_rounded_bottom_and_separate_parts_are_kept(self):
        es = [projected((2.5,1,0),(9.5,1.2,1)), projected((2,1.2,0),(10,1.4,1)),
              projected((12,1,0),(13,1.2,1)), projected((12,1.2,0),(13,1.4,1))]
        original = deepcopy(es)
        level_bottoms(es, ['foot_0','foot_1','foot_2','foot_3'])
        self.assertEqual(es, original)

    def incline(self):
        steps = [projected((2+.01*i,4+.1*i,2+.2*i),(10-.01*i,4.1+.1*i,12)) for i in range(20)]
        for e in steps:
            e['faces']['up'] = deepcopy(e['faces']['north'])
        badge = [projected((5,4.5+.1*i,2.5),(7,4.6+.1*i,2.8)) for i in range(5)]
        names = [f'sloping_control_deck_{i}' for i in range(20)] + [f'lid_badge_{i}' for i in range(5)]
        return steps, badge, names

    def test_incline_gains_smooth_covers_over_recessed_steps(self):
        steps, badge, names = self.incline()
        result = simplify(deepcopy(steps + badge), names)
        bodies = [e for e in result if not e.get('rotation')]
        covers = [e for e in result if e.get('rotation') and e['from'][0] < 5]
        self.assertEqual(len(covers), len(bodies))
        self.assertLess(len(bodies), len(steps))
        for body in bodies:
            self.assertNotIn('north', body['faces'])
            cover = next(e for e in covers if e['rotation']['origin'][1] == body['from'][1])
            self.assertAlmostEqual(cover['rotation']['angle'], -26.565, places=2)
            self.assertEqual(cover['rotation']['axis'], 'x')
            # The cover spans its steps along the incline and reaches below
            # their inner corners, so nothing shows beneath its edges.
            self.assertAlmostEqual(cover['to'][2]-cover['from'][2], (body['to'][1]-body['from'][1])*5**.5)
            self.assertGreater(cover['to'][1], body['from'][1])
            self.assertGreater(body['from'][1]-cover['from'][1], 2*(body['to'][1]-body['from'][1])/5**.5)
            self.assertEqual(set(cover['faces']), set(DIRECTIONS))
            self.assertEqual(body['from'][2], max(s['from'][2] for s in steps if body['from'][1] <= s['from'][1] < body['to'][1]))
            self.assertEqual((cover['from'][0], cover['to'][0]), (body['from'][0], body['to'][0]))
            self.assertAlmostEqual(cover['faces']['up']['uv'][1], 16-body['from'][1], delta=ART_UV_TOLERANCE)
            self.assertAlmostEqual(cover['faces']['up']['uv'][3], 16-body['to'][1], delta=ART_UV_TOLERANCE)

    def test_badge_lies_on_its_incline(self):
        steps, badge, names = self.incline()
        result = simplify(deepcopy(steps + badge), names)
        decals = [e for e in result if e.get('rotation') and e['from'][0] == 5]
        self.assertTrue(decals)
        self.assertFalse(any(e['from'][2] == 2.5 for e in result))
        for e in decals:
            self.assertAlmostEqual(e['rotation']['angle'], -26.565, places=2)
            self.assertEqual(e['to'][0], 7)
            self.assertEqual(e['faces']['up']['texture'], '#1')
            self.assertNotIn('down', e['faces'])
            self.assertGreater(e['to'][1], e['rotation']['origin'][1])

    def test_texture_fits_power_of_two_around_used_texels(self):
        image = Image.new('RGB', (1000,1500), (255,255,255))
        image.paste((200,30,30), (300,300,700,1200))
        rect = [300/1000*16, 300/1500*16, 700/1000*16, 1200/1500*16]
        packed, (su, ou, sv, ov) = pack_texture(image, [rect])
        self.assertEqual(packed.size, (512,1024))
        self.assertEqual(packed.mode, 'RGB')
        mapped = [rect[0]*su+ou, rect[1]*sv+ov, rect[2]*su+ou, rect[3]*sv+ov]
        self.assertTrue(all(0 < value < 16 for value in mapped))
        x, y = mapped[0]/16*packed.width, mapped[1]/16*packed.height
        self.assertEqual(packed.getpixel((int(x)+2, int(y)+2)), (200,30,30))
        # The blank margin takes the artwork's colour instead of showing white.
        self.assertEqual(packed.getpixel((int(x)-8, int(y)-8)), (200,30,30))

    def test_shared_atlas_keeps_its_layout(self):
        packed, mapping = pack_texture(Image.new('RGB', (1254,1254), (9,9,9)), [[1,1,2,2]], crop=False)
        self.assertEqual(packed.size, (1024,1024))
        self.assertEqual(mapping, (1,0,1,0))


if __name__ == '__main__':
    unittest.main()
