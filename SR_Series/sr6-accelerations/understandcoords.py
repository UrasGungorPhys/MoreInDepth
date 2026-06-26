from manim import *
import numpy as np
import math

class Testcode(MovingCameraScene):
    def construct(self):
        ax = Axes(x_range=[-7,7,1], y_range=[-4,4,1], 
        x_length=14, y_length=14,axis_config={"include_ticks": False, "stroke_width":3.5})

        self.play(Create(ax))

        for j in range(-5, 5,2):
            for i in range(-7,7):

                di = Dot([i,j,0])
                dj = Dot(ax.c2p(i,j)).set_color(YELLOW)
                self.play(Create(di),run_time=0.1)
                self.play(Create(dj),run_time=0.1)


        self.wait(10)