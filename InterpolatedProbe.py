from manim import *
import manim as mn
from manim_slides import Slide
import numpy as np

mn.config.background_color = "#111111"

PROBE0_LENGTH = 0.5
PROBE0_NUM_RAYS = 4
MAX_LEVEL = 3
LEVEL_COLOURS = [mn.BLUE, mn.GOLD, mn.GREEN, mn.RED, mn.PURPLE]
BRANCHING = 1

class InterpolatedProbe(Slide):
    def construct(self):
        # NOTE(cmo): Draw intervals
        start_radius = 0.0
        for level in range(MAX_LEVEL+1):
            level_set = []
            radius = PROBE0_LENGTH * (1 << (level * BRANCHING))
            num_rays = PROBE0_NUM_RAYS * (1 << (level * BRANCHING))

            for ray_idx in range(num_rays):
                angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
                cos = np.cos(angle)
                sin = np.sin(angle)
                seg = mn.Line([start_radius * cos, start_radius * sin, 0], [radius * cos, radius * sin, 0], color=LEVEL_COLOURS[level])
                level_set.append(seg)

            cascade = mn.VGroup(*level_set)
            self.play(mn.Write(cascade))
            self.next_slide()
            start_radius = radius

        # NOTE(cmo): Highlight one interval
        highlight_path = [0, 0, 1, 3]
        highlit_segs = []
        end_coord = None
        for level in range(len(highlight_path)):
            radius = PROBE0_LENGTH * (1 << (level * BRANCHING))
            start_radius = 0.0
            if level != 0:
                start_radius = PROBE0_LENGTH * (1 << ((level - 1) * BRANCHING))
            num_rays = PROBE0_NUM_RAYS * (1 << (level * BRANCHING))
            ray_idx = highlight_path[level]
            angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
            cos = np.cos(angle)
            sin = np.sin(angle)

            to_draw = []
            seg = mn.Line([start_radius * cos, start_radius * sin, 0], [radius * cos, radius * sin, 0], color=mn.BLUE_A)
            seg.set_cap_style(mn.CapStyleType.ROUND)
            if end_coord is not None:
                connector = mn.Line(end_coord, [start_radius * cos, start_radius * sin, 0], color=mn.BLUE_A)
                connector.set_cap_style(mn.CapStyleType.ROUND)
                to_draw.append(connector)
            end_coord = [radius * cos, radius * sin, 0]
            to_draw.append(seg)
            self.play(*[mn.Write(x) for x in to_draw])
            highlit_segs += to_draw
            self.wait()

        self.next_slide()

        # NOTE(cmo): Remove highlight
        self.play(*[mn.Uncreate(x) for x in highlit_segs])
        self.wait()
        # NOTE(cmo): Highlight quadrant
        for level in range(MAX_LEVEL+1):
            radius = PROBE0_LENGTH * (1 << (level * BRANCHING))
            start_radius = 0.0
            if level != 0:
                start_radius = PROBE0_LENGTH * (1 << ((level - 1) * BRANCHING))
            num_rays = PROBE0_NUM_RAYS * (1 << (level * BRANCHING))

            max_ray = int(num_rays // 4)

            connectors = []
            if level > 0:
                prev_num_rays = PROBE0_NUM_RAYS * (1 << ((level - 1) * BRANCHING))
                for ray_idx in range(max_ray):
                    parent_idx = int(ray_idx // (2 * BRANCHING))
                    parent_angle = 2.0 * np.pi / prev_num_rays * (parent_idx + 0.5)
                    pcos = np.cos(parent_angle)
                    psin = np.sin(parent_angle)
                    angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    conn = mn.Line([start_radius * pcos, start_radius * psin, 0], [start_radius * cos, start_radius * sin, 0], color=mn.BLUE_A)
                    conn.set_cap_style(mn.CapStyleType.ROUND)
                    connectors.append(conn)

            segs = []
            for ray_idx in range(max_ray):
                angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
                cos = np.cos(angle)
                sin = np.sin(angle)
                seg = mn.Line([start_radius * cos, start_radius * sin, 0], [radius * cos, radius * sin, 0], color=mn.BLUE_A)
                seg.set_cap_style(mn.CapStyleType.ROUND)
                segs.append(seg)
            if len(connectors):
                self.play(*[mn.Write(x) for x in connectors])
            self.play(*[mn.Write(x) for x in segs])
            self.wait()

        self.next_slide()

