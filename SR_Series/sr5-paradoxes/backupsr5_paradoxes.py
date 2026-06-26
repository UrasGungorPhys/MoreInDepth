from manim import *
import numpy as np


class MainIntro(MovingCameraScene):
    def construct(self):
        pass


class AnimatedClock(Scene):
    def construct(self):
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

        clockscale = 1
        clockimg = ImageMobject("clock.png").scale(clockscale)
        clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale))
        clockcenter = always_redraw(lambda:Dot(clockimg.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
        clock12 = always_redraw(lambda:Dot(clockimg.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetip = Dot(clock12.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))


        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter)
        clockmove = Group(clockimg, clocklinetip)

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

        
        # self.play(FadeIn(A), FadeIn(B), FadeIn(C))
        # self.play(FadeIn(planetA), FadeIn(planetB))

        n=2  # set to adjust to time
        adjustarc = Arc(radius=2.9*clockscale, start_angle=PI/2-(n-1)*PI/6, 
                                angle=-PI/6, arc_center=clockcenter.get_center())
        clocklinetip.move_to(adjustarc.get_end())
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter)

        
        self.play(FadeIn(clock),run_time=1)
        self.play(AnimationGroup(advance_clock(2, 6, gamma=4/3)))
        self.wait(5)


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
        for i in range(1100):
            xs = np.random.uniform(-10,26)
            ys = np.random.uniform(-10,10)
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

        rocketright = rocket.animate(run_time=8, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0])

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
        rocketframe = AnimationGroup(rocketright,advance_clock(0,6, gamma=4/3), advance_clockB(0,6, gamma=4/3),
            self.camera.frame.animate(run_time=8, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0]))

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
        question1.move_to(Line(planet1.get_center(), planet2.get_center()).get_center()).shift(UP*6+RIGHT*2)
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

        ################ Reset yet again ###############

        self.play(AnimationGroup(FadeOut(rocket), planet1.animate.stretch(1/0.75, dim=0), planet2.animate.stretch(1/0.75, dim=0)))
        self.play(AnimationGroup(planet1.animate.move_to(planet1pos0), planet2.animate.move_to(planet2pos0),
                  self.camera.frame.animate.move_to(bigframecampos).scale(1/1.13)))
        
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        self.play(FadeIn(rocket))
        self.wait(5)

        # time to make things quantiative
        
        dist_planets = Line(Dot(planet1.get_center()).shift(UP*0.2).get_center(), 
                             [planet2.get_x(), Dot(planet1.get_center()).shift(UP*0.2).get_y(), 0]).set_color(propercolor)
        
        brace_label = MathTex("L").next_to(dist_planets.get_center(), DOWN*1.5).scale(2).set_color(propercolor)

        self.play(Create(dist_planets), FadeIn(brace_label))
        self.wait(3)

        rocketV = always_redraw(lambda: Arrow(start=rocket.get_right(), end=rocket.get_right()+RIGHT*0.8, buff=0.01)).set_color(propercolor)
        vlabel = always_redraw(lambda: MathTex("v").next_to(rocketV.get_right())).set_color(propercolor)

        self.play(FadeIn(rocketV), FadeIn(vlabel))
        self.play(rocket.animate(run_time=1.5).stretch(0.75, dim=0))
        self.play(rocket.animate(run_time=4).move_to([planet2.get_x(), rocket.get_y(),0]))
        self.play(AnimationGroup(rocket.animate(run_time=0.3).stretch(1/0.75, dim=0), FadeOut(*[rocketV, vlabel])))

        tb = MathTex(r"\Delta t_b = \frac{L}{v}").next_to(planet2.get_bottom(), DOWN).scale(1.5).set_color(gndhighlight)
        ta = MathTex(r"\Delta t_a = \frac{L}{v}").next_to(planet1.get_bottom(), DOWN).scale(1.5).set_color(gndcolor1)   

        self.play(Write(tb), Write(ta))
        self.wait(3)
        self.play(FadeOut(*[dist_planets, brace_label]))
        self.wait(2)

        tp = MathTex(r"\Delta t' =  \frac{\Delta t_b}{\gamma}").next_to(rocket.get_bottom()).shift(DOWN+LEFT).scale(1.9).set_color(phighlight)
        tplv = MathTex(r"\Delta t' =  \frac{L}{v\gamma}").next_to(rocket.get_bottom()).shift(DOWN+LEFT).scale(1.9).set_color(phighlight)
        self.play(Write(tp))
        self.wait(3)
        self.play(Transform(tp, tplv))
        self.wait(2)


        ############# This should be the last reset ##############
        self.play(FadeOut(*[rocket, tb, tp, ta]))
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        self.wait(3)
        

        self.play(AnimationGroup(planet2.animate(run_time=3).move_to([planet2.get_x()-planetdist0*1/4, planet2.get_y(), 0]).stretch(0.75, dim=0),
                            planet1.animate(run_time=3).stretch(0.75, dim=0).shift(RIGHT*0.25)), lag_ratio=0.1)
        self.play(FadeIn(rocket), run_time=1.5)
        self.wait(2)
        dist_planetscontracted = Line(Dot(planet1.get_center()).shift(UP*0.2).get_center(), 
                                       [planet2.get_x(), Dot(planet1.get_center()).shift(UP*0.2).get_y(), 0]).set_color(SkyBlue)
        
        brace_labelcontracted = MathTex("L/\gamma").next_to(dist_planetscontracted.get_center(), DOWN*2.5).scale(2).set_color(SkyBlue)

        planet1V = Arrow(start=planet1.get_left(), end=planet1.get_left()+LEFT*0.8, buff=0.01).set_color(propercolor)
        planet2V = Arrow(start=planet2.get_left(), end=planet2.get_left()+LEFT*0.8, buff=0.01).set_color(propercolor)
        
        planet1vlabel = MathTex("v").next_to(planet1V.get_left()).shift(UP*0.3).set_color(propercolor)
        planet2vlabel = MathTex("v").next_to(planet2V.get_left()).shift(UP*0.3).set_color(propercolor)

        self.play(Create(dist_planetscontracted), FadeIn(brace_labelcontracted), run_time=2)
        self.play(FadeIn(planet1V), FadeIn(planet2V), FadeIn(planet1vlabel),FadeIn(planet2vlabel), run_time=2)
        self.play(self.camera.frame.animate(run_time=3).move_to([rocket.get_x(), self.camera.frame.get_y(), 0]).scale(0.8))
        self.wait(2)
        self.play(AnimationGroup(AnimationGroup(rocket.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]), 
        self.camera.frame.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0])),lag_ratio=0.1))

        tpp = MathTex(r"\Delta t' =  \frac{L/\gamma}{v}").next_to(rocket.get_bottom()).shift(DOWN+LEFT).scale(1.9).set_color(phighlight)
        tbp = MathTex(r"\Delta t' = \frac{L}{v\gamma}").next_to(planet2.get_bottom(), DOWN).scale(1.5).set_color(gndhighlight)
        tap = MathTex(r"\Delta t' = \frac{L}{v\gamma}").next_to(planet1.get_bottom(), DOWN).scale(1.5).set_color(gndhighlight)
        tplvp = MathTex(r"\Delta t' =  \frac{L}{v\gamma}").next_to(rocket.get_bottom()).shift(DOWN+LEFT).scale(1.9).set_color(phighlight)

        timedil = Text("Time Dilation", weight=BOLD).set_color(gndhighlight).move_to(Line(tap, tbp).get_center()).scale(1.15).shift(DOWN*0.4)
        lengthcont = Text("Length \nContraction", weight=BOLD, should_center=True).set_color(phighlight).move_to(tplvp).shift(RIGHT*6).scale(1.15)

        self.play(AnimationGroup(FadeOut(*[planet1V, planet2V, planet1vlabel, planet2vlabel]), self.camera.frame.animate(run_time=2).move_to(bigframecampos).scale(1.2/0.8)))
        self.wait(2)
        self.play(Write(tpp), run_time=2)
        self.wait(2)
        self.play(Transform(tpp, tplvp), run_time=2)
        self.play(AnimationGroup(Write(tbp), Write(tap)), run_time=2)
        self.play(AnimationGroup(Write(timedil), Write(lengthcont)), run_time=2)
        self.wait(4)
        self.play(FadeOut(*[dist_planetscontracted, brace_labelcontracted]))
        self.play(FadeOut(*[tbp, tap, tpp]))
        self.play(FadeOut(*[timedil, lengthcont]))
 
        self.wait(5)
        ############# NOpe, just one more! ############################ Show how length contraction + time dilation means theres a gamma^2
        self.play(AnimationGroup(FadeOut(rocket), planet1.animate.stretch(1/0.75, dim=0), planet2.animate.stretch(1/0.75, dim=0)))
        self.play(AnimationGroup(planet1.animate.move_to(planet1pos0), planet2.animate.move_to(planet2pos0),
                  self.camera.frame.animate.scale(1/1.2)))
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        
        
        # first replay the initial animation, moving along with rocket, no length contraction

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
        self.wait(2)
        self.play(self.camera.frame.animate(run_time=3).move_to([planet1.get_x(), self.camera.frame.get_y(),0]).scale(0.8))

        self.play(AnimationGroup(rocket.animate(run_time=8, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]),
                                 advance_clock(0,6, gamma=4/3), advance_clockB(0,6, gamma=4/3),
            self.camera.frame.animate(run_time=8, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0])))
        self.wait(2)


        # reset again here!
        resets = [rocket, clock, clockB]
        self.play(FadeOut(*resets), run_time=2)
        self.play(self.camera.frame.animate.move_to(bigframecampos).scale(1/0.8),run_time=2)  # camchange back
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        clocklinetip.move_to(clock12.get_center())
        clocklinetipB.move_to(clock12B.get_center())
        clocklineB = always_redraw(lambda:Line(clockimgB.get_center(), clocklinetipB.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)
        clockB=Group(clockbgB, clockimgB, clocklineB, clock12B, clockcenterB, clocklinetipB)

        # reset complete 

        self.play(FadeIn(rocket))
        self.wait(2)

        self.play(AnimationGroup(planet2.animate(run_time=2).move_to([planet2.get_x()-planetdist0*1/4, planet2.get_y(), 0]).stretch(0.75, dim=0),
                            planet1.animate(run_time=2).stretch(0.75, dim=0).shift(RIGHT*0.25)))
        
        self.wait(2)
        dist_planetscontracted = Line(Dot(planet1.get_center()).shift(UP*0.2).get_center(), 
                                       [planet2.get_x(), Dot(planet1.get_center()).shift(UP*0.2).get_y(), 0]).set_color(SkyBlue)
        
        brace_labelcontracted = MathTex("L/\gamma").next_to(dist_planetscontracted.get_center(), DOWN*2.5).scale(2).set_color(SkyBlue)

        planet1V = Arrow(start=planet1.get_left(), end=planet1.get_left()+LEFT*0.8, buff=0.01).set_color(propercolor)
        planet2V = Arrow(start=planet2.get_left(), end=planet2.get_left()+LEFT*0.8, buff=0.01).set_color(propercolor)
        
        planet1vlabel = MathTex("v").next_to(planet1V.get_left()).shift(UP*0.4).set_color(propercolor)
        planet2vlabel = MathTex("v").next_to(planet2V.get_left()).shift(UP*0.4).set_color(propercolor)

        self.play(Create(dist_planetscontracted), FadeIn(brace_labelcontracted))
        
        self.play(self.camera.frame.animate(run_time=3).move_to([rocket.get_x(), self.camera.frame.get_y(), 0]).scale(0.8))
        self.play(FadeIn(planet1V), FadeIn(planet2V), FadeIn(planet1vlabel),FadeIn(planet2vlabel))
        self.play(AnimationGroup(AnimationGroup(rocket.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]), 
        self.camera.frame.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), self.camera.frame.get_y(),0])),lag_ratio=0.1))
        self.play(FadeOut(*[planet1V, planet2V, planet1vlabel, planet2vlabel]))

        self.wait(3)


        # Reset again here!

        self.play(FadeOut(*[dist_planetscontracted, brace_labelcontracted]))
        self.play(AnimationGroup(FadeOut(rocket), planet1.animate.stretch(1/0.75, dim=0), planet2.animate.stretch(1/0.75, dim=0)))
        self.play(AnimationGroup(planet1.animate.move_to(planet1pos0), planet2.animate.move_to(planet2pos0),
                  self.camera.frame.animate.scale(1/0.8).move_to(bigframecampos)))
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])

        self.wait(5)
        self.play(FadeIn(rocket), FadeIn(clock), FadeIn(clockB))
        
        self.play(AnimationGroup(self.camera.frame.animate(run_time=3).move_to([rocket.get_x(), self.camera.frame.get_y(), 0]).scale(0.8),
            planet2.animate(run_time=3).move_to([planet2.get_x()-planetdist0*1/4, planet2.get_y(), 0]).stretch(0.75, dim=0),
            clockB.animate(run_time=3).move_to([clockB.get_x()-planetdist0*1/4, clockB.get_y(), 0]),
                            planet1.animate(run_time=3).stretch(0.75, dim=0).shift(RIGHT*0.25)), lag_ratio=0.1)
        
        self.play(AnimationGroup(advance_clock(0, 4, gamma=(4/3)**2, halftick=True, runtime=6), advance_clockB(0, 4, gamma=(4/3)**2, halftick=True, runtime=6),
                rocket.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]), 
        self.camera.frame.animate(run_time=6, rate_func=linear).move_to([self.camera.frame.get_x()+planetdist0*0.75, self.camera.frame.get_y(),0])))
        self.wait()
        self.play(self.camera.frame.animate(run_time=3).move_to(bigframecampos).scale(1/0.8).shift(LEFT))
        self.wait(2)

        tbp1 = MathTex(r"\Delta t_b = \frac{\Delta t_s}{\gamma}").next_to(planet2.get_top(), UP).scale(1.5).set_color(phighlight)
        tap1 = MathTex(r"\Delta t_a = \frac{\Delta t_s}{\gamma}").move_to([planet1.get_x(), tbp1.get_y(), 0]).scale(1.5).set_color(phighlight)

        tpp2 = MathTex(r"\Delta t_s =  \frac{L}{v\gamma}").next_to(rocket.get_right()).shift(RIGHT).scale(1.9).set_color(phighlight)

        tbp2 = MathTex(r"\Delta t = \frac{\Delta t_s}{\gamma} = \frac{L}{v\gamma^2}").next_to(planet2.get_top(), UP).scale(1.5).set_color(phighlight)
        tap2 = MathTex(r"\Delta t = \frac{\Delta t_s}{\gamma} = \frac{L}{v\gamma^2}").move_to([planet1.get_x(), tbp1.get_y(), 0]).scale(1.5).set_color(phighlight)

        self.play(Write(tbp1), Write(tap1))
        self.wait(2)
        self.play(Write(tpp2))
        self.wait(2)
        self.play(AnimationGroup(Transform(tbp1, tbp2),Transform(tap1, tap2)))
        self.wait(5)

        ############# ONE LAST RESET TO DEMONSTRATE THE CORRECT ANIMATION ##################
    
        self.play(AnimationGroup(FadeOut(*[rocket, clock, clockB, tbp1, tap1, tpp2]), 
                                 planet1.animate.stretch(1/0.75, dim=0), planet2.animate.stretch(1/0.75, dim=0)))
        self.play(AnimationGroup(planet1.animate.move_to(planet1pos0), planet2.animate.move_to(planet2pos0),
                                 self.camera.frame.animate(run_time=2).move_to(bigframecampos)))
        
        rocket.move_to([planet1.get_x(), rocket.get_y(),0])
        clocklinetip.move_to(clock12.get_center())
        clocklinetipB.move_to(clock12B.get_center())
        clocklineB = always_redraw(lambda:Line(clockimgB.get_center(), clocklinetipB.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)
        clockB=Group(clockbgB, clockimgB, clocklineB, clock12B, clockcenterB, clocklinetipB)
        clock.move_to(planet1.get_center()).shift(RIGHT*2.5+DOWN*1.2)
        clockB.move_to(planet2.get_center()).shift(RIGHT*2.5+DOWN*1.2)


        self.wait(2)
        self.play(FadeIn(rocket), FadeIn(clock), FadeIn(clockB))
        gottimedilation.move_to(rocket.get_right()).shift(RIGHT*5+UP)
        getlengthcontraction.move_to(gottimedilation.get_center()).shift(DOWN*1.2)
        effect3.scale(0.8).move_to(getlengthcontraction.get_center()).shift(DOWN*1.2)
        itsrelativityofsimultaneity.move_to(effect3.get_center()).shift(DOWN*0.5)
        andsync.move_to(itsrelativityofsimultaneity.get_center()).shift(DOWN)

        self.play(FadeIn(gottimedilation), FadeIn(getlengthcontraction), FadeIn(effect3), run_time=2)
        self.wait()
        self.play(Indicate(effect3))
        self.wait()
        set_clockB_arc = Arc(radius=2.9*clockscale, start_angle=PI/2, 
                                angle=-3.5*PI/6, arc_center=clockcenterB.get_center()).set_opacity(0).set_color(BLACK)
        
        self.play(Transform(effect3, set_clockB_arc.copy(), run_time=2))
        self.play(MoveAlongPath(clocklinetipB, set_clockB_arc), run_time=1.5)
        self.wait(2)
        self.play(Write(itsrelativityofsimultaneity), run_time=3)
        self.play(Write(andsync))
        self.wait(5)

        ############# END OF INTRO? ###########
        ##### Result animation:
        self.play(FadeOut(*[gottimedilation, getlengthcontraction, effect3, andsync, itsrelativityofsimultaneity]))


        self.play(AnimationGroup(planet2.animate(run_time=3).move_to([planet2.get_x()-planetdist0*1/4, planet2.get_y(), 0]).stretch(0.75, dim=0),
            clockB.animate(run_time=3).move_to([clockB.get_x()-planetdist0*1/4, clockB.get_y(), 0]),
                            planet1.animate(run_time=3).stretch(0.75, dim=0).shift(RIGHT*0.25)), lag_ratio=0.1)
        
        self.play(AnimationGroup(advance_clock(0, 4, gamma=(4/3)**2, halftick=True, runtime=6),advance_clockB(3, 8, halftick0=True, gamma=(4/3)**2, runtime=6) ,
                rocket.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), rocket.get_y(),0]), 
        self.camera.frame.animate(run_time=6, rate_func=linear).move_to([planet2.get_x(), 
                                                                         self.camera.frame.get_y(),0]).scale(0.7).shift(DOWN*0.5)))
        self.wait(10)
        

