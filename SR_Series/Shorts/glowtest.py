from manim import *

class NeonGlow(Scene):
    def construct(self):
        # Create base text
        text = Text("NEON", font_size=144, color=WHITE)
        
        # Add fake glow layers
        glow_layers = VGroup()
        glow_color = BLUE
        for i in range(10, 0, -1):
            glow = text.copy()
            glow.set_stroke(color=glow_color, width=2*i, opacity=0.05*i)
            glow_layers.add(glow)

        # Set the top text (main layer)
        text.set_color(WHITE)
        text.set_stroke(color=glow_color, width=1)

        # Add to scene
        self.add(glow_layers, text)
