from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920

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


def makeclock(time, scale):

    clockscale = scale
    clockimg = ImageMobject("clock.png").scale(clockscale)
    clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale))
    clockcenter = always_redraw(lambda:Dot(clockimg.get_center()).set_color(BLACK).scale(1.4).scale(clockscale))
    clock12 = always_redraw(lambda:Dot(clockimg.get_top()).shift(DOWN*0.85*clockscale).set_opacity(0))
    clocklinetip = Dot(clock12.get_center()).set_color(VibrantGreen).set_opacity(0)

    n=time  # set to adjust to time
    adjustarc = Arc(radius=2.9*clockscale, start_angle=PI/2-(n-1)*PI/6, 
                            angle=-PI/6, arc_center=clockcenter.get_center())
    clocklinetip.move_to(adjustarc.get_end())
    clockline = always_redraw(lambda:Line(clockimg.get_center(), clocklinetip.get_center(), stroke_width=10*clockscale).set_color(BLACK))
    clock=Group(clockbg, clockimg, clockline, clock12, clockcenter, clocklinetip)

    return clock

class RearClockAheadTrain(MovingCameraScene):

    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")
        self.camera.frame.scale(0.75)


        train = ImageMobject("traindraw.png").scale(1.3).flip(UP)
        alice = ImageMobject("bobdraw.png").scale(0.12).move_to(train.get_center()).shift(LEFT*0.6)
        bob = ImageMobject("bobdraw.png").scale(0.12).move_to(train.get_center()).shift(LEFT*2.5)
        clocka = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(alice.get_center()).shift(UP*1.5))
        clockb = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(bob.get_center()).shift(UP*1.5))
        traingiller = Group(train, alice, bob)
        traingiller.shift(LEFT*7)
        self.add(traingiller)

        self.play(traingiller.animate(rate_func=linear, run_time=10).shift(RIGHT*12))



