
class TripletsIntro(MovingCameraScene):
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

        gndcolor1 = SkyBlue
        gndcolor2 = SteelBlue
        gndhighlight = LightBlue
        pcolor1 = OrangeOrange
        pcolor2=GoodOrange
        phighlight = NeonOrange
        highlight = VibrantGreen
        propercolor = Samoyed



        # Background stars:
        stars = VGroup()
        for i in range(1100):
            xs = np.random.uniform(-15,20)
            ys = np.random.uniform(-15,15)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)
        self.camera.frame.scale(1)
        self.add(stars)
        
        A = ImageMobject("Andy.png").scale(0.12)
        B = ImageMobject("Bob.png").shift(LEFT*2.5).scale(0.25).shift(DOWN*0.3)
        C = ImageMobject("Charlie.png").shift(RIGHT*2.5).scale(0.25).shift(DOWN*0.3)

        planetA = ImageMobject("earth.png").scale(0.35).to_corner(DL)
        planetC = ImageMobject("planet1.png").scale(0.35).to_corner(DR)

        rocketB = ImageMobject("rocket.png").scale(0.3).to_corner(UL).shift(LEFT*4+UP*0.5)
        Bghost = B.copy().scale(0.5).set_opacity(0).move_to(rocketB.get_center())
        rocketC = ImageMobject("rocketblue.png").move_to(planetC.get_center()).shift(UP*2).scale(0.3).stretch(-1, dim=0)
        Cghost = C.copy().scale(0.5).set_opacity(0).move_to(rocketC.get_center())
        Aghost = A.copy().scale(0.5).set_opacity(0).move_to(planetA.get_center())

        rocketBv = always_redraw(lambda: Arrow(rocketB.get_right(), [rocketB.get_x()+3.3, rocketB.get_y(), 0]).shift(UP*0.1).set_color(propercolor))
        Bvlabel = always_redraw(lambda: MathTex("v").move_to(rocketBv.get_end()).shift(RIGHT*0.3))

        rocketCv = always_redraw(lambda: Arrow(rocketC.get_left(), [rocketC.get_x()-3.3, rocketC.get_y(), 0]).set_color(propercolor))
        Cvlabel = always_redraw(lambda: MathTex("v").move_to(rocketCv.get_end()).shift(LEFT*0.3))

        clockscale = 0.2
        clockimg = ImageMobject("clock.png").scale(clockscale)
        clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale))
        clockcenter = always_redraw(lambda:Dot(clockimg.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
        clock12 = always_redraw(lambda:Dot(clockimg.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetip = Dot(clock12.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
        clock0=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)

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
        
        n = 3
        clocksetarc = Arc(radius=2.9*clockscale, start_angle=PI/2-(n-1)*PI/6, 
                                angle=-PI/6, arc_center=clockcenter.get_center())
        clocklinetipN = clocklinetip.copy().move_to(clocksetarc.get_end())
        clocklineN = always_redraw(lambda:Line(clockimg.get_center(), clocklinetipN.get_center(), stroke_width=10*clockscale).set_color(BLACK))

        Nclock=Group(clockbg.copy(), clockimg.copy(), clocklineN, clock12.copy(), clockcenter.copy(), clocklinetipN)


        clockscale = 0.2
        clockimg6 = clockimg.copy()
        clockbg6 = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg6.get_center()).scale(clockscale))
        clockcenter6 = always_redraw(lambda:Dot(clockimg6.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
        clock126 = always_redraw(lambda:Dot(clockimg6.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
        clocklinetip6 = Dot(clock126.get_center()).set_color(VibrantGreen).set_opacity(0)
        # tickcircle = Circle(radius=2.9).set_color(GoodOrange).move_to(clockimg.get_center())
        clockline6 = always_redraw(lambda:Line(clockimg6.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))

        n6 = 6
        clocksetarc6 = Arc(radius=2.9*clockscale, start_angle=PI/2-(n6-1)*PI/6, 
                                angle=-PI/6, arc_center=clockcenter6.get_center())
        clocklinetip6 = clocklinetip6.move_to(clocksetarc6.get_end())
        clockline6 = always_redraw(lambda:Line(clockimg6.get_center(), clocklinetip6.get_center(), stroke_width=10*clockscale).set_color(BLACK))

        clock6=Group(clockbg6, clockimg6, clockline6, clock126, clockcenter6, clocklinetip6)


        # self.play(FadeIn(N6clock))

        # clockA = clock0.copy()
        clockB = clock0.copy()
        clockBN = Nclock.copy()
        clockCN = Nclock.copy()
        clockCNghost = clockCN.copy()
        clockCNghost.set_opacity(0)

        self.camera.frame.scale(0.5)
        self.play(AnimationGroup(FadeIn(A), FadeIn(B), FadeIn(C), lag_ratio=1))

        cam0 = self.camera.frame.get_center()
        self.play(self.camera.frame.animate.shift(LEFT*2).scale(2.6), run_time=2.5)
        self.wait()

        # self.play(FadeIn(A), FadeIn(B), FadeIn(C))
        self.play(FadeIn(planetA), FadeIn(planetC))
        self.play(FadeIn(rocketB), FadeIn(rocketC))

        self.play(Transform(A, Aghost), run_time=2)
        self.wait(2)
        self.play(Transform(B, Bghost), run_time=2)
        self.wait(2)
        self.play(Transform(C, Cghost), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate(run_time=2).shift(LEFT*3.5).scale(0.85))

        self.play(Create(rocketBv), Write(Bvlabel))
        self.play(rocketB.animate(run_time=1.5, rate_func=linear).move_to([planetA.get_x(), rocketB.get_y(), 0]))
        clockB.move_to(rocketB.get_center()).shift(DOWN*1.2+RIGHT*1.5)
        # self.add(clock0)
        clock0.move_to([clockB.get_x(), planetA.get_y(), 0]).shift(DOWN*1.2)
        # self.play(clock0.animate.move_to([clockB.get_x(), planetA.get_y(), 0]).shift(DOWN*1.2))

        self.play(FadeIn(*[clock0, clockB]))
        self.wait()
        self.play(self.camera.frame.animate(run_time=2).move_to(cam0).scale(1/0.85))

        self.play(FadeOut(clockB))

        self.wait(2)

        self.play(Create(rocketCv), Write(Cvlabel))
        self.play(AnimationGroup(rocketB.animate(run_time=4, rate_func=linear
        ).move_to(Line(rocketB.get_center(), [planetC.get_x(), rocketB.get_y(), 0]).get_center()),
                    rocketC.animate(run_time=4, rate_func=linear).move_to(
                        Line(rocketC.get_center(), [planetA.get_x(), rocketC.get_y(), 0]).get_center()),
                        advance_clock(0,4,runtime=4)))

 
        clockBN.move_to(rocketB.get_center()).shift(DOWN*1.2+RIGHT*1.5)
        clockCNghost.move_to(rocketC.get_center())
        # self.play(Create(clockpass_arc))
        # self.play(MoveAlongPath(clockBN, clockpass_arc))

        self.play(FadeIn(clockBN))
        # self.play(ReplacementTransform(clockBN, clockCNghost), run_time=2)
        # self.play(clockBN.animate.move_to(rocketC.get_center()).shift(DOWN*1.2+LEFT*1.5))
        Cclockpos = Dot(rocketC.get_center()).shift(UP*1.2+LEFT*1.5)
        clockpass_arc = ArcBetweenPoints(clockBN.get_center(), Cclockpos.get_center())
        self.play(MoveAlongPath(clockBN, clockpass_arc))

        self.wait(2)
        self.remove(clockBN)

        self.play(AnimationGroup(rocketB.animate(run_time=4, rate_func=linear
        ).move_to([planetC.get_x(), rocketB.get_y(), 0]).get_center(),
                    rocketC.animate(run_time=4, rate_func=linear).move_to([planetA.get_x(), rocketC.get_y(), 0]).get_center(),
                    advance_clock(4,8,runtime=4)))
        
        clock6.move_to(Dot(rocketC.get_center()).shift(UP*1.2+LEFT*1.5).get_center())
        self.add(clock6)
        
        self.play(FadeOut(*[Cvlabel, Bvlabel, rocketBv, rocketCv]), run_time=2)
        self.wait(2)
        self.play(Indicate(clockline6), Indicate(clockimg6), Indicate(clockline),Indicate(clockimg))
        self.wait(2)


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
        xhatBax = [Bax.c2p(1,0) - Bax.c2p(0,0)]

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
                  ReplacementTransform(Cpath, Cpath_b), self.camera.frame.animate.shift(axshift_AB).scale(1.25), run_time=4)
        
        self.play(FadeOut(Aaxlines), Create(Bax), Create(Alabel_b), Create(Clabel_b), Create(Baxlabel), Create(Bpath_b), Create(Blabel_b), run_time=3)
        self.play(FadeOut(Bax_yline))
        self.wait(2)
        self.play(Create(endpt_B))

        camposB0 = self.camera.frame.get_center()
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
        # self.play(self.camera.frame.animate.shift(RIGHT*4+DOWN).scale(1.20), run_time=3)

        # brace_Ldivgamma = BraceBetweenPoints(Apath_b.get_start(), Cpath_b.get_start()).set_color(propercolor)
        # label_Ldivgamma = MathTex(r"\frac{L}{\gamma}").set_color(propercolor).next_to(brace_Ldivgamma, DOWN)

        # self.play(FadeIn(brace_Ldivgamma))
        # self.play(Write(label_Ldivgamma))

        # self.play(FadeOut(*[brace_Ldivgamma, label_Ldivgamma]), self.camera.frame.animate.shift(UP).scale(1.10/1.20), run_time=2)
        self.play(self.camera.frame.animate.shift(RIGHT*4).scale(1.10), run_time=2)
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
        self.wait(2)
        vc_aBresult.next_to(vc_aB4, DOWN).shift(DOWN*0.4).shift(RIGHT*2)
        vc_a.next_to([vc_aB4.get_x(), vc_aBresult.get_y(), 0]).shift(LEFT*4)
        self.play(FadeIn(vc_a))
        self.wait(2)
        self.play(Write(vc_aBresult))
        self.wait(2)

        self.wait(2)

        self.play(FadeOut(vc_a), vc_aBresult.animate(run_time=2.5).shift(LEFT*4).scale(0.9))
        setc1 = MathTex("c=1").next_to(vc_aBresult, RIGHT).shift(RIGHT*1.5).scale(1.4).set_color(lightcolor)

        self.play(Write(setc1))
        vc_aBnatty.move_to(vc_aBresult).shift(DOWN*2.5+RIGHT*1.3).scale(1.1)
        vc_aBnatty[0].set_color(lightcolor)
        self.play(Write(vc_aBnatty))
        self.wait(3)
        self.play(FadeOut(*[vc_aB4, vc_aBresult, setc1]))
        vc = MathTex(r"v_{\scriptstyle C} = ", r"\frac{2v}{1+v^2}").set_color(Bcolor).scale(1.2).move_to(vc_aBnatty.get_center()).shift(UP*4+LEFT)
        va = MathTex("v_A = v").set_color(Bcolor).scale(1.2).move_to(vc_aBnatty.get_center()).shift(UP*4+RIGHT*3)

        self.play(ReplacementTransform(vc_aBnatty, vc))
        self.wait(2)
        self.play(Write(va))
        self.wait(5)
        self.play(FadeOut(*[vc, va]))



        # Show B-C handoff time, difference in A's clock, calculate the rest
        t0B = MathTex("t_0").scale(1.3).move_to(BCmeet_b.get_right()).shift(RIGHT*0.3+UP*0.2).set_color(propercolor)

        Aworldlineeq = MathTex("\Delta x_A", " = vt_0 ", "+ v\Delta t").scale(1.5).set_color(Acolor).move_to(vc.get_center()).shift(DOWN+RIGHT*2)
        t0A = gli(Line(BCmeet_b.get_center(), [BCmeet_b.get_x()-15, BCmeet_b.get_y(), 0]), Apath_b)
        t0Adash = DashedLine(BCmeet_b.get_left(), t0A).set_color(propercolor)
        Apart1 = Arrow(og, t0A, buff=0.05).set_color(propercolor)
        Apart2 = Arrow(t0A, endpt_B.get_center(), buff=0.05).set_color(propercolor)

        self.play(Write(t0B))

        self.wait(2)
        self.play(Write(Aworldlineeq[0]))
        self.play(Create(t0Adash))
        self.play(Create(Apart1))
        self.wait(2)
        self.play(Write(Aworldlineeq[1]))
        self.wait(2)

        self.play(FadeOut(Apart1), Create(Apart2))
        self.wait(2)
        self.play(Write(Aworldlineeq[2]))
        self.wait(2)
        self.play(FadeOut(Apart2), FadeOut(t0Adash))
        self.wait(2)


        Cpart1 = Arrow(BCmeet_b.get_center(), endpt_B.get_center(), buff=0.05).set_color(propercolor)
        Cworldlineeq = MathTex("\Delta x_C = v_C \Delta t").scale(1.5).move_to(Aworldlineeq.get_center()).shift(DOWN*2+LEFT*0.7).set_color(Ccolor)
        Cclock0 = MathTex(r"t_{\scriptstyle C_0} = t_0").scale(1.5).move_to(Cworldlineeq.get_center()).shift(RIGHT*4).set_color(Bcolor2)

        self.wait(2)
        self.play(Create(Cpart1))
        self.wait(2)
        self.play(Write(Cworldlineeq))
        self.wait(2)
        self.play(Write(Cclock0))
        self.wait(3)
        self.play(FadeOut(Cclock0), FadeOut(Cpart1))


        self.wait(4)
        self.play(self.camera.frame.animate(run_time=2).shift(LEFT+DOWN).scale(1.1))
        meetdist = DashedLine(endpt_B.get_center(), [endpt_B.get_x(), og[1], 0]).set_color(propercolor)
        traveldist = Arrow(og, meetdist.get_end(), buff=0.05).set_color(propercolor)
        xaeqxc = MathTex("\Delta x_A", " = ", "\Delta x_C").move_to(traveldist.get_center()).shift(DOWN).scale(1.2)
        xaeqxc[0].set_color(Acolor)
        xaeqxc[1].set_color(propercolor)
        xaeqxc[2].set_color(Ccolor)

        self.play(Create(meetdist))
        self.wait(2)
        self.play(Create(traveldist))
        self.wait(2)
        self.play(Write(xaeqxc[0]))
        self.play(Write(xaeqxc[1]))
        self.play(Write(xaeqxc[2]))
        self.wait(2)
        self.play(AnimationGroup(xaeqxc.animate(run_time=3).move_to(Aworldlineeq.get_center()).shift(UP*2+RIGHT*3).scale(1.5),
                                 self.camera.frame.animate(run_time=2).shift(RIGHT*3+UP*1.5).scale(1.2)))
        self.play(xaeqxc[0].animate(run_time=3).shift(LEFT*0.6), xaeqxc[2].animate(run_time=3).shift(RIGHT*0.6))

        xaeqxcmath = MathTex("vt_0 + v\Delta t", " = ", "v_C \Delta t").scale(1.7).move_to(xaeqxc.get_center())
        xaeqxcmath[0].set_color(Acolor).shift(LEFT)
        xaeqxcmath[1].set_color(propercolor).shift(LEFT*0.3)
        xaeqxcmath[2].set_color(Ccolor)

        self.play(FadeOut(xaeqxc[0]), ReplacementTransform(Aworldlineeq, xaeqxcmath[0]))
        self.wait(2)
        self.play(ReplacementTransform(xaeqxc[1], xaeqxcmath[1]),
        FadeOut(xaeqxc[2]), ReplacementTransform(Cworldlineeq, xaeqxcmath[2]))

        self.wait(2)

        vcdud = vc.copy()
        vcdud.move_to(xaeqxcmath.get_center()).shift(DOWN*2).scale(1.5)
        self.play(FadeIn(vcdud))
        xaeqxcmath1 = MathTex("vt_0 + v\Delta t", " = ", r"\frac{2v}{1+v^2} \Delta t").scale(1.7).move_to(xaeqxc.get_center())
        xaeqxcmath1[0].set_color(Acolor)
        xaeqxcmath1[1].set_color(propercolor)
        xaeqxcmath1[2].set_color(Ccolor).shift(RIGHT*0.35)
        self.wait(2)
        self.play(FadeOut(xaeqxcmath[2]), ReplacementTransform(vcdud, xaeqxcmath1[2]))
        self.wait(2)
        self.play(ReplacementTransform(xaeqxcmath[0], xaeqxcmath1[0]),
                    ReplacementTransform(xaeqxcmath[1], xaeqxcmath1[1]),
                    xaeqxcmath1[2].animate.shift(LEFT*0.35))
        
        self.play(xaeqxcmath1.animate(run_time=2).set_color(Bcolor).shift(UP*2+LEFT*2))
        self.wait(2)
        xaeqxcmath2 = MathTex(r"vt_0 = \left(\frac{2v}{1+v^2} - v\right)\Delta t").scale(1.4).move_to(xaeqxcmath1.get_center()).shift(DOWN*3).set_color(Bcolor)
        xaeqxcmath3 = MathTex(r"t_0 = \left(\frac{2 - (1+v^2)}{1+v^2}\right)\Delta t").scale(1.4).move_to(xaeqxcmath2.get_center()).shift(DOWN*3).set_color(Bcolor)
        deltatresult = MathTex(r"\Delta t = \frac{1+v^2}{1-v^2}\,t_0").scale(1.4).move_to(xaeqxcmath3.get_center()).shift(DOWN*3).set_color(Bcolor2)
        self.play(Write(xaeqxcmath2))
        self.play(Write(xaeqxcmath3))
        self.wait(4)
        self.play(Write(deltatresult))

        self.wait(4)
        self.play(FadeOut(*[xaeqxcmath1, xaeqxcmath2, xaeqxcmath3]))
        self.play(deltatresult.animate(run_time=3).shift(UP*5+LEFT*2.5).scale(1.2).set_color(VibrantPink))
        deltatresultdud = deltatresult.copy()

        self.wait(2)
        deltB = Line(BCmeet_b, Bpath_b.get_end(), stroke_width=6).set_color(VibrantPink)
        self.play(Create(deltB), run_time=2)
        self.play(Indicate(deltB))

        self.wait(2)

        TB_b = MathTex("T_B = t_0 + \Delta t", " = t_0 + ", r"\frac{1+v^2}{1-v^2}\,t_0").move_to(Aworldlineeq.get_center()).shift(UP*2+RIGHT).scale(1.5).set_color(Bcolor)

        self.play(Write(TB_b[0]))
        self.wait(2)
        self.play(Write(TB_b[1]))
        self.wait()
        self.play(ReplacementTransform(deltatresult, TB_b[2]))
        self.play(FadeOut(deltB))
        

        TB_b1 = MathTex(r"T_B = \frac{1+v^2 + 1 - v^2}{1-v^2}\,t_0").move_to(TB_b.get_center()).shift(DOWN*3).scale(1.5).set_color(Bcolor)
        TB_b2 = MathTex(r"T_B = \frac{2t_0}{1-v^2}", r" = 2\gamma^2 t_0").move_to(TB_b1.get_center()).shift(DOWN*3).scale(1.5).set_color(Bcolor)
        gammanot = MathTex(r"\gamma = \frac{1}{\sqrt{1-v^2/c^2}}").move_to(TB_b2.get_center()).shift(DOWN*3).scale(1.5).set_color(lightcolor)
        gammanatty = MathTex(r"\gamma = \frac{1}{\sqrt{1-v^2}}").move_to(TB_b2.get_center()).shift(DOWN*3).scale(1.5).set_color(lightcolor)
        TB_bresult = MathTex(r"T_B = 2\gamma^2 t_0").move_to(TB_b.get_center()).scale(1.75).set_color(Bcolor)
        self.wait(2)
        self.play(Write(TB_b1))
        self.wait()
        self.play(Write(TB_b2[0]))
        self.wait(3)
        self.play(Write(TB_b2[1]))
        self.wait(2)
        self.play(Write(gammanot))
        self.wait(2)
        self.play(ReplacementTransform(gammanot, gammanatty))
        self.wait(2)
        self.play(FadeOut(*[gammanatty, TB_b, TB_b1]), run_time=2)
        self.play(ReplacementTransform(TB_b2, TB_bresult), run_time=2.5)
        self.wait(3)
        self.play(TB_bresult.animate(run_time=2).shift(UP+LEFT).scale(0.8))

        self.play(Indicate(Apath_b))
        self.wait(3)
        TA_b = MathTex(r"T_A = \frac{T_B}{\gamma}", r" = 2\gamma t_0").set_color(Acolor).move_to(TB_bresult.get_center()).shift(DOWN*3).scale(1.5)
        self.play(Write(TA_b[0]))
        self.wait(2)
        self.play(Write(TA_b[1]))
        self.wait(2)
        TA_bresult = MathTex(r"T_A = 2\gamma t_0").set_color(Acolor).move_to(TB_bresult.get_center()).shift(DOWN*3).scale(1.75)
        self.play(ReplacementTransform(TA_b, TA_bresult))
        self.wait(3)

        self.play(Indicate(Cpath1_b))
        self.wait(2)
        self.play(FadeOut(Cpath1_b))
        self.play(Indicate(t0B))

        TC_b0 = MathTex(r"T_C = t_0 + \frac{\Delta t}{\gamma}").set_color(Ccolor).move_to(TA_bresult.get_center()).scale(1.5)
        TC_b = MathTex(r"T_C = t_0 + \frac{\Delta t}{\gamma_c}").set_color(Ccolor).move_to(TA_bresult.get_center()).scale(1.5)

        self.play(TA_bresult.animate(run_time=2).move_to(TB_bresult.get_center()).shift(RIGHT*4.5).scale(0.8))
        self.play(self.camera.frame.animate(run_time=2).shift(RIGHT))
        self.wait(2)
        self.play(Write(TC_b0), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(TC_b0, TC_b), run_time=2)
        self.wait(2)

        gammac = MathTex(r"\gamma_c = \frac{1}{1-v_C^2}", r" = \frac{1}{1 - \left(\frac{2v}{1-v^2}\right)^2}").set_color(lightcolor).move_to(TC_b.get_center()).shift(DOWN*3+RIGHT*2).scale(1.4)
        gammacresult = MathTex(r"\gamma_c = \frac{1+v^2}{1-v^2}").set_color(lightcolor).move_to(gammac.get_center()).shift(DOWN*3).scale(1.5)

        self.play(Write(gammac[0]), run_time=2)
        self.wait(2)
        self.play(Write(gammac[1]), run_time=2)
        self.wait(2)
        self.play(Write(gammacresult), run_time=2)
        self.wait(2)
        self.play(FadeOut(gammac), gammacresult.animate(run_time=2).move_to(TC_b.get_center()).shift(RIGHT*6+UP*0.1))

        self.wait(3)
        TC_b1 = MathTex(r"T_C = t_0 + \Delta t", r"\left( \frac{1}{(1+v^2/1-v^2)}\right)").set_color(Ccolor).move_to(TC_b.get_center()).shift(DOWN*3+RIGHT*2).scale(1.5)
        TC_b2 = MathTex("T_C = t_0 + ", r"\frac{1-v^2}{1+v^2} \Delta t").set_color(Ccolor).move_to(TC_b.get_center()).shift(DOWN*3).scale(1.5)

        self.play(Write(TC_b1[0]), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(gammacresult, TC_b1[1]), TC_b.animate.shift(RIGHT), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(TC_b1, TC_b2), run_time=2)
        self.wait(2)
        deltatresult = MathTex(r"\Delta t = \frac{1+v^2}{1-v^2}\,t_0").scale(1.4)
        deltatresult.move_to(TC_b2.get_center()).shift(RIGHT*6).set_color(VibrantPink)
        self.play(Write(deltatresult), run_time=2)

        TC_b3 = MathTex(r"T_C = t_0 + \frac{1-v^2}{1+v^2}", r"\frac{1+v^2}{1-v^2} \,t_0").set_color(Ccolor).move_to(TC_b.get_center()).shift(DOWN*3+RIGHT).scale(1.5)
        self.wait(2)
        self.play(ReplacementTransform(TC_b2, TC_b3[0]), ReplacementTransform(deltatresult, TC_b3[1]), run_time=2)
        self.wait(2)
        TC_b4 = MathTex(r"T_C = t_0 + t_0").set_color(Ccolor).move_to(TC_b3.get_center()).shift(DOWN*3).scale(1.5)
        TC_bresult = MathTex("T_C = 2t_0").scale(1.7).move_to(TC_b.get_center()).set_color(VibrantPink).shift(LEFT)
        self.play(Write(TC_b4), run_time=2)
        self.wait(3)
        self.play(FadeOut(*[TC_b, TC_b3]), ReplacementTransform(TC_b4, TC_bresult), run_time=3)
        self.wait(3)
        self.play(TA_bresult.animate(run_time=3).scale(1/0.8).move_to(TC_bresult.get_center()).shift(RIGHT*5))
        self.wait(2)
        
        Bframeresult0 = MathTex(r"\implies ", "T_C", " = " , r"\frac{T_A}{\gamma}").set_color(NeonOrange).scale(2).move_to(TC_bresult.get_center()).shift(DOWN*3)
        Bframeresult0[1].set_color(Ccolor)
        Bframeresult0[3].set_color(Acolor)
        Bframeresult = MathTex("T_C", " = " , r"\frac{T_A}{\gamma}").set_color(NeonOrange).scale(2).move_to(TC_bresult.get_center()).shift(DOWN*3)


        boxBresult = SurroundingRectangle(Bframeresult, color=NeonOrange).scale(1.1)

        self.play(Write(Bframeresult0[0]))
        self.play(Write(Bframeresult0[1]))
        self.play(Write(Bframeresult0[2]))
        self.play(Write(Bframeresult0[3]))
        self.wait(2)
        self.play(ReplacementTransform(Bframeresult0, Bframeresult))
        
        self.play(Create(boxBresult))


        self.wait(5)


        
        Bframe = VGroup(Baxlabel, Adot_b, Bdot_b, Cdot_b, endpt_B, Alabel_b, Clabel_b, Blabel_b, Bpath_b00, Bpath_b0,
                        TA_bresult, TB_bresult, TC_bresult, traveldist, meetdist, t0B)
        
        #########################################################################################################################################
        # let's get a C frame:
        
        Cax = Axes(x_range=[-5, 5, 1], y_range=[0,10,1], x_length=7, y_length=7,axis_config={"include_ticks": False,"stroke_width":4.5}).set_color(Ccolor2)
        Caxlabel = Aax.get_axis_labels(x_label="x_C", y_label="t_C").set_color(Ccolor2)
        axshift_BC = og-Cax.c2p(0,0)
        Cax.shift(axshift_BC)

        Cax_xline = Line(Cax.c2p(-5,0), Cax.c2p(5,0), stroke_width=5).set_color(Ccolor)
        Cax_yline = Line(Cax.c2p(0,0), Cax.c2p(0,10), stroke_width=5).set_color(Ccolor)
        Caxlines = VGroup(Cax_xline, Cax_yline)

        caxlabelx = MathTex("x_C").next_to(Cax.x_axis.get_end(), DOWN+RIGHT).set_color(Ccolor)
        caxlabelnx = MathTex("-x_C").next_to(Cax.x_axis.get_left(), DOWN).set_color(Ccolor)
        caxlabelt = MathTex("t_C").next_to(Cax.y_axis.get_end(), RIGHT).set_color(Ccolor)
        caxlabel = VGroup(caxlabelx, caxlabelt, caxlabelnx)

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
        BCmeet_C = Dot(gli(Bpath_c, Cpath_c), radius=0.16).set_color(propercolor).set_z_index(1)

        Bpath_c0 = Line(B_c.get_center(), BCmeet_C.get_center()).set_color(Bcolor)
        Bpath_c1 = Line(BCmeet_C.get_center(), gli(Bpathghost_c, Cax.y_axis) + tphat_b_C*1.9).set_color(Bcolor)
        Cpath_c0 = Line(og, BCmeet_C.get_center()).set_color(Ccolor)
        Cpath_c1 = Line(BCmeet_C.get_center(), gli(Apathghost_c, Cax.y_axis)).set_color(Ccolor)

        Alabel_c = MathTex("A").next_to(Apath_c.get_center(), LEFT+UP).set_color(Acolor)
        Clabel_c = MathTex("C").next_to(Cpath_c0.get_center(), RIGHT*1.5).set_color(Ccolor)
        Blabel_c = MathTex("B").next_to(Bpath_c0.get_center(), RIGHT*0.5+DOWN).set_color(Bcolor)

        # transforming b frame to c frame:
        transform_BC = AnimationGroup(ReplacementTransform(Bpath_b, Bpath_c), ReplacementTransform(Apath_b, Apath_c), 
                ReplacementTransform(Cpath_b, Cax_yline), run_time=7)


        self.play(FadeOut(*Bframe), ReplacementTransform(Bax, Baxlines0), run_time=4)
        self.play(FadeOut(*[Bframeresult, boxBresult],run_time=2), self.camera.frame.animate(run_time=4).move_to(camposB0).scale(1.1*0.75))
        self.play(Baxlines0.animate.set_opacity(0.3))
        self.play(AnimationGroup(transform_BC, self.camera.frame.animate(run_time=8).scale(0.9).shift(RIGHT*1.2+DOWN*0.6)))
        self.play(FadeOut(Baxlines0), Create(Cax))
        self.play(FadeOut(Cax_yline))
        self.wait(3)

        self.play(FadeIn(*[Alabel_c, Blabel_c, Clabel_c]), run_time=2)
        self.play(FadeIn(caxlabel))

        self.play(Create(A_c), Create(B_c), Create(C_c))
        endpt_C = gli(Apathghost_c, Cax.y_axis)

        Dotmoves_c = AnimationGroup(MoveAlongPath(A_c, Line(Apath_c.get_start(),gli(Apathghost_c, Cax.y_axis)), rate_func=linear), 
                  MoveAlongPath(B_c, Bpath_cMOVE, rate_func=linear), 
                  MoveAlongPath(C_c, Cpath_c, rate_func=linear), run_time=8)

        Bpath_c00 = Bpath_c0.copy()
        Cpath0_ccolor = Cpath_c0.copy().set_color(Bcolor)
        handofftime_c = AnimationGroup(Wait(5.5), AnimationGroup(ReplacementTransform(Bpath_c00, Cpath0_ccolor, run_time=2),
                        ReplacementTransform(Bpath_c0, BCmeet_C, run_time=2)), lag_ratio=1)

        self.play(AnimationGroup(Dotmoves_c, handofftime_c, lag_ratio=0))
        self.wait(3)
        self.play(self.camera.frame.animate(run_time=3).shift(RIGHT*5).scale(1.15))
        
        va_c = MathTex(r"v_{\scriptstyle A} = v").scale(1.8).set_color(Acolor).move_to(Cax.y_axis.get_end()).shift(RIGHT*6)
        vb_c = MathTex(r"v_{\scriptstyle B} = \frac{2v}{1+v^2}").move_to(va_c.get_center()).shift(RIGHT*5+UP*0.15).scale(1.8).set_color(Bcolor)
        gamma_Bc = MathTex(r"\gamma_{\scriptstyle B} = \frac{1+v^2}{1-v^2}").scale(1.8).set_color(lightcolor).move_to(vb_c.get_center()).shift(DOWN*3)

        self.play(Write(va_c))
        self.wait(2) 
        self.play(Write(vb_c), run_time=2)
        self.wait(2)
        self.play(Write(vb_c))
        self.wait(2)
        self.play(Write(gamma_Bc))
        self.wait(4)

        self.play(AnimationGroup(va_c.animate(run_time=2).scale(0.7).shift(LEFT*2+UP),
                                 vb_c.animate(run_time=2).scale(0.7).shift(LEFT*3.5+UP)))
        self.play(gamma_Bc.animate(run_time=3).scale(0.7).move_to(vb_c.get_center()).shift(RIGHT*4.1+UP*0.05))
        
        deltBarrow = Arrow(Bpath_c.get_start(), BCmeet_C.get_center(),buff=0.1).set_color(Bcolor)
        deltBc0 = MathTex("\Delta t_B ", " = t_0").move_to(va_c.get_center()).scale(1.1).move_to(Blabel_c.get_center()).shift(RIGHT*0.6).set_color(Bcolor)
        deltBc01 = MathTex("\Delta t_B ", " = t_0").move_to(
            Line(va_c.get_center(), vb_c.get_center()).get_center()).set_color(Bcolor).scale(1.5).shift(DOWN*2)
        firsteqpos = deltBc01.get_center()
        # deltBc1 = MathTex("\Delta t_B ", r" = \frac{\Delta t_{C_0}}{\gamma_B}").move_to(
        #     Line(va_c.get_center(), vb_c.get_center()).get_center()).set_color(Ccolor).scale(1.5).shift(DOWN*2)
        
        t0C = MathTex("t_0").move_to(BCmeet_C.get_center()).shift(RIGHT*0.5+DOWN*0.15).scale(1.3)
        og = Cax.c2p(0,0)

        showdeltaTC = BraceBetweenPoints(og, BCmeet_C.get_center())
        showdeltaTCeq0 = MathTex("\Delta t_{C_0}", r"= \gamma_B\,\Delta t_B").scale(1.5).move_to(showdeltaTC.get_center()).shift(RIGHT*3)
        showdeltaTCeq01 = MathTex("\Delta t_{C_0}", r"= \gamma_B\,t_0").scale(1.5).move_to(showdeltaTC.get_center()).shift(RIGHT*3)

        tempfadeout = [Blabel_c, Clabel_c]

        self.play(FadeOut(*tempfadeout))

        self.play(Create(deltBarrow), run_time=2)
        self.wait(2)
        self.play(Write(deltBc0[0]), run_time=2)
        self.wait(2)
        self.play(FadeOut(deltBarrow))
        self.wait(2)
        self.play(FadeIn(showdeltaTC))
        self.wait()
        self.play(Write(showdeltaTCeq0[0]))
        self.wait(2)
        self.play(Write(showdeltaTCeq0[1]))
        self.wait(2)
        self.play(ReplacementTransform(deltBc0[0], deltBc01[0]), run_time=2)
        self.wait(2)
        self.play(FadeOut(showdeltaTC))
        self.play(Write(t0C), run_time=2)
        self.wait(2)
        self.play(Write(deltBc01[1]))
        self.wait(2)
        self.play(Transform(showdeltaTCeq0[1],showdeltaTCeq01[1]))
        self.wait(2)
        self.play(FadeOut(deltBc01, run_time=2), showdeltaTCeq0.animate(run_time=3).move_to(deltBc01.get_center()).set_color(Ccolor))
        self.wait(2)

        showdeltaTCeq1 = MathTex("\Delta t_{C_0}", r"= \frac{1+v^2}{1-v^2} \,t_0").move_to(showdeltaTCeq0.get_center()).scale(1.5).set_color(Ccolor)
        
        self.play(FadeOut(showdeltaTCeq0[1]), ReplacementTransform(showdeltaTCeq0[0], showdeltaTCeq1[0]), 
                  ReplacementTransform(gamma_Bc, showdeltaTCeq1[1]),run_time=2)
        self.wait(2)

        self.play(FadeOut(*[va_c, vb_c]),run_time=2)
        self.wait(2)
        self.play(showdeltaTCeq1.animate(run_time=2).move_to(firsteqpos).shift(UP*2).scale(0.9))

        showdelta_TC_arrow = Arrow(og, endpt_C, buff=0.05).set_color(VibrantPink2)
        showdelta_TC = MathTex("\Delta T_C", "= \Delta t_{C_0} + \Delta t").scale(1.3).set_color(VibrantPink2).move_to(showdelta_TC_arrow.get_center()).shift(RIGHT*3.5)
        showdeltaT = Arrow(BCmeet_C.get_center(), endpt_C, buff=0.01).set_color(propercolor)
        deltaTlabel = MathTex("\Delta t").set_color(propercolor).move_to(showdeltaT.get_center()).shift(RIGHT*0.5)


        reduce_opacity_ofB = [Cpath_c0, Bpath_c, BCmeet_C, Cpath0_ccolor, t0C]

        
        self.play(*(i.animate.set_opacity(0.2) for i in reduce_opacity_ofB))

        self.play(Create(showdelta_TC_arrow), run_time=2)
        self.wait(2)
        self.play(Write(showdelta_TC[0]), run_time=2)
        self.wait(3)
        self.play(Write(showdelta_TC[1]), run_time=2)
        self.wait()
        self.play(FadeOut(showdelta_TC_arrow))
        self.play(Create(showdeltaT), run_time=2)
        self.play(Write(deltaTlabel))
        self.wait(3)

        self.play(*(i.animate.set_opacity(1) for i in reduce_opacity_ofB))
        self.play(FadeIn(*tempfadeout), run_time=2)
        self.play(FadeOut(*[showdeltaT, deltaTlabel]))
        self.play(showdelta_TC.animate(run_time=4).move_to(showdeltaTCeq1.get_center()).shift(RIGHT*6).scale(0.9))

        TA_c = MathTex("T_A = ", r"\frac{\Delta T_C}{\gamma}").move_to(firsteqpos).shift(DOWN+LEFT*2).scale(1.4).set_color(Acolor)
        TA_c1 = MathTex("T_A = ", r"\frac{1}{\gamma} \left(\Delta t_{C_0} + \Delta t \right)").scale(1.4).move_to(TA_c.get_center()).shift(RIGHT*6.5).set_color(Acolor)
        TA_c2 = MathTex("T_A = ", r"\frac{1}{\gamma} \left(\frac{1+v^2}{1-v^2} \,t_0 + \Delta t \right)").move_to(TA_c.get_center()).scale(1.5).shift(DOWN*3+RIGHT*3).set_color(Acolor)

        self.play(Indicate(Apath_c))
        self.play(Write(TA_c), run_time=2)
        self.wait(2)
        self.play(Write(TA_c1[0]))
        self.wait(2)
        self.play(ReplacementTransform(showdelta_TC, TA_c1[1]), run_time=2)
        self.wait(2)
        self.play(Write(TA_c2[0]))
        self.wait(2)
        self.play(ReplacementTransform(showdeltaTCeq1, TA_c2[1]), run_time=2)
        self.wait(4)

        self.play(FadeOut(*[TA_c, TA_c1]), run_time=2)
        self.play(TA_c2.animate(run_time=2).move_to(firsteqpos).shift(UP*2+LEFT).scale(0.8))
        self.wait(2)


        TC_c = MathTex("T_C = t_0 + \Delta t").scale(1.5).set_color(Ccolor).move_to(firsteqpos)

        self.play(Write(TC_c), run_time=2)
        self.wait(2)
        self.play(Indicate(t0C))
        self.wait(2)
        self.play(TC_c.animate(run_time=2).move_to(TA_c2.get_center()).shift(RIGHT*6.5))
        self.wait(4)
        self.play(FadeOut(*[TA_c2, TC_c]), run_time=2)
        self.wait(2)

        eqscampos = self.camera.frame.get_center()
        self.play(self.camera.frame.animate(run_time=3).move_to(camposB0).shift(DOWN+RIGHT*3).scale(0.9))
        self.wait(2)

        showdelxarrow = Arrow(og, Apath_c.get_start(), buff=0.01).set_color(propercolor)
        showdelx = MathTex("\Delta x_A", " = ", "\Delta x_B").set_color(propercolor).scale(1.2).move_to(showdelxarrow.get_center()).shift(DOWN*0.5+RIGHT*0.5)
        showdelx[0].set_color(Acolor)
        showdelx[2].set_color(Bcolor)

        self.play(Create(showdelxarrow), run_time=2)
        self.wait(2)
        self.play(Write(showdelx), run_time=2.5)
        self.wait(2)

        delx_b = MathTex("\Delta x_B", r" = \Delta t_{C_0} \,v_B").scale(1.5).move_to(firsteqpos).shift(UP*2+RIGHT).set_color(Bcolor)
        delx_b1 = MathTex("\Delta x_B", r" = \gamma_B \,t_0\,", " v_B").scale(1.5).move_to(firsteqpos).shift(UP*2+RIGHT).set_color(Bcolor)
        delx_b2 = MathTex("\Delta x_B", r" = \left(\frac{1+v^2}{1-v^2} \,t_0\right)", 
                    r"\frac{2v}{1+v^2}").scale(1.5).move_to(delx_b1.get_center()).shift(DOWN*3+RIGHT).set_color(Bcolor)
        delx_b3 = MathTex("\Delta x_B", " = ", r"\frac{2v}{1-v^2}\,t_0").scale(1.5).move_to(delx_b2).shift(DOWN*3).set_color(Bcolor)

        self.play(self.camera.frame.animate(run_time=2).move_to(eqscampos).scale(1/0.9))
        self.wait()
        self.play(Indicate(Bpath_c))
        self.wait(2)
        self.play(Write(delx_b), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(delx_b, delx_b1), run_time=2)
        self.wait(2)
        self.play(Write(delx_b2), run_time=2)
        self.wait(2)
        self.play(Write(delx_b3), run_time=2)
        self.wait(4)

        self.play(FadeOut(*[delx_b, delx_b1, delx_b2]), run_time=2)
        self.wait(2)
        self.play(delx_b3.animate(run_time=2).move_to(firsteqpos).shift(UP*2).scale(0.9))
        self.wait(4)


        
        delx_a = MathTex("\Delta x_A", r" = \left(\Delta t_{C_0} + \Delta t\right)\, v").move_to(firsteqpos).scale(1.4).set_color(Acolor)
        delx_a1 = MathTex("\Delta x_A", r" =  \frac{1+v^2}{1-v^2} \,t_0 v + \Delta t \, v ").move_to(delx_a.get_center()).shift(DOWN*3).scale(1.4).set_color(Acolor)

        self.play(Write(delx_a), run_time=2.5)
        self.wait(2)
        self.play(ReplacementTransform(delx_a, delx_a1), run_time=2.5)
        self.wait(2)
        self.play(delx_a1.animate(run_time=2).move_to(delx_b3.get_center()).shift(DOWN*2+RIGHT*0.7))
        self.wait(2)
        delxa_eq_delxb = MathTex("\Delta x_B", " = ", "\Delta x_A").move_to(delx_a1.get_center()).shift(DOWN*2).scale(1.4).set_color(Acolor)

        delxa_eq_delxb1 = MathTex(r"\frac{2v}{1-v^2}\,t_0", " = ", r"\frac{1+v^2}{1-v^2} \,t_0 v + \Delta t \, v ").move_to(delxa_eq_delxb.get_center()).scale(1.4).set_color(Acolor).shift(DOWN*2)

        
        self.play(Write(delxa_eq_delxb), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(delx_b3, delxa_eq_delxb1[0]),
                 Write(delxa_eq_delxb1[1]), ReplacementTransform(delx_a1, delxa_eq_delxb1[2]), run_time=3)
                 
        self.wait(2)

        self.play(FadeOut(delxa_eq_delxb), delxa_eq_delxb1.animate(run_time=2).move_to(firsteqpos).shift(UP*1.5+RIGHT*2))
        self.wait(2)

        delxa_eq_delxb2 = MathTex(r"\Delta t = \left(\frac{2}{1-v^2} - \frac{1+v^2}{1-v^2}\right)\,t_0").move_to(delxa_eq_delxb1.get_center()).scale(1.4).set_color(Acolor).shift(DOWN*3)
        delxa_eq_delxb3 = MathTex(r"\Delta t = \left(\frac{1-v^2}{1-v^2}\right)\,t_0").move_to(delxa_eq_delxb2.get_center()).scale(1.4).set_color(Acolor).shift(DOWN*3)
        delxa_eq_delxbresult = MathTex(r"\Delta t = t_0").move_to(delxa_eq_delxb2.get_center()).scale(1.4).set_color(Acolor).shift(DOWN*3)

        self.play(Write(delxa_eq_delxb2),run_time=2)
        self.wait()
        self.play(Write(delxa_eq_delxb3), run_time=2)
        self.wait(4)
        self.play(ReplacementTransform(delxa_eq_delxb3, delxa_eq_delxbresult),run_time=2)
        self.wait(3)

        self.play(FadeOut(*[delxa_eq_delxb2, delxa_eq_delxb1]), delxa_eq_delxbresult.animate(run_time=2).move_to(TA_c2.get_center()).shift(DOWN*2+LEFT))
        self.wait(2)
        self.play(FadeIn(*[TA_c2, TC_c]), run_time=2)
        self.wait(2)




        TA_c3 = MathTex("T_A = ", r"\frac{1}{\gamma} \left(\frac{1+v^2}{1-v^2} \,t_0 + t_0 \right)").move_to(delxa_eq_delxbresult.get_center()).shift(DOWN*2+RIGHT*2).scale(1.5).set_color(Acolor)
        TA_c4 = MathTex("T_A = ", r"\frac{1}{\gamma} \left(\frac{2}{1-v^2}\right)\,t_0").move_to(TA_c3.get_center()).shift(DOWN*2.5).scale(1.5).set_color(Acolor)
        TA_c5 = MathTex(r"T_A = \frac{2}{\sqrt{1-v^2}} \,t_0", " = 2\gamma\,t_0").move_to(TA_c3.get_center()).shift(DOWN*2.5).scale(1.5).set_color(Acolor)
        TA_cresult = MathTex("T_A = 2\gamma\,t_0").move_to(TA_c3.get_center()).shift(DOWN*2.5).scale(1.5).set_color(Acolor)

        TC_c1 = MathTex("T_C = t_0 + t_0").move_to(delxa_eq_delxbresult.get_center()).shift(DOWN*2.5+RIGHT).scale(1.5).set_color(Ccolor)
        TC_cresult = MathTex("T_C = 2t_0").move_to(TC_c1.get_center()).shift(DOWN*2).scale(1.5).set_color(Ccolor)

        

        self.play(Write(TA_c3), run_time=2)
        self.wait(2)
        self.play(Write(TA_c4), run_time=2)
        self.wait(3)
        self.play(ReplacementTransform(TA_c4, TA_c5[0]), run_time=2)
        self.wait(2)
        self.play(Write(TA_c5[1]))
        self.wait(3)
        self.play(ReplacementTransform(TA_c5, TA_cresult), run_time=2)
        self.wait(2)
        self.play(FadeOut(*[TA_c3, TA_c2]), run_time=2)
        self.wait(2)
        self.play(TA_cresult.animate.move_to(TA_c2.get_center()))
        self.wait(2)

        self.play(Write(TC_c1), run_time=2)
        self.wait(2)
        self.play(Write(TC_cresult))

        self.wait(2)

        self.play(FadeOut(*[TC_c1, delxa_eq_delxbresult, TC_c]))
        self.play(TC_cresult.animate(run_time=2).move_to(TC_c.get_center()))

        Cframeresult0 = MathTex(r"\implies ", "T_C", " = " , r"\frac{T_A}{\gamma}").set_color(NeonOrange).scale(2).move_to(
            Line(TA_cresult.get_center(), TC_cresult.get_center()).get_center()
        ).shift(DOWN*3+LEFT)

        Cframeresult0[1].set_color(Ccolor)
        Cframeresult0[3].set_color(Acolor)
        Cframeresult = MathTex("T_C", " = " , r"\frac{T_A}{\gamma}").set_color(NeonOrange).scale(2).move_to(Cframeresult0.get_center()).shift(DOWN*2)

        self.wait(2)
        self.play(Write(Cframeresult0[0]))
        self.play(Write(Cframeresult0[1]))
        self.play(Write(Cframeresult0[2]))
        self.play(Write(Cframeresult0[3]))

        self.wait(3)
        self.play(FadeOut(*[TC_cresult, TA_cresult, Cframeresult0[0]]), 
            ReplacementTransform(Cframeresult0[1:4], Cframeresult), run_time=2)
        
        boxitC = SurroundingRectangle(Cframeresult, color=NeonOrange).scale(1.2)

        self.play(Create(boxitC), run_time=2)
        self.play(self.camera.frame.animate(run_time=8).move_to(Cframeresult.get_center()).shift(UP*2).scale(0.4),
                  boxitC.animate(run_time=8).shift(UP*2).set_color(propercolor), Cframeresult.animate(run_time=8).shift(UP*2).set_color(propercolor))
        self.wait(10)


        ########################### TADAAAAAAAAA! ###########################################


# Show the initial animation.
# Show A frame.
# Show transformation
# Show B frame, no algebra, emphasize the velocity addition rule
# Show transformation
# Show C frame no algebra, 