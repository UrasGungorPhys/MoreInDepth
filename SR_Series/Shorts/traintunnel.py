
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


# Show same lenght. Show length contraction on both frames.
# show how the light signal takes very long to reach the end.