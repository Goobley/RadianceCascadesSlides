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
            self.play(mn.Write(cascade), run_time=0.75)
            if level < 2:
                self.next_slide()
            else:
                self.wait(0.5)
            start_radius = radius
        self.next_slide()

        # NOTE(cmo): Highlight one interval
        highlight_path = [0, 0, 1, 3]
        highlit_segs = []
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

            path = mn.VMobject(color=mn.BLUE_A)

            if level > 0:
                prev_num_rays = PROBE0_NUM_RAYS * (1 << ((level - 1) * BRANCHING))
                parent_idx = highlight_path[level - 1]
                parent_angle = 2.0 * np.pi / prev_num_rays * (parent_idx + 0.5)
                pcos = np.cos(parent_angle)
                psin = np.sin(parent_angle)
                p_frac = 0.98
                path.set_points_as_corners([
                    [p_frac * start_radius * pcos, p_frac * start_radius * psin, 0.0],
                    [start_radius * pcos, start_radius * psin, 0.0],
                    [start_radius * cos, start_radius * sin, 0.0],
                    [radius * cos, radius * sin, 0.0],
                ])
            else:
                path = mn.Line([0.0, 0.0, 0.0], [radius * cos, radius * sin, 0.0], color=mn.BLUE_A)

            self.play(mn.Write(path), run_time=0.5)
            highlit_segs.append(path)
            self.wait(0.25)

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

            paths = []
            path = mn.VMobject(color=mn.BLUE_A)

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
                    p_frac = 0.98
                    path = mn.VMobject(color=mn.BLUE_A)

                    path = mn.VMobject(color=mn.BLUE_A)
                    path.set_points_as_corners([
                        [p_frac * start_radius * pcos, p_frac * start_radius * psin, 0.0],
                        [start_radius * pcos, start_radius * psin, 0.0],
                        [start_radius * cos, start_radius * sin, 0.0],
                        [radius * cos, radius * sin, 0.0],
                    ])
                    path.joint_type = mn.LineJointType.BEVEL
                    paths.append(path)
            else:
                angle = 2.0 * np.pi / num_rays * (0 + 0.5)
                cos = np.cos(angle)
                sin = np.sin(angle)
                path = mn.Line([0.0, 0.0, 0.0], [radius * cos, radius * sin, 0.0], color=mn.BLUE_A)
                paths.append(path)

            self.play(*[mn.Write(path) for path in paths], run_time=0.5)
            self.wait(0.5)

        self.next_slide()
