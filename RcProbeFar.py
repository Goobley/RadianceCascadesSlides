from manim import *
import manim as mn
from manim_slides import Slide
import numpy as np
from RadianceIntervals import *

class RcProbeFar(ProbeView):
    near_length = 3.5
    far_length = 7
    is_rc_probe = True
    is_first_show = False
    overdraw_annulus = True