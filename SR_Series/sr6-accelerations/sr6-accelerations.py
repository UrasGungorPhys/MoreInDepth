from manim import *
import numpy as np
import math

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


import sympy as sp


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



# 10%
# Animations for SR and GR. After the geodesics scene is done, this shouldn't take long.
class Intro(MovingCameraScene):
    def construct(self):
        pass


# 0%
# This is like a bunch of writing on a blackboard, and should be easy.
class AccelerationsGravity(MovingCameraScene):
    def construct(self):
        pass


# 97.5%
# Fix the yellowed value tracker not moving
# Then it works, just some smoothing to do left!
# Smooth out the transition from rapid fire frames to the last frame.
class Cameramen(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BGBlue1
        # Background stars:
        stars = VGroup()
        for i in range(300):
            xs = np.random.uniform(-10,150)
            ys = np.random.uniform(-10,10)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)

        self.play(FadeIn(stars))

        
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


# 90%
# show the first MoveAlongPath once with just P(tau), then a second time with the clock added in.
class CameramenDiagram(MovingCameraScene):
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

        self.play(Create(ax), Create(xct), Write(ax_labels), run_time=1)

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

        
        
        self.play(Create(worldline))

        self.wait(2)

        def get_hypframe(x, x0=hypx0, length=1.2):
            pt1 = hyperbola(x-0.01)
            pt2 = hyperbola(x+0.01)
            
            slope = (pt2-pt1)/0.02

            frameline = Line(OG, ax.c2p(length*2, length*slope*2)).set_color(SchoolBus)
            frameline.move_to(ax.c2p(x, hyperbola(x))).scale(length*2/frameline.get_length())
            return frameline
            
        
        

        wldot = Dot().set_color(LemonOrange).move_to(worldline.get_start())
        tautracker = ValueTracker(0)  # proper time along the particles worldline. Let's add the updaters:

        from scipy.integrate import quad
        def arc_length(xx, x0=hypx0):
            # integrand: sqrt(1 + (dy/dx)^2)
            integrand = lambda x: np.sqrt(1 + (2*x)**2)  # get arc length of hyperbola
            L, _ = quad(integrand, x0, xx)
            return L
        
        total_arc_length = arc_length(10)


        def makeclock(time, scale):

            clockscale = scale
            clockimg = ImageMobject("clock.png").scale(clockscale)
            clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Samoyed).move_to(clockimg.get_center()).scale(clockscale*0.9))
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


        self.play(Create(wldot))

        clockbg = always_redraw(lambda: Circle(radius=3, fill_opacity=1).set_color(Vanilla).scale(0.14).move_to(wldot).shift(LEFT*0.5+UP*0.4))
        clockcenter = always_redraw(lambda:Dot(clockbg.get_center()).set_color(BLACK).scale(1.4).scale(0.1))
        clock = VGroup(clockbg, clockcenter)
        # clock8 = makeclock(8,0.1)
        # clock3 = makeclock(3,0.1)
        # clock6 = makeclock(6,0.1)

        clock0 = makeclock(0, 0.14).move_to(clock.get_center()).set_z_index(1)
        

        def update_tautracker(tracker):
            xi = ax.p2c(wldot.get_center())[0]  # x coord of wldot in the ax coordinates.
            tau_i = arc_length(xi)/total_arc_length * 10  # want the full arc to be 10 units
            tracker.set_value(tau_i)
        
        tautracker.add_updater(update_tautracker)

        Ptau = always_redraw(lambda: MathTex("P(", f"{tautracker.get_value():.1f}", ")").move_to(ax.x_axis.get_center()).shift(UP*0.5+RIGHT))

        self.add(tautracker)
        self.add(Ptau)
        self.wait(2)
        self.play(MoveAlongPath(wldot, worldline, rate_func=linear), run_time=8)

        self.wait(5)

        self.play(MoveAlongPath(wldot, worldline, rate_func=lambda t:1-t), run_time=0.5)

        self.wait(2)

        Ptaunrd = MathTex("P(", f"{tautracker.get_value():.1f}", ")").move_to(ax.x_axis.get_center()).shift(UP*0.5+RIGHT)
        self.add(Ptaunrd)
        self.remove(Ptau)

        Ptau = always_redraw(lambda: MathTex("P(", r"\tau", f"= {tautracker.get_value():.1f}", ")").move_to(ax.x_axis.get_center()).shift(UP*0.5+RIGHT))
        propertime = Text("Proper Time").move_to(Ptau.get_center()).shift(UP*0.5)

        self.play(ReplacementTransform(Ptaunrd, Ptau))
        self.wait()
        self.play(Write(propertime))

        self.play(FadeIn(clock0))
        self.add(clock)
        self.wait(2)
        self.play(FadeOut(propertime))

        self.wait(2)
        self.remove(clock0)

        self.play(MoveAlongPath(wldot, worldline, rate_func=linear), run_time=8)

        self.wait(3)
        self.play(MoveAlongPath(wldot, worldline, rate_func=lambda t:1-t), run_time=0.5)
        self.play(FadeOut(clock))

   

        # let's do this with a loop for more control! 
        N=15
        xs = np.linspace(hypx0, hypxf, N)
        ts = np.linspace(0,np.sqrt(hypxf**2 - hypx0**2), N)
        
        # wldot = Dot().set_color(LemonOrange).move_to(worldline.get_start())
        # self.play(Create(wldot))
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
                tauline = get_hypframe(ax.p2c(wldot.get_center())[0])
                self.play(Create(tauline),run_time=1)
                self.wait()
                self.play(FadeOut(tauline), run_time=0.5)


            if tau == 5:
                tauline = get_hypframe(ax.p2c(wldot.get_center())[0])
                self.play(Create(tauline),run_time=1)
                self.wait()
                self.play(FadeOut(tauline), run_time=0.5)
            

            if tau>N/3 and tau%2==0:

                if tau == 8:
                    tauline = get_hypframe(ax.p2c(wldot.get_center())[0])
                    self.play(Create(tauline),run_time=1)
                    self.wait()
                    self.play(FadeOut(tauline), run_time=0.5)

                if tau == 12:
                    tauline = get_hypframe(ax.p2c(wldot.get_center())[0])
                    self.play(Create(tauline),run_time=1)
                    self.wait()
                    self.play(FadeOut(tauline), run_time=0.5)

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
# Show two rockets accelerating side by side, should be a simple one.
# Perhaps then show as the concluding scene, how one rocket seems to accelerate faster as seen by the other,
# due to the loss of simultaneity.
class TwoAcceleratedRockets(MovingCameraScene):
    def construct(self):
        pass


