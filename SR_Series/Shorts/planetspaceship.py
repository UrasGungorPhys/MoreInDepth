from manim import *
import numpy as np


# config.pixel_width = 1080
# config.pixel_height = 1920

config.pixel_width = 360
config.pixel_height = 640

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
        for i in range(100):
            xs = np.random.uniform(-10,26)
            ys = np.random.uniform(-20,20)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)


        clockscale = 0.25
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

        rocket = ImageMobject("rocket.png").scale(0.5).to_edge(UP+LEFT, buff=0).shift(UP*5)
        rocketpos0 = rocket.get_center()
        planet1 = ImageMobject("planet1.png").scale(0.45).to_corner(DOWN, buff=1).shift(DOWN*5+RIGHT)
        planet2 = ImageMobject("planet2.png").scale(0.5).to_corner(RIGHT+DOWN, buff=1).shift(RIGHT*9+DOWN*5)

        clock.move_to(planet1.get_center()).shift(RIGHT*3+DOWN*0.5)

        rocketV = always_redraw(lambda: Arrow(start=rocket.get_right(), end=rocket.get_right()+RIGHT*0.8, buff=0.01)).set_color(propercolor)
        vlabel = always_redraw(lambda: MathTex("v").next_to(rocketV.get_right())).set_color(propercolor)

        self.add(stars)
        self.play(FadeIn(planet1))
        self.play(FadeIn(planet2))
        self.play(FadeIn(rocket))
        self.play(FadeIn(rocketV), FadeIn(vlabel))
        self.wait(2)
        self.play(rocket.animate.move_to([planet1.get_x(), rocket.get_y(),0]), run_time=1.5, rate_func=linear)
        spaceshipclock = clock.copy().move_to(rocket).shift(RIGHT*2.5+DOWN*1.6)

        # set t=0 when they're aligned.
        t0line = DashedLine(start=rocket.get_center(), end=planet1.get_center()).set_color(propercolor)
        t0label = MathTex("t = 0").next_to(t0line.get_bottom()).set_color(gndhighlight)
        tp0label = MathTex("t'= 0").next_to(t0line.get_top(), RIGHT+DOWN*3).set_color(phighlight)

        self.play(AnimationGroup(FadeIn(clock), FadeIn(spaceshipclock)))
        self.wait(2.5)
        # self.play(FadeIn(t0label), FadeIn(tp0label))
        # self.wait(2)
        # self.play(FadeOut(t0label), FadeOut(tp0label))
        camchange = self.camera.frame.animate(run_time=3).move_to(RIGHT*8.5).scale(1.45)
        self.play(AnimationGroup(camchange,FadeOut(*[clock, spaceshipclock])))

        clockscale = 0.35
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


        def advance_clock(startN, N,runtime=8, rate=0.5, gamma=1, halftick=False):
            tickrange = np.abs(startN-N)
            clockanimationlist = []
            for i in range(tickrange):
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-i*PI/6, 
                                angle=-PI/6, arc_center=clockcenter.get_center()).set_opacity(0).set_color(GoodOrange))
                tickanimation = MoveAlongPath(clocklinetip, tickarc_i, run_time=rate*gamma)
                # tickanimation=(Create(tickarc_i))
                clockanimationlist.append(tickanimation)

            if halftick:
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-N*PI/6, 
                                angle=-PI/12, arc_center=clockcenter.get_center()).set_opacity(0).set_color(GoodOrange))
                tickanimation = MoveAlongPath(clocklinetip, tickarc_i, run_time=rate*gamma/2)
                clockanimationlist.append(tickanimation)

            # tickcircleN = Arc(radius=2.9, start_angle=PI/2-startN*PI/6, angle=-np.abs(startN-N)*PI/6).set_opacity(0)
            # clockanimation = MoveAlongPath(clocklinetip, tickcircleN, rate_func=linear, run_time=np.abs(startN-N)*rate)
            clockanimation = AnimationGroup(*clockanimationlist, lag_ratio=2.2*gamma, run_time=runtime)
            return clockanimation
        

        def advance_clockB(startN, N, runtime=8, rate=0.5, gamma=1, halftick=False, halftick0=False):
    
            clockanimationlist = []

            if halftick0:
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-PI/12, 
                                angle=-PI/12, arc_center=clockcenterB.get_center()).set_opacity(0).set_color(GoodOrange))
                tickanimation = MoveAlongPath(clocklinetipB, tickarc_i, run_time=rate*gamma/2)
                clockanimationlist.append(tickanimation)
                startN+=1

            tickrange = np.abs(startN-N)

            for i in range(tickrange):
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-i*PI/6, 
                                angle=-PI/6, arc_center=clockcenterB.get_center()).set_opacity(0).set_color(GoodOrange))
                tickanimation = MoveAlongPath(clocklinetipB, tickarc_i, run_time=rate*gamma)
                # tickanimation=(Create(tickarc_i))
                clockanimationlist.append(tickanimation)

            if halftick:
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-N*PI/6, 
                                angle=-PI/12, arc_center=clockcenterB.get_center()).set_opacity(0).set_color(GoodOrange))
                tickanimation = MoveAlongPath(clocklinetipB, tickarc_i, run_time=rate*gamma/2)
                clockanimationlist.append(tickanimation)

                
            # tickcircleN = Arc(radius=2.9, start_angle=PI/2-startN*PI/6, angle=-np.abs(startN-N)*PI/6).set_opacity(0)
            # clockanimation = MoveAlongPath(clocklinetip, tickcircleN, rate_func=linear, run_time=np.abs(startN-N)*rate)
            clockanimation = AnimationGroup(*clockanimationlist, lag_ratio=2.2*gamma, run_time=runtime)
            return clockanimation
        

        clock.move_to(planet1.get_center()).shift(RIGHT*2.5+DOWN*1.2)
        clockB.move_to(planet2.get_center()).shift(RIGHT*2.5+DOWN*1.2)

        rocketright = rocket.animate(run_time=4, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0])

        self.play(AnimationGroup(FadeIn(clock), FadeIn(clockB)), run_time=2)
        self.play(AnimationGroup(advance_clock(0,8), advance_clockB(0,8), rocketright))

        self.wait(4)

        bigframecampos = self.camera.frame.get_center()

        ################ Reset the scene ##############
        resets = [rocket, clock, clockB, vlabel, rocketV]
        self.play(FadeOut(*resets), run_time=2)
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        clocklinetip.move_to(clock12.get_center())
        clocklinetipB.move_to(clock12B.get_center())
        clocklineB = always_redraw(lambda:Line(clockimgB.get_center(), clocklinetipB.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)
        clockB=Group(clockbgB, clockimgB, clocklineB, clock12B, clockcenterB, clocklinetipB)

        planetAv = always_redraw(lambda: Arrow(start=planet1.get_left(), end=planet1.get_left()+LEFT*0.8, buff=0.01)).set_color(propercolor)
        Avlabel = always_redraw(lambda: MathTex("v").next_to(planetAv.get_left())).set_color(propercolor)

        planetBv = always_redraw(lambda: Arrow(start=planet2.get_left(), end=planet2.get_left()+LEFT*0.8, buff=0.01)).set_color(propercolor)
        Bvlabel = always_redraw(lambda: MathTex("v").next_to(planetBv.get_left())).set_color(propercolor)

        self.wait()
        self.play(FadeIn(rocket), FadeIn(clock), FadeIn(clockB))
        self.wait(3)
        self.play(self.camera.frame.animate(run_time=3).move_to([planet1.get_x(), self.camera.frame.get_y(),0]).scale(0.8))
        rocketframe = AnimationGroup(rocketright,advance_clock(0,6, gamma=4/3, runtime=4), advance_clockB(0,6, gamma=4/3, runtime=4),
            self.camera.frame.animate(run_time=4, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0]))

        self.play(rocketframe)
        self.wait(2)
        tbpiswat = MathTex("t_b = ?").next_to(rocket.get_right()).shift(RIGHT).scale(1.9).set_color(phighlight)
        self.play(Write(tbpiswat))

        self.wait(2)

        ##################### Show length contractions ############
        # Reseting again:
        # show length contraction, show that the clock really shows 6 on this frame too.
        # Then be quantiative about it, show the L/v and L/vgamma
        resets = [rocket, clock, clockB, tbpiswat]
        self.play(FadeOut(*resets), run_time=2)
        self.play(self.camera.frame.animate.move_to(bigframecampos).scale(1/0.8),run_time=2)  # camchange back
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        clocklinetip.move_to(clock12.get_center())
        clocklinetipB.move_to(clock12B.get_center())
        clocklineB = always_redraw(lambda:Line(clockimgB.get_center(), clocklinetipB.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)
        clockB=Group(clockbgB, clockimgB, clocklineB, clock12B, clockcenterB, clocklinetipB)

        self.wait()
        self.play(FadeIn(rocket))
        self.wait(3)
        ################# Talk about how we've only used time dilation and disregarded length contraction + a surprise effect

        question1 = Text("\tHow will the astronaut explain \nwhat they see on B's clock?", should_center=False).set_color(propercolor).scale(1.25)
        question1.move_to(Line(planet1.get_center(), planet2.get_center()).get_center()).shift(UP*15+RIGHT*2)
        self.play(Write(question1),run_time=3)
        self.wait(2.5)
        self.play(question1.animate.shift(UP+LEFT*0.2).scale(1/1.25))

        gottimedilation = Text("Time Dilation", weight=BOLD).set_color(gndhighlight).move_to(question1.get_center()).shift(DOWN*2)
        effect2 = Text("???", weight=BOLD).set_color(phighlight).scale(1.5).move_to(gottimedilation.get_center()).shift(DOWN*2)
        effect3 = Text("???", weight=BOLD).set_color(VibrantGreen).scale(1.5).move_to(effect2.get_center()).shift(DOWN*2)

        getlengthcontraction = Text("Length Contraction", weight=BOLD).set_color(phighlight).move_to(gottimedilation.get_center()).shift(DOWN*2)
        itsrelativityofsimultaneity = Text("Relativity of Simultaneity", weight=BOLD).set_color(VibrantGreen).move_to(effect2.get_center()).shift(DOWN*2)
        andsync = Text("(and synchronization)").set_color(VibrantGreen).set_opacity(0.95).move_to(itsrelativityofsimultaneity.get_center()).shift(DOWN*1.5)

        self.play(FadeIn(gottimedilation), FadeIn(effect2), FadeIn(effect3), run_time=3)
        self.wait(2)
        self.play(ReplacementTransform(effect2, getlengthcontraction), run_time=2)
        self.wait(2)

        self.play(FadeOut(*[question1, gottimedilation, getlengthcontraction, effect3], run_time=2))
        self.wait()


        planetdist0 = np.abs(planet2.get_x() - planet1.get_x())
        planet1pos0 = planet1.get_center()
        planet2pos0 = planet2.get_center()

        self.play(rocket.animate.stretch(0.75,dim=0))
        self.play(rocket.animate(run_time=2, rate_func=linear).move_to([planet1.get_x()+planetdist0*1/4, rocket.get_y(),0]))
        self.wait()

        self.play(AnimationGroup(self.camera.frame.animate.move_to([planet1.get_x()+planetdist0*2/8, self.camera.frame.get_y(),0]).shift(LEFT*2).scale(1.13), 
                        AnimationGroup(rocket.animate.stretch(1/0.75, dim=0)),
                        AnimationGroup(planet2.animate(run_time=3).move_to([planet2.get_x()-planetdist0*1/4, planet2.get_y(), 0]).stretch(0.75, dim=0),
                            planet1.animate(run_time=3).stretch(0.75, dim=0).shift(RIGHT*0.25))))
        
        self.play(AnimationGroup(rocket.animate(run_time=4.5, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]), 
            self.camera.frame.animate(run_time=4.5, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0])))

        self.wait(5)


