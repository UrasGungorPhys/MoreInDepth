# COOLEST part of SR

# all observers agree that this is the length L from the origin, where it lands on the coordinates of the others
# Show how the distances are shorter as they get closer to the lightray
# Show how the hyperbolae represent the same thing as the circles do on Euc space.
from manim import *
import numpy as np
import math
import sympy as sp


config.pixel_width = 1080
config.pixel_height = 1920



MistyBlue= ManimColor.from_hex("#404e7c")
ChopinBlue= ManimColor.from_hex("#2a3d45")
FernGreen= ManimColor.from_rgb([58, 125, 68])
Mustard= ManimColor.from_rgb([231, 187, 65])
VibrantPink= ManimColor.from_hex("#ED217C")
VibrantPink2= ManimColor.from_hex("#BF1363")
PastelGreen=ManimColor.from_hex("#00AF54")
VibrantGreen= ManimColor.from_hex("#29BF12")
LightBlue= ManimColor.from_hex("#74C0F3")
LighterBlue = ManimColor.from_hex("#99CBED")
RedOrange= ManimColor.from_hex("#BA1200")
SkyBlue= ManimColor.from_hex("#01FDF6")
OrangeOrange= ManimColor.from_hex("#FF5714")
NicerOrange= ManimColor.from_hex("#F75C03")
GoodOrange= ManimColor.from_hex("#E53D00")
Salmon= ManimColor.from_hex("#C73E1D")
PastelRed= ManimColor.from_hex("#9E2B25")
SteelBlue = ManimColor.from_hex("#3F88C5")
Samoyed = ManimColor.from_hex("#E0E2DB")
NeonOrange = ManimColor.from_hex("#F9823C")
DarkPurple = ManimColor.from_hex("#2f3061")
Emerald = ManimColor.from_hex("#23CE6B")
FakeRaspberry = ManimColor.from_hex("#F72585")
MateOrange = ManimColor.from_hex("#E4572E")

BGBlue1 = ManimColor.from_hex("#0B1A27")
BGBlue2 = ManimColor.from_hex("#091D2E")
BGtry = ManimColor.from_hex("#141D29")

FunRed = ManimColor.from_hex("#EF271B")
Greenough = ManimColor.from_hex("#53FF45")
PlasticPink = ManimColor.from_hex("#ED217C")
Vanilla = ManimColor.from_hex("#F5E2C8")
SchoolBus = ManimColor.from_hex("#FDE12D")
NewOrange1 = ManimColor.from_hex("#F34213")
NewOrange2 = ManimColor.from_hex("#FE5F00")
LemonOrange = ManimColor.from_hex("#F18F01")
Vanilla2 = ManimColor.from_hex("#E8D0B7")

gndcolor1 = Vanilla2
gndcolor2 = SteelBlue
gndhighlight = LightBlue
gndhighlight2 = Greenough

pcolor1 = LightBlue
pcolor2 = SteelBlue
phighlight = LemonOrange
phighlight2 = FakeRaspberry

highlight = Emerald

propercolor = Vanilla2
lightcolor = LemonOrange


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


def gl_sxinterval(line, length):

    #only works for lines from origin
    st = line.get_start()
    en = line.get_end()
    delx = np.abs(en[0] - st[0])
    dely = np.abs(en[1] - st[1])
    slope = delx/dely

    int_t = np.sqrt(length**2/(1-slope**2))
    int_x = slope*int_t
    

    return([int_x, int_t, 0])


def homemade_grid(axes, xrange, yrange, colorchoice, opacitychoice=0.25):

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


def line_function_intersection(line, func, ax):
    """
    Finds intersection points between a Manim Line mobject
    and a curve defined as y = func(x).

    Parameters
    ----------
    line : Line (Manim mobject)
        The line to intersect with the function.
    func : callable
        A function f(x) returning y values (e.g. lambda x: ...).

    Returns
    -------
    intersections : list of np.array([x, y, 0])
        A list of intersection points (can be 0, 1, or more).
    """
    # Symbols
    x = sp.symbols("x")

    # Line endpoints
    p1 = ax.p2c(line.get_start())
    p2 = ax.p2c(line.get_end())

    # Line equation in parametric form
    t = sp.symbols("t", real=True)
    x_t = p1[0] + t * (p2[0] - p1[0])
    y_t = p1[1] + t * (p2[1] - p1[1])

    # Equation of intersection: y_line(t) - f(x_line(t)) = 0
    eq = sp.Eq(y_t, func(x_t))

    # Solve
    sols = sp.solve(eq, t)

    intersections = []
    for s in sols:
        if s.is_real:
            xi = float(x_t.subs(t, s))
            yi = float(y_t.subs(t, s))
            if xi >= 8:
                intersections.append(np.array([xi, yi, 0.0]))

    return intersections


def lorentz_grid(xp, tp, colorchoice, opacitychoice=0.25):
    pass


def reverse_rate_func(func):
    return lambda t: func(1 - t)


def makeclock(time, scale):

    clockscale = scale
    clockimg = ImageMobject("clock.png").scale(clockscale)
    clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(gndcolor1).move_to(clockimg.get_center()).scale(clockscale))
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



