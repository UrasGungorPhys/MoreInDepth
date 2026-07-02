from itertools import tee

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
gndhighlight = PlasticPink
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


# 97.5%
# Fix the yellowed value tracker not moving
# Then it works, just some smoothing to do left!
# Smooth out the transition from rapid fire frames to the last frame.
class Cameramen(MovingCameraScene):
    def construct(self):
        # self.camera.background_color = BGBlue1
        # Background stars:
        stars = VGroup()
        for i in range(1000):
            xs = np.random.uniform(-10,150)
            ys = np.random.uniform(-10,10)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)

        # self.play(FadeIn(stars))

        
        dot1 = ImageMobject("rocket.png").scale(0.2).shift(LEFT*5)
        dot1ghost = dot1.copy().set_opacity(0)
        startpos = dot1.get_center()


        def insertcam(t, v, vtracker, cam, vcam, enter, exit, camframev0, framedelta=30):
            
            camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*camframev0)
            # vlabelpos = always_redraw(lambda: Dot().move_to(cam.get_corner(DR)).shift(LEFT+UP).set_opacity(0))
            # if t>=enter+framedelta-2 == False:  # make it yellow instead in that range.
            # vl = always_redraw(lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v").set_color(propercolor).move_to(vlabelpos.get_center()))

            # if t==enter:   
            #     # self.add(vlabelpos)
            #     # self.add(vl)
                    
            #Fade in
            if enter<=t<=enter+int(framedelta/3):
                opacity = (t-(enter))/10  # start from 0.1, increase +0.1 each iteration up to enter+10
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_stroke(opacity=opacity).set_fill(opacity=0),
                                         vtracker.animate(run_time=frame_time, rate_func=linear).set_value(vcam/v),
                                         camframeanim)
                
            else:
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam),
                                         vtracker.animate(run_time=frame_time, rate_func=linear).set_value(vcam/v),
                                         camframeanim)

            if enter+math.floor(framedelta/2)<=t<=enter+math.ceil(framedelta*5/6):
                vcamframe = (cam.get_x() - self.camera.frame.get_x())/10 + vcam
                # camframeanim = self.camera.frame.animate(run_time=frame_time*10, rate_func=linear).move_to(cam1.get_center()).scale(0.7)
                camframeanim = self.camera.frame.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcamframe).scale(0.98)
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam), 
                                         vtracker.animate(run_time=frame_time, rate_func=linear).set_value(vcam/v), camframeanim)

            if enter+int(5*framedelta/6)< t<= exit-int(framedelta/3)+1:
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam))
                                         
                if t >= enter + framedelta - 2:
                    camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_color(LemonOrange))
                                             
                    # vl = always_redraw(lambda: MathTex("v_f = v").set_color(LemonOrange).move_to(vlabelpos.get_center()))
                if t >= enter+ framedelta + 4:
                    camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_color(Vanilla))
                                             

                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam)
                camanim = AnimationGroup(camanim, camframeanim, vtracker.animate(run_time=frame_time, rate_func=linear).set_value(vcam/v))


            if exit-int(framedelta/3)+1 < t<= exit:
                fadeout = (exit - t)/9
                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam).scale(1/0.98)
                camanim = cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_stroke(opacity=fadeout).set_fill(opacity=0)
                camanim = AnimationGroup(camanim, camframeanim, vtracker.animate(run_time=frame_time, rate_func=linear).set_value(vcam/v))

            if t>exit:
                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam)
                camanim=camframeanim
            
            self.play(AnimationGroup(mainanim, camanim))
            
            if t==exit:
                self.remove(cam)
                self.remove(vl)
                # self.remove(vlabelpos)


        a = 0.003
        N=340
        frame_time = 0.15
        enter_cam1 = 40
        exit_cam1 = 90
        enter_cam2 = 95
        exit_cam2 = 145
        enter_cam3 = 150
        exit_cam3 = 182
        enter_cam4 = 183
        exit_cam4 = 208
        enter_cam5 = 210
        exit_cam5=228
        enter_cam6 = 229
        exit_cam6 = 247
        enter_cam7 = 248
        exit_cam7 = 256
        enter_cams = 257
        resultcam = 280
        # first get x's in a preliminary loop:
        deltaxs = []
        velocities = []
        for t in range(N):
            v = t*a
            deltaxs.append(RIGHT*v)
            velocities.append(v)

        cami_added=False # for later
        for t in range(N):
            v = t*a
            # self.play(dot1.animate(run_time=0.1, rate_func=linear).shift(RIGHT*v))
            mainanim = dot1.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*v)
            dot1ghost.shift(RIGHT*v)

            if enter_cam1 <= t < enter_cam2:

                if t == enter_cam1:
                    framedelta = 30
                    vcam1 = velocities[enter_cam1+framedelta]
                    deltavs = np.sum(velocities[enter_cam1:enter_cam1+framedelta])
                    deltaLEFT = framedelta*vcam1 - deltavs
                    cam1 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam1/v)
                    vlabelpos = always_redraw(lambda: Dot(cam1.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                    lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam1+ framedelta + 4 >=t >= enter_cam1 + framedelta - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam1+ framedelta + 4 >= t >= enter_cam1 + framedelta - 2 else propercolor)
                    .move_to(vlabelpos.get_center()))

                    self.add(vlabelpos)
                    self.add(vl)
                    

                if t==enter_cam1+ framedelta + 5:
                    self.remove(vl)
                    self.add(vl)

                insertcam(t, v, vtracker, cam1, vcam1, enter_cam1, exit_cam1, 0)
                vtracker=ValueTracker(vcam1/v)
                


            elif enter_cam2 <= t < enter_cam3:

                if t == enter_cam2:
                    framedelta = 30
                    vcam2 = velocities[enter_cam2+framedelta]
                    deltavs = np.sum(velocities[enter_cam2:enter_cam2+framedelta])
                    deltaLEFT = framedelta*vcam2 - deltavs
                    cam2 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam2/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam2.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam2+ framedelta + 4 >=t >= enter_cam2 + framedelta - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam2+ framedelta + 4 >= t >= enter_cam2 + framedelta - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )
                    self.add(vlabelpos)
                    self.add(vl)
                    
                if t==enter_cam2+ framedelta + 5:
                    self.remove(vl)
                    self.add(vl)
                
                    
                
                insertcam(t, v, vtracker, cam2, vcam2, enter_cam2, exit_cam2, vcam1)
                vtracker=ValueTracker(vcam2/v)
                


            elif enter_cam3 <= t < enter_cam4:

                if t == enter_cam3:
                    framedelta3 = 24
                    vcam3 = velocities[enter_cam3+framedelta3]
                    deltavs = np.sum(velocities[enter_cam3:enter_cam3+framedelta3])
                    deltaLEFT = framedelta3*vcam3 - deltavs
                    cam3 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam3/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam3.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam3+ framedelta3 + 4 >=t >= enter_cam3 + framedelta3 - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam3+ framedelta3 + 4 >= t >= enter_cam3 + framedelta3 - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )
                    self.add(vlabelpos)
                    self.add(vl)
                    
                if t==enter_cam3+ framedelta3 + 5:
                    self.remove(vl)
                    self.add(vl)
                
                
                insertcam(t, v, vtracker, cam3, vcam3, enter_cam3, exit_cam3, vcam2, framedelta=framedelta3)
                vtracker=ValueTracker(vcam3/v)
                


            elif enter_cam4 <= t < enter_cam5:

                if t == enter_cam4:
                    framedelta4 = 15
                    vcam4 = velocities[enter_cam4+framedelta4]
                    deltavs = np.sum(velocities[enter_cam4:enter_cam4+framedelta4])
                    deltaLEFT = framedelta4*vcam4 - deltavs
                    cam4 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam4/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam4.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam4+ framedelta4 + 4 >= t >= enter_cam4 + framedelta4 - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam4+ framedelta4 + 4 >= t >= enter_cam4 + framedelta4 - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )   
                    
                    self.add(vlabelpos)
                    self.add(vl)
                    
                if t==enter_cam4+ framedelta4 + 5:
                    self.remove(vl)
                    self.add(vl)
                
                
                insertcam(t, v, vtracker, cam4, vcam4, enter_cam4, exit_cam4, vcam3, framedelta=framedelta4)
                vtracker=ValueTracker(vcam4/v)
                


            elif enter_cam5 <= t < enter_cam6:

                if t == enter_cam5:
                    framedelta5 = 9
                    vcam5 = velocities[enter_cam5+framedelta5]
                    deltavs = np.sum(velocities[enter_cam5:enter_cam5+framedelta5])
                    deltaLEFT = framedelta5*vcam5 - deltavs
                    cam5 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam5/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam5.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam5+ framedelta5 + 4 >=t >= enter_cam5 + framedelta5 - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam5+ framedelta5 + 4 >= t >= enter_cam5 + framedelta5 - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )
                    
                self.add(vlabelpos)
                self.add(vl)
                if t==enter_cam5+ framedelta5 + 5:
                    self.remove(vl)
                    self.add(vl)
                
                
                insertcam(t, v, vtracker, cam5, vcam5, enter_cam5, exit_cam5, vcam4, framedelta=framedelta5)
                vtracker=ValueTracker(vcam5/v)
                


            elif enter_cam6 <= t < enter_cam7:

                if t == enter_cam6:
                    framedelta6 = 9
                    vcam6 = velocities[enter_cam6+framedelta6]
                    deltavs = np.sum(velocities[enter_cam6:enter_cam6+framedelta6])
                    deltaLEFT = framedelta6*vcam6 - deltavs
                    cam6 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam6/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam6.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam6+ framedelta6 + 4 >=t >= enter_cam6 + framedelta6 - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam6+ framedelta6 + 4 >= t >= enter_cam6 + framedelta6 - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )   
                    
                self.add(vlabelpos)
                self.add(vl)
                if t==enter_cam6+ framedelta6 + 5:
                    self.remove(vl)
                    self.add(vl)
                
                
                insertcam(t, v, vtracker, cam6, vcam6, enter_cam6, exit_cam6, vcam5, framedelta=framedelta6)
                vtracker=ValueTracker(vcam6/v)
                

            
            elif enter_cam7 <= t < enter_cams:

                if t == enter_cam7:
                    framedelta7 = 9
                    vcam7 = velocities[enter_cam7+framedelta7]
                    deltavs = np.sum(velocities[enter_cam7:enter_cam7+framedelta7])
                    deltaLEFT = framedelta7*vcam7 - deltavs
                    cam7 = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                    vtracker = ValueTracker(vcam7/v)
                    vlabelpos = always_redraw(lambda: Dot().move_to(cam7.get_corner(DR)).shift(LEFT*1.5+UP).set_opacity(0))
                    vl = always_redraw(
                lambda: MathTex(f"v_f = {vtracker.get_value():.2f} v" if not (enter_cam7+ framedelta7 + 4 >=t >= enter_cam7 + framedelta7 - 2) else "v_f = v")
                    .set_color(LemonOrange if enter_cam7+ framedelta7 + 4 >= t >= enter_cam7 + framedelta7 - 2 else propercolor)
                    .move_to(vlabelpos.get_center())
            )   
                self.add(vlabelpos)
                self.add(vl)
                if t==enter_cam7+ framedelta7 + 5:
                    self.remove(vl)
                    self.add(vl)
                
                
                insertcam(t, v, vtracker, cam7, vcam7, enter_cam7, exit_cam7, vcam6, framedelta=framedelta7)
                vtracker=ValueTracker(vcam7/v)
                
                
            else:
                camframeanimation = self.camera.frame.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*v)

                if enter_cams <= t <= resultcam:
                    if cami_added:
                        cami_old = cami
                        cami_animation = cami_old.animate(run_time=frame_time, rate_func=linear).set_stroke(opacity=0.4).set_fill(opacity=0).set_color(Vanilla)  # previous cams get faded a bit

                        if t%3 ==0:
                            caminew = Create(cami, run_time=frame_time)
                            self.play(AnimationGroup(mainanim, cami_animation, camframeanimation))

                        else:
                            self.play(mainanim, camframeanimation)
                    
                    cami = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_color(LemonOrange)
                    if cami_added == False:
                            caminew = Create(cami, run_time=frame_time)
                            self.play(AnimationGroup(mainanim, camframeanimation))
                            cami_added=True
                            continue
                    
                    if t==resultcam:
                        finalcam = Rectangle(height=6, width=8).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_color(LemonOrange)

                
                elif t>resultcam:
                    
                    camframeanimation = self.camera.frame.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*v)
                    finalcamanimation = finalcam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*v)
                    self.play(AnimationGroup(mainanim, finalcamanimation, camframeanimation))

                else:
                    self.play(mainanim, camframeanimation)



