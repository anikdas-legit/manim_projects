from manim import *

class Schrodinger(Scene):
    def construct(self):
        # Testing LaTeX rendering for physics
        eq = MathTex(r"i\hbar \frac{\partial}{\partial t} \Psi = \hat{H} \Psi")
        self.play(Write(eq))
        self.play(eq.animate.set_color(BLUE).scale(1.5))
        self.wait(2)