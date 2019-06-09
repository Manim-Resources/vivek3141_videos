from manimlib.constants import *

from manimlib.animation.animation import *
from manimlib.animation.composition import *
from manimlib.animation.creation import *
from manimlib.animation.fading import *
from manimlib.animation.growing import *
from manimlib.animation.indication import *
from manimlib.animation.movement import *
from manimlib.animation.numbers import *
from manimlib.animation.rotation import *
from manimlib.animation.specialized import *
from manimlib.animation.transform import *
from manimlib.animation.update import *

from manimlib.camera.camera import *
from manimlib.camera.mapping_camera import *
from manimlib.camera.moving_camera import *
from manimlib.camera.three_d_camera import *

from manimlib.mobject.coordinate_systems import *
from manimlib.mobject.changing import *
from manimlib.mobject.frame import *
from manimlib.mobject.functions import *
from manimlib.mobject.geometry import *
from manimlib.mobject.matrix import *
from manimlib.mobject.mobject import *
from manimlib.mobject.number_line import *
from manimlib.mobject.numbers import *
from manimlib.mobject.probability import *
from manimlib.mobject.shape_matchers import *
from manimlib.mobject.svg.brace import *
from manimlib.mobject.svg.drawings import *
from manimlib.mobject.svg.svg_mobject import *
from manimlib.mobject.svg.tex_mobject import *
from manimlib.mobject.three_d_utils import *
from manimlib.mobject.three_dimensions import *
from manimlib.mobject.types.image_mobject import *
from manimlib.mobject.types.point_cloud_mobject import *
from manimlib.mobject.types.vectorized_mobject import *
from manimlib.mobject.mobject_update_utils import *
from manimlib.mobject.value_tracker import *
from manimlib.mobject.vector_field import *

from manimlib.once_useful_constructs.arithmetic import *
from manimlib.once_useful_constructs.combinatorics import *
from manimlib.once_useful_constructs.complex_transformation_scene import *
from manimlib.once_useful_constructs.counting import *
from manimlib.once_useful_constructs.fractals import *
from manimlib.once_useful_constructs.graph_theory import *
from manimlib.once_useful_constructs.light import *

from manimlib.scene.graph_scene import *
from manimlib.scene.moving_camera_scene import *
from manimlib.scene.reconfigurable_scene import *
from manimlib.scene.scene import *
from manimlib.scene.sample_space_scene import *
from manimlib.scene.graph_scene import *
from manimlib.scene.scene_from_video import *
from manimlib.scene.three_d_scene import *
from manimlib.scene.vector_space_scene import *
from manimlib.scene.zoomed_scene import *

from manimlib.utils.bezier import *
from manimlib.utils.color import *
from manimlib.utils.config_ops import *
from manimlib.utils.images import *
from manimlib.utils.iterables import *
from manimlib.utils.file_ops import *
from manimlib.utils.paths import *
from manimlib.utils.rate_functions import *
from manimlib.utils.simple_functions import *
from manimlib.utils.sounds import *
from manimlib.utils.space_ops import *
from manimlib.utils.strings import *

# Non manim libraries that are also nice to have without thinking

import inspect
import itertools as it
import numpy as np
import operator as op
import os
import random
import re
import string
import sys
import math

from PIL import Image
from colour import Color


class Intro(Scene):
    def construct(self):
        eq = TexMobject(
            r"\int_C \vec{\text{F}} \bullet \text{d}\vec{\text{r}} = \iint_D \nabla \times \vec{\text{F}} \ \text{dA}")
        eq.scale(1)

        title = TextMobject("Line Integral")
        title.scale(1)
        title.to_edge(UP)
        rect = ScreenRectangle(height=4)
        rect.next_to(title, DOWN)

        title.shift(2 * DOWN)
        rect.shift(2 * DOWN)

        self.play(Write(eq))
        self.wait()

        self.play(ApplyMethod(eq.shift, 3 * UP))
        self.wait()

        self.play(
            FadeInFromDown(title),
            Write(rect)
        )
        self.wait()


