from manim import *
import numpy as np

class ProjectileComparison(Scene):
    def construct(self):
        # 1. SETUP: Introduction Text (Duration: ~4s)
        title = Text("Projectile Motion", font_size=48).to_edge(UP)
        subtitle = Text("Vacuum vs. Air Resistance", font_size=36, color=GRAY).next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.wait(1)

        # 2. SETUP: Axes and Ground (Duration: ~3s)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            axis_config={"include_numbers": True},
            x_length=10,
            y_length=6
        ).to_edge(DOWN).shift(UP*0.5)
        
        labels = axes.get_axis_labels(x_label="Distance (x)", y_label="Height (y)")

        self.play(Create(axes), Write(labels), run_time=2)
        self.play(FadeOut(subtitle), run_time=1)

        # 3. PHYSICS CONSTANTS
        v0 = 8.5        # Initial velocity
        theta = 60 * DEGREES # Launch angle
        g = 9.8         # Gravity
        k = 0.3         # Drag coefficient for air resistance
        
        # 4. DEFINE PATHS
        # Path 1: Ideal (Vacuum) - Simple Parabola
        # x(t) = v0 * cos(theta) * t
        # y(t) = v0 * sin(theta) * t - 0.5 * g * t^2
        def ideal_func(t):
            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2
            return axes.c2p(x, y, 0)

        # Path 2: Real (Air Resistance) - Approximation for visual
        # With drag, velocity decreases exponentially. 
        def drag_func(t):
            # Analytic solution for linear drag
            term = (1 - np.exp(-k * t))
            x = (v0 * np.cos(theta) / k) * term
            vt = g / k 
            y = (v0 * np.sin(theta) + vt) / k * term - vt * t
            
            if y < 0: y = 0 
            return axes.c2p(x, y, 0)

        # 5. CREATE OBJECTS (Duration: ~2s)
        dot_ideal = Dot(color=BLUE)
        dot_drag = Dot(color=RED)
        
        label_ideal = Text("Vacuum", color=BLUE, font_size=24).next_to(dot_ideal, UP)
        label_drag = Text("Air Drag", color=RED, font_size=24).next_to(dot_drag, UP)

        path_ideal = TracedPath(dot_ideal.get_center, stroke_color=BLUE, stroke_width=4)
        path_drag = TracedPath(dot_drag.get_center, stroke_color=RED, stroke_width=4)

        self.add(path_ideal, path_drag)
        self.play(FadeIn(dot_ideal), FadeIn(dot_drag), run_time=1)

        # 6. ANIMATE MOTION (Duration: ~10s)
        flight_time = 2 * v0 * np.sin(theta) / g
        
        self.play(
            MoveAlongPath(dot_ideal, ParametricFunction(ideal_func, t_range=[0, flight_time], fill_opacity=0).set_opacity(0)),
            MoveAlongPath(dot_drag, ParametricFunction(drag_func, t_range=[0, flight_time], fill_opacity=0).set_opacity(0)),
            run_time=8,
            rate_func=linear
        )
        self.wait(1)

        # 7. RESULTS & FORMULAS (Duration: ~10s)
        range_line = Line(start=dot_drag.get_center(), end=dot_ideal.get_center(), color=YELLOW)
        range_text = Text("Range Loss", font_size=24, color=YELLOW).next_to(range_line, UP)

        formula = MathTex(r"\vec{F}_d = -k \vec{v}", color=RED).to_corner(UR).shift(DOWN*1)

        self.play(Create(range_line), Write(range_text), run_time=2)
        self.play(Write(formula), run_time=2)
        
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(Group(axes, labels, dot_ideal, dot_drag, title, range_line, range_text, formula, path_ideal, path_drag)))