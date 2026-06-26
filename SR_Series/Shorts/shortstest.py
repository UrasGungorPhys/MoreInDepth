from manim import *
import numpy as np


config.pixel_width = 1080
config.pixel_height = 1920

class Paradox1(MovingCameraScene):

    def construct(self):
        # custom colors
        MistyBlue= ManimColor.from_hex("#404e7c")
        ChopinBlue= ManimColor.from_hex("#2a3d45")
        FernGreen= ManimColor.from_rgb([58, 125, 68])
        Mustard= ManimColor.from_rgb([231, 187, 65])
        VibrantPink= ManimColor.from_rgb([219, 39, 99])
        VibrantPink2= ManimColor.from_hex("#BF1363")
        PastelGreen=ManimColor.from_hex("#00AF54")
        VibrantGreen= ManimColor.from_hex("#29BF12")
        LightBlue= ManimColor.from_hex("#08BDBD")
        RedOrange= ManimColor.from_hex("#BA1200")
        SkyBlue= ManimColor.from_hex("#00BBF9")
        OrangeOrange= ManimColor.from_hex("#FF5714")
        NicerOrange= ManimColor.from_hex("#F75C03")
        GoodOrange= ManimColor.from_hex("#E53D00")
        Salmon= ManimColor.from_hex("#C73E1D")
        PastelRed= ManimColor.from_hex("#9E2B25")
        SteelBlue = ManimColor.from_hex("#3F88C5")
        Samoyed = ManimColor.from_hex("#E0E2DB")
        NeonOrange = ManimColor.from_hex("#FE5F00")
        DarkPurple = ManimColor.from_hex("#2f3061")

        gndcolor1 = SkyBlue
        gndcolor2 = SteelBlue
        gndhighlight = LightBlue

        pcolor1 = OrangeOrange
        pcolor2=GoodOrange
        phighlight = NeonOrange

        highlight = VibrantGreen
        propercolor = Samoyed
        lightcolor = Mustard


        # Background stars:
        stars = VGroup()
        for i in range(1500):
            xs = np.random.uniform(-10,26)
            ys = np.random.uniform(-20,20)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)


        clockscale = 0.2
        clockimg = ImageMobject("clock.png").scale(clockscale)
        clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale))
        clockcenter = always_redraw(lambda:Dot(clockimg.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
        clock12 = always_redraw(lambda:Dot(clockimg.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetip = Dot(clock12.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))

        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)

        clockimgB = ImageMobject("clock.png").scale(clockscale)
        clockbgB = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimgB.get_center()).scale(clockscale))
        clockcenterB = always_redraw(lambda:Dot(clockimgB.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
        clock12B = always_redraw(lambda:Dot(clockimgB.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetipB = Dot(clock12B.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clocklineB = always_redraw(lambda:Line(clockimgB.get_center(), clocklinetipB.get_center(), stroke_width=10*clockscale).set_color(BLACK))

        clockB=Group(clockbgB, clockimgB, clocklineB, clock12B, clockcenterB, clocklinetipB)

        rocket = ImageMobject("rocket.png").scale(0.3).to_edge(UP+LEFT, buff=0)
        rocketpos0 = rocket.get_center()
        planet1 = ImageMobject("planet1.png").scale(0.3).to_edge(DOWN, buff=1).shift(DOWN*0.7)
        planet2 = ImageMobject("planet2.png").scale(0.4).to_corner(RIGHT+DOWN, buff=1).shift(RIGHT*10+DOWN*0.7)

        clock.move_to(planet1.get_center()).shift(RIGHT*2.5+DOWN*0.5)

        rocketV = always_redraw(lambda: Arrow(start=rocket.get_right(), end=rocket.get_right()+RIGHT*0.8, buff=0.01)).set_color(propercolor)
        vlabel = always_redraw(lambda: MathTex("v").next_to(rocketV.get_right())).set_color(propercolor)

        self.add(stars)
        self.play(FadeIn(planet1))
        self.play(FadeIn(planet2))
        self.play(FadeIn(rocket))
        self.play(FadeIn(rocketV), FadeIn(vlabel))
        self.wait(2)
        self.play(rocket.animate.move_to([planet1.get_x(), rocket.get_y(),0]), run_time=1.5, rate_func=linear)