class Setup(Scene):
    CONFIG = {
        "color_list": ['#e22b2b', '#e88e10', '#eae600', '#88ea00',
                       '#00eae2', '#0094ea', "#2700ea", '#bf00ea', '#ea0078'],
        "prop": 0
    }

    def construct(self):
        axes_config = {"x_min": -5,
                       "x_max": 5,
                       "y_min": -5,
                       "y_max": 5,
                       "z_axis_config": {},
                       "z_min": -1,
                       "z_max": 1,
                       "z_normal": DOWN,
                       "num_axis_pieces": 20,
                       "light_source": 9 * DOWN + 7 * LEFT + 10 * OUT,
                       "number_line_config": {
                           "include_tip": False,
                       },
                       }

        axes = Axes(**axes_config)
        f = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.vect, prop=0)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        field = VGroup(axes, f)
        # field.scale(0.6)

        axes2 = Axes(**axes_config)
        f2 = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.vect, prop=0).set_fill(opacity=0.5)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        field2 = VGroup(axes, f2)
        # field2.scale(0.6)

        c = ParametricFunction(
            self.func,
            t_min=-2,
            t_max=2,
        )
        c.set_stroke(opacity=0.75)
        label = TextMobject("C")
        label.shift(3 * LEFT)
        label.scale(2)

        s = ParametricSurface(
            self.surface,
            u_min=-2,
            u_max=2,
            v_min=-1,
            v_max=1,
            fill_color=BLUE,
            checkerboard_colors=[BLUE, BLUE],
            stroke_color=BLUE
        ).set_fill(opacity=0.5)

        r = TextMobject("R", color=BLUE)
        r.scale(1.5)
        r.shift(2 * RIGHT + 3.5 * UP)

        curve = VGroup(label, c)
        surface = VGroup(r, s)

        self.play(ShowCreation(field))
        self.wait()

        self.play(Write(curve))
        self.wait()

        self.play(Transform(field, field2))
        self.wait()

        self.play(Write(surface))
        self.wait()

    def calc_field_color(self, point, f, prop=0.0, opacity=None):
        x, y = point[:2]
        func = f(x, y)
        magnitude = math.sqrt(func[0] ** 2 + func[1] ** 2)
        func = func / magnitude if magnitude != 0 else np.array([0, 0])
        func = func / 1.5
        v = int(magnitude / 10 ** prop)
        index = len(self.color_list) - 1 if v > len(self.color_list) - 1 else v
        c = self.color_list[index]
        v = Vector(func, color=c).shift(point)
        if opacity:
            v.set_fill(opacity=opacity)
        return v

    @staticmethod
    def vect(x, y):
        return np.array([
            y,
            x,
            0
        ])

    @staticmethod
    def func(t):
        return np.array([
            1 - 2*t**2 + 2,
            t**3 - 4*t,
            0
        ])

    @staticmethod
    def surface(t, v):
        return np.array([
            1 - 2*t**2 + 2,
            v*(t**3 - 4*t),
            0
        ])


class GreenEquation(Scene):
    def construct(self):
        eq = TexMobject(
            r"\int_C \vec{\text{F}} \bullet \text{d}\vec{\text{r}} = \iint_D \nabla \times \vec{\text{F}} \ \text{dA}")
        eq.scale(1.5)
        self.play(Write(eq))
        self.wait()


