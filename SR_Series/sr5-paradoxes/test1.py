from manim import *

class Lineex(Scene):
    def construct(self):
        v = 0.60
        gamma = 1/np.sqrt(1-v**2)
        
        properL = 4 # in coordinate distances
        Lprime = 4/gamma


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

        gndax = Axes(x_range=[0, 10, 1], y_range=[0,10,1], x_length=7, y_length=7,axis_config={"include_ticks": False,"stroke_width":3.5})
        gndaxlabel = gndax.get_axis_labels(x_label="x", y_label="t")
        xphat = np.array([1,v,0])/np.linalg.norm(np.array([1,v,0]))
        tphat = np.array([v,1,0])/np.linalg.norm(np.array([v,1,0]))
        
        trainbackdot = Dot(gndax.c2p(0,0))
        trainfrontdot = Dot(gndax.c2p(Lprime,0))

        tpfront = Arrow(start=trainfrontdot.get_center(), end=trainfrontdot.get_center() + tphat*8, buff=0)
        tpback = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + tphat*8, buff=0)
        tpfrontlabel = always_redraw(lambda: MathTex("t_f '").next_to(tpfront.get_end(), UP*0.7))
        tpbacklabel = always_redraw(lambda: MathTex("t_b '").next_to(tpback.get_end(), UP*0.7))

        xpog = Arrow(start=trainbackdot.get_center(), end=trainbackdot.get_center() + xphat*8, buff=0)
        xplabel = always_redraw(lambda: MathTex("x '").next_to(xpog.get_end(), RIGHT))


        line1 = Line(gndax.c2p(0,0), gndax.c2p(9,5))
        Ldivgammadot = Dot(trainfrontdot.get_center())
    

        spacelike_invariant_hyperbola = gndax.plot(lambda x : np.sqrt(x**2 - properL**2), x_range=[4,10,0.01])
        timelike_invariant_hyperbola = gndax.plot(lambda x : np.sqrt(x**2 + properL**2), x_range=[0,9.17,0.01])

        hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(spacelike_invariant_hyperbola.get_end(), RIGHT+UP)

        intersect_dot = Dot(gndax.c2p(*gl_stinterval(line1, 4))).set_color(YELLOW)
        slopetest = glslope(line1)

        slopedots = VGroup()
        for i in range(5):
            dotipts = [i, slopetest*i]
            doti = Dot(gndax.c2p(*dotipts))
            slopedots.add(doti)

        self.play(Create(gndax))
        self.wait(2)
        self.play(Create(spacelike_invariant_hyperbola))
        self.wait(2)
        self.play(Create(line1))

        self.wait(2)
        self.play(Create(intersect_dot))

        self.wait(2)
        self.play(Create(slopedots))


        self.wait(10)

        