class RearClockAheadDiagram(MovingCameraScene):

    def construct(self):
        self.camera.frame.scale(0.5)
        self.camera.background_color = ManimColor.from_hex("#171717")

        
        ll = 6  # axis lengths to draw
        axrange = 10  # coordinate ranges
        norm = ll/axrange  # normalize any distance to fit
        pcolor=BLUE_C  # Color to use for theLT primed axes

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
        # lightlabel = MathTex("c").next_to(xct.get_end(), UR).set_color(lightcolor)

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
        v = 0.35
        gamma = 1/np.sqrt(1-v**2)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0]) 

        xphat = xp_direction
        tphat = tp_direction

        xp = Arrow(start=OG, end=OG + 6.5*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)

        tp = Arrow(start=OG, end=OG + 6.5*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        tplabel = MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2)

        xct_long = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange+2.5,axrange+2.5)).set_color(lightcolor)
        # lightlabel_long = MathTex("c").next_to(xct_long.get_end(), DR).set_color(lightcolor)

        # Lorentz grid

        manual_gridspx = VGroup()
        manual_gridspy = VGroup()
        for i in range(1,10):

            xpline = Line(start=OG + i*tp_direction*norm*1.01,
                         end=OG + i*tp_direction*norm*1.01 + 5.7*xp_direction*1.01, buff=0, 
                         stroke_color=pcolor1, stroke_opacity=0.5,stroke_width=2)


            tpline = Line(start=OG + i*xp_direction*norm*1.01,
                         end=OG + i*xp_direction*norm*1.01 + 5.7*tp_direction*1.01, buff=0,
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
        self.play(Create(ax), Create(ax_labels), run_time=1)
        self.play(AnimationGroup(Create(grid),Create(xct)), run_time=2)
        self.bring_to_front(ax)

        self.play(FadeIn(*[xpi, tpi, manual_grids0x, manual_grids0y]), run_time=2)
        self.wait(0.5)


        # self.play(FadeOut(lightlabel))
        self.play(Transform(xpi, xp), Transform(tpi, tp),
                    Transform(manual_grids0x, manual_gridspx),
                    Transform(manual_grids0y, manual_gridspy),
                    Transform(xct, xct_long),
                    self.camera.frame.animate.scale(1.22).shift(UP*0.5+RIGHT*0.74),run_time=4.5)

        self.play(FadeIn(xplabel), FadeIn(tplabel), run_time=2)
        self.wait()
        # insert constant t lines here
        
        self.play(manual_grids0x.animate.set_opacity(0.1), manual_grids0y.animate.set_opacity(0.1),
                  xpi.animate.set_opacity(0.2), tpi.animate.set_opacity(0.2), xct.animate.set_opacity(0.2),
                  xplabel.animate.set_opacity(0.2), tplabel.animate.set_opacity(0.2))

        # Initial Lorentz grid
        manual_grids0xnew = VGroup()
        for i in range(1,10):

            xline = Line(start=OG + i*that,
                         end=OG + i*that + 9.5*xhat, buff=0,
                         stroke_color=gndcolor1, stroke_opacity=0.7,stroke_width=3.5)

            manual_grids0xnew.add(xline)
        
        self.play(FadeIn(manual_grids0xnew))
        self.wait()
        self.play(Indicate(manual_grids0xnew))
        self.wait(2)

        self.play(FadeOut(manual_grids0xnew), manual_grids0x.animate.set_opacity(0.35), manual_grids0y.animate.set_opacity(0.35),
                  xpi.animate.set_opacity(1), tpi.animate.set_opacity(1), xct.animate.set_opacity(1),
                  xplabel.animate.set_opacity(1), tplabel.animate.set_opacity(1))
        
        # self.play(Indicate(manual_grids0y))
        self.play(Indicate(manual_grids0x))
        self.wait(1)

        xplabelt0 = MathTex("t'=0").next_to(xp.get_end(), RIGHT*0.8).set_color(pcolor2).scale(0.8)
        self.play(Transform(xplabel, xplabelt0))

        self.play(FadeOut(manual_grids0x),FadeOut(manual_grids0y),FadeOut(grid),
                    Transform(xct,xct0.set_opacity(0.4)),
                    self.camera.frame.animate.shift(DOWN*0.1, LEFT*0.5), run_time=2)
        

        self.wait(2)

        
        clock1p = makeclock(0, 0.12).move_to(OG).set_z_index(1)
        clock2p = makeclock(0, 0.12).move_to(OG+ xphat*2.5).set_z_index(1)
        clock3p = makeclock(0, 0.12).move_to(OG+ xphat*5).set_z_index(1)

        tp0labels = VGroup(
            MathTex("t'=0").move_to(clock1p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.7),
            MathTex("t'=0").move_to(clock2p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.7),
            MathTex("t'=0").move_to(clock3p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.7)
        )

        self.play(FadeIn(*[clock1p, clock2p, clock3p]), run_time=2)
        self.wait()
        self.play(Write(tp0labels), run_time=2)
        self.wait(2)
        self.play(AnimationGroup(self.camera.frame.animate(run_time=3).scale(0.70).shift(DOWN*1.65+LEFT*0.68),
                                        FadeOut(tp0labels)))
        
        self.wait(2)

        clock2p_prj = DashedLine(clock2p.get_left(), [OG[0], clock2p.get_y(),0])
        clock3p_prj = DashedLine(clock3p.get_left(), [OG[0], clock3p.get_y(),0])
        
        clock2 = makeclock(1, 0.12).move_to([OG[0], clock2p.get_y(),0]).set_z_index(1)
        clock3 = makeclock(2, 0.12).move_to([OG[0], clock3p.get_y(),0]).set_z_index(1)

        self.play(Create(clock2p_prj))
        self.play(Create(clock3p_prj), run_time=2)

        self.wait()

        self.play(FadeIn(*[clock2, clock3]), run_time=2)
        self.wait()
        self.play(FadeOut(*[clock2p_prj, clock3p_prj]))
        self.wait(2)
        self.play(FadeOut(*[clock2, clock3]), run_time=2)
        self.wait(2)

        clock1f = makeclock(2, 0.12).move_to([OG[0], clock3p.get_y(),0]).set_z_index(1)
        clock2f = makeclock(1, 0.12).move_to([clock2p.get_x(), clock3p.get_y(),0]).set_z_index(1)

        clock3sim = Line([OG[0], clock3p.get_y(),0], [xp.get_end()[0]-0.5, clock3p.get_y(),0], buff=0).set_color(VibrantPink)

        clock1delt = Arrow(OG, [OG[0], clock3p.get_y(),0], buff=0).set_color(VibrantGreen)
        clock2delt = Arrow(clock2p.get_center(), [clock2p.get_x(), clock3p.get_y(),0], buff=0).set_color(VibrantGreen)

        self.play(Create(clock3sim), run_time=3)
        self.play(Create(clock1delt), Create(clock2delt), run_time=2)
        self.wait(2)        

        self.play(AnimationGroup(Transform(clock1p, clock1f), Transform(clock2p, clock2f),
                                 FadeOut(*[clock1delt, clock2delt])), run_time=3.5)

        self.wait(3)
        self.play(FadeOut(*[clock1p, clock2p, clock3p, clock3sim]), run_time=2)
        

        clock1s = makeclock(0, 0.12).move_to([clock1p.get_x(), OG[1],0]).set_z_index(1)
        clock2s = makeclock(0, 0.12).move_to([clock2p.get_x(), OG[1],0]).set_z_index(1)
        clock3s = makeclock(0, 0.12).move_to([clock3p.get_x(), OG[1],0]).set_z_index(1)

        self.play(FadeIn(*[clock1s, clock2s, clock3s]), run_time=2)


        negax = Axes(x_range=[-5,axrange,1], y_range=[-5,axrange,1], 
        x_length=ll+3, y_length=ll+3,axis_config={"include_ticks": False}).set_color(gndcolor1)
        negax.shift(OG - negax.c2p(0, 0))  # align origins

        # Draw theLT negative axes:
        negxp = Arrow(start=OG, end=OG - 4*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        negxplabel = always_redraw(lambda: MathTex("-x'").next_to(negxp.get_end(), LEFT).set_color(pcolor1))

        negtp = Arrow(start=OG, end=OG - 4*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        negtplabel = always_redraw(lambda : MathTex("-t'").next_to(negtp.get_end(), LEFT).set_color(pcolor1))


        self.play(self.camera.frame.animate(run_time=3).scale(1.3).shift(LEFT+DOWN),
                  Create(negax), Create(negxp), Create(negtp), Write(negxplabel), Write(negtplabel), run_time=3)
        
        clock2sprj = DashedLine(clock2s.get_center(), gli(Line(clock2s.get_center(), clock2s.get_center()-xphat*20), negtp))
        clock3sprj = DashedLine(clock3s.get_center(), gli(Line(clock3s.get_center(), clock3s.get_center()-xphat*20), negtp))

        clock2sp = makeclock(11, 0.12).move_to(clock2sprj.get_end())
        clock3sp = makeclock(10, 0.12).move_to(clock3sprj.get_end())

        self.play(Create(clock2sprj), Create(clock3sprj), run_time=3)
        self.wait(2)
        self.play(FadeIn(*[clock2sp, clock3sp]),run_time=2)
        self.wait(3)
        self.play(FadeOut(*[clock2sp, clock3sp, clock2sprj, clock3sprj]), run_time=2)
        self.wait(2)

        clock3s_sim = Line(gli(Line(clock3s.get_center(), clock3s.get_center()-xphat*20), negtp), clock3s.get_center()).set_color(NeonOrange)
        self.play(Create(clock3s_sim), run_time=2)

        clock2sdeltp = Arrow(clock2s.get_center(), gli(Line(clock2s.get_center(), clock2s.get_center()-tphat*10), clock3s_sim), buff=0).set_color(VibrantGreen)
        clock1sdeltp = Arrow(clock1s.get_center(), clock3s_sim.get_start(), buff=0).set_color(VibrantGreen)

        self.play(Create(clock2sdeltp), Create(clock1sdeltp), run_time=3)

        clock1sf = makeclock(10, 0.12).move_to(clock3s_sim.get_start())
        clock2sf = makeclock(11, 0.12).move_to(gli(Line(clock2s.get_center(), clock2s.get_center()-tphat*10), clock3s_sim))

        self.play(Transform(clock1s, clock1sf), Transform(clock2s, clock2sf),
                  FadeOut(*[clock1sdeltp, clock2sdeltp]), run_time=2)

        self.wait(5)
        self.play(Indicate(clock3s))
        self.wait(2)
        self.play(FadeOut(*[clock1s, clock2s, clock3s, negax, negtp, negxp, negtplabel, negxplabel, clock3s_sim]), run_time=2)
        self.play(self.camera.frame.animate(run_time=3).scale(1.1).shift(UP*0.7+RIGHT*2))


        theLT = MathTex(r"t' = \gamma\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*1.5+LEFT).scale(1.15)

        xpt = Dot([clock3s.get_x(), OG[1],0]).set_color(LightBlue)
        xppt = Dot(gli(Line(xpt.get_center(), xpt.get_center()+that*10), xp)).set_color(LightBlue)
        tpt = Dot([OG[0], xppt.get_y(), 0]).set_color(LightBlue)

        xpt_xppt = DashedLine(xpt.get_top(), xppt.get_bottom(), buff=0).set_color(LightBlue)
        xppt_tpt = DashedLine(xppt.get_left(), tpt.get_right(), buff=0).set_color(LightBlue)

        xptcoords = MathTex("(x,t)", "= (L, 0)").move_to(xpt.get_center()).shift(DOWN*0.55+RIGHT*0.6).set_color(gndhighlight)
        xptcoords1 = MathTex("x = L").move_to(xpt.get_center()).shift(DOWN*0.55+RIGHT*0.6).set_color(gndhighlight)
        xpptcoords = MathTex("t'=0").move_to(xppt.get_center()).shift(DOWN*0.4+RIGHT*0.7).set_color(phighlight)

        self.play(Create(xpt), Create(xppt), Create(tpt), run_time=2)
        self.play(Create(xpt_xppt), Create(xppt_tpt), run_time=2)
        self.wait(2)
        self.play(Write(theLT), run_time=3)
        self.wait(2)
        self.play(Write(xptcoords), run_time=2)
        self.wait()
        self.play(Transform(xptcoords, xptcoords1),run_time=1.5)
        self.wait(2)
        self.play(Write(xpptcoords), run_time=1.5)
        self.wait(1)
        self.play(AnimationGroup(Indicate(xpt), Indicate(tpt)))
        self.wait()
        self.play(Indicate(xppt))

        theLT0 = MathTex("0", r"= \gamma", r"\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*3+LEFT).scale(1.15)
        theLT0[0].set_color(phighlight)
        zerobrace = Brace(theLT0[2]).set_color(gndhighlight)
        iszero = MathTex("0").set_color(gndhighlight).move_to(zerobrace.get_center()).shift(DOWN*0.4)

        theLT1 = MathTex("t", "-",  r"\frac{v}{c^2}L", "= 0").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*4.5+LEFT).scale(1.15)
        theLT1[0].set_color(gndhighlight)
        theLT1[2].set_color(gndhighlight).set_opacity(0.2)


        theLT0ghost = theLT0.copy().set_opacity(0.2)

        theLTresult = MathTex("t", "=",  r"\frac{Lv}{c^2}").set_color(propercolor).move_to(ax.x_axis.get_center()).move_to(theLT1.get_center()).scale(1.5)

        self.play(Write(theLT0ghost), run_time=2)
        self.play(ReplacementTransform(xpptcoords, theLT0[0]), run_time=2)
        self.wait()
        self.play(ReplacementTransform(theLT0ghost, theLT0))
        self.wait()
        self.play(FadeIn(zerobrace), Write(iszero), run_time=2)
        self.wait(2)
        self.play(FadeOut(*[zerobrace, iszero]))
        self.play(Write(theLT1))
        self.wait(2)
        self.play(xptcoords.animate(run_time=3).move_to(theLT1[2].get_center()).set_opacity(0),
                  theLT1[2].animate(run_time=1).set_opacity(1))
        
        self.wait(2)
        self.play(FadeOut(*[theLT, theLT0]),run_time=2)
        self.play(ReplacementTransform(theLT1, theLTresult),run_time=3)
        self.play(theLTresult.animate(run_time=2.5).move_to(theLT.get_center()))
        self.wait()
        boxit = SurroundingRectangle(theLTresult).scale(1.1).set_color(propercolor)
        self.play(self.camera.frame.animate(run_time=6).scale(1.5).move_to(theLTresult))

 
