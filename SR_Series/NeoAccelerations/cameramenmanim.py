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
        resultcam = 316
        # first get x's in a preliminary loop:
        deltaxs = []
        velocities = []
        for t in range(N):
            v = t*a
            deltaxs.append(RIGHT*v)
            velocities.append(v)

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

                if t == enter_cams:
                    rapid_start = enter_cams
                    rapid_initial_q = rapid_start - 1
                    rapid_end = N - 1
                    rapid_clock = ValueTracker(rapid_initial_q)
                    rapid_dot_start = dot1.get_center().copy()
                    rapid_frame_start = self.camera.frame.get_center().copy()
                    rapid_run_time = frame_time * (rapid_end - rapid_initial_q)

                    def smoothstep(x):
                        x = np.clip(x, 0, 1)
                        return x * x * (3 - 2 * x)

                    def completed_shift(q):
                        return 0.5 * a * (q * (q + 1) - rapid_initial_q * (rapid_initial_q + 1))

                    def rocket_center_at(q):
                        return rapid_dot_start + RIGHT * completed_shift(q)

                    dot1.add_updater(lambda mob: mob.move_to(rocket_center_at(rapid_clock.get_value())))
                    self.camera.frame.add_updater(
                        lambda mob: mob.move_to(rapid_frame_start + RIGHT * completed_shift(rapid_clock.get_value()))
                    )

                    rapid_frames = VGroup()
                    staccato_offsets = [0, 8, 16, 23, 29, 34, 38]
                    staccato_spawn_times = [rapid_start + offset for offset in staccato_offsets]
                    smooth_start = rapid_start + 41

                    for spawn in staccato_spawn_times:
                        meet = min(resultcam, spawn + 5)
                        spawn_q = spawn - 1
                        meet_q = meet
                        vcam = velocities[meet]
                        delta_left = vcam * (meet_q - spawn_q) - (
                            completed_shift(meet_q) - completed_shift(spawn_q)
                        )
                        birth_center = rocket_center_at(spawn_q) + LEFT * delta_left

                        cami = Rectangle(height=6, width=8).set_fill(opacity=0)
                        cami.set_stroke(color=Vanilla, opacity=0, width=2)

                        def update_staccato_cam(
                            mob,
                            spawn_q=spawn_q,
                            meet_q=meet_q,
                            vcam=vcam,
                            birth_center=birth_center,
                        ):
                            q = rapid_clock.get_value()
                            age = q - spawn_q
                            if age < 0:
                                mob.set_stroke(opacity=0)
                                return mob

                            mob.move_to(birth_center + RIGHT * (vcam * age))
                            glow = np.exp(-((q - meet_q) / 1.25) ** 2)
                            fade_in = smoothstep(age / 1.2)
                            fade_out = 1 - smoothstep((q - meet_q - 16) / 8)
                            opacity = (0.28 + 0.62 * glow) * fade_in * fade_out
                            color = interpolate_color(Vanilla, LemonOrange, glow)
                            mob.stretch_to_fit_width(8)
                            mob.stretch_to_fit_height(6)
                            mob.set_stroke(color=color, opacity=opacity, width=2.4 + 2.6 * glow)
                            mob.set_fill(opacity=0)
                            return mob

                        cami.add_updater(update_staccato_cam)
                        rapid_frames.add(cami)

                    rapid_spawn_times = list(range(smooth_start, resultcam + 1))
                    for spawn in rapid_spawn_times:
                        progress = (spawn - smooth_start) / max(1, resultcam - smooth_start)
                        lookahead = max(0, int(round(interpolate(8, 0, smoothstep(progress)))))
                        meet = min(resultcam, spawn + lookahead)
                        spawn_q = spawn - 1
                        meet_q = meet
                        vcam = velocities[meet]
                        delta_left = vcam * (meet_q - spawn_q) - (
                            completed_shift(meet_q) - completed_shift(spawn_q)
                        )
                        birth_center = rocket_center_at(spawn_q) + LEFT * delta_left

                        cami = Rectangle(height=6, width=8).set_fill(opacity=0)
                        cami.set_stroke(color=Vanilla, opacity=0, width=2)

                        def update_rapid_cam(
                            mob,
                            spawn_q=spawn_q,
                            meet_q=meet_q,
                            vcam=vcam,
                            birth_center=birth_center,
                            progress=progress,
                        ):
                            q = rapid_clock.get_value()
                            age = q - spawn_q
                            if age < 0:
                                mob.set_stroke(opacity=0)
                                return mob

                            mob.move_to(birth_center + RIGHT * (vcam * age))
                            glow = np.exp(-((q - meet_q) / 1.45) ** 2)
                            fade_in = smoothstep(age / 1.5)
                            fade_out = 1 - smoothstep((q - meet_q - 4) / 10)
                            opacity = (0.12 + 0.70 * glow) * fade_in * fade_out
                            color = interpolate_color(Vanilla, LemonOrange, glow)
                            trail_scale = interpolate(0.90, 0.985, smoothstep(progress))
                            visible_scale = trail_scale + (1 - trail_scale) * glow
                            mob.stretch_to_fit_width(8 * visible_scale)
                            mob.stretch_to_fit_height(6 * visible_scale)
                            mob.set_stroke(color=color, opacity=opacity, width=2.2 + 2.8 * glow)
                            mob.set_fill(opacity=0)
                            return mob

                        cami.add_updater(update_rapid_cam)
                        rapid_frames.add(cami)

                    finalcam = Rectangle(height=6, width=8).set_fill(opacity=0)
                    finalcam.set_stroke(color=LemonOrange, opacity=0, width=4)

                    def update_final_cam(mob):
                        q = rapid_clock.get_value()
                        alpha = smoothstep((q - resultcam - 3) / 10)
                        mob.move_to(rocket_center_at(q))
                        mob.set_stroke(color=LemonOrange, opacity=0.95 * alpha, width=4)
                        mob.set_fill(opacity=0)
                        return mob

                    finalcam.add_updater(update_final_cam)
                    self.add(rapid_frames, finalcam)
                    self.play(rapid_clock.animate.set_value(rapid_end), run_time=rapid_run_time, rate_func=linear)
                    break

                else:
                    self.play(mainanim, camframeanimation)