# class InvariantHyperbolasCONFUSION(MovingCameraScene):

#     def construct(self):
#         self.camera.background_color = ManimColor.from_hex("#171717")
  
#         campos0 = self.camera.frame.get_center()

        
#         ll = 6  # axis lengths to draw
#         axrange = 10  # coordinate ranges
#         norm = ll/axrange  # normalize any distance to fit
#         pcolor=BLUE_C  # Color to use for the primed axes

#         # Stationary axes:

#         ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
#         x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


#         ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

#         xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange-0.2,axrange-0.2)).set_color(lightcolor)
#         xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange-0.2,axrange-0.2)).set_color(lightcolor)
#         # lightlabel = MathTex("c").next_to(xct.get_end(), UR).set_color(lightcolor)

#         # Initial axes, to be Lorentz transformed:
#         OG = ax.c2p(0,0)
#         xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
#         that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

#         xpi = Arrow(start=OG, end=OG+10*xhat, buff=0).set_color(pcolor1)
#         tpi = Arrow(start=OG, end=OG+10*that, buff=0).set_color(pcolor1)

#         xp0 = Arrow(start=OG, end=OG+10*xhat, buff=0).set_color(pcolor1).set_opacity(0)
#         tp0 = Arrow(start=OG, end=OG+10*that, buff=0).set_color(pcolor1).set_opacity(0)


#         # Lorentz axes

#         def lorentz_axifier(v, origin, length):
#             OG = origin
#             gamma = 1/np.sqrt(1-v**2)

#             xp_direction = np.array([1,v,0])
#             tp_direction = np.array([v,1,0]) 

#             xphat = xp_direction
#             tphat = tp_direction

#             xp = Arrow(start=OG, end=OG + length*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
#             xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)

#             tp = Arrow(start=OG, end=OG + length*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
#             tplabel = always_redraw(lambda : MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2))

#             return [xp, tp, xplabel, tplabel]

#         xct_long = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange+2.5,axrange+2.5)).set_color(lightcolor)
#         # lightlabel_long = MathTex("c").next_to(xct_long.get_end(), DR).set_color(lightcolor)

#         hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(ax.x_axis.get_center(), DOWN).set_color(SchoolBus)


#         # L1 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 3)))
#         # L2 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 5)))
#         # L3 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 7)))

#         L0x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 1))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L1x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 2))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L2x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 3))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L3x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 4))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L4x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 5))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L5x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 6))).set_color(PlasticPink).scale(1.1).set_z_index(1))
#         L6x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 7))).set_color(PlasticPink).scale(1.1).set_z_index(1))

#         L0t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 1))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L1t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 2))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L2t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 3))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L3t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 4))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L4t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 5))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L5t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 6))).set_color(SkyBlue).scale(1.1).set_z_index(1))
#         L6t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 7))).set_color(SkyBlue).scale(1.1).set_z_index(1))

#         Ldots = VGroup(L0x,L1x,L2x,L3x,L4x,L5x,L6x, L0t,L1t,L2t,L3t,L4t,L5t,L6t)

#         # xpu_Lpt = Dot(gndax.c2p(*gl_stinterval(xpu, properL))).set_color(propercolor)
        
#         # Plays!
#         self.play(Create(ax), Create(ax_labels), run_time=1)
#         self.play(AnimationGroup(Create(xct)), run_time=2)
#         self.bring_to_front(ax)
#         metricwrong = MathTex(r"x^2 + y^2 = s^2").next_to(ax.x_axis.get_center(), UP).shift(UP*3.8).set_color(Vanilla).set_opacity(0.8).scale(1.8)
#         rectwrong = SurroundingRectangle(metricwrong).set_fill(opacity=1).set_color(MistyBlue)
#         metricright = MathTex(r"x^2 - c^2 t^2 = s^2").next_to(ax.x_axis.get_center(), UP).shift(UP*1.7).set_color(Vanilla).set_opacity(0.8).scale(1.8)
#         rectright = SurroundingRectangle(metricright).set_fill(opacity=1).set_color(MistyBlue)

#         self.play(Create(rectwrong), Write(metricwrong))
#         self.wait()
#         self.play(Create(rectright), Write(metricright))
#         self.wait()
#         self.play(metricwrong.animate.set_color(FunRed).set_opacity(0.4),
#                   metricright.animate.set_color(Greenough).set_opacity(1))
#         self.wait(2)
#         self.play(FadeOut(*[metricright, metricwrong]))
#         self.play(FadeOut(*[rectwrong, rectright]), run_time=0.2)

#         self.play(FadeIn(*[xpi, tpi]), run_time=2)
#         self.wait(0.5)
#         self.play(FadeIn(Ldots))