# Fix camera angles
# Fix transitions
# Fix grid
class Hyperbolic(MovingCameraScene):
    def construct(self):
        # Plan for the scene, subchapters.
        # 1 - Hyperbolic worldline, show dx and dts to clarify.
        # 2 - Draw tangent line at a single point, that's the same as the cameraman catching it
        # 3 - Draw many of these tangent lines, that's the other cameramen catching it at different points
        # 4 - Argue that these lines are the t' axis, since the acc is at rest in their own frame
        # 5 - Draw the x' axis using t', light ray, and symmetry.
        # 6 - The x' axis is made up of all points that are "now" to the observer.
        # 7 - Show that the axes scissors in as the accelerator gets faster, by drawing it at different points on the worldline.


        ############################################### Initializing ########################################################
        #################### Set up axes
        self.camera.background_color = BGtry
        ax = Axes(x_range=[0,10,1], y_range=[0,10,1], 
        x_length=8, y_length=8,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        self.camera.frame.scale(1.22).shift(DOWN*0.1)
        og = ORIGIN
        OG = ORIGIN


        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor).set_opacity(0.5)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])

        self.play(Create(ax), Write(xlabel), Write(tlabel), run_time=1)
        grids = homemade_grid(ax, [0,10], [0,10], gndcolor1, opacitychoice=0.25)
        self.play(Create(grids))
        #################### Set up hyperbola, draw worldline
        hypx0 = 2
        hypxf = 8
        center=-2
        def hyperbola(x, x0=hypx0, center=-2):
            return np.sqrt((x-center)**2 - (x0)**2)
        

        def nhyperbola(x, x0=hypx0, center=-2):
            return -np.sqrt((x-center)**2 - (x0)**2)
        

        def hyperbolapiece(x1, x2, opacity=1, x0=hypx0, center=-2):
            wlpiece = ax.plot(lambda x: hyperbola(x), x_range=[x1, x2, 0.01],use_smoothing=False, stroke_width=5).set_color(phighlight2)
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

        worldline = ax.plot(lambda x: hyperbola(x), x_range=[hypx0+center,hypxf,0.01], stroke_width=4.5).set_color(gndcolor2)


        ############################################ Scenes ###############################################
        # 1 - Hyperbolic worldline, show dx and dts to clarify.
        # 2 - Draw tangent line at a single point, that's the same as the cameraman catching it
        # 3 - Draw many of these tangent lines, that's the other cameramen catching it at different points
        # 4 - Argue that these lines are the t' axis, since the acc is at rest in their own frame
        # 5 - Draw the x' axis using t', light ray, and symmetry.
        # 6 - The x' axis is made up of all points that are "now" to the observer.
        # 7 - Show that the axes scissors in as the accelerator gets faster, by drawing it at different points on the worldline.

        ############## Chapter 1: The hyperbolic worldline
        print(type(rate_functions))
        self.play(Create(worldline), run_time=1.2)
        x0 = hypx0+center

        # 1st piece
        wlpiece1 = hyperbolapiece(x0, x0+1)
        wlp0 = Dot(wlpiece1.get_start())
        wlp1 = Dot(wlpiece1.get_end())
        self.play(Create(wlpiece1), run_time=1)


        wlp0t = gli(ax.y_axis, Line(wlp0.get_center(), wlp0.get_center() - xhat*10))
        wlp1t = gli(ax.y_axis, Line(wlp1.get_center(), wlp1.get_center() - xhat*10))
        

        wlp0x = gli(ax.x_axis, Line(wlp0.get_center(), wlp0.get_center() - that*10))
        wlp1x = gli(ax.x_axis, Line(wlp1.get_center(), wlp1.get_center() - that*10))
        wlp1xprj = DashedLine(wlp1, wlp1x).set_color(gndhighlight)
        wlp1tprj = DashedLine(wlp1, wlp1t).set_color(gndhighlight)

        self.play(Create(wlp1tprj), Create(wlp1xprj))
        delt = Line(wlp0t, wlp1t, stroke_width=6).set_color(gndhighlight)
        deltlabel = MathTex(r"\Delta t").set_color(gndhighlight).move_to(delt.get_center()).shift(LEFT*0.5)
        delx = Line(wlp0x, wlp1x, stroke_width=6).set_color(gndhighlight)
        delxlabel = MathTex(r"\Delta x").set_color(gndhighlight).move_to(delx.get_center()).shift(DOWN*0.5)
        self.play(Create(delt), Create(delx), Write(deltlabel), Write(delxlabel), run_time=1.5)
        self.wait(2)

        fadeouts1 = [wlpiece1, wlp1tprj, wlp1xprj, delt, delx, deltlabel, delxlabel]

        self.play(FadeOut(*fadeouts1))

        # Second piece
        wlpiece1 = hyperbolapiece(x0+1.6, x0+3)
        self.play(Create(wlpiece1), run_time=1)
        wlp0 = Dot(wlpiece1.get_start())
        wlp1 = Dot(wlpiece1.get_end())

        wlp0t = gli(ax.y_axis, Line(wlp0.get_center(), wlp0.get_center() - xhat*10))
        wlp1t = gli(ax.y_axis, Line(wlp1.get_center(), wlp1.get_center() - xhat*10))
        

        wlp0x = gli(ax.x_axis, Line(wlp0.get_center(), wlp0.get_center() - that*10))
        wlp1x = gli(ax.x_axis, Line(wlp1.get_center(), wlp1.get_center() - that*10))

        wlp0xprj = DashedLine(wlp0, wlp0x).set_color(gndhighlight)
        wlp0tprj = DashedLine(wlp0, wlp0t).set_color(gndhighlight)
        wlp1xprj = DashedLine(wlp1, wlp1x).set_color(gndhighlight)
        wlp1tprj = DashedLine(wlp1, wlp1t).set_color(gndhighlight)

        self.play(Create(wlp0tprj), Create(wlp0xprj),Create(wlp1tprj), Create(wlp1xprj))
        
        delt = Line(wlp0t, wlp1t, stroke_width=6).set_color(gndhighlight)
        deltlabel = MathTex(r"\Delta t").set_color(gndhighlight).move_to(delt.get_center()).shift(LEFT*0.5)
        delx = Line(wlp0x, wlp1x, stroke_width=6).set_color(gndhighlight)
        delxlabel = MathTex(r"\Delta x").set_color(gndhighlight).move_to(delx.get_center()).shift(DOWN*0.5)
        self.play(Create(delt), Create(delx), Write(deltlabel), Write(delxlabel), run_time=1.5)
        self.wait(2)

        fadeouts1 = [wlpiece1, wlp0tprj, wlp0xprj, wlp1tprj, wlp1xprj, delt, delx, deltlabel, delxlabel]
        self.play(FadeOut(*fadeouts1))

        # 3rd piece
        wlpiece1 = hyperbolapiece(x0+4.8, x0+6.5)
        self.play(Create(wlpiece1), run_time=1)
        wlp0 = Dot(wlpiece1.get_start())
        wlp1 = Dot(wlpiece1.get_end())

        wlp0t = gli(ax.y_axis, Line(wlp0.get_center(), wlp0.get_center() - xhat*10))
        wlp1t = gli(ax.y_axis, Line(wlp1.get_center(), wlp1.get_center() - xhat*10))
        

        wlp0x = gli(ax.x_axis, Line(wlp0.get_center(), wlp0.get_center() - that*10))
        wlp1x = gli(ax.x_axis, Line(wlp1.get_center(), wlp1.get_center() - that*10))

        wlp0xprj = DashedLine(wlp0, wlp0x).set_color(gndhighlight)
        wlp0tprj = DashedLine(wlp0, wlp0t).set_color(gndhighlight)
        wlp1xprj = DashedLine(wlp1, wlp1x).set_color(gndhighlight)
        wlp1tprj = DashedLine(wlp1, wlp1t).set_color(gndhighlight)

        self.play(Create(wlp0tprj), Create(wlp0xprj),Create(wlp1tprj), Create(wlp1xprj))
        
        delt = Line(wlp0t, wlp1t, stroke_width=6).set_color(gndhighlight)
        deltlabel = MathTex(r"\Delta t").set_color(gndhighlight).move_to(delt.get_center()).shift(LEFT*0.5)
        delx = Line(wlp0x, wlp1x, stroke_width=6).set_color(gndhighlight)
        delxlabel = MathTex(r"\Delta x").set_color(gndhighlight).move_to(delx.get_center()).shift(DOWN*0.5)
        self.play(Create(delt), Create(delx), Write(deltlabel), Write(delxlabel), run_time=1.5)
        

        fadeouts1 = [wlpiece1, wlp0tprj, wlp0xprj, wlp1tprj, wlp1xprj, delt, delx, deltlabel, delxlabel]
        self.play(FadeOut(*fadeouts1))
        self.wait(2)

        ############## Chapter 2: Tangent line as the cameraman

        tangent_length = 3.2

        def get_tgline(x):
            y0 = hyperbola(x)
            slope = (x-center)/y0
            tangent_point = ax.c2p(x, y0, 0)

            # Normalize in scene space so every tangent has exactly the same
            # visible length, independent of its slope.
            tangent_direction = ax.c2p(x+1, y0+slope, 0) - tangent_point
            tangent_direction /= np.linalg.norm(tangent_direction)
            half_length = tangent_length/2
            tgline0 = Line(
                tangent_point-tangent_direction*half_length,
                tangent_point+tangent_direction*half_length,
                stroke_width=5,
                color=LemonOrange,
            )
            tgdot = Dot(tangent_point, radius=0.055).set_color(Vanilla)

            return [tgdot, tgline0]

        def get_tprime_axis(x):
            tangent_point = ax.c2p(x, hyperbola(x), 0)
            tangent_direction = get_tgline(x)[1].get_unit_vector()
            tprime_axis_length = 2.3
            return Arrow(
                tangent_point,
                tangent_point+tangent_direction*tprime_axis_length,
                buff=0,
                stroke_width=5,
                color=LightBlue,
                tip_length=0.16,
                max_tip_length_to_length_ratio=0.10,
            )

        def spring(t):
            """Damped overshoot ending exactly at the target mobject."""
            return 1-np.exp(-6*t)*np.cos(4.5*np.pi*t)
        

        acc1 = Dot(worldline.get_start())
        self.play(Create(acc1))

        # Add two closely spaced samples before the old starting point and three
        # more samples farther along the flatter, upper part of the hyperbola.
        original_tgxs = np.geomspace(0.3, 4.5, 14)
        tgxs = np.concatenate((
            [0, 0.08, 0.15, 0.22],
            original_tgxs,
            [5.3, 6.0, 6.7],
        ))


        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate()
            .scale(1.15))
        tglines = VGroup()
        for i in range(len(tgxs)-1):

            xi = tgxs[i+1]
            
            self.play(
                MoveAlongPath(acc1, hyperbolapiece(tgxs[i], xi)),
                run_time=0.5,
                rate_func=linear,
            )
            
            tglinei = get_tgline(xi)[1]
            self.play(Create(tglinei), run_time=0.18)
            self.wait(0.5)
            self.play(
                tglinei.animate.set_stroke(width=3, opacity=0.35),
                run_time=0.12,
            )
            tglines.add(tglinei)

        self.wait(3)
        self.play(FadeOut(tglines, acc1), Restore(self.camera.frame), run_time=1.4)
        self.wait(3)
        

        ############## Chapter 4: Tangent lines as the t' axis for the accelerator
        # self.camera.frame.save_state()
        # self.play(
        #     self.camera.frame.animate()
        #     .scale(1.15)
        #     .move_to(ax.c2p(3.2, 5.0)),
        #     run_time=1.4,
        # )

        acc1 = Dot(worldline.get_start())
        self.play(Create(acc1))

        # Use every third tangent position so the longer t' axes stay legible.
        tprime_xs = np.concatenate(([0], tgxs[1::3]))

        demonstration_steps = 6
        tprime_axes = VGroup()
        for i in range(len(tprime_xs)-1):
            if i == demonstration_steps:
                break

            xi = tprime_xs[i+1]

            self.play(
                MoveAlongPath(acc1, hyperbolapiece(tprime_xs[i], xi)),
                run_time=0.5,
                rate_func=linear,
            )

            tangent = get_tgline(xi)[1]
            tprime_axis = get_tprime_axis(xi)
            tprime_label = MathTex(r"t^\prime").set_color(LightBlue)
            tprime_label.scale(0.55).next_to(tprime_axis.get_end(), UR, buff=0.06)

            self.play(Create(tangent), run_time=0.3)
            self.wait(0.4)
            self.play(
                ReplacementTransform(tangent, tprime_axis, rate_func=rate_functions.ease_in_out_elastic),
                FadeIn(tprime_label, shift=tprime_axis.get_unit_vector()*0.15),
                run_time=0.9,
            )
            self.wait(0.3)
            self.play(
                tprime_axis.animate.set_stroke(width=3, opacity=0.35).set_fill(opacity=0.35),
                FadeOut(tprime_label),
                run_time=0.18,
            )
            tprime_axes.add(tprime_axis)

        self.wait(1)
        # self.play(Restore(self.camera.frame), run_time=1.4)
        self.play(FadeOut(tprime_axes, acc1), run_time=0.6)

        # Bring back every tangent from Chapter 2, then turn all of their upper
        # halves into momentarily co-moving t' axes in one smooth motion.
        all_tangents = VGroup(*[
            get_tgline(x)[1].set_stroke(width=3, opacity=0.35)
            for x in tgxs[1:]
        ])
        last_demonstrated_x = tprime_xs[demonstration_steps]
        last_demonstrated_index = np.where(
            np.isclose(tgxs, last_demonstrated_x)
        )[0][0]

        # Before the final demonstrated axis, transform alternating tangents.
        # From that point onward, transform every tangent so the arrow spacing
        # opens near the vertex and becomes denser farther up the hyperbola.
        alternating_indices = np.arange(last_demonstrated_index, 0, -2)[::-1]
        later_indices = np.arange(last_demonstrated_index+1, len(tgxs))
        arrow_indices = np.concatenate((alternating_indices, later_indices))
        skipped_indices = np.setdiff1d(np.arange(1, len(tgxs)), arrow_indices)

        all_tprime_axes = VGroup(*[
            get_tprime_axis(tgxs[index])
            for index in arrow_indices
        ])

        self.play(
            # self.camera.frame.animate.scale(1.15).move_to(ax.c2p(3.2, 5.0)),
            *[FadeIn(tangent) for tangent in all_tangents],
            run_time=1.2,
        )

        wlcopy = worldline.copy().set_color(LemonOrange)
        self.wait(2)
        self.play(Transform(all_tangents, wlcopy), run_time=2.5)

        self.wait(5)
        # self.wait(0.5)
        # self.play(
        #     *[
        #         ReplacementTransform(all_tangents[index-1], tprime_axis)
        #         for index, tprime_axis in zip(arrow_indices, all_tprime_axes)
        #     ],
        #     *[
        #         FadeOut(all_tangents[index-1])
        #         for index in skipped_indices
        #     ],
        #     run_time=2.2,
        #     rate_func=smooth,
        # )
        # self.wait(3)

        ############## Chapter 5: Drawing the x' axis using light rays and symmetry
        ############## Chapter 6: x' axes as lines of simultaneity for "now"


        ############## Chapter 7: Smooth animation of the axes
        # Move along path approach:
        # acc1 = Dot(worldline.get_start())
        # self.play(Create(acc1))
        # accxp0 = getxprime(ax.p2c(acc1.get_center())[0])
        # acctp0 = gettprime(ax.p2c(acc1.get_center())[0])
        # # self.play(Create(accxp0), Create(acctp0))

        # accxp = always_redraw(lambda: getxprime(ax.p2c(acc1.get_center())[0]))
        # acctp = always_redraw(lambda: gettprime(ax.p2c(acc1.get_center())[0]))
        # self.play(Create(accxp))
        # self.play(Create(acctp))
        # self.play(MoveAlongPath(acc1, hyperbolapiece(0, 0.1), run_time=3, rate_func=rate_functions.ease_in_out_quad))
        # self.wait(2)

        # self.play(MoveAlongPath(acc1, hyperbolapiece(0.1, 0.8), run_time=6, rate_func=linear))
        # self.wait(2)



