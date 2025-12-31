from manim import *

# --- Instagram Reel Config (9:16) ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

class GaussianEliminationFinal(Scene):
    def construct(self):
        # ---------------------------------------------
        # 1. PERMANENT HEADER
        # ---------------------------------------------
        header = Text("Gaussian Elimination", font_size=50, color=BLUE).to_edge(UP, buff=1.0)
        self.add(header)

        # ---------------------------------------------
        # 2. INTRO
        # ---------------------------------------------
        goal_text = Tex(r"Find values for \textbf{x}, \textbf{y}, \textbf{z}", font_size=50).next_to(header, DOWN, buff=1.0)
        self.play(Write(goal_text))
        self.wait(1)
        self.play(FadeOut(goal_text))

        # ---------------------------------------------
        # 3. SYSTEM & TRANSITION
        # ---------------------------------------------
        eq1 = MathTex("1", "x", "+", "1", "y", "+", "1", "z", "=", "6", font_size=55)
        eq2 = MathTex("2", "x", "+", "3", "y", "+", "1", "z", "=", "11", font_size=55)
        eq3 = MathTex("3", "x", "+", "1", "y", "+", "2", "z", "=", "11", font_size=55)
        
        equations = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 2)
        self.play(Write(equations), run_time=1.5)
        self.wait(0.5)

        # Split fade/keep groups
        vars_to_fade = VGroup(
            eq1[1], eq1[2], eq1[4], eq1[5], eq1[7], eq1[8], 
            eq2[1], eq2[2], eq2[4], eq2[5], eq2[7], eq2[8],
            eq3[1], eq3[2], eq3[4], eq3[5], eq3[7], eq3[8]
        )
        numbers_to_keep = VGroup(
            eq1[0], eq1[3], eq1[6], eq1[9],
            eq2[0], eq2[3], eq2[6], eq2[9],
            eq3[0], eq3[3], eq3[6], eq3[9]
        )
        
        # Evacuate
        self.play(FadeOut(vars_to_fade, shift=UP*0.5), run_time=1)
        
        # Form Matrix
        matrix = MathTex(
            r"\left[\begin{array}{ccc|c}"
            r"1 & 1 & 1 & 6 \\"
            r"2 & 3 & 1 & 11 \\"
            r"3 & 1 & 2 & 11"
            r"\end{array}\right]",
            font_size=65
        ).move_to(equations)

        self.play(ReplacementTransform(numbers_to_keep, matrix), run_time=1.5)
        self.wait(1)

        # Move Matrix UP
        self.play(matrix.animate.shift(UP * 1.5))

        # ---------------------------------------------
        # 4. ROW OPERATIONS (FIXED ARROW)
        # ---------------------------------------------
        
        # --- Arrow Setup ---
        arrow = Arrow(start=LEFT, end=RIGHT, color=RED).scale(1.2)
        # Positioned nicely at Row 2
        arrow.next_to(matrix, LEFT, buff=0.4).shift(UP * 0.1) 

        # --- Op 1: R2 = R2 - 2R1 ---
        op1_text = MathTex(r"R_2 \leftarrow R_2 - 2R_1", font_size=40, color=YELLOW).next_to(matrix, DOWN, buff=0.8)
        
        self.play(GrowArrow(arrow), Write(op1_text))
        
        matrix_step1 = MathTex(
            r"\left[\begin{array}{ccc|c}"
            r"1 & 1 & 1 & 6 \\"
            r"0 & 1 & -1 & -1 \\"
            r"3 & 1 & 2 & 11"
            r"\end{array}\right]",
            font_size=65
        ).move_to(matrix)
        
        self.play(FadeOut(matrix), FadeIn(matrix_step1), run_time=1)
        matrix = matrix_step1 
        self.wait(0.5)

        # --- Op 2: R3 = R3 - 3R1 ---
        op2_text = MathTex(r"R_3 \leftarrow R_3 - 3R_1", font_size=40, color=YELLOW).move_to(op1_text)
        
        # Fixed Arrow Movement (0.85 units down)
        self.play(
            ReplacementTransform(op1_text, op2_text),
            arrow.animate.shift(DOWN * 0.85) 
        )

        matrix_step2 = MathTex(
            r"\left[\begin{array}{ccc|c}"
            r"1 & 1 & 1 & 6 \\"
            r"0 & 1 & -1 & -1 \\"
            r"0 & -2 & -1 & -7"
            r"\end{array}\right]",
            font_size=65
        ).move_to(matrix)
        
        self.play(FadeOut(matrix), FadeIn(matrix_step2), run_time=1)
        matrix = matrix_step2
        self.wait(0.5)

        # --- Op 3: R3 = R3 + 2R2 ---
        op3_text = MathTex(r"R_3 \leftarrow R_3 + 2R_2", font_size=40, color=ORANGE).move_to(op1_text)
        
        self.play(
            ReplacementTransform(op2_text, op3_text),
            Indicate(arrow, color=ORANGE) 
        )

        matrix_final = MathTex(
            r"\left[\begin{array}{ccc|c}"
            r"1 & 1 & 1 & 6 \\"
            r"0 & 1 & -1 & -1 \\"
            r"0 & 0 & -3 & -9"
            r"\end{array}\right]",
            font_size=65
        ).move_to(matrix)

        self.play(FadeOut(matrix), FadeIn(matrix_final), run_time=1)
        matrix = matrix_final
        
        self.play(FadeOut(op3_text), FadeOut(arrow))

        # Triangle Result
        p_corner = matrix.get_corner(DL) + UP*0.2 + RIGHT*0.4
        triangle = Polygon(
            p_corner, 
            p_corner + UP*1.3, 
            p_corner + RIGHT*1.7, 
            color=GREEN, stroke_width=6
        )
        self.play(Create(triangle))
        self.wait(0.5)
        self.play(FadeOut(triangle))

        # ---------------------------------------------
        # 5. SUBSTITUTION (POSITIONS ADJUSTED)
        # ---------------------------------------------
        
        # Solve Z
        eq_z = MathTex("-3", "z", "=", "-9", font_size=55).next_to(matrix, DOWN, buff=0.8)
        self.play(Write(eq_z))
        
        ans_z = MathTex("z", "=", "3", font_size=55, color=GREEN).move_to(eq_z)
        self.play(TransformMatchingShapes(eq_z, ans_z))
        
        # --- POSITION FIX: Move to (DOWN * 1.0) instead of bottom edge ---
        self.play(ans_z.animate.move_to(DOWN * 1.0 + LEFT * 2.5))
        
        # Solve Y
        eq_y_raw = MathTex("y", "-", "1", "z", "=", "-1", font_size=55).next_to(matrix, DOWN, buff=0.8)
        self.play(Write(eq_y_raw))
        self.wait(0.5)
        
        z_copy = ans_z[2].copy()
        eq_y_sub = MathTex("y", "-", "1", "(3)", "=", "-1", font_size=55).move_to(eq_y_raw)
        
        self.play(
            Transform(z_copy, eq_y_sub[3]), 
            TransformMatchingShapes(eq_y_raw, eq_y_sub)
        )
        self.remove(z_copy)
        
        ans_y = MathTex("y", "=", "2", font_size=55, color=GREEN).move_to(eq_y_sub)
        self.play(TransformMatchingShapes(eq_y_sub, ans_y))
        
        # Move Y next to Z (Automatically adheres to the higher position)
        self.play(ans_y.animate.next_to(ans_z, RIGHT, buff=1))

        # Solve X
        eq_x_raw = MathTex("x", "+", "1", "y", "+", "1", "z", "=", "6", font_size=55).next_to(matrix, DOWN, buff=0.8)
        self.play(Write(eq_x_raw))
        
        y_copy = ans_y[2].copy()
        z_copy = ans_z[2].copy()
        eq_x_sub = MathTex("x", "+", "1", "(2)", "+", "1", "(3)", "=", "6", font_size=55).move_to(eq_x_raw)
        
        self.play(
            Transform(y_copy, eq_x_sub[3]),
            Transform(z_copy, eq_x_sub[6]),
            TransformMatchingShapes(eq_x_raw, eq_x_sub)
        )
        self.remove(y_copy, z_copy)

        ans_x = MathTex("x", "=", "1", font_size=55, color=GREEN).move_to(eq_x_sub)
        self.play(TransformMatchingShapes(eq_x_sub, ans_x))
        self.play(ans_x.animate.next_to(ans_y, RIGHT, buff=1))
        
        # Final Box
        final_group = VGroup(ans_z, ans_y, ans_x)
        box = SurroundingRectangle(final_group, color=YELLOW, buff=0.2)
        label = Text("Solution", font_size=30).next_to(box, UP)
        
        self.play(Create(box), Write(label))
        self.wait(2)

        # ---------------------------------------------
        # 6. OUTRO ANIMATION
        # ---------------------------------------------
        
        main_objects = VGroup(header, matrix, box, label, final_group)
        self.play(FadeOut(main_objects), run_time=1)

        follow_text = Text("Follow for more!", font_size=50, weight=BOLD, gradient=(GREEN, BLUE))
        sub_text = Text("@think_nebulae", font_size=30, color=GRAY).next_to(follow_text, DOWN)

        self.play(
            Write(follow_text),
            FadeIn(sub_text, shift=UP),
            run_time=2
        )
        self.wait(3)