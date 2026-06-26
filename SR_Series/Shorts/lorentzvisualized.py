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


class RearClockAheadDiagram(MovingCameraScene):

    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")
        self.camera.frame.scale(0.5)

        
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
        # lightlabel_long = MathTex("c").next_to(xct_long.get_end(), DR).set_color(lightcolor)

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
                    self.camera.frame.animate.scale(1.2).shift(UP*0.5+RIGHT*0.6),run_time=4.5)

        self.play(FadeIn(xplabel), FadeIn(tplabel), run_time=2)
        
        self.play(Indicate(manual_grids0y))

        self.play(Indicate(manual_grids0x))
        self.wait(1)

        self.play(FadeOut(manual_grids0x),FadeOut(manual_grids0y),FadeOut(grid),
                    Transform(xct,xct0.set_opacity(0.4)),
                    self.camera.frame.animate.shift(DOWN*0.1, RIGHT*0.2).scale(1.05))

        # Demonstrate projection for event p
        self.wait(1)
        self.play(Create(event0pt))
        self.bring_to_front(event0pt)
        self.wait()
        self.play(Create(event0label))
        self.wait()
        self.play(Create(event0labels), Create(event0labelsp))
        self.wait()
        self.play(FadeOut(event0labelsp), FadeOut(event0labels))
        self.wait()
        self.play(self.camera.frame.animate.shift(LEFT*0.5).scale(1/1.05))

        # self.play(Create(event0_prjtp),Create(event0_prjxp))  # to check if needed
        self.add(xplenfortransform)
        self.play(ShowPassingFlash(xpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(xplenfortransform.animate.shift(xpshift), run_time=2)  # moving a piece of x' until it intersects the event
        self.wait()
        self.play(FadeOut(xplenfortransform))
        self.play(Create(event0tp), run_time=1)
        self.play(Create(intersection_tppt))
        self.play(Create(tplen))
        self.bring_to_front(intersection_tppt)
        self.play(Create(ptplabel))

        self.wait(1.5)

        self.add(tplenfortransform)
        self.play(ShowPassingFlash(tpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(tplenfortransform.animate.shift(tpshift),run_time=2)
        self.wait()
        self.play(FadeOut(tplenfortransform))
        self.play(Create(event0xp), run_time=1)
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

        self.play(event0pt.animate.shift(RIGHT*0.5), run_time=1.5)
        self.play(event0pt.animate.shift(LEFT*3 + UP*1.6), run_time=2)
        self.play(event0pt.animate.shift(LEFT*1.2 + DOWN*2.6), run_time=1.5)
        self.play(event0pt.animate.shift(RIGHT*1.2 + DOWN*2), run_time=1.5)
        self.play(event0pt.animate.move_to(event0), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(event0label), FadeOut(event0x), FadeOut(event0t), FadeOut(pxdot), FadeOut(ptdot),
        FadeOut(event0xp),FadeOut(event0tp), FadeOut(intersection_tppt), FadeOut(intersection_xppt),
        FadeOut(pxlabel), FadeOut(ptlabel), FadeOut(tlen), FadeOut(xplen), FadeOut(tplen), FadeOut(pxplabel), FadeOut(ptplabel), run_time=2)


# Put a train where they measure proper L
# Show length contraction of train
# Show train moving to the other point while length contracted to yield the Lgamma distance

# Maybe put an emphasis on clarifying confusion? 
# (you will no longer think that) Spacetime diagrams are confusing! For example how do you project this point down?
# So skip the Lorentz transforming part maybe?