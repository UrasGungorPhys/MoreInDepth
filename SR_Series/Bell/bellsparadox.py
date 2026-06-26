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
LightBlue= ManimColor.from_hex("#85C7F2")
RedOrange= ManimColor.from_hex("#BA1200")
SkyBlue= ManimColor.from_hex("#01FDF6")
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

BGBlue1 = ManimColor.from_hex("#0B1A27")
BGBlue2 = ManimColor.from_hex("#091D2E")

FunRed = ManimColor.from_hex("#EF271B")
Greenough = ManimColor.from_hex("#53FF45")
PlasticPink = ManimColor.from_hex("#ED217C")
Vanilla = ManimColor.from_hex("#F5E2C8")
SchoolBus = ManimColor.from_hex("#FDE12D")
NewOrange1 = ManimColor.from_hex("#F34213")
NewOrange2 = ManimColor.from_hex("#FE5F00")
LemonOrange = ManimColor.from_hex("#F18F01")

gndcolor1 = Vanilla
gndcolor2 = SteelBlue
gndhighlight = LightBlue
gndhighlight2 = Greenough

pcolor1 = NewOrange1
pcolor2 = NewOrange2
phighlight = LemonOrange
phighlight2 = FakeRaspberry

highlight = Emerald

propercolor = Vanilla
lightcolor = SchoolBus

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



class Intro(MovingCameraScene):
    def construct(self):
        pass


class HyperbolaStuff1(MovingCameraScene):
    def construct(self):
        # Plan for the scene, subchapters.
        

        ############################################### Initializing ########################################################
        #################### Set up axes
        self.camera.background_color = BGBlue1
        # self.camera.frame.scale(0.9)
        ax = Axes(x_range=[0,10,1], y_range=[0,10,1], 
        x_length=7, y_length=7,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor).set_opacity(0.5)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor)
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

        self.play(Create(ax), Write(ax_labels), run_time=1)

        #################### Set up hyperbola, draw worldline
        hypx0 = 2
        hypxf = 8
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
        def getxprime(x, P_point=P):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            xp = Arrow(hyp_point, hyp_point+xphat*3, buff=0)

            return xp
        
        def gettprime(x, P_point=P):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            tphat = np.array([xphat[1], xphat[0], 0])
            tp = Arrow(hyp_point, hyp_point+tphat*3, buff=0)

            return tp

        worldline = ax.plot(lambda x: hyperbola(x), x_range=[hypx0+center,hypxf,0.01], stroke_width=7).set_color(gndcolor2)



class HyperbolaStuff2(MovingCameraScene):
    def construct(self):
    

    ############################################### Initializing ########################################################
        #################### Set up axes
        self.camera.background_color = BGBlue1
        ax = Axes(x_range=[-6,10,1], y_range=[0,10,1], 
        x_length=9, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor).set_opacity(0.5)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor)
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

        self.play(Create(ax), Write(ax_labels), run_time=1)

        #################### Set up hyperbola, draw worldline
        hypx0 = 3
        hypxf = 8
        center=-2
        def hyperbola(x, x0=hypx0, center=-2):
            return np.sqrt((x+center)**2 - (x0)**2)
        
        def nhyperbola(x, x0=hypx0, center=-2):
            return -np.sqrt((x+center)**2 - (x0)**2)
        

        def hyperbolapiece(x1, x2, opacity=0, x0=hypx0, center=-2):
            wlpiece = ax.plot(lambda x: np.sqrt((x+center)**2 - (x0+center)**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        P = Dot(ax.c2p(center, 0, 0))
        def getxprime(x, P_point=P):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            xp = Arrow(hyp_point, hyp_point+xphat*3, buff=0)

            return xp
        
        def gettprime(x, P_point=P):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xphat = intline.get_unit_vector()
            tphat = np.array([xphat[1], xphat[0], 0])
            tp = Arrow(hyp_point, hyp_point+tphat*3, buff=0)

            return tp