#         xp1, tp1, xplabel1, tplabel1 = lorentz_axifier(0.25, OG, length=6.5)
#         xp2, tp2, xplabel2, tplabel2 = lorentz_axifier(0.50, OG, length=7.3)
#         xp3, tp3, xplabel3, tplabel3 = lorentz_axifier(0.75, OG, length=8.5)
#         xp4, tp4, xplabel4, tplabel4 = lorentz_axifier(0.85, OG, length=11)
#         vtracker = ValueTracker(0.00)
#         vlabelpos = Dot().move_to(xp0.get_end()).shift(UP*0.8+LEFT).scale(0.8).set_opacity(0)
#         vl = always_redraw(lambda: MathTex(f"v = {vtracker.get_value():.2f}c").scale(0.75).set_color(propercolor).move_to(vlabelpos.get_center()))
#         vl1 = MathTex("v = 0.25c").set_color(propercolor).move_to(xp1.get_end()).shift(UP*0.6+LEFT*0.4).scale(0.75)
#         vl2 = MathTex("v = 0.50c").set_color(propercolor).move_to(xp2.get_end()).shift(UP*0.8+LEFT*0.2).scale(0.75)
#         vl3 = MathTex("v = 0.75c").set_color(propercolor).move_to(xp3.get_end()).shift(RIGHT).scale(0.75)
#         vl4 = MathTex("v = 0.85c").set_color(propercolor).move_to(xp4.get_end()).shift(DOWN*1.8+LEFT*0.5).scale(0.75)

#         self.play(Write(vl))
#         self.wait()
#         self.play(AnimationGroup(Transform(xpi, xp1, rate_func=linear), Transform(tpi, tp1, rate_func=linear),
#                 self.camera.frame.animate.scale(1.2).shift(UP*0.5+RIGHT*0.6),run_time=2.5),
#                 vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.25) ,
#                 vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl1))
        
#         self.wait()

#         self.play(AnimationGroup(Transform(xpi, xp2, rate_func=linear), Transform(tpi, tp2, rate_func=linear),run_time=2.5),
#                                   vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.50),
#                                     vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl2))
#         self.wait()
        
#         self.play(AnimationGroup(Transform(xpi, xp3, rate_func=linear), Transform(tpi, tp3, rate_func=linear),
#                                  self.camera.frame.animate.scale(1.1).shift(UP*0.5+RIGHT*0.6),run_time=2.5),
#                   vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.75),
#                                     vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl3))
#         self.wait()
        
#         self.play(AnimationGroup(Transform(xpi, xp4, rate_func=linear), Transform(tpi, tp4, rate_func=linear),
#                  Transform(xct, xct_long), run_time=2.5),
#                   vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.85),
#                                     vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl4))

#         self.wait(2)
#         self.play(FadeOut(*[Ldots, vl]))
#         # to understand exactly what this means, let's keep track of one point, call it a distance L down here.
#         self.play(Transform(xpi, xp0), Transform(tpi, tp0), Transform(xct, xct0), ax.animate.set_color(FunRed),
#                   ax_labels.animate.set_color(FunRed),
#                   self.camera.frame.animate.scale(0.8).shift(LEFT*0.9+DOWN),run_time=1.5)

#         L4x = Dot(ax.c2p(*gl_stinterval(xpi, 5))).set_z_index(1)
#         L4t = Dot(ax.c2p(*gl_sxinterval(tpi, 5))).set_color(SkyBlue).set_z_index(1)
#         Llabel = MathTex("L").set_color(Vanilla).move_to(L4x).shift(DOWN*0.5)


#         self.play(FadeIn(*[L4x, L4t]))
#         self.play(Write(Llabel))
        

#         self.wait(2)

#         spacelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 - 5**2), x_range=[5,10.4,0.01]).set_color(NewOrange2)
#         timelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 + 5**2), x_range=[0,9.11,0.01]).set_color(NewOrange2)

#         self.play(Create(spacelike_invariant_hyperbola), run_time=2)
#         self.play(Create(timelike_invariant_hyperbola), run_time=2)
#         self.wait(2)

#         hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(spacelike_invariant_hyperbola.get_start(), DOWN).set_color(NewOrange2)
#         self.play(ReplacementTransform(Llabel, hyperbola_eqq))

#         L4xp = Dot(ax.c2p(*gl_stinterval(xp1, 5))).set_color(PlasticPink)
#         L4tp = Dot(ax.c2p(*gl_sxinterval(tp1, 5))).set_color(SkyBlue)
       
#         L4xpp = Dot(ax.c2p(*gl_stinterval(xp2, 5))).set_color(PlasticPink)
#         L4tpp = Dot(ax.c2p(*gl_sxinterval(tp2, 5))).set_color(SkyBlue)
        
#         L4xppp = Dot(ax.c2p(*gl_stinterval(xp3, 5))).set_color(PlasticPink)
#         L4tppp = Dot(ax.c2p(*gl_sxinterval(tp3, 5))).set_color(SkyBlue)
        
#         L4xplabel = MathTex("x'").move_to(xp1.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor1)
#         L4tplabel = MathTex("t'").move_to(tp1.get_end()).shift(RIGHT*0.3).set_color(pcolor1)
#         xp1.set_color(pcolor1)
#         tp1.set_color(pcolor1)

#         L4xpplabel = MathTex("x''").move_to(xp2.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor2)
#         L4tpplabel = MathTex("t''").move_to(tp2.get_end()).shift(RIGHT*0.3).set_color(pcolor2)
#         xp2.set_color(pcolor2)
#         tp2.set_color(pcolor2)