class PlanetsSpaceship(MovingCameraScene):

    #TODO: 
    # Fix some of the highlights for the equations, fix timings
    # Do same for the last resolution equations
    # Illustrate the last projection better, show how L/vgamma^2 ticks on B's clock in spaceship frame.

    def construct(self):
        ll = 6  # axis length
        llx = 0.6*12
        axl = 10
        axlx = 12
        axr = [0,axlx,1]  # axis coordinate range
        ayr = [0,axl,1]
        normy = ll/axl
        normx = llx/axlx

        xhat = np.array([1,0,0])
        yhat= np.array([0,1,0])
        pcolor=BLUE_C
        self.camera.background_color = ManimColor.from_hex("#171717")

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

        def get_line_intersection(line1, line2):
            p1, p2 = line1.get_start(), line1.get_end()
            p3, p4 = line2.get_start(), line2.get_end()

            # Direction vectors
            d1 = p2 - p1
            d2 = p4 - p3

            # Solve for intersection using determinant
            matrix = np.array([d1[:2], -d2[:2]]).T
            if np.linalg.det(matrix) == 0:
                return None  # Lines are parallel or coincident

            b = p3[:2] - p1[:2]
            t_vals = np.linalg.solve(matrix, b)

            # Optional: check if intersection is within segments (0 ≤ t ≤ 1)
            if not (0 <= t_vals[0] <= 1 and 0 <= t_vals[1] <= 1):
                return None  # Intersection is outside segment

            intersection = p1 + t_vals[0] * d1
            return intersection
        

        def homemade_grid(axes, xrange, yrange, colorchoice, opacitychoice=0.3):

            xmin = xrange[0]
            xmax = xrange[1]
            ymin = yrange[0]
            ymax = yrange[1]

            xhat = np.array([Dot(axes.c2p(1,0)).get_x() - Dot(axes.c2p(0,0)).get_x(),0,0])
            yhat = np.array([0, Dot(axes.c2p(0,1)).get_y() - Dot(axes.c2p(0,0)).get_y(),0])

            # testpts = VGroup()
            # for i in range(10):
            #     testpti = Dot(axes.c2p(0,0) + xhat*i)
            #     testpts.add(testpti)

            xgrids = VGroup()

            for i in range(xmin+1, xmax):

                if i == 0:
                    continue

                linex_i = Line(axes.c2p(i, ymin), axes.c2p(i, ymax),stroke_width=2).set_color(colorchoice).set_opacity(opacitychoice)
                xgrids.add(linex_i)


            ygrids = VGroup()

            for i in range(ymin+1, ymax):

                if i == 0:
                    continue

                liney_i = Line(axes.c2p(xmin, i), axes.c2p(xmax, i),stroke_width=2).set_color(colorchoice).set_opacity(opacitychoice)
                ygrids.add(liney_i)

            gridgroup = VGroup(xgrids, ygrids)

            return gridgroup

        ################################ Setting up the spacetime diagram ###########################################
        
        planets_frame = Axes(x_range=axr, y_range=ayr, x_length=llx, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        planets_label = planets_frame.get_axis_labels(x_label="x", y_label="t_A").set_color(gndcolor2)

        # planets_grid = NumberPlane(x_range=[1,axlx,1], y_range=[1,axl,1], x_length=llx, y_length=ll,
        # background_line_style={"stroke_color": gndcolor2,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,})

        planets_grid = homemade_grid(planets_frame, xrange=[0,axlx], yrange=[0,axl], colorchoice=gndcolor2)
        og = planets_frame.c2p(0,0)
        light_line = DashedLine(start=og, end=planets_frame.c2p(axl,axl)).set_color(lightcolor)
        light_label = MathTex("x=ct").next_to(light_line.get_end()).set_color(lightcolor)


        rocket = ImageMobject("rocket.png").scale(0.17).move_to(og)
        planet1 = ImageMobject("planet1.png").scale(0.3).to_edge(DOWN, buff=1)
        planet2 = ImageMobject("planet2.png").scale(0.4).to_corner(RIGHT+DOWN, buff=1).shift(RIGHT*10)
        planetAdot = Dot(og, radius=0.15).set_color(GoodOrange)
        planetA = planet1.move_to(og).scale(0.3)
        Alabel = MathTex("A").next_to(planetA.get_center(), DOWN).shift(DOWN*0.07)
        bpos = planets_frame.c2p(7,0)  # position of planet B
        planetBdot = Dot(bpos, radius=0.15).set_color(Mustard)
        planetB = planet2.move_to(bpos).scale(0.3)
        Blabel = MathTex("B").next_to(planetB.get_center(), DOWN).shift(DOWN*0.07)
        arrivaldot = Dot(planets_frame.c2p(7,9))

        # set v,gamma for spaceship
        v=0.78
        gamma = 1/np.sqrt(1-v**2)

        xphat = np.array([1,v,0])/np.linalg.norm(np.array([1,v,0]))
        tphat = np.array([v,1,0])/np.linalg.norm(np.array([v,1,0]))

        nxphat = np.array([-1,-v,0])/np.linalg.norm(np.array([1,v,0]))
        ntphat = np.array([v,1,0])/np.linalg.norm(np.array([v,1,0]))

        xp = Arrow(start=og, end=og + xphat*8, buff=0).set_color(pcolor1)
        tp = Arrow(start=og, end=og + tphat*8, buff=0).set_color(pcolor1)

        arrivalpt = planets_frame.c2p(7,9)
        arrivalptdot = Dot(arrivalpt).set_color(propercolor)
        tpa = Line(start=og, end=arrivalpt, buff=0) #tp axis up to the arrival point, to move rocket

        trace_rocket = TracedPath(rocket.get_center, stroke_color=pcolor2)
        xvtlabel = MathTex("x=vt").next_to(tp.get_end(), UP).set_color(pcolor2).shift(DOWN*0.03+RIGHT*0.1)
        xvtlabelxp = MathTex(r"x=vt \implies x' = 0").next_to(tp.get_end(), UP).set_color(pcolor).shift(DOWN*0.03+RIGHT*0.1)
        xp0 = MathTex("x' = 0").next_to(tp.get_end(), UP).set_color(pcolor2).shift(DOWN*0.03+RIGHT*0.1)
        tplabel = MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2).shift(DOWN*0.03+RIGHT*0.1)

        xplabel0 = MathTex("x'").next_to(xp.get_end(),DOWN).set_color(pcolor2)
        tp0 = MathTex("t' = 0").next_to(xp.get_end(),DOWN).set_color(pcolor2).shift(RIGHT*0.5)
        xplabel = MathTex("x'").next_to(xp.get_end(),DOWN).set_color(pcolor2)

        arrival_t = DashedLine(start=planets_frame.c2p(7,9), end=planets_frame.c2p(0,9)).set_color(gndcolor2)
        arrival_x = DashedLine(start=planets_frame.c2p(7,9), end=bpos).set_color(gndcolor2)

        arrival_tl = Line(start=planets_frame.c2p(7,9), end=planets_frame.c2p(0,9)).set_color(gndcolor2)

        tAB = MathTex(r"\frac{L}{v}").next_to(planets_frame.c2p(0,9), LEFT).scale(0.9).shift(LEFT*0.1).set_color(gndcolor2)

        arrivalprime0 = MathTex(r"(x', t')").move_to(arrivalpt).shift(LEFT*0.7 + UP*0.6).set_color(pcolor2)
        arrivalprime1 = MathTex(r"(x', t') = (0, \frac{L}{v\gamma})").move_to(arrivalpt).shift(LEFT*1.6 + UP*0.6).set_color(pcolor2)
        arrivalprime2 = MathTex(r"t' = \frac{L}{v\gamma}").move_to(arrivalpt).shift(LEFT*0.9 + UP*0.6).set_color(pcolor2)
        arrivalprime3 = MathTex(r"t' = \frac{L}{v\gamma}").move_to(arrivalpt).shift(LEFT*0.6 + UP*0.55).scale(0.7).set_color(pcolor2)

    
        self.play(Create(planets_frame))
        self.play(FadeIn(planets_grid))
        self.wait(2)
        self.play(FadeIn(planetA))
        self.play(FadeIn(planetB))
        self.play(FadeIn(Alabel), FadeIn(Blabel))
        self.play(FadeIn(planets_label))
        self.wait(2)
        self.play(Create(light_line), FadeIn(light_label))
        self.wait(4)
        self.play(FadeIn(rocket))
        self.wait(1)
        self.add(trace_rocket)
        self.play(MoveAlongPath(rocket, tpa), run_time=5)
        self.wait(3)
        self.play(Create(arrival_t), Create(arrival_x))
        self.wait(5)
        self.play(FadeOut(planetA), FadeOut(planetB), FadeOut(rocket), light_label.animate.set_opacity(0.75), light_line.animate.set_opacity(0.75))
        self.play(Create(planetAdot), Create(planetBdot), Create(arrivaldot))
        self.wait(5)

        self.play(Create(tp), run_time=3)
        self.play(Write(xvtlabel), FadeOut(trace_rocket))
        self.wait(2)
        self.play(ShowPassingFlash(arrival_tl))
        self.play(Write(tAB))
        self.wait(3)
        self.play(ShowPassingFlash(tp.copy().set_stroke(WHITE)))
        self.play(Indicate(tp, color=WHITE))
        self.wait(5)
        self.play(Indicate(xvtlabel, color=WHITE))
        self.wait(2)
        self.play(TransformMatchingTex(xvtlabel, xvtlabelxp), run_time=2)
        self.wait(2)
        self.play(Transform(xvtlabelxp, xp0))
        self.wait(2)
        self.play(Transform(xvtlabelxp, tplabel))
        self.wait(2)
        self.play(Indicate(arrivalptdot))
        self.wait(2)
        self.play(Write(arrivalprime0))
        self.wait(2)
        self.play(Transform(arrivalprime0, arrivalprime1))
        self.wait(2)
        self.play(Transform(arrivalprime0, arrivalprime2))
        self.wait(3)
        self.play(Transform(arrivalprime0, arrivalprime3))
        self.wait(5)

    ############################################## Setup complete ####################################################

        ptint = Dot(get_line_intersection(xp, arrival_x)).set_color(pcolor1)
        ptintlabel = MathTex("t'=0").next_to(ptint.get_center(), RIGHT).set_color(pcolor2)
        ptint_t = DashedLine(start=ptint.get_center(), 
                             end=[planetA.get_x(), ptint.get_y(), 0]).set_color(gndcolor2)
        ptint_tl = Line(start=ptint.get_center(), 
                             end=[planetA.get_x(), ptint.get_y(), 0]).set_color(gndcolor2)
        
        lv_c2 = MathTex(r"\frac{Lv}{c^2}").next_to(ptint_t.get_end(), LEFT).set_color(gndhighlight)
        Bcoords = MathTex("(x, t) = (L, 0)").next_to(bpos, UP+RIGHT*0.1).scale(0.9).set_color(gndcolor2)
        # xptpcoords = MathTex(r"(x',t') = (x', 0)").next_to(ptint.get_right(), RIGHT)

        # show these as review
        LorentzTransform1 = MathTex(r"x' = \gamma (x-vt)").move_to(light_label.get_right()).shift(RIGHT*4).set_color(highlight).scale(1.3)
        LorentzTransform2 = MathTex(r"t' = \gamma \left(t - \frac{v}{c^2}x\right)").move_to(LorentzTransform1).shift(DOWN*2).set_color(highlight).scale(1.3)
        LorentzTransform3 = MathTex(r"x = \gamma (x'+vt')").move_to(LorentzTransform2).shift(DOWN*2).set_color(highlight).scale(1.3)
        LorentzTransform4 = MathTex(r"t = \gamma \left(t' + \frac{v}{c^2}x'\right)").move_to(LorentzTransform3).shift(DOWN*2).set_color(highlight).scale(1.3)

        LorentzTransforms = [LorentzTransform1, LorentzTransform2, LorentzTransform3, LorentzTransform4]

        LT1 = Arrow(start=bpos, end=ptint.get_center()).set_color(phighlight)
        LT2 = Arrow(start=ptint.get_center(), end=[og[0], ptint.get_y(),0]).set_color(gndhighlight)
        LTs = VGroup(LT1, LT2)
        LTeq = MathTex("t' ",  r"= \gamma \left(t - \frac{v}{c^2}x\right)").move_to(ptint_t.get_center()).shift(DOWN).set_color(propercolor)
        LTmainpos = LTeq.get_center()
        LTeq1 = MathTex("0 ",  r"= \gamma", r"\left(t - \frac{v}{c^2}x\right)").move_to(LTmainpos).shift(DOWN*1.3).set_color(propercolor)
        LTeq[0].set_color(phighlight)
        LTeq1[0].set_color(phighlight)
        LTeq1ghost = LTeq1.copy().set_opacity(0.35)
        LTeq2 = MathTex(r"t - \frac{v}{c^2}","x = 0").move_to(LTmainpos).set_color(propercolor)
        LTeq3 = MathTex(r"t - \frac{v}{c^2}","L",  " = 0").move_to(LTmainpos).shift(DOWN*1.3).set_color(propercolor)
        LTeq3ghost = LTeq3.copy().set_opacity(0.35)
        LTeq4 = MathTex(r"t = \frac{Lv}{c^2}").move_to(LTmainpos).set_color(propercolor)
        
        simlineB = Arrow(start=bpos, end=bpos -xphat*15, buff=0).set_color(pcolor1)
        negtp = Arrow(start=og, end=og - tphat*12, buff=0).set_color(pcolor1)

        tbpzero = Dot(get_line_intersection(simlineB, negtp)).set_color(gndhighlight)

        reduce_opacity = [xp, tp, light_line, planets_grid, xplabel, tplabel, ptint_t, tAB,arrival_x, arrival_t, arrivalprime0, light_label]

        self.play(Create(xp), FadeIn(xplabel), run_time=3)
        self.wait(3)
        self.play(Transform(xplabel, tp0))
        self.wait(2)
        self.play(Transform(xplabel, xplabel0))
        self.wait(2)
        self.play(ShowPassingFlash(xp.copy().set_stroke(WHITE), run_time=1.5))
        self.wait(2)
        self.play(Create(ptint))
        self.wait(2)
        self.play(Write(ptintlabel))
        self.wait(2)
        self.play(Create(ptint_t))
        self.wait(2)
        self.play(ShowPassingFlash(ptint_tl.copy().set_stroke(WHITE)), run_time=1)
        self.play(Write(lv_c2))
        self.wait(5)
        self.play(Create(LTs), run_time=1.5)
        self.wait(2)
        self.play(self.camera.frame.animate.shift(RIGHT*3.5).scale(1.2))
        self.play(Write(LorentzTransform1))
        self.play(Write(LorentzTransform2))
        self.play(Write(LorentzTransform3))
        self.play(Write(LorentzTransform4))
        self.wait(2)
        self.play(Indicate(LorentzTransform2))
        self.wait(4)
        self.play(FadeOut(*LorentzTransforms))
        self.play(self.camera.frame.animate.shift(LEFT*3.5).scale(1/1.2))
        self.wait(2)
        self.play(*(i.animate.set_opacity(0.2) for i in reduce_opacity))
        self.play(Write(Bcoords), run_time=2)
        self.play(Write(tbpzero), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(LTs, LTeq))
        self.wait(2)
        self.play(Write(LTeq1ghost))
        self.play(ReplacementTransform(ptintlabel, LTeq1[0]))
        self.play(ReplacementTransform(LTeq, LTeq1))
        self.remove(LTeq1ghost)
        self.play(LTeq1.animate.move_to(LTmainpos))
        zerobrace = Brace(LTeq1[2])
        zerobracezero = MathTex("0").next_to(zerobrace.get_center(),DOWN)
        self.play(Create(zerobrace))
        self.play(Write(zerobracezero))
        self.wait(2)
        self.play(FadeOut(zerobrace), FadeOut(zerobracezero))
        self.wait()
        self.play(ReplacementTransform(LTeq1, LTeq2))
        self.play(Write(LTeq3ghost))
        self.play(ReplacementTransform(Bcoords, LTeq3ghost[1]))
        self.play(FadeIn(LTeq3))
        self.play(FadeOut(LTeq2), FadeOut(LTeq1))
        self.remove(LTeq3ghost)
        self.remove(LTeq3ghost[1])
        self.remove(LTeq3ghost[0])
        self.remove(LTeq2[0])
        self.play(ReplacementTransform(LTeq3, LTeq4))

        self.wait(3)

        self.wait(4)
        self.play(FadeOut(LTeq4))
        self.play(*(i.animate.set_opacity(1) for i in reduce_opacity))

        self.wait(5)
        self.play(Create(simlineB), Create(negtp), self.camera.frame.animate.scale(2.5).shift(LEFT*3+DOWN*3),run_time=10)
        self.wait(2)
        self.play(Create(tbpzero))
        self.wait(2)

        planets_frame_ext = Axes(x_range=[-24, 24, 1], y_range=[-20,20,1],
         x_length=llx*3, y_length=ll*3,axis_config={"include_ticks": False}).move_to(og).set_color(gndcolor1)

        planets_label_ext = planets_frame_ext.get_axis_labels(x_label="x", y_label="t_A").set_color(gndcolor1)

        # planets_grid_ext = NumberPlane(x_range=[-24, 24, 1], y_range=[-20,20,1], x_length=llx*3, y_length=ll*3,
        # background_line_style={"stroke_color": gndcolor2,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,}).move_to(og)

        planets_grid_ext = homemade_grid(planets_frame_ext, xrange=[-24,24], yrange=[-20,20], colorchoice=gndcolor2)
        newlabelsax = planets_frame_ext.get_axis_labels(x_label="x", y_label="t_A").set_color(gndcolor2)

        self.play(FadeOut(planets_frame), FadeOut(planets_grid))
        self.play(Create(planets_frame_ext),Create(planets_grid_ext), Transform(planets_label, newlabelsax))
        self.wait(4)
        self.play(self.camera.frame.animate.scale(1/2.5).shift(RIGHT*3 + UP*3), run_time=5)
        self.wait(3)

        # Resolve the paradox
        deltparrow = Arrow(start=og, end=arrivalptdot, buff=0, stroke_width=7.5).set_color(VibrantPink)
        deltpline = Line(start=og, end=arrivalptdot, buff=0, stroke_width=7.5).set_color(VibrantPink)

        deltbparrow = Arrow(start=ptint, end=arrivalptdot, buff=0, stroke_width=7.5).set_color(VibrantPink2)
        deltbline = Line(start=ptint, end=arrivalptdot, buff=0, stroke_width=7.5).set_color(VibrantPink2)

        deltLTarrow = Arrow(start=og, end=ptint, buff=0, stroke_width=7.5).set_color(VibrantGreen)
        deltLTline = Line(start=og, end=ptint, buff=0, stroke_width=7.5).set_color(VibrantGreen)
        deltbp = MathTex(r"\frac{t'}{\gamma}").move_to(deltbline.get_center()).shift(RIGHT+DOWN).set_color(VibrantPink)
        deltbp1 = MathTex(r"\frac{L/v\gamma}{\gamma}").move_to(deltbline.get_center()).shift(RIGHT+DOWN).set_color(VibrantPink)
        deltbp2 = MathTex(r"\frac{L}{v\gamma^2}").move_to(deltbline.get_center()).shift(RIGHT+DOWN).set_color(VibrantPink)

        self.play(Indicate(tAB))
        self.play(arrivalprime0.animate.scale(1/0.7).set_color(VibrantPink).shift(LEFT+UP*0.2))
        self.play(Create(deltparrow), tAB.animate.set_color(VibrantPink2), run_time=2)
        self.play(Transform(deltparrow, deltpline))
        self.wait(2)
        self.play(Create(deltbparrow), run_time=2)
        self.play(Transform(deltbparrow, deltbline))
        self.wait(2)
        self.play(Create(deltLTarrow), run_time=2)
        self.add(deltLTline)
        self.play(ReplacementTransform(deltLTarrow, deltbp), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(deltbp, deltbp1))
        self.wait(2)
        self.play(ReplacementTransform(deltbp1, deltbp2))
        self.play(self.camera.frame.animate.shift(RIGHT*4).scale(1.35))

        resolveeq1 = MathTex("\Delta t_B = ", r"\frac{L}{v\gamma^2}").move_to(light_label.get_right()).shift(RIGHT*4.5).set_color(VibrantGreen).scale(1.3)
        resolveeq2 = MathTex("t_B  = ", r"\frac{Lv}{c^2}", r"\text{   when }t'=0").next_to(resolveeq1, DOWN*1.25).set_color(VibrantGreen).scale(1.3)

        resolveeq3 = MathTex(r"t_B(\text{arrival})", " = \Delta t_B + t_B (t=0)").next_to(resolveeq2, DOWN*1.25).set_color(VibrantGreen).scale(1.3)
        resolveeq3_1 = MathTex(r"t_B(\text{arrival})", r" = \frac{L}{v\gamma^2} + \frac{Lv}{c^2}").set_color(VibrantGreen).scale(1.3).move_to(resolveeq3).shift(DOWN*1.25)
        resolveeq3_2 = MathTex(r"t_B(\text{arrival})", r" = \frac{L}{v} \left(\frac{1}{\gamma^2} + \frac{v^2}{c^2}\right)").set_color(VibrantGreen).scale(1.3).shift(DOWN*1.25)
        resolveeq3_3 = MathTex(r"t_B(\text{arrival})", r" = \frac{L}{v} \left(\frac{1}{\frac{1}{1 - v^2/c^2}} + \frac{v^2}{c^2}\right)").set_color(VibrantGreen).scale(1.3).shift(DOWN*1.25)
        resolveeq3_4 = MathTex(r"t_B(\text{arrival})", r" = \frac{L}{v} \left(1 - \frac{v^2}{c^2} + \frac{v^2}{c^2}\right)").set_color(VibrantGreen).scale(1.3).shift(DOWN*1.25)
        resolveeq3_5 = MathTex(r"t_B(\text{arrival})", r" = \frac{L}{v}").set_color(VibrantGreen).scale(1.3).shift(DOWN*1.25)

        self.play(Write(resolveeq1))
        self.wait(2)
        self.play(Write(resolveeq2))
        self.wait(3)
        self.play(Write(resolveeq3))
        self.wait(3)
        self.play(Write(resolveeq3_1), run_time=2)
        self.play(resolveeq3_1.animate.move_to(resolveeq3), FadeOut(resolveeq3), run_time=2)
        self.wait(3)

        self.play(Write(resolveeq3_2), run_time=2)
        self.play(resolveeq3_2.animate.move_to(resolveeq3_1), FadeOut(resolveeq3_1), run_time=2)
        self.wait(3)

        self.play(Write(resolveeq3_3), run_time=2)
        self.play(resolveeq3_3.animate.move_to(resolveeq3_2), FadeOut(resolveeq3_2), run_time=2)
        self.wait(3)

        self.play(Write(resolveeq3_4), run_time=2)
        self.play(resolveeq3_4.animate.move_to(resolveeq3_3), FadeOut(resolveeq3_3), run_time=2)
        self.wait(3)

        self.play(Write(resolveeq3_5), run_time=2)
        self.play(resolveeq3_5.animate.move_to(resolveeq3_4), FadeOut(resolveeq3_4), run_time=2)
        self.wait(10)