class TprimeAxes(MovingCameraScene):
    # Show why the t' axes are the tangent lines to the hyperbolic worldline of an accelerating observer.
    # Demonstrate that an observer being in rest in their own frame leads to this.

    def construct(self):
        self.camera.background_color = BGtry

        ax = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_ticks": False, "stroke_width": 5},
        ).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0, 0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0, 7], [0, 7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8, 6.8)).set_color(lightcolor)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)

        self.camera.frame.scale(0.6)
        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ogdot))
        self.wait(1)
        self.play(
            Transform(ogdot, ax.x_axis),
            self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4),
            rate_func=rate_functions.ease_out_back,
            run_time=1.1,
        )
        self.play(
            Create(ax.y_axis),
            self.camera.frame.animate.shift(UP*3.8),
            rate_func=rate_functions.ease_out_back,
            run_time=1.1,
        )
        self.play(Write(xlabel), Write(tlabel))
        self.play(Create(grid1), run_time=1.2)
        self.play(Create(lightray), run_time=1.2)

        def line_or_empty(start, end, color, stroke_width=4, opacity=1, dashed=False):
            if np.linalg.norm(end-start) < 0.01:
                return VGroup()
            line = DashedLine(start, end, dash_length=0.08) if dashed else Line(start, end)
            line.set_color(color).set_stroke(width=stroke_width, opacity=opacity)
            return line

        def unit_vector(vector):
            norm = np.linalg.norm(vector)
            if norm == 0:
                return vector
            return vector/norm

        ################################ Ground frame rest ################################
        ground_tau = 3.25
        ground_tilt = ValueTracker(0)

        def ground_tip():
            return ax.c2p(ground_tilt.get_value()*ground_tau, ground_tau)

        def ground_xfoot():
            return ax.c2p(ground_tilt.get_value()*ground_tau, 0)

        def ground_tfoot():
            return ax.c2p(0, ground_tau)

        ground_arrow = always_redraw(
            lambda: Arrow(
                og,
                ground_tip(),
                buff=0,
                stroke_width=7,
                max_tip_length_to_length_ratio=0.08,
            ).set_color(pcolor1).set_z_index(3)
        )
        ground_x_projector = always_redraw(
            lambda: line_or_empty(ground_tip(), ground_xfoot(), gndcolor1, 3, 0.75, dashed=True)
        )
        ground_t_projector = always_redraw(
            lambda: line_or_empty(ground_tip(), ground_tfoot(), gndcolor1, 3, 0.75, dashed=True)
        )
        ground_delta_t = always_redraw(
            lambda: line_or_empty(og, ground_tfoot(), gndhighlight, 6, min(1, ground_tilt.get_value()*6))
        )
        ground_delta_x = always_redraw(
            lambda: line_or_empty(og, ground_xfoot(), gndhighlight, 6, min(1, ground_tilt.get_value()*6))
        )
        ground_dt_label = always_redraw(
            lambda: MathTex(r"\Delta t").set_color(gndhighlight).scale(0.75)
            .move_to((og+ground_tfoot())/2).shift(LEFT*0.45)
        )
        ground_dx_label = always_redraw(
            lambda: MathTex(r"\Delta x").set_color(gndhighlight).scale(0.75)
            .move_to((og+ground_xfoot())/2).shift(DOWN*0.35)
            .set_opacity(min(1, ground_tilt.get_value()*6))
        )

        self.wait(2)
        self.play(Create(ground_arrow), run_time=0.8)
        self.wait(2)
        # self.play(ground_tilt.animate.set_value(0.27), run_time=2, rate_func=smooth)
        self.play(
            Create(ground_x_projector),
            Create(ground_t_projector),
            Create(ground_delta_t),
            Create(ground_delta_x),
            Write(ground_dt_label),
            Write(ground_dx_label),
            run_time=1,
        )
        self.play(ground_tilt.animate.set_value(0.27), run_time=2, rate_func=smooth)

        self.wait(2)
        self.play(ground_tilt.animate.set_value(0), run_time=2, rate_func=smooth)
        ground_v_label = MathTex(r"\vec v").set_color(pcolor2).scale(1.1)
        ground_v_label.next_to(ground_arrow.get_end(), RIGHT+UP*0.3, buff=0.15)
        self.play(Write(ground_v_label), run_time=0.7)
        self.wait(2)
        self.play(
            FadeOut(
                ground_x_projector,
                ground_t_projector,
                ground_delta_t,
                ground_delta_x,
                ground_dt_label,
                ground_dx_label,
                ground_arrow,
                ground_v_label,
            ),
            run_time=0.8,
        )

        ################################ Primed inertial frame rest ################################
        prime_v = ValueTracker(0.33)
        prime_axis_length = 3.75

        def prime_t_end():
            speed = prime_v.get_value()
            return ax.c2p(speed*prime_axis_length, np.sqrt(prime_axis_length**2+(speed*prime_axis_length)**2))

        def prime_x_end():
            speed = prime_v.get_value()
            return ax.c2p(np.sqrt(prime_axis_length**2+(speed*prime_axis_length)**2), speed*prime_axis_length)

        def tphat():
            return unit_vector(prime_t_end()-og)

        def xphat():
            return unit_vector(prime_x_end()-og)

        tpax = always_redraw(lambda: Arrow(og, prime_t_end(), buff=0).set_color(pcolor1))
        xpax = always_redraw(lambda: Arrow(og, prime_x_end(), buff=0).set_color(pcolor1))
        xplabel = always_redraw(
            lambda: MathTex("x'").move_to(xpax.get_end()).shift(UP*0.5+LEFT*0.15).set_color(SteelBlue)
        )
        tplabel = always_redraw(
            lambda: MathTex("t'").move_to(tpax.get_end()).shift(RIGHT*0.4+DOWN*0.07).set_color(SteelBlue)
        )

        self.play(Create(tpax), Create(xpax), run_time=0.9, rate_func=rate_functions.ease_out_cubic)
        self.play(Write(xplabel), Write(tplabel), run_time=0.6)

        prime_alpha = ValueTracker(0)
        prime_tilt = ValueTracker(0)
        prime_motion_length = 2.55

        def prime_event_point(alpha=None):
            if alpha is None:
                alpha = prime_alpha.get_value()
            return og+prime_motion_length*alpha*(tphat()+prime_tilt.get_value()*xphat())

        prime_dot = always_redraw(
            lambda: Dot(prime_event_point(), radius=0.095).set_color(NeonOrange).set_z_index(5)
        )
        prime_rest_label = always_redraw(
            lambda: MathTex(r"\Delta x'=0").set_color(gndhighlight).scale(0.75)
            .next_to(prime_dot, RIGHT, buff=0.15)
        )

        self.play(Create(prime_dot), Write(prime_rest_label), run_time=0.7)
        self.play(prime_alpha.animate.set_value(0.86), run_time=1.8, rate_func=linear)
        self.wait(0.6)
        self.play(prime_alpha.animate.set_value(0), FadeOut(prime_rest_label), run_time=0.7)

        prime_tilt.set_value(0.27)
        prime_motion_arrow = always_redraw(
            lambda: Arrow(
                og,
                prime_event_point(alpha=1),
                buff=0,
                stroke_width=7,
                max_tip_length_to_length_ratio=0.08,
            ).set_color(gndhighlight).set_z_index(3)
        )

        def prime_projection_point():
            return prime_event_point()

        def prime_foot_on_x():
            point = prime_projection_point()
            axis_line = Line(og-xphat()*9, og+xphat()*9).set_opacity(0)
            projector = Line(point-tphat()*9, point+tphat()*9).set_opacity(0)
            intersection = gli(axis_line, projector)
            return og if intersection is None else intersection

        def prime_foot_on_t():
            point = prime_projection_point()
            axis_line = Line(og-tphat()*9, og+tphat()*9).set_opacity(0)
            projector = Line(point-xphat()*9, point+xphat()*9).set_opacity(0)
            intersection = gli(axis_line, projector)
            return og if intersection is None else intersection

        def prime_dx_opacity():
            return min(1, prime_alpha.get_value()*prime_tilt.get_value()*7)

        prime_x_projector = always_redraw(
            lambda: line_or_empty(prime_projection_point(), prime_foot_on_x(), gndhighlight, 3, 0.75, dashed=True)
        )
        prime_t_projector = always_redraw(
            lambda: line_or_empty(prime_projection_point(), prime_foot_on_t(), gndhighlight, 3, 0.75, dashed=True)
        )
        prime_delta_x = always_redraw(
            lambda: line_or_empty(og, prime_foot_on_x(), gndhighlight, 6, prime_dx_opacity())
        )
        prime_delta_t = always_redraw(
            lambda: line_or_empty(og, prime_foot_on_t(), gndhighlight, 6, min(1, prime_alpha.get_value()*4))
        )
        prime_dx_label = always_redraw(
            lambda: MathTex(r"\Delta x'").set_color(gndhighlight).scale(0.7)
            .move_to((og+prime_foot_on_x())/2-tphat()*0.35)
            .set_opacity(prime_dx_opacity())
        )
        prime_dt_label = always_redraw(
            lambda: MathTex(r"\Delta t'").set_color(gndhighlight).scale(0.7)
            .move_to((og+prime_foot_on_t())/2-xphat()*0.35)
            .set_opacity(min(1, prime_alpha.get_value()*4))
        )

        self.play(Create(prime_motion_arrow), run_time=0.6)
        self.play(prime_alpha.animate.set_value(0.14), run_time=0.25, rate_func=linear)
        self.play(
            Create(prime_x_projector),
            Create(prime_t_projector),
            Create(prime_delta_x),
            Create(prime_delta_t),
            Write(prime_dx_label),
            Write(prime_dt_label),
            run_time=0.8,
        )
        self.play(prime_alpha.animate.set_value(1), run_time=1.8, rate_func=linear)
        self.wait(0.6)

        self.play(prime_tilt.animate.set_value(0), FadeOut(prime_delta_t), FadeOut(prime_dot), run_time=1.8, rate_func=smooth)
        prime_v_label = MathTex(r"\vec v").set_color(gndhighlight).scale(0.9)
        prime_v_label.next_to(prime_motion_arrow.get_end(), RIGHT, buff=0.15)
        self.play(Write(prime_v_label), run_time=0.7)
        self.wait(0.8)
        self.play(
            FadeOut(
                prime_x_projector,
                prime_t_projector,
                prime_delta_x,
                prime_delta_t,
                prime_dx_label,
                prime_dt_label,
                prime_motion_arrow,
                prime_v_label,
                tpax,
                xpax,
                tplabel,
                xplabel,
            ),
            run_time=0.9,
        )

        ################################ Accelerated observer ################################
        hypx0 = 2
        hypxf = 5.5
        center = -2

        def hyperbola(x, x0=hypx0, center=center):
            return np.sqrt((x-center)**2-x0**2)

        def hyperbolapiece(x1, x2, opacity=1):
            return ax.plot(
                lambda x: hyperbola(x),
                x_range=[x1, x2, 0.01],
                use_smoothing=False,
                stroke_width=8,
            ).set_opacity(opacity).set_color(phighlight2)

        P = ax.c2p(center, 0, 0)

        def getxprime(x, P_point=P, colorchoice=pcolor1):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xprime_hat = intline.get_unit_vector()
            return Arrow(hyp_point, hyp_point+xprime_hat*2.75, buff=0, stroke_width=5).set_color(colorchoice)

        def gettprime(x, P_point=P, colorchoice=pcolor1):
            hyp_point = ax.c2p(x, hyperbola(x))
            intline = Line(P_point, hyp_point)
            xprime_hat = intline.get_unit_vector()
            tprime_hat = np.array([xprime_hat[1], xprime_hat[0], 0])
            return Arrow(hyp_point, hyp_point+tprime_hat*2.75, buff=0, stroke_width=5).set_color(colorchoice)

        worldline = ax.plot(
            lambda x: hyperbola(x),
            x_range=[hypx0+center, hypxf, 0.01],
            stroke_width=7,
        ).set_color(gndcolor2)

        self.play(Create(worldline), run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        acc1 = Dot(worldline.get_start(), radius=0.12).set_color(NeonOrange).set_z_index(5)
        self.play(Create(acc1))

        def acc_x_value():
            return np.clip(ax.p2c(acc1.get_center())[0], hypx0+center+0.001, hypxf)

        acctp = always_redraw(lambda: gettprime(acc_x_value()))
        accxp = always_redraw(lambda: getxprime(acc_x_value()))
        acctplabel = always_redraw(
            lambda: MathTex("t'").set_color(SkyBlue).scale(0.7).next_to(acctp.get_end(), UR, buff=0.07)
        )
        accxplabel = always_redraw(
            lambda: MathTex("x'").set_color(SkyBlue).scale(0.7).next_to(accxp.get_end(), UR, buff=0.07)
        )
        

        self.play(Create(acctp), Create(accxp), Write(acctplabel), Write(accxplabel), run_time=0.9)
        self.play(MoveAlongPath(acc1, hyperbolapiece(0, 1.6)), run_time=6, rate_func=linear)

        accvlabel = always_redraw(
            lambda: MathTex(r"\vec v").set_color(NeonOrange).scale(1.1).next_to(acctp.get_end(), UL, buff=0.1)
        )

        self.play(FadeOut(accxp), FadeOut(accxplabel), FadeOut(acctplabel), FadeIn(accvlabel), run_time=0.8)
        self.play(MoveAlongPath(acc1, hyperbolapiece(1.6, 4.5)), run_time=5, rate_func=rate_functions.ease_in_sine)
        self.wait(2)



class LikeCalculus(MovingCameraScene):
    # Argue that this is the same idea as we use in basic calculus, where we need an infinite number of 
    # tangent lines to fully describe a curve with a slope that changes at all points. Put together with the
    # concept of locality, we can fully describe an accelerated worldline.

    def construct(self):
        self.camera.background_color = BGtry

        ax = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_ticks": False, "stroke_width": 5},
        ).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.shift(ORIGIN-ax.c2p(0, 0))
        og = ORIGIN
        grid1 = homemade_grid(ax, [0, 7], [0, 7], propercolor)
        lightray = DashedLine(og, ax.c2p(6.8, 6.8)).set_color(lightcolor)
        xlabel = MathTex("x").move_to(ax.x_axis.get_end()).shift(UP*0.5).set_color(gndcolor1)
        tlabel = MathTex("t").move_to(ax.y_axis.get_end()).shift(RIGHT*0.35+UP*0.1).set_color(gndcolor1)
        self.camera.frame.scale(0.6)

        ogdot = Dot(ORIGIN).set_color(gndcolor1)
        self.play(Create(ogdot))
        self.wait(0.5)
        self.play(
            Transform(ogdot, ax.x_axis),
            self.camera.frame.animate.scale(1/0.6).shift(RIGHT*4),
            rate_func=rate_functions.ease_out_back,
            run_time=1.1,
        )
        self.play(
            Create(ax.y_axis),
            self.camera.frame.animate.shift(UP*3.8),
            rate_func=rate_functions.ease_out_back,
            run_time=1.1,
        )
        self.play(Write(xlabel), Write(tlabel))
        self.play(Create(grid1), Create(lightray), run_time=1.2)

        plateau_slope = 1.5
        left_span = 0.7
        right_span = 0.7
        root = np.sqrt(plateau_slope**2-1)
        hyp_radius = left_span/(plateau_slope/root-1)
        join_height = hyp_radius/root
        join_offset = hyp_radius*plateau_slope/root

        def left_hyperbola(x):
            return np.sqrt(np.maximum((x+hyp_radius)**2-hyp_radius**2, 0))

        def curve_data(plateau_span):
            x1 = left_span
            y1 = join_height
            x2 = x1+plateau_span
            y2 = y1+plateau_slope*plateau_span
            right_center = x2-join_offset
            right_shift = y2-join_height
            return x1, y1, x2, y2, right_center, right_shift

        def right_hyperbola(x, plateau_span):
            x1, y1, x2, y2, right_center, right_shift = curve_data(plateau_span)
            return np.sqrt(np.maximum((x-right_center)**2-hyp_radius**2, 0))+right_shift

        def plateau_point(plateau_span, alpha):
            x1, y1, x2, y2, right_center, right_shift = curve_data(plateau_span)
            x = x1+alpha*plateau_span
            return ax.c2p(x, y1+plateau_slope*(x-x1))

        def make_worldline(plateau_span):
            x1, y1, x2, y2, right_center, right_shift = curve_data(plateau_span)
            left_xs = np.linspace(0, x1, 45)
            plateau_xs = np.linspace(x1, x2, 90)
            right_xs = np.linspace(x2, x2+right_span, 45)
            points = []

            for x in left_xs:
                points.append(ax.c2p(x, left_hyperbola(x)))
            for x in plateau_xs:
                points.append(ax.c2p(x, y1+plateau_slope*(x-x1)))
            for x in right_xs:
                points.append(ax.c2p(x, right_hyperbola(x, plateau_span)))

            curve = VMobject()
            curve.set_points_smoothly(points)
            curve.set_stroke(gndcolor2, width=7)
            return curve

        def unit_scene_vector(dx, dt):
            vector = ax.c2p(dx, dt)-ax.c2p(0, 0)
            return vector/np.linalg.norm(vector)

        tprime_hat = unit_scene_vector(1, plateau_slope)
        xprime_hat = unit_scene_vector(1, 1/plateau_slope)
        local_axis_length = 1.75

        def focus_on_plateau(plateau_span, zoom=0.72):
            midpoint = plateau_point(plateau_span, 0.5)
            return self.camera.frame.animate.scale(zoom).move_to(midpoint).shift(UP*0.35+RIGHT*0.1)

        def run_local_frame(plateau_span, start=0.12, end=0.88, run_time=4):
            alpha = ValueTracker(start)

            local_origin = always_redraw(
                lambda: Dot(plateau_point(plateau_span, alpha.get_value()), radius=0.075)
                .set_color(NeonOrange)
                .set_z_index(5)
            )
            tp = always_redraw(
                lambda: Arrow(
                    plateau_point(plateau_span, alpha.get_value()),
                    plateau_point(plateau_span, alpha.get_value())+tprime_hat*local_axis_length,
                    buff=0,
                    stroke_width=5,
                    max_tip_length_to_length_ratio=0.12,
                ).set_color(pcolor1)
            )
            xp = always_redraw(
                lambda: Arrow(
                    plateau_point(plateau_span, alpha.get_value()),
                    plateau_point(plateau_span, alpha.get_value())+xprime_hat*local_axis_length,
                    buff=0,
                    stroke_width=5,
                    max_tip_length_to_length_ratio=0.12,
                ).set_color(pcolor1)
            )
            moving_grid = always_redraw(
                lambda: lorentz_grid(xp, tp, pcolor1, opacitychoice=0.35, spacing=0.35, length_ratio=0.82)
            )
            tplabel = always_redraw(
                lambda: MathTex("t'").set_color(SkyBlue).scale(0.55).next_to(tp.get_end(), UR, buff=0.05)
            )
            xplabel = always_redraw(
                lambda: MathTex("x'").set_color(SkyBlue).scale(0.55).next_to(xp.get_end(), UR, buff=0.05)
            )

            self.play(
                Create(tp),
                Create(xp),
                FadeIn(moving_grid),
                Create(local_origin),
                Write(tplabel),
                Write(xplabel),
                run_time=0.9,
            )
            self.play(alpha.animate.set_value(end), run_time=run_time, rate_func=linear)
            self.wait(0.35)
            self.play(
                FadeOut(tp),
                FadeOut(xp),
                FadeOut(moving_grid),
                FadeOut(local_origin),
                FadeOut(tplabel),
                FadeOut(xplabel),
                run_time=0.7,
            )

        plateau_spans = [2.1, 1.05, 0.525]
        worldline = make_worldline(plateau_spans[0])
        self.play(Create(worldline), run_time=1.4, rate_func=rate_functions.ease_out_cubic)
        self.wait(0.5)

        self.play(focus_on_plateau(plateau_spans[0], zoom=0.68), run_time=1.2)
        run_local_frame(plateau_spans[0], run_time=4.3)

        for i, plateau_span in enumerate(plateau_spans[1:]):
            new_worldline = make_worldline(plateau_span)
            self.play(
                Transform(worldline, new_worldline),
                self.camera.frame.animate.move_to(plateau_point(plateau_span, 0.5)).shift(UP*0.35+RIGHT*0.1),
                run_time=1.4,
                rate_func=smooth,
            )
            if i == 1:
                self.play(
                    self.camera.frame.animate.scale(0.82).move_to(plateau_point(plateau_span, 0.5)).shift(UP*0.35+RIGHT*0.1),
                    run_time=1,
                )
            run_local_frame(plateau_span, run_time=3.6-i*0.5)

        self.wait(2)



