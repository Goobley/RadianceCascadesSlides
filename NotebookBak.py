TRI_POS = [1.05, 1.2 + np.sqrt(3) / 2 * 0.15, 0]
CIRC_POS = [1.0, 1.0, 0]
RECT_POS = [0.575, 1.075, 0]
MAIN_TRANS = [-2.8, 0.5, 0]
PROBE_CENTRE = [3.9, -1.6, 0]
PROBE_START_ANGLE = 60
PROBE_END_ANGLE = 200
PROBE_ANGLE_STEP = 0.1
PRIM_COLOURS = [mn.TEAL, mn.RED, mn.GOLD]
PROBE_RADIUS = 1.2

def compress_int_ranges(ints):
    if len(ints) == 0:
        return None

    start_idx = 0
    result = []
    while start_idx < len(ints):
        needle = ints[start_idx]
        idx = start_idx

        while idx < len(ints) and ints[idx] == needle:
            idx += 1

        result.append((needle, start_idx, idx))
        start_idx = idx

    return result

def convert_int_ranges(ranges):
    return list(map(lambda v: (
        v[0],
        v[1] * PROBE_ANGLE_STEP + PROBE_START_ANGLE,
        v[2] * PROBE_ANGLE_STEP + PROBE_START_ANGLE), ranges
    ))

class ProbeView(mn.Scene):
    near_length = 0.0
    far_length = 20.0
    is_first_show = True
    is_rc_probe = False
    overdraw_annulus = False

    def construct(self):
        circ = mn.Circle(radius=0.15, color=PRIM_COLOURS[0], fill_opacity=0.5).move_to(CIRC_POS)
        rect = mn.Rectangle(width=0.35, height=0.15, color=PRIM_COLOURS[1], fill_opacity=0.5).move_to(RECT_POS)
        tri = mn.Polygon([0.9, 1.2, 0], [1.2, 1.2, 0], [1.05, 1.2 + np.sqrt(3) / 2 * 0.3, 0], color=PRIM_COLOURS[2], fill_opacity=0.5).move_to(TRI_POS)

        prims = mn.VGroup(tri, circ, rect).scale(4).shift(MAIN_TRANS)
        probe = mn.Dot(PROBE_CENTRE).shift(MAIN_TRANS)
        probe.z_index = 2
        # self.play(mn.GrowFromCenter(probe))
        probe_outline = mn.DashedVMobject(
            mn.Circle(radius=PROBE_RADIUS, color=mn.LIGHT_GREY, stroke_width=2).move_to(probe.get_center()),
            dashed_ratio=0.4,
            num_dashes=40,
        )
        ann = mn.Annulus(inner_radius=self.near_length, outer_radius=self.far_length, fill_opacity=0.1, stroke_width=1).move_to(probe.get_center())
        if self.is_rc_probe and not self.overdraw_annulus:
            probe_group = mn.VGroup(probe, probe_outline, ann)
        else:
            probe_group = mn.VGroup(probe, probe_outline)


        if self.is_first_show:
            self.play(mn.GrowFromCenter(prims))
            self.play(mn.Write(probe_group))
        else:
            self.add(prims)
            self.add(probe_group)

        if self.overdraw_annulus:
            self.play(mn.Write(ann))

        self.wait()

        first_int = []
        for theta in np.linspace(
            PROBE_START_ANGLE,
            PROBE_END_ANGLE,
            num=(int((PROBE_END_ANGLE - PROBE_START_ANGLE) / PROBE_ANGLE_STEP) + 1)
        ):
            px, py, _ = probe.get_center()
            offset_size = 1e-3
            ray_start = [px + np.cos(np.deg2rad(theta)) * self.near_length - offset_size, py + np.sin(np.deg2rad(theta)) * self.near_length, 0]
            ray_start_off = [px + np.cos(np.deg2rad(theta)) * self.near_length + offset_size, py + np.sin(np.deg2rad(theta)) * self.near_length, 0]
            ray_end = [px + np.cos(np.deg2rad(theta)) * self.far_length - offset_size, py + np.sin(np.deg2rad(theta)) * self.far_length, 0]
            ray_end_off = [px + np.cos(np.deg2rad(theta)) * self.far_length + offset_size, py + np.sin(np.deg2rad(theta)) * self.far_length, 0]

            ray = mn.Polygon(ray_start, ray_start_off, ray_end_off, ray_end)
            # self.add(ray)
            intersections = [mn.Intersection(ray, p).has_points() for p in [circ, rect, tri]]
            if not any(intersections):
                int_idx = -1
            else:
                int_idx = intersections.index(True)
            first_int.append(int_idx)
        int_ranges = convert_int_ranges(compress_int_ranges(first_int))



        for int_idx, (p_idx, theta1, theta2) in enumerate(int_ranges):
            px, py, _ = probe.get_center()
            line1 = mn.Line(
                [px, py, 0],
                [px + np.cos(np.deg2rad(theta1)) * self.far_length, py + np.sin(np.deg2rad(theta1)) * self.far_length, 0],
                stroke_width=2,
                color=mn.LIGHT_GREY,
            )
            line2 = mn.Line(
                [px, py, 0],
                [px + np.cos(np.deg2rad(theta2)) * self.far_length, py + np.sin(np.deg2rad(theta2)) * self.far_length, 0],
                stroke_width=2,
                color=mn.LIGHT_GREY,
            )

            if theta1 != PROBE_START_ANGLE:
                self.play(mn.Write(line1))

            if p_idx == -1:
                continue

            inner_arc = mn.Angle(
                    line1,
                    line2,
                    color=PRIM_COLOURS[p_idx],
                    radius=PROBE_RADIUS,
                    stroke_width=8,
                )
            self.play(mn.Write(inner_arc))

        self.wait()

