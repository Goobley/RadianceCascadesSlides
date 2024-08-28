from manim import *
import manim as mn
from manim_slides import Slide
import numpy as np
from RadianceIntervals import *

class RcProbeNear(ProbeView):
    near_length = 1.8
    far_length = 3.5
    is_rc_probe = True
    is_first_show = False
    overdraw_annulus = True