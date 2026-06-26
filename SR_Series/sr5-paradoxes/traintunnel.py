from manim import *
import numpy as np


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
        # x_intersects = VGroup()

        for i in range(5):
            u = show_off_vs[i]
            colori = show_off_colors[i]
            hatlength = hatlengths[i]

            xphatu = np.array([1,u,0])/np.linalg.norm(np.array([1,u,0]))
            tphatu = np.array([u,1,0])/np.linalg.norm(np.array([u,1,0]))
            tpu = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + tphatu*hatlength, buff=0).set_color(colori)
            xpu = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + xphatu*hatlength, buff=0).set_color(colori)

            show_off_xps.add(xpu)
            show_off_tps.add(tpu)
            # xpu_intersection = intersects(xpu, spacelike_invariant_hyperbola)
            # xpuintdot = Dot(xpu_intersection)
            # x_intersects.add(xpuintdot)


        self.wait(3)
        self.play(Create(show_off_xps), run_time=6)

        self.wait(3)
        # self.play(Create(x_intersects), run_time=3)
        # self.wait(3)

        self.play(Create(timelike_invariant_hyperbola), run_time=4)
        self.play(Create(show_off_tps), run_time=4)

        self.wait(5)

        self.play(FadeOut(show_off_tps), FadeOut(show_off_xps))
        self.wait(2)

        # Back to scene1 objects
        scene2fadeouts = [timelike_invariant_hyperbola, spacelike_invariant_hyperbola,hyperbola_eqq, Ldivgammadot, Lgammadot, Ldivgammalabel, Lgammalabel,fronttnotzero, prj_ground, Llabel, fronttpzero]
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


