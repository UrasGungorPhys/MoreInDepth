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


config.pixel_width = 1080
config.pixel_height = 1920


# Complete
class SLorentzTransform(MovingCameraScene):
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

            animations.append(self.camera.frame.animate(run_time=6).shift(UP*1.5+RIGHT*1.5))
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
        self.wait(5)


# Complete
class SInvariantDemonstrationLT(MovingCameraScene):
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
        

        self.camera.frame.scale(0.5)
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

        

        self.camera.frame.move_to([xcoord.get_center()[0], realworldL.get_center()[1],0]).shift(UP*0.4+LEFT*0.6)
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
                                                           ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).shift(DOWN*1.2+LEFT*0.3).scale(1.2)
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
        

        # self.play(xcoord.animate.set_opacity(0.3),
        #           ycoord.animate.set_opacity(0.3), 
        #           xprj.animate.set_opacity(0.3),
        #           yprj.animate.set_opacity(0.3),
        #           xl.animate.set_opacity(0),
        #           yl.animate.set_opacity(0),
        #           xcoordlabel.animate.set_opacity(0.3),
        #           ycoordlabel.animate.set_opacity(0.3),
        #           eq1.animate.set_opacity(0))
        
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
                                            ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).scale(1.2).shift(DOWN*1.6+LEFT*0.3)
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
                                            ).move_to([self.camera.frame.get_center()[0],xcoord.get_center()[1],0]).scale(1.2).shift(DOWN*0.8+LEFT*1.3)
        eq3[2].set_color(FunRed)
        
        xppcoordlabel = MathTex("x''").move_to(xppcoord.get_end()).shift(UP*0.35).set_color(SteelBlue)
        yppcoordlabel = MathTex("y''").move_to(yppcoord.get_end()).shift(UP*0.3+RIGHT*0.35).set_color(SteelBlue)


        self.play(Create(xppcoordlabel), Create(yppcoordlabel), Create(xppl))
        self.play(Write(eq3))

        self.play(xppcoord.animate.set_opacity(0.3),
                  yppcoord.animate.set_opacity(0.3), 
                  xppl.animate.set_opacity(0),
                  xppcoordlabel.animate.set_opacity(0.3),
                  yppcoordlabel.animate.set_opacity(0.3),
                  eq3.animate.set_opacity(0))
        
        
        c1s = [realworldL, xcoord, xprj, xcoordlabel, ycoord, yprj, ycoordlabel, xl, yl, Llabel, eq1]
        c1sgp = VGroup(*c1s)
        c2s = [realworldL1, xpcoord, xpprj, xpcoordlabel, ypcoord, ypprj, ypcoordlabel, xpl, ypl, Llabel1, eq2]
        c2sgp = VGroup(*c2s)
        c3s = [realworldL2, xppcoord, xppcoordlabel, yppcoord, yppcoordlabel, Llabel2, xppl, eq3]
        c3sgp = VGroup(*c3s)

        self.wait(2)

        self.play(FadeOut(*c2sgp), FadeOut(*c3sgp))
        self.wait(2)
        self.play(FadeIn(*c2sgp), FadeIn(*c3sgp))
        self.wait(5)
        self.play(self.camera.frame.animate.scale(1.3),
                  c1sgp.animate.set_opacity(1), c2sgp.animate.shift(UP*7).set_opacity(1),
                  c3sgp.animate.set_opacity(1).shift(DOWN*7+RIGHT))
        
        self.wait()
        

        self.wait(5)


# Complete
class SHyperbolaTransform(MovingCameraScene):

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


        d1hyp = hyperbolapiece(d1coords[0], d1primes[0], x0=np.sqrt(5)).set_color(Vanilla).set_opacity(0.3)
        d1transform = MoveAlongPath(d1, d1hyp)

        xcopy = ax.x_axis.copy()
        ycopy = ax.y_axis.copy()


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
        minkmetric = MathTex(r"x^2 - {ct}^2", "= s^2").set_color(gndcolor1).move_to(ax.x_axis.get_center()).shift(DOWN*2.5).scale(2)
        minkmetric[0].set_color(gndcolor1)
        self.play(Write(minkmetric))
        self.wait(3)
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


