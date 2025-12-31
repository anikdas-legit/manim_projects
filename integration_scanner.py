from manim import *
import numpy as np

# --- CONFIG FOR INSTAGRAM REELS (9:16) ---
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0
# -----------------------------------------

class IntegrationScannerSin(Scene):
    def construct(self):
        # 1. PERMANENT WATERMARK
        watermark = Text("think_nebulae", font_size=24, color=GRAY, weight=BOLD)
        watermark.set_opacity(0.3)
        watermark.to_edge(DOWN, buff=1.0).to_edge(RIGHT, buff=0.5)
        self.add(watermark)

        # 2. LAYOUT SETUP
        # Top Axis: f(x) = sin(x)
        # x_range covers -4 to 7 to show negative and positive sides
        ax1 = Axes(
            x_range=[-4, 7, 1], y_range=[-1.5, 1.5, 1],
            x_length=7, y_length=4,
            axis_config={"include_tip": True, "font_size": 24}
        ).move_to(UP * 3.5)
        
        # Bottom Axis: F(x) = -cos(x)
        ax2 = Axes(
            x_range=[-4, 7, 1], y_range=[-1.5, 1.5, 1],
            x_length=7, y_length=4,
            axis_config={"include_tip": True, "font_size": 24}
        ).move_to(DOWN * 2.5)

        # 3. MATH FUNCTIONS
        def func(x):
            return np.sin(x)

        def integral(x):
            # Pure antiderivative as requested
            return -np.cos(x)

        # Draw the curve for the full visual range
        curve = ax1.plot(func, color=BLUE, stroke_width=4, x_range=[-4, 6.5])
        
        # 4. LABELS
        title = Text("Integral Scanner", font_size=48, weight=BOLD).to_edge(UP, buff=1)


        label1 = MathTex(r"f(x) = \sin(x)", color=BLUE, font_size=48).next_to(ax1, UP)
        label2 = MathTex(r"F(x) = -\cos(x)", color=GREEN, font_size=48).next_to(ax2, UP)

        # 5. DYNAMIC ELEMENTS
        # FIX 1: Start scanning from -4 (Negative Side)
        k = ValueTracker(-4) 

        # The Area Shader
        # FIX 2: Area fills from -4 to k.get_value()
        # FIX 4: Adjusted opacity to 0.5 for better color visibility
        area = always_redraw(lambda: ax1.get_area(
            curve,
            x_range=[-4, k.get_value()], 
            color=BLUE,
            opacity=0.5 
        ))

        # Vertical Scanning Line on Top
        scan_line = always_redraw(lambda: Line(
            start=ax1.c2p(k.get_value(), 0),
            end=ax1.c2p(k.get_value(), func(k.get_value())),
            color=YELLOW, stroke_width=4
        ))

        # Dot on Integral Curve (Bottom)
        dot_integral = always_redraw(lambda: Dot(
            ax2.c2p(k.get_value(), integral(k.get_value())), 
            color=GREEN, radius=0.12
        ))
        
        # Traced Path for Integral (Draws the green line)
        integral_path = TracedPath(dot_integral.get_center, stroke_color=GREEN, stroke_width=5)

        # Digital Counter for Value
        area_val = always_redraw(lambda: DecimalNumber(
            integral(k.get_value()), 
            num_decimal_places=2, 
            color=GREEN, 
            font_size=30
        ).next_to(dot_integral, UP, buff=0.2))

        # Connector Line (Syncs top and bottom)
        connector = always_redraw(lambda: DashedLine(
            start=ax1.c2p(k.get_value(), 0),
            end=ax2.c2p(k.get_value(), integral(k.get_value())),
            stroke_opacity=0.5, color=WHITE
        ))

        # Group for rendering
        main_objects = VGroup(
            title, ax1, ax2, label1, label2, curve, 
            area, scan_line, dot_integral, integral_path, area_val, connector
        )

        # 6. RENDER ANIMATION
        self.add(main_objects)
        
        # Scan Animation
        # FIX 3: Extended duration (run_time=20) and scan range (-4 to 6.28)
        self.play(k.animate.set_value(2 * np.pi), run_time=20, rate_func=linear)
        self.wait(1)

        # 7. OUTRO ANIMATION
        self.play(FadeOut(main_objects), run_time=1)
        
        follow_text = Text("Follow for more!", font_size=50, weight=BOLD, gradient=(GREEN, BLUE))
        sub_text = Text("@think_nebulae", font_size=30, color=GRAY).next_to(follow_text, DOWN)
        
        self.play(
            Write(follow_text),
            FadeIn(sub_text, shift=UP),
            run_time=2
        )
        self.wait(1)