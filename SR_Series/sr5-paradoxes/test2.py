from manim import *

class TriggerExample(Scene):
    def construct(self):
        dot = Dot(LEFT * 4, color=BLUE)
        other_dot = Dot(UP * 2, color=RED).set_opacity(0)

        triggered = False

        def check_position(mob, dt):
            nonlocal triggered
            if not triggered and mob.get_center()[0] > 0:
                triggered = True  # Just set flag

        dot.add_updater(check_position)
        self.add(dot, other_dot)

        self.play(dot.animate.move_to(RIGHT * 4), run_time=4)
        dot.remove_updater(check_position)

        if triggered:
            self.play(FadeIn(other_dot))