class LongCharView(ProbeView):
    near_length = 0.0
    far_length = 20.0

class RcProbeNear(ProbeView):
    near_length = 1.8
    far_length = 3.5
    is_rc_probe = True
    is_first_show = False
    overdraw_annulus = True

class RcProbeNear(ProbeView):
    near_length = 3.5
    far_length = 7
    is_rc_probe = True
    is_first_show = False
    overdraw_annulus = True

class InterpolatedProbes(mn.Scene):
    def construct(self):
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
            self.wait()
            start_radius = radius

        highlight_path = [0, 0, 1, 3]
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
            if end_coord is not None:
                connector = mn.Line(end_coord, [start_radius * cos, start_radius * sin, 0], color=mn.BLUE_A)
                to_draw.append(connector)
            end_coord = [radius * cos, radius * sin, 0]
            to_draw.append(seg)
            self.play(*[mn.Write(x) for x in to_draw])
            self.wait()

class InterpolatedProbes(mn.Scene):
    def construct(self):
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
            self.wait()
            start_radius = radius

        highlight_path = [0, 0, 1, 3]
        highlit_segs = []
        end_coord = None
        highlight_obj = mn.VMobject(color=mn.BLUE_A)
        highlight_obj.set_points_as_corners(np.array([[0,0,0], [0,0,0]]))
        prev_highlight = highlight_obj.copy()
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
            if level > 0:
                highlight_obj.add_line_to(np.array([start_radius * cos, start_radius * sin, 0]))
            highlight_obj.add_line_to(np.array([radius * cos, radius * sin, 0]))

            #self.play(mn.ReplacementTransform(prev_highlight, highlight_obj))
            self.add(highlight_obj)
            self.wait()



        #self.play(*[mn.Uncreate(x) for x in highlit_segs])
        #self.wait()

        # for level in range(MAX_LEVEL+1):
        #     radius = PROBE0_LENGTH * (1 << (level * BRANCHING))
        #     start_radius = 0.0
        #     if level != 0:
        #         start_radius = PROBE0_LENGTH * (1 << ((level - 1) * BRANCHING))
        #     num_rays = PROBE0_NUM_RAYS * (1 << (level * BRANCHING))

        #     max_ray = int(num_rays // 4)

        #     connectors = []
        #     if level > 0:
        #         prev_num_rays = PROBE0_NUM_RAYS * (1 << ((level - 1) * BRANCHING))
        #         for ray_idx in range(max_ray):
        #             parent_idx = int(ray_idx // (2 * BRANCHING))
        #             parent_angle = 2.0 * np.pi / prev_num_rays * (parent_idx + 0.5)
        #             pcos = np.cos(parent_angle)
        #             psin = np.sin(parent_angle)
        #             angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
        #             cos = np.cos(angle)
        #             sin = np.sin(angle)

        #             conn = mn.Line([start_radius * pcos, start_radius * psin, 0], [start_radius * cos, start_radius * sin, 0], color=mn.BLUE_A)
        #             connectors.append(conn)

        #     segs = []
        #     for ray_idx in range(max_ray):
        #         angle = 2.0 * np.pi / num_rays * (ray_idx + 0.5)
        #         cos = np.cos(angle)
        #         sin = np.sin(angle)
        #         seg = mn.Line([start_radius * cos, start_radius * sin, 0], [radius * cos, radius * sin, 0], color=mn.BLUE_A)
        #         segs.append(seg)
        #     if len(connectors):
        #         self.play(*[mn.Write(x) for x in connectors])
        #     self.play(*[mn.Write(x) for x in segs])
        #     self.wait()