#         L4xppplabel = MathTex("x'''").move_to(xp3.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(phighlight)
#         L4tppplabel = MathTex("t'''").move_to(tp3.get_end()).shift(RIGHT*0.3).set_color(phighlight)
#         xp3.set_color(phighlight)
#         tp3.set_color(phighlight)

#         self.wait(3)
#         self.play(Create(xp1), Create(tp1), L4x.animate.set_color(PlasticPink), run_time=2)
#         self.play(Create(L4xp), Create(L4tp))
#         self.play(Write(L4xplabel), Write(L4tplabel))
#         self.wait()
#         self.play(Create(xp2), Create(tp2),run_time=2)
#         self.play(Create(L4xpp), Create(L4tpp))
#         self.play(Write(L4xpplabel), Write(L4tpplabel))
#         self.wait()
#         self.play(Create(xp3), Create(tp3),run_time=2)
#         self.play(Create(L4xppp), Create(L4tppp))
#         self.play(Write(L4xppplabel), Write(L4tppplabel))
#         self.wait(2)

#         # Draw 2 more
#         spacelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 - 3**2), x_range=[3,10,0.01]).set_color(FunRed)
#         timelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 + 3**2), x_range=[0,9.53,0.01]).set_color(FunRed)

#         spacelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 - 7**2), x_range=[7,11,0.01]).set_color(LemonOrange)
#         timelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 + 7**2), x_range=[0,8.48,0.01]).set_color(LemonOrange)

#         self.play(FadeOut(*[L4xp, L4xpp, L4xppp, L4tp, L4tpp, L4tppp, L4x, L4t,
#                             L4xplabel, L4tplabel, L4xpplabel, L4tpplabel, L4xppplabel, L4tppplabel]), run_time=2)
#         self.play(FadeOut(*[xp1, tp1, xp2, tp2, xp3, tp3]),run_time=2)
#         self.wait(3)

#         self.play(Create(spacelike_invariant_hyperbola0), Create(timelike_invariant_hyperbola0), run_time=2)
#         self.play(Create(spacelike_invariant_hyperbola2), Create(timelike_invariant_hyperbola2), run_time=2)

#         axC = Axes(x_range=[-8,8,1], y_range=[0,8,1], 
#         x_length=16, y_length=8, axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(propercolor)
#         axC.shift(OG - axC.c2p(0,0))
#         ax_labelx = MathTex("x").move_to(axC.x_axis.get_end()).shift(UP+LEFT*0.4).set_color(propercolor)
#         ax_labely = MathTex("y").move_to(axC.y_axis.get_end()).shift(DOWN*0.4+RIGHT).set_color(propercolor)
        

#         arc0 = Arc(radius=3, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(FunRed)
#         arc0n = Arc(radius=3, start_angle=PI/2, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(FunRed)
#         arc1 = Arc(radius=5, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(NewOrange2)
#         arc1n = Arc(radius=5, start_angle=PI/2, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(NewOrange2)
#         arc2 = Arc(radius=7, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(LemonOrange)
#         arc2n = Arc(radius=7, start_angle=PI/2, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(LemonOrange)


#         hyp0 = spacelike_invariant_hyperbola0
#         hyp0n = timelike_invariant_hyperbola0
#         hyp1 = spacelike_invariant_hyperbola
#         hyp1n = timelike_invariant_hyperbola
#         hyp2 = spacelike_invariant_hyperbola2
#         hyp2n = timelike_invariant_hyperbola2

#         xp1, tp1, xplabel1, tplabel1 = lorentz_axifier(0.25, OG, length=8.5)
#         xp2, tp2, xplabel2, tplabel2 = lorentz_axifier(0.50, OG, length=8.5)
#         xp3, tp3, xplabel3, tplabel3 = lorentz_axifier(0.75, OG, length=8.5)

#         xp1.set_color(SchoolBus)
#         xp2.set_color(SchoolBus)
#         xp3.set_color(SchoolBus)
#         tp1.set_color(SchoolBus)
#         tp2.set_color(SchoolBus)
#         tp3.set_color(SchoolBus)

#         self.play(FadeOut(hyperbola_eqq), run_time=2)
#         self.play(self.camera.frame.animate(run_time=2).scale(1.2).shift(LEFT*2.5))

#         self.play(ReplacementTransform(ax, axC), ReplacementTransform(ax_labels, VGroup(ax_labelx, ax_labely)))
        
#         self.wait(2)
#         self.play(ReplacementTransform(hyp0, arc0), ReplacementTransform(hyp0n, arc0n),
#                   ReplacementTransform(hyp1, arc1), ReplacementTransform(hyp1n, arc1n),
#                   ReplacementTransform(hyp2, arc2), ReplacementTransform(hyp2n, arc2n), FadeOut(xct),run_time=3)
        
#         self.wait(2)
#         self.play(FadeIn(*[xp1, tp1, xp2, tp2, xp3, tp3]))

