from manim import *
import numpy as np
import math
import sympy as sp


MistyBlue= ManimColor.from_hex("#404e7c")
ChopinBlue= ManimColor.from_hex("#2a3d45")
FernGreen= ManimColor.from_rgb([58, 125, 68])
Mustard= ManimColor.from_rgb([231, 187, 65])
VibrantPink= ManimColor.from_hex("#ED217C")
VibrantPink2= ManimColor.from_hex("#BF1363")
PastelGreen=ManimColor.from_hex("#00AF54")
VibrantGreen= ManimColor.from_hex("#29BF12")
LightBlue= ManimColor.from_hex("#74C0F3")
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
Basetry = ManimColor.from_hex("#25282B")

FunRed = ManimColor.from_hex("#EF271B")
Greenough = ManimColor.from_hex("#53FF45")
GreenoughDark = ManimColor.from_hex("#3AA631")
GreenoughLight = ManimColor.from_hex("#75FA69")
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


def primes(coords, v):
            x = coords[0]
            t = coords[1]

            xp = (x + v*t)/np.sqrt(1-v**2)
            tp = (t + v*x)/np.sqrt(1-v**2)

            return [xp, tp]
        

def primeslt(coords, v):
    x = coords[0]
    t = coords[1]

    xp = (x - v*t)/np.sqrt(1-v**2)
    tp = (t - v*x)/np.sqrt(1-v**2)

    return [xp, tp]


def gndslt(pcoords, v):
    xp = pcoords[0]
    tp = pcoords[1]

    x = (x + v*t)/np.sqrt(1-v**2)
    t = (t + v*x)/np.sqrt(1-v**2)

    return [x, t]


# Complete
class Intro(MovingCameraScene):
    def construct(self):

        # Inits
        self.camera.background_color=BGtry

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        


        ################################ Scene 1 - First diagram ################################
        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ogdot))
        self.wait(1)
        self.play(Transform(ogdot, ax.x_axis), self.camera.frame.animate.scale(1.1/0.6).shift(RIGHT*4), rate_func=rate_functions.ease_out_back, run_time=1.1)
        self.play(Create(ax.y_axis, rate_func=rate_functions.ease_out_back), self.camera.frame.animate(rate_func=rate_functions.ease_out_back).shift(UP*3.7), run_time=1.1)

        self.play(Create(grid1), Create(lightray), run_time=1.2)


        # Create labels?

        ################################ Scene 2 - Lorentz contract ################################
        # Let's add another pair of axes, make them blue. Add a blue label with v = 0.0 c as an updater. 
        # change the velocity and contract the axes accordingly to showcase Lorentz contraction
        v = ValueTracker(0.00)
        self.add(v)
        vlabel = always_redraw(lambda: MathTex("v ", f"= {v.get_value():.2f} c").set_color(pcolor1).move_to(lightray.get_end()).shift(LEFT*2).scale(1.4))
        tpax0 = Arrow(og,ax.c2p(0,6.2))
        xpax0 = Arrow(og,ax.c2p(6.2, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v.get_value()*L0, np.sqrt(L0**2 + (v.get_value()*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v.get_value()*L0)**2), v.get_value()*L0), buff=0).set_color(pcolor1))
        xlabel = Tex("Space").move_to(ax.x_axis.get_end()).shift(UP*0.8).set_color(gndcolor1)
        tlabel = Tex("Time").move_to(ax.y_axis.get_end()).shift(RIGHT).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(2)
        xlabelp = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabelp = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Transform(xlabel, xlabelp), Transform(tlabel, tlabelp))
        
        self.play(Create(tpax), Create(xpax), rate_func=rate_functions.ease_out_cubic)
        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))
        self.play(Write(xplabel), Write(tplabel))
        self.wait()
        self.play(Write(vlabel), run_time=1.2)
        
        self.wait()

        # self.play(v.animate.set_value(0.2), run_time=1)
        self.wait()
        self.play(v.animate.set_value(0.5), run_time=1.5)
        self.wait()
        # self.play(v.animate.set_value(0.3), run_time=0.6)
        self.wait()
        # self.play(v.animate.set_value(0.6), run_time=1.5)
        self.wait(5)


# Complete
class Intro2(MovingCameraScene):
    def construct(self):
        inftext = Text("INTRO PART 2, CUT PART WITH THIS TEXT")
        self.play(Write(inftext))

        # Inits
        self.camera.background_color=BGtry

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ogdot))
        self.wait(1)
        self.play(Transform(ogdot, ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4), rate_func=rate_functions.ease_out_back, run_time=1.1)
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)
        self.play(Write(xlabel), Write(tlabel))

        self.play(Create(grid1), run_time=1.2)
        self.play(Create(lightray), run_time=1.2)

        self.remove(inftext)
        self.wait(3)
        
        ################################ Scene 3 - Hyperbolic ################################
        #################### Set up hyperbola, draw worldline ########################
        hypx0 = 2
        hypxf = 5.5
        center=-2
        def hyperbola(x, x0=hypx0, center=-2):
            return np.sqrt((x-center)**2 - (x0)**2)
        

        def nhyperbola(x, x0=hypx0, center=-2):
            return -np.sqrt((x-center)**2 - (x0)**2)
        

        def hyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=-2):
            wlpiece = ax.plot(lambda x: hyperbola(x), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=8).set_color(phighlight2)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01], stroke_width=8).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        P = Dot(ax.c2p(center, 0, 0))
        def getxprime(x, P_point=P, colorchoice=NeonOrange):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            xp = Arrow(hyp_point, hyp_point+xphat*3, buff=0).set_color(colorchoice)

            return xp
        
        def gettprime(x, P_point=P, colorchoice=NeonOrange):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            tphat = np.array([xphat[1], xphat[0], 0])
            tp = Arrow(hyp_point, hyp_point+tphat*3, buff=0).set_color(colorchoice)
            acchere = Dot(hyp_point)

            return tp

        worldline = ax.plot(lambda x: hyperbola(x), x_range=[hypx0+center,hypxf,0.01], stroke_width=7).set_color(gndcolor2)

        ########### Setup complete ################


        self.play(Create(worldline), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        acc1 = Dot(hyperbolapiece(0,0.2).get_end(), radius=0.12).set_color(NeonOrange)
        self.play(Create(acc1))
        acctp = always_redraw(lambda: gettprime(ax.p2c(acc1.get_center())[0]))
        accxp = always_redraw(lambda: getxprime(ax.p2c(acc1.get_center())[0]))
        vlabel = always_redraw(lambda: MathTex(f"v = {glslope(accxp):.2f} c").set_z_index(1).move_to(acc1.get_center()).shift(DOWN*0.5+RIGHT*0.5).set_color(NeonOrange))
        vlabelbox = always_redraw(lambda: RoundedRectangle(corner_radius=0.2, width=vlabel.width+0.5, height=vlabel.height+0.2).set_stroke(MistyBlue).set_fill(MistyBlue, opacity=1).move_to(vlabel.get_center()))

        self.play(Create(acctp), Create(accxp))
        self.play(Write(vlabel), Create(vlabelbox)) # Add a little box around this to show it over the lines 

        self.play(MoveAlongPath(acc1, hyperbolapiece(0.2, 4.5), rate_func=rate_functions.ease_in_sine, run_time=10))        


# Complete
class Intro3(MovingCameraScene):
    def construct(self):
        inftext = Text("INTRO PART 3, CUT PART WITH THIS TEXT")
        self.play(Write(inftext))

        # Inits
        self.camera.background_color=BGtry

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ogdot))
        self.wait(1)
        self.play(ReplacementTransform(ogdot, ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4), rate_func=rate_functions.ease_out_back, run_time=1.1)
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        self.play(Create(lightray), run_time=1.2)

        self.remove(inftext)
        ################################ Scene 4 - Light rays in gravitational field, Schwarzschild ################################
        # in_geodesics = lambda r,m: r + 2*m*np.log(np.abs(r-2*m))
        # out_geodesics = lambda r,m: -r -2*m*np.log(np.abs(r-2*m))
        in_geodesics = lambda r: r + 2*np.log(np.abs(r-2)) # set m=1
        out_geodesics = lambda r: -r -2*np.log(np.abs(r-2))

        og_in_geodesics = lambda r: r+2 + 2*np.log(np.abs(r))

        x1=2.001
        x2=8

        gdsc0 = ax.plot(lambda x: og_in_geodesics(x), x_range=[0.001, x2, 0.01],use_smoothing=False, stroke_width=4).set_color(lightcolor)
        lightrayn =  Line(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        self.play(Transform(lightray, lightrayn))
        self.play(Transform(lightray, gdsc0), run_time=2, rate_func=rate_functions.ease_in_quad)

        gdsc1 = ax.plot(lambda x: in_geodesics(x), x_range=[x1,x2, 0.01], use_smoothing=False, stroke_width=4).set_color(lightcolor)
        m2line = DashedLine(ax.c2p(2,-10), ax.c2p(2,10), stroke_width=5).set_color(MistyBlue)
        self.play(Transform(lightray,gdsc1), run_time=1.2)
        self.play(FadeOut(grid1))
        self.play(Create(m2line))
        
        in_geodesic_vg = VGroup()
        for c in np.arange(-16,8,2):
            gdsci = ax.plot(lambda x: in_geodesics(x)+c, x_range=[x1, x2-c, 0.01],use_smoothing=False, stroke_width=4).set_color(lightcolor)
            gdscirev = gdsci.copy().reverse_points()
            in_geodesic_vg.add(gdscirev)


        out_geodesic_vg = VGroup()
        for c in np.arange(-6,18,2):
            gdsci = ax.plot(lambda x: out_geodesics(x)+c, x_range=[x1, x2+c, 0.01],use_smoothing=False, stroke_width=4).set_color(SteelBlue)

            out_geodesic_vg.add(gdsci)

        horizon_in_geodesic_vg = VGroup()
        for c in np.arange(-6,6,1.5):
            horizon_in_gdsc = ax.plot(lambda x: in_geodesics(x)+c, x_range=[0.01, 1.99, 0.01], use_smoothing=False, stroke_width=4).set_color(lightcolor)
            horizon_in_gdsc_rev = horizon_in_gdsc.copy().reverse_points()
            horizon_in_geodesic_vg.add(horizon_in_gdsc_rev)

        horizon_out_geodesic_vg = VGroup()
        for c in np.arange(-6,6,1.5):
            horizon_out_gdsc = ax.plot(lambda x: out_geodesics(x)+c, x_range=[0.01, 1.99, 0.01], use_smoothing=False, stroke_width=4).set_color(SteelBlue)
            horizon_out_geodesic_vg.add(horizon_out_gdsc)

        ax2 = Axes(x_range=[0,14,1], y_range=[-7,7,1],
        x_length=16, y_length=12,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        ax2.move_to(ax.c2p(7,0))
        
        # self.play(AnimationGroup(Create(in_geodesic_vg, lag_ratio=0, rate_func=rate_functions.ease_in_quint, run_time=6),
        #           ax.y_axis.animate(run_time=2).shift(DOWN*2.8), down_y_ax.animate(run_time=2).shift(UP*2.8),
        #           Transform(ax.x_axis, ax2.x_axis, run_time=2),
        #           self.camera.frame.animate(rate_func=rate_functions.ease_out_back, run_time=1.2
        #                                         ).scale(0.9).move_to(ax.c2p(self.camera.frame.get_x(), 0)).shift(RIGHT*2.5), lag_ratio=0))
        self.play(AnimationGroup(Create(in_geodesic_vg, lag_ratio=0, run_time=6),
                  ReplacementTransform(ax, ax2, run_time=2),
                  self.camera.frame.animate(rate_func=rate_functions.ease_out_back, run_time=1.2
                                                ).scale(0.85).move_to(ax.c2p(self.camera.frame.get_x(), 0)).shift(RIGHT*2.5), lag_ratio=0))
        
        self.play(Create(out_geodesic_vg, lag_ratio=0),
                  Create(horizon_in_geodesic_vg, lag_ratio=0),
                  Create(horizon_out_geodesic_vg, lag_ratio=0), run_time=6)
        # Change the rate functions to look smooth
        # Get the camera in the middle, get the y axis shorter, make it fit as densely on the screen as possible.
        
        self.wait(5)


# Complete
class RelativeTime(MovingCameraScene):

    # Chapters
    # 1 - A B C synchronization experiment
    # 2 - Experiment with their tilted worldlines. Light rays are always 45 degrees.
    # 3 - C has to emit their beam from a different point on the diagram.
    # 4 - Drawing an axis to that point, on the train that is t'=0
    # 5 - 


    def construct(self):

        # Inits
        self.camera.background_color=BGtry

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        self.play(Create(lightray), run_time=1.2)
        self.wait(5)

        v = ValueTracker(0.00)
        self.add(v)
        
        tpax0 = Arrow(og,ax.c2p(0,6.2))
        xpax0 = Arrow(og,ax.c2p(6.2, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v.get_value()*L0, np.sqrt(L0**2 + (v.get_value()*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v.get_value()*L0)**2), v.get_value()*L0), buff=0).set_color(pcolor1))
        
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(2)
        # Show the t=1 constant line
        linet1 = Line(ax.c2p(0, 1), ax.c2p(7, 1),stroke_width=3).set_color(propercolor)
        t1label = MathTex("t = 1").set_color(propercolor).move_to(linet1.get_end()).shift(RIGHT)
        self.play(Create(linet1))
        self.play(Write(t1label))
        self.wait()

        t1dots = VGroup()
        for i in range(1,7):
            t1doti = Dot(ax.c2p(i,1)).set_color(Salmon).set_z_index(1)
            t1dots.add(t1doti)
            self.wait(0.05)
            self.play(Create(t1doti), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(*[t1dots, t1label, linet1]))
        self.wait()

        
        # Add the lorentz axes, show oblique grid (fade out normal grid), show the t'=1 constant line
        self.play(Create(tpax), Create(xpax), rate_func=rate_functions.ease_out_cubic)
        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))
        self.play(Write(xplabel), Write(tplabel))
        self.wait()
        self.play(v.animate.set_value(0.3))

        # The lorentz grid:
        xp_direction = np.array([1,v.get_value(),0])
        tp_direction = np.array([v.get_value(),1,0])

        
        manual_gridspx = VGroup()
        manual_gridspy = VGroup()
        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl
        for i in range(1,7):
        
            xpline = Line(start=og + i*tphat,
                         end=og + i*tphat + 6.2*xphat, buff=0, 
                         stroke_color=pcolor1, stroke_opacity=0.5,stroke_width=2)


            tpline = Line(start=og + i*xphat,
                         end=og + i*xphat + 6.2*tphat, buff=0,
                         stroke_color=pcolor1, stroke_opacity=0.5,stroke_width=2)

            manual_gridspx.add(xpline)
            manual_gridspy.add(tpline)

         
        self.wait()
        self.play(Create(manual_gridspx), Create(manual_gridspy), self.camera.frame.animate.shift(RIGHT*0.8+UP).scale(1.1))
        linetp1 = Line(og+tphat, og+tphat+6.2*xphat).set_color(SteelBlue)
        tp1label = MathTex("t' = 1").set_color(SteelBlue).move_to(linetp1.get_end()).shift(RIGHT)
        self.play(Create(linetp1))
        self.play(Write(tp1label))

        tp1dots = VGroup()
        for i in range(1,7):
            tp1doti = Dot(og+tphat+i*xphat).set_color(FakeRaspberry).set_z_index(1)
            tp1dots.add(tp1doti)
            self.wait(0.05)
            self.play(Create(tp1doti), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(*[tp1dots, tp1label, linetp1]))
        self.wait()

        
        self.wait(5)


