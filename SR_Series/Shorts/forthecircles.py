from manim import *
import numpy as np

MistyBlue= ManimColor.from_hex("#404e7c")
ChopinBlue= ManimColor.from_hex("#2a3d45")
FernGreen= ManimColor.from_rgb([58, 125, 68])
Mustard= ManimColor.from_rgb([231, 187, 65])
VibrantPink= ManimColor.from_hex("#ED217C")
VibrantPink2= ManimColor.from_hex("#BF1363")
PastelGreen=ManimColor.from_hex("#00AF54")
VibrantGreen= ManimColor.from_hex("#29BF12")
LightBlue= ManimColor.from_hex("#85C7F2")
RedOrange= ManimColor.from_hex("#BA1200")
SkyBlue= ManimColor.from_hex("#01FDF6")
OrangeOrange= ManimColor.from_hex("#FF5714")
NicerOrange= ManimColor.from_hex("#F75C03")
GoodOrange= ManimColor.from_hex("#E53D00")
Salmon= ManimColor.from_hex("#C73E1D")
PastelRed= ManimColor.from_hex("#9E2B25")
SteelBlue = ManimColor.from_hex("#3F88C5")
Samoyed = ManimColor.from_hex("#E0E2DB")
NeonOrange = ManimColor.from_hex("#FE5F00")
DarkPurple = ManimColor.from_hex("#2f3061")
Emerald = ManimColor.from_hex("#23CE6B")
FakeRaspberry = ManimColor.from_hex("#F72585")
MateOrange = ManimColor.from_hex("#E4572E")

BGBlue1 = ManimColor.from_hex("#0B1A27")
BGBlue2 = ManimColor.from_hex("#091D2E")

FunRed = ManimColor.from_hex("#EF271B")
Greenough = ManimColor.from_hex("#53FF45")
PlasticPink = ManimColor.from_hex("#ED217C")
Vanilla = ManimColor.from_hex("#F5E2C8")
SchoolBus = ManimColor.from_hex("#FDE12D")
NewOrange1 = ManimColor.from_hex("#F34213")
NewOrange2 = ManimColor.from_hex("#FE5F00")
LemonOrange = ManimColor.from_hex("#F18F01")

gndcolor1 = Vanilla
gndcolor2 = SteelBlue
gndhighlight = LightBlue
gndhighlight2 = Greenough

pcolor1 = NewOrange1
pcolor2 = NewOrange2
phighlight = LemonOrange
phighlight2 = FakeRaspberry

highlight = Emerald

propercolor = Vanilla
lightcolor = SchoolBus

class Circles(MovingCameraScene):
    def construct(self):


        ll = 6  # axis lengths to draw
        axrange = 10  # coordinate ranges
        norm = ll/axrange  # normalize any distance to fit
        pcolor=BLUE_C  # Color to use for the primed axes

        # Stationary axes:

        axC = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        # grid = NumberPlane(x_range=[1,axrange,1], y_range=[1,axrange,1], 
        # x_length=ll, y_length=ll,
        # background_line_style={"stroke_color": gndcolor2,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,})


        ax_labelsC = axC.get_axis_labels(x_label="x", y_label="y").set_color(gndcolor1)


        circs = VGroup()
        for r in [4, 7, 10]:
            circi = Circle(
                radius=r * norm,  # scale radius to match axis scale
                color=gndcolor1,       # or whatever color you want
                stroke_width=2
            ).move_to(axC.c2p(0, 0))  # center at the origin of axC
            circs.add(circi)


        self.play(Create(circs))
        self.wait(5)