# 70%
# Show how simultaneity breaks right away, and show where the two observe eachother on their worldlines
# But does the front rocket agree with this? Show that it also sees the rear one slower, or rather further in the past.
class TwoAcceleratedObservers(MovingCameraScene):
    
    def construct(self):
        self.camera.background_color = BGBlue1

        ax = Axes(x_range=[0,15,1], y_range=[0,15,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)
        xct1 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(9.5,9.5)).set_color(lightcolor).set_opacity(0.5)
        # xct2 = DashedLine(start=ax.c2p(-9.5,9.5), end=ax.c2p(9.5,-9.5)).set_color(lightcolor).set_opacity(0.5)
        OG=ax.c2p(0,0)


        def hyperbolapiece(hyperbola, x1, x2, opacity=0):
            wlpiece = ax.plot(hyperbola, x_range=[x1, x2, 0.001]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
        
        def get_hypaxest(hyperbola, mobject, x0, length=1.2):
            x = ax.p2c(mobject.get_center())[0]
            y = ax.p2c(mobject.get_center())[1]

            if x<=x0:

                frameline = Line(OG, OG+UP*length).set_color(LightBlue)
                frameline.move_to(ax.c2p(x, y)).scale(length*2/frameline.get_length())
                # top part won't work if you shift hyperbola up!
                frameline.shift(frameline.get_center() - frameline.get_start())
                return frameline
            
            # elif x0<x<x0+0.1:

            
            else:
                pt1 = hyperbola(x)
                pt2 = hyperbola(x+0.001)
                
                slope = (pt2-pt1)/0.001

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
            
        
        def get_hypaxesx(hyperbola, mobject, x0, length=1.2):
            x = ax.p2c(mobject.get_center())[0]
            y = ax.p2c(mobject.get_center())[1]
            if x<=x0:

                frameline = Line(OG, OG+UP*length).set_color(LightBlue)
                frameline.move_to(ax.c2p(x, y)).scale(length*2/frameline.get_length())
                frameline.shift(frameline.get_center() - frameline.get_start())
                xpaxis = Line(OG, OG+RIGHT*length*2).set_color(LightBlue)

                xpaxis.move_to(ax.c2p(x, y)).scale(length*2/frameline.get_length())
                xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())
                return xpaxis

            else:

                pt1 = hyperbola(x)
                pt2 = hyperbola(x+0.001)
                
                slope = (pt2-pt1)/0.001
                

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
        

        hypf1 = lambda x: np.sqrt(x**2 - 3**2)
        hypf2 = lambda x: np.sqrt((x-5)**2 - 3**2)

        hyp1 = ax.plot(hypf1, x_range=[3,9.5,0.1])
        hyp2 = ax.plot(hypf2, x_range=[8,14.5,0.1])

        self.play(Create(ax), Create(xct1))
        self.play(Create(hyp1), Create(hyp2))
        self.wait(2)
        acc1 = Dot(hyp1.get_start())
        acc2 = Dot(hyp2.get_start())

        self.play(Create(acc1))
        self.play(Create(acc2))


        xax1 = always_redraw(lambda: get_hypaxesx(hypf1, acc1, 3))
        tax1 = always_redraw(lambda: get_hypaxest(hypf1, acc1, 3))

        xax2 = always_redraw(lambda: get_hypaxesx(hypf2, acc2, 8))
        tax2 = always_redraw(lambda: get_hypaxest(hypf2, acc2, 8))

        self.play(Create(xax1), Create(tax1), Create(xax2), Create(tax2))


        self.play(MoveAlongPath(acc1, hyp1), MoveAlongPath(acc2, hyp2), run_time=10, rate_func=linear)

        self.wait(3)
        self.play(FadeOut(*[xax1, tax1, xax2, tax2]), self.camera.frame.animate.move_to(hyp1.get_start()).shift(UP*2+RIGHT).scale(0.7))
        self.remove(*[xax1, tax1, xax2, tax2])
        self.play(MoveAlongPath(acc1, hyp1), MoveAlongPath(acc2, hyp2), run_time=0.5, rate_func=lambda t:1-t)
        self.wait(2)

        xax1 = always_redraw(lambda: get_hypaxesx(hypf1, acc1, 3, length=2))
        self.play(Create(xax1))

        ph1 = hyperbolapiece(hypf1, 3, 3.05)
        ph2 = hyperbolapiece(hypf1, 3.05, 3.2)
        ph3 = hyperbolapiece(hypf1, 3.2, 3.7)
        ph4 = hyperbolapiece(hypf1, 3.7, 10)
        
        
        # print(ax.c2p(* line_function_intersection(xax1, lambda x: sp.sqrt((x-5)**2 - 3**2), ax)))
        d1 = always_redraw(lambda: Dot(ax.c2p(*line_function_intersection(xax1, lambda x: sp.sqrt((x-5)**2 - 3**2), ax)[0])))

        self.play(Create(d1))

        self.play(MoveAlongPath(acc1, ph1), run_time=6)
        self.wait(3)
        self.play(MoveAlongPath(acc1, ph2), run_time=4, rate_func=linear)
        self.wait()
        self.play(MoveAlongPath(acc1, ph3), run_time=4, rate_func=linear)
        self.wait()
        self.play(MoveAlongPath(acc1, ph4), run_time=6, rate_func=linear)

        
        # self.play(Create(Dot(ax.c2p(*d1[1]))))

        self.wait(5)


