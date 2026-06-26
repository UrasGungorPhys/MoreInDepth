from manim import *
import numpy as np

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




class Intro(MovingCameraScene):
    def construct(self):
        pass


class EquivalencePrinciple(MovingCameraScene):
    def construct(self):
        pass


class Cameramen(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BGBlue1
        # Background stars:
        stars = VGroup()
        for i in range(100):
            xs = np.random.uniform(-10,50)
            ys = np.random.uniform(-10,10)
            r = np.random.uniform(0.25,0.08)
            stari = Dot(point=[xs,ys,0], radius=0.01, color=WHITE)
            stars.add(stari)

        self.play(FadeIn(stars))

        dot1 = Dot(radius=0.1).shift(LEFT*5)
        dot1ghost = dot1.copy().set_opacity(0)
        startpos = dot1.get_center()


        def insertcam(t, cam, vcam, enter, exit, camframev0, move_camframe, framedelta=30):

            # if t<=move_camframe+15:
            camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*camframev0)

            #Fade in
            if enter<=t<=enter+10:
                opacity = (t-(enter))/10  # start from 0.1, increase +0.1 each iteration up to enter+10
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_stroke(opacity=opacity).set_fill(opacity=0),
                                         camframeanim)
                
            else:
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam),
                                         camframeanim)

            if enter+15<=t<=enter+25:
                vcamframe = (cam.get_x() - self.camera.frame.get_x())/10 + vcam
                # camframeanim = self.camera.frame.animate(run_time=frame_time*10, rate_func=linear).move_to(cam1.get_center()).scale(0.7)
                camframeanim = self.camera.frame.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcamframe).scale(0.98)
                camanim = AnimationGroup(cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam), camframeanim)

            if enter+25< t<= exit-10:
                camanim = cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam)
                if t == enter+framedelta-4:
                    camanim = cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_color(LemonOrange)
                if t == enter+framedelta+4:
                    camanim = cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_color(Vanilla)

                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam)
                camanim = AnimationGroup(camanim, camframeanim)


            if exit-10 <= t<= exit:
                fadeout = (exit - t)/10
                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam).scale(1/0.98)
                camanim = cam.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam).set_stroke(opacity=fadeout).set_fill(opacity=0)
                camanim = AnimationGroup(camanim, camframeanim)

            if t>exit:
                camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam)
                camanim=camframeanim
            
            self.play(AnimationGroup(mainanim, camanim))
            
            if t==exit:
                self.remove(cam)

        a = 0.003
        N=250
        frame_time = 0.15
        enter_cam1 = 40
        exit_cam1 = 90
        enter_cam2 = 95
        exit_cam2 = 140
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
                    deltavs = np.sum(velocities[enter_cam1:enter_cam1+framedelta-1])
                    deltaLEFT = framedelta*vcam1 - deltavs
                    cam1 = Rectangle(height=5, width=7).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)

                insertcam(t, cam1, vcam1, enter_cam1, exit_cam1, 0, enter_cam1)


            elif enter_cam2 <= t <= exit_cam2:

                if t == enter_cam2:
                    framedelta = 30
                    vcam2 = velocities[enter_cam2+framedelta]
                    deltavs = np.sum(velocities[enter_cam2:enter_cam2+framedelta-1])
                    deltaLEFT = framedelta*vcam2 - deltavs
                    cam2 = Rectangle(height=5, width=7).move_to(dot1.get_center()).shift(LEFT*deltaLEFT).set_opacity(0).set_color(Vanilla)
                
                insertcam(t, cam2, vcam2, enter_cam2, exit_cam2, vcam1, enter_cam2)

                # if t<enter_cam2+15:
                #     camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam1)

               
                # if enter_cam2<=t<=enter_cam2+10:
                #     opacity = (t-(enter_cam2))/10  # start from 0.1, increase +0.1 each iteration up to enter_cam1+10
                #     camanim = AnimationGroup(cam2.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam2).set_stroke(opacity=opacity).set_fill(opacity=0),
                #                              mainanim, camframeanim)
                    
                # else:
                #     camanim = AnimationGroup(cam2.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam2),
                #                              mainanim, camframeanim)

                # if enter_cam2+15<=t<=120:
                #     vcamframe = (cam2.get_x() - self.camera.frame.get_x())/10 + vcam2
                #     camframeanim = self.camera.frame.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcamframe)
                #     camanim = AnimationGroup(camanim, camframeanim)

                # if 120< t<= exit_cam2-10:
                #     if t == enter_cam2+framedelta-4:
                #         camanim = cam2.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam2).set_color(LemonOrange)
                #     if t == enter_cam2+framedelta+4:
                #         camanim = cam2.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam2).set_color(Vanilla)

                #     camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam2)
                #     camanim = AnimationGroup(camanim, camframeanim)


                # if exit_cam2-10 <= t<= exit_cam2:
                #     fadeout = (exit_cam2 - t)/10
                #     camframeanim = self.camera.frame.animate(run_time=frame_time,rate_func=linear).shift(RIGHT*vcam2)
                #     camanim = cam2.animate(run_time=frame_time, rate_func=linear).shift(RIGHT*vcam2).set_stroke(opacity=fadeout).set_fill(opacity=0)
                #     camanim = AnimationGroup(camanim, camframeanim)
                
                # self.play(AnimationGroup(mainanim, camanim))
                
                # if t==exit_cam2:
                #     self.remove(cam2)

            else:
                self.play(mainanim)


class TwinsParadox(MovingCameraScene):
    def construct(self):
        pass

        