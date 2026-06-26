from manim import *
import numpy as np

class RearClockAheadDiagram(MovingCameraScene):
    def construct(self):


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

        ll = 6  # axis lengths to draw
        axrange = 10  # coordinate ranges
        norm = ll/axrange  # normalize any distance to fit
        pcolor=BLUE_C  # Color to use for the primed axes

        # Stationary axes:

        ax = Axes(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5})
        grid = NumberPlane(x_range=[0,axrange,1], y_range=[0,axrange,1], 
        x_length=ll, y_length=ll,  
        background_line_style={"stroke_color": WHITE,
                                "stroke_width": 1,
                                "stroke_opacity": 0.5,})

        ax_labels = ax.get_axis_labels(x_label="x", y_label="t")

        xct = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange,axrange)).set_color(YELLOW_E)
        xct0 = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange,axrange)).set_color(YELLOW_E)
        lightlabel = MathTex("x=ct").next_to(xct.get_end(), UR).set_color(YELLOW_E)

        # Initial axes, to be Lorentz transformed:
        OG = ax.c2p(0,0)
        xhat = np.array([1,0,0])
        that = np.array([0,1,0])

        xpi = Arrow(start=OG, end=OG+6*xhat, buff=0).set_color(pcolor)
        tpi = Arrow(start=OG, end=OG+6*that, buff=0).set_color(pcolor)

        # Initial Lorentz grid
        manual_grids0x = VGroup()
        manual_grids0y = VGroup()
        for i in range(1,10):

            xline = Line(start=OG + i*that*norm,
                         end=OG + i*that*norm + 5.8*xhat, buff=0,
                         stroke_color=pcolor, stroke_opacity=0.5)

            tline = Line(start=OG + i*xhat*norm,
                         end=OG + i*xhat*norm + 5.8*that, buff=0,
                         stroke_color=pcolor, stroke_opacity=0.5)

            manual_grids0x.add(xline)
            manual_grids0y.add(tline)

        # Lorentz axes
        v = 0.25
        gamma = 1/np.sqrt(1-v**2)

        xp_direction = np.array([1,v,0])
        tp_direction = np.array([v,1,0])

        xphat = xp_direction
        tphat = tp_direction

        xp = Arrow(start=OG, end=OG + 6.4*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        xplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor)

        tp = Arrow(start=OG, end=OG + 6.4*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        tplabel = always_redraw(lambda : MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor))

        xct_long = DashedLine(start=ax.c2p(0,0), end=ax.c2p(axrange+2.5,axrange+2.5)).set_color(YELLOW_E)
        lightlabel_long = MathTex("x=ct").next_to(xct_long.get_end(), DR).set_color(YELLOW_E)

        # Lorentz grid

        manual_gridspx = VGroup()
        manual_gridspy = VGroup()
        for i in range(1,10):

            xpline = Line(start=OG + i*tp_direction*norm,
                         end=OG + i*tp_direction*norm + 5.8*xp_direction, buff=0, 
                         stroke_color=pcolor, stroke_opacity=0.5)


            tpline = Line(start=OG + i*xp_direction*norm,
                         end=OG + i*xp_direction*norm + 5.8*tp_direction, buff=0,
                         stroke_color=pcolor, stroke_opacity=0.5)

            manual_gridspx.add(xpline)
            manual_gridspy.add(tpline)


        event00 = xct.get_center()
        event0pt = Dot(event00).shift(RIGHT*2+UP).set_color(ORANGE)
        event0 = event0pt.get_center()
        event0label = always_redraw(lambda: MathTex("p").next_to(event0pt, RIGHT).set_color(ORANGE))

        event0labelsp = MathTex("= (x_p', t_p')").next_to(event0label, RIGHT*2.1).set_color(pcolor)
        event0labels = MathTex("= (x_p,t_p)").next_to(event0labelsp, DOWN)

        event0_prjxp = always_redraw(lambda:Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15))  # not gonna draw these
        event0_prjtp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center() - tphat*15))
        intersection_tp = gli(event0_prjxp, tp)
        intersection_xp = gli(event0_prjtp, xp)

        event0xp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - tphat*15), xp)).set_color(ORANGE))
        event0tp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15), tp)).set_color(ORANGE))

        intersection_xppt = always_redraw(lambda: Dot(event0xp.get_end()).set_color(ORANGE))
        intersection_tppt = always_redraw(lambda: Dot(event0tp.get_end()).set_color(ORANGE))

        xplen = always_redraw(lambda:Line(start=OG, end=event0xp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))
        tplen = always_redraw(lambda:Line(start=OG, end=event0tp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))

        pxplabel = always_redraw(lambda: MathTex("x_p'").next_to(intersection_xppt.get_center(), DOWN).set_color(ORANGE))
        ptplabel = always_redraw(lambda: MathTex("t_p'").next_to(intersection_tppt.get_center(), LEFT).set_color(ORANGE))

        event0x = always_redraw(lambda: DashedLine(start=event0pt.get_center(),end=[event0pt.get_x(),OG[1],0]).set_color(MAROON_D))
        event0t = always_redraw(lambda: DashedLine(start=event0pt.get_center(),end=[OG[0], event0pt.get_y(),0]).set_color(MAROON_D))

        pxdot = always_redraw(lambda: Dot([event0pt.get_x(),OG[1],0]).set_color(MAROON_D))
        ptdot = always_redraw(lambda: Dot([OG[0], event0pt.get_y(),0]).set_color(MAROON_D))

        pxlabel = always_redraw(lambda: MathTex("x_p").next_to(pxdot, DOWN).set_color(MAROON_D))
        ptlabel = always_redraw(lambda: MathTex("t_p").next_to(ptdot, LEFT).set_color(MAROON_D))

        xlen = always_redraw(lambda:Line(start=OG, end=pxdot.get_center(), stroke_width=6,buff=0).set_color(MAROON_C))
        tlen = always_redraw(lambda:Line(start=OG, end=ptdot.get_center(), stroke_width=6,buff=0).set_color(MAROON_C))


        # Plays!
        self.play(Create(ax), Create(ax_labels), run_time=3)
        self.play(Create(grid), run_time=2)
        self.play(Create(xct), FadeIn(lightlabel))
        self.wait(2)

        self.play(Create(xpi), Create(tpi))
        self.wait(2)
        self.play(Create(manual_grids0x), Create(manual_grids0y),run_time=1)
        self.wait(2)

        self.play(FadeOut(lightlabel))

        self.play(Transform(xpi, xp), Transform(tpi, tp),
                    Transform(manual_grids0x, manual_gridspx),
                    Transform(manual_grids0y, manual_gridspy),
                    Transform(xct, xct_long),
                    self.camera.frame.animate.scale(1.12).shift(UP*0.5+RIGHT),run_time=4)

        self.play(FadeIn(xplabel), FadeIn(tplabel), FadeIn(lightlabel_long.set_opacity(0.8)), run_time=2)
        self.wait(4)
        
        self.play(Indicate(manual_grids0y))
        self.play(Indicate(tpi))
        self.wait(1)

        self.play(Indicate(manual_grids0x))
        self.play(Indicate(xpi))
        self.wait(5)

        self.play(FadeOut(manual_grids0x),FadeOut(manual_grids0y),FadeOut(grid),
                    Transform(xct,xct0.set_opacity(0.4)), FadeOut(lightlabel_long),
                    self.camera.frame.animate.shift(DOWN*0.1+LEFT), run_time=2)

        # Demonstrate projection for event p
        self.wait(1)
        self.play(Create(event0pt))
        self.wait()
        self.play(Create(event0label))
        self.wait(2)
        self.play(Create(event0labels), Create(event0labelsp))
        self.wait(3)
        self.play(FadeOut(event0labelsp), FadeOut(event0labels))
        self.wait(2)

        # self.play(Create(event0_prjtp),Create(event0_prjxp))  # to check if needed
        self.play(ShowPassingFlash(xpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(Create(event0tp), run_time=1.5)
        self.wait(1)
        self.play(Create(intersection_tppt))
        self.play(Create(tplen))
        self.bring_to_front(intersection_tppt)
        self.play(Create(ptplabel))

        self.wait(1.5)

        self.play(ShowPassingFlash(tpi.copy().reverse_points().set_stroke(WHITE)))
        self.play(Create(event0xp), run_time=1.5)
        self.wait(1)
        self.play(Create(intersection_xppt))
        self.play(Create(xplen))
        self.bring_to_front(intersection_xppt)
        self.play(Create(pxplabel))

        self.wait()
        self.play(FadeIn(manual_gridspx), FadeIn(manual_gridspy))
        self.wait(2)
        self.play(FadeOut(manual_gridspx), FadeOut(manual_gridspy))

        self.wait(3)
        self.play(Create(event0x), Create(event0t),run_time=1)
        self.play(Create(pxdot), Create(ptdot))
        self.wait()
        self.play(FadeIn(grid))
        self.wait()
        self.play(Create(xlen), Create(tlen))
        self.bring_to_front(pxdot)
        self.bring_to_front(ptdot)
        self.play(Create(pxlabel), Create(ptlabel))
        self.wait()
        self.play(FadeOut(grid))

        self.play(event0pt.animate.shift(RIGHT*0.5), run_time=2)
        self.play(event0pt.animate.shift(LEFT*3 + UP*1.6), run_time=3.5)
        self.play(event0pt.animate.shift(LEFT*1.2 + DOWN*2.6), run_time=2)
        self.play(event0pt.animate.shift(RIGHT*1.2 + DOWN*2), run_time=2)
        self.play(event0pt.animate.move_to(event0), run_time=2)
        self.wait(2)

        self.play(FadeOut(event0label), FadeOut(event0x), FadeOut(event0t), FadeOut(pxdot), FadeOut(ptdot),
        FadeOut(event0xp),FadeOut(event0tp), FadeOut(intersection_tppt), FadeOut(intersection_xppt),
        FadeOut(pxlabel), FadeOut(ptlabel), FadeOut(tlen), FadeOut(xplen), FadeOut(tplen), FadeOut(pxplabel), FadeOut(ptplabel), run_time=2)
        
        self.wait(1)
        self.play(event0pt.animate.move_to(ax.c2p(8.5,0)))
        self.play(FadeOut(xlen))
        planetB = ImageMobject("planet2.png").move_to(ax.c2p(8.5,0)).scale(0.12)
        self.wait()
        self.play(FadeOut(event0pt), FadeIn(planetB))
        self.wait(2)
        self.play(Indicate(xpi))
        self.wait(2)

        # Moving onto a larger diagram:
        self.play(self.camera.frame.animate.scale(1.3).move_to(ax.c2p(3,3)), run_time=3)
        self.wait(1)

        negax = Axes(x_range=[-5,axrange,1], y_range=[-5,axrange,1], 
        x_length=ll+3, y_length=ll+3,axis_config={"include_ticks": False})
        negax.shift(OG - negax.c2p(0, 0))  # align origins

        # Draw the negative axes:
        negxp = Arrow(start=OG, end=OG - 3*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        negxplabel = always_redraw(lambda: MathTex("-x'").next_to(negxp.get_end(), LEFT).set_color(pcolor))

        negtp = Arrow(start=OG, end=OG - 3*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        negtplabel = always_redraw(lambda : MathTex("-t'").next_to(negtp.get_end(), LEFT).set_color(pcolor))
        

        self.play(Transform(ax, negax))
        self.wait(2)
        self.play(Create(negtp), Create(negtplabel), run_time=2)
        self.wait(1)
        self.play(Create(negxp), Create(negxplabel), run_time=2)
        self.wait(2)
        self.play(FadeOut(planetB), FadeIn(event0pt))

        negprjxp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()+ tphat*15))
        negprjtp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()- xphat*15))

        # get some extra long lines that won't be drawn, to prevent intersection finding error in case I overshoot:
        xplongghost = Arrow(start=OG, end=OG + 10*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        negtplongghost = Arrow(start=OG, end=OG - 3*tp_direction/np.linalg.norm(tp_direction), buff=0, stroke_width=3.5).set_color(pcolor)

        worldlineB = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center() + that*5.5))
        worldlineBlabel = always_redraw(lambda: MathTex("x_B(t)").next_to(worldlineB.get_end(), RIGHT).scale(0.8))

        along_wlB = Dot(gli(worldlineB, xpi)).set_color(PURPLE_E)
        prjx_wlB = always_redraw(lambda: DashedLine(start=along_wlB.get_bottom(), 
                                         end=gli(Line(start=along_wlB.get_center(), end=along_wlB.get_center() - tphat*15), xpi)).set_color(PURPLE_E))
        prjt_wlB = always_redraw(lambda: DashedLine(start=along_wlB.get_left(),
                                         end=gli(Line(start=along_wlB.get_center(), end=along_wlB.get_center() - xphat*15), tpi)).set_color(PURPLE_E))
        wlb_xlen = always_redraw(lambda: Line(start=OG, end=prjx_wlB.get_end(), stroke_width=6).set_color(PURPLE_E))
        wlb_tlen = always_redraw(lambda: Line(start=OG, end=prjt_wlB.get_end(), stroke_width=6).set_color(PURPLE_E))
        
        
        negevent0xp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xplongghost)).set_color(MAROON_C))

        negevent0tp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15), negtplongghost)).set_color(ORANGE))

        negpxpdot = always_redraw(lambda: Dot(negevent0xp.get_end()).set_color(pcolor))
        negptpdot = always_redraw(lambda: Dot(negevent0tp.get_end()).set_color(pcolor))

        negpxplabel = always_redraw(lambda: MathTex("x_B(t'=0)").next_to(negpxpdot, DOWN*0.1+RIGHT*0.1).set_color(pcolor).scale(0.75))
        negptplabel = always_redraw(lambda: MathTex("\Delta t'").next_to(negptpdot, LEFT).set_color(pcolor).scale(0.75))

        negxplen = always_redraw(lambda:Line(start=OG, end=negevent0xp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))
        negtplen = always_redraw(lambda:Line(start=OG, end=negevent0tp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))

        self.wait(2)
        self.play(Create(negevent0tp))
        self.wait(2)
        # show that this is where tb' is simultaneous with tb=0
        self.play(Create(negptpdot))

        tbzero = MathTex("t_B =  0").next_to(event0pt.get_center(), DOWN*1.2).scale(0.8).shift(RIGHT*0.2)
        angleofxp = np.arctan(v)
        simline = MathTex(r"\text{Line of simultaneous events}").scale(0.7).set_color(pcolor).rotate(angleofxp).next_to(negevent0tp.get_end()).shift(RIGHT*0.5+UP*0.2)
        
        tbpzero1 = MathTex("t=0" ).next_to(negptpdot.get_center(), LEFT*1.5)
        tbpzero2 = MathTex("t_B' = ?" ).set_color(pcolor).next_to(tbpzero1,DOWN).set_color(pcolor)

        self.play(Indicate(ax.x_axis))
        self.wait()
        self.play(Write(tbzero))
        self.wait(2)
        self.play(Create(simline))
        self.play(Indicate(negptpdot))
        self.wait()
        self.play(ShowPassingFlash(negevent0tp.copy()))
        self.play(Write(tbpzero1),run_time=2)
        self.play(Write(tbpzero2),run_time=2)

        self.wait(4)
        self.play(Create(worldlineB), run_time=2)
        self.play(Write(worldlineBlabel))
        self.wait(2)
        self.play(Create(along_wlB))
        self.play(Create(prjx_wlB), Create(prjt_wlB), run_time=2)
        self.play(Create(wlb_xlen), Create(wlb_tlen), run_time=2)
        self.play(along_wlB.animate.move_to(worldlineB.get_end()), run_time=5)
        self.wait(2)
        delx_alongwlb = Line(start=gli(xpi,worldlineB),end=wlb_xlen.get_end(),stroke_width=6).set_color(RED_D)
        self.add(delx_alongwlb)
        self.play(Indicate(delx_alongwlb))
        self.wait(2)
        wlbfadeouts = [along_wlB, prjt_wlB, prjx_wlB, wlb_tlen, wlb_xlen, delx_alongwlb]
        self.play(FadeOut(*wlbfadeouts), run_time=3)

        self.wait(3)

        self.play(Create(negevent0xp))
        self.play(Create(negpxpdot))
        self.play(Create(negpxplabel), run_time=2)
        self.wait()
        self.play(FadeOut(worldlineB), FadeOut(worldlineBlabel))
        self.wait(3)

        # show the B clock ahead delta tb
        prjt = always_redraw(lambda: DashedLine(start=negpxpdot.get_left(), end=[OG[0],negpxpdot.get_y(),0]).set_color(MAROON_E))
        prjtdot = always_redraw(lambda: Dot(prjt.get_end()).set_color(MAROON_E))
        lenpt = always_redraw(lambda: Line(start=OG, end=prjt.get_end(), stroke_width=6,buff=0).set_color(MAROON_C))
        deltlabel = always_redraw(lambda: MathTex("\Delta t").scale(0.8).next_to(lenpt.get_center(), LEFT).set_color(MAROON_C))
        # tpzero = MathTex("t' =  0").set_color(pcolor).next_to(negpxpdot.get_center(), UP*1.2+LEFT*0.02)
        tbattpzero1 = MathTex("t'=0").next_to(prjtdot, LEFT*1.5+UP*0.3).set_color(pcolor)
        tbattpzero2 = MathTex("t_B = ?").next_to(tbattpzero1, DOWN)
        # tbattpzero[0].set_color(pcolor)
        # tbattpzero[1].set_color(WHITE)
        fadeouts0 = [tbzero, simline, tbpzero1,tbpzero2, tbattpzero1, tbattpzero2]

        self.play(Indicate(xpi))
        self.wait()
        # self.play(Write(tpzero))
        self.wait(2)
        self.play(Create(prjt),run_time=2)
        self.play(Create(prjtdot))
        self.wait(2)
        self.play(Create(lenpt), run_time=2)
        self.bring_to_front(prjtdot)
        self.play(Write(tbattpzero1))
        self.play(Write(tbattpzero2))
        self.bring_to_front(negpxpdot)
        # self.play(Write(deltlabel))


        self.wait(4)
        self.play(FadeOut(*fadeouts0))
        self.play(FadeIn(negptplabel), FadeIn(deltlabel))
        self.wait(2)
        self.play(Create(negtplen), run_time=2)
        self.bring_to_front(negpxpdot)
        self.bring_to_front(negptpdot)


        # derive Lv/c^2 with Lorentz transform
        statcoords = MathTex("(x_B,t_B) = (L, 0)").set_color(ORANGE).next_to(event0pt.get_center(), DOWN+RIGHT*0.3)
        LTarrow = Arrow(start=event0pt.get_center(), end=negptpdot.get_center()).set_color(pcolor)
        LTforB = MathTex(r"t' = \gamma\left( t - \frac{v}{c^2}x\right)").move_to(LTarrow.get_center()).shift(DOWN+RIGHT).scale(1.2).set_color(pcolor)

        LTforB1 = MathTex("\Delta t' = ",r"\gamma\left(t_B - \frac{v}{c^2}x_B\right)").scale(1.2).set_color(pcolor)
        LTforB2 = MathTex("\Delta t' = ",r"\gamma\left(0 - \frac{v}{c^2}L\right)").scale(1.2).set_color(pcolor)
        LTforB3 = MathTex("\Delta t' = - ", r"\gamma", r"\frac{Lv}{c^2}").scale(1.2).set_color(pcolor)


        self.wait(2)
        self.play(Indicate(event0pt))
        self.wait()
        self.play(Create(statcoords))
        self.wait(2)
        self.play(Indicate(negptplabel))
        self.wait()
        self.play(Create(LTarrow), run_time=2)
        self.wait(2)
        self.play(FadeOut(statcoords))

        # self.play(Write(LTforB))
        eqposdot = Dot(LTarrow.get_center()).shift(DOWN+RIGHT)
        self.wait(2)
        self.play(Write(LTforB), FadeOut(LTarrow))
        self.play(Write(LTforB1.next_to(LTforB, DOWN)))
        self.wait(2)
        self.play(FadeOut(LTforB), LTforB1.animate.move_to(eqposdot.get_center()))
        self.wait(2)
        self.play(FadeIn(statcoords))
        self.wait(2)
        self.play(Write(LTforB2.next_to(LTforB1, DOWN)))
        self.wait(2)
        self.play(FadeOut(LTforB1), LTforB2.animate.move_to(LTforB1.get_center()))
        self.play(FadeOut(statcoords))
        self.wait(2)
        self.play(Write(LTforB3.next_to(LTforB2, DOWN)))
        self.wait(2)
        self.play(FadeOut(LTforB2), LTforB3.animate.move_to(LTforB2.get_center()))
        self.wait(2)
        self.play(Indicate(LTforB3[2]))
        self.wait(1)
        self.play(Indicate(LTforB3[1]))

        self.wait(5)


        ## move the point closer and further on x axis to show L dependence
        ## LT into a new frame with larger v to show v and gamma dependence, also better to differ points

        # get some longer axes to show distance
        

        xplong = Arrow(start=OG, end=OG + 8.5*xp_direction/np.linalg.norm(xp_direction), buff=0, stroke_width=3.5).set_color(pcolor)
        xplonglabel = MathTex("x'").next_to(xplong.get_end(), RIGHT).set_color(pcolor)
        xplabel0 = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor)
        

        xlong = Axes(x_range=[-5,axrange+3,1], y_range=[-5,axrange,1], 
        x_length=ll+6, y_length=ll+3,axis_config={"include_ticks": False})
        xlong.shift(OG - xlong.c2p(0, 0))  # align origins
        xlong_labels = xlong.get_axis_labels(x_label="x", y_label="t")

        ax0 = Axes(x_range=[-5,axrange,1], y_range=[-5,axrange,1], 
        x_length=ll+3, y_length=ll+3,axis_config={"include_ticks": False})
        ax0.shift(OG - ax0.c2p(0, 0))  # align origins  # keeping this to transform back
        ax0labels = ax0.get_axis_labels(x_label="x", y_label="t")


        self.play(event0pt.animate.shift(LEFT*3), run_time=2)
        self.wait()
        self.play(Indicate(negtplen))
        self.play(Indicate(lenpt))
        self.wait(1)
        self.play(event0pt.animate.shift(RIGHT*5), Transform(ax, xlong), Transform(xpi, xplong),
                 Transform(ax_labels, xlong_labels), Transform(xplabel, xplonglabel), run_time=2)  # get longer axes
        self.wait()
        self.play(Indicate(negtplen))
        self.play(Indicate(lenpt))
        self.wait(2)
        self.play(event0pt.animate.shift(LEFT*2), Transform(ax, ax0), Transform(xpi, xp),
                  Transform(ax_labels, ax0labels),Transform(xplabel, xplabel0), run_time=2)  # back to old axes





        ## LT into a new frame with larger v to show v and gamma dependence, also better to differ points
        # let's start by removing the always_redraw stuff with static ones

        nrdnegprjxp = Line(start=event0pt.get_center(), end=event0pt.get_center()+ tphat*15)
        nrdnegprjtp = Line(start=event0pt.get_center(), end=event0pt.get_center()- xphat*15)

        nrdnegevent0xp = DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xp)).set_color(MAROON_C)

        nrdnegevent0tp = DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xphat*15), negtp)).set_color(ORANGE)

        nrdnegpxpdot = Dot(negevent0xp.get_end()).set_color(pcolor)
        nrdnegptpdot = Dot(negevent0tp.get_end()).set_color(pcolor)

        nrdnegpxplabel = MathTex("x_B(t'=0)").next_to(negpxpdot, DOWN*0.3+RIGHT*0.2).set_color(pcolor).scale(0.75)
        nrdnegptplabel = MathTex("\Delta t'").next_to(negptpdot, LEFT).set_color(pcolor).scale(0.75)

        # nrdnegxplen = Line(start=OG, end=negevent0xp.get_end(), stroke_width=6,buff=0).set_color(ORANGE)
        nrdnegtplen = Line(start=OG, end=negevent0tp.get_end(), stroke_width=6,buff=0).set_color(ORANGE)

        nrdxplabel = MathTex("x'").next_to(xp.get_end(), RIGHT).set_color(pcolor)
        nrdtplabel = MathTex("t'").next_to(tp.get_end(), UP).set_color(pcolor)

        nrdprjt = DashedLine(start=negpxpdot.get_left(), end=[OG[0],negpxpdot.get_y(),0]).set_color(MAROON_E)
        nrdprjtdot = Dot(prjt.get_end()).set_color(MAROON_E)
        nrdlenpt = Line(start=OG, end=prjt.get_end(), stroke_width=6,buff=0).set_color(MAROON_C)
        nrddeltlabel = MathTex("\Delta t").scale(0.8).next_to(lenpt.get_center(), LEFT).set_color(MAROON_C) 


        redrawObjects = [negevent0xp,negevent0tp,negpxpdot,negptpdot,negpxplabel,negptplabel,negxplen,negtplen,xplabel,tplabel, prjt, prjtdot, lenpt, deltlabel]
        noredrawObjects = [nrdnegevent0xp,nrdnegevent0tp,nrdnegpxpdot,nrdnegptpdot,nrdnegpxplabel,nrdnegptplabel,nrdnegtplen, nrdxplabel, nrdtplabel, nrdprjt, nrdlenpt, nrdprjtdot, nrddeltlabel]
        self.remove(*redrawObjects)
        self.add(*noredrawObjects)

        u = 0.4

        xpphat = np.array([1,u,0])
        tpphat = np.array([u,1,0])


        xpp = Arrow(start=OG, end=OG + 7.5*xpphat/np.linalg.norm(xpphat), buff=0, stroke_width=3.5).set_color(BLUE_E)
        xpplabel = always_redraw(lambda: MathTex("x'").next_to(xpp.get_end(), RIGHT).set_color(BLUE_E))
        tpp = Arrow(start=OG, end=OG + 7.5*tpphat/np.linalg.norm(tpphat), buff=0, stroke_width=3.5).set_color(BLUE_E)
        tpplabel = always_redraw(lambda : MathTex("t'").next_to(tpp.get_end(), UP).set_color(BLUE_E))

        negxpp = Arrow(start=OG, end=OG - 5.5*xpphat/np.linalg.norm(xpphat), buff=0, stroke_width=3.5).set_color(BLUE_E)
        negxpplabel = always_redraw(lambda: MathTex("-x'").next_to(negxpp.get_end(), LEFT).set_color(BLUE_E))

        negtpp = Arrow(start=OG, end=OG - 5.5*tpphat/np.linalg.norm(tpphat), buff=0, stroke_width=3.5).set_color(BLUE_E)
        negtpplabel = always_redraw(lambda : MathTex("-t'").next_to(negtpp.get_end(), LEFT).set_color(BLUE_E))

        negprjxpp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()+ that*15))
        negprjtpp = always_redraw(lambda: Line(start=event0pt.get_center(), end=event0pt.get_center()- xpphat*15))

        negevent0xpp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() + that*15), xpp)).set_color(MAROON_C))

        negevent0tpp = always_redraw(lambda: DashedLine(start=event0pt.get_center(),
                        end=gli(Line(start=event0pt.get_center(), end=event0pt.get_center() - xpphat*15), negtpp)).set_color(ORANGE))

        negpxppdot = always_redraw(lambda: Dot(negevent0xpp.get_end()).set_color(pcolor))
        negptppdot = always_redraw(lambda: Dot(negevent0tpp.get_end()).set_color(pcolor))

        negpxpplabel = always_redraw(lambda: MathTex(r"x_{B_0'}").next_to(negpxppdot, DOWN*0.1+RIGHT*0.1).set_color(pcolor).scale(0.75))
        negptpplabel = always_redraw(lambda: MathTex("\Delta t'").next_to(negptppdot, LEFT).set_color(pcolor))

        negxpplen = always_redraw(lambda:Line(start=OG, end=negevent0xpp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))
        negtpplen = always_redraw(lambda:Line(start=OG, end=negevent0tpp.get_end(), stroke_width=6,buff=0).set_color(ORANGE))

        newprjt = always_redraw(lambda: DashedLine(start=negpxppdot.get_left(), end=[OG[0],negpxppdot.get_y(),0]).set_color(MAROON_C))
        newprjtdot = always_redraw(lambda: Dot(newprjt.get_end()).set_color(MAROON_E))
        newlenpt = always_redraw(lambda: Line(start=OG, end=newprjt.get_end(), stroke_width=6,buff=0).set_color(MAROON_C))
    


        self.play(Transform(xpi, xpp), Transform(tpi, tpp), Transform(negxp, negxpp), Transform(negtp, negtpp),
        Transform(nrdxplabel, xpplabel),Transform(nrdtplabel, tpplabel),
        Transform(nrdnegevent0xp, negevent0xpp),Transform(nrdnegevent0tp, negevent0tpp),Transform(nrdnegpxpdot, negpxppdot),
        Transform(nrdnegptpdot, negptppdot), Transform(nrdnegpxplabel, negpxpplabel), Transform(nrdnegptplabel, negptpplabel),
        Transform(nrdnegtplen, negtpplen),self.camera.frame.animate.scale(1.2).shift(DOWN+RIGHT), 
        Transform(nrdprjt, newprjt), Transform(nrdlenpt,newlenpt), Transform(nrdprjtdot, newprjtdot), run_time=3.5)
        self.bring_to_front(negpxppdot)
        self.play(Indicate(nrdnegtplen), Indicate(newlenpt))


        lvc2pt = Dot(gli(negevent0tpp, ax.y_axis)).set_color(MAROON_C)
        mlvc2 = Line(start=lvc2pt.get_top(),end=OG).set_color(MAROON_C)
        mdeltlabel = MathTex("-\Delta t").next_to(mlvc2, RIGHT).set_color(MAROON_C)
        lt_to_lvc2 = Arrow(start=negptppdot.get_center(),end=lvc2pt.get_left(), buff=0.01)
        lt_to_lvc2eq = MathTex(r"-\Delta t =\frac{1}{\gamma}\left(t' + \frac{v}{c^2}x'\right)").next_to(LTforB3, DOWN)
        lt_to_lvc2eq2 = MathTex(r"- \Delta t = -\frac{\Delta t'}{\gamma}").next_to(LTforB3, DOWN)
        lt_to_lvc2eq3 = MathTex(r"\Delta t = \frac{\Delta t'}{\gamma} = \frac{1}{\gamma} \left(\gamma\frac{Lv}{c^2}\right)").next_to(LTforB3, DOWN).set_color(MAROON_C)
        lt_to_lvc2eq4 = MathTex(r"\Delta t = \frac{Lv}{c^2}").next_to(LTforB3, DOWN*2.5).scale(1.6).set_color(MAROON_C)
        boxit = SurroundingRectangle(lt_to_lvc2eq4, color=MAROON_C)

        self.play(Create(lvc2pt))
        self.play(self.camera.frame.animate.scale(0.65).shift(DOWN*2+LEFT),run_time=3.5)
        self.play(Create(lt_to_lvc2))
        self.wait(2)
        self.play(Transform(lt_to_lvc2, lt_to_lvc2eq))
        self.wait(2)
        self.play(Transform(lt_to_lvc2, lt_to_lvc2eq2))
        self.wait(2)
        self.play(Create(mlvc2),Create(mdeltlabel))
        self.play(Indicate(newlenpt), Indicate(negptpplabel))
        self.wait()
        self.play(Indicate(mlvc2), Indicate(mdeltlabel))
        self.wait(2)
        self.play(FadeOut(mdeltlabel), FadeOut(mlvc2))
        self.play(Transform(lt_to_lvc2, lt_to_lvc2eq3))
        self.wait(2)
        self.play(Transform(lt_to_lvc2, lt_to_lvc2eq4))
        self.play(Create(boxit), run_time=2)


        self.wait(10)