# Complete
class Simultaneity(MovingCameraScene):
    def construct(self):
        # Inits
        self.camera.background_color=BGtry

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        # self.play(Create(lightray), run_time=1.2)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(5)

        gndscolor = VibrantPink2
        adot = Dot().set_color(gndscolor).move_to(ax.c2p(0,0)).set_z_index(1)
        bdot = Dot().set_color(gndscolor).move_to(ax.c2p(3,0)).set_z_index(1)
        cdot = Dot().set_color(gndscolor).move_to(ax.c2p(6,0)).set_z_index(1)

        aline = Line(adot.get_center(), ax.c2p(0,6), stroke_width=5).set_color(gndscolor)
        bline = Line(bdot.get_center(), ax.c2p(3,6), stroke_width=5).set_color(gndscolor)
        cline = Line(cdot.get_center(), ax.c2p(6,6), stroke_width=5).set_color(gndscolor)

        alabel = Text("A").move_to(aline.get_end()).shift(UP*0.4+LEFT*0.3).set_color(gndscolor).scale(0.9).set_opacity(0.9)
        blabel = Text("B").move_to(bline.get_end()).shift(UP*0.4).set_color(gndscolor).scale(0.9).set_opacity(0.9)
        clabel = Text("C").move_to(cline.get_end()).shift(UP*0.4).set_color(gndscolor).scale(0.9).set_opacity(0.9)


        abray = DashedLine(og, bline.get_center()).set_color(lightcolor)
        cbray = DashedLine(cdot.get_center(), bline.get_center()).set_color(lightcolor)

        self.play(Create(adot), Create(bdot), Create(cdot), lag_ratio=0.1)
        self.wait()
        self.play(Create(aline), Create(bline), Create(cline), lag_ratio=0.1)
        self.wait()
        self.play(Write(alabel), Write(blabel), Write(clabel))
        self.wait(3)
        self.play(Create(abray), run_time=3, rate_func=linear)
        self.wait(3)
        self.play(Create(cbray), run_time=3, rate_func=linear)
        self.wait(5)
        self.play(FadeOut(*[alabel, blabel, clabel]))

        
        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        v = 0.3
        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl


        apline = Line(adot.get_center(), adot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)
        bpline = Line(bdot.get_center(), bdot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)
        cpline = Line(cdot.get_center(), cdot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)

        aplabel = Text("A").move_to(apline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)
        bplabel = Text("B").move_to(bpline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)
        cplabel = Text("C").move_to(cpline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)

        self.play(FadeOut(*[aline, bline, cline, abray, cbray]))
        self.play(adot.animate.set_color(pcolor1), bdot.animate.set_color(pcolor1), cdot.animate.set_color(pcolor1))
        self.play(Create(apline), Create(bpline), Create(cpline), rate_func=linear, run_time=3)
        self.play(Write(aplabel), Write(bplabel), Write(cplabel))

        # Demonstrate the classical intuition
        cabemit0 = Line(og, ax.c2p(1.3*6, 6))
        cabcatch0 = gli(cabemit0, bpline)
        cabray = DashedLine(og, cabcatch0).set_color(lightcolor)
        ccbray = DashedLine(cdot.get_center(), cabcatch0).set_color(lightcolor)
        self.wait(2)
        self.play(Create(cabray), Create(ccbray), run_time=2, rate_func=linear)
        self.wait(3)
        self.play(FadeOut(cabray), FadeOut(ccbray))


        # Back to relativity

        bpcatch = gli(lightray, bpline)
        cbemit = gli(cpline, xpax)

        abpray = DashedLine(og, bpcatch).set_color(lightcolor)
        cbfail = gli(Line(cdot.get_center(), bline.get_center()), bpline)
        cbpfailray = DashedLine(cdot.get_center(), cbfail).set_color(lightcolor)
        cbpray = DashedLine(cbemit, bpcatch).set_color(lightcolor)


        self.play(AnimationGroup(Create(cbpfailray, run_time=1, rate_func=linear), 
                                 Create(abpray, run_time=2.7, rate_func=linear), lag_ratio=0))
        self.wait(2.3)
        self.wait(2)
        self.play(FadeOut(cbpfailray), FadeOut(abpray))
        self.wait(5)

        simrays = AnimationGroup(Create(abpray, rate_func=linear, run_time=2), 
                                 Succession(Wait(1.41), Create(cbpray, rate_func=linear, run_time=0.59)))
        self.play(simrays, lag_ratio=0)

        cpsimdot = Dot(cbemit).set_color(FakeRaspberry).set_z_index(1).scale(1.2)
        self.play(Create(cpsimdot), adot.animate.set_color(FakeRaspberry).scale(1.2))
        self.wait()
        self.play(Indicate(cpsimdot), Indicate(adot))
        self.wait(2)

        
        self.play(Create(xpax), run_time=2)
        self.wait(5)


        self.play(FadeOut(*[xpax, cpsimdot, adot]))
        self.play(FadeOut(*[apline, bpline, cpline, aplabel, bplabel, cplabel, abpray, cbpray]))
        cbrayL0 = cbray.copy().scale(1.5).set_opacity(0)
        cbrayL1 = cbpray.copy().scale(1.5).set_opacity(0)

        clinedud = cline.copy().scale(1.5).set_opacity(0)
        cplinedud = cpline.copy().scale(1.5).set_opacity(0)
        # self.play(Create(cbrayL0), Create(cbrayL1))


        catchdot = always_redraw(lambda: Dot(gli(cbrayL0, bline)).set_color(FakeRaspberry).set_z_index(1).scale(1.2))
        cemit = always_redraw(lambda: Dot(gli(cbrayL0, clinedud)).set_color(FakeRaspberry).set_z_index(1).scale(1.2))


        abrays = always_redraw(lambda: DashedLine(og, catchdot.get_center()).set_color(lightcolor))
        cbrays = always_redraw(lambda: DashedLine(cemit.get_center(), catchdot.get_center()).set_color(lightcolor))


        self.play(FadeIn(*[adot, aline, bline, cline, abrays, cbrays, alabel, blabel, clabel, catchdot, cemit]))
        self.wait(2)
        self.play(Transform(aline, apline), Transform(bline, bpline), Transform(cline, cpline), Transform(alabel, aplabel),
                  Transform(cbrayL0, cbrayL1), Transform(clinedud, cplinedud),
                Transform(blabel, bplabel), Transform(clabel, cplabel), run_time=3)

        self.wait(3)


# Complete
class LorentzAxes(MovingCameraScene):
    def construct(self):

        # PICKING UP WHERE WE LEFT OFF LAST SCENE:
        self.camera.background_color=BGtry
        inftext = Text("LORENTZ AXES, CUT PART WITH THIS TEXT")
        self.play(Write(inftext))

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        # self.play(Create(lightray), run_time=1.2)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(5)

        gndscolor = VibrantPink2
        adot = Dot().set_color(gndscolor).move_to(ax.c2p(0,0)).set_z_index(1)
        bdot = Dot().set_color(gndscolor).move_to(ax.c2p(3,0)).set_z_index(1)
        cdot = Dot().set_color(gndscolor).move_to(ax.c2p(6,0)).set_z_index(1)

        aline = Line(adot.get_center(), ax.c2p(0,6), stroke_width=5).set_color(gndscolor)
        bline = Line(bdot.get_center(), ax.c2p(3,6), stroke_width=5).set_color(gndscolor)
        cline = Line(cdot.get_center(), ax.c2p(6,6), stroke_width=5).set_color(gndscolor)

        alabel = Text("A").move_to(aline.get_end()).shift(UP*0.4+LEFT*0.3).set_color(gndscolor).scale(0.9).set_opacity(0.9)
        blabel = Text("B").move_to(bline.get_end()).shift(UP*0.4).set_color(gndscolor).scale(0.9).set_opacity(0.9)
        clabel = Text("C").move_to(cline.get_end()).shift(UP*0.4).set_color(gndscolor).scale(0.9).set_opacity(0.9)


        abray = DashedLine(og, bline.get_center()).set_color(lightcolor)
        cbray = DashedLine(cdot.get_center(), bline.get_center()).set_color(lightcolor)

        
        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        v = 0.3
        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl


        apline = Line(adot.get_center(), adot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)
        bpline = Line(bdot.get_center(), bdot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)
        cpline = Line(cdot.get_center(), cdot.get_center() + tphat*6, stroke_width=5).set_color(pcolor1)

        alabel = Text("A").move_to(apline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)
        blabel = Text("B").move_to(bpline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)
        clabel = Text("C").move_to(cpline.get_end()).shift(UP*0.4).set_color(SteelBlue).scale(0.9)

        self.play(adot.animate.set_color(pcolor1), bdot.animate.set_color(pcolor1), cdot.animate.set_color(pcolor1))
        self.play(Create(apline), Create(bpline), Create(cpline), rate_func=linear, run_time=3)
        self.play(Write(alabel), Write(blabel), Write(clabel))

        bpcatch = gli(lightray, bpline)
        cbemit = gli(cpline, xpax)

        abpray = DashedLine(og, bpcatch).set_color(lightcolor)
        cbpray = DashedLine(cbemit, bpcatch).set_color(lightcolor)

        self.play(Create(abpray)) 

       
        self.play(Create(cbpray), run_time=2, rate_func=linear)

        cpsimdot = Dot(cbemit).set_color(FakeRaspberry).set_z_index(1).scale(1.2)
        self.play(Create(cpsimdot), adot.animate.set_color(FakeRaspberry).scale(1.2))

        self.play(FadeOut(inftext))
        self.wait(5)

        # NOW THE SAME AS LAST SCENE LAST FRAME
        self.wait(2)
        emit_t0A = MathTex("t' = 0").move_to(og).shift(LEFT).set_color(SteelBlue)
        emit_t0C = MathTex("t' = 0").move_to(cbemit).shift(RIGHT+DOWN*0.3).set_color(SteelBlue)
        xpaxt0label = MathTex("t'=0").move_to(xpax.get_end()).shift(RIGHT*0.8+UP*0.2).set_color(SteelBlue)
        tpaxx0label = MathTex("x'=0").move_to(alabel.get_center()).set_color(SteelBlue)

        tplabel = MathTex("t'").next_to(tpax.get_end(), UP*0.8+RIGHT*0.2).set_color(pcolor2)
        xplabel = MathTex("x'").next_to(xpax.get_end(), RIGHT*0.8+UP*0.2).set_color(pcolor2)

        self.play(Write(emit_t0A), Write(emit_t0C))
        self.wait(3)
        self.play(FadeOut(*[emit_t0A,emit_t0C]), Create(xpax), Write(xpaxt0label))
                  
        self.wait(3)
        self.play(ReplacementTransform(alabel, tpaxx0label), self.camera.frame.animate.shift(UP*0.3).scale(1.03), run_time=2)
        self.wait(2)


        self.play(FadeOut(*[cbpray, cpsimdot, alabel, blabel, clabel, bpline, cpline, bdot, cdot, adot]),
                          ReplacementTransform(abpray, lightray), ReplacementTransform(apline, tpax),
                          tpaxx0label.animate.move_to(tplabel.get_center()))
        self.wait(2)
        self.play(ReplacementTransform(xpaxt0label, xplabel), ReplacementTransform(tpaxx0label, tplabel))
        self.wait(5)

        
        # Finally show equations
        LorentzTransform1 = MathTex(r"x' = \gamma (x-vt)").move_to(lightray.get_end()).shift(RIGHT*3.5+DOWN).scale(1.3)
        LorentzTransform2 = MathTex(r"t' = \gamma \left(t - \frac{v}{c^2}x\right)").move_to(LorentzTransform1).shift(DOWN*1.5).set_color(highlight).scale(1.3)
        LorentzTransform3 = MathTex(r"x = \gamma (x'+vt')").move_to(LorentzTransform2).shift(DOWN*1.5).set_color(highlight).scale(1.3)
        LorentzTransform4 = MathTex(r"t = \gamma \left(t' + \frac{v}{c^2}x'\right)").move_to(LorentzTransform3).shift(DOWN*1.5).set_color(highlight).scale(1.3)

        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{xcolor}")

        MathTex.set_default(tex_template=template)
        basetries = "#6B7887"
        LorentzTransform1 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{x'} = \gamma ("
            r"\textcolor[HTML]{E8D0B7}{x}-v\textcolor[HTML]{E8D0B7}{t}"
            r")}"
        ).move_to(lightray.get_end()).shift(RIGHT*4.5+DOWN*0.5).scale(1.3)

        LorentzTransform2 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{t'} = \gamma \left("
            r"\textcolor[HTML]{E8D0B7}{t} - \frac{v}{c^2}\textcolor[HTML]{E8D0B7}{x}"
            r"\right)}"
        ).move_to(LorentzTransform1).shift(DOWN*2).scale(1.3)

        LorentzTransform3 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = \gamma ("
            r"\textcolor[HTML]{74C0F3}{x'}+v\textcolor[HTML]{74C0F3}{t'}"
            r")}"
        ).move_to(LorentzTransform2).shift(DOWN*2).scale(1.3)

        LorentzTransform4 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{t} = \gamma \left("
            r"\textcolor[HTML]{74C0F3}{t'} + \frac{v}{c^2}\textcolor[HTML]{74C0F3}{x'}"
            r"\right)}"
        ).move_to(LorentzTransform3).shift(DOWN*2).scale(1.3)


        LorentzTransforms = [LorentzTransform1, LorentzTransform2, LorentzTransform3, LorentzTransform4]
        self.play(self.camera.frame.animate.shift(RIGHT*3))
        self.play(Write(LorentzTransform1), Write(LorentzTransform2) ,Write(LorentzTransform3), Write(LorentzTransform4), lag_ratio=0.2)
        self.wait(5)
        self.play(FadeOut(*LorentzTransforms))
        self.play(self.camera.frame.animate.move_to(xpax.get_center()).scale(0.6), run_time=5)
        self.wait(5)