class CurlDemo(Scene):
    CONFIG = {
        "color_list": ['#e22b2b', '#e88e10', '#eae600', '#88ea00',
                       '#00eae2', '#0094ea', "#2700ea", '#bf00ea', '#ea0078'],
        "prop": 0.1
    }

    def construct(self):
        axes_config = {"x_min": -5,
                       "x_max": 5,
                       "y_min": -5,
                       "y_max": 5,
                       "z_axis_config": {},
                       "z_min": -1,
                       "z_max": 1,
                       "z_normal": DOWN,
                       "num_axis_pieces": 20,
                       "light_source": 9 * DOWN + 7 * LEFT + 10 * OUT,
                       "number_line_config": {
                           "include_tip": False,
                       },
                       }

        axes = Axes(**axes_config)
        f1 = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.field1, prop=0)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )
        c = Circle(fill_color=RED, fill_opacity=0.25, color=WHITE, radius=1)
        field1 = VGroup(axes, f1, c)
        field1.scale(0.6)

        axes = Axes(**axes_config)
        f2 = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.field2, prop=0)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        c = Circle(fill_color=RED, fill_opacity=0.25, color=WHITE, radius=1)
        field2 = VGroup(axes, f2, c)
        field2.scale(0.6)

        axes = Axes(**axes_config)
        f3 = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.field3, prop=0)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        c = Circle(fill_color=RED, fill_opacity=0.25, color=WHITE, radius=1)
        field3 = VGroup(axes, f3, c)
        field3.scale(0.6)

        text1 = TexMobject(r"\text{curl}\textbf{F} > 0",
                           tex_to_color_map={">": YELLOW})
        text1.shift(3 * UP)

        text2 = TexMobject(r"\text{curl}\textbf{F} < 0",
                           tex_to_color_map={"<": YELLOW})
        text2.shift(3 * UP)

        self.play(Write(field1))
        self.wait()

        # self.play(Write(c))
        self.play(Write(text1))
        self.wait()

        self.play(
            Transform(field1, field2),
            Transform(text1, text2)
        )
        self.wait()

        self.play(
            Transform(field1, field3)
        )
        self.wait()

    def calc_field_color(self, point, f, prop=0.0, opacity=None):
        x, y = point[:2]
        func = f(x, y)
        magnitude = math.sqrt(func[0] ** 2 + func[1] ** 2)
        func = func / magnitude if magnitude != 0 else np.array([0, 0])
        func = func / 1.5
        v = int(magnitude / 10 ** prop)
        index = len(self.color_list) - 1 if v > len(self.color_list) - 1 else v
        c = self.color_list[index]
        v = Vector(func, color=c).shift(point)
        if opacity:
            v.set_fill(opacity=opacity)
        return v

    @staticmethod
    def field1(x, y):
        return np.array([
            -y,
            x
        ])

    @staticmethod
    def field2(x, y):
        return np.array([
            y,
            -x
        ])

    @staticmethod
    def field3(x, y):
        return np.array([
            max(0.1, y),
            0
        ])


class CurlEquation(Scene):
    def construct(self):
        ddel = TexMobject(r"\nabla = \begin{bmatrix} \
                \frac{\partial}{\partial x} \\ \
                \frac{\partial}{\partial y} \
                \end{bmatrix}", tex_to_color_map={r"\nabla": RED})
        ddel.scale(1.5)

        curl = TexMobject(
            r"\text{curl}\textbf{F} = \nabla \times \vec{\text{F}}",
            tex_to_color_map={"F": YELLOW, r"\nabla": RED})
        curl.scale(1.5)
        curl.shift(1.5 * DOWN)

        self.play(Write(ddel))
        self.wait()

        self.play(ApplyMethod(ddel.shift, 1.5 * UP))
        self.play(Write(curl))
        self.wait()