class AccLorentzAxes(MovingCameraScene):
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



# 85%
# I guess only aesthetics left here
class CameramenLorentzAxes(MovingCameraScene):
    def construct(self):
        
        self.camera.background_color = BGBlue1
        ax = Axes(x_range=[0,10,1], y_range=[0,10,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor).set_opacity(0.5)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor)
        # lightlabel = MathTex("c").next_to(xct.get_end(), UR).set_color(lightcolor)

        # Initial axes, to be Lorentz transformed:
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])


        hypx0 = 4
        hypxf = 10
        def hyperbola(x, x0=hypx0):
            return np.sqrt(x**2 - x0**2)
        

        def hyperbolapiece(x1, x2, opacity=0, x0=hypx0):
            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece

        worldline = ax.plot(lambda x : np.sqrt(x**2 - hypx0**2), x_range=[hypx0,hypxf,0.01]).set_color(NewOrange2)

        self.add(*[ax, xct, ax_labels, worldline])

        self.wait(2)

        def get_hypaxes(x, x0=hypx0, length=1.2):
            pt1 = hyperbola(x-0.01)
            pt2 = hyperbola(x+0.01)
            
            slope = (pt2-pt1)/0.02

            frameline = Arrow(OG, ax.c2p(length*2, length*slope*2), buff=0).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())
            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Arrow(OG, OG+xpdir*frameline.get_length(), buff=0).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            lightline = DashedLine(ax.c2p(x, hyperbola(x)), ax.c2p(x+length*2, hyperbola(x)+length*2)).set_color(lightcolor)

            return frameline, xpaxis, lightline
            
            
        # let's do this with a loop for more control! 
        N=15
        xs = np.linspace(hypx0, hypxf, N)
        ts = np.linspace(0,np.sqrt(hypxf**2 - hypx0**2), N)
        
        wldot = Dot().set_color(LemonOrange).move_to(worldline.get_start())
        self.play(Create(wldot))
        frametime=1
        self.play(self.camera.frame.animate.scale(0.7).move_to(wldot).shift(UP*2+RIGHT*1.5), run_time=2)
        first_skip=False
        for tau in range(N):
            if tau==N-1:
                break
            hyptau = hyperbolapieceT(ts[tau], ts[tau+1], opacity=0)
            delt0 = ts[1]-ts[0]
            delt = ts[tau+1] - ts[tau]
            frametimei = frametime*(delt/delt0)**4  # start slow, get faster

            if tau == 2:
                tauline, tauxax, lightline = get_hypaxes(ax.p2c(wldot.get_center())[0])
                # self.play(Create(tauline),run_time=1)
                tparrow = Arrow(tauline.get_start(), tauline.get_end(), buff=0, stroke_width=2).set_color(LightBlue)
                xparrow = Arrow(tauxax.get_start(), tauxax.get_end(), buff=0, stroke_width=2).set_color(LightBlue)

                tplabel = MathTex("t'").set_color(SkyBlue).scale(0.7).move_to(tparrow.get_end()).shift(UP*0.2+RIGHT*0.2)

                xpiszero = MathTex("x'=0").set_color(LightBlue).scale(0.8).move_to(wldot).shift(DOWN*0.15,RIGHT*0.55)
                xplabel = MathTex("x'").set_color(SkyBlue).scale(0.7).move_to(xparrow.get_end()).shift(UP*0.2+RIGHT*0.2)

                self.play(Create(tparrow))
                self.play(Write(tplabel))
                self.wait(2)
                self.play(Write(xpiszero))
                self.wait(2)
                self.play(FadeOut(xpiszero))
                self.wait()
                self.play(Create(lightline))
                self.wait(2)
                self.play(Create(xparrow))
                self.play(Write(xplabel))
                self.wait(2)
                self.play(FadeOut(*[tparrow, lightline, xparrow, tplabel, xplabel]), run_time=0.5)


            if tau == 5:
                tauline, tauxax, lightline = get_hypaxes(ax.p2c(wldot.get_center())[0])
                tparrow = Arrow(tauline.get_start(), tauline.get_end(), buff=0, stroke_width=2).set_color(LightBlue)
                xparrow = Arrow(tauxax.get_start(), tauxax.get_end(), buff=0, stroke_width=2).set_color(LightBlue)

                tplabel = MathTex("t'").set_color(SkyBlue).scale(0.7).move_to(tparrow.get_end()).shift(UP*0.2+RIGHT*0.2)
                xplabel = MathTex("x'").set_color(SkyBlue).scale(0.7).move_to(xparrow.get_end()).shift(UP*0.2+RIGHT*0.2)


                self.play(Create(tparrow),Create(xparrow), Create(lightline), run_time=1)
                self.wait()
                self.play(FadeOut(tparrow),FadeOut(xparrow), FadeOut(lightline), run_time=0.5)
            

            if tau>N/3 and tau%2==0:

                if tau == 8:
                    tauline, tauxax, lightline = get_hypaxes(ax.p2c(wldot.get_center())[0])
                    self.play(Create(tauline),Create(tauxax), run_time=1)
                    self.wait()
                    self.play(FadeOut(tauline),FadeOut(tauxax), run_time=0.5)

                if tau == 12:
                    tauline, tauxax, lightline = get_hypaxes(ax.p2c(wldot.get_center())[0])
                    self.play(Create(tauline),Create(tauxax), run_time=1)
                    self.wait()
                    self.play(FadeOut(tauline),FadeOut(tauxax), run_time=0.5)

                first_skip=True
                continue
            
            elif tau>N/3 and tau%2==1 and first_skip:

                hyptau = hyperbolapieceT(ts[tau-1], ts[tau+1], opacity=0)
                delt0 = ts[1]-ts[0]
                delt = ts[tau+1] - ts[tau]
                frametimei = frametime*1.5*(delt/delt0)**4  # start slow, get faster
                self.play(MoveAlongPath(wldot, hyptau), self.camera.frame.animate.move_to(wldot),
                          rate_func=linear, run_time=frametimei)
                
            else:
                self.play(MoveAlongPath(wldot, hyptau),rate_func=linear, run_time=frametimei)
                
            # self.play(Create(hyptau))

        self.wait(5)