# Complete
class RearClockAhead(MovingCameraScene):
    def construct(self):

        self.camera.background_color = BGtry

        
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

        grid = homemade_grid(ax, xrange=[0,axrange], yrange=[0,axrange], colorchoice=propercolor)

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
        xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT*0.8+UP*0.2).set_color(pcolor2)

        tp = Arrow(start=OG, end=OG + 6.5*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        tplabel = MathTex("t'").next_to(tp.get_end(), UP*0.8+RIGHT*0.2).set_color(pcolor2)
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

        xplabelt0 = MathTex("t'=0").next_to(xp.get_end(), RIGHT*0.8+UP*0.2).set_color(pcolor2).scale(0.8)
        self.play(Transform(xplabel, xplabelt0))

        self.play(FadeOut(manual_grids0x),FadeOut(manual_grids0y),FadeOut(grid),
                    Transform(xct,xct0.set_opacity(0.4)),
                    self.camera.frame.animate.shift(DOWN*0.1, LEFT*0.5), run_time=2)
        

        self.wait(2)

        
        clock1p = makeclock(0, 0.12).move_to(OG).set_z_index(1)
        clock2p = makeclock(0, 0.12).move_to(OG+ xphat*2.5).set_z_index(1)
        clock3p = makeclock(0, 0.12).move_to(OG+ xphat*5).set_z_index(1)

        tp0labels = VGroup(
            MathTex("t'=0").move_to(clock1p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.8),
            MathTex("t'=0").move_to(clock2p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.8),
            MathTex("t'=0").move_to(clock3p.get_center()).shift(DOWN*0.5).set_color(pcolor2).scale(0.8)
        )

        self.play(FadeIn(*[clock1p, clock2p, clock3p]), run_time=2)
        self.wait()
        self.play(Write(tp0labels), run_time=2)
        self.wait(2)
        self.play(AnimationGroup(self.camera.frame.animate(run_time=3).scale(0.70).shift(DOWN*1.65),
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


        clock3sim = Line([OG[0], clock3p.get_y(),0], [xp.get_end()[0]-0.5, clock3p.get_y(),0], buff=0).set_color(propercolor)

        clock1delt = Arrow(OG, [OG[0], clock3p.get_y(),0], buff=0).set_color(gndcolor1)
        clock2delt = Arrow(clock2p.get_center(), [clock2p.get_x(), clock3p.get_y(),0], buff=0).set_color(gndcolor1)

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


        self.play(self.camera.frame.animate(run_time=3).scale(1.25).shift(LEFT+DOWN*2),
                  Create(negax), Create(negxp), Create(negtp), Write(negxplabel), Write(negtplabel), run_time=3)
        
        clock2sprj = DashedLine(clock2s.get_center(), gli(Line(clock2s.get_center(), clock2s.get_center()-xphat*20), negtp)).set_color(pcolor1)
        clock3sprj = DashedLine(clock3s.get_center(), gli(Line(clock3s.get_center(), clock3s.get_center()-xphat*20), negtp)).set_color(pcolor1)

        clock2sp = makeclock(11, 0.12).move_to(clock2sprj.get_end()).set_z_index(1)
        clock3sp = makeclock(10, 0.12).move_to(clock3sprj.get_end()).set_z_index(1)

        self.play(Create(clock2sprj), Create(clock3sprj), run_time=3)
        self.wait(2)
        self.play(FadeIn(*[clock2sp, clock3sp]),run_time=2)
        self.wait(3)
        self.play(FadeOut(*[clock2sp, clock3sp, clock2sprj, clock3sprj]), run_time=2)
        self.wait(2)

        clock3s_sim = Line(gli(Line(clock3s.get_center(), clock3s.get_center()-xphat*20), negtp), clock3s.get_center()).set_color(pcolor1)
        self.play(Create(clock3s_sim), run_time=2)

        clock2sdeltp = Arrow(clock2s.get_center(), gli(Line(clock2s.get_center(), clock2s.get_center()-tphat*10), clock3s_sim), buff=0).set_color(pcolor2)
        clock1sdeltp = Arrow(clock1s.get_center(), clock3s_sim.get_start(), buff=0).set_color(pcolor2)

        self.play(Create(clock2sdeltp), Create(clock1sdeltp), run_time=3)

        clock1sf = makeclock(10, 0.12).move_to(clock3s_sim.get_start()).set_z_index(1)
        clock2sf = makeclock(11, 0.12).move_to(gli(Line(clock2s.get_center(), clock2s.get_center()-tphat*10), clock3s_sim)).set_z_index(1)

        self.play(Transform(clock1s, clock1sf), Transform(clock2s, clock2sf),
                  FadeOut(*[clock1sdeltp, clock2sdeltp]), run_time=2)

        self.wait(5)
        self.play(Indicate(clock3s))
        self.wait(2)
        self.play(FadeOut(*[clock1s, clock2s, clock3s, negax, negtp, negxp, negtplabel, negxplabel, clock3s_sim]), run_time=2)
        self.play(self.camera.frame.animate(run_time=3).scale(1.1).shift(UP*0.7+RIGHT*2))


        # theLT = MathTex(r"t' = \gamma\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*1.5+LEFT).scale(1.15)

        # xpt = Dot([clock3s.get_x(), OG[1],0]).set_color(pcolor1)
        # xppt = Dot(gli(Line(xpt.get_center(), xpt.get_center()+that*10), xp)).set_color(pcolor1)
        # tpt = Dot([OG[0], xppt.get_y(), 0]).set_color(pcolor1)

        # xpt_xppt = DashedLine(xpt.get_top(), xppt.get_bottom(), buff=0).set_color(pcolor1)
        # xppt_tpt = DashedLine(xppt.get_left(), tpt.get_right(), buff=0).set_color(pcolor1)

        # xptcoords = MathTex("(x,t)", "= (L, 0)").move_to(xpt.get_center()).shift(DOWN*0.55+RIGHT*0.6).set_color(gndhighlight)
        # xptcoords1 = MathTex("x = L").move_to(xpt.get_center()).shift(DOWN*0.55+RIGHT*0.6).set_color(gndhighlight)
        # xpptcoords = MathTex("t'=0").move_to(xppt.get_center()).shift(DOWN*0.4+RIGHT*0.7).set_color(phighlight)

        # self.play(Create(xpt), Create(xppt), Create(tpt), run_time=2)
        # self.play(Create(xpt_xppt), Create(xppt_tpt), run_time=2)
        # self.wait(2)
        # self.play(Write(theLT), run_time=3)
        # self.wait(2)
        # self.play(Write(xptcoords), run_time=2)
        # self.wait()
        # self.play(Transform(xptcoords, xptcoords1),run_time=1.5)
        # self.wait(2)
        # self.play(Write(xpptcoords), run_time=1.5)
        # self.wait(1)
        # self.play(AnimationGroup(Indicate(xpt), Indicate(tpt)))
        # self.wait()
        # self.play(Indicate(xppt))

        # theLT0 = MathTex("0", r"= \gamma", r"\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*3+LEFT).scale(1.15)
        # theLT0[0].set_color(phighlight)
        # zerobrace = Brace(theLT0[2]).set_color(gndhighlight)
        # iszero = MathTex("0").set_color(gndhighlight).move_to(zerobrace.get_center()).shift(DOWN*0.4)

        # theLT1 = MathTex("t", "-",  r"\frac{v}{c^2}L", "= 0").set_color(propercolor).move_to(ax.x_axis.get_center()).shift(DOWN*4.5+LEFT).scale(1.15)
        # theLT1[0].set_color(gndhighlight)
        # theLT1[2].set_color(gndhighlight).set_opacity(0.2)


        # theLT0ghost = theLT0.copy().set_opacity(0.2)

        # theLTresult = MathTex("t", "=",  r"\frac{Lv}{c^2}").set_color(propercolor).move_to(ax.x_axis.get_center()).move_to(theLT1.get_center()).scale(1.5)

        # self.play(Write(theLT0ghost), run_time=2)
        # self.play(ReplacementTransform(xpptcoords, theLT0[0]), run_time=2)
        # self.wait()
        # self.play(ReplacementTransform(theLT0ghost, theLT0))
        # self.wait()
        # self.play(FadeIn(zerobrace), Write(iszero), run_time=2)
        # self.wait(2)
        # self.play(FadeOut(*[zerobrace, iszero]))
        # self.play(Write(theLT1))
        # self.wait(2)
        # self.play(xptcoords.animate(run_time=3).move_to(theLT1[2].get_center()).set_opacity(0),
        #           theLT1[2].animate(run_time=1).set_opacity(1))
        
        # self.wait(2)
        # self.play(FadeOut(*[theLT, theLT0]),run_time=2)
        # self.play(ReplacementTransform(theLT1, theLTresult),run_time=3)
        # self.play(theLTresult.animate(run_time=2.5).move_to(theLT.get_center()))
        # self.wait()
        # boxit = SurroundingRectangle(theLTresult).scale(1.1).set_color(propercolor)
        # self.play(self.camera.frame.animate(run_time=6).scale(1.5).move_to(theLTresult))


# Complete
class LorentzTransform(MovingCameraScene):
    def construct(self):
        # Inits
        self.camera.background_color=BGtry
        self.camera.frame.shift(RIGHT*4)
        self.camera.frame.shift(UP*4)
        

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(7,7)).set_color(lightcolor)

        
        self.play(Create(ax.x_axis))
        self.play(Create(ax.y_axis))
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Create(xlabel))
        self.play(Create(tlabel))

        hypx0 = 2
        hypxf = 7
        hcenter=0
        def hyperbola(x, x0=hypx0, center=hcenter):
            return np.sqrt((x)**2 - (x0)**2)
        
        def thyperbola(x, x0=hypx0, center=hcenter):
            return np.sqrt((x)**2 + x0**2)
        

        def nhyperbola(x, x0=hypx0, center=hcenter):
            return -np.sqrt((x-center)**2 - (x0)**2)
        

        def hyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=hcenter):
            wlpiece = ax.plot(lambda x: hyperbola(x, x0=x0), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=2.6).set_color(phighlight2)
            return wlpiece
        

        def thyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=hcenter):
            wlpiece = ax.plot(lambda x: thyperbola(x, x0=x0), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=2.6).set_color(phighlight2)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01], stroke_width=8).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece

        # CH1 - Transform for one dot first!
        def primes(coords, v):
            x = coords[0]
            t = coords[1]

            xp = (x + v*t)/np.sqrt(1-v**2)
            tp = (t + v*x)/np.sqrt(1-v**2)

            return [xp, tp]
        
        def primeslt(coords, v):
            x = coords[0]
            t = coords[1]

            xp = (x - v*t)/np.sqrt(1-v**2)
            tp = (t - v*x)/np.sqrt(1-v**2)

            return [xp, tp]

        x0i = np.sqrt(5)
        hyp0 = ax.plot(lambda x: hyperbola(x, x0=np.sqrt(5)), x_range=[x0i+hcenter,hypxf,0.01], stroke_width=3).set_color(gndcolor2)
       
        # self.play(Create(hyp0))

        v=0.35

        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()

        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))

        xplabelghost = xplabel.copy().set_opacity(0.3)
        tplabelghost = tplabel.copy().set_opacity(0.3)

        tpaxghost = tpax.copy().set_opacity(0.3)
        xpaxghost = xpax.copy().set_opacity(0.3)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl

        d1 = Dot(ax.c2p(3, hyperbola(3, x0=np.sqrt(5)))).set_color(Vanilla).set_z_index(1)
        
        d1og = d1.copy()
        d1coords = ax.p2c(d1.get_center())
        d1primes = primes(d1coords, v)
        d1lts = primeslt(d1coords, v)
        d1p = Dot(ax.c2p(d1primes))

        d1tex = MathTex("(x, t) = (3, 2)").set_color(Vanilla).move_to(d1.get_center()).shift(RIGHT*1.5).scale(0.8)

        LorentzTransform1 = MathTex(r"x' = \gamma (x-vt)").move_to(lightray.get_center()).shift(RIGHT*4+UP).set_color(pcolor1)
        LorentzTransform2 = MathTex(r"t' = \gamma \left(t - \frac{v}{c^2}x\right)").move_to(LorentzTransform1).shift(DOWN).set_color(pcolor1)
        LorentzTransform2c1 = MathTex(r"t' = \gamma \left(t - vx\right)").move_to(LorentzTransform1).shift(DOWN*0.6).set_color(pcolor1)
        d1ptex = MathTex(f"(x', t') = ({d1lts[0]:.2f}, {d1lts[1]:.2f})").move_to(d1tex).shift(UP*0.6+RIGHT*0.6).set_color(pcolor1).scale(0.8)


        self.play(Create(d1))

        self.wait()
        self.play(Create(d1tex))
        self.wait(2)
        self.play(Write(LorentzTransform1), Write(LorentzTransform2))
        self.wait()
        self.play(Transform(LorentzTransform2, LorentzTransform2c1))
        self.wait(2)
        self.play(FadeIn(xpaxghost), FadeIn(tpaxghost), FadeIn(xplabelghost), FadeIn(tplabelghost))
        self.play(Write(d1ptex))
        self.play(FadeOut(LorentzTransform1), FadeOut(LorentzTransform2))

        self.wait(3)

        self.play(FadeOut(d1tex), FadeOut(d1ptex), FadeOut(xpaxghost), FadeOut(tpaxghost), FadeOut(xplabelghost), FadeOut(tplabelghost))


        d1hyp = hyperbolapiece(d1coords[0], d1primes[0], x0=np.sqrt(5)).set_color(Vanilla).set_opacity(0.3)
        d1transform = MoveAlongPath(d1, d1hyp)


        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()

        self.play(d1transform, Transform(xcopy, xpax), Transform(ycopy, tpax), Create(d1hyp),
                  ax.x_axis.animate.set_opacity(0.3), ax.y_axis.animate.set_opacity(0.3), 
                  xlabel.animate.set_opacity(0.3), tlabel.animate.set_opacity(0.3), run_time=4, rate_func=linear)
        
        self.play(Write(xplabel), Write(tplabel))
        
        

        d1ptex = MathTex("(x', t') = (3, 2)").set_color(pcolor1).move_to(d1.get_center()).shift(RIGHT*1.8).scale(0.8)
        self.play(d1.animate.set_color(pcolor1), Write(d1ptex))

        self.wait(2)

        

        self.play(FadeIn(d1og), FadeIn(d1tex))
        self.wait(4)

        fadeouts0 = [d1, d1og, xcopy, ycopy, d1hyp, d1tex, d1ptex, xplabel, tplabel]
        self.play(FadeOut(*fadeouts0))

        v = 0.5
        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()

        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        tpaxghost = tpax.copy().set_opacity(0.3)
        xpaxghost = xpax.copy().set_opacity(0.3)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl

        d2 = Dot(ax.c2p(np.sqrt(5), 0)).set_color(Vanilla).set_z_index(1)

        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))

        xplabelghost = xplabel.copy().set_opacity(0.3)
        tplabelghost = tplabel.copy().set_opacity(0.3)

        d2primes = primes(ax.p2c(d2.get_center()), v)
        d2hyp = hyperbolapiece(np.sqrt(5), d2primes[0]-0.092, x0=np.sqrt(5)).set_color(Vanilla).set_opacity(0.3)
        
        d2transform = MoveAlongPath(d2, d2hyp)

        self.play(ax.x_axis.animate.set_opacity(1), ax.y_axis.animate.set_opacity(1),
                  xlabel.animate.set_opacity(1), tlabel.animate.set_opacity(1), run_time=3)
        
        self.wait(2)
        self.play(Create(d2))
        self.wait(2)

        self.play(d2transform, Transform(xcopy, xpax), Transform(ycopy, tpax), Create(d2hyp),
                  ax.x_axis.animate.set_opacity(0.3), ax.y_axis.animate.set_opacity(0.3),
                  self.camera.frame.animate.scale(1.1).shift(UP*0.3),
                  xlabel.animate.set_opacity(0.3), tlabel.animate.set_opacity(0.3), run_time=4, rate_func=linear)
        self.play(Write(xplabel), Write(tplabel))
        
        self.wait(3)
        self.play(FadeOut(d2hyp), FadeOut(d2))
        self.wait(2)
        self.play(Create(hyp0))
        self.wait(2)
        self.play(Create(lightray), run_time=2)
        self.wait(4)
        newax = Axes(x_range=[-7,7,1], y_range=[-7,7,1], 
        x_length=16, y_length=16,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8

        fadeouts = [xcopy, ycopy, xplabel, tplabel]
        self.wait(5)
        self.play(FadeOut(*fadeouts), ax.x_axis.animate.set_opacity(1), ax.y_axis.animate.set_opacity(1),
                  xlabel.animate.set_opacity(1), tlabel.animate.set_opacity(1))

        # ############## RANDOTS LT PART: 
        v=0.3
        np.random.seed(17)

        dots = VGroup()
        N = 100
        for i in range(N):
            doti = np.random.uniform(0,7,2)
            dots.add(Dot(ax.c2p(doti[0], doti[1]), radius=0.06).set_z_index(1))

        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()
        

        
        hypx0_values = [1.23, np.sqrt(5), 3.23, 4.23,5.23, 6.23]
        hyperbolas = VGroup()

        # setting up the hyperbolic grid, picking 2 points on top of each hyperbola:
                    
        for x0i in hypx0_values:
            print("\n\nIteration for x0 = ", x0i)
            xs = np.random.uniform(x0i, hypxf-0.5, 2)
            print(xs)

            hypi = ax.plot(lambda x: hyperbola(x, x0=x0i), x_range=[x0i+hcenter+0.000001,hypxf,0.01], stroke_width=3).set_color(gndcolor2)
            
            tmax = hyperbola(hypxf, x0=x0i)
            # print(tmax)
            thypi = ax.plot(lambda x: thyperbola(x, x0=x0i), x_range=[0, tmax, 0.01], stroke_width=3).set_color(gndcolor2)

            xts = np.random.uniform(0, tmax, 2)
            hyperbolas.add(hypi)
            hyperbolas.add(thypi)


            for x in xs:
                
                di = Dot(ax.c2p(x, hyperbola(x, x0=x0i)), radius=0.06)
                dots.add(di)

            for xt in xts:

                dti = Dot(ax.c2p(xt, thyperbola(xt, x0=x0i)), radius=0.06)
                dots.add(dti)

        self.wait()
        self.play(Create(hyperbolas), Create(dots), run_time=6)


        # getting hyperbolas and Lorentz transforms for all the dots:
        

        animations = []
        for doti in dots:
            pt = doti.get_center()
            ptcoords = ax.p2c(pt)
            ptprimes = primes(ptcoords, v)

            if ptcoords[0]**2 < ptcoords[1]**2:
                # timelike case:
                ptx0 = np.sqrt(-ptcoords[0]**2 + ptcoords[1]**2)
                pt_hyp_piece = thyperbolapiece(ptcoords[0], ptprimes[0], x0=ptx0).set_color(Vanilla).set_opacity(0.3)

            else:
                # spacelike case:
                ptx0 = np.sqrt(ptcoords[0]**2 - ptcoords[1]**2)
                pt_hyp_piece = hyperbolapiece(ptcoords[0], ptprimes[0], x0=ptx0).set_color(Vanilla).set_opacity(0.3)

            animations.append(self.camera.frame.animate(run_time=6).shift(UP+RIGHT).scale(1.1))
            animations.append(MoveAlongPath(doti, pt_hyp_piece, run_time=8, rate_func=linear))
            animations.append(Create(pt_hyp_piece, run_time=12, rate_func=linear))
            # colormations.append(doti.animate.set_color(pcolor1))

        animations.append(Transform(xcopy, xpax, run_time=12, rate_func=linear))
        animations.append(Transform(ycopy, tpax, run_time=12, rate_func=linear))
        animations.append(ax.x_axis.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(ax.y_axis.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(xlabel.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(tlabel.animate(run_time=12, rate_func=linear).set_opacity(0.3))

            
        self.play(*animations)

        xplabel = MathTex("x'").move_to(xcopy.get_end()).shift(RIGHT*0.3).set_color(SteelBlue)
        tplabel = MathTex("t'").move_to(ycopy.get_end()).shift(UP*0.3).set_color(SteelBlue)
        self.play(Write(xplabel), Write(tplabel))
        # self.play(colormations)



        # # self.play(Create(grid1), run_time=1.2)
        # # self.play(Create(lightray), run_time=1.2)
        # xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        # tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        # self.play(Write(xlabel),Write(tlabel))
        self.wait(5)


# Complete
class RcaDerivation(MovingCameraScene):
    def construct(self):

        self.camera.background_color = BGtry

        
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

        grid = homemade_grid(ax, xrange=[0,axrange], yrange=[0,axrange], colorchoice=propercolor)

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
        xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT*0.8+UP*0.2).set_color(pcolor2)

        tp = Arrow(start=OG, end=OG + 6.5*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor1)
        tplabel = MathTex("t'").next_to(tp.get_end(), UP*0.8+RIGHT*0.2).set_color(pcolor2)

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
                    self.camera.frame.animate.scale(1.15).shift(UP*0.5+RIGHT*0.74),run_time=4.5)

        self.play(FadeIn(xplabel), FadeIn(tplabel), run_time=2)
        self.wait()
        # insert constant t lines here
        


        theLT = MathTex(r"t' = \gamma\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(xct_long.get_end()).shift(RIGHT*3.5+DOWN*2).scale(1.3)
        clock3p = makeclock(0, 0.12).move_to(OG+ xphat*5).set_z_index(1)
        clock3s = makeclock(0, 0.12).move_to([clock3p.get_x(), OG[1],0]).set_z_index(1)
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
        self.play(self.camera.frame.animate(run_time=1.5).shift(RIGHT*3))
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

        theLT0 = MathTex("0", r"= \gamma", r"\left(t - \frac{v}{c^2}x\right)").set_color(propercolor).move_to(theLT.get_center()).shift(DOWN*2).scale(1.3)
        theLT0[0].set_color(phighlight)
        zerobrace = Brace(theLT0[2]).set_color(gndhighlight)
        iszero = MathTex("0").set_color(gndhighlight).move_to(zerobrace.get_center()).shift(DOWN*0.4)

        theLT1 = MathTex("t", "-",  r"\frac{v}{c^2}L", "= 0").set_color(propercolor).move_to(theLT0.get_center()).shift(DOWN*2).scale(1.3)
        theLT1[0].set_color(gndhighlight)
        theLT1[2].set_color(gndhighlight).set_opacity(0.2)


        theLT0ghost = theLT0.copy().set_opacity(0.2)

        theLTresult = MathTex("t", "=",  r"\frac{Lv}{c^2}").set_color(propercolor).move_to(theLT1.get_center()).scale(1.5)

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
        self.wait()
        boxit = SurroundingRectangle(theLTresult).scale(1.1).set_color(propercolor)
        self.play(Create(boxit))
        ltresultandbox = VGroup(theLTresult, boxit)
        self.wait()
        self.play(ltresultandbox.animate(run_time=2.5).move_to([theLTresult.get_center()[0], 
                                                            self.camera.frame.get_center()[1],0]))
        
        self.wait(5)
        # self.play(self.camera.frame.animate(run_time=6).scale(1.5).move_to(theLTresult))


# Complete
class LengthContraction(MovingCameraScene):
    def construct(self):
        # REDRAWING THE DIAGRAM TO MOVE ON:
        self.camera.background_color=BGtry
        self.camera.frame.shift(UP*0.15)
        inftext = Text("LORENTZ CONTRACTION, CUT PART WITH THIS TEXT")
        self.play(Write(inftext))

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        # self.play(Create(lightray), run_time=1.2)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(5)

        gndscolor = VibrantPink2

        
        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        v = 0.3
        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl

        self.play(FadeOut(inftext))
        self.wait(5)
        self.play(Create(xpax), Create(tpax), run_time=2)
        self.play(Write(xplabel), Write(tplabel))

        self.wait()

        # LorentzTransform1 = MathTex(r"x' = \gamma (x-vt)").move_to(tpax.get_end()).shift(RIGHT*10+DOWN).scale(1.3)
        # LorentzTransform2 = MathTex(r"t' = \gamma \left(t - \frac{v}{c^2}x\right)").move_to(LorentzTransform1).shift(DOWN*2).scale(1.3)
        # LorentzTransform3 = MathTex(r"x = \gamma (x'+vt')").move_to(LorentzTransform2).shift(DOWN*2).scale(1.3)
        # LorentzTransform4 = MathTex(r"t = \gamma \left(t' + \frac{v}{c^2}x'\right)").move_to(LorentzTransform3).shift(DOWN*2).scale(1.3)

        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{xcolor}")

        MathTex.set_default(tex_template=template)

        basetries = "#6B7887"
        LorentzTransform1 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{x'} = \gamma ("
            r"\textcolor[HTML]{E8D0B7}{x}-v\textcolor[HTML]{E8D0B7}{t}"
            r")}"
        ).move_to(tpax.get_end()).shift(RIGHT*10+DOWN).scale(1.3)

        LorentzTransform2 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{t'} = \gamma \left("
            r"\textcolor[HTML]{E8D0B7}{t} - \frac{v}{c^2}\textcolor[HTML]{E8D0B7}{x}"
            r"\right)}"
        ).move_to(LorentzTransform1).shift(DOWN*2).scale(1.3)

        LorentzTransform3 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = \gamma ("
            r"\textcolor[HTML]{74C0F3}{x'}+v\textcolor[HTML]{74C0F3}{t'}"
            r")}"
        ).move_to(LorentzTransform2).shift(DOWN*2).scale(1.3)

        LorentzTransform4 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{t} = \gamma \left("
            r"\textcolor[HTML]{74C0F3}{t'} + \frac{v}{c^2}\textcolor[HTML]{74C0F3}{x'}"
            r"\right)}"
        ).move_to(LorentzTransform3).shift(DOWN*2).scale(1.3)

        LorentzTransforms = [LorentzTransform1, LorentzTransform2, LorentzTransform3, LorentzTransform4]

        self.play(FadeIn(*LorentzTransforms), self.camera.frame.animate.shift(RIGHT*3))
        self.wait(3)
        self.play(FadeOut(*[LorentzTransform1, LorentzTransform2]))
        self.play(LorentzTransform3.animate.shift(UP*2), LorentzTransform4.animate.shift(UP*2))

        exdot = Dot(ax.c2p(4,3)).set_color(pcolor1).set_z_index(1)
        tpline = Line(exdot.get_center(), exdot.get_center() - tphat*10).set_opacity(0)
        exxp = gli(tpline, xpax)
        exxpdot = Dot(exxp).set_color(SteelBlue)

        xpline = Line(exdot.get_center(), exdot.get_center() - xphat*10).set_opacity(0)
        extp = gli(xpline, tpax)
        extpdot = Dot(extp).set_color(SteelBlue)
        

        exprj_xp = DashedLine(exdot.get_center(), exxp).set_color(SteelBlue)
        exprj_tp = DashedLine(exdot.get_center(), extp).set_color(SteelBlue)


        self.play(Create(exdot))
        self.wait(2)


        self.play(Create(exprj_xp), Create(exprj_tp), run_time=2)
        self.play(Create(extpdot), Create(exxpdot))
        self.wait(2)



        [xp, tp] = primeslt([4,3], v)
        expcoords = MathTex(f"(x', t') = ({xp:.2f}, {tp:.2f})").move_to(exdot).shift(RIGHT+UP*0.4).set_color(pcolor1).scale(0.85)
        xpcoord = MathTex(f"x' = {xp:.2f}").move_to(exxpdot.get_center()).shift(RIGHT*0.2+DOWN*0.5).set_color(SteelBlue).scale(0.85)
        tpcoord = MathTex(f"t' = {tp:.2f}").move_to(extpdot.get_center()).shift(DOWN*0.2+RIGHT).set_color(SteelBlue).scale(0.85)
        
        self.play(Write(xpcoord), Write(tpcoord))
        self.wait(2)

        self.play(xpcoord.animate.move_to(expcoords.get_center()).set_opacity(0), 
                  tpcoord.animate.move_to(expcoords.get_center()).set_opacity(0), run_time=2)
        self.play(FadeIn(expcoords))

        vtex = MathTex("v = 0.3c").set_color(Vanilla).move_to(LorentzTransform3.get_center()).shift(UP*2.5)
        gammatex0 = MathTex(r"\gamma = \frac{1}{\sqrt{1-0.3^2}}").set_color(Vanilla).move_to(vtex.get_center()).shift(DOWN*1.3)
        gammanum = 1/np.sqrt(1-v**2)
        gammatex = MathTex(f"\gamma = {gammanum:.2f}").set_color(Vanilla).move_to(vtex.get_center()).shift(DOWN)


        self.play(Write(vtex))
        self.play(Write(gammatex0))
        self.play(Transform(gammatex0, gammatex))
        self.play(FadeOut(vtex), gammatex0.animate.move_to(vtex.get_center()))

        self.play(LorentzTransform3.animate.shift(UP))

        LTnums3 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = 1.05 ("
            r"\textcolor[HTML]{74C0F3}{3.25}+0.3c\,\textcolor[HTML]{74C0F3}{1.89}"
            r")}"
        ).move_to(LorentzTransform3).shift(DOWN*1.2)

        LTnums4 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{t} = 1.05 \left("
            r"\textcolor[HTML]{74C0F3}{1.89} + \frac{0.3c}{c^2}\,\textcolor[HTML]{74C0F3}{3.25}"
            r"\right)}"
        ).move_to(LorentzTransform4).shift(DOWN*1.5)

        xttex = MathTex("(x, t) = (4, 3)").set_color(Vanilla).scale(1.2).move_to(LTnums4).shift(DOWN*1.5)

        self.play(Write(LTnums3), Write(LTnums4))

        self.wait(1.5)
        self.play(Write(xttex))
        self.wait(2)
        self.play(FadeOut(*[gammatex0, LorentzTransform3, LorentzTransform4, LTnums3, LTnums4]), 
                  xttex.animate.scale(1/1.2*0.85).move_to(expcoords.get_center()).shift(UP*0.8),
                  self.camera.frame.animate(run_time=2).shift(LEFT*3))
        
        exprjx = DashedLine(exdot.get_center(), ax.c2p(4,0)).set_color(Vanilla)
        exprjt = DashedLine(exdot.get_center(), ax.c2p(0,3)).set_color(Vanilla)
        exxdot = Dot(ax.c2p(4,0)).set_color(Vanilla)
        extdot = Dot(ax.c2p(0,3)).set_color(Vanilla)
        self.wait()
        self.play(Create(exprjx), Create(exprjt), Create(exxdot), Create(extdot))
        

        self.wait(5)
        self.play(FadeOut(*[exdot, exprjx, exprjt, expcoords, xttex, exprj_tp, exprj_xp, extpdot, exxpdot, exxdot, extdot]))
        self.wait(5)



        # STARTING LENGTH CONTRACTION
        # self.play(Write(expcoords), run_time=2)

        lxdot = Dot(ax.c2p(5.5, 0)).set_color(gndcolor1)
        
        lpdot = Dot(gli(Line(lxdot.get_center(), lxdot.get_center()+UP*5), xpax)).set_color(pcolor1).set_z_index(1)
        ltdot = Dot(gli(Line(lpdot.get_center(), lpdot.get_center()+LEFT*10), ax.y_axis)).set_color(gndcolor1)

        lplabel = MathTex("(x', t') = (L', 0)").set_color(pcolor1).move_to(lpdot.get_center()).shift(UP*0.7+LEFT*0.3).scale(0.95)

        self.play(Create(lpdot))
        self.play(Write(lplabel))
        self.wait(2)

        lprjx = DashedLine(lpdot.get_center(), lxdot.get_center()).set_color(Vanilla)
        lprjt = DashedLine(lpdot.get_center(), ltdot.get_center()).set_color(Vanilla)

        self.play(Create(lprjx), Create(lprjt))
        self.play(Create(lxdot), Create(ltdot))
        self.wait(2)
        self.play(FadeOut(*[lprjt, ltdot]))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*3), run_time=1.5)

        LorentzTransform3.shift(UP)
        LTcontract = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = \gamma ("
            r"\textcolor[HTML]{74C0F3}{L'}+v\,\textcolor[HTML]{74C0F3}{0}"
            r")}"
        ).move_to(LorentzTransform3).shift(DOWN*1.3).scale(1.3)

        ltext = MathTex("L",  r"= \gamma", "L'").move_to(LTcontract).shift(DOWN*1.4).scale(1.3)
        ltext[0].set_color(gndcolor1)
        basec = ManimColor.from_hex(basetries)
        ltext[1].set_color(basec)
        ltext[2].set_color(pcolor1)

        t1 = MathTex(r"\gamma = \frac{1}{\sqrt{1-v^2/c^2}}").set_color(basec).move_to(ltext.get_center()).shift(DOWN*1.5+LEFT*0.5).scale(0.95)
        t2 = MathTex("v < c").move_to(t1.get_center()).shift(DOWN*1.15+LEFT*1.2).set_color(basec).scale(0.95)
        t3 = MathTex(r"\implies \gamma > 1").move_to(t2.get_center()).shift(RIGHT*2).set_color(basec).scale(0.95)
        t4 = MathTex(r"\implies ", "L", ">", "L'").set_color(basec).move_to(t3.get_center()).shift(DOWN+LEFT).scale(1.2)
        
        t4[1].set_color(gndcolor1)
        t4[3].set_color(pcolor1)

        self.play(Write(LorentzTransform3))
        self.wait(2)
        self.play(Write(LTcontract))
        self.wait(2)
        self.play(Write(ltext))
        self.wait(2)

        self.play(Write(t1))
        self.play(Write(t2), Write(t3))
        self.wait()
        self.play(Write(t4))

        self.wait(5)


# 0%
class MinkowskiMetric(MovingCameraScene):

    def construct(self):

        # REDRAWING THE DIAGRAM TO MOVE ON:
        self.camera.background_color=BGtry
        inftext = Text("MINKOWSKI METRIC, CUT PART WITH THIS TEXT")
        self.play(Write(inftext))

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        self.play(Create(grid1), run_time=1.2)
        # self.play(Create(lightray), run_time=1.2)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Write(xlabel),Write(tlabel))
        self.wait(5)

        gndscolor = VibrantPink2

        
        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()
        # t^2 - x^2 = L0^2  means if x = v, t = sqrt(L0^2 + v^2)
        # tpax = Arrow(og, ax.c2p((0.3*L0), np.sqrt(L0**2 + (0.3*L0)**2)), buff=0).set_color(LightBlue)

        v = 0.3
        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl

        

        self.play(Create(xpax), Create(tpax), run_time=2)
        self.play(Write(xplabel), Write(tplabel))

        lxdot = Dot(ax.c2p(5.5, 0)).set_color(gndcolor1)
        
        lpdot = Dot(gli(Line(lxdot.get_center(), lxdot.get_center()+UP*5), xpax)).set_color(pcolor1).set_z_index(1)
        ltdot = Dot(gli(Line(lpdot.get_center(), lpdot.get_center()+LEFT*10), ax.y_axis)).set_color(gndcolor1)

        lplabel = MathTex("(x', t') = (L', 0)").set_color(pcolor1).move_to(lpdot.get_center()).shift(UP*0.7+LEFT*0.3).scale(0.95)

        self.play(Create(lpdot))
        self.play(Write(lplabel))


        lprjx = DashedLine(lpdot.get_center(), lxdot.get_center()).set_color(Vanilla)
        lprjt = DashedLine(lpdot.get_center(), ltdot.get_center()).set_color(Vanilla)

        self.play(Create(lprjx), Create(lprjt))
        self.play(Create(lxdot), Create(ltdot))

        self.play(FadeOut(*[lprjt, ltdot]))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*3), run_time=1.5)


        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{xcolor}")

        MathTex.set_default(tex_template=template)

        basetries = "#6B7887"

        LorentzTransform1 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{x'} = \gamma ("
            r"\textcolor[HTML]{E8D0B7}{x}-v\textcolor[HTML]{E8D0B7}{t}"
            r")}"
        ).move_to(tpax.get_end()).shift(RIGHT*10+DOWN).scale(1.3)

        LorentzTransform2 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{74C0F3}{t'} = \gamma \left("
            r"\textcolor[HTML]{E8D0B7}{t} - \frac{v}{c^2}\textcolor[HTML]{E8D0B7}{x}"
            r"\right)}"
        ).move_to(LorentzTransform1).shift(DOWN*2).scale(1.3)

        LorentzTransform3 = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = \gamma ("
            r"\textcolor[HTML]{74C0F3}{x'}+v\textcolor[HTML]{74C0F3}{t'}"
            r")}"
        ).move_to(LorentzTransform2).shift(DOWN*2).scale(1.3)

        LorentzTransform3.shift(UP*4)
        LTcontract = MathTex(
            r"\textcolor[HTML]{92A3B6}{"
            r"\textcolor[HTML]{E8D0B7}{x} = \gamma ("
            r"\textcolor[HTML]{74C0F3}{L'}+v\,\textcolor[HTML]{74C0F3}{0}"
            r")}"
        ).move_to(LorentzTransform3).shift(DOWN*1.3).scale(1.3)

        ltext = MathTex("L",  r"= \gamma", "L'").move_to(LTcontract).shift(DOWN*1.4).scale(1.3)
        ltext[0].set_color(gndcolor1)
        basec = ManimColor.from_hex(basetries)
        ltext[1].set_color(basec)
        ltext[2].set_color(pcolor1)

        t1 = MathTex(r"\gamma = \frac{1}{\sqrt{1-v^2/c^2}}").set_color(basec).move_to(ltext.get_center()).shift(DOWN*1.5+LEFT*0.5).scale(0.95)
        t2 = MathTex("v < c").move_to(t1.get_center()).shift(DOWN*1.15+LEFT*1.2).set_color(basec).scale(0.95)
        t3 = MathTex(r"\implies \gamma > 1").move_to(t2.get_center()).shift(RIGHT*2).set_color(basec).scale(0.95)
        t4 = MathTex(r"\implies ", "L", ">", "L'").set_color(basec).move_to(t3.get_center()).shift(DOWN+LEFT).scale(1.2)
        t4s = MathTex(r"L", ">", "L' ", r"\,\, ???").set_color(basec).move_to(t3.get_center()).shift(DOWN+LEFT).scale(1.2)
        
        t4[1].set_color(gndcolor1)
        t4[3].set_color(pcolor1)
        t4s[0].set_color(gndcolor1)
        t4s[2].set_color(pcolor1)
        t4s[3].set_color(NeonOrange).scale(1.05)

        self.play(Write(LorentzTransform3))
        self.wait(2)
        self.play(Write(LTcontract))
        self.wait(2)
        self.play(Write(ltext))
        self.wait(2)

        self.play(Write(t1))
        self.play(Write(t2), Write(t3))
        self.wait()
        self.play(Write(t4))

        self.play(FadeOut(inftext))
        self.wait(2)

        # START OF NEW SCENE
        self.play(FadeOut(*[LorentzTransform3, t1, t2, t3, lplabel, LTcontract]))
        self.play(ltext.animate.shift(LEFT*1.5), t4.animate.move_to(ltext.get_center()).shift(DOWN*1.2+LEFT*1.2))
        lplabel = MathTex("L'").set_color(pcolor1).move_to(lpdot.get_center()).shift(UP*0.4+LEFT*0.3).scale(1.2)
        llabel = MathTex("L").set_color(gndcolor1).move_to(lxdot.get_center()).shift(UP*0.4+LEFT*0.35).scale(1.2)
        self.wait()
        self.play(FadeIn(lplabel), FadeIn(llabel))
        self.wait(2)

        prjlabel = MathTex("T").move_to(lprjx.get_center()).shift(RIGHT*0.3+UP*0.1).set_color(gndcolor1)
        pythtext = MathTex(r"L^2 + T^2", " = ", r"{L'}^2").set_color(basec).move_to(t4.get_center()).shift(DOWN*1.5).scale(1.3)
        pythtext[0].set_color(gndcolor1)
        pythtext[2].set_color(pcolor1)
        self.play(Write(prjlabel))
        self.wait(2)
        self.play(Write(pythtext))
        t4s.move_to(pythtext.get_center()).shift(DOWN*1.2)
        self.wait(2)
        self.play(Write(t4s))
        self.wait(3)
        texts1 = VGroup(t4s, t4, pythtext, ltext)
        self.play(texts1.animate.shift(UP*3))



        ict = MathTex("x^2 + ", "(it)^2", " = ", " {x'} ^2").set_color(gndcolor1).move_to(t4s.get_center()).shift(DOWN*1.5).scale(1.2)
        ict[1].set_color(NeonOrange)
        ict[2].set_color(basec)
        ict[3].set_color(pcolor1)

        ict2 = MathTex("x^2 + ", "(ict)^2", " = ", " {x'} ^2").set_color(gndcolor1).move_to(t4s.get_center()).shift(DOWN*1.5).scale(1.2)
        ict2[1].set_color(NeonOrange)
        ict2[2].set_color(basec)
        ict2[3].set_color(pcolor1)


        self.play(Write(ict))

        self.wait(3)
        self.play(Transform(ict, ict2))

        mkmetric = MathTex("x^2 - ", "(ct)^2", " = ", " {x'} ^2").set_color(gndcolor1).move_to(t4s.get_center()).shift(DOWN*1.5).scale(1.2)
        mkmetric[1].set_color(SchoolBus)
        mkmetric[2].set_color(basec)
        mkmetric[3].set_color(pcolor1)

        self.wait(5)
        self.play(Transform(ict, mkmetric))
        
        

        self.wait(5)


