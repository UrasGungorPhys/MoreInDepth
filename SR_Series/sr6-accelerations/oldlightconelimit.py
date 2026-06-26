class LightconeLimit(MovingCameraScene):
    def construct(self):
        ax = Axes(x_range=[-7,7,1], y_range=[-4,4,1], 
        x_length=14, y_length=8,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.move_to(ORIGIN)

        # rewriting hypax function for practice:
        def get_hypaxes2t(obs, negworldline, posworldline):
            # x = ax.p2c(obs.get_center())[0]
            # t = ax.p2c(obs.get_center())[1]
            x = obs.get_center()[0]
            t = obs.get_center()[1]

            dx = 0.05

            if t<-dx*10:
                wlpt = [x, negworldline(x), 0]
                slope = (negworldline(x-dx) - negworldline(x))/dx
                tprime = Arrow(wlpt, [wlpt[0]+3, wlpt[1]-3*slope, 0])
                xprime = Arrow(wlpt, [wlpt[0]-3*slope, wlpt[1]+3, 0])
            elif t>dx*10:
                wlpt = [x, posworldline(x), 0]
                slope = (posworldline(x+dx) - posworldline(x))/dx
                tprime = Arrow(wlpt, [wlpt[0]-3, wlpt[1]+3*slope, 0], buff=0)
                xprime = Arrow(wlpt, [wlpt[0]+3*slope, wlpt[1]+3, 0], buff=0)

            else:
                if t<0:
                    xprime = Arrow(obs, [obs.get_x()-3, obs.get_y(),0], buff=0)
                    tprime = Arrow(obs, [obs.get_x(), obs.get_y()+3,0], buff=0)

                else:
                    xprime = Arrow(obs, [obs.get_x()+3, obs.get_y(),0], buff=0)
                    tprime = Arrow(obs, [obs.get_x(), obs.get_y()+3,0], buff=0)
                    
            return tprime
        

        def get_hypaxes2x(obs, negworldline, posworldline):
            
            # x = ax.p2c(obs.get_center())[0]
            # t = ax.p2c(obs.get_center())[1]
            x = obs.get_center()[0]
            t = obs.get_center()[1]
            dx = 0.05
            

            if t<-dx*10:
                wlpt = [x, negworldline(x), 0]
                slope = (negworldline(x-dx) - negworldline(x))/dx
                tprime = Arrow(wlpt, [wlpt[0]-3, wlpt[1]+3*slope, 0])
                xprime = Arrow(wlpt, [wlpt[0]-3*slope, wlpt[1]+3, 0])
            elif t>dx*10:
                wlpt = [x, posworldline(x), 0]
                slope = (posworldline(x+dx) - posworldline(x))/dx
                tprime = Arrow(wlpt, [wlpt[0]+3, wlpt[1]+3*slope, 0], buff=0)
                xprime = Arrow(wlpt, [wlpt[0]+3*slope, wlpt[1]+3, 0], buff=0)

            else:
                if t<0:
                    xprime = Arrow(obs, [obs.get_x()-3, obs.get_y(),0], buff=0)
                    tprime = Arrow(obs, [obs.get_x(), obs.get_y()+3,0], buff=0)

                else:
                    xprime = Arrow(obs, [obs.get_x()+3, obs.get_y(),0], buff=0)
                    tprime = Arrow(obs, [obs.get_x(), obs.get_y()+3,0], buff=0)

            return xprime
  


        

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)
        xct1 = DashedLine(start=ax.c2p(-9.5,-9.5), end=ax.c2p(9.5,9.5)).set_color(lightcolor).set_opacity(0.5)
        xct2 = DashedLine(start=ax.c2p(-9.5,9.5), end=ax.c2p(9.5,-9.5)).set_color(lightcolor).set_opacity(0.5)
        OG=ax.c2p(0,0)


        hypmfunc = lambda x: -np.sqrt(x**2 - 3**2)
        hyppfunc = lambda x: np.sqrt(x**2 - 3**2)

        hypm = ax.plot(lambda x: -np.sqrt(x**2 - 3**2), x_range=[3,9.5,0.01])
        hypp = ax.plot(lambda x: np.sqrt(x**2 - 3**2), x_range=[3,9.5,0.01])

        hypphalf = ax.plot(lambda x: np.sqrt(x**2 - 3**2), x_range=[3,5,0.01])
        

        acc = Dot().move_to(hypm.get_end())
        acc.set_z_index(1)

        xctp = always_redraw(lambda: DashedLine(start=[acc.get_x()+4.5, acc.get_y()-4.5,0], end=[acc.get_x()-4.5, acc.get_y()+4.5,0]).set_color(lightcolor).set_opacity(0.5))
        xctm = always_redraw(lambda: DashedLine(start=[acc.get_x()-4.5, acc.get_y()-4.5,0], end=[acc.get_x()+4.5, acc.get_y()+4.5,0]).set_color(lightcolor).set_opacity(0.5))

        tp = always_redraw(lambda: get_hypaxes2t(acc, hypmfunc, hyppfunc))
        xp = always_redraw(lambda: get_hypaxes2x(acc, hypmfunc, hyppfunc))

        self.play(Create(ax))
        self.play(Create(hypm))
        self.play(Create(hypp))
        # self.play(Create(xct1), Create(xct2))

        self.play(Create(acc))
        self.play(Create(xctp), Create(xctm))
        self.play(Create(tp), Create(xp))
        self.play(MoveAlongPath(acc, hypm, rate_func=lambda t:1-t), run_time=5)
        self.play(MoveAlongPath(acc, hypp, rate_func=linear), run_time=5)
        self.wait(2)
        self.play(FadeOut(*[xctp, xctm]))
        self.play(MoveAlongPath(acc, hypp, rate_func=lambda t:1-t), run_time=2)
        self.play(Create(xct1), Create(xct2), run_time=1.5)
        self.play(AnimationGroup(hypm.animate(run_time=1.5).set_color(SchoolBus), hypp.animate(run_time=1.5).set_color(SchoolBus)))


        # self.play(MoveAlongPath(acc, hypphalf))
        # self.play(Create(get_hypaxes2t(acc, hypmfunc, hyppfunc)))



        self.wait(5)