# 80%
# Why the heck do the axes open back up like that?! 
class OverlapProblem1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BGBlue1

        acchyp = lambda x : np.sqrt((x+6)**2 - 6**2)+3

        def get_hypaxest(x, x0=6.0, length=1.2):
            pt1 = acchyp(np.clip(x-0.01, 0.00, 1000))
            pt2 = acchyp(np.clip(x, 0.01, 1000)+0.01)
            
            slope = (pt2-pt1)/0.02

            frameline = Arrow(OG, ax.c2p(length*2, length*slope*2), buff=0).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())
            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Line(OG, OG+xpdir*frameline.get_length()).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())


            return frameline
        

        def get_hypaxesx(x, x0=6, length=1.2):
            pt1 = acchyp(np.clip(x-0.01, 0.01, 1000))
            pt2 = acchyp(np.clip(x, 0.01, 1000)+0.01)

            
            slope = (pt2-pt1)/0.02

            frameline = Line(OG, ax.c2p(length*2, length*slope*2)).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())

            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Arrow(OG, OG+xpdir*frameline.get_length(), buff=0).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            return xpaxis
        
        

        ax = Axes(x_range=[0,20,1], y_range=[0,20,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)
        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(20-0.2,20-0.2)).set_color(lightcolor).set_opacity(0.5)
        OG=ax.c2p(0,0)

        wl1 = Line(ax.c2p(0,-1), ax.c2p(0,3), stroke_width=6).set_color(MistyBlue)

        accx = 2
        acchyp = lambda x : np.sqrt((x+6)**2 - 6**2)+3
        accwl = ax.plot(acchyp, x_range=[0,accx,0.01], stroke_width=6).set_color(NewOrange1)

        lastpiece = Line(ax.c2p(accx-0.01, acchyp(accx-0.01)),ax.c2p(accx, acchyp(accx))).set_color(OrangeOrange)
        wl2slope = glslope(lastpiece)
        accwlend = ax.p2c(accwl.get_end())


        wl2 = Line(accwl.get_end(), ax.c2p(accwlend[0]+6, 6*wl2slope+accwlend[1]), stroke_width=6).set_color(LemonOrange)
        
        wl2tphat = np.array([wl2slope, 1, 0])
        wl2xphat = np.array([1, wl2slope, 0])

        def hyperbolapieceT(t1, t2, opacity=0, x0=6, const=3):
            #t = sqrt((x+x0)**2 - x0**2)+const
            x1 = np.sqrt((t1-const)**2 +x0**2) - x0
            x2 = np.sqrt((t2-const)**2 +x0**2) - x0

            wlpiece = ax.plot(lambda x : np.sqrt((x+6)**2 - 6**2)+3, x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece


        self.play(Create(ax), Create(xct))
        self.play(Write(ax_labels))
        self.play(Create(wl1))
        self.play(Create(accwl))
        self.play(Create(wl2))
        
        wldot = Dot(wl1.get_start())
        
        tpaxis0=Arrow(wldot.get_center(), wldot.get_center()+UP*2.4)
        tpaxis1 = always_redraw(lambda: Arrow(wldot.get_center(), wldot.get_center()+UP*2.4, buff=0
                                              ).set_color(LightBlue))
        xpaxis1 = always_redraw(lambda: Arrow(wldot.get_center(), wldot.get_center()+RIGHT*2.4, buff=0
                                              ).set_color(LightBlue))


        self.play(Create(wldot))
        self.wait()
        self.play(Create(tpaxis1), Create(xpaxis1))
        
        self.play(MoveAlongPath(wldot, wl1), rate_func=linear, run_time=2.5)
        
        tpaxisA0 = get_hypaxest(ax.p2c(wldot.get_center())[0]).set_opacity(0)
        tpaxisA = always_redraw(lambda: get_hypaxest(ax.p2c(wldot.get_center())[0]))
        xpaxisA = always_redraw(lambda: get_hypaxesx(ax.p2c(wldot.get_center())[0]))

        self.play(ReplacementTransform(tpaxis1, tpaxisA), ReplacementTransform(xpaxis1, xpaxisA), run_time=0.5)
        
        self.play(MoveAlongPath(wldot, accwl), rate_func=linear, run_time=4)

        tpaxis20 = get_hypaxest(ax.p2c(wldot.get_center())[0]).copy()
        
        xpaxis20 = get_hypaxesx(ax.p2c(wldot.get_center())[0]).copy()

        tpaxis2 = always_redraw(lambda: tpaxis20.move_to(wldot.get_center()).shift(tpaxis20.get_unit_vector()*tpaxis20.get_length()/2))
        xpaxis2 = always_redraw(lambda: xpaxis20.move_to(wldot.get_center()).shift(xpaxis20.get_unit_vector()*xpaxis20.get_length()/2))
        self.remove(*[tpaxisA, xpaxisA])
        self.add(tpaxis2, xpaxis2)

        # tpaxis2 = always_redraw(lambda:Arrow(wldot.get_center(), wldot.get_center()+wl2tphat*2, buff=0))
        # xpaxis2 = always_redraw(lambda:Arrow(wldot.get_center(), wldot.get_center()+wl2xphat*2, buff=0))
        # or try moving the old axes along with wldot since they don't change anymore
        self.play(MoveAlongPath(wldot, wl2, rate_func=linear, run_time=3))
        self.wait(5)


# 75%
# Get to the actual lesson in overlap.
class OverlapProblem2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BGBlue1

        acchyp = lambda x : np.sqrt((x+6)**2 - 6**2)+3

        def get_hypaxest(x, x0=6.0, length=1.2):
            pt1 = acchyp(np.clip(x-0.01, 0.00, 1000))
            pt2 = acchyp(np.clip(x+0.01, 0.02, 1000))
            
            slope = (pt2-pt1)/0.02

            frameline = Arrow(OG, ax.c2p(length*2, length*slope*2), buff=0).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())
            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Line(OG, OG+xpdir*frameline.get_length()).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            return frameline
        

        def get_hypaxesx(x, x0=6, length=1.2):
            pt1 = acchyp(np.clip(x-0.01, 0.01, 1000))
            pt2 = acchyp(np.clip(x, 0.01, 1000)+0.01)

            
            slope = (pt2-pt1)/0.02

            frameline = Line(OG, ax.c2p(length*2, length*slope*2)).set_color(LightBlue)
            frameline.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            frameline.shift(frameline.get_center() - frameline.get_start())

            tpdir = np.array([1, 1*slope, 0])/np.linalg.norm(np.array([1, 1*slope, 0]))
            xpdir = np.array([1*slope, 1, 0])/np.linalg.norm(np.array([1*slope, 1, 0]))

            xpaxis = Arrow(OG, OG+xpdir*frameline.get_length(), buff=0).set_color(LightBlue)

            xpaxis.move_to(ax.c2p(x, acchyp(x))).scale(length*2/frameline.get_length())
            xpaxis.shift(xpaxis.get_center() - xpaxis.get_start())

            return xpaxis
        

        ax = Axes(x_range=[0,20,1], y_range=[0,20,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)
        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(18-0.2,18-0.2)).set_color(lightcolor).set_opacity(0.5)
        OG=ax.c2p(0,0)

        wl1 = Line(ax.c2p(0,0), ax.c2p(0,3), stroke_width=8).set_color(MistyBlue)

        accx = 2
        acchyp = lambda x : np.sqrt((x+6)**2 - 6**2)+3
        accwl = ax.plot(acchyp, x_range=[0,accx,0.01], stroke_width=8).set_color(NewOrange1)

        lastpiece = Line(ax.c2p(accx-0.01, acchyp(accx-0.01)),ax.c2p(accx, acchyp(accx))).set_color(OrangeOrange)
        wl2slope = glslope(lastpiece)
        accwlend = ax.p2c(accwl.get_end())

        wl2 = Line(accwl.get_end(), ax.c2p(accwlend[0]+6, 6*wl2slope+accwlend[1]), stroke_width=8).set_color(LemonOrange)
        
        wl2tphat = np.array([wl2slope, 1, 0])
        wl2xphat = np.array([1, wl2slope, 0])

        def hyperbolapieceT(t1, t2, opacity=0, x0=6, const=3):
            #t = sqrt((x+x0)**2 - x0**2)+const
            x1 = np.sqrt((t1-const)**2 +x0**2) - x0
            x2 = np.sqrt((t2-const)**2 +x0**2) - x0

            wlpiece = ax.plot(lambda x : np.sqrt((x+6)**2 - 6**2)+3, x_range=[x1, x2, 0.01]).set_opacity(opacity).set_color(SchoolBus)
            return wlpiece
 

        def get_grids(xhat, that, gdog, whichax, N=10, spacing_ratio=1, length=5, opacity=0.7, color=NewOrange1):

            manual_grids0x = VGroup()
            manual_grids0t = VGroup()

            for ii in range(1,N):
                i=ii*spacing_ratio

                xline = Line(start=gdog + i*that - length*xhat - length*that,
                            end=gdog + i*that + length*xhat- length*that, buff=0,
                            stroke_color=color, stroke_opacity=opacity,stroke_width=2)

                tline = Line(start=gdog + i*xhat - length*that - length*xhat,
                            end=gdog + i*xhat + length*that- length*xhat, buff=0,
                            stroke_color=color, stroke_opacity=opacity,stroke_width=2)
                
                manual_grids0x.add(xline)
                manual_grids0t.add(tline)

            if whichax==0:
                return manual_grids0x
            if whichax==1:
                return manual_grids0t
                

        # Let's get grids


        self.play(Create(ax), Create(xct))
        self.play(Write(ax_labels))
        self.play(Create(wl1))
        self.play(Create(accwl))
        self.play(Create(wl2))
        self.wait()
        self.play(xct.animate.set_opacity(0.3), ax.animate.set_opacity(0.2), run_time=2)

        # wl1
        wldot = Dot(wl1.get_start())


        tpaxis0=Arrow(wldot.get_center(), wldot.get_center()+UP*2.4)
        tpaxis1 = always_redraw(lambda: Arrow(wldot.get_center(), wldot.get_center()+UP*2.4, buff=0
                                              ).set_color(LightBlue))
        xpaxis1 = always_redraw(lambda: Arrow(wldot.get_center(), wldot.get_center()+RIGHT*2.4, buff=0
                                              ).set_color(LightBlue))


        tphat1 = tpaxis1.get_unit_vector()
        xphat1 = xpaxis1.get_unit_vector()

        wl1xgrids = always_redraw(lambda: get_grids(xphat1, tphat1, wldot.get_center(), whichax=0))
        wl1tgrids = always_redraw(lambda: get_grids(xphat1, tphat1, wldot.get_center(), whichax=1))

        self.play(Create(wldot))
        self.wait()
        self.play(Create(tpaxis1), Create(xpaxis1))
        self.play(Create(wl1xgrids), Create(wl1tgrids))
        
        self.play(MoveAlongPath(wldot, wl1), rate_func=linear, run_time=2.5)
        

        # accelerated wl

        tpaxisA = always_redraw(lambda: get_hypaxest(ax.p2c(wldot.get_center())[0]))
        xpaxisA = always_redraw(lambda: get_hypaxesx(ax.p2c(wldot.get_center())[0]))

        acctphat = always_redraw(lambda: get_hypaxest(ax.p2c(wldot.get_center())[0])).get_unit_vector()
        accxphat = always_redraw(lambda: get_hypaxesx(ax.p2c(wldot.get_center())[0])).get_unit_vector()    
        # get_hypaxest(ax.p2c(wldot.get_center())[0])
        

        accxgrids = always_redraw(lambda: get_grids(
            get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.8/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), 
            get_hypaxest(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.8/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), wldot.get_center(), whichax=0, N=10, spacing_ratio=1, length=5))


        # acctgrids = always_redraw(lambda: get_grids(
        #     get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector(), 
        #     get_hypaxest(ax.p2c(wldot.get_center())[0]).get_vector(), 
        #     wldot.get_center(), whichax=1, N=10, spacing_ratio=1, length=5))

        acctgrids = always_redraw(lambda: get_grids(
            get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.8/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), 
            get_hypaxest(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.8/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), wldot.get_center(), whichax=1, N=10, spacing_ratio=1, length=5))
        # that's the most disgusting code I've ever spawned into this world

        self.play(FadeOut(*[wl1xgrids, wl1tgrids, tpaxis1, xpaxis1]))
        self.remove(*[wl1xgrids, wl1tgrids, tpaxis1, xpaxis1])

        self.play(Create(tpaxisA), Create(xpaxisA))
        self.play(Create(accxgrids), Create(acctgrids))

        self.play(MoveAlongPath(wldot, accwl), rate_func=linear, run_time=6)
        
        # wl2

        tpaxis20 = get_hypaxest(ax.p2c(wldot.get_center())[0]).copy()
        
        xpaxis20 = get_hypaxesx(ax.p2c(wldot.get_center())[0]).copy()

        tpaxis2 = always_redraw(lambda: tpaxis20.move_to(wldot.get_center()).shift(tpaxis20.get_unit_vector()*tpaxis20.get_length()/2))
        xpaxis2 = always_redraw(lambda: xpaxis20.move_to(wldot.get_center()).shift(xpaxis20.get_unit_vector()*xpaxis20.get_length()/2))
        self.remove(*[tpaxisA, xpaxisA])
        self.add(tpaxis2, xpaxis2)

        accxgrids0 = get_grids(
            get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.6/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), 
            get_hypaxest(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.6/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), wldot.get_center(), whichax=0, N=10, spacing_ratio=1, length=5).copy()

        acctgrids0 = get_grids(
            get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.6/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), 
            get_hypaxest(ax.p2c(wldot.get_center())[0]).get_vector(
            )*(1/(np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())/(
                  np.linalg.norm(wldot.get_center()-accwl.get_end())/np.linalg.norm(accwl.get_start() - accwl.get_end())
                  +np.linalg.norm(get_hypaxesx(ax.p2c(wldot.get_center())[0]).get_vector())*(
                    np.linalg.norm(wldot.get_center()-accwl.get_start())*0.6/np.linalg.norm(accwl.get_start() - accwl.get_end()))
                  ))), wldot.get_center(), whichax=1, N=10, spacing_ratio=1, length=5).copy()
        

        wl2xgrids = always_redraw(lambda: accxgrids0.move_to(wldot.get_center()).set_color(Vanilla))
        wl2tgrids = always_redraw(lambda: acctgrids0.move_to(wldot.get_center()).set_color(Vanilla))
        

        self.play(FadeOut(*[accxgrids, acctgrids]))
        self.remove(*[accxgrids, acctgrids])
        self.play(FadeIn(*[wl2xgrids, wl2tgrids]))

        self.play(MoveAlongPath(wldot, wl2), run_time=3.5)

        self.wait(2)
        self.play(FadeOut(*[wldot, wl2xgrids, wl2tgrids, tpaxis2, xpaxis2]))

        # the overlap region

        def get_gridsSP(xhat, that, gdog, whichax, N=10, spacing_ratio=1/2, length=2.5, opacity=0.7, color=NewOrange1):

            manual_grids0x = VGroup()
            manual_grids0t = VGroup()

            for ii in range(1,N):
                i=ii*spacing_ratio

                if ii%2 ==0:
                    xline = Line(start=gdog + i/2*that - length*xhat,
                                end=gdog + i/2*that + length*xhat, buff=0,
                                stroke_color=color, stroke_opacity=opacity,stroke_width=2)
                    
                    manual_grids0x.add(xline)

                tline = Line(start=gdog + i*xhat - length*xhat,
                            end=gdog + i*xhat + length*that- length*xhat, buff=0,
                            stroke_color=color, stroke_opacity=opacity,stroke_width=2)
                
                
                manual_grids0t.add(tline)

            if whichax==0:
                return manual_grids0x
            if whichax==1:
                return manual_grids0t
            

        def get_gridsSP2(xhat, that, gdog, whichax, N=10, spacing_ratio=1/2, length=1.5, opacity=0.7, color=NewOrange1):

            manual_grids0x = VGroup()
            manual_grids0t = VGroup()

            for ii in range(1,N):
                i=ii*spacing_ratio

                if ii%2 ==0:
                    xline = Line(start=gdog + i/1.8*that - length*2*xhat,
                                end=gdog + i/1.8*that + length*xhat/3, buff=0,
                                stroke_color=color, stroke_opacity=opacity,stroke_width=2)
                    
                    manual_grids0x.add(xline)

                tline = Line(start=gdog + i*xhat - length*2*xhat,
                            end=gdog + i*xhat + length*that- length*2*xhat, buff=0,
                            stroke_color=color, stroke_opacity=opacity,stroke_width=2)
                
                
                manual_grids0t.add(tline)

            if whichax==0:
                return manual_grids0x
            if whichax==1:
                return manual_grids0t
            

        compgrids1x = get_gridsSP(xphat1, tphat1, OG, whichax=0)
        compgrids1t = get_gridsSP(xphat1, tphat1, OG, whichax=1)

        compgrids2x = get_gridsSP2(get_hypaxesx(ax.p2c(wl2.get_start())[0]).get_vector(),
                                get_hypaxest(ax.p2c(wl2.get_start())[0]).get_vector(), wl2.get_start(),
                                  whichax=0, color=Vanilla, spacing_ratio=1/3.6)
        

        compgrids2t = get_gridsSP2(get_hypaxesx(ax.p2c(wl2.get_start())[0]).get_vector(), 
                                get_hypaxest(ax.p2c(wl2.get_start())[0]).get_vector(), wl2.get_start(), 
                                whichax=1, color=Vanilla, spacing_ratio=1/3.6)


        xax = Arrow(OG+DOWN*2.4, OG+UP*2.4, buff=0).set_color(NewOrange1)
        tax = Arrow(OG+LEFT*2.4, OG+RIGHT*2.4, buff=0).set_color(NewOrange1)

        xpax = Arrow(wl2.get_start()-wl2tphat*3, wl2.get_start()+wl2tphat*3, buff=0).set_color(Vanilla)
        tpax = Arrow(wl2.get_start()-wl2xphat*3, wl2.get_start()+wl2xphat*3, buff=0).set_color(Vanilla)

        self.play(Create(xax), Create(tax))
        self.play(Create(xpax), Create(tpax))

        self.play(FadeIn(*[compgrids1x, compgrids1t]))
        self.play(FadeIn(*[compgrids2x, compgrids2t]))

        self.wait(3)