class GreenTheoremVisual(Scene):
    CONFIG = {
        "color_list": ['#e22b2b', '#e88e10', '#eae600', '#88ea00',
                       '#00eae2', '#0094ea', "#2700ea", '#bf00ea', '#ea0078'],
        "prop": 0
    }

    def construct(self):
        axes_config = {"x_min": -5,
                       "x_max": 5,
                       "y_min": -5,
                       "y_max": 5,
                       "z_axis_config": {},
                       "z_min": -1,
                       "z_max": 1,
                       "z_normal": DOWN,
                       "num_axis_pieces": 20,
                       "light_source": 9 * DOWN + 7 * LEFT + 10 * OUT,
                       "number_line_config": {
                           "include_tip": False,
                       },
                       }

        axes = Axes(**axes_config)
        f = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.vect, prop=0)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        field = VGroup(axes, f)
        # field.scale(0.6)

        axes2 = Axes(**axes_config)
        f2 = VGroup(
            *[self.calc_field_color(x * RIGHT + y * UP, self.vect, prop=0).set_fill(opacity=0.5)
              for x in np.arange(-5, 5, 1)
              for y in np.arange(-5, 5, 1)
              ]
        )

        field2 = VGroup(axes, f2)
        # field2.scale(0.6)

        c = ParametricFunction(
            self.func,
            t_min=-2,
            t_max=2,
        )
        c.set_stroke(opacity=0.75)
        label = TextMobject("C")
        label.shift(3 * LEFT)
        label.scale(2)

        surface = ParametricSurface(
            self.surface,
            u_min=-2,
            u_max=2,
            v_min=-1,
            v_max=1,
            fill_color=BLUE,
            checkerboard_colors=[BLUE, BLUE],
            stroke_color=BLUE
        ).set_fill(opacity=0.5)

        curve = VGroup(label, c)

        eq = TexMobject(
            r"\int_C \vec{\text{F}} \bullet \text{d}\vec{\text{r}}")
        back = BackgroundRectangle(eq, color=BLACK, fill_opacity=1)
        eq0 = VGroup(back, eq)
        eq0.shift(3 * UP)

        eq = TexMobject(
            r"\int_C \vec{\text{F}} \bullet \text{d}\vec{\text{r}} = \int_{C_1} \vec{\text{F}} \bullet \text{d}\vec{\text{r}} + \int_{C_2} \vec{\text{F}} \bullet \text{d}\vec{\text{r}}")
        back = BackgroundRectangle(eq, color=BLACK, fill_opacity=1)
        eq1 = VGroup(back, eq)
        eq1.shift(3 * UP)

        eq = TexMobject(
            r"\int_{C_r} \vec{\text{F}} \bullet \text{d}\vec{\text{r}} = \nabla \times \vec{\text{F}} |r|")
        back = BackgroundRectangle(eq, color=BLACK, fill_opacity=1)
        eq2 = VGroup(back, eq)
        eq2.shift(3 * UP)

        eq = TexMobject(
            r"\int_C \vec{\text{F}} \bullet \text{d}\vec{\text{r}} = \iint_D \nabla \times \vec{\text{F}} \ \text{dA}")
        back = BackgroundRectangle(eq, color=BLACK, fill_opacity=1)
        eqf = VGroup(back, eq)
        eqf.shift(3 * UP)

       # div = TexMobject(r"\iint_S \vec{\text{F}} \bullet \text{d}\vec{\text{S}}= \iiint_V \vec{\nabla} \bullet \text{d}\vec{\text{V}}
       #
       #                 ")
        t1 = [1.225]
        t2 = [0.75, 1.5]
        t3 = [i for i in np.arange(0, 2, 0.25)]
        c1 = VGroup(
            *[Line(-self.func(t)[1]*UP, self.func(t)[1] *
                   UP, color=RED, stroke_width=DEFAULT_STROKE_WIDTH*2).shift(self.func(t)[0]*RIGHT) for t in t1],
            ParametricFunction(
                self.func,
                t_min=1.22,
                t_max=2,
                color=RED,
                stroke_width=DEFAULT_STROKE_WIDTH*2
            ),
            ParametricFunction(
                self.func,
                t_min=-2,
                t_max=-1.22,
                color=RED,
                stroke_width=DEFAULT_STROKE_WIDTH*2
            ),
            TexMobject(r"\text{C}_1", color=RED).shift(
                2 * LEFT + 1.5 * UP).scale(1.5)

        )
        c2 = VGroup(
            *[Line(-self.func(t)[1]*UP, self.func(t)[1] *
                   UP, color=GREEN, stroke_width=DEFAULT_STROKE_WIDTH*2).shift(self.func(t)[0]*RIGHT) for t in t1],

            ParametricFunction(
                self.func,
                t_min=-1.22,
                t_max=1.22,
                color=GREEN,
                stroke_width=DEFAULT_STROKE_WIDTH*2
            ),
            TexMobject(r"\text{C}_2", color=GREEN).shift(
                2 * RIGHT + 1.5 * UP).scale(1.5)
        )

        table2 = VGroup()

        table3 = VGroup()

        self.play(ShowCreation(field))
        self.wait()

        self.play(Write(curve))
        self.wait()

        self.play(Transform(field, field2))
        self.wait()
        """
        self.play(Write(surface))
        self.wait()

        self.play(Write(eq0))
        self.wait()

        self.play(Transform(eq0, eq1))
        # self.wait())
        self.wait()

        self.play(Transform(eq0, eq2))
        self.wait()

        self.play(Transform(eq0, eqf))
        self.wait()
        """
        self.play(Write(c1))
        self.wait()

        self.play(Write(c2))
        self.wait()

    def calc_field_color(self, point, f, prop=0.0, opacity=None):
        x, y = point[:2]
        func = f(x, y)
        magnitude = math.sqrt(func[0] ** 2 + func[1] ** 2)
        func = func / magnitude if magnitude != 0 else np.array([0, 0])
        func = func / 1.5
        v = int(magnitude / 10 ** prop)
        index = len(self.color_list) - 1 if v > len(self.color_list) - 1 else v
        c = self.color_list[index]
        v = Vector(func, color=c).shift(point)
        if opacity:
            v.set_fill(opacity=opacity)
        return v

    @staticmethod
    def func(t):
        return np.array([
            1 - 2*t**2 + 2,
            t**3 - 4*t,
            0
        ])

    @staticmethod
    def surface(t, v):
        return np.array([
            1 - 2*t**2 + 2,
            v*(t**3 - 4*t),
            0
        ])

    @staticmethod
    def vect(x, y):
        return np.array([
            y,
            x,
            0
        ])


