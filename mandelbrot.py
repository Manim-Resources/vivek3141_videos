from manimlib import *

YELLOW_Z = "#e2e1a4"

A_AQUA = "#8dd3c7"
A_YELLOW = "#ffffb3"
A_LAVENDER = "#bebada"
A_RED = "#fb8072"
A_BLUE = "#80b1d3"
A_ORANGE = "#fdb462"
A_GREEN = "#b3de69"
A_PINK = "#fccde5"
A_GREY = "#d9d9d9"
A_VIOLET = "#bc80bd"
A_UNKA = "#ccebc5"
A_UNKB = "#ffed6f"


def c_to_str(c, conv=int, compare=lambda c: c.imag < 0):
    '''
    Complex Number to String
    (1+1j) -> "1 + i"
    (1) -> "1"
    (1-1j) -> "1 - i"
    '''
    if c.imag == 0:
        return f"{conv(c.real)}"
    else:
        return f"{conv(c.real)} {'-' if compare(c) else '+'} {conv(abs(c.imag))}i"


class MandelbrotSet(Mobject):
    CONFIG = {
        "shader_folder": "shaders/mandelbrot",
        "num_steps": 100,
        "max_arg": 2.0,
        "color_style": 0
    }

    def __init__(self, plane, **kwargs):
        super().__init__(
            scale_factor=plane.get_x_unit_size(),
            offset=plane.n2p(0),
            **kwargs,
        )
        self.replace(plane, stretch=True)

    def init_uniforms(self):
        super().init_uniforms()
        self.uniforms["scale_factor"] = self.scale_factor
        self.uniforms["opacity"] = self.opacity
        self.uniforms["num_steps"] = self.num_steps
        self.uniforms["max_arg"] = self.max_arg
        self.uniforms["opacity"] = self.opacity
        self.uniforms["offset"] = self.offset
        self.uniforms["color_style"] = self.color_style

    def init_data(self):
        self.data = {
            "points": np.array([UL, DL, UR, DR]),
        }

    def set_opacity(self, opacity):
        self.uniforms["opacity"] = opacity


class MandelbrotTest(Scene):
    def construct(self):
        c = ComplexPlane()
        t = MandelbrotSet(c)
        self.add(t)
        self.embed()


class Intro(Scene):
    def construct(self):
        c = ComplexPlane(x_range=(-3, 2), y_range=(-1, 1))
        c.scale(4)

        m = MandelbrotSet(c, opacity=0.75)
        v = ValueTracker(1)

        def m_updater(m, v=v, c=c):
            m_ = MandelbrotSet(c, opacity=0.75, num_steps=v.get_value())
            m.become(m_)
        m.add_updater(m_updater)

        self.add(c, m)
        self.wait(1)
        self.play(v.increment_value, 100, run_time=5)
        self.wait()

        self.embed()