# Complete
class HyperbolaTransform(MovingCameraScene):

    def construct(self):
        # Inits
        self.camera.background_color=BGtry
        self.camera.frame.shift(RIGHT*4)
        self.camera.frame.shift(UP*4)
        

        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(7,7)).set_color(lightcolor)

        
        self.play(Create(ax.x_axis))
        self.play(Create(ax.y_axis))
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.play(Create(xlabel))
        self.play(Create(tlabel))

        hypx0 = 2
        hypxf = 7
        hcenter=0
        def hyperbola(x, x0=hypx0, center=hcenter):
            return np.sqrt((x)**2 - (x0)**2)
        
        def thyperbola(x, x0=hypx0, center=hcenter):
            return np.sqrt((x)**2 + x0**2)
        

        def nhyperbola(x, x0=hypx0, center=hcenter):
            return -np.sqrt((x-center)**2 - (x0)**2)
        

        def hyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=hcenter):
            wlpiece = ax.plot(lambda x: hyperbola(x, x0=x0), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=2.6).set_color(phighlight2)
            return wlpiece
        

        def thyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=hcenter):
            wlpiece = ax.plot(lambda x: thyperbola(x, x0=x0), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=2.6).set_color(phighlight2)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01], stroke_width=8).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece

        # CH1 - Transform for one dot first!
        def primes(coords, v):
            x = coords[0]
            t = coords[1]

            xp = (x + v*t)/np.sqrt(1-v**2)
            tp = (t + v*x)/np.sqrt(1-v**2)

            return [xp, tp]
        
        def primeslt(coords, v):
            x = coords[0]
            t = coords[1]

            xp = (x - v*t)/np.sqrt(1-v**2)
            tp = (t - v*x)/np.sqrt(1-v**2)

            return [xp, tp]

        x0i = np.sqrt(5)
        hyp0 = ax.plot(lambda x: hyperbola(x, x0=np.sqrt(5)), x_range=[x0i+hcenter,hypxf,0.01], stroke_width=3).set_color(gndcolor2)
       
        # self.play(Create(hyp0))

        v=0.35

        tpax0 = Arrow(og,ax.c2p(0,6.5))
        xpax0 = Arrow(og,ax.c2p(6.5, 0))
        L0 = tpax0.get_length()

        tpax = always_redraw(lambda: Arrow(og, ax.c2p(v*L0, np.sqrt(L0**2 + (v*L0)**2)), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, ax.c2p(np.sqrt(L0**2 + (v*L0)**2), v*L0), buff=0).set_color(pcolor1))

        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4 + DOWN*0.07).set_color(SteelBlue))

        xplabelghost = xplabel.copy().set_opacity(0.3)
        tplabelghost = tplabel.copy().set_opacity(0.3)

        tpaxghost = tpax.copy().set_opacity(0.3)
        xpaxghost = xpax.copy().set_opacity(0.3)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        dl = 1.4
        tphat = tp_direction*norm*dl
        xphat = xp_direction*norm*dl

        d1 = Dot(ax.c2p(3, hyperbola(3, x0=np.sqrt(5)))).set_color(Vanilla).set_z_index(1)
        d1og = d1.copy()
        d1coords = ax.p2c(d1.get_center())
        d1primes = primes(d1coords, v)
        d1lts = primeslt(d1coords, v)
        d1p = Dot(ax.c2p(d1primes))

        d1tex = MathTex("(x, t) = (3, 2)").set_color(Vanilla).move_to(d1.get_center()).shift(RIGHT*1.5).scale(0.8)

        LorentzTransform1 = MathTex(r"x' = \gamma (x-vt)").move_to(lightray.get_center()).shift(RIGHT*4+UP).set_color(pcolor1)
        LorentzTransform2 = MathTex(r"t' = \gamma \left(t - \frac{v}{c^2}x\right)").move_to(LorentzTransform1).shift(DOWN).set_color(pcolor1)
        LorentzTransform2c1 = MathTex(r"t' = \gamma \left(t - vx\right)").move_to(LorentzTransform1).shift(DOWN*0.6).set_color(pcolor1)
        d1ptex = MathTex(f"(x', t') = ({d1lts[0]:.2f}, {d1lts[1]:.2f})").move_to(d1tex).shift(UP*0.6+RIGHT*0.6).set_color(pcolor1).scale(0.8)


        # self.play(Create(d1))

        # self.wait()
        # self.play(Create(d1tex))
        # self.wait(2)
        # self.play(Write(LorentzTransform1), Write(LorentzTransform2))
        # self.wait()
        # self.play(Transform(LorentzTransform2, LorentzTransform2c1))
        # self.wait(2)
        # self.play(FadeIn(xpaxghost), FadeIn(tpaxghost), FadeIn(xplabelghost), FadeIn(tplabelghost))
        # self.play(Write(d1ptex))
        # self.play(FadeOut(LorentzTransform1), FadeOut(LorentzTransform2))

        # self.wait(3)

        # self.play(FadeOut(d1tex), FadeOut(d1ptex), FadeOut(xpaxghost), FadeOut(tpaxghost), FadeOut(xplabelghost), FadeOut(tplabelghost))


        d1hyp = hyperbolapiece(d1coords[0], d1primes[0], x0=np.sqrt(5)).set_color(Vanilla).set_opacity(0.3)
        d1transform = MoveAlongPath(d1, d1hyp)

        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()

        # self.play(d1transform, Transform(xcopy, xpax), Transform(ycopy, tpax), Create(d1hyp),
        #           ax.x_axis.animate.set_opacity(0.3), ax.y_axis.animate.set_opacity(0.3), 
        #           xlabel.animate.set_opacity(0.3), tlabel.animate.set_opacity(0.3), run_time=4, rate_func=linear)
        
        # self.play(Write(xplabel), Write(tplabel))
        
        

        d1ptex = MathTex("(x', t') = (3, 2)").set_color(pcolor1).move_to(d1.get_center()).shift(RIGHT*1.8).scale(0.8)
        # self.play(d1.animate.set_color(pcolor1), Write(d1ptex))

        # self.wait(2)

        # self.play(FadeIn(d1og), FadeIn(d1tex))
        # self.wait()
        # self.play(Create(hyp0))
        
        
        newax = Axes(x_range=[-7,7,1], y_range=[-7,7,1], 
        x_length=16, y_length=16,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8

        fadeouts = [d1, d1og, xcopy, ycopy, d1hyp, d1tex, d1ptex, xplabel, tplabel]
        self.wait(5)
        self.play(FadeOut(*fadeouts), ax.x_axis.animate.set_opacity(1), ax.y_axis.animate.set_opacity(1),
                  xlabel.animate.set_opacity(1), tlabel.animate.set_opacity(1))

        ############## RANDOTS LT PART: 
        v=0.3

        dots = VGroup()
        # N = 50
        # for i in range(N):
        #     doti = np.random.uniform(0,7,2)
        #     dots.add(Dot(ax.c2p(doti[0], doti[1]), radius=0.06).set_z_index(1))

        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()
        

        self.play(Create(lightray), run_time=2)
        hypx0_values = [1.23, np.sqrt(5), 3.23, 4.23,5.23, 6.23]
        hyperbolas = VGroup()

        # setting up the hyperbolic grid, picking 2 points on top of each hyperbola:
                    
        for x0i in hypx0_values:
            print("\n\nIteration for x0 = ", x0i)
            xs = np.random.uniform(x0i, hypxf-0.5, 1)
            print(xs)

            hypi = ax.plot(lambda x: hyperbola(x, x0=x0i), x_range=[x0i+hcenter+0.000001,hypxf,0.01], stroke_width=3).set_color(gndcolor2)
            
            tmax = hyperbola(hypxf, x0=x0i)
            # print(tmax)
            thypi = ax.plot(lambda x: thyperbola(x, x0=x0i), x_range=[0, tmax, 0.01], stroke_width=3).set_color(gndcolor2)

            xts = np.random.uniform(0, tmax, 1)
            hyperbolas.add(hypi)
            hyperbolas.add(thypi)


            for x in xs:
                
                di = Dot(ax.c2p(x, hyperbola(x, x0=x0i)), radius=0.06)
                dots.add(di)

            for xt in xts:

                dti = Dot(ax.c2p(xt, thyperbola(xt, x0=x0i)), radius=0.06)
                dots.add(dti)

        self.wait()
        self.play(Create(hyperbolas), Create(dots), self.camera.frame.animate.shift(UP*0.5+RIGHT*0.5).scale(1.1), run_time=6)


        # getting hyperbolas and Lorentz transforms for all the dots:
        pt1s = []
        pt2s = []

        animations = []
        colormations = []
        for doti in dots:
            pt = doti.get_center()
            ptcoords = ax.p2c(pt)
            ptprimes = primes(ptcoords, v)

            

            if ptcoords[0]**2 < ptcoords[1]**2:
                # timelike case:
                ptx0 = np.sqrt(-ptcoords[0]**2 + ptcoords[1]**2)
                pt_hyp_piece = thyperbolapiece(ptcoords[0], ptprimes[0], x0=ptx0).set_color(Vanilla).set_opacity(0.5)

            else:
                # spacelike case:
                ptx0 = np.sqrt(ptcoords[0]**2 - ptcoords[1]**2)
                pt_hyp_piece = hyperbolapiece(ptcoords[0], ptprimes[0], x0=ptx0).set_color(Vanilla).set_opacity(0.5)
                pt1s.append(pt_hyp_piece.get_start())
                pt2s.append(pt_hyp_piece.get_end())

            
            animations.append(MoveAlongPath(doti, pt_hyp_piece, run_time=8, rate_func=linear))
            animations.append(Create(pt_hyp_piece, run_time=12, rate_func=linear))
            # colormations.append(doti.animate.set_color(pcolor1))

        animations.append(Transform(xcopy, xpax, run_time=12, rate_func=linear))
        animations.append(Transform(ycopy, tpax, run_time=12, rate_func=linear))
        animations.append(ax.x_axis.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(ax.y_axis.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(xlabel.animate(run_time=12, rate_func=linear).set_opacity(0.3))
        animations.append(tlabel.animate(run_time=12, rate_func=linear).set_opacity(0.3))

            
        self.play(*animations)
        xplabel = always_redraw(lambda:MathTex("x'").move_to(xpax.get_end()).shift(RIGHT*0.3).set_color(SteelBlue))
        tplabel = always_redraw(lambda:MathTex("t'").move_to(tpax.get_end()).shift(UP*0.3).set_color(SteelBlue))
        self.play(Write(xplabel), Write(tplabel))
        # self.play(colormations)



        # # self.play(Create(grid1), run_time=1.2)
        # # self.play(Create(lightray), run_time=1.2)
        # xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        # tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        # self.play(Write(xlabel),Write(tlabel))
        self.wait(3)

        self.play(FadeOut(*dots))


        for i in reversed(range(len(pt1s))):
            # l1 = Line(og, ax.c2p(*pt1s[i]), buff=0).set_color(Greenough)
            # l2 = Line(og, ax.c2p(*pt2s[i]), buff=0).set_color(Greenough)

            l1 = Line(og, pt1s[i], buff=0).set_color(Greenough)
            l2 = Line(og, pt2s[i], buff=0).set_color(Greenough)

            il = len(pt1s) - i
            lilabel = MathTex(f"s_{il}").scale(1.3).set_color(Greenough
                                            ).move_to(l2.get_center() + (l2.get_center()-l1.get_center())).set_z_index(1)

            self.play(Create(l1), Create(l2), lag_ratio=1.5)

            self.wait()
            self.play(Write(lilabel))
            self.wait(3)
            self.play(FadeOut(*[l1, l2, lilabel]))
            self.wait()

            
# Complete
class InvariantDemonstration(MovingCameraScene):
    def construct(self):
        self.camera.background_color=BGtry
        
        ax = Axes(x_range=[0,7,1], y_range=[0,7,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":5}).set_color(gndcolor1)
        norm = 7/8
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0,0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0,7], [0,7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8,6.8)).set_color(lightcolor)
        

        self.camera.frame.scale(0.8)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        # self.play(Create(ax.x_axis), self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4))
        # self.play(Create(ax.y_axis), self.camera.frame.animate.shift(UP*3.8), rate_func=rate_functions.ease_out_back, run_time=1.1)

        # self.play(Create(grid1), run_time=1.2)
        # self.play(Create(lightray), run_time=1.2)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        ylabel = MathTex("y").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        # self.play(Write(xlabel),Write(ylabel))

        realworldL = Line(og, og + RIGHT*4 + UP*3).set_color(FunRed).set_z_index(1)
        realworldL1 = realworldL.copy()
        realworldL2 = realworldL.copy()

        Llabel = MathTex("5m").set_color(FunRed).move_to(realworldL.get_center()).shift(DOWN*0.5+RIGHT*0.3)
        Llabel1 = Llabel.copy()
        Llabel2 = Llabel.copy()
        
        xcoord = Arrow(og, og+RIGHT*5, buff=0, stroke_width=3).set_color(LemonOrange)
        ycoord = Arrow(og, og+UP*4, buff=0, stroke_width=3).set_color(LemonOrange)

        

        self.camera.frame.move_to([xcoord.get_center()[0], realworldL.get_center()[1],0]).shift(UP*0.4)
        self.play(Create(realworldL))
        self.wait()
        self.play(Create(Llabel))
        xcoord0 = Line(og, og+RIGHT*6).set_color(LemonOrange)
        ycoord0 = Line(og, og+UP*6).set_color(LemonOrange)

        xcoordint = gli(Line(realworldL.get_end(), realworldL.get_end()+DOWN*10), xcoord0)
        ycoordint = gli(Line(realworldL.get_end(), realworldL.get_end()+LEFT*10), ycoord0)

        xl = MathTex("4m").set_color(LemonOrange).move_to(Line(og, xcoordint).get_center()).shift(DOWN*0.3)
        yl = MathTex("3m").set_color(LemonOrange).move_to(Line(og, ycoordint).get_center()).shift(LEFT*0.5)
        eq1 = MathTex("x^2 + y^2 = ", r"{5m}^2").set_color(LemonOrange
                                                           ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).shift(DOWN*2.2).scale(1.2)
        eq1[1].set_color(FunRed)


        xcoordlabel = MathTex("x").move_to(xcoord.get_end()).shift(UP*0.5).set_color(LemonOrange)
        ycoordlabel = MathTex("y").move_to(ycoord.get_end()).shift(UP*0.1+RIGHT*0.35).set_color(LemonOrange)

        xprj = DashedLine(realworldL.get_end(), xcoordint).set_color(LemonOrange)
        yprj = DashedLine(realworldL.get_end(), ycoordint).set_color(LemonOrange)

        
        self.play(Create(xcoord), Create(ycoord))
        self.play(Create(xprj), Create(yprj))
        self.play(Create(xcoordlabel), Create(ycoordlabel))

        self.wait()
        self.play(Create(xl), Create(yl))
        self.wait()
        self.play(Write(eq1), self.camera.frame.animate.shift(DOWN).scale(1.1))

        self.wait(3)

        xpcoord = xcoord.copy().set_color(GreenoughDark)
        ypcoord = ycoord.copy().set_color(GreenoughDark)

        xppcoord = Arrow(og, og+RIGHT*6, buff=0, stroke_width=3).set_color(SteelBlue)
        yppcoord = ycoord.copy().set_color(SteelBlue)
        

        self.play(xcoord.animate.set_opacity(0.3),
                  ycoord.animate.set_opacity(0.3), 
                  xprj.animate.set_opacity(0.3),
                  yprj.animate.set_opacity(0.3),
                  xl.animate.set_opacity(0),
                  yl.animate.set_opacity(0),
                  xcoordlabel.animate.set_opacity(0.3),
                  ycoordlabel.animate.set_opacity(0.3),
                  eq1.animate.set_opacity(0))
        
        self.wait()
        
        self.play(FadeIn(xpcoord), FadeIn(ypcoord))
        self.play(xpcoord.animate.rotate(-8.13 * DEGREES, about_point=xpcoord.get_start()),
                  ypcoord.animate.rotate(-8.13 * DEGREES, about_point=ypcoord.get_start()))
        
        xpcoordlabel = MathTex("x'").move_to(xpcoord.get_end()).shift(UP*0.5).set_color(GreenoughDark)
        ypcoordlabel = MathTex("y'").move_to(ypcoord.get_end()).shift(UP*0.1+RIGHT*0.35).set_color(GreenoughDark)
        self.play(Create(xpcoordlabel), Create(ypcoordlabel))
        
        xpcoordint = gli(Line(realworldL.get_end(), realworldL.get_end()+DOWN*10
                              ).rotate(-8.13 * DEGREES, about_point=realworldL.get_end()), xpcoord)
        ypcoordint = gli(Line(realworldL.get_end(), realworldL.get_end()+LEFT*10
                              ).rotate(-8.13 * DEGREES, about_point=realworldL.get_end()), ypcoord)
        
        xpprj = DashedLine(realworldL.get_end(), xpcoordint).set_color(GreenoughDark)
        ypprj = DashedLine(realworldL.get_end(), ypcoordint).set_color(GreenoughDark)

        xpl = MathTex(r"\frac{5}{2}\sqrt{2}\, m").set_color(GreenoughDark).move_to(Line(og, xpcoordint).get_center()).shift(DOWN*0.45+LEFT*0.2).scale(0.8)
        ypl = MathTex(r"\frac{5}{2}\sqrt{2}\, m").set_color(GreenoughDark).move_to(Line(og, ypcoordint).get_center()).shift(RIGHT*0.8+DOWN*0.1).scale(0.8)
        eq2 = MathTex(r"{x'}^2 + {y'}^2", " = ", r"{5m}^2").set_color(GreenoughDark
                                            ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).scale(1.2).shift(DOWN*2.2)
        eq2[2].set_color(FunRed)

        self.play(Create(xpprj), Create(ypprj))

        self.play(Create(xpl), Create(ypl))
        self.wait()
        self.play(Write(eq2))

        self.wait(5)


        self.play(xpcoord.animate.set_opacity(0.3),
                  ypcoord.animate.set_opacity(0.3), 
                  xpprj.animate.set_opacity(0.3),
                  ypprj.animate.set_opacity(0.3),
                  xpl.animate.set_opacity(0),
                  ypl.animate.set_opacity(0),
                  xpcoordlabel.animate.set_opacity(0.3),
                  ypcoordlabel.animate.set_opacity(0.3),
                  eq2.animate.set_opacity(0))
        
        self.wait()

        self.play(FadeIn(xppcoord), FadeIn(yppcoord))
        self.play(xppcoord.animate.rotate(36.9 * DEGREES, about_point=xppcoord.get_start()),
                  yppcoord.animate.rotate(36.9 * DEGREES, about_point=yppcoord.get_start()))
        
        xppl = MathTex(r"5m").set_color(SteelBlue).move_to(realworldL.get_center()).shift(UP*0.5+LEFT*0.3)

        eq3 = MathTex(r"{x'}^2", " = ", r"{5m}^2").set_color(SteelBlue
                                            ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).scale(1.2).shift(DOWN*2.2)
        eq3[2].set_color(FunRed)
        
        xppcoordlabel = MathTex("x''").move_to(xppcoord.get_end()).shift(UP*0.35).set_color(SteelBlue)
        yppcoordlabel = MathTex("y''").move_to(yppcoord.get_end()).shift(UP*0.3+RIGHT*0.35).set_color(SteelBlue)


        self.play(Create(xppcoordlabel), Create(yppcoordlabel), Create(xppl))
        self.play(Write(eq3))
        
        c1s = [realworldL, xcoord, xprj, xcoordlabel, ycoord, yprj, ycoordlabel, xl, yl, Llabel, eq1]
        c1sgp = VGroup(*c1s)
        c2s = [realworldL1, xpcoord, xpprj, xpcoordlabel, ypcoord, ypprj, ypcoordlabel, xpl, ypl, Llabel1, eq2]
        c2sgp = VGroup(*c2s)
        c3s = [realworldL2, xppcoord, xppcoordlabel, yppcoord, yppcoordlabel, Llabel2, xppl, eq3]
        c3sgp = VGroup(*c3s)

        self.wait(5)
        self.play(self.camera.frame.animate.shift(RIGHT*5.8).scale(1.52/1.1),
                  c1sgp.animate.set_opacity(1).shift(LEFT), c2sgp.animate.shift(RIGHT*5.8).set_opacity(1),
                  c3sgp.animate.shift(RIGHT*13.5))
        self.wait()
        
        

        self.wait(5)


# EST%
class InvariantHyperbolae(MovingCameraScene):

    def construct(self):
        self.camera.background_color = BGtry
  
        campos0 = self.camera.frame.get_center()

        
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

        self.play(Create(rectwrong), Write(metricwrong))
        self.wait()
        self.play(Create(rectright), Write(metricright))
        self.wait()
        self.play(metricwrong.animate.set_color(FunRed).set_opacity(0.4),
                  metricright.animate.set_color(Greenough).set_opacity(1))
        self.wait(2)
        self.play(FadeOut(*[metricright, metricwrong]))
        self.play(FadeOut(*[rectwrong, rectright]), run_time=0.2)

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
        self.play(Transform(xpi, xp0), Transform(tpi, tp0), Transform(xct, xct0), ax.animate.set_color(FunRed),
                  ax_labels.animate.set_color(FunRed),
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

        L4xp = Dot(ax.c2p(*gl_stinterval(xp1, 5))).set_color(PlasticPink)
        L4tp = Dot(ax.c2p(*gl_sxinterval(tp1, 5))).set_color(SkyBlue)
       
        L4xpp = Dot(ax.c2p(*gl_stinterval(xp2, 5))).set_color(PlasticPink)
        L4tpp = Dot(ax.c2p(*gl_sxinterval(tp2, 5))).set_color(SkyBlue)
        
        L4xppp = Dot(ax.c2p(*gl_stinterval(xp3, 5))).set_color(PlasticPink)
        L4tppp = Dot(ax.c2p(*gl_sxinterval(tp3, 5))).set_color(SkyBlue)
        
        L4xplabel = MathTex("x'").move_to(xp1.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor1)
        L4tplabel = MathTex("t'").move_to(tp1.get_end()).shift(RIGHT*0.3).set_color(pcolor1)
        xp1.set_color(pcolor1)
        tp1.set_color(pcolor1)

        L4xpplabel = MathTex("x''").move_to(xp2.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(pcolor2)
        L4tpplabel = MathTex("t''").move_to(tp2.get_end()).shift(RIGHT*0.3).set_color(pcolor2)
        xp2.set_color(pcolor2)
        tp2.set_color(pcolor2)

        L4xppplabel = MathTex("x'''").move_to(xp3.get_end()).shift(RIGHT*0.1+UP*0.45).set_color(phighlight)
        L4tppplabel = MathTex("t'''").move_to(tp3.get_end()).shift(RIGHT*0.3).set_color(phighlight)
        xp3.set_color(phighlight)
        tp3.set_color(phighlight)

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


import math
import random
import numpy as np

class CodexBlackHole(MovingCameraScene):



    """A 2D black hole with glowing orbiting particles and mist.

    Render with:
        manim -pqh black_hole_accretion_disk.py BlackHoleAccretionDisk

    Use -pql for a faster preview or -p for your preferred quality preset.
    """

    def construct(self):
        random.seed(11)
        # self.camera.background_color = "#02030a"
        self.camera.frame.scale(0.9)

        clock = ValueTracker(0)
        disk_y_scale = 0.34

        def lens_lift_for_radius(radius):
            return 0.72 * math.exp(-0.48 * (radius - 1.45))

        def lensed_disk_point(radius, angle, lift=None, vertical_offset=0.0):
            if lift is None:
                lift = lens_lift_for_radius(radius)
            x = radius * math.cos(angle)
            base_y = disk_y_scale * radius * math.sin(angle)
            back_side = max(math.sin(angle), 0)
            smooth_back_side = back_side * back_side * (3 - 2 * back_side)
            central_focus = math.exp(-((x / 1.08) ** 2))
            vertical_wrap = lift * smooth_back_side * central_focus
            shoulder_sag = -0.06 * lift * smooth_back_side * math.cos(2 * angle)
            return np.array([x, base_y + vertical_wrap + shoulder_sag + vertical_offset, 0])

        def orbit_point(radius, angle, precession=0.0):
            a = angle + precession
            return lensed_disk_point(radius, a)

        def glow_dot(radius, color, layers=6, opacity=0.18):
            glow = VGroup()
            for i in range(layers, 0, -1):
                glow.add(
                    Dot(
                        radius=radius * (1 + i * 1.1),
                        color=color,
                        fill_opacity=opacity / (i * 0.65),
                    )
                )
            glow.add(Dot(radius=radius, color=WHITE, fill_opacity=0.95))
            return glow

        def lensed_disk_path(radius, lift=None, thickness=0.0):
            def path(u):
                return lensed_disk_point(radius, u, lift=lift, vertical_offset=thickness)

            return path

        # stars = VGroup()
        # for _ in range(130):
        #     x = random.uniform(-7.2, 7.2)
        #     y = random.uniform(-4.0, 4.0)
        #     distance_from_center = math.hypot(x, y / disk_y_scale)
        #     if distance_from_center < 2.0:
        #         continue
        #     stars.add(
        #         Dot(
        #             point=[x, y, 0],
        #             radius=random.uniform(0.006, 0.017),
        #             color=random.choice(["#61708f", "#b7c7ff", "#ffffff"]),
        #             fill_opacity=random.uniform(0.18, 0.62),
        #         )
        #     )

        stars = VGroup()
        for i in range(800):
            xs = np.random.uniform(-7.2,7.2)
            ys = np.random.uniform(-4.0,4.0)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)

        photon_ring = VGroup()
        for i, (radius, opacity, width, color) in enumerate(
            [
                (1.03, 0.95, 7.5, "#ffd477"),
                (1.13, 0.48, 12.0, "#ff8f36"),
                (1.29, 0.16, 20.0, "#ff4f24"),
                (1.52, 0.08, 28.0, "#fff1a8"),
            ]
        ):
            photon_ring.add(
                Circle(radius=radius)
                .set_stroke(color=color, width=width, opacity=opacity)
                .set_fill(opacity=0)
            )

        event_horizon_glow = VGroup()
        for i in range(10, 0, -1):
            event_horizon_glow.add(
                Circle(radius=0.88 + i * 0.055)
                .set_fill("#08090e", opacity=0.04)
                .set_stroke("#1b1028", width=7, opacity=0.035)
            )

        event_horizon = Circle(radius=0.92).set_fill(BLACK, opacity=1).set_stroke(
            "#050507", width=2, opacity=1
        )

        disk_rings = [
            (1.55, 0.72, 34, 0.18, "#fff3ac"),
            (1.82, 0.63, 46, 0.18, "#ffb340"),
            (2.16, 0.54, 38, 0.16, "#ff6425"),
            (2.55, 0.44, 30, 0.13, "#ffdf78"),
            (2.95, 0.34, 24, 0.11, "#ff9b28"),
            (3.40, 0.25, 17, 0.085, "#53ccff"),
            (3.85, 0.19, 12, 0.065, "#7a1dff"),
        ]

        rear_disk = VGroup()
        for radius, lift, width, opacity, color in disk_rings:
            rear_disk.add(
                ParametricFunction(
                    lensed_disk_path(radius, lift),
                    t_range=[0, TAU],
                ).set_stroke(
                    color=color,
                    width=width,
                    opacity=opacity,
                )
            )
        rear_disk.set_z_index(1)
        lensed_wrap_foreground = VGroup()
        front_disk = VGroup()
        for radius, lift, width, opacity, color in disk_rings:
            lensed_wrap_foreground.add(
                ParametricFunction(
                    lensed_disk_path(radius, lift),
                    t_range=[0.08 * PI, 0.92 * PI],
                ).set_stroke(
                    color=color,
                    width=width * 0.82,
                    opacity=min(opacity * 1.65, 0.32),
                )
            )
            front_disk.add(
                ParametricFunction(
                    lensed_disk_path(radius, lift),
                    t_range=[PI, TAU],
                ).set_stroke(
                    color=color,
                    width=width,
                    opacity=min(opacity * 1.45, 0.28),
                )
            )

        lensed_hot_rim = VGroup()
        for _ in range(18):
            radius = random.uniform(1.48, 2.85)
            lift = random.uniform(0.36, 0.78)
            start = random.uniform(0.16 * PI, 0.72 * PI)
            length = random.uniform(0.045 * PI, 0.13 * PI)
            color = random.choice(["#fff6c2", "#ffd06a", "#ff832e", "#ff4926"])
            speed = random.uniform(0.045, 0.12)
            phase = random.uniform(0, TAU)
            width = random.uniform(3.0, 7.5)

            def make_lensed_streak(r=radius, l=lift, a=start, span=length, c=color, s=speed, p=phase, w=width):
                now = 0.13 * PI + ((a + clock.get_value() * s + p) % (0.74 * PI))
                return ParametricFunction(
                    lensed_disk_path(r, l),
                    t_range=[now, min(now + span, 0.87 * PI)],
                ).set_stroke(c, width=w, opacity=0.52)

            lensed_hot_rim.add(always_redraw(make_lensed_streak))

        hot_streaks = VGroup()
        for _ in range(24):
            radius = random.uniform(1.75, 4.0)
            angle = random.uniform(0, TAU)
            streak_len = random.uniform(0.09, 0.24)
            color = random.choice(["#ffd36e", "#ff7c25", "#fff6b8", "#ff3d21"])
            phase = random.uniform(0, TAU)
            speed = random.uniform(0.12, 0.34)
            width = random.uniform(2.5, 7.0)

            def make_streak(r=radius, a=angle, p=phase, s=speed, sl=streak_len, c=color, w=width):
                now = a + clock.get_value() * s + p
                return ParametricFunction(
                    lensed_disk_path(r),
                    t_range=[now, now + sl],
                ).set_stroke(
                    color=c,
                    width=w,
                    opacity=0.46,
                )

            hot_streaks.add(always_redraw(make_streak))

        mist = VGroup()
        mist_palette = ["#ffb13c", "#ff5a20", "#ffe8a6", "#794dff", "#6ad8ff"]

        for _ in range(90):
            radius = random.uniform(1.45, 4.2)
            start = random.uniform(0, TAU)
            speed = random.uniform(0.08, 0.27) * random.choice([0.78, 1.0, 1.18])
            size = random.uniform(0.045, 0.16)
            color = random.choice(mist_palette)
            phase = random.uniform(0, TAU)

            def make_mist(r=radius, a=start, s=speed, sz=size, c=color, p=phase):
                t = clock.get_value()
                wobble = 0.07 * math.sin(t * 1.4 + p)
                point = orbit_point(r + wobble, a + t * s)
                fuzzy = VGroup()
                for layer in range(4, 0, -1):
                    fuzzy.add(
                        Circle(radius=sz * layer)
                        .move_to(point)
                        .set_fill(c, opacity=0.018 + 0.018 / layer)
                        .set_stroke(c, width=0, opacity=0)
                    )
                return fuzzy

            mist.add(always_redraw(make_mist))

        sparks = VGroup()
        spark_palette = ["#ffffff", "#fff0a3", "#ffae38", "#ff4b21", "#8c6bff"]
        for _ in range(52):
            radius = random.uniform(1.28, 3.95)
            start = random.uniform(0, TAU)
            speed = random.uniform(0.16, 0.52)
            size = random.uniform(0.015, 0.045)
            color = random.choice(spark_palette)
            twinkle = random.uniform(0.6, 1.5)
            phase = random.uniform(0, TAU)

            def make_spark(r=radius, a=start, s=speed, sz=size, c=color, tw=twinkle, p=phase):
                t = clock.get_value()
                point = orbit_point(r, a + t * s)
                pulse = 0.72 + 0.28 * math.sin(t * tw + p)
                particle = glow_dot(sz * pulse, c, layers=4, opacity=0.16)
                particle.move_to(point)
                return particle

            sparks.add(always_redraw(make_spark))

        lens_shadow = Circle(radius=1.0).set_fill(BLACK, opacity=1).set_stroke(BLACK, 0)
        lens_shadow.move_to(ORIGIN)

        title = (
            Text("BLACK HOLE", font_size=28, weight=BOLD)
            .set_color("#dce7ff")
            .to_corner(UL, buff=0.35)
            .set_opacity(0.72)
        )
        subtitle = (
            Text("orbiting particles and accretion mist", font_size=16)
            .set_color("#7f8aa7")
            .next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)
            .set_opacity(0.7)
        )

        # self.add(stars)
        self.add(rear_disk, mist, hot_streaks, sparks)
        self.add(event_horizon_glow, photon_ring, lens_shadow, event_horizon)
        # self.add(lensed_wrap_foreground, front_disk, lensed_hot_rim)
        # self.add(title, subtitle)

        self.play(FadeIn(rear_disk))
        self.play(FadeIn(event_horizon_glow), FadeIn(photon_ring), FadeIn(event_horizon))
        self.play(
            FadeIn(mist, lag_ratio=0.02),
            FadeIn(sparks, lag_ratio=0.01),
            # FadeIn(lensed_wrap_foreground),
            # FadeIn(front_disk),
            # FadeIn(lensed_hot_rim, lag_ratio=0.03),
            run_time=1.5,
        )

        self.play(clock.animate.set_value(50), run_time=20, rate_func=linear)
        self.wait(0.5)
        

class StarryBackground(Scene):

    def construct(self):
        
        stars = VGroup()
        for i in range(800):
            xs = np.random.uniform(-7.2,7.2)
            ys = np.random.uniform(-4.0,4.0)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)
        self.add(stars)

        self.wait(5)


# PNG Equations
class Eq1(Scene):
    def construct(self):
        
        eq1 = MathTex("v_{c_1} = c + v").set_color(lightcolor).scale(1.5)
        self.add(eq1)


class Eq2(Scene):
    def construct(self):
        
        eq2 = MathTex("v_{c_2} = c - v").set_color(lightcolor).scale(1.5)
        self.add(eq2)


class Eq3(Scene):
    def construct(self):
        
        eq3 = MathTex("v = c").set_color(lightcolor).scale(1.5)
        self.add(eq3)


class Postulate1(Scene):
    def construct(self):
        
        postulate1 = Text("Postulate 1: All laws of physics are the\n  same in all inertial reference frames.").set_color(gndcolor1).scale(1)
        subtitle1 = Text("All experiments will yield the same results.").set_color(gndcolor1).scale(0.7).move_to(postulate1.get_bottom() + DOWN * 0.5)
        self.play(Write(postulate1))
        self.wait(2)
        self.play(FadeIn(subtitle1))
        self.wait(5)


class Postulate2(Scene):
    def construct(self):
        
        postulate2 = Text("Postulate 2: The speed of light is the constant c.").set_color(gndcolor1).scale(1)
        subtitle2 = Text("It will be measured the same in all inertial reference frames!").set_color(gndcolor1).scale(0.7).move_to(postulate2.get_bottom() + DOWN * 0.5)
        self.play(Write(postulate2))
        self.wait(2)
        self.play(FadeIn(subtitle2))
        self.wait(5)