class RearClockAheadDiagram(MovingCameraScene):

    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")

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
        Emerald = ManimColor.from_hex("#23CE6B")
        FakeRaspberry = ManimColor.from_hex("#F72585")
        MateOrange = ManimColor.from_hex("#E4572E")

        gndcolor1 = SkyBlue
        gndcolor2 = SteelBlue
        gndhighlight = LightBlue
        gndhighlight2 = FernGreen

        pcolor1 = OrangeOrange
        pcolor2=MateOrange
        phighlight = NeonOrange
        phighlight2 = FakeRaspberry

        highlight = Emerald

        propercolor = Samoyed
        lightcolor=Mustard


        def gli(line1, line2):
            p1, p2 = line1.get_start(), line1.get_end()
            p3, p4 = line2.get_start(), line2.get_end()

            # Direction vectors
            d1 = p2 - p1
            d2 = p4 - p3

            # Solve for intersection using determinant
            matrix = np.array([d1[:2], -d2[:2]]).T
            if np.linalg.det(matrix) == 0:
                return None  # Lines are parallel or coincident

            b = p3[:2] - p1[:2]
            t_vals = np.linalg.solve(matrix, b)

            # Optional: check if intersection is within segments (0 ≤ t ≤ 1)
            if not (0 <= t_vals[0] <= 1 and 0 <= t_vals[1] <= 1):
                return None  # Intersection is outside segment

            intersection = p1 + t_vals[0] * d1
            return intersection
        

        def homemade_grid(axes, xrange, yrange, colorchoice, opacitychoice=0.3):

            xmin = xrange[0]
            xmax = xrange[1]
            ymin = yrange[0]
            ymax = yrange[1]

            xhat = np.array([Dot(axes.c2p(1,0)).get_x() - Dot(axes.c2p(0,0)).get_x(),0,0])
            yhat = np.array([0, Dot(axes.c2p(0,1)).get_y() - Dot(axes.c2p(0,0)).get_y(),0])

            # testpts = VGroup()
            # for i in range(10):
            #     testpti = Dot(axes.c2p(0,0) + xhat*i)
            #     testpts.add(testpti)

            xgrids = VGroup()

            for i in range(xmin+1, xmax):

                if i == 0:
                    continue

                linex_i = Line(axes.c2p(i, ymin), axes.c2p(i, ymax),stroke_width=2).set_color(colorchoice).set_opacity(opacitychoice)
                xgrids.add(linex_i)


            ygrids = VGroup()

            for i in range(ymin+1, ymax):

                if i == 0:
                    continue

                liney_i = Line(axes.c2p(xmin, i), axes.c2p(xmax, i),stroke_width=2).set_color(colorchoice).set_opacity(opacitychoice)
                ygrids.add(liney_i)

            gridgroup = VGroup(xgrids, ygrids)

            return gridgroup

        ll = 6  # axis lengths to draw
        axrange = 10  # coordinate ranges
        norm = ll/axrange  # normalize any distance to fit
        pcolor=BLUE_C  # Color to use for the primed axes

        # Stationary axes:

        ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        # grid = NumberPlane(x_range=[1,axrange,1], y_range=[1,axrange,1], 
        # x_length=ll, y_length=ll,
        # background_line_style={"stroke_color": gndcolor2,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,})

        grid = homemade_grid(ax, xrange=[0,axrange], yrange=[0,axrange], colorchoice=gndcolor2)

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange,axrange)).set_color(lightcolor)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange,axrange)).set_color(lightcolor)
        lightlabel = MathTex("x=ct").next_to(xct.get_end(), UR).set_color(lightcolor)

        # Initial axes, to be Lorentz transformed:
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

        xpi = Arrow(start=OG, end=OG+10*xhat, buff=0).set_color(pcolor1)
        tpi = Arrow(start=OG, end=OG+10*that, buff=0).set_color(pcolor1)

        # Initial Lorentz grid
        manual_grids0x = VGroup()
        manual_grids0y = VGroup()
        for i in range(1,10):

            xline = Line(start=OG + i*that,
                         end=OG + i*that + 9.5*xhat, buff=0,
                         stroke_color=pcolor2, stroke_opacity=0.5,stroke_width=2)

            tline = Line(start=OG + i*xhat,
                         end=OG + i*xhat + 9.5*that, buff=0,
                         stroke_color=pcolor2, stroke_opacity=0.5,stroke_width=2)

            manual_grids0x.add(xline)
            manual_grids0y.add(tline)

        # Lorentz axes
        v = 0.25
        gamma = 1/np.sqrt(1-v**2)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0]) 

        xphat = xp_direction
        tphat = tp_direction

        xp = Arrow(start=OG, end=OG + 6.4*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)

        tp = Arrow(start=OG, end=OG + 6.4*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        tplabel = always_redraw(lambda : MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2))

        xct_long = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange+2.5,axrange+2.5)).set_color(lightcolor)
        lightlabel_long = MathTex("x=ct").next_to(xct_long.get_end(), DR).set_color(lightcolor)

        # Lorentz grid

        manual_gridspx = VGroup()
        manual_gridspy = VGroup()
        for i in range(1,10):

            xpline = Line(start=OG + i*tp_direction*norm*1.01,
                         end=OG + i*tp_direction*norm*1.01 + 5.8*xp_direction*1.01, buff=0, 
                         stroke_color=pcolor1, stroke_opacity=0.5,stroke_width=2)


            tpline = Line(start=OG + i*xp_direction*norm*1.01,
                         end=OG + i*xp_direction*norm*1.01 + 5.8*tp_direction*1.01, buff=0,
                         stroke_color=pcolor1, stroke_opacity=0.5,stroke_width=2)

            manual_gridspx.add(xpline)
            manual_gridspy.add(tpline)


        event00 = xct.get_center()
        event0pt = Dot(event00).shift(RIGHT*2+UP).set_color(propercolor)
        event0 = event0pt.get_center()
        event0label = always_redraw(lambda: MathTex("p").next_to(event0pt, RIGHT).set_color(propercolor))

        event0labelsp = MathTex("= (x_p', t_p')").next_to(event0label, RIGHT*2.1).set_color(pcolor2)
        event0labels = MathTex("= (x_p,t_p)").next_to(event0labelsp, DOWN).set_color(gndcolor2)

        event0_prjxp = always_redraw(lambda:Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*50))  # not gonna draw these
        event0_prjtp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center() - tphat*50))
        intersection_tp = gli(event0_prjxp, tp)
        intersection_xp = gli(event0_prjtp, xp)

        event0xp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - tphat*50), xp)).set_color(pcolor1))
        event0tp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*50), tp)).set_color(pcolor1))

        intersection_xppt = always_redraw(lambda: Dot(event0xp.get_end()).set_color(phighlight))
        intersection_tppt = always_redraw(lambda: Dot(event0tp.get_end()).set_color(phighlight))

        xplen = always_redraw(lambda:Line(start=OG, end=event0xp.get_end(), stroke_width=6,buff=0).set_color(phighlight2))
        tplen = always_redraw(lambda:Line(start=OG, end=event0tp.get_end(), stroke_width=6,buff=0).set_color(phighlight2))

        xplenfortransform = Line(start=OG, end=event0xp.get_end(), stroke_width=4,buff=0).set_color(pcolor1)
        tplenfortransform  = Line(start=OG, end=event0tp.get_end(), stroke_width=4,buff=0).set_color(pcolor1)

        xpshift = tplenfortransform.get_end() - tplenfortransform.get_start()
        tpshift = xplenfortransform.get_end() - xplenfortransform.get_start()

        pxplabel = always_redraw(lambda: MathTex("x_p'").next_to(intersection_xppt.get_center(), DOWN).set_color(pcolor2))
        ptplabel = always_redraw(lambda: MathTex("t_p'").next_to(intersection_tppt.get_center(), LEFT).set_color(pcolor2))

        event0x = always_redraw(lambda: DashedLine(start=event0pt.get_center(),end=[event0pt.get_x(),OG[1],0]).set_color(gndcolor2))
        event0t = always_redraw(lambda: DashedLine(start=event0pt.get_center(),end=[OG[0], event0pt.get_y(),0]).set_color(gndcolor2))

        pxdot = always_redraw(lambda: Dot([event0pt.get_x(),OG[1],0]).set_color(gndhighlight))
        ptdot = always_redraw(lambda: Dot([OG[0], event0pt.get_y(),0]).set_color(gndhighlight))

        pxlabel = always_redraw(lambda: MathTex("x_p").next_to(pxdot, DOWN).set_color(gndcolor2))
        ptlabel = always_redraw(lambda: MathTex("t_p").next_to(ptdot, LEFT).set_color(gndcolor2))

        xlen = always_redraw(lambda:Line(start=OG, end=pxdot.get_center(), stroke_width=6,buff=0).set_color(gndhighlight2))
        tlen = always_redraw(lambda:Line(start=OG, end=ptdot.get_center(), stroke_width=6,buff=0).set_color(gndhighlight2))


        # Plays!
        self.play(Create(ax), Create(ax_labels), run_time=3)
        self.play(Create(grid), run_time=2)
        self.bring_to_front(ax)
        self.play(Create(xct), FadeIn(lightlabel))
        self.wait(2)

        self.play(Create(xpi), Create(tpi))
        self.wait(2)
        self.play(Create(manual_grids0x), Create(manual_grids0y),run_time=1)
        self.wait(2)

        self.play(FadeOut(lightlabel))

        self.play(Transform(xpi, xp), Transform(tpi, tp),
                    Transform(manual_grids0x, manual_gridspx),
                    Transform(manual_grids0y, manual_gridspy),
                    Transform(xct, xct_long),
                    self.camera.frame.animate.scale(1.12).shift(UP*0.5+RIGHT),run_time=4)

        self.play(FadeIn(xplabel), FadeIn(tplabel), FadeIn(lightlabel_long.set_opacity(0.8)), run_time=2)
        self.wait(4)
        
        self.play(Indicate(manual_grids0y))
        self.play(Indicate(tpi))
        self.wait(1)

        self.play(Indicate(manual_grids0x))
        self.play(Indicate(xpi))
        self.wait(5)

        self.play(FadeOut(manual_grids0x),FadeOut(manual_grids0y),FadeOut(grid),
                    Transform(xct,xct0.set_opacity(0.4)), FadeOut(lightlabel_long),
                    self.camera.frame.animate.shift(DOWN*0.1+LEFT), run_time=2)

        # Demonstrate projection for event p
        self.wait(1)
        self.play(Create(event0pt))
        self.bring_to_front(event0pt)
        self.wait()
        self.play(Create(event0label))
        self.wait(2)
        self.play(Create(event0labels), Create(event0labelsp))
        self.wait(3)
        self.play(FadeOut(event0labelsp), FadeOut(event0labels))
        self.wait(2)

        # self.play(Create(event0_prjtp),Create(event0_prjxp))  # to check if needed
        self.add(xplenfortransform)
        self.play(ShowPassingFlash(xpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(xplenfortransform.animate.shift(xpshift), run_time=4)  # moving a piece of x' until it intersects the event
        self.wait(2)
        self.play(FadeOut(xplenfortransform))
        self.play(Create(event0tp), run_time=1.5)
        self.wait(1)
        self.play(Create(intersection_tppt))
        self.play(Create(tplen))
        self.bring_to_front(intersection_tppt)
        self.play(Create(ptplabel))

        self.wait(1.5)

        self.add(tplenfortransform)
        self.play(ShowPassingFlash(tpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(tplenfortransform.animate.shift(tpshift),run_time=4)
        self.wait(2)
        self.play(FadeOut(tplenfortransform))
        self.play(Create(event0xp), run_time=1.5)
        self.wait(1)
        self.play(Create(intersection_xppt))
        self.play(Create(xplen))
        self.bring_to_front(intersection_xppt)
        self.play(Create(pxplabel))

        self.wait()
        self.play(FadeIn(manual_gridspx), FadeIn(manual_gridspy))
        self.wait(2)
        self.play(FadeOut(manual_gridspx), FadeOut(manual_gridspy))

        self.wait(3)
        self.play(Create(event0x), Create(event0t),run_time=1)
        self.play(Create(pxdot), Create(ptdot))
        self.wait()
        self.bring_to_front(ax)
        self.play(FadeIn(grid))
        self.bring_to_front(ax)
        self.wait()
        self.play(Create(xlen), Create(tlen))
        self.bring_to_front(pxdot)
        self.bring_to_front(ptdot)
        self.play(Create(pxlabel), Create(ptlabel))
        self.wait()
        self.play(FadeOut(grid))

        self.play(event0pt.animate.shift(RIGHT*0.5), run_time=2)
        self.play(event0pt.animate.shift(LEFT*3 + UP*1.6), run_time=2.5)
        self.play(event0pt.animate.shift(LEFT*1.2 + DOWN*2.6), run_time=1.5)
        self.play(event0pt.animate.shift(RIGHT*1.2 + DOWN*2), run_time=1.5)
        self.play(event0pt.animate.move_to(event0), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(event0label), FadeOut(event0x), FadeOut(event0t), FadeOut(pxdot), FadeOut(ptdot),
        FadeOut(event0xp),FadeOut(event0tp), FadeOut(intersection_tppt), FadeOut(intersection_xppt),
        FadeOut(pxlabel), FadeOut(ptlabel), FadeOut(tlen), FadeOut(xplen), FadeOut(tplen), FadeOut(pxplabel), FadeOut(ptplabel), run_time=2)
        
        self.wait(1)
        self.bring_to_front(event0pt)
        self.play(event0pt.animate.move_to(ax.c2p(8.5,0)))
        self.bring_to_front(event0pt)
        self.play(FadeOut(xlen))
        planetB = ImageMobject("planet2.png").move_to(ax.c2p(8.5,0)).scale(0.12)
        self.wait()
        self.play(FadeOut(event0pt), FadeIn(planetB))
        self.wait(2)
        self.play(Indicate(xpi))
        self.wait(2)

        # Moving onto a larger diagram:
        self.play(self.camera.frame.animate.scale(1.3).move_to(ax.c2p(3,3)), run_time=3)
        self.wait(1)

        negax = Axes(x_range=[-5,axrange,1], y_range=[-5,axrange,1], 
        x_length=ll+3, y_length=ll+3,axis_config={"include_ticks": False}).set_color(gndcolor1)
        negax.shift(OG - negax.c2p(0, 0))  # align origins

        # Draw the negative axes:
        negxp = Arrow(start=OG, end=OG - 3*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        negxplabel = always_redraw(lambda: MathTex("-x'").next_to(negxp.get_end(), LEFT).set_color(pcolor1))

        negtp = Arrow(start=OG, end=OG - 3*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        negtplabel = always_redraw(lambda : MathTex("-t'").next_to(negtp.get_end(), LEFT).set_color(pcolor1))
        

        self.play(Transform(ax, negax))
        self.wait(2)
        self.play(Create(negtp), Create(negtplabel), run_time=2)
        self.bring_to_front(negtp)
        self.wait(1)
        self.play(Create(negxp), Create(negxplabel), run_time=2)
        self.bring_to_front(negxp)
        self.wait(2)
        self.play(FadeOut(planetB), FadeIn(event0pt))

        negprjxp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()+ tphat*15))
        negprjtp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()- xphat*15))

        # get some extra long lines that won't be drawn, to prevent intersection finding error in case I overshoot:
        xplongghost = Arrow(start=OG, end=OG + 10*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        negtplongghost = Arrow(start=OG, end=OG - 3*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)

        worldlineB = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center() + that*9.1)).set_color(propercolor)
        worldlineBlabel = always_redraw(lambda: MathTex("x_B(t)").next_to(worldlineB.get_end(), RIGHT).scale(0.8)).set_color(propercolor)

        along_wlB = Dot(gli(worldlineB, xpi)).set_color(highlight)
        prjx_wlB = always_redraw(lambda: DashedLine(start=along_wlB.get_bottom(), 
                                         end=gli(Line(start=along_wlB.get_center(), end=along_wlB.get_center() - tphat*15), xpi)).set_color(highlight))
        prjt_wlB = always_redraw(lambda: DashedLine(start=along_wlB.get_left(),
                                         end=gli(Line(start=along_wlB.get_center(), end=along_wlB.get_center() - xphat*15), tpi)).set_color(highlight))
        wlb_xlen = always_redraw(lambda: Line(start=OG, end=prjx_wlB.get_end(), stroke_width=6).set_color(gndhighlight2))
        wlb_tlen = always_redraw(lambda: Line(start=OG, end=prjt_wlB.get_end(), stroke_width=6).set_color(gndhighlight2))
        
        
        negevent0xp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xplongghost)).set_color(pcolor2))

        negevent0tp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15), negtplongghost)).set_color(phighlight))

        negpxpdot = always_redraw(lambda: Dot(negevent0xp.get_end()).set_color(pcolor2))
        negptpdot = always_redraw(lambda: Dot(negevent0tp.get_end()).set_color(phighlight))

        negpxplabel = always_redraw(lambda: MathTex("x_B(t'=0)").next_to(negpxpdot, DOWN*0.1+RIGHT*0.1).set_color(pcolor2).scale(0.75))
        negptplabel = always_redraw(lambda: MathTex("\Delta t'").next_to(negptpdot, LEFT).set_color(pcolor2).scale(0.75))

        negxplen = always_redraw(lambda:Line(start=OG, end=negevent0xp.get_end(), stroke_width=6,buff=0).set_color(phighlight2))
        negtplen = always_redraw(lambda:Line(start=OG, end=negevent0tp.get_end(), stroke_width=6,buff=0).set_color(phighlight2))

        self.wait(2)
        self.play(Create(negevent0tp))
        self.wait(2)
        # show that this is where tb' is simultaneous with tb=0
        self.play(Create(negptpdot))

        tbzero = MathTex("t_B =  0").next_to(event0pt.get_center(), DOWN*1.2).scale(0.8).shift(RIGHT*0.2).set_color(gndhighlight)
        angleofxp = np.arctan(v)
        simline = MathTex(r"\text{Line of simultaneous events}").scale(0.7).set_color(pcolor1).rotate(angleofxp).next_to(negevent0tp.get_end()).shift(RIGHT*0.5+UP*0.2)
        
        tbpzero1 = MathTex("t=0" ).next_to(negptpdot.get_center(), LEFT*1.5).set_color(gndhighlight)
        tbpzero2 = MathTex("t_B' = ?" ).set_color(pcolor).next_to(tbpzero1,DOWN).set_color(phighlight)

        self.play(Indicate(ax.x_axis))
        self.wait()
        self.play(Write(tbzero))
        self.wait(2)
        self.play(Create(simline))
        self.play(Indicate(negptpdot))
        self.wait()
        self.play(ShowPassingFlash(negevent0tp.copy()))
        self.play(Write(tbpzero1),run_time=2)
        self.play(Write(tbpzero2),run_time=2)

        self.wait(4)
        self.play(Create(worldlineB), run_time=2)
        self.play(Write(worldlineBlabel))
        self.wait(2)
        self.play(Create(along_wlB))
        self.play(Create(prjx_wlB), Create(prjt_wlB), run_time=2)
        self.play(Create(wlb_xlen), Create(wlb_tlen), run_time=2)
        self.play(along_wlB.animate.move_to(worldlineB.get_end()), run_time=5)
        self.wait(2)
        delx_alongwlb = Line(start=gli(xpi,worldlineB),end=wlb_xlen.get_end(),stroke_width=6).set_color(RED_C)
        self.add(delx_alongwlb)
        self.play(Indicate(delx_alongwlb))
        self.wait(2)
        wlbfadeouts = [along_wlB, prjt_wlB, prjx_wlB, wlb_tlen, wlb_xlen, delx_alongwlb]
        self.play(FadeOut(*wlbfadeouts), run_time=3)

        self.wait(3)

        self.play(Create(negevent0xp))
        self.play(Create(negpxpdot))
        self.play(Create(negpxplabel), run_time=2)
        self.wait()
        self.play(FadeOut(worldlineB), FadeOut(worldlineBlabel))
        self.wait(3)

        # show the B clock ahead delta tb
        prjt = always_redraw(lambda: DashedLine(start=negpxpdot.get_left(), end=[OG[0],negpxpdot.get_y(),0]).set_color(gndhighlight2))
        prjtdot = always_redraw(lambda: Dot(prjt.get_end()).set_color(gndhighlight2))
        lenpt = always_redraw(lambda: Line(start=OG, end=prjt.get_end(), stroke_width=6,buff=0).set_color(gndhighlight))
        deltlabel = always_redraw(lambda: MathTex("\Delta t").scale(0.8).next_to(lenpt.get_center(), LEFT).set_color(gndhighlight))
        # tpzero = MathTex("t' =  0").set_color(pcolor).next_to(negpxpdot.get_center(), UP*1.2+LEFT*0.02)
        tbattpzero1 = MathTex("t'=0").next_to(prjtdot, LEFT*1.5+UP*0.3).set_color(pcolor1)
        tbattpzero2 = MathTex("t_B = ?").next_to(tbattpzero1, DOWN).set_color(gndhighlight)
        # tbattpzero[0].set_color(pcolor)
        # tbattpzero[1].set_color(WHITE)
        fadeouts0 = [tbzero, simline, tbpzero1,tbpzero2, tbattpzero1, tbattpzero2]

        self.play(Indicate(xpi))
        self.wait()
        # self.play(Write(tpzero))
        self.wait(2)
        self.play(Create(prjt),run_time=2)
        self.play(Create(prjtdot))
        self.wait(2)
        self.play(Create(lenpt), run_time=2)
        self.bring_to_front(prjtdot)
        self.play(Write(tbattpzero1))
        self.play(Write(tbattpzero2))
        self.bring_to_front(negpxpdot)
        # self.play(Write(deltlabel))


        self.wait(4)
        self.play(FadeOut(*fadeouts0))
        self.play(FadeIn(negptplabel), FadeIn(deltlabel))
        self.wait(2)
        self.play(Create(negtplen), run_time=2)
        self.bring_to_front(negpxpdot)
        self.bring_to_front(negptpdot)


        # derive Lv/c^2 with Lorentz transform
        statcoords = MathTex("(x_B,t_B) = (L, 0)").set_color(ORANGE).next_to(event0pt.get_center(), DOWN+RIGHT*0.3)
        LTarrow = Arrow(start=event0pt.get_center(), end=negptpdot.get_center()).set_color(pcolor1)
        LTforB = MathTex(r"t' = \gamma\left( t - \frac{v}{c^2}x\right)").move_to(LTarrow.get_center()).shift(DOWN*1.5+RIGHT).scale(1.2).set_color(pcolor1)

        LTforB1 = MathTex("\Delta t' = ",r"\gamma\left(t_B - \frac{v}{c^2}x_B\right)").scale(1.2).set_color(pcolor1)
        LTforB2 = MathTex("\Delta t' = ", "\gamma (", "0", r" - \frac{v}{c^2}", "L", ")").scale(1.2).set_color(pcolor1)
        LTforB2[2].set_color(ORANGE)
        LTforB2[4].set_color(ORANGE)
        LTforB3 = MathTex("\implies \Delta t' = - ", r"\gamma", r"\frac{Lv}{c^2}").scale(1.2).set_color(pcolor1)
        LTforB4 = MathTex("\Delta t' = - ", r"\gamma", r"\frac{Lv}{c^2}").scale(1.3).move_to(LTforB.get_center()).set_color(phighlight2)


        self.wait(2)
        self.play(Indicate(event0pt))
        self.wait()
        self.play(Create(statcoords))
        self.wait(2)
        self.play(Indicate(negptplabel))
        self.wait()
        self.play(Create(LTarrow), run_time=2)
        self.wait(2)
        self.play(FadeOut(statcoords),
                  self.camera.frame.animate(run_time=2).shift(DOWN*4+RIGHT*2.8).scale(0.83))

        # self.play(Write(LTforB))
        eqposdot = Dot(LTarrow.get_center()).shift(DOWN+RIGHT)
        self.wait(2)
        self.play(ReplacementTransform(LTarrow, LTforB), run_time=2)
        self.wait(2)
        # self.play(Write(LTforB), FadeOut(LTarrow), run_time=2)
        self.play(Write(LTforB1.next_to(LTforB, DOWN).shift(DOWN*0.5)), run_time=2)
        self.wait(2)
        # self.play(FadeOut(LTforB), LTforB1.animate.move_to(eqposdot.get_center()))
        # self.wait(2)
        self.play(FadeIn(statcoords), run_time=2)
        self.wait(2)
        self.play(Write(LTforB2.next_to(LTforB1, DOWN).shift(DOWN*0.5)), run_time=2)
        self.wait(2)
        # self.play(FadeOut(LTforB1), LTforB2.animate.move_to(LTforB1.get_center()))
        self.play(FadeOut(statcoords))
        self.play(Write(LTforB3.next_to(LTforB1, RIGHT).shift(RIGHT).scale(1.1)), run_time=2)
        self.wait(2)
        self.play(FadeOut(*[LTforB, LTforB1, LTforB2]))
        self.play(self.camera.frame.animate(run_time=4).shift(UP*4+LEFT*2).scale(1/0.83), 
            ReplacementTransform(LTforB3, LTforB4), run_time=2.5)
        self.wait(2)
        self.play(Indicate(LTforB4[2]))
        self.wait(1)
        self.play(Indicate(LTforB4[1]))

        self.wait(5)


        ## move the point closer and further on x axis to show L dependence
        ## LT into a new frame with larger v to show v and gamma dependence, also better to differ points

        # get some longer axes to show distance
        

        xplong = Arrow(start=OG, end=OG + 8.5*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        xplonglabel = MathTex("x'").next_to(xplong.get_end(), RIGHT).set_color(pcolor2)
        xplabel0 = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)
        

        xlong = Axes(x_range=[-5,axrange+3,1], y_range=[-5,axrange,1], 
        x_length=ll+6, y_length=ll+3,axis_config={"include_ticks": False}).set_color(gndcolor1)
        xlong.shift(OG - xlong.c2p(0, 0))  # align origins
        xlong_labels = xlong.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor2)

        ax0 = Axes(x_range=[-5,axrange,1], y_range=[-5,axrange,1], 
        x_length=ll+3, y_length=ll+3,axis_config={"include_ticks": False}).set_color(gndcolor1)
        ax0.shift(OG - ax0.c2p(0, 0))  # align origins  # keeping this to transform back
        ax0labels = ax0.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor2)


        self.play(event0pt.animate.shift(LEFT*3), run_time=2)
        self.wait()
        self.play(Indicate(negtplen))
        self.play(Indicate(lenpt))
        self.wait(1)
        self.play(event0pt.animate.shift(RIGHT*5), Transform(ax, xlong), Transform(xpi, xplong),
                 Transform(ax_labels, xlong_labels), Transform(xplabel, xplonglabel), run_time=2)  # get longer axes
        self.wait()
        self.play(Indicate(negtplen))
        self.play(Indicate(lenpt))
        self.wait(2)
        self.play(event0pt.animate.shift(LEFT*2), Transform(ax, ax0), Transform(xpi, xp),
                  Transform(ax_labels, ax0labels),Transform(xplabel, xplabel0), run_time=2)  # back to old axes


        ## LT into a new frame with larger v to show v and gamma dependence, also better to differ points
        # let's start by removing the always_redraw stuff with static ones

        nrdnegprjxp = Line(start=event0pt.get_center(), end=event0pt.get_center()+ tphat*15)
        nrdnegprjtp = Line(start=event0pt.get_center(), end=event0pt.get_center()- xphat*15)

        nrdnegevent0xp = DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xp)).set_color(pcolor2)

        nrdnegevent0tp = DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15), negtp)).set_color(phighlight)

        nrdnegpxpdot = Dot(negevent0xp.get_end()).set_color(pcolor1)
        nrdnegptpdot = Dot(negevent0tp.get_end()).set_color(pcolor1)

        nrdnegpxplabel = MathTex("x_B(t'=0)").next_to(negpxpdot, DOWN*0.1+RIGHT*0.1).set_color(pcolor2).scale(0.75)
        nrdnegptplabel = MathTex("\Delta t'").next_to(negptpdot, LEFT).set_color(pcolor2).scale(0.75)

        # nrdnegxplen = Line(start=OG, end=negevent0xp.get_end(), stroke_width=6,buff=0).set_color(ORANGE)
        nrdnegtplen = Line(start=OG, end=negevent0tp.get_end(), stroke_width=6,buff=0).set_color(phighlight)

        nrdxplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)
        nrdtplabel = MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2)

        nrdprjt = DashedLine(start=negpxpdot.get_left(), end=[OG[0],negpxpdot.get_y(),0]).set_color(gndhighlight2)
        nrdprjtdot = Dot(prjt.get_end()).set_color(gndhighlight2)
        nrdlenpt = Line(start=OG, end=prjt.get_end(), stroke_width=6,buff=0).set_color(gndhighlight)
        # nrddeltlabel = MathTex("\Delta t").scale(0.8).next_to(lenpt.get_center(), LEFT).set_color(gndhighlight2)


        redrawObjects = [negevent0xp,negevent0tp,negpxpdot,negptpdot,negpxplabel,negptplabel,negxplen,negtplen,xplabel,tplabel, prjt, prjtdot, lenpt]
        noredrawObjects = [nrdnegevent0xp,nrdnegevent0tp,nrdnegpxpdot,nrdnegptpdot,nrdnegpxplabel,nrdnegptplabel,nrdnegtplen, nrdxplabel, nrdtplabel, nrdprjt, nrdlenpt, nrdprjtdot]
        self.remove(*redrawObjects)
        self.add(*noredrawObjects)

        u = 0.4

        xpphat = np.array([1,u,0])
        tpphat = np.array([u,1,0])


        xpp = Arrow(start=OG, end=OG + 7.5*xpphat/np.linalg.norm(xpphat), buff=0, stroke_width=3.5).set_color(pcolor1)
        xpplabel = always_redraw(lambda: MathTex("x'").next_to(xpp.get_end(), RIGHT).set_color(pcolor1))
        tpp = Arrow(start=OG, end=OG + 7.5*tpphat/np.linalg.norm(tpphat), buff=0, stroke_width=3.5).set_color(pcolor1)
        tpplabel = always_redraw(lambda : MathTex("t'").next_to(tpp.get_end(), UP).set_color(pcolor1))

        negxpp = Arrow(start=OG, end=OG - 5.5*xpphat/np.linalg.norm(xpphat), buff=0, stroke_width=3.5).set_color(pcolor1)
        negxpplabel = always_redraw(lambda: MathTex("-x'").next_to(negxpp.get_end(), LEFT).set_color(pcolor2))

        negtpp = Arrow(start=OG, end=OG - 5.5*tpphat/np.linalg.norm(tpphat), buff=0, stroke_width=3.5).set_color(pcolor1)
        negtpplabel = always_redraw(lambda : MathTex("-t'").next_to(negtpp.get_end(), LEFT).set_color(pcolor2))

        negprjxpp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()+ that*15))
        negprjtpp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()- xpphat*15))

        negevent0xpp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xpp)).set_color(gndhighlight))

        negevent0tpp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xpphat*15), negtpp)).set_color(phighlight))

        negpxppdot = always_redraw(lambda: Dot(negevent0xpp.get_end()).set_color(phighlight))
        negptppdot = always_redraw(lambda: Dot(negevent0tpp.get_end()).set_color(phighlight))

        negpxpplabel = always_redraw(lambda: MathTex(r"x_{B_0'}").next_to(negpxppdot, DOWN*0.1+RIGHT*0.1).set_color(pcolor2).scale(0.75))
        negptpplabel = always_redraw(lambda: MathTex("\Delta t'").next_to(negptppdot, LEFT).set_color(pcolor2))

        negxpplen = always_redraw(lambda:Line(start=OG, end=negevent0xpp.get_end(), stroke_width=6,buff=0).set_color(phighlight))
        negtpplen = always_redraw(lambda:Line(start=OG, end=negevent0tpp.get_end(), stroke_width=6,buff=0).set_color(phighlight))

        newprjt = always_redraw(lambda: DashedLine(start=negpxppdot.get_left(), end=[OG[0],negpxppdot.get_y(),0]).set_color(gndhighlight))
        newprjtdot = always_redraw(lambda: Dot(newprjt.get_end()).set_color(gndhighlight))
        newlenpt = always_redraw(lambda: Line(start=OG, end=newprjt.get_end(), stroke_width=6,buff=0).set_color(gndhighlight))
    


        self.play(Transform(xpi, xpp), Transform(tpi, tpp), Transform(negxp, negxpp), Transform(negtp, negtpp),
        Transform(nrdxplabel, xpplabel),Transform(nrdtplabel, tpplabel),
        Transform(nrdnegevent0xp, negevent0xpp),Transform(nrdnegevent0tp, negevent0tpp),Transform(nrdnegpxpdot, negpxppdot),
        Transform(nrdnegptpdot, negptppdot), Transform(nrdnegpxplabel, negpxpplabel), Transform(nrdnegptplabel, negptpplabel),
        Transform(nrdnegtplen, negtpplen),self.camera.frame.animate.scale(1.2).shift(DOWN+RIGHT), 
        Transform(nrdprjt, newprjt), Transform(nrdlenpt,newlenpt), Transform(nrdprjtdot, newprjtdot), run_time=3.5)
        self.bring_to_front(negpxppdot)
        self.play(Indicate(nrdnegtplen), Indicate(newlenpt))
        self.wait(2)
        self.play(FadeOut(LTforB4),run_time=2)


        lvc2pt = Dot(gli(negevent0tpp, ax.y_axis)).set_color(gndhighlight2)
        mlvc2 = Line(start=lvc2pt.get_top(),end=OG).set_color(gndhighlight2)
        mdeltlabel = MathTex("-\Delta t").next_to(mlvc2, RIGHT).set_color(gndhighlight2)

        lt_to_lvc2 = Arrow(start=negptppdot.get_center(),end=lvc2pt.get_left(), buff=0.01)
        lt_to_lvc2eq = MathTex(r"t' =\gamma\left(t - \frac{v}{c^2}x\right)").move_to(LTforB4.get_center()).set_color(Emerald).scale(1.2)
        lt_to_lvc2eq20 = MathTex(r"\implies t' =\gamma t").next_to(lt_to_lvc2eq, RIGHT*2).set_color(gndhighlight2).scale(1.2)
        lt_to_lvc2eq2 = MathTex(r"\Delta t' =\gamma \Delta t").move_to(LTforB4.get_center()).shift(LEFT*0.4+UP*0.3).set_color(gndhighlight2).scale(1.2)

        lt_to_lvc2eq3 = MathTex(r"\Delta t = \frac{\Delta t'}{\gamma} = \frac{1}{\gamma} \left(\gamma\frac{Lv}{c^2}\right)").next_to(lt_to_lvc2eq, DOWN*1.5).set_color(gndhighlight2).scale(1.2)
        lt_to_lvc2eq4 = MathTex(r"\Delta t = \frac{Lv}{c^2}").next_to(lt_to_lvc2eq3, DOWN*1.5).scale(1.6).set_color(gndhighlight2).scale(1.2)
        

        self.play(Create(lvc2pt))
        self.play(self.camera.frame.animate.scale(0.8).shift(DOWN*2),run_time=3.5)
        self.play(Create(lt_to_lvc2))
        self.wait(2)
        self.play(ReplacementTransform(lt_to_lvc2, lt_to_lvc2eq))
        self.wait(2)
        self.play(Write(lt_to_lvc2eq20))
        self.wait(2)
        self.play(Transform(lt_to_lvc2eq, lt_to_lvc2eq2), FadeOut(lt_to_lvc2eq20), run_time=2)
        self.wait(2)
        self.play(Create(mlvc2),Create(mdeltlabel))
        self.play(Indicate(negptpplabel))
        self.wait(2)
        self.play(Indicate(mlvc2), Indicate(mdeltlabel))
        self.wait(2)
        self.play(FadeOut(mdeltlabel), FadeOut(mlvc2))
        self.wait(2)
        self.play(Write(LTforB4.move_to(lt_to_lvc2eq.get_center()).shift(RIGHT*4.5).scale(1/1.1)), run_time=2)
        self.wait(2)
        self.play(Indicate(lt_to_lvc2eq))
        self.play(ReplacementTransform(LTforB4, lt_to_lvc2eq3), run_time=2)
        self.wait(2)
        lasteqpos = lt_to_lvc2eq3.get_center()
        self.play(FadeOut(lt_to_lvc2eq), lt_to_lvc2eq3.animate.move_to(lt_to_lvc2eq.get_center()).shift(RIGHT*2+DOWN*0.3))
        self.wait(2)
        self.play(Write(lt_to_lvc2eq4.move_to(lasteqpos).shift(DOWN)), run_time=2)
        self.wait(2)
        self.play(FadeOut(*[lt_to_lvc2eq3]), lt_to_lvc2eq4.animate(run_time=2).move_to(lt_to_lvc2eq.get_center()).shift(DOWN+RIGHT*0.5).set_color(propercolor))
        self.wait()
        boxit = SurroundingRectangle(lt_to_lvc2eq4, color=propercolor)
        self.play(Create(boxit), run_time=2)
        self.play(self.camera.frame.animate(run_time=8, rate_func=linear).move_to(lt_to_lvc2eq4.get_center()).scale(0.4))

        self.wait(5)