class MandelbrotIntro(Scene):
    CONFIG = {
        "color_map": {**{str(i): A_YELLOW for i in range(10)},
                      "i": A_YELLOW, "-": A_YELLOW, ".": A_YELLOW,
                      "f": A_GREEN, "z": A_PINK}
    }

    def construct(self):
        # This is some bad code by me, but hey it works. This is something I think manim can do better.
        # If you're wondering why I don't transform each ComplexPlane into one another,
        # it's because the coordinate labels make it weird-looking.

        c1 = ComplexPlane()
        c1.add_coordinate_labels()
        c1.remove(c1.coordinate_labels)

        c2 = ComplexPlane()
        c2.scale(3)
        c2.add_coordinate_labels()
        c2.remove(c2.coordinate_labels)

        c3 = ComplexPlane()
        c3.scale(3)
        c3.shift(2.25 * LEFT)
        c3.add_coordinate_labels()

        self.play(Write(c1), Write(c1.coordinate_labels))
        self.wait()

        self.play(Uncreate(c1.coordinate_labels), Transform(c1, c2))
        self.play(Write(c2.coordinate_labels))

        c2.add(c2.coordinate_labels)
        self.remove(c1)
        self.add(c2)

        rect = Polygon(
            [0.77, FRAME_HEIGHT/2, 0],
            [FRAME_WIDTH/2, FRAME_HEIGHT/2, 0],
            [FRAME_WIDTH/2, -FRAME_HEIGHT/2, 0],
            [0.77, -FRAME_HEIGHT/2, 0],
            fill_opacity=1,
            stroke_width=0,
            fill_color=BLACK
        )

        c = ComplexPlane(x_range=(-2, 1), y_range=(-2, 2))
        c.scale(3)
        c.shift(3.75 * LEFT)
        c.add_coordinate_labels()

        self.play(Transform(c2, c3))
        self.play(FadeIn(rect))

        m = MandelbrotSet(c, opacity=0.75, color_style=1)

        l = Line(10 * UP, 10 * DOWN).shift(c.n2p(1))

        self.play(Write(l))
        self.play(FadeIn(m))
        self.wait()

        eq1 = Tex("f(z) = z^2 + c",
                  tex_to_color_map={"2": A_YELLOW, "f": A_GREEN, "z": A_PINK, "c": A_YELLOW})
        eq2 = Tex("f(z) = z^2 + ", "(", "-1+i", ")", tex_to_color_map={
                  "f": A_GREEN, "z": A_PINK, "1": A_YELLOW, "i": A_YELLOW, "2": A_YELLOW, "-": A_YELLOW})
        eq2.scale(1.25)
        eq1.scale(1.25)

        # 3.93 = (FRAME_WIDTH/2 - 0.75)/2 + 0.75
        eq1.move_to(3 * UP + 3.93 * RIGHT)
        eq2.move_to(3 * UP + 3.93 * RIGHT)

        self.play(Write(eq1))
        self.wait()

        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()

        vals = []
        curr = 0
        for _ in range(10):
            vals.append(curr)
            curr = (lambda z: z**2 + (-1 + 1j))(curr)

        steps = VGroup()
        for i in range(4):
            eq = Tex("f(", c_to_str(vals[i]), ")", "=", c_to_str(vals[i+1]),
                     tex_to_color_map={**self.color_map, "f": A_GREEN})
            eq.scale(1.25)
            eq.move_to(eq2, LEFT)
            eq.shift((i+1) * 1.25*DOWN)
            steps.add(eq)

        d = [self.get_dot_grp(z, c) for z in vals[:6]]

        self.play(Write(d[0]))
        self.wait()

        self.play(Write(steps[0]))
        self.play(TransformFromCopy(steps[0][-5:], d[1][1]))
        self.play(Transform(d[0][0], d[1][0]), Uncreate(d[0][1]))
        self.wait()

        for i in range(3):
            self.play(
                TransformFromCopy(steps[i][-5:], steps[i+1][2:7]),
                Write(steps[i+1][:2]), Write(steps[i+1][7])
            )
            self.play(Write(steps[i+1][8:]))
            self.play(TransformFromCopy(steps[i+1][-5:], d[i+2][1]))
            if i < 2:
                self.play(Transform(d[0][0], d[i+2][0]), Uncreate(d[i+1][1]))
                self.wait()

        vdots = Tex(r"\vdots").scale(1.25)
        vdots.move_to(steps[-1])
        vdots.shift(1.25 * DOWN)

        self.play(Write(vdots))
        self.wait()

        eq3 = Tex("f(z) = z^2 + ", "(", "-0.25+0.25i", ")", tex_to_color_map={
                  "f": A_GREEN, "z": A_PINK, "0.25": A_YELLOW,
                  "i": A_YELLOW, "2": A_YELLOW, "-": A_YELLOW})
        eq3.move_to(eq2)

        self.play(FadeOut(VGroup(steps, vdots), DOWN))
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait()

        mandel1 = self.get_mandel_lines(-0.25 + 0.25j, c)
        steps2 = VGroup()

        curr, prev = -0.25+0.25j, 0
        for i in range(5):
            eq = Tex(
                "f(", c_to_str(prev, conv=lambda x: f"{x:.2f}"), ")",
                "=", c_to_str(curr, conv=lambda x: f"{x:.2f}"),
                tex_to_color_map={**self.color_map, "f": A_GREEN}
            )
            eq.scale(0.85)
            eq.move_to(eq3, LEFT)
            eq.shift((i+1) * 1*DOWN)
            steps2.add(eq)
            curr, prev = (lambda z: z**2 + (-0.25 + 0.25j))(curr), curr

        vdots = Tex(r"\vdots").scale(1.25)
        vdots.move_to(steps2[4]).shift(1.1 * DOWN)

        self.play(TransformFromCopy(eq3, mandel1))
        for i in steps2:
            self.play(FadeIn(i, DOWN))
        self.play(Write(vdots))
        self.wait()

        self.play(Uncreate(mandel1), FadeOut(steps2, UP), FadeOut(vdots, UP))

        d = self.get_dot_grp(-0.75, c, conv=lambda s: f"{s:.2f}", color=A_RED)
        eq4 = Tex("f(z) = z^2 + (-0.75)", tex_to_color_map=self.color_map)
        eq4.move_to(eq3, LEFT)

        self.play(Write(d))
        self.play(FocusOn(d))
        self.play(Uncreate(eq3[8:]), Write(eq4[-1]))
        self.play(TransformFromCopy(d[1], eq4[7:12]))

        self.remove(self.mobjects[-1], eq3)
        self.add(eq4)

        self.play(eq4.move_to, 3 * UP + 3.93 * RIGHT)
        self.wait()

        v = ValueTracker(0)

        def dot_updater(d):
            d_ = self.get_dot_grp(
                -0.75 + v.get_value()*1j, c,
                conv=lambda s: f"{s:.2f}", color=A_RED)
            d.become(d_)

        def m_updater(m):
            m_ = self.get_mandel_lines(-0.75 + v.get_value()*1j, c)
            m.become(m_)
            self.bring_to_front(d)

        m1 = self.get_mandel_lines(-0.75, c)
        m1.add_updater(m_updater)
        d.add_updater(dot_updater)

        self.play(Write(m1))
        self.play(v.increment_value, 1, run_time=7.5)
        self.wait()

        h1 = Tex(r"\epsilon", color=A_LAVENDER)
        h1.scale(1.5)
        h1.move_to(2.34 * RIGHT + 1.75 * UP)

        h_eq = Tex(r"f(z) = z^2 + (-0.75 + \epsilon i)",
                   tex_to_color_map={**self.color_map, r"\epsilon": A_LAVENDER})
        h_text = Text("# of steps till\n\nreaches a magnitude of 2")
        h2 = VGroup(h_text, h_eq)
        h2.scale(0.5)
        h2.move_to(5.52 * RIGHT + 1.75 * UP)

        l1 = Line(2.25 * UP, 5 * DOWN).shift(3.93 * RIGHT)
        l2 = Line(0.75 * RIGHT, 7 * RIGHT).shift(1.25 * UP)

        self.play(Write(l1), Write(l2))
        self.play(Write(h1), Write(h2))

        tab = VGroup()
        for i in range(5):
            t1 = Tex(str(1/10**i)).move_to(h1).shift(1 * (i+1) * DOWN)
            t2 = Tex(str(int(10**i*PI))).move_to(h2).shift(1 * (i+1) * DOWN)
            tab.add(t1, t2)
        tab.shift(0.1 * DOWN)

        for i in range(2):
            self.play(TransformFromCopy(d[-5:-1], tab[2*i]))
            self.play(TransformFromCopy(m1, tab[2*i+1]))
            self.play(v.set_value, 1/10**(i+1))

        self.play(TransformFromCopy(d[-5:-1], tab[2*2]))
        self.play(TransformFromCopy(m1, tab[2*2+1]))

        for i in range(3, 5):
            self.play(FadeIn(tab[2*i], DOWN), FadeIn(tab[2*i+1], DOWN))

        self.wait()
        self.embed()

    def get_dot_grp(self, z, c, conv=int,
                    c_str_func=c_to_str, color=A_ORANGE,
                    tex_to_color_map=None, radius=0.1):
        if tex_to_color_map is None:
            tex_to_color_map = self.color_map

        d_ = Dot(c.n2p(z), color=color, radius=radius)
        return VGroup(
            d_,
            Tex(c_str_func(z, conv), tex_to_color_map=tex_to_color_map
                ).next_to(d_, DOWN).add_background_rectangle(buff=0.075),
        )

    def get_mandel_lines(self, point, c, steps=15, max_arg=10000):
        curr, prev = point, 0
        grp = VGroup()

        for i in range(steps):
            grp.add_to_back(
                Line(c.n2p(curr), c.n2p(prev), stroke_opacity=0.5))
            grp.add(Dot(c.n2p(prev), color=A_ORANGE))
            if abs(curr) < max_arg:  # Avoid overflow
                curr, prev = (lambda z: z**2 + point)(curr), curr
            else:
                break

        return grp


