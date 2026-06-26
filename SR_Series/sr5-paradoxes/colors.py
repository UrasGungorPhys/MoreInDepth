from manim import *

class ColorPaletteShowcase(MovingCameraScene):
    def construct(self):
        
        self.camera.background_color = ManimColor.from_hex("#161616")  # Soft chalkboard gray
        self.camera.frame.scale(1.9).shift(RIGHT*3+DOWN*3)

        title = Text("Custom Color Palette", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Define all colors using ManimColor.from_hex
        def hexify(rgb):
            return "#{:02X}{:02X}{:02X}".format(*rgb)

        CUSTOM_COLORS = {
            "Misty Blue": ManimColor.from_hex("#404e7c"),
            "Chopin Blue": ManimColor.from_hex("#2a3d45"),
            "Fern Green": ManimColor.from_hex(hexify((58, 125, 68))),
            "Mustard": ManimColor.from_hex(hexify((231, 187, 65))),
            "Vibrant Pink": ManimColor.from_hex(hexify((219, 39, 99))),
            "Another Vibrant Pink": ManimColor.from_hex("#BF1363"),
            "Vibrant Green": ManimColor.from_hex("#00AF54"),
            "Another Vibrant Green": ManimColor.from_hex("#29BF12"),
            "Light Blue": ManimColor.from_hex("#08BDBD"),
            "Red-Orange": ManimColor.from_hex("#BA1200"),
            "Sky Blue": ManimColor.from_hex("#00BBF9"),
            "Orange Orange": ManimColor.from_hex("#FF5714"),
            "Nicer Orange": ManimColor.from_hex("#F75C03"),
            "Good Orange": ManimColor.from_hex("#E53D00"),
            "Salmon": ManimColor.from_hex("#C73E1D"),
            "Pastel Red": ManimColor.from_hex("#9E2B25"),
        }

        squares = VGroup()

        for i, (name, color) in enumerate(CUSTOM_COLORS.items()):
            square = Square(side_length=0.8).set_fill(color, 1).set_stroke(WHITE, 0.5)
            label = Text(name, font_size=20).next_to(square, DOWN, buff=0.15).scale(0.5)
            square_group = VGroup(square, label)

            row = i // 4
            col = i % 4
            square_group.move_to(LEFT * 4 + RIGHT * col * 2 + DOWN * row * 2.2 + DOWN * 1)

            squares.add(square_group)

        self.play(LaggedStart(*[FadeIn(sq) for sq in squares], lag_ratio=0.05))
        self.wait(1)

        # Draw some curves using every 3rd color
        curves = VGroup()
        colors_for_lines = list(CUSTOM_COLORS.values())[::3]

        for i, color in enumerate(colors_for_lines):
            func = FunctionGraph(
                lambda x: 0.3 * (x ** 2) - i,
                x_range=[-3, 3],
                color=color
            ).shift(RIGHT*4)
            curves.add(func)

        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2))
        self.wait(2)