# 60%
# Smoothness, the problematic transition at the start, camera angles.
class CameramenLorentzAxes2(MovingCameraScene):
    def construct(self):
        
        self.camera.background_color = BGBlue1
        ax = Axes(x_range=[0,10,1], y_range=[0,10,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)


        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor).set_opacity(0.5)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(10-0.2,10-0.2)).set_color(lightcolor)
        # lightlabel = MathTex("c").next_to(xct.get_end(), UR).set_color(lightcolor)

        # Initial axes, to be Lorentz transformed:
        OG = ax.c2p(0,0)
        xhat = np.array([Dot(ax.c2p(1,0)).get_x() - Dot(ax.c2p(0,0)).get_x(),0,0])
        that = np.array([0, Dot(ax.c2p(0,1)).get_y() - Dot(ax.c2p(0,0)).get_y(),0])


        hypx0 = 4
        hypxf = 10
        def hyperbola(x, x0=hypx0):
            return np.sqrt(x**2 - x0**2)
        

        def hyperbolapiece(x1, x2, opacity=0, x0=hypx0):
            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        def hyperbolapieceT(t1, t2, opacity=0, x0=hypx0):
            #t^2 = sqrt(x^2 - x0^2)
            x1 = np.sqrt(t1**2 +x0**2)
            x2 = np.sqrt(t2**2 +x0**2)

            wlpiece = ax.plot(lambda x: np.sqrt(x**2 - x0**2), x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece

        worldline = ax.plot(lambda x : np.sqrt(x**2 - hypx0**2), x_range=[hypx0,hypxf,0.01]).set_color(NewOrange2)

        self.add(*[ax, xct, ax_labels, worldline])

        self.wait(2)

        def get_hypaxest(x, x0=hypx0, length=1.2):
            pt1 = hyperbola(x-0.01)
            pt2 = hyperbola(x+0.01)
            
            slope = (pt2-pt1)/0.02

            frameline = Line(OG, ax.c2p(length*2, length*slope*2)).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())
            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Line(OG, OG+xpdir*frameline.get_length()).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            lightline = DashedLine(ax.c2p(x, hyperbola(x)), ax.c2p(x+length*2, hyperbola(x)+length*2)).set_color(lightcolor)

            return frameline
        
        def get_hypaxesx(x, x0=hypx0, length=1.2):
            pt1 = hyperbola(x-0.01)
            pt2 = hyperbola(x+0.01)
            
            slope = (pt2-pt1)/0.02

            frameline = Line(OG, ax.c2p(length*2, length*slope*2)).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())
            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Line(OG, OG+xpdir*frameline.get_length()).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            lightline = DashedLine(ax.c2p(x, hyperbola(x)), ax.c2p(x+length*2, hyperbola(x)+length*2)).set_color(lightcolor)

            return xpaxis
            
            
        # let's do this with a loop for more control! 
        N=30
        xs = np.linspace(hypx0, hypxf, N)
        ts = np.linspace(0,np.sqrt(hypxf**2 - hypx0**2), N)
        
        wldot = Dot().set_color(LemonOrange).move_to(worldline.get_start())

        self.play(Create(wldot))
        frametime=1
        self.play(self.camera.frame.animate.scale(0.7).move_to(wldot).shift(UP*2+RIGHT*1.5), run_time=2)

        tautracker = ValueTracker(0)
        taushow = always_redraw(lambda: MathTex(f"{tautracker.get_value()}"))
        self.play(Write(taushow))
        

        for tau in range(N):
            tautracker.add_updater(tautracker.set_value(tau))
            tpaxis = always_redraw(lambda: get_hypaxest(ax.p2c(wldot.get_center())[0]))
            xpaxis = always_redraw(lambda: get_hypaxesx(ax.p2c(wldot.get_center())[0]))
            if tau==0:
                    self.play(Create(xpaxis), Create(tpaxis))

            if tau==N-1:
                break
            hyptau = hyperbolapieceT(ts[tau], ts[tau+1], opacity=0)
            delt0 = ts[1]-ts[0]
            delt = ts[tau+1] - ts[tau]
            frametimei = frametime*(delt/delt0)**4  # start slow, get faster


            self.play(MoveAlongPath(wldot, hyptau), rate_func=linear, run_time=frametimei)
            

        self.wait(5)


