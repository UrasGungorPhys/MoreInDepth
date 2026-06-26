from manim import *
import numpy as np


class test3(MovingCameraScene):
      def construct(self):

        ll = 6  # axis length
        llx = 0.6*12
        axl = 10
        axlx = 12
        axr = [0,axlx,1]  # axis coordinate range
        ayr = [0,axl,1]
        normy = ll/axl
        normx = llx/axlx

        xhat = np.array([1,0,0])
        yhat= np.array([0,1,0])
        pcolor=BLUE_C
        self.camera.background_color = ManimColor.from_hex("#171717")

        # custom colors
        MistyBlue= ManimColor.from_hex("#404e7c")
        ChopinBlue= ManimColor.from_hex("#2a3d45")
        FernGreen= ManimColor.from_rgb([58, 125, 68])
        Mustard= ManimColor.from_rgb([231, 187, 65])
        VibrantPink= ManimColor.from_rgb([219, 39, 99])
        VibrantPink2= ManimColor.from_hex("#BF1363")
        PastelGreen=ManimColor.from_hex("#00AF54")
        VibrantGreen= ManimColor.from_hex("#29BF12")
        LightBlue= ManimColor.from_hex("#08BDBD")
        RedOrange= ManimColor.from_hex("#BA1200")
        SkyBlue= ManimColor.from_hex("#00BBF9")
        OrangeOrange= ManimColor.from_hex("#FF5714")
        NicerOrange= ManimColor.from_hex("#F75C03")
        GoodOrange= ManimColor.from_hex("#E53D00")
        Salmon= ManimColor.from_hex("#C73E1D")
        PastelRed= ManimColor.from_hex("#9E2B25")
        SteelBlue = ManimColor.from_hex("#3F88C5")
        Samoyed = ManimColor.from_hex("#E0E2DB")
        NeonOrange = ManimColor.from_hex("#FE5F00")
        DarkPurple = ManimColor.from_hex("#2f3061")

        gndcolor1 = SkyBlue
        gndcolor2 = SteelBlue
        gndhighlight = LightBlue

        pcolor1 = OrangeOrange
        pcolor2=GoodOrange
        phighlight = NeonOrange

        highlight = VibrantGreen
        propercolor = Samoyed
        lightcolor = Mustard
            

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
            # return testpts
        


        planets_frame = Axes(x_range=axr, y_range=ayr, x_length=llx, y_length=ll,axis_config={"include_ticks": False, "stroke_width":3.5}).set_color(gndcolor1)
        planets_label = planets_frame.get_axis_labels(x_label="x", y_label="t_A").set_color(gndcolor2)
        og = planets_frame.c2p(0,0)

        planets_frame_ext = Axes(x_range=[-24, 24, 1], y_range=[-20,20,1],
         x_length=llx*3, y_length=ll*3,axis_config={"include_ticks": False}).move_to(og).set_color(gndcolor1)

        planets_griddef = NumberPlane(x_range=[0,axlx,1], y_range=[0,axl,1], x_length=llx, y_length=ll,
        background_line_style={"stroke_color": gndcolor2,
                                "stroke_width": 1,
                                "stroke_opacity": 0.5,})

        planets_grid = homemade_grid(planets_frame, xrange=[0,axlx], yrange=[0,axl], colorchoice=gndcolor1)
        planets_gridext = homemade_grid(planets_frame_ext, xrange=[-24,24], yrange=[-20,20], colorchoice=phighlight)
        testdots = VGroup(Dot(planets_frame_ext.c2p(-24, -20), radius=0.2).set_color(phighlight),
                          Dot(planets_frame_ext.c2p(24, 20), radius=0.2).set_color(phighlight))
        
        square = Square(fill_color=RED, fill_opacity=1)
        self.add(square)
        square.set_z_index(1)



        self.play(Create(planets_frame))
        # self.play(Create(planets_griddef))
        self.play(FadeIn(planets_grid))

        # self.play(self.camera.frame.animate.scale(3).move_to(og))
        self.play(Create(testdots))
        self.wait(10)