from manim import *
import numpy as np


class LocalityOfPhysics(MovingCameraScene):
    """A Manim scene showing a visible motion as the endpoint of local collisions."""

    def construct(self):
        self.camera.background_color = "#070914"

        self.show_observed_motion()
        self.show_local_cause()
        self.show_full_causal_chain()
        self.final_hold()

    def particle(self, point, color="#45C7FF", radius=0.16, name=None):
        core = Circle(radius=radius)
        core.set_fill(color, opacity=1)
        core.set_stroke(WHITE, width=1.5, opacity=0.9)

        glow = Circle(radius=radius * 1.75)
        glow.set_fill(color, opacity=0.13)
        glow.set_stroke(color, width=2, opacity=0.18)

        body = VGroup(glow, core).move_to(point)
        if name:
            label = Text(name, font_size=20, color=WHITE).next_to(body, DOWN, buff=0.18)
            return VGroup(body, label)
        return body

    def velocity_mark(self, particle, direction=RIGHT, label="v", color="#FFD166"):
        direction = normalize(direction)
        start = particle.get_center() + direction * 0.20 + UP * 0.28
        end = start + direction * 0.82
        arrow = Arrow(
            start,
            end,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=color,
        )
        tex = MathTex(label, color=color).scale(0.72)
        tex.next_to(arrow, UP, buff=0.05)
        return VGroup(arrow, tex)

    def trail(self, start, end, color="#45C7FF"):
        line = DashedLine(start, end, dash_length=0.12, dashed_ratio=0.55)
        line.set_stroke(color, width=3, opacity=0.42)
        return line

    def collision_flash(self, point, color="#FFD166", radius=0.6):
        ring = Circle(radius=0.08).move_to(point)
        ring.set_stroke(color, width=5, opacity=0.95)
        ring.set_fill(color, opacity=0.10)

        sparks = VGroup()
        for angle in np.linspace(0, TAU, 10, endpoint=False):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            spark = Line(point + direction * 0.09, point + direction * 0.28)
            spark.set_stroke(color, width=3, opacity=0.9)
            sparks.add(spark)

        burst = VGroup(ring, sparks)
        burst.set_z_index(10)

        return Succession(
            FadeIn(burst, scale=0.4, run_time=0.06),
            AnimationGroup(
                ring.animate.scale(radius / 0.08).set_stroke(opacity=0).set_fill(opacity=0),
                LaggedStart(
                    *[
                        spark.animate.shift((spark.get_end() - spark.get_start()) * 0.65).set_stroke(opacity=0)
                        for spark in sparks
                    ],
                    lag_ratio=0.035,
                ),
                run_time=0.39,
            ),
        )

    def show_observed_motion(self):
        title = Text("Observed motion", font_size=32, color="#DDE7FF")
        title.to_edge(UP, buff=0.35)

        first = self.particle(LEFT * 1.9, color="#45C7FF", name="A")
        marker = self.velocity_mark(first, RIGHT, "v")
        path = self.trail(first.get_center(), first.get_center() + RIGHT * 2.6)

        self.play(FadeIn(title, shift=DOWN * 0.25), FadeIn(first, scale=0.92), run_time=0.8)
        self.play(GrowArrow(marker[0]), Write(marker[1]), Create(path), run_time=0.8)
        self.play(first.animate.shift(RIGHT * 2.6), marker.animate.shift(RIGHT * 2.6), run_time=1.55)
        self.wait(0.35)
        self.play(FadeOut(path), FadeOut(title), FadeOut(marker), FadeOut(first), run_time=0.55)

    def show_local_cause(self):
        rewind = Text("rewind", font_size=30, color="#B8C7FF").to_edge(UP, buff=0.38)
        first = self.particle(RIGHT * 0.7, color="#45C7FF", name="A")
        incoming = self.particle(LEFT * 3.6, color="#FF6B6B", name="B")
        incoming_arrow = self.velocity_mark(incoming, RIGHT, "v", color="#FFD166")
        local_zone = Circle(radius=0.82, color="#7A88FF").move_to(LEFT * 0.4)
        local_zone.set_stroke("#7A88FF", width=2.5, opacity=0.55)
        local_zone.set_fill("#7A88FF", opacity=0.04)

        self.play(FadeIn(rewind, shift=DOWN * 0.2), FadeIn(first), run_time=0.55)
        self.play(
            first.animate.move_to(LEFT * 0.4),
            Rotate(rewind, angle=TAU, rate_func=there_and_back),
            run_time=1.0,
        )
        self.play(FadeIn(local_zone), FadeIn(incoming), GrowArrow(incoming_arrow[0]), Write(incoming_arrow[1]))
        self.play(incoming_arrow.animate.shift(RIGHT * 2.85), incoming.animate.move_to(LEFT * 0.55), run_time=1.0)
        self.play(
            self.collision_flash(LEFT * 0.45, color="#FFD166", radius=0.62),
            first.animate.shift(RIGHT * 1.45),
            FadeOut(incoming_arrow),
            incoming.animate.set_opacity(0.45),
            run_time=0.68,
        )
        result_arrow = self.velocity_mark(first, RIGHT, "v", color="#FFD166")
        self.play(GrowArrow(result_arrow[0]), Write(result_arrow[1]), run_time=0.45)
        self.wait(0.35)
        self.play(
            *[FadeOut(mob) for mob in [rewind, first, incoming, local_zone, result_arrow]],
            run_time=0.65,
        )

    def show_full_causal_chain(self):
        header = Text("same event, earlier causes", font_size=30, color="#DDE7FF")
        header.to_edge(UP, buff=0.34)

        positions = [
            LEFT * 5.6 + DOWN * 0.1,
            LEFT * 4.2 + UP * 0.62,
            LEFT * 3.0 + DOWN * 0.55,
            LEFT * 1.8 + UP * 0.34,
            LEFT * 0.72 + DOWN * 0.72,
            RIGHT * 0.42 + UP * 0.55,
            RIGHT * 1.55 + DOWN * 0.28,
            RIGHT * 2.68 + UP * 0.34,
            RIGHT * 3.72 + DOWN * 0.2,
        ]

        colors = [
            "#FF6B6B",
            "#2DD4BF",
            "#B8F35A",
            "#F472B6",
            "#A78BFA",
            "#4ADE80",
            "#F59E0B",
            "#38BDF8",
            "#FF6B6B",
        ]

        particles = VGroup(*[self.particle(pos, colors[i]) for i, pos in enumerate(positions)])
        first_particle = self.particle(RIGHT * 5.15 + DOWN * 0.2, color="#45C7FF", name="A")
        first_marker = self.velocity_mark(first_particle, RIGHT, "v", color="#FFD166")

        faint_links = VGroup()
        for a, b in zip(positions[:-1], positions[1:]):
            link = DashedLine(a, b, dash_length=0.08, dashed_ratio=0.45)
            link.set_stroke("#C7D2FE", width=1.7, opacity=0.16)
            faint_links.add(link)

        self.play(FadeIn(header, shift=DOWN * 0.2), FadeIn(particles, lag_ratio=0.08), Create(faint_links), run_time=1.1)

        first_arrow = self.velocity_mark(particles[0], RIGHT, "v", color="#FFD166")
        self.play(GrowArrow(first_arrow[0]), Write(first_arrow[1]), run_time=0.55)

        active_arrow = first_arrow
        for i in range(len(particles) - 1):
            source = particles[i]
            target = particles[i + 1]
            source_start = source.get_center()
            target_start = target.get_center()
            direction = normalize(target_start - source_start)
            impact = target_start - direction * 0.30
            next_shift = direction * 0.54

            self.play(
                source.animate.move_to(impact),
                active_arrow.animate.move_to(impact + UP * 0.42 + direction * 0.28),
                run_time=0.42 if i < 4 else 0.34,
                rate_func=smooth,
            )
            self.play(
                self.collision_flash(target_start, color=colors[(i + 2) % len(colors)], radius=0.44),
                target.animate.shift(next_shift),
                source.animate.set_opacity(0.45),
                FadeOut(active_arrow, shift=direction * 0.2),
                run_time=0.36,
            )
            active_arrow = self.velocity_mark(target, direction, "v", color="#FFD166")
            self.play(GrowArrow(active_arrow[0]), Write(active_arrow[1]), run_time=0.20)

            if i in {2, 4, 5}:
                jitter_group = VGroup(*[p for j, p in enumerate(particles) if j > i + 1])
                if len(jitter_group) > 0:
                    self.play(
                        LaggedStart(
                            *[
                                mob.animate.shift(
                                    np.array([
                                        0.10 * np.sin((j + 1) * 1.7),
                                        0.09 * np.cos((j + 2) * 1.3),
                                        0,
                                    ])
                                )
                                for j, mob in enumerate(jitter_group)
                            ],
                            lag_ratio=0.04,
                        ),
                        run_time=0.22,
                    )

        final_mover = particles[-1]
        final_arrow = active_arrow
        final_start = final_mover.get_center()
        final_hit = first_particle.get_center() + LEFT * 0.30
        final_path = self.trail(final_start, final_hit, color="#FF6B6B")
        incoming_arrow = self.velocity_mark(final_mover, RIGHT, "v", color="#FFD166")

        self.play(
            FadeIn(first_particle),
            Create(final_path),
            ReplacementTransform(final_arrow, incoming_arrow),
            run_time=0.55,
        )
        self.play(
            final_mover.animate.move_to(final_hit),
            incoming_arrow.animate.move_to(final_hit + RIGHT * 0.48 + UP * 0.35),
            run_time=1.0,
            rate_func=smooth,
        )
        self.play(
            self.collision_flash(first_particle.get_center(), color="#FFD166", radius=0.70),
            first_particle.animate.shift(RIGHT * 1.05),
            FadeOut(incoming_arrow),
            FadeOut(final_path),
            final_mover.animate.set_opacity(0.42),
            run_time=0.70,
        )
        self.play(GrowArrow(first_marker[0]), Write(first_marker[1]), run_time=0.45)
        self.wait(0.6)

        self.chain_mobjects = VGroup(header, particles, faint_links, first_particle, first_marker)

    def final_hold(self):
        message = Text("local pushes, global story", font_size=34, color="#DDE7FF")
        message.to_edge(DOWN, buff=0.42)
        glow_line = Line(LEFT * 5.6 + DOWN * 1.25, RIGHT * 5.8 + DOWN * 1.25)
        glow_line.set_stroke("#FFD166", width=4, opacity=0.7)

        self.play(FadeIn(message, shift=UP * 0.18), Create(glow_line), run_time=0.8)
        self.wait(1.2)