class TrainTunnelAnimation(MovingCameraScene):

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

        self.camera.background_color = ManimColor.from_hex("#171717")
        self.camera.frame.scale(1.5)

        train0 = ImageMobject("train.png").scale(0.95).shift(DOWN*1.6+LEFT*5)
        tunnel0 = ImageMobject("tunnel.png").scale(1.35).shift(RIGHT*5)
        tunneltransparent0 = ImageMobject("tunneltp.png").shift(RIGHT*5+DOWN*0.03).scale(1.35)

        train = ImageMobject("train.png").scale(0.95).shift(DOWN*1.6+LEFT*5)
        tunnel = ImageMobject("tunnel.png").scale(1.35).shift(RIGHT*5)
        tunneltransparent = ImageMobject("tunneltp.png").shift(RIGHT*5+DOWN*0.03).scale(1.35)

        coordv = 1/1.5  # shift 1.5 units = 1 run_time, multiply the shift by this to get runtime


        signal = []
        for i in range(5):
            arci = Arc(angle=PI*0.6, start_angle=-PI*0.3).move_to(tunnel.get_left()).shift(DOWN*2+RIGHT*4)
            anim_1 = Succession(Create(arci, run_time=0.05), arci.animate(run_time=1.5).shift(RIGHT*14).scale(5), FadeOut(arci, run_time=0.2))
            signal.append(anim_1)


        self.play(FadeIn(train))
        self.play(FadeIn(tunnel))
        self.wait(5)
        # self.play(train.animate.stretch(0.7, dim=0))
        # enter_tunnel = Succession(train.animate(run_time=4, rate_func=linear).shift(RIGHT*6),
        #                 FadeOut(tunnel),FadeIn(tunneltransparent))
        
        self.play(train.animate(run_time=6*coordv, rate_func=linear).shift(RIGHT*6))
        self.play(FadeOut(tunnel), FadeIn(tunneltransparent))
        
        self.play(self.camera.frame.animate(run_time=4).scale(0.8).shift(RIGHT*4.5),
                    train.animate(rate_func=linear, run_time=4.4*coordv).shift(RIGHT*4.4))

        explosionimg0 = ImageMobject("explosion.png").scale(0.01).move_to(tunnel.get_right()).shift(LEFT*4+DOWN*2)
        explosionimg=explosionimg0.copy()
        explosion_animation = Succession(Add(explosionimg), 
                                         explosionimg.animate(run_time=0.5, rate_func=linear).scale(80), FadeOut(explosionimg))
        self.wait(3)
        self.play(explosion_animation)

        self.wait(3)
        self.play(AnimationGroup(*signal, lag_ratio=0.15, run_time=3))
        self.wait(4)
        # self.play(AnimationGroup(*signal, lag_ratio=0.15, run_time=3), explosion_animation)

        # RESET BUTTON
        
        self.play(FadeOut(train), FadeOut(tunneltransparent))
        self.camera.frame.shift(LEFT*4.5).scale(1/0.8)
        train.move_to(train0.get_center())
        signal = []
        for i in range(5):
            arci = Arc(angle=PI*0.6, start_angle=-PI*0.3).move_to(tunnel.get_left()).shift(DOWN*2+RIGHT*4)
            anim_1 = Succession(Create(arci, run_time=0.05), arci.animate(run_time=1.5).shift(RIGHT*14).scale(5), FadeOut(arci, run_time=0.2))
            signal.append(anim_1)
        #END RESET BUTTON
        stretchfactor=0.5

        # Ground frame (train contracted)
        gndframe_title = Text("Ground Frame").to_corner(UL).shift(LEFT*2+UP*1.5).set_color(SteelBlue)
        gndframe_subtitle = Text("(Train is length contracted)").next_to(gndframe_title, DOWN).scale(0.75).set_color(MistyBlue)
        contractrain = train.copy()
        contractrain.stretch(stretchfactor, dim=0)
        signalgroup = AnimationGroup(*signal, lag_ratio=0.15, run_time=3)

        move_signal = AnimationGroup(
            AnimationGroup(contractrain.animate(run_time=coordv*18, rate_func=linear).shift(RIGHT*20), self.camera.frame.animate(run_time=4).scale(0.8).shift(RIGHT*4.5),
                            FadeOut(gndframe_title), FadeOut(gndframe_subtitle), lag_ratio=0),
            AnimationGroup(Wait(5), signalgroup, lag_ratio=1), lag_ratio=0
        )
        
        self.play(FadeIn(train), FadeIn(tunneltransparent),run_time=2)
        self.play(Wait(2))
        self.play(Write(gndframe_title))
        self.wait(3)
        self.play(Write(gndframe_subtitle))
        self.play(train.animate(run_time=2).stretch(stretchfactor, dim=0))
        
        self.add(contractrain)
        self.remove(train)
        self.wait(2)
        self.play(move_signal)
        # self.play(train.animate(run_time=10*coordv, rate_func=linear).shift(RIGHT*10), self.camera.frame.animate(run_time=4).scale(0.8).shift(RIGHT*4.5))
        # self.play(contract_move_signal_move)
        #RESET BUTTON
        self.remove(explosionimg)
        explosionimg1 = ImageMobject("explosion.png").scale(0.01).move_to(tunnel.get_right()).shift(LEFT*6+DOWN*2)
        explosionimg = explosionimg1.copy()
        explosion_animation = Succession(explosionimg.animate(run_time=0.5, rate_func=linear).scale(80), FadeOut(explosionimg),lag_ratio=0.1)
        self.play(FadeOut(contractrain), FadeOut(tunneltransparent))
        self.camera.frame.shift(LEFT*4.5).scale(1/0.8)
        train.move_to(train0.get_center()).stretch(1/stretchfactor, dim=0)
        #END RESET BUTTON

        # Train frame (tunnel is contracted)
        trainframe_title = Text("Train Frame").to_corner(UL).shift(LEFT*2+UP*1.5).set_color(Salmon)
        trainframe_subtitle = Text("(Tunnel is length contracted)").next_to(gndframe_title, DOWN).scale(0.75).set_color(PastelRed)
        self.play(FadeIn(train), FadeIn(tunneltransparent),run_time=2)
        self.wait(2)
        self.play(Write(trainframe_title))
        self.play(Write(trainframe_subtitle))
        self.wait(2)

        self.play(AnimationGroup(train.animate(run_time=8*coordv, rate_func=linear).shift(RIGHT*8), 
                                self.camera.frame.animate(run_time=4).scale(0.8).shift(RIGHT*1.5), 
                                FadeOut(trainframe_title), FadeOut(trainframe_subtitle),
                                tunneltransparent.animate(run_time=1.8).stretch(stretchfactor, dim=0)))
        self.play(explosion_animation, FadeOut(train))

        self.wait(10)


