from manim import *
import numpy as np

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

        Nparticles = 5
        results = []
        for p in range(Nparticles):

            T = 150
            N=750
            dt = T/N
            positions = np.array([[-2,1+p*2,-2+p*3]])
            mass_pos = np.array([7,-3,0])
            m=1
            mv = np.array([1.0, 0.3,0])
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
                zi = zi0 + mv[2]*dt

                
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




