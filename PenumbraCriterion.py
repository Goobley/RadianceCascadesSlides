from manim import *
import manim as mn
from manim_slides import Slide
import numpy as np

LEFT_EDGE = -4.0
RIGHT_EDGE = 4.0
IM_RES = 1200

class PenumbraCriterion(Slide):
    def construct(self):
        light_a = np.array([LEFT_EDGE * 0.4, 3.9, 0.0])
        light_b = np.array([RIGHT_EDGE * 0.4, 3.9, 0.0])
        blocker_y = 2.0
        blocker_a = np.array([LEFT_EDGE, blocker_y, 0.0])
        blocker_b = np.array([0.0, blocker_y, 0.0])
        light_colour = mn.PURPLE_A
        gamma = 2.8
        a_plane_y = 1.0
        b_plane_y = -2.0

        light_source = mn.Line(light_a, light_b, color=light_colour)
        self.play(mn.Create(light_source))

        x_grid = np.linspace(LEFT_EDGE, RIGHT_EDGE, IM_RES+1)
        x_grid = 0.5 * (x_grid[1:] + x_grid[:-1])
        y_grid = np.linspace(LEFT_EDGE, RIGHT_EDGE, IM_RES+1)
        y_grid = 0.5 * (y_grid[1:] + y_grid[:-1])[::-1]
        xx, yy = np.meshgrid(x_grid, y_grid)
        coords = np.stack((xx, yy), axis=-1)
        im = np.zeros((IM_RES, IM_RES))
        vec_a = light_a[:-1][None, None, :] - coords
        vec_b = light_b[:-1][None, None, :] - coords
        norm_a = np.sqrt(np.sum(vec_a**2, axis=-1))
        norm_b = np.sqrt(np.sum(vec_b**2, axis=-1))
        a_dot_b = vec_a[:, :, 0] * vec_b[:, :, 0] + vec_a[:, :, 1] * vec_b[:, :, 1]
        ang_size = np.arccos(a_dot_b / (norm_a * norm_b))
        ang_size **= (1.0 / gamma)
        ang_size = ang_size[:, :, None] * mn.hex_to_rgb(light_colour)[None, None, :]
        ang_size /= ang_size.max()
        ang_size *= 255
        ang_size = ang_size.astype(np.uint8)

        img = mn.ImageMobject(ang_size)
        img.height = 8
        self.play(mn.FadeIn(img))
        self.next_slide()

        self.play(mn.FadeOut(img))
        blocker = mn.Line(blocker_a, blocker_b, color=mn.GREY_D)
        blocker.z_index = 10
        self.play(mn.Create(blocker))
        a_dot_horiz = vec_a[:, :, 0]
        b_dot_horiz = vec_b[:, :, 0]
        illum_a_theta = np.arccos(a_dot_horiz / norm_a)
        illum_b_theta = np.arccos(b_dot_horiz / norm_b)
        illum_theta_start = np.minimum(illum_a_theta, illum_b_theta)
        illum_theta_end = np.maximum(illum_a_theta, illum_b_theta)

        vec_bl_a = blocker_a[:-1][None, None, :] - coords
        vec_bl_b = blocker_b[:-1][None, None, :] - coords
        norm_bl_a = np.sqrt(np.sum(vec_bl_a**2, axis=-1))
        norm_bl_b = np.sqrt(np.sum(vec_bl_b**2, axis=-1))
        bl_a_dot_horiz = vec_bl_a[:, :, 0]
        bl_b_dot_horiz = vec_bl_b[:, :, 0]
        bl_a_theta = np.arccos(bl_a_dot_horiz / norm_bl_a)
        bl_b_theta = np.arccos(bl_b_dot_horiz / norm_bl_b)
        bl_theta_start = np.minimum(bl_a_theta, bl_b_theta)
        bl_theta_end = np.maximum(bl_a_theta, bl_b_theta)

        full_illum = np.arccos(a_dot_b / (norm_a * norm_b))
        blocked_ang = np.minimum(illum_theta_end, bl_theta_end) - np.maximum(illum_theta_start, bl_theta_start)
        blocked_ang[blocked_ang < 0.0] = 0.0
        blocked_ang[yy > blocker_y] = 0.0
        blocked_illum = full_illum - blocked_ang
        blocked_illum[blocked_illum < 0.0] = 0.0
        blocked_illum **= (1.0 / gamma)
        blocked_illum = blocked_illum[:, :, None] * mn.hex_to_rgb(light_colour)[None, None, :]
        blocked_illum /= blocked_illum.max()
        blocked_illum *= 255
        blocked_illum = blocked_illum.astype(np.uint8)

        img_blocked = mn.ImageMobject(blocked_illum)
        img_blocked.height = 8
        self.play(mn.FadeIn(img_blocked))
        self.next_slide()

        d1 = (blocker_b - light_a) / np.linalg.norm(blocker_b - light_a)
        d2 = (blocker_b - light_b) / np.linalg.norm(blocker_b - light_b)
        t1_max = (RIGHT_EDGE - light_a[0]) / d1[0]
        t2_max = (LEFT_EDGE - light_b[0]) / d2[0]

        boundaries = [
            mn.DashedLine(light_a, light_a + t1_max * d1, color=mn.GREY_C, dash_length=0.1),
            mn.DashedLine(light_b, light_b + t2_max * d2, color=mn.GREY_C, dash_length=0.1),
        ]
        self.play(mn.Write(b) for b in boundaries)

        t1a = (a_plane_y - light_a[1]) / d1[1]
        t2a = (a_plane_y - light_b[1]) / d2[1]
        start_a = light_a + t1a * d1
        end_a = light_b + t2a * d2

        to_add = [
            mn.Line(start_a, end_a),
            mn.Dot(start_a),
            mn.Dot(end_a),
        ]
        for x in to_add[1:]:
            x.z_index = 10
        to_add.append(mn.MathTex("A").scale(0.8).move_to(to_add[0].get_center() + 2 * mn.DOWN * mn.SMALL_BUFF))
        self.play(mn.Write(x) for x in to_add)

        t1b = (b_plane_y - light_a[1]) / d1[1]
        t2b = (b_plane_y - light_b[1]) / d2[1]
        start_b = light_a + t1b * d1
        end_b = light_b + t2b * d2

        to_add = [
            mn.Line(start_b, end_b),
            mn.Dot(start_b),
            mn.Dot(end_b),
        ]
        for x in to_add[1:]:
            x.z_index = 10
        to_add.append(mn.MathTex("B").scale(0.8).move_to(to_add[0].get_center() + 2 * mn.DOWN * mn.SMALL_BUFF))
        self.play(mn.Write(x) for x in to_add)

        self.next_slide()

        alpha_colour = mn.TEAL
        elbow = mn.VMobject(color=alpha_colour)
        elbow.set_points_as_corners([light_a, start_a, light_b])
        l1 = mn.Line(start_a, light_a)
        l2 = mn.Line(start_a, light_b)
        angle = mn.Angle(l2, l1, radius=0.5, color=alpha_colour)
        angle_label = mn.MathTex(r"\alpha").scale(0.8).move_to(
            mn.Angle(
                l2, l1, radius=0.5 + 3 * SMALL_BUFF
            ).point_from_proportion(0.5)
        )
        to_add = [elbow, angle]
        self.play(mn.Write(x) for x in to_add)
        self.play(mn.Write(angle_label))

        beta_colour = mn.MAROON
        elbow = mn.VMobject(color=beta_colour)
        elbow.set_points_as_corners([light_a, start_b, light_b])
        l1 = mn.Line(start_b, light_a)
        l2 = mn.Line(start_b, light_b)
        angle = mn.Angle(l2, l1, radius=0.8, color=beta_colour)
        angle_label = mn.MathTex(r"\beta").scale(0.8).move_to(
            mn.Angle(
                l2, l1, radius=0.8 + 3 * SMALL_BUFF
            ).point_from_proportion(0.5)
        )
        to_add = [mn.DashedVMobject(elbow, num_dashes=55), angle]
        self.play(mn.ChangeSpeed(mn.Write(to_add[0]), speedinfo={0.0: 2, 1.0: 2}), mn.Write(angle))
        self.play(mn.Write(angle_label))
        self.next_slide()
