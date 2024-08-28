import manim as mn
from manim import *
from manim_slides import Slide
import numpy as np

mn.config.background_color = "#111111"

PROBE0_LENGTH = 0.25
PROBE0_NUM_RAYS = 4
PROBE0_SPACING = 1
MAX_LEVEL = 3
LEVEL_COLOURS = [mn.BLUE, mn.GOLD, mn.GREEN, mn.RED, mn.PURPLE]
X_PROBE0 = 8
X_OFFSET = -4
Y_PROBE0 = 8
Y_OFFSET = -4
BRANCHING = 1

class ProbeGrid(Slide):
    def construct(self):
        x_centres = (np.arange(X_PROBE0) + 0.5) * PROBE0_SPACING + X_OFFSET
        y_centres = (np.arange(Y_PROBE0) + 0.5) * PROBE0_SPACING + Y_OFFSET
        start_radius = 0.0
        for level in range(MAX_LEVEL+1):
            level_set = []
            spacing = PROBE0_SPACING * (1 << level)
            radius = PROBE0_LENGTH * (1 << (level * BRANCHING))
            num_rays = PROBE0_NUM_RAYS * (1 << (level * BRANCHING))
            nx = X_PROBE0 / (1 << level)
            ny = Y_PROBE0 / (1 << level)
            x_centres = (np.arange(nx) + 0.5) * spacing + X_OFFSET
            y_centres = (np.arange(ny) + 0.5) * spacing + Y_OFFSET
            for x in x_centres:
                for y in y_centres:
                    for ray_idx in range(num_rays):
                        angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
                        cos = np.cos(angle)
                        sin = np.sin(angle)
                        seg = mn.Line([x + start_radius * cos, y + start_radius * sin, 0], [x + radius * cos, y + radius * sin, 0], color=LEVEL_COLOURS[level])
                        level_set.append(seg)

            cascade = mn.VGroup(*level_set)
            self.play(mn.Write(cascade))
            self.next_slide()
            start_radius = radius