class TrainTunnelDiagram(MovingCameraScene):

    # TODO: Fix how the lines overlap in the fadeout at the L proper animation

    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")

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

        def gli(line1, line2):
            p1, p2 = line1.get_start(), line1.get_end()
            p3, p4 = line2.get_start(), line2.get_end()

            # Direction vectors
            d1 = p2 - p1
            d2 = p4 - p3

            # Solve for intersection using determinant
            matrix = np.array([d1[:2], -d2[:2]]).T
            if np.linalg.det(matrix) == 0:
                return None  # Lines are parallel or coincident

            b = p3[:2] - p1[:2]
            t_vals = np.linalg.solve(matrix, b)

            # Optional: check if intersection is within segments (0 ≤ t ≤ 1)
            if not (0 <= t_vals[0] <= 1 and 0 <= t_vals[1] <= 1):
                return None  # Intersection is outside segment

            intersection = p1 + t_vals[0] * d1
            return intersection


        def glslope(line):
            st = line.get_start()
            en = line.get_end()
            delx = np.abs(en[0] - st[0])
            dely = np.abs(en[1] - st[1])

            return dely/delx


        def gl_stinterval(line, length):

            #only works for lines from origin
            st = line.get_start()
            en = line.get_end()
            delx = np.abs(en[0] - st[0])
            dely = np.abs(en[1] - st[1])
            slope = dely/delx

            int_x = np.sqrt(length**2/(1-slope**2))
            int_t = slope*int_x

            return([int_x, int_t, 0])


        ################################ SCENE 1: Setting up the problem diagram
        
        gndax = Axes(x_range=[0, 10, 1], y_range=[0,10,1], x_length=7, y_length=7,axis_config={"include_ticks": False,"stroke_width":3.5}).set_color(gndcolor2)
        gndaxlabel = gndax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor2)

        # gndgrid = NumberPlane(x_range=[1, 10, 1],  y_range=[1,10,1], x_length=7, y_length=7,
        # background_line_style={"stroke_color": MistyBlue,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,})

        og = gndax.c2p(0,0)
        ogdot = Dot(og).set_color(propercolor)
        xhat = np.array([1,0,0])*0.7  #normalize with xrange and xlen
        that = np.array([0,1,0])*0.7
        light_line = DashedLine(start=og, end=gndax.c2p(10,10)).set_color(Mustard).set_opacity(0.75)
        light_label = MathTex("x=ct").next_to(light_line.get_end()).set_color(Mustard).set_opacity(0.75)

        v = 0.60
        gamma = 1/np.sqrt(1-v**2)
        
        properL = 4 # in coordinate distances
        Lprime = 4/gamma
        tunnelent = Dot(gndax.c2p(4,0)).set_color(gndcolor1)
        tunnelext = Dot(gndax.c2p(4+properL,0)).set_color(gndcolor1)
        tunnelproper = Line(tunnelent.get_center(), tunnelext.get_center(), stroke_width=5.5).set_color(propercolor)
        tunnelL = BraceBetweenPoints(tunnelent.get_center(), tunnelext.get_center()).set_color(propercolor)
        tunnelLlabel = MathTex("L").next_to(tunnelL.get_center(),DOWN).set_color(propercolor)

        tunnelentwl = Line(start=tunnelent.get_center(), end=tunnelent.get_center()+that*10, stroke_width=1.5).set_color(gndcolor2)
        tunnelextwl = Line(start=tunnelext.get_center(), end=tunnelext.get_center()+that*10, stroke_width=1.5).set_color(gndcolor2)

        tunnelentlabel = MathTex(r"\text{Entrance}").next_to(tunnelent.get_center(), DOWN).scale(0.8).set_color(gndcolor1)
        tunnelextlabel = MathTex(r"\text{Exit}").next_to(tunnelext.get_center(), DOWN).scale(0.8).set_color(gndcolor1)

        gndframe = [gndax, gndaxlabel, light_line, light_label]


        # Train axes 
        # print("###################### gamma = ", gamma, "L/gamma = ", 1/gamma, "L", "4/gamma = ", 4/gamma)
        xphat = np.array([1,v,0])/np.linalg.norm(np.array([1,v,0]))
        tphat = np.array([v,1,0])/np.linalg.norm(np.array([v,1,0]))
        
        trainbackdot = Dot(gndax.c2p(0,0)).set_color(pcolor1)
        trainfrontdot = Dot(gndax.c2p(Lprime,0)).set_color(pcolor1)

        tpfront = Arrow(start=trainfrontdot.get_center(), end=trainfrontdot.get_center() + tphat*8, buff=0).set_color(pcolor1)
        tpback = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + tphat*8, buff=0).set_color(pcolor1)
        tpfrontlabel = always_redraw(lambda: MathTex("t_f '").next_to(tpfront.get_end(), UP*0.7).set_color(pcolor2))
        tpbacklabel = always_redraw(lambda: MathTex("t_b '").next_to(tpback.get_end(), UP*0.7).set_color(pcolor2))

        xpog = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + xphat*8, buff=0).set_color(pcolor2)
        xplabel = always_redraw(lambda: MathTex("x '").next_to(xpog.get_end(), RIGHT).set_color(pcolor2))

        # events of interest
        front_out = Dot(gli(tpfront, tunnelextwl))  # front of train exits tunnel
        back_in = Dot(gli(tpback, tunnelentwl))  # back of train enters tunnel
        lentrain = Dot(gli(tpfront, xpog))  # proper length of train measurement

        trainLp = BraceBetweenPoints(trainbackdot.get_bottom(), trainfrontdot.get_bottom()).set_color(gndcolor2)
        trainLpline = Line(trainbackdot.get_center(), trainfrontdot.get_center(), stroke_width=5.5).set_color(gndcolor2)
        trainLplabel = MathTex(r"L/\gamma").next_to(trainLp.get_center(), DOWN).set_color(gndcolor2)

        ogtpzero = MathTex("t'=0").next_to(ogdot, DOWN*0.3).set_color(pcolor2)
        fronttpzero = MathTex("t'=0").next_to(lentrain, DOWN*0.3+RIGHT*0.3).set_color(propercolor)
        fronttpnotzero = MathTex(r"t'\neq 0").next_to(trainfrontdot, DOWN*0.3).set_color(pcolor2)

        trainproper = Line(og, lentrain.get_center(), stroke_width=5.5).set_color(propercolor)
        trainproperL = MathTex("L").next_to(trainproper.get_center(), LEFT*0.3+UP*0.3)

        scene1fadeouts = [tunnelent, tunnelext, trainfrontdot, tpfront, trainproperL, tpfrontlabel, tunnelproper, tunnelentwl, tunnelextwl, tunnelentlabel, tunnelextlabel]
        # tunnel
        self.camera.frame.scale(1.15).shift(DOWN*0.3)
        self.play(*[Create(i)for i in gndframe], run_time=2.5)
        self.wait(3)
        self.play(FadeOut(light_label), light_line.animate.set_opacity(0.2))
        self.play(Create(tunnelent), Create(tunnelext))
        self.play(Write(tunnelentlabel))
        self.play(Write(tunnelextlabel))
        self.wait(2)
        self.play(Create(tunnelentwl), Create(tunnelextwl))
        self.wait(2)
        self.play(FadeOut(tunnelentlabel), FadeOut(tunnelextlabel))
        tunnelentlabel.move_to(tunnelentwl.get_end()).shift(UP*0.3).scale(0.7)
        tunnelextlabel.move_to(tunnelextwl.get_end()).shift(UP*0.3).scale(0.7)
        self.play(FadeIn(tunnelentlabel), FadeIn(tunnelextlabel))
        self.wait(3)
        self.play(Create(tunnelproper))
        self.play(FadeIn(tunnelL), Write(tunnelLlabel),run_time=2)
        self.wait(3)
        self.play(FadeOut(tunnelL), FadeOut(tunnelLlabel))
        self.wait(3)

        # train
        self.play(Create(trainfrontdot), Create(trainbackdot))
        self.wait(2)
        
        self.wait(2)
        self.play(Create(tpfront),run_time=3)
        self.play(Write(tpfrontlabel))
        self.play(Create(tpback),run_time=3)
        self.play(Write(tpbacklabel))
        self.wait(2)
        self.play(Create(trainLpline))
        self.play(FadeIn(trainLp), Write(trainLplabel))
        self.wait(2)
        self.play(FadeOut(trainLp), FadeOut(trainLplabel), FadeOut(trainLpline))
        self.play(Write(ogtpzero), run_time=2)
        self.wait()
        self.play(Write(fronttpnotzero), run_time=2)
        self.wait(2)

        self.wait(2)
        self.play(FadeOut(fronttpnotzero))
        self.wait(2)
        self.play(Create(xpog), run_time=3)
        self.play(Write(xplabel))
        self.wait(2)
        self.play(FadeOut(trainbackdot),ogtpzero.animate.set_color(propercolor), Create(ogdot), Create(lentrain))
        self.play(Write(fronttpzero))
        self.wait(2)
        self.play(Create(trainproper), run_time=2)
        self.play(Write(trainproperL))
        self.wait(3)
        self.play(FadeOut(*scene1fadeouts))
        self.wait(3)

        # SCENE 2 demonstrate projections

        prj_ground = DashedLine(lentrain.get_center(), [lentrain.get_x(), og[1], 0]).set_color(gndhighlight)
        prj_prime = DashedLine(lentrain.get_center(), trainfrontdot.get_center()).set_color(phighlight)

        Lgammadot = Dot(prj_ground.get_end()).set_color(gndhighlight)
        Lgammalabel = MathTex(r"L\gamma").next_to(Lgammadot.get_center(), DOWN).set_color(gndhighlight)
        fronttnotzero = MathTex(r"t \neq 0").set_color(gndhighlight).next_to(lentrain.get_center(), RIGHT+DOWN)

        fronttpzero0 = MathTex("t'=0").next_to(lentrain, DOWN*0.3+RIGHT*0.3).set_color(propercolor)  # in case I wanna transform back

        Ldivgammadot = Dot(trainfrontdot.get_center()).set_color(phighlight)
        Ldivgammalabel = MathTex(r"L/\gamma").next_to(Ldivgammadot.get_center(), DOWN).set_color(phighlight)
        Ldivgammaline = trainLpline.copy().set_color(phighlight)

        self.wait(3)
        self.play(Transform(fronttpzero, fronttnotzero), run_time=2)
        self.play(Create(prj_prime),run_time=2)
        self.play(Create(Ldivgammadot))
        self.wait(2)
        self.play(Create(Ldivgammaline), run_time=1.5)
        self.play(Write(Ldivgammalabel))
        self.wait(4)

        self.play(Create(prj_ground), run_time=3)
        self.wait(2)
        self.play(Indicate(gndax.x_axis))
        self.wait(2)
        self.play(Create(Lgammadot))
        self.play(Write(Lgammalabel))
        self.wait(2)
        self.play(Indicate(trainproper))

        self.wait(5)

        # Where is L?
        whereL = Line(Ldivgammadot.get_center(), Lgammadot.get_center(), stroke_width=5.5)
        Ldot = Dot(whereL.get_center())
        Llabel = always_redraw(lambda: MathTex("L").next_to(Ldot.get_center() ,DOWN))
        Lcorrect = gndax.c2p(properL,0)

        spacelike_invariant_hyperbola = gndax.plot(lambda x : np.sqrt(x**2 - properL**2), x_range=[4,10,0.01]).set_color(VibrantPink2)
        timelike_invariant_hyperbola = gndax.plot(lambda x : np.sqrt(x**2 + properL**2), x_range=[0,9.17,0.01]).set_color(VibrantPink2)

        hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(spacelike_invariant_hyperbola.get_end(), RIGHT+UP).set_color(VibrantPink)

        self.play(Create(whereL), Indicate(whereL))
        self.wait(2)
        self.play(Create(Ldot), Create(Llabel))
        self.play(Ldot.animate.move_to(Ldivgammadot.get_right()),run_time=2)
        self.play(Ldot.animate.move_to(Lgammadot.get_left()),run_time=2)
        self.play(Ldot.animate.move_to(Ldivgammadot.get_right()),run_time=2)
        self.play(Ldot.animate.move_to(Lcorrect),run_time=2)
        self.play(Indicate(Ldot))
        self.wait(3)
        self.play(Create(spacelike_invariant_hyperbola), run_time=4)
        self.play(Write(hyperbola_eqq), run_time=3)
        self.wait(2)
        self.play(Indicate(hyperbola_eqq))

        # def intersects(mobj1, mobj2, ax=None, tolerance=0.05):
        #     intersections = []
        #     mobj1_points = mobj1.get_all_points()
        #     mobj2_points = mobj2.get_all_points()

        #     for p1 in mobj1_points:
        #         for p2 in mobj2_points:
        #             if np.linalg.norm(p1 - p2) < tolerance:
        #                 if ax:
        #                     coord = ax.p2c((p1 + p2) / 2)
        #                 else:
        #                     coord = ((p1 + p2) / 2)[:2]  # fall back to raw scene coordinates
        #                 intersections.append(coord)
        #     return intersections

        # Show off with a bunch of coordinate axes intersecting the hyperbola:
        show_off_xps = VGroup()
        show_off_tps = VGroup()

        show_off_vs = [0.30, 0.40, 0.50, 0.70, 0.80]
        show_off_colors = [MistyBlue, VibrantGreen, DarkPurple, Salmon, SteelBlue]
        hatlengths = [5, 6, 7, 9, 10]
        x_intersects = VGroup()
        x_intersects_lines = VGroup()

        for i in range(5):
            u = show_off_vs[i]
            colori = show_off_colors[i]
            hatlength = hatlengths[i]

            xphatu = np.array([1,u,0])/np.linalg.norm(np.array([1,u,0]))
            tphatu = np.array([u,1,0])/np.linalg.norm(np.array([u,1,0]))
            tpu = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + tphatu*hatlength, buff=0).set_color(colori)
            xpu = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + xphatu*hatlength, buff=0).set_color(colori)
            xpu_Lpt = Dot(gndax.c2p(*gl_stinterval(xpu, properL))).set_color(propercolor)
            xpu_Lptline = Line(trainbackdot.get_center(), xpu_Lpt.get_center()).set_color(propercolor)
            show_off_xps.add(xpu)
            show_off_tps.add(tpu)
            x_intersects.add(xpu_Lpt)
            x_intersects_lines.add(xpu_Lptline)

            # xpu_intersection = intersects(xpu, spacelike_invariant_hyperbola)
            # xpuintdot = Dot(xpu_intersection)
            # x_intersects.add(xpuintdot)

        prefadeouts = [Ldivgammadot, Lgammadot, Ldivgammalabel, Lgammalabel,fronttnotzero]
        self.wait(3)
        self.play(FadeOut(*prefadeouts))
        self.play(Create(show_off_xps), run_time=6)
        self.play(Create(x_intersects), Create(x_intersects_lines), run_time=4)

        self.wait(3)

        self.play(Create(timelike_invariant_hyperbola), run_time=4)
        self.play(Create(show_off_tps), run_time=4)

        self.wait(5)

        self.play(FadeOut(show_off_tps), FadeOut(show_off_xps), FadeOut(x_intersects), FadeOut(x_intersects_lines))
        self.wait(2)

        # Back to scene1 objects
        scene2fadeouts = [timelike_invariant_hyperbola, spacelike_invariant_hyperbola,hyperbola_eqq, prj_ground, Llabel, fronttpzero]
        self.play(FadeOut(*scene2fadeouts), FadeIn(*scene1fadeouts), run_time=3)
        self.remove(*scene2fadeouts)

        self.wait(5)

        # SCENE 3

        t_frontout = DashedLine(front_out.get_left(), [og[0], front_out.get_y(),0]).set_color(gndhighlight)
        t_backin = DashedLine(back_in.get_left(), [og[0], back_in.get_y(),0]).set_color(gndhighlight)

        t_frontout_label = MathTex(r"\text{Explosion!}").next_to(t_frontout.get_end(), LEFT).scale(0.8).set_color(propercolor)
        t_backin_label = MathTex(r"\text{Diffusion??}").next_to(t_backin.get_end(), LEFT).scale(0.8).set_color(propercolor)

        # Need longer axes again...
        gndaxlong = Axes(x_range=[0, 16, 1], y_range=[0,16,1], x_length=7*16/10, y_length=7*16/10,axis_config={"include_ticks": False,"stroke_width":3.5}).set_color(gndcolor2)
        gndaxlong.shift(og - gndaxlong.c2p(0,0))
        gndaxlabellong = gndaxlong.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor2)
        tunnelentwllong = Line(start=tunnelent.get_center(), end=tunnelent.get_center()+that*15.5, stroke_width=2.5).set_color(gndcolor2)
        tunnelextwllong = Line(start=tunnelext.get_center(), end=tunnelext.get_center()+that*15.5, stroke_width=2.5).set_color(gndcolor2)
        light_linelong = DashedLine(start=og, end=gndax.c2p(16,16)).set_color(Mustard).set_opacity(0.75)

        tpfrontlong = Arrow(start=trainfrontdot.get_center(), end=trainfrontdot.get_center() + tphat*13, buff=0).set_color(pcolor1)
        tpbacklong = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + tphat*13, buff=0).set_color(pcolor1)
        diffuse_signalghost = DashedLine(back_in.get_center(), back_in.get_center()+xhat*8.5 +that*8.5).set_color(Mustard)
        signal_received = Dot(gli(diffuse_signalghost, tpfrontlong))
        diffuse_signal = DashedLine(back_in.get_center(), signal_received.get_center()).set_color(Mustard)
        
        xpoglong = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + xphat*13, buff=0).set_color(pcolor2)
        
        t_diffuse = DashedLine(signal_received.get_left(), [og[0], signal_received.get_y(),0])
        t_diffuse_label = MathTex(r"\text{Diffusion!}").next_to(t_diffuse.get_end(), LEFT).scale(0.8).set_color(propercolor)

        self.play(Create(front_out), Create(back_in))           
        self.play(Create(t_frontout), run_time=2.5)
        self.wait()
        self.play(Create(t_backin), run_time=2.5)
        self.play(Write(t_frontout_label), run_time=2)
        self.wait(2)
        self.play(Write(t_backin_label), run_time=2)
        self.wait(3)
        self.play(Indicate(back_in))
        self.wait()
        self.play(Indicate(front_out))
        self.wait(2)
        self.play(FadeOut(t_backin), FadeOut(t_backin_label))

        self.play(Create(diffuse_signal), run_time=3)
        self.wait(2)

        self.play(Transform(gndax, gndaxlong), Transform(tpfront, tpfrontlong), Transform(gndaxlabel, gndaxlabellong),
        Transform(tpback, tpbacklong), Transform(xpog, xpoglong), Transform(light_line, light_linelong),
        Transform(tunnelentwl, tunnelentwllong), Transform(tunnelextwl, tunnelextwllong),
        tunnelentlabel.animate.move_to(tunnelentwllong.get_end()).shift(UP*0.3).scale(1.2),
        tunnelextlabel.animate.move_to(tunnelextwllong.get_end()).shift(UP*0.3).scale(1.2),
        self.camera.frame.animate.scale(1.6).shift(UP*2.8+RIGHT*2), run_time=5)

        self.wait()
        self.play(Create(signal_received), run_time=1.5)
        self.wait(2)
        self.play(Create(t_diffuse), run_time=2)
        self.wait()
        self.play(Write(t_diffuse_label), run_time=2)
        scene3fadeouts = [t_frontout, t_frontout_label]
        self.wait(3)

        # Scene 4 - show again on the train frame

        self.play(FadeOut(*scene3fadeouts))
        self.wait(4)
        tpbackinlabel = MathTex(r"t_{\text{Back-in}}'").next_to(back_in.get_center(), LEFT*1.5).set_color(phighlight)
        xpbackin = Arrow(start=back_in.get_center(), end=back_in.get_center() + xphat*8, buff=0).set_color(pcolor2)
        xpbackinlabel = MathTex(r"t_{\text{Back-in}}'").next_to(xpbackin.get_end(), RIGHT).set_color(phighlight)

        tp_explosionghost = Line(front_out.get_center(), front_out.get_center()-xphat*10)

        tp_explosiondot = Dot(gli(tpback, tp_explosionghost)).set_color(phighlight)
        tp_explosionprj = DashedLine(front_out.get_center(), tp_explosiondot.get_center()).set_color(phighlight)

        self.play(Write(tpbackinlabel), run_time=2)
        self.wait(2)
        self.play(Create(xpbackin), run_time=2.5)
        self.wait(2)
        self.play(Write(xpbackinlabel),run_time=2)
        self.wait(2)
        self.play(Create(tp_explosionprj), run_time=2.5)
        self.play(Create(tp_explosiondot))
        self.wait(2)
      
        self.wait(10)


