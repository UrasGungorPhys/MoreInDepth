from manim import *

class MovingTickingClock(Scene):
    def construct(self):
        # Clock face and hands
        face = Circle()
        hour_hand = Line(ORIGIN, UP * 0.5, color=BLUE)
        minute_hand = Line(ORIGIN, UP, color=RED)

        clock = VGroup(face, hour_hand, minute_hand)
        clock.move_to(LEFT * 4)  # Start on the left
        self.add(clock)

        # Animate hands ticking using always_redraw + ValueTrackers
        minute_angle = ValueTracker(0)
        hour_angle = ValueTracker(0)

        def update_minute_hand(hand):
            hand.become(Line(ORIGIN, UP).rotate(minute_angle.get_value()).set_color(RED))

        def update_hour_hand(hand):
            hand.become(Line(ORIGIN, UP * 0.5).rotate(hour_angle.get_value()).set_color(BLUE))

        minute_hand.add_updater(update_minute_hand)
        hour_hand.add_updater(update_hour_hand)

        # Animate: ticking + move to right
        self.play(
            minute_angle.animate.increment_value(PI * 4),  # 2 full ticks
            hour_angle.animate.increment_value(PI * 2),    # 1 full tick
            clock.animate.shift(RIGHT * 8),
            run_time=4,
            rate_func=linear
        )

        self.wait()