# 35%
# Lightcones, accelerated worldline, illustrate the impossibility of causal relationships etc.
class LightconeLimit(MovingCameraScene):
    def construct(self):
        ax = Axes(x_range=[-7,7,1], y_range=[-4,4,1], 
        x_length=14, y_length=8,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        self.camera.frame.scale(1.2)
        ax.move_to(ORIGIN)

        # rewriting hypax function for practice:

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

        self.play(Create(ax))
        self.play(Create(hypm))
        self.play(Create(hypp))
        # self.play(Create(xct1), Create(xct2))

        self.play(Create(acc))
        self.play(Create(xctp), Create(xctm))
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


# 15%
# Walk through the problem step by step by showing lines of simultaneity and time dilation at all points.
class TwinsParadox(MovingCameraScene):
    def construct(self):
        ax = Axes(x_range=[0,20,1], y_range=[0,20,1], 
        x_length=6, y_length=6,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t").set_color(gndcolor1)
        xct1 = DashedLine(start=ax.c2p(-9.5,-9.5), end=ax.c2p(9.5,9.5)).set_color(lightcolor).set_opacity(0.5)
        xct2 = DashedLine(start=ax.c2p(-9.5,9.5), end=ax.c2p(9.5,-9.5)).set_color(lightcolor).set_opacity(0.5)
        OG=ax.c2p(0,0)

        # hypm = ax.plot(lambda x: -np.sqrt(x**2 - 3**2), x_range=[3,9.5,0.1])
        # hypp = ax.plot(lambda x: np.sqrt(x**2 - 3**2), x_range=[3,9.5,0.1])

        twinline1 = Line(OG, ax.c2p(10,10))
        twinline2 = Line(twinline1.get_end(), ax.c2p(0,20))
        twinline22 = Line(ax.c2p(0,20), twinline1.get_end())
        
        twinhyp1 = ax.plot(lambda x: np.sqrt((x-10)**2 - 1**2)+10, x_range=[0,9,0.1])
        twinhyp2 = ax.plot(lambda x: -np.sqrt((x-10)**2 - 1**2)+10, x_range=[0,9,0.1])


        self.play(Create(ax))
        self.play(Create(twinline1), Create(twinline2))
        self.wait()
        self.add(twinline22)
        self.remove(twinline2)
        
        self.play(ReplacementTransform(twinline22, twinhyp1), ReplacementTransform(twinline1, twinhyp2))
        self.wait(5)


# 0%
# See how gravity and acceleration cancel out, hinting at a fundamental equivalence
class EquivalencePrinciple(MovingCameraScene):
    def construct(self):
        pass


# 63%
# Well this one is tough. Takes so long to render.
# Need to draw a nice curved manifold on top of a sphere using an N body simultaion, by tracing the paths of test particles.
# Make them criss cross eachother to get a curved coordinate grid.
# Find a good camera angle later.
class Geodesics(ThreeDScene):
    def construct(self):
        self.renderer.camera.is_perspective = False
        self.camera.set_zoom(0.5)
        # self.set_camera_orientation(theta=PI/4)
        # self.set_camera_orientation(phi=PI/2)

        # self.move_camera(phi=30*DEGREES, distance=10)
        ax = ThreeDAxes(
            x_range=(-10,10,5),
            y_range=(-10,10,5),
            z_range=(0,10,5)
        )
        ax.center()
        axlabels = ax.get_axis_labels(x_label="x", y_label="y", z_label="z")
        self.play(Create(ax))
        self.play(Write(axlabels))
        # self.begin_ambient_camera_rotation(rate=0.1)

        y_layers = 1
        results = []
        particle_per_y = 11
        mass_pos = np.array([3,-1/2,3])


        def get_those_damn_points(masspos, p0, d_angle, howmanyoneachside, vzorvx):


            theline = Line(masspos, p0).set_opacity(0)
            linevec = theline.get_vector()

            if vzorvx == 0:
                v0 = np.array([0,0,1.5])
                rotationline = np.array([linevec[0], -linevec[2], linevec[1]]) # this is certainly not gonna be general
                  

            if vzorvx == 1:
                v0 = np.array([1.5, 0,0])

                rotationline = np.array([linevec[1], -linevec[0], linevec[2]]) # this is certainly not gonna be general
                

            # print("RL1", rotationline)
            # self.play(Create(theline))
            # self.play(Create(Line(theline.get_start(), theline.get_start()+rotationline*3).set_color(Greenough)))
            pts = [p0]
            vs = [theline.get_unit_vector()/10 + v0]
            for i in range(howmanyoneachside):
                theline.rotate(-d_angle, axis=rotationline, about_point=theline.get_start())
                
                pti = theline.get_end()
                pts.append(pti)
                vzi = theline.get_unit_vector()/10 + v0
                vs.append(vzi)
            

            # theline.rotate(-d_angle*howmanyoneachside, axis=rotationline, about_point=theline.get_start())
            theline = Line(masspos, p0).set_opacity(0)
            # to reset the line to its initial angle.


            for i in range(howmanyoneachside):
                theline.rotate(d_angle, axis=rotationline, about_point=theline.get_start())
                pti = theline.get_end()
                pts.append(pti)
                vzi = theline.get_unit_vector()/10 + v0
                vs.append(vzi)
                

            return pts, vs
        
        ##################### Starting the Nbody sim for geodesics #################################
        particlesN = 11  # there will be x2 these for two sides of square in total
        T = 70
        N=500
        dt = T/N
        
        left_right_particles = int(np.floor(particlesN/2))  # for 11, we get 5 per side + one in the middle

        positions0, vzs = get_those_damn_points(np.array([3,-1/2,3]), np.array([3, 3,-2]), PI/20, left_right_particles, 0)
        positions111, vxs = get_those_damn_points(np.array([3,-1/2,3]), np.array([-2, 3,3]), PI/20, left_right_particles, 1)

        positions1 = []
        for ps in positions0:
            adjust = np.array([-0.53553391,  1.97487373, -1.31566913])
            adjx = -(1.31566913 -0.53553391)
            adjz = (1.31566913 -0.53553391)
            ps1 = np.array([ps[2]+adjx, ps[1], ps[0]+adjz])
            positions1.append(ps1)


        print(f"######## positions0:\n{positions0}")
        print(f"\n\n######## positions1:\n{positions1}")
        
        
        self.play(Create(Dot(mass_pos, radius=1)))

        self.play(Create(Dot(np.array([3, 3,-2]))))
        self.play(Create(Dot(np.array([-2, 3,3])).set_color(Greenough)))


        self.play(Create(Line(np.array([3,-1/2,3]), np.array([3, 3,-2]))))

        self.play(Create(Line(mass_pos, np.array([3, 3,-2]))))
        self.play(Create(Line(mass_pos, np.array([-2, 3,3])).set_color(Greenough)))

        self.wait(5)

        for p in positions0:
            self.play(Create(Dot(p)))

        for p in positions1:
            self.play(Create(Dot(p).set_color(Greenough)))


        both_results = []
        for ii in range(2):
            initial_positions = [positions0, positions1][ii]
            velocities = [vzs, vxs][ii]
            # velocities = [np.array([0,0,1.5]) , np.array([1.5,0,0])]

            results = []
            for p in range(len(initial_positions)):
                positions = np.array([initial_positions[p]])  # start sim with this particles initial position
                m=1
                mv = velocities[p]
                # mv = np.array([0, 0, 2.0])
                M=4
                for t in range(T):
                    # print("\n\n",t)
                    # print(positions)
                    xi0 = positions[t][0]
                    yi0 = positions[t][1]
                    zi0 = positions[t][2]

                    r = mass_pos - positions[t]
                    F = m*M*r / np.linalg.norm(r)**3

                    mv += F*dt

                    xi = xi0 + mv[0]*dt
                    yi = yi0 + mv[1]*dt
                    zi = zi0 + mv[2]*dt

                    
                    newpos = np.array([xi, yi, zi])
                    positions = np.vstack([positions, newpos])

                results.append(positions)  # append the resulting positions vector for particle p for all t's 

            both_results.append(results)

        results1 = both_results[0]
        results2 = both_results[1]

        # self.play(Create(Dot(np.array([3,3,4])).set_color(Greenough)))
        
        # self.play(Create(Sphere(radius=1.7, resolution=(32, 32)).move_to(mass_pos)))


        geodesics = []
        for p in range(particlesN):

            vec_ylayeri_pi = results1[p]
            # print(vec_ylayeri_pi)
            

            path_ylayeri_pi = VMobject().set_points_as_corners(vec_ylayeri_pi)
            geodesics.append(path_ylayeri_pi)

        geodesicsgp = VGroup(*geodesics)
        self.play(Create(geodesicsgp))
        self.wait(5)


        geodesics2 = []
        for p in range(particlesN):

            vec_ylayeri_pi = results2[p]
            # print(vec_ylayeri_pi)
            

            path_ylayeri_pi = VMobject().set_points_as_corners(vec_ylayeri_pi)
            geodesics2.append(path_ylayeri_pi)

        geodesicsgp2 = VGroup(*geodesics2)
        self.play(Create(geodesicsgp2))
        self.wait(5)

        # particles = []
        # for path in geodesics:
        #     doti = Sphere(radius=0.05).move_to(path.get_start())
        #     particles.append(doti)
        #     self.play(Create(doti), run_time=0.1)


        # traces = []
        # for particle in particles:
        #     tracei = TracedPath(particle.get_center, stroke_color=YELLOW, stroke_width=4)
        #     traces.append(tracei)
        #     self.add(tracei)


        # animations = []
        # for i in range(len(particles)):
        #     pathi = geodesics[i]
        #     particlei = particles[i]
        #     anim_i = MoveAlongPath(particlei, pathi)
        #     animations.append(anim_i)
                
        # particle_animations = AnimationGroup(*animations)

        # self.play(particle_animations, run_time=10)
        # self.wait(3)


