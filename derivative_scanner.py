from manim import *
import numpy as np

# --- CONFIG FOR INSTAGRAM REELS (9:16) ---
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
# -----------------------------------------

class DerivativeScannerReels(Scene):
    def construct(self):
        # 1. PERMANENT WATERMARK
        watermark = Text("think_nebulae", font_size=24, color=GRAY, weight=BOLD)
        watermark.set_opacity(0.3)
        watermark.to_edge(DOWN, buff=1.0).to_edge(RIGHT, buff=0.5)
        self.add(watermark)

        # 2. LAYOUT SETUP
        # Top Axis: Original Function f(x) = x^2
        # y_range goes up to 10 because 3^2 = 9
        ax1 = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-1, 10, 2],
            x_length=7, y_length=5,
            axis_config={"include_tip": True, "font_size": 24}
        ).move_to(UP * 3.5)
        
        # Bottom Axis: The Derivative f'(x) = 2x
        # y_range goes from -7 to 7 because 2*3 = 6 and 2*-3 = -6
        ax2 = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-8, 8, 2],
            x_length=7, y_length=5,
            axis_config={"include_tip": True, "font_size": 24}
        ).move_to(DOWN * 3.5)

        # 3. MATH FUNCTIONS
        def func(x):
            return x**2

        def deriv(x):
            return 2*x

        # Draw the main parabola immediately
        curve = ax1.plot(func, color=BLUE, stroke_width=4, x_range=[-3.2, 3.2])
        
        # 4. LABELS
        title = Text("Derivative Parabola", font_size=48, weight=BOLD).to_edge(UP, buff=0.5)
        
        label1 = MathTex(r"f(x) = x^2", color=BLUE, font_size=40).next_to(ax1, UP, buff=0.1)
        label2 = MathTex(r"f'(x) = 2x \text{ (Slope)}", color=RED, font_size=40).next_to(ax2, UP, buff=0.1)

        # 5. DYNAMIC ELEMENTS
        # Start scanning from x = -3
        k = ValueTracker(-3) 

        # Dot on the Top Parabola
        dot_func = always_redraw(lambda: Dot(
            point=ax1.c2p(k.get_value(), func(k.get_value())),
            color=YELLOW, radius=0.12
        ))

        # The Tangent Line (Sliding slope)
        tangent = always_redraw(lambda: TangentLine(
            curve,
            alpha=(k.get_value() + 3.2) / 6.4, # Map x to alpha [0, 1] based on plot range
            length=3,
            color=YELLOW
        ))

        # Dot on Derivative Graph (Bottom)
        dot_deriv = always_redraw(lambda: Dot(
            ax2.c2p(k.get_value(), deriv(k.get_value())), 
            color=RED, radius=0.12
        ))
        
        # Traced Path for Derivative (Draws the red line)
        deriv_path = TracedPath(dot_deriv.get_center, stroke_color=RED, stroke_width=5)

        # Digital Counter for Slope Value
        # Placed next to the top tangent point to match the video style
        slope_val = always_redraw(lambda: DecimalNumber(
            deriv(k.get_value()), 
            num_decimal_places=2, 
            color=YELLOW, 
            font_size=30
        ).next_to(dot_func, UP, buff=0.2))

        # Connector Line (Vertical line from Top Dot to Bottom Dot)
        # Added small offset to avoid 0-length crash
        connector = always_redraw(lambda: DashedLine(
            start=ax1.c2p(k.get_value(), func(k.get_value())),
            end=ax2.c2p(k.get_value(), deriv(k.get_value()) + 0.001),
            stroke_opacity=0.5, color=WHITE
        ))

        # Group for rendering
        main_objects = VGroup(
            title, ax1, ax2, label1, label2, curve, 
            tangent, dot_func, dot_deriv, deriv_path, slope_val, connector
        )

        # 6. RENDER ANIMATION
        self.add(main_objects)
        
        # Scan Animation
        # Scanning from x=-3 to x=3
        self.play(k.animate.set_value(3), run_time=12, rate_func=linear)
        self.wait(1)

        # 7. OUTRO ANIMATION
        self.play(FadeOut(main_objects), run_time=1)
        
        follow_text = Text("Follow for more!", font_size=50, weight=BOLD, gradient=(YELLOW, RED))
        sub_text = Text("@think_nebulae", font_size=30, color=GRAY).next_to(follow_text, DOWN)
        
        self.play(
            Write(follow_text),
            FadeIn(sub_text, shift=UP),
            run_time=2
        )
        self.wait(3)