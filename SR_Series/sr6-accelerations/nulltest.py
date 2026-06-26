from manim import *


# Base & background
bgcolor        = ManimColor.from_hex("#1E2A35")  # Dark grayish-blue background
proper         = ManimColor.from_hex("#F3E9D2")  # Vanilla main drawing/text color

# Ground frame
gnd1           = ManimColor.from_hex("#A6B1B9")  # Soft desaturated blue-gray
gnd2           = ManimColor.from_hex("#8B9AA4")  # Darker steel-gray-blue
gndhighlight   = ManimColor.from_hex("#4DD0E1")  # Bright cyan highlight (matches blues)

# Moving frame (orange theme)
prime1         = ManimColor.from_hex("#D4B483")  # Muted sandy beige-orange
prime2         = ManimColor.from_hex("#B88A50")  # Warm caramel-brown
primehighlight = ManimColor.from_hex("#FFA726")  # Bright orange highlight


class ColorSwatchScene(Scene):
    def construct(self):
        self.camera.background_color = bgcolor

        def make_swatch(color, label_text):
            rect = Rectangle(width=2, height=1, fill_color=color, fill_opacity=1, stroke_width=0)
            label = Text(label_text, font_size=24, color=proper)
            label.next_to(rect, DOWN, buff=0.15)
            return VGroup(rect, label)

        # Proper swatch at top
        proper_swatch = make_swatch(proper, "proper (main)")

        # Ground frame row
        gnd_swatch_row = VGroup(
            make_swatch(gnd1, "gnd1"),
            make_swatch(gnd2, "gnd2"),
            make_swatch(gndhighlight, "gndhighlight")
        ).arrange(RIGHT, buff=0.5)

        # Moving frame row
        prime_swatch_row = VGroup(
            make_swatch(prime1, "prime1"),
            make_swatch(prime2, "prime2"),
            make_swatch(primehighlight, "primehighlight")
        ).arrange(RIGHT, buff=0.5)

        # Arrange all
        swatches = VGroup(
            proper_swatch,
            gnd_swatch_row,
            prime_swatch_row
        ).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(FadeIn(swatches, shift=UP))
        self.wait(2)
