from manim import *
import manim as mn
from manim_slides import Slide
import numpy as np

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

class ProbeView(Slide):
    near_length = 0.0
    far_length = 20.0
    is_first_show = True
    is_rc_probe = False
    overdraw_annulus = False

    def update_canvas(self):
        self.counter += 1
        old_slide_number = self.canvas["slide_number"]
        new_slide_number = Text(f"{self.counter}").move_to(old_slide_number)
        self.play(Transform(old_slide_number, new_slide_number))

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

        self.next_slide()

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

class RcProbeFar(ProbeView):
    near_length = 3.5
    far_length = 7
    is_rc_probe = True
    is_first_show = False
    overdraw_annulus = True


# class RcPresentationTitle(Slide):
#     def construct(self):
#         title = mn.VGroup(
#             mn.Text("Towards the Next Generation"),
#             mn.Text("of Radiative Transfer Models:"),
#             mn.Text("Radiance Cascades", color=mn.TEAL).scale(0.8),
#         ).arrange(mn.DOWN).shift(mn.UP)
#         author = mn.VGroup(
#             mn.Text("Chris Osborne").scale(0.8),
#             mn.Text("University of Glasgow").scale(0.6),
#         ).arrange(mn.DOWN).next_to(title, 4 * mn.DOWN)
#         self.add(title)
#         self.add(author)
#         self.wait()

# %%manim_slides -v WARNING --progress_bar None RcPresentationTitle --manim-slides controls=true
# https://github.com/jeertmans/jeertmans.github.io/tree/main/_slides/2023-12-07-confirmation/main.py

class Item:
    def __init__(self, initial=1):
        self.value = initial

    def __repr__(self):
        s = repr(self.value)
        self.value += 1
        return s


def paragraph(*strs, alignment=LEFT, direction=DOWN, **kwargs):
    texts = VGroup(*[Text(s, **kwargs) for s in strs]).arrange(direction)

    if len(strs) > 1:
        for text in texts[1:]:
            text.align_to(texts[0], direction=alignment)

    return texts

class RcPresentationTitle(Slide):

    def next_slide_title_anim(self, title):
        return Transform(
            self.slide_title,
            Text(title, color=mn.WHITE, font_size=36)
            .move_to(self.slide_title)
            .align_to(self.slide_title, mn.LEFT),
        )

    # Slides new slide and contents in
    def new_slide(self, title, contents=None):
        if self.mobjects_without_canvas:
            self.play(
                self.next_slide_title_anim(title),
                self.wipe(
                    self.mobjects_without_canvas,
                    contents if contents else [],
                    return_animation=True,
                ),
            )
        else:
            self.play(
                self.next_slide_title_anim(title),
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slide_title = mn.Text(
            "Contents", color=mn.WHITE, font_size=36
        ).to_corner(UL)
        self.add_to_canvas(slide_title=self.slide_title)

    def construct(self):
        title = mn.VGroup(
            mn.Text("Towards the Next Generation"),
            mn.Text("of Radiative Transfer Models:"),
            mn.Text("Radiance Cascades", color=mn.TEAL).scale(0.8),
        ).arrange(mn.DOWN).shift(mn.UP)
        author = mn.VGroup(
            mn.Text("Chris Osborne").scale(0.8),
            mn.Text("University of Glasgow").scale(0.6),
        ).arrange(mn.DOWN).next_to(title, 4 * mn.DOWN)
        self.add(title)
        self.add(author)
        self.wait()

        self.next_slide()
        i = Item()
        contents = paragraph(
            f"{i}. Where are we at?",
            f"{i}. What is wrong in RT?",
            f"{i}. How do we fix this?",
            f"{i}. Radiance Cascades",
            f"{i}. Applications",
            f"{i}. Conclusion",
            color=mn.WHITE,
            font_size=24,
        ).align_to(self.slide_title, LEFT)
        self.wipe(self.mobjects_without_canvas, [*self.canvas_mobjects, contents])

        next_bit = paragraph(
        "Some info",
        "But this isn't good enough",
        color=mn.WHITE,
        font_size=24
        )
        self.next_slide()
        self.new_slide("What's happening?", next_bit)