#         def get_circ_intersects(line, radius):
#             lineslope = (line.get_end()[1] - line.get_start()[1])/(line.get_end()[0] - line.get_start()[0])
#             x = np.sqrt(radius**2 / (1+lineslope**2))
#             y = lineslope*x

#             return([x,y,0])
        
#         arc1_intersections = VGroup()
#         for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
#             ints = get_circ_intersects(line, 3)
#             print(ints)
#             intdot = Dot(axC.c2p(*ints)).set_color(BLUE_C)
#             arc1_intersections.add(intdot)

        
#         arc2_intersections = VGroup()
#         for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
#             ints = get_circ_intersects(line, 5)
#             print(ints)
#             intdot = Dot(axC.c2p(*ints)).set_color(BLUE_B)
#             arc2_intersections.add(intdot)


#         arc3_intersections = VGroup()
#         for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
#             ints = get_circ_intersects(line, 7)
#             print(ints)
#             intdot = Dot(axC.c2p(*ints)).set_color(SkyBlue)
#             arc3_intersections.add(intdot)

#         self.play(Create(arc1_intersections))
#         self.play(Create(arc2_intersections))
#         self.play(Create(arc3_intersections))

#         self.wait(3)

#         self.play(FadeOut(*[xp1, tp1, xp2, tp2, xp3, tp3, arc1_intersections, arc2_intersections, arc3_intersections]), run_time=2)

#         ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
#         x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

#         spacelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 - 3**2), x_range=[3,10,0.01]).set_color(FunRed)
#         timelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 + 3**2), x_range=[0,9.53,0.01]).set_color(FunRed)

#         spacelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 - 7**2), x_range=[7,11,0.01]).set_color(LemonOrange)
#         timelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 + 7**2), x_range=[0,8.48,0.01]).set_color(LemonOrange)
#         spacelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 - 5**2), x_range=[5,10.4,0.01]).set_color(NewOrange2)
#         timelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 + 5**2), x_range=[0,9.11,0.01]).set_color(NewOrange2)




#         hyp0 = VGroup(spacelike_invariant_hyperbola0, timelike_invariant_hyperbola0)
#         hyp1 = VGroup(spacelike_invariant_hyperbola, timelike_invariant_hyperbola)
#         hyp2 = VGroup(spacelike_invariant_hyperbola2, timelike_invariant_hyperbola2)

        
#         ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)


#         self.play(ReplacementTransform(axC, ax), ReplacementTransform(VGroup(ax_labelx, ax_labely), ax_labels),
#             ReplacementTransform(arc0, hyp0), ReplacementTransform(arc1, hyp1), ReplacementTransform(arc2,hyp2),
#             self.camera.frame.animate.shift(LEFT*0.5+DOWN*0.5).scale(0.9), run_time=3)
        
#         self.wait(5)