# 0%
class Horizon(MovingCameraScene):
    def construct(self):
    # Chapters:
    # 1 - Show that the negative and positive hyperbolas asymptotes intersect on the x axis.
    # 2 - Show that all x' axes also intersect this point.
    # 3 - Show that this means the point is frozen in time for the accelerator.
    # 4 - 


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

        worldline = ax.plot(lambda x: hyperbola(x), x_range=[hypx0-center,hypxf-center,0.01]).set_color(NewOrange2)


        ###################################### Scenes ##############################################
        # 1 - Show that the negative and positive hyperbolas asymptotes intersect on the x axis.
        # 2 - Show that all x' axes also intersect this point.
        # 3 - Show that this means the point is frozen in time for the accelerator.
        # 4 - 
        ############# Chapter 1:
        ############# Chapter 2:
        ############# Chapter 3:
        ############# Chapter 4:
        ############# Chapter 5:


# 80%
class Geodesics(ThreeDScene):
    """Particles tracing same-radius free-fall paths around a massive body."""

    def construct(self):
        self.body_center = np.array([0.0, 0.0, -1.35])
        self.orbit_radius = 2.55

        self.set_camera_orientation(
            phi=64 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.86,
            focal_distance=7.0,
        )

        body = self.make_massive_body()
        shell = self.make_faint_shell()
        self.add(shell, body)
        self.begin_ambient_camera_rotation(rate=0.025)

        first_phase = self.play_random_shell_reveal()
        self.wait(0.35)
        self.play(
            *[FadeOut(mob, shift=0.12 * IN) for mob in first_phase],
            run_time=1.25,
            rate_func=smooth,
        )

        self.play_grid_reveal()
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

    def make_massive_body(self):
        glow = Sphere(radius=0.98, resolution=(32, 16))
        glow.move_to(self.body_center)
        glow.set_fill("#1d2b44", opacity=0.10)
        glow.set_stroke("#516d92", width=0.3, opacity=0.10)

        body = Sphere(radius=0.58, resolution=(48, 24))
        body.move_to(self.body_center)
        body.set_fill("#101828", opacity=1.0)
        body.set_stroke("#8ba4c7", width=0.4, opacity=0.35)

        inner_shadow = Sphere(radius=0.50, resolution=(32, 16))
        inner_shadow.move_to(self.body_center + 0.09 * IN + 0.08 * DOWN)
        inner_shadow.set_fill("#03050a", opacity=0.28)
        inner_shadow.set_stroke(opacity=0)

        return VGroup(glow, body, inner_shadow)

    def make_faint_shell(self):
        shell = Sphere(radius=self.orbit_radius, resolution=(36, 18))
        shell.move_to(self.body_center)
        shell.set_fill("#1f3448", opacity=0)
        shell.set_stroke("#3f536a", width=0.25, opacity=0)
        return shell

    def play_random_shell_reveal(self):
        colors = ["#6ee7ff", "#ffe66d", "#ff8fb3", "#9bff9b", "#c7a6ff"]
        starts_and_hints = [
            ([-0.88, -0.12, 0.45], [0.15, 0.96, 0.25]),
            ([0.54, -0.70, 0.47], [-0.87, 0.18, 0.34]),
            ([-0.28, 0.78, 0.56], [0.93, -0.10, 0.20]),
            ([0.86, 0.24, 0.45], [-0.22, -0.91, 0.30]),
            ([0.10, -0.93, 0.36], [0.74, 0.40, 0.53]),
        ]

        phase_mobjects = []
        sweep = 1.70
        run_time = 1.8

        for i, (start, hint) in enumerate(starts_and_hints):
            path_func = self.great_circle_path(start, hint, sweep=sweep)
            tracker, trail, particle = self.make_traced_particle(
                path_func,
                color=colors[i],
                stroke_width=5.0,
                particle_radius=0.065,
                max_points=90,
            )
            phase_mobjects.extend([trail, particle])
            self.add(trail, particle)
            self.play(
                tracker.animate.set_value(1.0),
                run_time=run_time,
                rate_func=linear,
            )
            trail.clear_updaters()
            particle.clear_updaters()
            self.play(FadeOut(particle, scale=0.8), run_time=0.22)
            phase_mobjects.remove(particle)

        return phase_mobjects

    def play_grid_reveal(self):
        horizontal_color = "#6ee7ff"
        vertical_color = "#ffda6b"
        latitudes = np.linspace(-0.68, 0.68, 10)
        longitudes = np.linspace(-0.94, 0.94, 10)

        horizontal = [
            self.make_traced_particle(
                self.latitude_path(lat),
                color=horizontal_color,
                stroke_width=3.2,
                particle_radius=0.045,
                max_points=58,
            )
            for lat in latitudes
        ]
        vertical = [
            self.make_traced_particle(
                self.longitude_path(lon),
                color=vertical_color,
                stroke_width=3.2,
                particle_radius=0.045,
                max_points=58,
            )
            for lon in longitudes
        ]

        trackers = []
        for left_to_right, bottom_to_top in zip(horizontal, vertical):
            for tracker, trail, particle in (left_to_right, bottom_to_top):
                trackers.append(tracker)
                self.add(trail, particle)

        self.play(
            LaggedStart(
                *[tracker.animate.set_value(1.0) for tracker in trackers],
                lag_ratio=0.035,
            ),
            run_time=7.2,
            rate_func=linear,
        )

        for _, trail, particle in horizontal + vertical:
            trail.clear_updaters()
            particle.clear_updaters()

        self.play(
            *[FadeOut(particle, scale=0.75) for _, _, particle in horizontal + vertical],
            run_time=0.55,
        )

        field_glow = VGroup(*[trail.copy().set_stroke(opacity=0.35) for _, trail, _ in horizontal + vertical])
        self.add(field_glow)
        self.play(
            field_glow.animate.set_opacity(0.72),
            run_time=0.8,
            rate_func=there_and_back,
        )

    def make_traced_particle(
        self,
        path_func,
        color,
        stroke_width=4.0,
        particle_radius=0.055,
        max_points=72,
    ):
        tracker = ValueTracker(0)

        trail = VMobject()
        trail.set_stroke(color=color, width=stroke_width, opacity=0.88)
        trail.set_points_as_corners([path_func(0), path_func(0)])

        particle = Dot3D(point=path_func(0), radius=particle_radius, color=color)

        def update_trail(mob):
            alpha = tracker.get_value()
            point_count = max(2, int(2 + max_points * alpha))
            points = [path_func(t) for t in np.linspace(0, alpha, point_count)]
            mob.set_points_smoothly(points)

        trail.add_updater(update_trail)
        particle.add_updater(lambda mob: mob.move_to(path_func(tracker.get_value())))
        return tracker, trail, particle

    def great_circle_path(self, start_vector, tangent_hint, sweep):
        start = self.unit(start_vector)
        tangent_hint = self.unit(tangent_hint)
        tangent = tangent_hint - np.dot(tangent_hint, start) * start
        tangent = self.unit(tangent)

        def path(alpha):
            angle = sweep * alpha
            local = np.cos(angle) * start + np.sin(angle) * tangent
            return self.body_center + self.orbit_radius * local

        return path

    def latitude_path(self, latitude):
        lon_min, lon_max = -1.08, 1.08

        def path(alpha):
            longitude = interpolate(lon_min, lon_max, alpha)
            return self.spherical_point(latitude, longitude)

        return path

    def longitude_path(self, longitude):
        lat_min, lat_max = -0.78, 0.78

        def path(alpha):
            latitude = interpolate(lat_min, lat_max, alpha)
            return self.spherical_point(latitude, longitude)

        return path

    def spherical_point(self, latitude, longitude):
        radius = self.orbit_radius
        return self.body_center + radius * np.array(
            [
                np.cos(latitude) * np.sin(longitude),
                np.sin(latitude),
                np.cos(latitude) * np.cos(longitude),
            ]
        )

    @staticmethod
    def unit(vector):
        vector = np.array(vector, dtype=float)
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("Cannot normalize a zero vector.")
        return vector / norm


