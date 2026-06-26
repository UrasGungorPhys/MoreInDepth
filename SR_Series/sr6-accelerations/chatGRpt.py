from manim import *
import numpy as np

class NewtonianPotentialSurfaces(ThreeDScene):
    def construct(self):
        # Camera / view
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        # zoom out so both sheets + sphere fit nicely
        # (ThreeDCamera has set_zoom)
        self.camera.set_zoom(0.7)

        # Central mass (the "sun")
        sphere_radius = 1.0
        sun = Sphere(radius=sphere_radius, resolution=(64, 64), color=YELLOW)
        # Add a soft glowing shell to look more sun-like
        glow = Sphere(radius=sphere_radius * 1.06, resolution=(64, 64),
                      color=YELLOW, fill_opacity=0.15, stroke_width=0)

        # Physical / plotting parameters (choose GM=1 for simplicity)
        GM = 1.0
        eps = 0.3   # softening to avoid singularity at r=0
        # Surface scaling: converts energy units to visible height
        height_scale = 0.9

        # Effective potential (per unit test-mass)
        def Veff(r, L):
            # Use r+eps in attractive term to avoid blow-up at r=0
            return -GM / (r + eps) + 0.5 * (L**2) / (r**2 + 1e-9)

        # Height mapping: we invert sign so deep potential wells appear as *dips*
        # above the sphere (i.e. surfaces hover and show valleys)
        def height_from_r(r, L, base_height):
            # careful: we want a smooth falloff to zero at large r,
            # so map Veff -> z by -Veff * scale
            return base_height - height_scale * Veff(r, L)

        # Parametric surface factory: returns a function (u,v) -> (x,y,z)
        def potential_surface_func(L, base_height):
            def func(u, v):
                r = np.sqrt(u * u + v * v)
                z = height_from_r(r, L, base_height)
                return np.array([u, v, z])
            return func

        # Two surfaces: inner (closer, stronger curvature), outer (further, milder)
        L1 = 1.2    # angular momentum for inner sheet -> r_circ = L1^2 / GM
        L2 = 1.6    # for outer sheet

        # compute circular orbit radii (exact from dVeff/dr = 0 => L^2 = GM r)
        # check arithmetic carefully:
        # r_circ = L^2 / GM
        r_circ1 = (L1 ** 2) / GM  # e.g. 1.44 if L1=1.2 and GM=1
        r_circ2 = (L2 ** 2) / GM  # e.g. 2.56 if L2=1.6 and GM=1

        # choose base heights so surfaces float above the sphere cleanly:
        inner_base = sphere_radius + 0.35   # close above the sphere
        outer_base = sphere_radius + 1.15   # higher up

        # surfaces with sparse mesh so you can see through:
        inner_surface = Surface(
            potential_surface_func(L1, inner_base),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0,
            stroke_color=BLUE_A,
            stroke_width=1.0,
        )

        outer_surface = Surface(
            potential_surface_func(L2, outer_base),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(20, 20),
            fill_opacity=0,
            stroke_color=BLUE_E,
            stroke_width=1.0,
        )

        # Rings marking the circular-orbit radii (projected onto the corresponding surface)
        def z_at_radius(r, L, base_height):
            # same mapping as used in the surface
            return height_from_r(r, L, base_height)

        ring1 = Circle(radius=r_circ1, stroke_color=RED, stroke_width=3).move_to(
            np.array([0, 0, z_at_radius(r_circ1, L1, inner_base)])
        )
        ring2 = Circle(radius=r_circ2, stroke_color=ORANGE, stroke_width=3).move_to(
            np.array([0, 0, z_at_radius(r_circ2, L2, outer_base)])
        )

        # Slight rotation of rings to sit flush on curved surface (visually)
        # rotate around x-axis by small amount so they don't clip with sphere when rendered
        ring1.rotate(0.0, axis=RIGHT)  # keep in XY plane but at z>0
        ring2.rotate(0.0, axis=RIGHT)

        # Add everything
        self.add(sun, glow, inner_surface, outer_surface, ring1, ring2)

        # Add labels for clarity (optional)
        label1 = Text(f"r_circ={r_circ1:.2f}", font_size=24).next_to(
            ring1, UP + RIGHT, buff=0.2
        ).shift(IN * 0.5).set_z(z_at_radius(r_circ1, L1, inner_base) + 0.05)
        label2 = Text(f"r_circ={r_circ2:.2f}", font_size=24).next_to(
            ring2, UP + RIGHT, buff=0.2
        ).shift(IN * 0.5).set_z(z_at_radius(r_circ2, L2, outer_base) + 0.05)

        # small animation to introduce elements
        self.play(FadeIn(sun), FadeIn(glow))
        self.play(Create(inner_surface), Create(outer_surface))
        self.play(Create(ring1), Create(ring2))
        self.wait(0.5)
        self.play(FadeIn(label1), FadeIn(label2))
        # subtle camera rotation to show 3D
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
