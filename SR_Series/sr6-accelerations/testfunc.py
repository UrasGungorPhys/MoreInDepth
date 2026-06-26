import numpy as np
from manim import *
# no, gpt didn't write this

class SphereArc(ThreeDScene):
    def construct(self):
        self.camera.set_zoom(0.6)
        # self.set_camera_orientation(theta=PI/8)
        # self.set_camera_orientation(phi=PI/4)
        ax = ThreeDAxes(
            x_range=(-10,10,5),
            y_range=(-10,10,5),
            z_range=(0,10,5)
        )
        axlabels = ax.get_axis_labels(x_label="x", y_label="y", z_label="z")
        self.play(Create(ax))
        self.play(Write(axlabels))

        mass_pos = np.array([3,-1/2,3])

        p00 = np.array([3,3,3])

        
        p1 = np.array([3, 3,-2])
        theline00 = Line(mass_pos, p00)
        theline = Line(mass_pos, p1)
        rotationlinemobject = Line(theline.get_start(), theline.get_start()+np.array([0,5,3.5]))
        rotationline = np.array([0,5,3.5])
        

        self.play(Create(Sphere(mass_pos, radius=0.1)))
        # self.play(Create(Sphere(p1, radius=0.1)))
        

        
        # self.play(Create(theline))
        
        # print(theline.get_vector())
        # print(theline.get_angle())
        
        # self.play(theline.animate.rotate(PI/20, axis=rotationline, about_point=theline.get_start()))
        # pt2 = theline.get_end()
        # self.play(theline.animate.rotate(PI/20, axis=rotationline, about_point=theline.get_start()))
        # pt3 = theline.get_end()
        # self.play(Create(Sphere(pt2, radius=0.1)))
        # self.play(Create(Sphere(pt3, radius=0.1)))

        # self.play(theline.animate.rotate(-PI/20*3, axis=rotationline, about_point=theline.get_start()))
        # pt4 = theline.get_end()
        # self.play(theline.animate.rotate(-PI/20, axis=rotationline, about_point=theline.get_start()))
        # pt5 = theline.get_end()
        # self.play(Create(Sphere(pt4, radius=0.1)))
        # self.play(Create(Sphere(pt5, radius=0.1)))



        def get_those_damn_points(masspos, p0, d_angle, howmanyoneachside):
            vx0 = np.array([1.5, 0,0])
            vz0 = np.array([0,0,1.5])
            # p1 and masspos must be aligned on one axis.
            theline = Line(masspos, p0).set_opacity(0)
            linevec = theline.get_vector()

            if linevec[0] == 0:
                flip = 1

            if linevec[1] == 0:
                flip=0

            if linevec[2] == 0:
                flip=1

            rotationline = np.array([linevec[0], linevec[2], linevec[1]]) # this is certainly not gonna be general
            rotationline[flip] = -rotationline[flip]  # flip that index to get a perpendicular line as ax of rotation

            # print("RL1", rotationline)
            # self.play(Create(theline))
            # self.play(Create(Line(theline.get_start(), theline.get_start()+rotationline*3)))
            pts = [p0]
            vzs = [theline.get_unit_vector()/10 + vz0]
            for i in range(howmanyoneachside):
                theline.rotate(-d_angle, axis=rotationline, about_point=theline.get_start())
                
                pti = theline.get_end()
                pts.append(pti)
                vzi = theline.get_unit_vector()/10 + vz0
                vzs.append(vzi)
            

            # theline.rotate(-d_angle*howmanyoneachside, axis=rotationline, about_point=theline.get_start())
            theline = Line(masspos, p0).set_opacity(0)
            # to reset the line to its initial angle.


            for i in range(howmanyoneachside):
                theline.rotate(d_angle, axis=rotationline, about_point=theline.get_start())
                pti = theline.get_end()
                pts.append(pti)
                vzi = theline.get_unit_vector()/10 + vz0
                vzs.append(vzi)
                
            print(vzs)

            rotationline2 = np.array([-rotationline[2], rotationline[1], rotationline[0]]) # flip these around to get the
            #  second set of points through different rotation, getting a full "square"
            # print("RL2", rotationline2)
            # self.play(Create(Line(theline.get_start(), theline.get_start()+rotationline2*3)))

            pts2 = [pts[-1]]  # take the last element so the "square" is complete.
            # we will give these a different velocity so it's needed.
            vxs = [theline.get_unit_vector()/10 + vx0]
            for i in range(howmanyoneachside*2):
                theline.rotate(-d_angle, axis=rotationline2, about_point=theline.get_start())
                # self.play(theline.animate.rotate(-d_angle, axis=rotationline2, about_point=theline.get_start()))
                pti = theline.get_end()
                pts2.append(pti)
                vxi = theline.get_unit_vector()/10 + vx0
                vxs.append(vxi)
            print(vxs)



            return pts, pts2, vzs, vxs


        ptest1, ptest2, vxvals, vzvals = get_those_damn_points(np.array([3,-1/2,3]), np.array([3, 3,-2]), PI/20, 3)
        for pt in ptest1:
            self.play(Create(Dot(pt, radius=0.1)))


        for pt in ptest2:
            self.play(Create(Dot(pt, radius=0.1).set_color(YELLOW)))

        self.wait(5)