class TripletsIntro(Scene):
    def construct(self):

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

        self.camera.background_color = ManimColor.from_hex("#171717")
        
        A = ImageMobject("Andy.png").shift(LEFT).scale(0.3)
        B = ImageMobject("Bob.png").shift(RIGHT).scale(0.3)
        C = ImageMobject("Charlie.png").shift(DOWN).scale(0.3)

        planetA = ImageMobject("earth.png").scale(0.3).shift(LEFT*2)
        planetC = ImageMobject("planet1.png").scale(0.3).shift(RIGHT*2)

        rocketB = ImageMobject("rocket.png")
        rocketC = ImageMobject("rocketblue.png")


        clockscale = 0.15
        clockimg = ImageMobject("clock.png").scale(clockscale).shift(LEFT*3)
        clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale))
        clockcenter = always_redraw(lambda:Dot(clockimg.get_center()).set_color(VibrantGreen).scale(1.4).scale(clockscale))
        clock12 = always_redraw(lambda:Dot(clockimg.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetip = Dot(clock12.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=3).set_color(BLACK))


        clock=Group(clockbg, clockimg, clockline, clock12, clockcenter)
        clockmove = Group(clockimg, clocklinetip)

        def advance_clock(startN, N, rate=1/3):
            tickrange = np.abs(startN-N)
            clockanimationlist = []
            for i in range(N):
                tickarc_i = always_redraw(lambda: Arc(radius=2.9*clockscale, start_angle=PI/2-startN*PI/6-i*PI/6, 
                                angle=-PI/6, arc_center=clockcenter.get_center()).set_opacity(1).set_color(GoodOrange))
                # tickanimation = MoveAlongPath(clocklinetip, tickarc_i, run_time=1.5*rate)
                tickanimation=(Create(tickarc_i))
                clockanimationlist.append(tickanimation)

            # tickcircleN = Arc(radius=2.9, start_angle=PI/2-startN*PI/6, angle=-np.abs(startN-N)*PI/6).set_opacity(0)
            # clockanimation = MoveAlongPath(clocklinetip, tickcircleN, rate_func=linear, run_time=np.abs(startN-N)*rate)
            clockanimation = AnimationGroup(*clockanimationlist, lag_ratio=1.5)
            return clockanimation
        
        # self.play(FadeIn(A), FadeIn(B), FadeIn(C))
        # self.play(FadeIn(planetA), FadeIn(planetB))

        self.add(clock)
        self.wait(3)
        self.play(AnimationGroup(clockmove.animate(run_time=10, rate_func=linear).shift(RIGHT*8), 
                                 advance_clock(0, 9)))

        # self.play(clock.animate.scale(0.3).shift(LEFT))
        # self.bring_to_front()

        self.wait(10)


class Triplets(MovingCameraScene):
    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")

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
        Emerald = ManimColor.from_hex("#23CE6B")
        FakeRaspberry = ManimColor.from_hex("#F72585")
        MateOrange = ManimColor.from_hex("#E4572E")
        
        Acolor = LightBlue
        Acolor2 = MistyBlue
        Bcolor = Emerald
        Bcolor2 = VibrantGreen
        Ccolor = GoodOrange
        Ccolor2 = NeonOrange
        propercolor=Samoyed
        lightcolor = Mustard
        
        def gli(line1, line2):
            p1, p2 = line1.get_start(), line1.get_end()
            p3, p4 = line2.get_start(), line2.get_end()

            # Direction vectors
            d1 = p2 - p1
            d2 = p4 - p3

            # Solve for intersection using determinant
            matrix = np.array([d1[:2], -d2[:2]]).T
            if np.linalg.det(matrix) == 0:
                return None  # Lines are parallel or coincident

            b = p3[:2] - p1[:2]
            t_vals = np.linalg.solve(matrix, b)

            # Optional: check if intersection is within segments (0 ≤ t ≤ 1)
            if not (0 <= t_vals[0] <= 1 and 0 <= t_vals[1] <= 1):
                return None  # Intersection is outside segment

            intersection = p1 + t_vals[0] * d1
            return intersection


        def get_lorentz_axes(gndaxes, observer, velocity):
            if velocity < 0:
                v = -velocity
                neg= -1
            else:
                v = velocity
                neg=1

            obs_pos = observer.get_center()

            gammav = 1/np.sqrt(1-v**2)

            xphatv = np.array([neg*1,v,0])/np.linalg.norm(np.array([1,v,0]))
            tphatv = np.array([neg*v,1,0])/np.linalg.norm(np.array([v,1,0]))

            axlengthx = 5
            axlengtht = 5

            xpax = Line(obs_pos, obs_pos + xphatv*axlengthx)
            tpax = Line(obs_pos, obs_pos + tphatv*axlengtht)

            return VGroup(xpax, tpax)
        

        def get_lorentz_vectors(observer, velocity):
            if velocity < 0:
                v = -velocity
                neg= -1
            else:
                v = velocity
                neg=1

            obs_pos = observer.get_center()

            gammav = 1/np.sqrt(1-v**2)

            xphatv = np.array([neg*1,v,0])/np.linalg.norm(np.array([1,v,0]))
            tphatv = np.array([neg*v,1,0])/np.linalg.norm(np.array([v,1,0]))


            return [xphatv, tphatv]


        Aax = Axes(x_range=[0, 10, 1], y_range=[0,10,1], x_length=7, y_length=7,axis_config={"include_ticks": False,"stroke_width":3.5}).set_color(Acolor2)
        Aaxlabel = Aax.get_axis_labels(x_label="x", y_label="t").set_color(Acolor2)

        # gndgrid = NumberPlane(x_range=[1, 10, 1],  y_range=[1,10,1], x_length=7, y_length=7,
        # background_line_style={"stroke_color": MistyBlue,
        #                         "stroke_width": 1,
        #                         "stroke_opacity": 0.5,})

        og = Aax.c2p(0,0)
        ogdot = Dot(og).set_color(propercolor)
        xhat = np.array([1,0,0])*0.7  #normalize with xrange and xlen
        that = np.array([0,1,0])*0.7
        light_line = DashedLine(start=og, end=Aax.c2p(10,10)).set_color(Mustard).set_opacity(0.75)
        light_label = MathTex("x=ct").next_to(light_line.get_end()).set_color(Mustard).set_opacity(0.75)

        v = 0.70
        gamma = 1/np.sqrt(1-v**2)

        xphat = np.array([1,v,0])/np.linalg.norm(np.array([1,v,0]))
        tphat = np.array([v,1,0])/np.linalg.norm(np.array([v,1,0]))

        Bpath = Line(og, og+tphat*7.5, stroke_width=6.5).set_color(Emerald)
        Lac_prop = Aax.p2c(Bpath.get_end())[0]  # set the first proper distance wherever the path looks good
        print(Lac_prop)

        A_a = Dot(og, radius=0.15).set_color(LightBlue)
        B_a = Dot(Aax.c2p(0, 0), radius=0.15).set_color(Emerald)
        C_a = Dot(Aax.c2p(Lac_prop,0), radius=0.15).set_color(NeonOrange)

        Alabel = always_redraw(lambda: MathTex("A").next_to(A_a, LEFT).set_color(Acolor))
        Blabel = always_redraw(lambda: MathTex("B").next_to(B_a, RIGHT+UP).set_color(Bcolor))
        Clabel = always_redraw(lambda: MathTex("C").next_to(C_a, RIGHT+UP).set_color(Ccolor))

        Bpath_firsthalf = Line(og, og+tphat*7.5/2, stroke_width=6.5).set_color(Emerald)
        Bpath_secondhalf = Line(og+tphat*7.5/2, og+tphat*7.5, stroke_width=6.5).set_color(Emerald)
        Bpathend_t = gli(Line(Bpath.get_end(), Bpath.get_end()-xhat*15), Aax.y_axis)
        Bpathend_x = gli(Line(Bpath.get_end(), Bpath.get_end()-that*15), Aax.x_axis)
        Apath = Line(og, Bpathend_t, stroke_width=6.5).set_color(LightBlue)
        Apath_firsthalf = Line(og, Apath.get_center(), stroke_width=6.5).set_color(LightBlue)
        Apath_secondhalf = Line(Apath.get_center(), Apath.get_end(), stroke_width=6.5).set_color(LightBlue)
        Cpath = Line(Bpathend_x, Apath.get_end(), stroke_width=6.5).set_color(NeonOrange)
        BCmeet_A = Dot(gli(Bpath, Cpath), radius=0.16).set_color(propercolor)
        Cpath_firsthalf = Line(Bpathend_x, BCmeet_A.get_center(), stroke_width=6.5).set_color(NeonOrange)
        Cpath_secondhalf = Line(BCmeet_A.get_center(), Apath.get_end(), stroke_width=6.5).set_color(NeonOrange)
        paths = [Bpath, Apath, Cpath]

        Apathlabel = MathTex("A").next_to(Apath.get_center(), LEFT).set_color(Acolor)
        Bpathlabel = MathTex("B").next_to(Bpath.get_end(), RIGHT).set_color(Bcolor)
        Cpathlabel = MathTex("C").next_to(Cpath.get_end(), RIGHT).set_color(Ccolor).shift(RIGHT*0.2)

        traceB = TracedPath(B_a.get_center, stroke_color=Bcolor, stroke_width=3)
        traceA = TracedPath(A_a.get_center, stroke_color=Acolor, stroke_width=3)
        traceC = TracedPath(C_a.get_center, stroke_color=Ccolor, stroke_width=3)
        traces = [traceA, traceB, traceC]

        # A Frame Show:
        self.play(Create(Aax), Write(Aaxlabel))
        self.wait(2)
        self.play(Create(A_a),Create(B_a),Create(C_a))
        self.play(Create(Alabel), Create(Blabel), Create(Clabel))
    
        self.add(*traces)
        
        self.bring_to_front(*[A_a, B_a, C_a])

        self.play(MoveAlongPath(A_a, Apath, rate_func=linear), MoveAlongPath(B_a, Bpath, rate_func=linear), 
        MoveAlongPath(C_a, Cpath, rate_func=linear), run_time=5)


        Alabelnrd = MathTex("A").next_to(A_a, LEFT).set_color(Acolor)
        Blabelnrd = MathTex("B").next_to(B_a, RIGHT+UP).set_color(Bcolor)
        Clabelnrd = MathTex("C").next_to(C_a, RIGHT+UP).set_color(Ccolor)

        self.add(*[Alabelnrd, Blabelnrd, Clabelnrd])
        self.remove(*[Alabel, Blabel, Clabel])
        self.wait()
        self.play(FadeOut(*traces), FadeIn(*paths), FadeOut(*[A_a,B_a,C_a]), 
        Alabelnrd.animate(run_time=4).move_to(Apathlabel.get_center()),
        Blabelnrd.animate(run_time=4).move_to(Bpathlabel.get_center()),
        Clabelnrd.animate(run_time=4).move_to(Cpathlabel.get_center()))

        self.remove(*[Alabelnrd, Blabelnrd, Clabelnrd])
        self.add(*[Apathlabel, Bpathlabel, Cpathlabel])

        self.wait(2)

        self.add(Bpath_firsthalf, Cpath_firsthalf, Cpath_secondhalf)
        self.remove(Cpath)

        A_a.move_to(Apath.get_start())
        B_a.move_to(Bpath.get_start())
        C_a.move_to(Cpath.get_start())

        self.play(Create(A_a), Create(B_a), Create(C_a))
        
        self.play(MoveAlongPath(A_a, Apath_firsthalf, rate_func=linear), MoveAlongPath(B_a, Bpath_firsthalf, rate_func=linear), 
        MoveAlongPath(C_a, Cpath_firsthalf, rate_func=linear), run_time=4)
        self.play(B_a.animate.set_opacity(0.3), C_a.animate.set_opacity(0.3))
        self.play(ReplacementTransform(Bpath_firsthalf, BCmeet_A), run_time=2)
        self.bring_to_front(BCmeet_A)
        self.play(Cpath_firsthalf.animate.set_color(Bcolor))
        self.bring_to_front(BCmeet_A)
        tc_eq_tb_a = MathTex("t_c = t_b").set_color(propercolor).next_to(BCmeet_A, RIGHT)
        tc_eq_tb_a1 = MathTex("t_c = ", "t_0").set_color(Ccolor).next_to(BCmeet_A, RIGHT)
        tc_eq_tb_a1[1].set_color(Bcolor)
        ta_atbc = MathTex("t_a = \gamma ", " t_0").set_color(Acolor).next_to(Apath.get_center(), LEFT).shift(LEFT)
        ta_atbc[1].set_color(Bcolor)
        self.play(Write(tc_eq_tb_a))
        self.wait()
        self.play(Transform(tc_eq_tb_a, tc_eq_tb_a1))
        self.wait()
        self.play(Write(ta_atbc))


        self.play(B_a.animate.set_opacity(1), C_a.animate.set_opacity(1), run_time=2)
        self.play(MoveAlongPath(A_a, Apath_secondhalf, rate_func=linear), MoveAlongPath(B_a, Bpath_secondhalf, rate_func=linear), 
        MoveAlongPath(C_a, Cpath_secondhalf, rate_func=linear), run_time=4)
        self.wait()

        ta_at_end = MathTex("T_a = 2\gamma ","t_0").set_color(Acolor).next_to(Apath.get_end(), LEFT+DOWN).shift(DOWN*0.2)
        tc_at_end = MathTex("T_c = 2","t_0").set_color(Ccolor).next_to(Cpath.get_end(), RIGHT).shift(LEFT*2.5)
        ta_at_end[1].set_color(Bcolor)
        tc_at_end[1].set_color(Bcolor)
        tc_tadivgamma = MathTex(r"T_c = \frac{T_a}{\gamma}").set_color(propercolor).move_to(BCmeet_A).shift(RIGHT*2)
        halfwaypt = DashedLine(BCmeet_A.get_left(), Apath.get_center()).set_color(Acolor)

        self.play(FadeOut(*[A_a, B_a, C_a]))
        self.play(Create(halfwaypt),run_time=2)
        self.wait(2)
        self.play(Transform(tc_eq_tb_a, tc_at_end), Transform(ta_atbc, ta_at_end), run_time=3)
        self.wait(2)
        self.play(Write(tc_tadivgamma), run_time=2)
        self.wait(3)

        Aframe = VGroup(Aaxlabel, Apathlabel, Bpathlabel, Cpathlabel, tc_eq_tb_a, ta_atbc, tc_tadivgamma)

        ############################################################################################################################
        # let's get a B frame:
        
        Bax = Axes(x_range=[-8, 5, 1], y_range=[0,12,1], x_length=7*1.3, y_length=7*1.2,axis_config={"include_ticks": False,"stroke_width":4.5}).set_color(Bcolor)
        axshift_AB = og-Bax.c2p(0,0)
        Bax.shift(axshift_AB)
        baxlabelx = MathTex("x_B").next_to(Bax.x_axis.get_end(), DOWN).set_color(Bcolor)
        baxlabelnx = MathTex("-x_B").next_to(Bax.x_axis.get_left(), DOWN).set_color(Bcolor)
        baxlabelt = MathTex("t_B").next_to(Bax.y_axis.get_end(), RIGHT).set_color(Bcolor)
        Baxlabel = VGroup(baxlabelx, baxlabelt, baxlabelnx)

        Bax_xline = Line(Bax.c2p(-8,0), Bax.c2p(5,0), stroke_width=5).set_color(Bcolor)
        Bax_yline = Line(Bax.c2p(0,0), Bax.c2p(0,12), stroke_width=5).set_color(Bcolor)
        Baxlines = VGroup(Bax_xline, Bax_yline)
        Baxlines0 = Baxlines.copy()

        Aax_xline = Line(Aax.c2p(0,0), Aax.c2p(10,0), stroke_width=5).set_color(Acolor2)
        Aax_yline = Line(Aax.c2p(0,0), Aax.c2p(0,10), stroke_width=5).set_color(Acolor2)
        Aaxlines = VGroup(Aax_xline, Aax_yline)

        V_aB = v
        V_cB = 2*v/(1+v**2)

        gammaB = 1/np.sqrt(1-V_cB**2)
        print(gammaB)

        Lac_B = Lac_prop/gammaB
        A_b = Dot(og).set_color(Acolor)
        B_b = Dot(og).set_color(Bcolor)
        C_b = Dot(Bax.c2p(Lac_B,0))

        xphat_a_B = np.array([-1, V_aB, 0])/np.linalg.norm(np.array([1, V_aB, 0]))
        tphat_a_B = np.array([-V_aB, 1, 0])/np.linalg.norm(np.array([V_aB, 1, 0]))

        xphat_c_B = np.array([-1, V_cB,0])/np.linalg.norm([1, V_cB,0])
        tphat_c_B = np.array([-V_cB, 1 ,0])/np.linalg.norm([V_cB, 1 ,0])

        C_b_axes = get_lorentz_axes(Bax, C_b, -V_cB).set_color(Ccolor)
        A_b_axes = get_lorentz_axes(Bax, A_b, -V_aB).set_color(Acolor)

        Apathghost_b = Line(A_b.get_center(),A_b.get_center()+tphat_a_B*20)        
        Cpathghost_b = Line(C_b.get_center(), C_b.get_center() +tphat_c_B*20)
        endpt_B = Dot(gli(Cpathghost_b, Apathghost_b), radius=0.1).set_color(propercolor)

        Cpath_b = Line(C_b.get_center(), endpt_B.get_center()+tphat_c_B, stroke_width=7.5).set_color(Ccolor)
        Apath_b = Line(A_b.get_center(), endpt_B.get_center()+tphat_a_B, stroke_width=7.5).set_color(Acolor)
        Bpath_b = Line(og, [og[0], endpt_B.get_y(),0], stroke_width=7.5).set_color(Bcolor2)

        BCmeet_b = Dot(gli(Cpath_b, Bpath_b), radius=0.16).set_color(propercolor)
        tc_eq_tb_b = MathTex("t_c = ", "t_0")
        tc_eq_tb_b[0].set_color(Ccolor)
        tc_eq_tb_b[1].set_color(Bcolor)
        Cpath0_b = Line(C_b.get_center(), BCmeet_b.get_center(), stroke_width=7.5).set_color(Ccolor)
        Cpath1_b = Line(BCmeet_b.get_center(), endpt_B.get_center(),stroke_width=7.5).set_color(Ccolor)

        Bpath_b0 = Line(og, BCmeet_b.get_center(), stroke_width=7.5).set_color(Bcolor2)
        Bpath_b1 = Line(BCmeet_b.get_center(), [og[0], endpt_B.get_y(),0], stroke_width=7.5).set_color(Bcolor2)

        Apath_b0 = Line(A_b.get_center(), BCmeet_b.get_center(), stroke_width=7.5).set_color(Acolor)
        Apath_b1 = Line(BCmeet_b.get_center(), endpt_B.get_center()+tphat_a_B, stroke_width=7.5).set_color(Acolor)


        Alabel_b = MathTex("A").next_to(Apath_b.get_center(), LEFT+DOWN).set_color(Acolor)
        Clabel_b = MathTex("C").next_to(Cpath_b.get_center(), RIGHT+UP).set_color(Ccolor)
        Blabel_b = MathTex("B").next_to(Bpath_b.get_center(), RIGHT).set_color(Bcolor)

        endpt_B = Dot(gli(Cpathghost_b, Apathghost_b), radius=0.15).set_color(propercolor)


        # transforming A frame to B frame
        self.play(FadeOut(BCmeet_A), FadeOut(halfwaypt))
        self.play(FadeIn(Cpath), FadeOut(Cpath_firsthalf, Cpath_secondhalf))

        self.play(ReplacementTransform(Aax, Aaxlines), FadeOut(*Aframe))
        self.play(Aaxlines.animate.set_opacity(0.3))
        self.play(ReplacementTransform(Bpath, Bax_yline), ReplacementTransform(Apath, Apath_b),
                  ReplacementTransform(Cpath, Cpath_b), self.camera.frame.animate.shift(axshift_AB).scale(1.2), run_time=4)
        
        self.play(FadeOut(Aaxlines), Create(Bax), Create(Alabel_b), Create(Clabel_b), Create(Baxlabel), Create(Bpath_b), Create(Blabel_b), run_time=3)
        self.play(FadeOut(Bax_yline))
        self.wait(2)
        self.play(Create(endpt_B))

        # Retrace the paths:
        self.play(Indicate(Bpath_b))
        self.wait(2)
        Adot_b = Dot(Apath_b.get_start(), radius=0.15).set_color(Acolor2)
        Bdot_b = Dot(Bpath_b.get_start(), radius=0.15).set_color(Bcolor2)
        Cdot_b = Dot(Cpath_b.get_start(), radius=0.15).set_color(Ccolor2)

        self.play(FadeIn(*[Adot_b, Bdot_b, Cdot_b]))
        
        Dotmoves_b = AnimationGroup(MoveAlongPath(Adot_b, Line(Apath_b.get_start(), endpt_B.get_center()), rate_func=linear), 
                  MoveAlongPath(Bdot_b, Bpath_b, rate_func=linear), 
                  MoveAlongPath(Cdot_b, Line(Cpath_b.get_start(), endpt_B.get_center()), rate_func=linear), run_time=10)
        Bpath_b00 = Bpath_b0.copy()
        Cpath0_bcolor = Cpath0_b.copy().set_color(Bcolor2)
        handofftime_b = AnimationGroup(Wait(2), AnimationGroup(Transform(Bpath_b00, Cpath0_bcolor, run_time=2),
                        Transform(Bpath_b0, BCmeet_b, run_time=2), lag_ratio=0), lag_ratio=1)

        self.play(AnimationGroup(Dotmoves_b, handofftime_b, lag_ratio=0))

        self.wait(5)

        # Show length contraction from L between A and C to L/gamma
        self.play(self.camera.frame.animate.shift(RIGHT*4+DOWN).scale(1.20), run_time=3)

        brace_Ldivgamma = BraceBetweenPoints(Apath_b.get_start(), Cpath_b.get_start()).set_color(propercolor)
        label_Ldivgamma = MathTex(r"\frac{L}{\gamma}").set_color(propercolor).next_to(brace_Ldivgamma, DOWN)

        self.play(FadeIn(brace_Ldivgamma))
        self.play(Write(label_Ldivgamma))

        self.wait(3) 
        self.play(FadeOut(*[brace_Ldivgamma, label_Ldivgamma]), self.camera.frame.animate.shift(UP).scale(1.10/1.20), run_time=2)
        self.wait(2)


        # Show C velocity with velocity addition formula
        vc_atext = MathTex(r"v_{\scriptstyle C}\text{ as measured by A }= v").set_color(Acolor).scale(1.3).shift(RIGHT*3+UP*4)
        vc_a = MathTex(r"v_{\scriptscriptstyle C(A)} = v").set_color(Acolor).scale(1.4).next_to(vc_atext, DOWN).shift(DOWN*0.5)

        vc_aprime = MathTex(r"v_{\scriptscriptstyle C(A)} = ", r"\frac{\Delta x'}{\Delta t'}").set_color(Acolor).scale(1.4).next_to(vc_atext, DOWN).shift(LEFT*2+DOWN*0.5)
        vc_aB = MathTex(r"v_{\scriptscriptstyle C(B)} = ", r"\frac{\Delta x}{\Delta t}").set_color(Bcolor).scale(1.4).next_to(vc_aprime, RIGHT).shift(RIGHT*0.5)
        vc_aB1 = MathTex(r"v_{\scriptscriptstyle C(B)} = ", r"\frac{\Delta x}{\Delta t}=", 
                         r"\frac{\gamma \left(\Delta x' + v \Delta t'\right)}{\gamma \left(\Delta t' + \frac{v}{c^2}\Delta x'\right)}").set_color(Bcolor).scale(1.4).next_to(vc_atext, DOWN).shift(DOWN*2)
        
        vc_aB2 = MathTex(r"v_{\scriptscriptstyle C(B)} = ", r"\frac{\Delta x}{\Delta t}=", 
                         r"\frac{\left(\Delta x' + v \Delta t'\right)}{\left(\Delta t' + \frac{v}{c^2}\Delta x'\right)}").set_color(Bcolor).scale(1.4).next_to(vc_aB1, DOWN).shift(DOWN*0.5)
        
        vc_aB3 = MathTex("v_{\scriptscriptstyle C(B)} = ", r"\frac{\Delta x}{\Delta t}=", 
                r"\frac{\left(\frac{\Delta x'}{\Delta t'} + v \frac{\Delta t'}{\Delta t'}\right)}{\left(\frac{\Delta t'}{\Delta t'} + \frac{v}{c^2}\frac{\Delta x'}{\Delta t'}\right)}",
                ).set_color(Bcolor).scale(1.4).next_to(vc_aB2, DOWN)


        # vc_aB3.set_color_by_tex_to_color_map({r"\frac{\Delta x'}{\Delta t'}": Acolor})

        vc_aB4 = MathTex(r"v_{\scriptscriptstyle C(B)} = ", r"\frac{\Delta x}{\Delta t}=", r"\frac{v_{\scriptscriptstyle C(A)} + v}{1 + \frac{v\,v_{\scriptscriptstyle C(A)}}{c^2}}").set_color(Bcolor).scale(1.4).next_to(vc_atext, DOWN).shift(DOWN)

        vc_aBresult = MathTex(r"v_{\scriptscriptstyle C(B)} = ", r"\frac{2v}{1+\frac{v^2}{c^2}}").set_color(Bcolor).scale(1.4).next_to(vc_atext, DOWN).shift(DOWN+LEFT)
        vc_aBnatty = MathTex(r"\implies", r"v_{\scriptscriptstyle C(B)} = ", r"\frac{2v}{1+v^2}").set_color(Bcolor).scale(1.4).next_to(vc_atext, DOWN).shift(DOWN)

        self.play(Write(vc_atext))
        self.wait(2)
        self.play(Write(vc_a))
        self.wait(2)
        self.play(FadeOut(vc_atext), vc_a.animate.move_to(vc_atext.get_center()))

        self.wait()
        self.play(Write(vc_aprime))


        self.wait()
        self.play(Write(vc_aB))
        self.wait(3)
        self.play(FadeOut(vc_a), vc_aprime.animate.shift(UP).scale(0.9))
        self.play(vc_aB.animate.move_to(vc_aprime.get_right()).shift(RIGHT*2.5).scale(0.9))

        self.wait()
        self.play(Write(vc_aB1))

        self.wait()
        self.play(Write(vc_aB2))
        self.wait(3)
        self.play(FadeOut(*[vc_aB, vc_aprime, vc_aB1]), vc_aB2.animate(run_time=2).move_to(vc_aprime).shift(RIGHT*1.5).scale(0.9))

        self.wait(2)
        vc_aB3.next_to(vc_aB2, DOWN).shift(DOWN*0.5)
        self.play(Write(vc_aB3))
        
        self.wait()
        vc_aB4.next_to(vc_aB3, DOWN).shift(DOWN*0.5)
        self.play(Write(vc_aB4))
        self.wait(2)

        self.wait(2)
        self.play(FadeOut(*[vc_aB2, vc_aB3]), vc_aB4.animate.move_to(vc_aprime).shift(RIGHT*2))
        vc_aBresult.next_to(vc_aB4, DOWN).shift(DOWN*0.4)
        self.play(Write(vc_aBresult))
        self.wait(2)

        self.wait(3)

        self.play(vc_aBresult.animate.shift(LEFT*2).scale(0.9))
        setc1 = MathTex("c=1").next_to(vc_aBresult, RIGHT).shift(RIGHT).scale(1.4).set_color(lightcolor)

        self.play(Write(setc1))
        vc_aBnatty.move_to(vc_aBresult).shift(DOWN*2.5+RIGHT*1.3).scale(1.1)
        vc_aBnatty[0].set_color(lightcolor)
        self.play(Write(vc_aBnatty))
        self.wait(3)
        self.play(FadeOut(*[vc_aB4, vc_aBresult, setc1]))
        self.play(vc_aBnatty.animate.shift(UP*2))
        self.wait(3)

        # Show B-C handoff time, difference in A's clock, calculate the rest
        
        Bframe = VGroup(Baxlabel, Adot_b, Bdot_b, Cdot_b, endpt_B, Alabel_b, Clabel_b, Blabel_b, Bpath_b00, Bpath_b0)
        
        #########################################################################################################################################
        # let's get a C frame:
        
        Cax = Axes(x_range=[-5, 5, 1], y_range=[0,10,1], x_length=7, y_length=7,axis_config={"include_ticks": False,"stroke_width":4.5}).set_color(Ccolor2)
        Caxlabel = Aax.get_axis_labels(x_label="x_C", y_label="t_C").set_color(Ccolor2)
        axshift_BC = og-Cax.c2p(0,0)
        Cax.shift(axshift_BC)

        Cax_xline = Line(Cax.c2p(-5,0), Cax.c2p(5,0), stroke_width=5).set_color(Ccolor)
        Cax_yline = Line(Cax.c2p(0,0), Cax.c2p(0,10), stroke_width=5).set_color(Ccolor)
        Caxlines = VGroup(Cax_xline, Cax_yline)

        V_aC = v
        V_bC = 2*v/(1+v**2)

        gammaCB = 1/np.sqrt(1-V_bC**2)
        print(gammaCB)

        Lac_C = Lac_prop/gamma
        A_c = Dot(Cax.c2p(-Lac_C, 0), radius=0.15).set_color(Acolor)
        B_c = Dot(Cax.c2p(-Lac_C, 0), radius=0.15).set_color(Bcolor)
        C_c = Dot(og, radius=0.15).set_color(Ccolor)

        xphat_a_C = np.array([1, V_aC, 0])/np.linalg.norm(np.array([1, V_aC, 0]))
        tphat_a_C = np.array([V_aC, 1, 0])/np.linalg.norm(np.array([V_aC, 1, 0]))

        xphat_b_C = np.array([1, V_bC,0])/np.linalg.norm([1, V_bC,0])
        tphat_b_C = np.array([V_bC, 1 ,0])/np.linalg.norm([V_bC, 1 ,0])

        B_c_axes = get_lorentz_axes(Cax, C_c, V_bC).set_color(Bcolor)
        A_c_axes = get_lorentz_axes(Cax, A_c, V_aC).set_color(Acolor)

        Apathghost_c = Line(A_c.get_center(),A_c.get_center()+tphat_a_C*20).set_color(Acolor)
        Bpathghost_c = Line(B_c.get_center(), B_c.get_center() +tphat_b_C*20).set_color(Bcolor)

        Apath_c = Line(A_c.get_center(), gli(Apathghost_c, Cax.y_axis) + tphat_a_C).set_color(Acolor)
        Bpath_c = Line(B_c.get_center(), gli(Bpathghost_c, Cax.y_axis) + tphat_b_C*1.9).set_color(Bcolor)
        Bpath_cMOVE = Line(B_c.get_center(), gli(Bpathghost_c, Cax.y_axis) + tphat_b_C*1.55).set_color(Bcolor)

        Cpath_c = Line(og, gli(Apathghost_c, Cax.y_axis)).set_color(Ccolor)
        BCmeet_C = Dot(gli(Bpath_c, Cpath_c), radius=0.16).set_color(propercolor)

        Bpath_c0 = Line(B_c.get_center(), BCmeet_C.get_center()).set_color(Bcolor)
        Bpath_c1 = Line(BCmeet_C.get_center(), gli(Bpathghost_c, Cax.y_axis) + tphat_b_C*1.9).set_color(Bcolor)
        Cpath_c0 = Line(og, BCmeet_C.get_center()).set_color(Ccolor)
        Cpath_c1 = Line(BCmeet_C.get_center(), gli(Apathghost_c, Cax.y_axis)).set_color(Ccolor)

        # transforming b frame to c frame:
        transform_BC = AnimationGroup(ReplacementTransform(Bpath_b, Bpath_c), ReplacementTransform(Apath_b, Apath_c), 
                ReplacementTransform(Cpath_b, Cax_yline), run_time=7)
        
        self.play(FadeOut(*Bframe), ReplacementTransform(Bax, Baxlines0))
        self.play(Baxlines0.animate.set_opacity(0.3))
        self.play(AnimationGroup(transform_BC, self.camera.frame.animate(run_time=8).scale(0.9).shift(RIGHT*1.2+DOWN*0.6)))
        self.play(FadeOut(Baxlines0), Create(Cax))
        self.play(FadeOut(Cax_yline))
        self.wait(3)

        self.play(Create(A_c), Create(B_c), Create(C_c))

        Dotmoves_c = AnimationGroup(MoveAlongPath(A_c, Line(Apath_c.get_start(),gli(Apathghost_c, Cax.y_axis)), rate_func=linear), 
                  MoveAlongPath(B_c, Bpath_cMOVE, rate_func=linear), 
                  MoveAlongPath(C_c, Cpath_c, rate_func=linear), run_time=8)

        Bpath_c00 = Bpath_c0.copy()
        Cpath0_ccolor = Cpath_c0.copy().set_color(Bcolor)
        handofftime_c = AnimationGroup(Wait(5.5), AnimationGroup(Transform(Bpath_c00, Cpath0_ccolor, run_time=2),
                        Transform(Bpath_c0, BCmeet_C, run_time=2)), lag_ratio=1)

        self.play(AnimationGroup(Dotmoves_c, handofftime_c, lag_ratio=0))

        self.wait(2)
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN))
        
        brace_Ldivgamma_c = BraceBetweenPoints(Apath_c.get_start(), Cpath_c.get_start()).set_color(propercolor)
        label_Ldivgamma_c = MathTex(r"\frac{L}{\gamma}").set_color(propercolor).next_to(brace_Ldivgamma_c, DOWN)
        self.play(Write(label_Ldivgamma_c), FadeIn(brace_Ldivgamma_c))
        self.wait(2)
        self.play(FadeOut(*[label_Ldivgamma_c, brace_Ldivgamma_c]),self.camera.frame.animate.scale(1/1.1).shift(UP))

        # Show B velocity with velocity addition formula
        # Show B-C handoff time, difference in A's clock, calculate the rest
        self.wait(10)