class FTC(Scene):
    CONFIG = {
        "x_max": 4,
        "x_labeled_nums": list(range(-1, 5)),
        "y_min": 0,
        "y_max": 2,
        "y_tick_frequency": 2.5,
        "y_labeled_nums": list(range(5, 20, 5)),
        "n_rect_iterations": 2,
        "default_right_x": 3,
        "func": lambda x: 0.1*math.pow(x-2, 2) + 1,
    }

    def construct(self):
        ftc = TexMobject(r"\int_a^b f'(x) \ dx = f(b) - f(a)")
        ftc.shift(3 * UP)

        self.play(Write(ftc))
        self.wait()

        self.setup_axes()
        self.show_graph()
        self.show_area()

    def show_graph(self):
        graph = self.get_graph(self.func)
        self.play(ShowCreation(graph))
        self.wait()

        self.graph = graph

    def show_area(self):
        dx_list = [0.25/(2**n) for n in range(self.n_rect_iterations)]
        rect_lists = [
            self.get_riemann_rectangles(
                self.graph,
                x_min=1,
                x_max=self.default_right_x,
                dx=dx,
                stroke_width=4*dx,
            )
            for dx in dx_list
        ]
        rects = rect_lists[0]
        foreground_mobjects = [self.axes, self.graph]

        self.play(
            DrawBorderThenFill(
                rect_lists[-1],
                run_time=2,
                rate_func=smooth,
                lag_ratio=0.5,
            ),
            *list(map(Animation, foreground_mobjects))
        )
        self.wait()


class AreaUnderParabola(GraphScene):

    """for new_rects in rect_lists[1:]:
        self.play(
            Transform(
                rects, new_rects,
                lag_ratio=0.5,
            ),
            *list(map(Animation, foreground_mobjects))
        )
    self.wait()

    self.rects = rects
    self.dx = dx_list[-1]
    self.foreground_mobjects = foreground_mobjects"""