class InvariantHyperbolas(MovingCameraScene):

    def construct(self):
        self.camera.background_color = ManimColor.from_hex("#171717")
  
        campos0 = self.camera.frame.get_center()
        self.camera.frame.scale(0.6)

        
        ll = 6  # axis lengths to draw
        axrange = 10  # coordinate ranges
        norm = ll/axrange  # normalize any distance to fit
        pcolor=BLUE_C  # Color to use for the primed axes

        # Stationary axes:

        ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange-0.2,axrange-0.2)).set_color(lightcolor)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange-0.2,axrange-0.2)).set_color(lightcolor)
        # lightlabel = MathTex("c").next_to(xct.get_end(), UR).set_color(lightcolor)

        # Initial axes, to be Lorentz transformed:
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

        xpi = Arrow(start=OG, end=OG+10*xhat, buff=0).set_color(pcolor1)
        tpi = Arrow(start=OG, end=OG+10*that, buff=0).set_color(pcolor1)

        xp0 = Arrow(start=OG, end=OG+10*xhat, buff=0).set_color(pcolor1).set_opacity(0)
        tp0 = Arrow(start=OG, end=OG+10*that, buff=0).set_color(pcolor1).set_opacity(0)


        # Lorentz axes

        def lorentz_axifier(v, origin, length):
            OG = origin
            gamma = 1/np.sqrt(1-v**2)

            xp_direction = np.array([1,v,0])
            tp_direction = np.array([v,1,0]) 

            xphat = xp_direction
            tphat = tp_direction

            xp = Arrow(start=OG, end=OG + length*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
            xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor2)

            tp = Arrow(start=OG, end=OG + length*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
            tplabel = always_redraw(lambda : MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor2))

            return [xp, tp, xplabel, tplabel]

        xct_long = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange+2.5,axrange+2.5)).set_color(lightcolor)
        # lightlabel_long = MathTex("c").next_to(xct_long.get_end(), DR).set_color(lightcolor)

        hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(ax.x_axis.get_center(), DOWN).set_color(SchoolBus)


        # L1 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 3)))
        # L2 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 5)))
        # L3 = Dot(ax.c2p(*gl_stinterval(ax.x_axis, 7)))

        L0x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 1))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L1x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 2))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L2x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 3))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L3x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 4))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L4x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 5))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L5x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 6))).set_color(PlasticPink).scale(1.1).set_z_index(1))
        L6x = always_redraw(lambda:Dot(ax.c2p(*gl_stinterval(xpi, 7))).set_color(PlasticPink).scale(1.1).set_z_index(1))

        L0t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 1))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L1t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 2))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L2t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 3))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L3t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 4))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L4t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 5))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L5t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 6))).set_color(SkyBlue).scale(1.1).set_z_index(1))
        L6t = always_redraw(lambda:Dot(ax.c2p(*gl_sxinterval(tpi, 7))).set_color(SkyBlue).scale(1.1).set_z_index(1))

        Ldots = VGroup(L0x,L1x,L2x,L3x,L4x,L5x,L6x, L0t,L1t,L2t,L3t,L4t,L5t,L6t)

        # xpu_Lpt = Dot(gndax.c2p(*gl_stinterval(xpu, properL))).set_color(propercolor)
        
        # Plays!
        self.play(Create(ax), Create(ax_labels), run_time=1)
        self.play(AnimationGroup(Create(xct)), run_time=2)
        self.bring_to_front(ax)
        metricwrong = MathTex(r"x^2 + y^2 = s^2").next_to(ax.x_axis.get_center(), UP).shift(UP*3.8).set_color(Vanilla).set_opacity(0.8).scale(1.8)
        rectwrong = SurroundingRectangle(metricwrong).set_fill(opacity=1).set_color(MistyBlue)
        metricright = MathTex(r"x^2 - c^2 t^2 = s^2").next_to(ax.x_axis.get_center(), UP).shift(UP*1.7).set_color(Vanilla).set_opacity(0.8).scale(1.8)
        rectright = SurroundingRectangle(metricright).set_fill(opacity=1).set_color(MistyBlue)

        # self.play(Create(rectwrong), Write(metricwrong))
        # self.wait()
        # self.play(Create(rectright), Write(metricright))
        # self.wait()
        # self.play(metricwrong.animate.set_color(FunRed).set_opacity(0.4),
        #           metricright.animate.set_color(Greenough).set_opacity(1))
        # self.wait(2)
        # self.play(FadeOut(*[metricright, metricwrong]))
        # self.play(FadeOut(*[rectwrong, rectright]), run_time=0.2)

        self.play(FadeIn(*[xpi, tpi]), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(Ldots))

        xp1, tp1, xplabel1, tplabel1 = lorentz_axifier(0.25, OG, length=6.5)
        xp2, tp2, xplabel2, tplabel2 = lorentz_axifier(0.50, OG, length=7.3)
        xp3, tp3, xplabel3, tplabel3 = lorentz_axifier(0.75, OG, length=8.5)
        xp4, tp4, xplabel4, tplabel4 = lorentz_axifier(0.85, OG, length=11)
        vtracker = ValueTracker(0.00)
        vlabelpos = Dot().move_to(xp0.get_end()).shift(UP*0.8+LEFT).scale(0.8).set_opacity(0)
        vl = always_redraw(lambda: MathTex(f"v = {vtracker.get_value():.2f}c").scale(0.75).set_color(propercolor).move_to(vlabelpos.get_center()))
        vl1 = MathTex("v = 0.25c").set_color(propercolor).move_to(xp1.get_end()).shift(UP*0.6+LEFT*0.4).scale(0.75)
        vl2 = MathTex("v = 0.50c").set_color(propercolor).move_to(xp2.get_end()).shift(UP*0.8+LEFT*0.2).scale(0.75)
        vl3 = MathTex("v = 0.75c").set_color(propercolor).move_to(xp3.get_end()).shift(RIGHT).scale(0.75)
        vl4 = MathTex("v = 0.85c").set_color(propercolor).move_to(xp4.get_end()).shift(DOWN*1.8+LEFT*0.5).scale(0.75)

        self.play(Write(vl))
        self.wait()
        self.play(AnimationGroup(Transform(xpi, xp1, rate_func=linear), Transform(tpi, tp1, rate_func=linear),
                self.camera.frame.animate.scale(1.2).shift(UP*0.5+RIGHT*0.6),run_time=2.5),
                vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.25) ,
                vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl1))
        
        self.wait()

        self.play(AnimationGroup(Transform(xpi, xp2, rate_func=linear), Transform(tpi, tp2, rate_func=linear),run_time=2.5),
                                  vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.50),
                                    vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl2))
        self.wait()
        
        self.play(AnimationGroup(Transform(xpi, xp3, rate_func=linear), Transform(tpi, tp3, rate_func=linear),
                                 self.camera.frame.animate.scale(1.1).shift(UP*0.5+RIGHT*0.6),run_time=2.5),
                  vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.75),
                                    vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl3))
        self.wait()
        
        self.play(AnimationGroup(Transform(xpi, xp4, rate_func=linear), Transform(tpi, tp4, rate_func=linear),
                 Transform(xct, xct_long), run_time=2.5),
                  vtracker.animate(run_time=2.5, rate_func=linear).set_value(0.85),
                                    vlabelpos.animate(run_time=2.5, rate_func=linear).move_to(vl4))

        self.wait(2)
        self.play(FadeOut(*[Ldots, vl]))
        # to understand exactly what this means, let's keep track of one point, call it a distance L down here.
        self.play(Transform(xpi, xp0), Transform(tpi, tp0), Transform(xct, xct0), ax.animate.set_color(LighterBlue),
                  ax_labels.animate.set_color(LighterBlue),
                  self.camera.frame.animate.scale(0.8).shift(LEFT*0.9+DOWN),run_time=1.5)

        L4x = Dot(ax.c2p(*gl_stinterval(xpi, 5))).set_z_index(1)
        L4t = Dot(ax.c2p(*gl_sxinterval(tpi, 5))).set_color(SkyBlue).set_z_index(1)
        Llabel = MathTex("L").set_color(Vanilla).move_to(L4x).shift(DOWN*0.5)


        self.play(FadeIn(*[L4x, L4t]))
        self.play(Write(Llabel))
        

        self.wait(2)

        spacelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 - 5**2), x_range=[5,10.4,0.01]).set_color(NewOrange2)
        timelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 + 5**2), x_range=[0,9.11,0.01]).set_color(NewOrange2)

        self.play(Create(spacelike_invariant_hyperbola), run_time=2)
        self.play(Create(timelike_invariant_hyperbola), run_time=2)
        self.wait(2)

        hyperbola_eqq = MathTex(r"x^2 - c^2 t^2 = L^2").next_to(spacelike_invariant_hyperbola.get_start(), DOWN).set_color(NewOrange2)
        self.play(ReplacementTransform(Llabel, hyperbola_eqq))

        L4xp = Dot(ax.c2p(*gl_stinterval(xp1, 5))).set_color(Vanilla)
        L4tp = Dot(ax.c2p(*gl_sxinterval(tp1, 5))).set_color(Vanilla)
       
        L4xpp = Dot(ax.c2p(*gl_stinterval(xp2, 5))).set_color(Vanilla)
        L4tpp = Dot(ax.c2p(*gl_sxinterval(tp2, 5))).set_color(Vanilla)
        
        L4xppp = Dot(ax.c2p(*gl_stinterval(xp3, 5))).set_color(Vanilla)
        L4tppp = Dot(ax.c2p(*gl_sxinterval(tp3, 5))).set_color(Vanilla)
        
        L4xplabel = MathTex("x'").move_to(xp1.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor1)
        L4tplabel = MathTex("t'").move_to(tp1.get_end()).shift(RIGHT*0.3).set_color(pcolor1)
        xp1.set_color(pcolor1)
        tp1.set_color(pcolor1)

        L4xpplabel = MathTex("x''").move_to(xp2.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor2)
        L4tpplabel = MathTex("t''").move_to(tp2.get_end()).shift(RIGHT*0.3).set_color(pcolor2)
        xp2.set_color(pcolor2)
        tp2.set_color(pcolor2)

        L4xppplabel = MathTex("x'''").move_to(xp3.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(MistyBlue)
        L4tppplabel = MathTex("t'''").move_to(tp3.get_end()).shift(RIGHT*0.3).set_color(MistyBlue)
        xp3.set_color(MistyBlue)
        tp3.set_color(MistyBlue)

        self.wait(3)
        self.play(Create(xp1), Create(tp1), L4x.animate.set_color(PlasticPink), run_time=2)
        self.play(Create(L4xp), Create(L4tp))
        self.play(Write(L4xplabel), Write(L4tplabel))
        self.wait()
        self.play(Create(xp2), Create(tp2),run_time=2)
        self.play(Create(L4xpp), Create(L4tpp))
        self.play(Write(L4xpplabel), Write(L4tpplabel))
        self.wait()
        self.play(Create(xp3), Create(tp3),run_time=2)
        self.play(Create(L4xppp), Create(L4tppp))
        self.play(Write(L4xppplabel), Write(L4tppplabel))
        self.wait(2)

        # Draw 2 more
        spacelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 - 3**2), x_range=[3,10,0.01]).set_color(FunRed)
        timelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 + 3**2), x_range=[0,9.53,0.01]).set_color(FunRed)

        spacelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 - 7**2), x_range=[7,11,0.01]).set_color(LemonOrange)
        timelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 + 7**2), x_range=[0,8.48,0.01]).set_color(LemonOrange)

        self.play(FadeOut(*[L4xp, L4xpp, L4xppp, L4tp, L4tpp, L4tppp, L4x, L4t,
                            L4xplabel, L4tplabel, L4xpplabel, L4tpplabel, L4xppplabel, L4tppplabel]), run_time=2)
        self.play(FadeOut(*[xp1, tp1, xp2, tp2, xp3, tp3]),run_time=2)
        self.wait(3)

        self.play(Create(spacelike_invariant_hyperbola0), Create(timelike_invariant_hyperbola0), run_time=2)
        self.play(Create(spacelike_invariant_hyperbola2), Create(timelike_invariant_hyperbola2), run_time=2)

        axC = Axes(x_range=[0,8,1], y_range=[0,8,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(propercolor)
        axC.shift(OG - axC.c2p(0,0))
        ax_labelx = MathTex("x").move_to(axC.x_axis.get_end()).shift(UP+LEFT*0.4).set_color(propercolor)
        ax_labely = MathTex("y").move_to(axC.y_axis.get_end()).shift(DOWN*0.4+RIGHT).set_color(propercolor)
        

        arc0 = Arc(radius=3, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(FunRed)
        arc1 = Arc(radius=5, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(NewOrange2)
        arc2 = Arc(radius=7, angle=PI/2, arc_center=axC.c2p(0,0)).set_color(LemonOrange)

        hyp0 = VGroup(spacelike_invariant_hyperbola0, timelike_invariant_hyperbola0)
        hyp1 = VGroup(spacelike_invariant_hyperbola, timelike_invariant_hyperbola)
        hyp2 = VGroup(spacelike_invariant_hyperbola2, timelike_invariant_hyperbola2)

        xp1, tp1, xplabel1, tplabel1 = lorentz_axifier(0.25, OG, length=8.5)
        xp2, tp2, xplabel2, tplabel2 = lorentz_axifier(0.50, OG, length=8.5)
        xp3, tp3, xplabel3, tplabel3 = lorentz_axifier(0.75, OG, length=8.5)

        xp1.set_color(SchoolBus)
        xp2.set_color(SchoolBus)
        xp3.set_color(SchoolBus)
        tp1.set_color(SchoolBus)
        tp2.set_color(SchoolBus)
        tp3.set_color(SchoolBus)

        self.play(FadeOut(hyperbola_eqq), run_time=2)
        self.play(self.camera.frame.animate(run_time=2).scale(1.2).shift(RIGHT*0.7))

        self.play(ReplacementTransform(ax, axC), ReplacementTransform(ax_labels, VGroup(ax_labelx, ax_labely)))
        
        self.wait(2)
        self.play(ReplacementTransform(hyp0, arc0), ReplacementTransform(hyp1, arc1), 
                  ReplacementTransform(hyp2, arc2), FadeOut(xct),run_time=3)
        self.wait(2)
        self.play(FadeIn(*[xp1, tp1, xp2, tp2, xp3, tp3]))

        def get_circ_intersects(line, radius):
            lineslope = (line.get_end()[1] - line.get_start()[1])/(line.get_end()[0] - line.get_start()[0])
            x = np.sqrt(radius**2 / (1+lineslope**2))
            y = lineslope*x

            return([x,y,0])
        
        arc1_intersections = VGroup()
        for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
            ints = get_circ_intersects(line, 3)
            print(ints)
            intdot = Dot(axC.c2p(*ints)).set_color(BLUE_C)
            arc1_intersections.add(intdot)

        
        arc2_intersections = VGroup()
        for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
            ints = get_circ_intersects(line, 5)
            print(ints)
            intdot = Dot(axC.c2p(*ints)).set_color(BLUE_B)
            arc2_intersections.add(intdot)


        arc3_intersections = VGroup()
        for line in [xp1, tp1, xp2, tp2, xp3, tp3]:
            ints = get_circ_intersects(line, 7)
            print(ints)
            intdot = Dot(axC.c2p(*ints)).set_color(SkyBlue)
            arc3_intersections.add(intdot)

        self.play(Create(arc1_intersections))
        self.play(Create(arc2_intersections))
        self.play(Create(arc3_intersections))

        self.wait(3)

        self.play(FadeOut(*[xp1, tp1, xp2, tp2, xp3, tp3, arc1_intersections, arc2_intersections, arc3_intersections]), run_time=2)

        ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

        spacelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 - 3**2), x_range=[3,10,0.01]).set_color(FunRed)
        timelike_invariant_hyperbola0 = ax.plot(lambda x : np.sqrt(x**2 + 3**2), x_range=[0,9.53,0.01]).set_color(FunRed)

        spacelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 - 7**2), x_range=[7,11,0.01]).set_color(LemonOrange)
        timelike_invariant_hyperbola2 = ax.plot(lambda x : np.sqrt(x**2 + 7**2), x_range=[0,8.48,0.01]).set_color(LemonOrange)
        spacelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 - 5**2), x_range=[5,10.4,0.01]).set_color(NewOrange2)
        timelike_invariant_hyperbola = ax.plot(lambda x : np.sqrt(x**2 + 5**2), x_range=[0,9.11,0.01]).set_color(NewOrange2)


        hyp0 = VGroup(spacelike_invariant_hyperbola0, timelike_invariant_hyperbola0)
        hyp1 = VGroup(spacelike_invariant_hyperbola, timelike_invariant_hyperbola)
        hyp2 = VGroup(spacelike_invariant_hyperbola2, timelike_invariant_hyperbola2)

        
        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)


        self.play(ReplacementTransform(axC, ax), ReplacementTransform(VGroup(ax_labelx, ax_labely), ax_labels),
            ReplacementTransform(arc0, hyp0), ReplacementTransform(arc1, hyp1), ReplacementTransform(arc2,hyp2),
            self.camera.frame.animate.shift(LEFT*0.5+DOWN*0.5).scale(0.9), run_time=3)
        
        self.wait(5)



