from manim import *
import numpy as np
from manim.opengl import *


class GRsim1(MovingCameraScene):

    def construct(self):
       

        Nparticles = 5
        results = []
        for p in range(Nparticles):

            T = 150
            N=750
            dt = T/N
            positions = np.array([[-2,1+p*2,0]])
            mass_pos = np.array([7,-3,0])
            m=1
            mv = np.array([1.0, 0,0])
            M=5

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
                zi = zi0

                
                newpos = np.array([xi, yi, zi])
                positions = np.vstack([positions, newpos])

            results.append(positions)

        print(np.shape(results))
        print(np.shape(results[0]))

            
        testv0 = VMobject().set_points_smoothly(results[0])
        testv1 = VMobject().set_points_smoothly(results[1])
        testv2 = VMobject().set_points_smoothly(results[2])
        testv3 = VMobject().set_points_smoothly(results[3])
        testv4 = VMobject().set_points_smoothly(results[4])

        self.play(Create(Dot(mass_pos, radius=1).set_color(YELLOW)))
        self.play(self.camera.frame.animate(run_time=3).move_to(mass_pos).shift(UP*4+RIGHT*5).scale(3))


        p0 = Dot(testv0.get_start())
        p1 = Dot(testv1.get_start())
        p2 = Dot(testv2.get_start())
        p3 = Dot(testv3.get_start())
        p4 = Dot(testv4.get_start())

        trace0 = TracedPath(p0.get_center, stroke_color=YELLOW, stroke_width=4)
        trace1 = TracedPath(p1.get_center, stroke_color=YELLOW, stroke_width=4)
        trace2 = TracedPath(p2.get_center, stroke_color=YELLOW, stroke_width=4)
        trace3 = TracedPath(p3.get_center, stroke_color=YELLOW, stroke_width=4)
        trace4 = TracedPath(p4.get_center, stroke_color=YELLOW, stroke_width=4)

        self.play(AnimationGroup(Create(p0),
                                 Create(p1),
                                 Create(p2),
                                 Create(p3),
                                 Create(p4)), run_time=1.5)
        

        self.add(*[trace0, trace1, trace2, trace3, trace4])
        
        self.play(AnimationGroup(MoveAlongPath(p0, testv0,run_time=10),
                                MoveAlongPath(p1, testv1,run_time=10),
                                MoveAlongPath(p2, testv2,run_time=10),
                                MoveAlongPath(p3, testv3,run_time=10),
                                MoveAlongPath(p4, testv4,run_time=10)))
        
        self.wait(10)


class GRsim3d(ThreeDScene):
    def construct(self):
        # self.camera.set_zoom(0.5)
        # self.set_camera_orientation(phi=-30*DEGREES)

        self.move_camera(phi=30*DEGREES, distance=10)
        ax = ThreeDAxes(
            x_range=(-10,10,5),
            y_range=(-10,10,5),
            z_range=(0,10,5)
        )
        ax.center()
        self.play(Create(ax))
        self.begin_ambient_camera_rotation(rate=0.1)

        y_layers = 3
        results = []
        particle_per_y = 3
        
        for yp in range(y_layers):
            ypos = 2+yp*1.5
            results_per_y = []

            for p in range(particle_per_y):

                T = 150
                N=300
                dt = T/N
                positions = np.array([[-5, ypos,-2+p]])
                mass_pos = np.array([3,-1,0])
                m=1
                mv = np.array([0.8, 1.0,0])
                M=10

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

                results_per_y.append(positions)

            results.append(results_per_y)


        self.play(Create(Sphere(radius=1.7, resolution=(32, 32)).move_to(mass_pos)))

        geodesics = []
        for y_layer in range(y_layers):
            for pz in range(particle_per_y):

                vec_ylayeri_pi = results[y_layer][pz]
                

                path_ylayeri_pi = VMobject().set_points_as_corners(vec_ylayeri_pi)
                geodesics.append(path_ylayeri_pi)


        particles = []
        for path in geodesics:
            doti = Sphere(radius=0.05).move_to(path.get_start())
            particles.append(doti)
            self.play(Create(doti), run_time=0.1)


        traces = []
        for particle in particles:
            tracei = TracedPath(particle.get_center, stroke_color=YELLOW, stroke_width=4)
            traces.append(tracei)
            self.add(tracei)


        animations = []
        for i in range(len(particles)):
            pathi = geodesics[i]
            particlei = particles[i]
            anim_i = MoveAlongPath(particlei, pathi)
            animations.append(anim_i)
                
        particle_animations = AnimationGroup(*animations)

        self.play(particle_animations, run_time=10)
        self.wait(3)




