from manimlib.imports import *


class Intro(Scene):
    def construct(self):
        axes = Axes(
            x_min=-2,
            x_max=4,
            y_min=-2,
            y_max=4,
            number_line_config={"include_tip": False}
        )

        f = FunctionGraph(
            self.func,
            x_min=-2,
            x_max=4
        )

        s = [-0.904, 0.904, 3.528]

        lbl = TexMobject("f(x)", color=YELLOW).move_to(f, RIGHT)
        xlbl = TexMobject("x").shift(4.5 * RIGHT)
        ylbl = TexMobject("y").shift(4.5 * UP)

        lines = VGroup(*[self.get_lines(i) for i in s])
        graph = VGroup(axes, f, lbl, xlbl, ylbl)

        grp = VGroup(graph, lines)
        grp.scale(0.9)
        grp.move_to(3 * LEFT)

        self.play(Write(graph))
        self.wait()

        head1 = TextMobject("Stationary Points", color=GOLD_B)
        head1.shift(3.5 * RIGHT + 3 * UP)
        head1.scale(1.25)

        self.play(Write(head1))

        eq1 = TexMobject("f'(x) = 0")
        eq1.scale(1)
        eq1.shift(3.5 * RIGHT + 1.5 * UP)

        self.wait()

        brect1 = BackgroundRectangle(
            eq1, buff=0.25, stroke_opacity=1, fill_opacity=0, stroke_width=4, color=BLUE)

        self.play(Write(eq1))
        self.play(Write(brect1), Write(lines))
        self.wait()

        head2 = TextMobject("Local min/max", color=GREEN)
        head2.shift(3.5 * RIGHT + 1 * DOWN)
        head2.scale(1.25)

        eq2 = TexMobject(r"\text{sign of } f''(x)")
        eq2.shift(3.5 * RIGHT + 2.5 * DOWN)

        brect2 = BackgroundRectangle(
            eq2, buff=0.25, stroke_opacity=1, fill_opacity=0, stroke_width=4, color=PURPLE)

        self.play(Write(head2))
        self.play(Write(brect2), Write(eq2))
        self.wait()

    def func(self, x):
        return x * np.sin(np.cos(x)) + 2

    def get_lines(self, point):
        ret = VGroup()
        ret.add(DashedLine(ORIGIN, self.func(point) * UP,
                           dash_length=0.1, stroke_opacity=0.7).shift(point * RIGHT))
        ret.add(Line(0.75 * LEFT, 0.75 * RIGHT,
                     color=BLUE).shift([point, self.func(point), 0]))

        return ret


class Functional(Scene):
    def construct(self):
        eq1 = TexMobject("D(f(x))", tex_to_color_map={
                         "f": RED, "D": BLUE, "x": GREEN})
        eq1.scale(3)

        eq2 = TexMobject("D(f)", tex_to_color_map={
                         "f": RED, "D": BLUE, "x": GREEN})
        eq2.scale(3)

        self.play(Write(eq1))
        self.wait()

        self.play(Transform(eq1, eq2))
        self.play(eq1.scale, 1.5/3)
        self.play(eq1.shift, 3 * UP)

        axes = Axes(
            x_min=-3,
            x_max=3,
            y_min=-2,
            y_max=2,
            number_line_config={"include_tip": False}
        )

        tracker = ValueTracker(-1)

        func = ParametricFunction(
            self.f_r(theta=PI/4), color=RED, t_min=-2, t_max=2)
        func.add_updater(lambda x: x.become(
            ParametricFunction(
                self.f_r(theta=PI/4, alpha=np.sin(tracker.get_value())), color=RED, t_min=-2, t_max=2)
        ).shift(0.5 * DOWN))
        grp = VGroup(axes, func)
        grp.shift(0.5 * DOWN)

        p1 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p1.shift([-np.sqrt(2), -np.sqrt(2) - 0.5, 0])

        p2 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p2.shift([np.sqrt(2), np.sqrt(2) - 0.5, 0])

        lbl1 = TexMobject("A").move_to(p1).shift(0.5 * DOWN)
        lbl2 = TexMobject("B").move_to(p2).shift(0.5 * UP)

        points = VGroup(p1, p2, lbl1, lbl2)

        self.play(Write(points))
        self.wait()

        self.bring_to_back(grp)
        self.play(Write(grp))
        self.wait()

        self.play(tracker.increment_value, 8, rate_func=linear,
                  run_time=4*DEFAULT_ANIMATION_RUN_TIME)
        self.wait()

        head1 = TextMobject(r"Distance from \( A \) to \( B \) along \( f \)", tex_to_color_map={
                            r"\( f \)": RED, r"\( A \)": GREEN, r"\( B \)": GREEN})
        head1.scale(1.25)
        head1.shift(3 * UP + 1.75 * RIGHT)

        self.play(eq1.shift, 5 * LEFT)

        arrow = Arrow(4 * LEFT, 2.5 * LEFT, color=GOLD).shift(3 * UP)
        self.play(Write(arrow), FadeInFromDown(head1))

        self.wait()

    def f(self, x, alpha=0):
        return alpha * np.cos(PI/4 * x)

    def f_r(self, theta=PI/4, alpha=0):
        return lambda t: [
            t * np.cos(theta) - self.f(t, alpha=alpha) * np.sin(theta),
            t * np.sin(theta) + self.f(t, alpha=alpha) * np.cos(theta),
            0]

    def func(self, t):
        return [t - self.f(t), t + self.f(t), 0]


class Difference(Scene):
    def construct(self):
        t1 = TextMobject("Traditional Calculus", color=GOLD)
        t2 = TextMobject("Variational Calculus", color=PURPLE)

        t1.shift(3.5 * LEFT + 3 * UP)
        t2.shift(3.5 * RIGHT + 3 * UP)

        t1.scale(1.25)
        t2.scale(1.25)

        l1 = Line(6 * UP, 6 * DOWN)
        l2 = Line(10 * LEFT, 10 * RIGHT).shift(2 * UP)

        grp = VGroup(t1, t2, l1, l2)

        self.play(Write(grp))
        self.wait()

        