class ExpIntro(MandelbrotIntro):
    def construct(self):
        c = ComplexPlane(x_range=(-3, 2), y_range=(-1, 1))
        c.scale(4)
        c.add_coordinate_labels()

        m = MandelbrotSet(c, opacity=0.75, color_style=1)
        d1 = self.get_dot_grp(0.25, c, conv=lambda s: f"{s:.2f}", color=A_RED)

        self.play(Write(c), FadeIn(m))
        self.play(Write(d1), FocusOn(d1[0]))
        self.wait()

        d2 = self.get_dot_grp(
            0.6, c, c_str_func=lambda c, _: r"0.25 + \epsilon",
            tex_to_color_map={"0.25": A_YELLOW, "+": A_YELLOW, r"\epsilon": A_LAVENDER})

        self.play(TransformFromCopy(d1, d2))
        self.wait()

        eq = Tex("f(z) = z^2 + 0.25", tex_to_color_map=self.color_map)
        eq.scale(1.5)
        eq.shift(3.35 * UP)
        eq.add_background_rectangle(buff=0.1, opacity=0.9)

        axes = Axes(
            x_range=(-1, 1, 0.5), y_range=(0, 1, 0.5), axis_config={"include_tip": False},
            x_axis_config={"stroke_width": 6}, y_axis_config={"stroke_width": 6},
        )
        axes.scale(0.95)
        axes.shift(0.3 * DOWN)
        axes.add_coordinate_labels(font_size=36, num_decimal_places=1)

        c1 = axes.get_graph(
            lambda x: x**2 + 0.25,
            x_range=(-np.sqrt(0.75), np.sqrt(0.75)),
            color=A_RED, stroke_width=6
        )

        self.play(Write(eq))
        self.wait()

        l1 = DashedLine(
            axes.c2p(-1, 0.25), axes.c2p(1, 0.25), dash_length=0.1,
            positive_space_ratio=0.4, color=A_YELLOW, opacity=0.5)

        lbl1 = Tex("0.25", color=A_YELLOW)
        lbl1.move_to(l1, LEFT)
        lbl1.shift(0.4 * UP)

        cp = lbl1.copy()
        cp.scale(1.5)
        cp.move_to(eq[8:12])

        self.play(FadeOut(m), Uncreate(d1), Uncreate(d2), Uncreate(c))
        self.play(Write(axes))
        self.play(TransformFromCopy(eq, c1))
        self.play(Write(l1))
        self.play(TransformFromCopy(cp, lbl1))
        self.wait()

        l2 = axes.get_graph(lambda x: x)
        l2_lbl = Tex("y = x")
        l2_lbl.rotate(np.arctan2(5.805, 5.7))  # c2p(1, 1) - c2p(0, 0)
        l2_lbl.move_to(4.2844 * RIGHT + 0.5710 * UP)

        curr = 0
        def f(z): return z**2 + 0.25
        dot = Dot(axes.c2p(0, 0), color=A_BLUE)

        self.play(Write(l2), Write(l2_lbl))
        self.wait()

        self.play(Write(dot))
        self.play(FocusOn(dot))

        for _ in range(10):
            self.play(
                ShowCreation(
                    Line(axes.c2p(curr, curr), axes.c2p(curr, f(curr)),
                         color=A_BLUE, stroke_width=6)),
                ApplyMethod(dot.move_to, axes.c2p(curr, f(curr)))
            )
            self.play(
                ShowCreation(
                    Line(axes.c2p(curr, f(curr)), axes.c2p(f(curr), f(curr)),
                         color=A_BLUE, stroke_width=6)),
                ApplyMethod(dot.move_to, axes.c2p(f(curr), f(curr)))
            )
            curr = f(curr)
        self.wait()

        self.embed()
