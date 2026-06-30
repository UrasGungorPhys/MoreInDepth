from pathlib import Path
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TRANSPARENT_BACKGROUND = os.environ.get("TRANSPARENT_BACKGROUND") == "1"
FRAME_SUBDIR = os.environ.get(
    "FRAME_SUBDIR",
    "particle_collision_frames_alpha" if TRANSPARENT_BACKGROUND else "particle_collision_frames",
)
FRAME_DIR = ROOT / "work" / FRAME_SUBDIR

WIDTH = 3840
HEIGHT = 2160
FPS = 60
SIM_TIME = 11.0
DT = 1 / 300
RENDER_EVERY = int(round(1 / (FPS * DT)))

RADIUS = 0.105
MIN_DIST = 2 * RADIUS
RESTITUTION = 0.992
DRAW_RADIUS_SCALE = 0.64

WORLD_X = (-6.2, 7.4)
WORLD_Y = (-3.85, 3.85)
SEED = 18
BACKGROUND_RGB = (20, 29, 41)
BACKGROUND_RGBA = (*BACKGROUND_RGB, 0 if TRANSPARENT_BACKGROUND else 255)
FOLLOW_START = 5.6
FOLLOW_END = 8.0
VELOCITY_LABEL_START = FOLLOW_END + 0.35


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT = load_font(28)
FONT_SMALL = load_font(22)
FONT_BOLD = load_font(32, bold=True)
VELOCITY_FONT = load_font(92, bold=True)


def make_initial_state():
    rng = np.random.default_rng(SEED)

    positions = [np.array([-5.75, 0.04], dtype=float)]
    velocities = [np.array([3.45, 0.01], dtype=float)]

    spacing_factor = 1.45
    spacing = MIN_DIST * spacing_factor
    dy = math.sqrt(3) * RADIUS * spacing_factor

    # A loose, imperfect hex cloud. There is enough empty space between disks
    # for individual collisions to read before the cascade becomes chaotic.
    for row in range(-5, 6):
        row_width = 11 - max(0, abs(row) - 1)
        y = row * dy
        x_start = -1.05 - 0.5 * spacing * (row_width - 1)
        for col in range(row_width):
            x = x_start + col * spacing + (0.5 * spacing if row % 2 else 0)
            if ((x - 0.02) / 2.10) ** 2 + (y / 1.75) ** 2 > 1.03:
                continue
            jitter = rng.normal(0, 0.014, size=2)
            positions.append(np.array([x, y], dtype=float) + jitter)
            velocities.append(np.zeros(2, dtype=float))

    return np.array(positions), np.array(velocities)


def resolve_overlaps_once(positions):
    n_particles = len(positions)
    for _ in range(16):
        moved = False
        for i in range(n_particles - 1):
            for j in range(i + 1, n_particles):
                delta = positions[j] - positions[i]
                dist2 = float(np.dot(delta, delta))
                if dist2 >= MIN_DIST * MIN_DIST:
                    continue
                dist = math.sqrt(dist2) if dist2 > 1e-12 else MIN_DIST
                normal = delta / dist if dist > 1e-12 else np.array([1.0, 0.0])
                overlap = MIN_DIST - dist
                positions[i] -= 0.5 * overlap * normal
                positions[j] += 0.5 * overlap * normal
                moved = True
        if not moved:
            break


def simulate():
    positions, velocities = make_initial_state()
    resolve_overlaps_once(positions)

    n_particles = len(positions)
    active_time = np.full(n_particles, np.inf)
    active_time[0] = 0.0

    position_frames = []
    velocity_frames = []
    collision_events = []
    collision_count = 0

    total_steps = int(SIM_TIME / DT)
    for step in range(total_steps + 1):
        if step % RENDER_EVERY == 0:
            position_frames.append(positions.copy())
            velocity_frames.append(velocities.copy())

        if step == total_steps:
            break

        positions += velocities * DT
        t = (step + 1) * DT

        # Two passes keep dense, simultaneous contacts from tunneling through.
        for _ in range(2):
            for i in range(n_particles - 1):
                for j in range(i + 1, n_particles):
                    delta = positions[j] - positions[i]
                    dist2 = float(np.dot(delta, delta))
                    if dist2 >= MIN_DIST * MIN_DIST:
                        continue

                    if dist2 < 1e-12:
                        normal = np.array([1.0, 0.0])
                        dist = MIN_DIST
                    else:
                        dist = math.sqrt(dist2)
                        normal = delta / dist

                    overlap = MIN_DIST - dist
                    positions[i] -= 0.5 * overlap * normal
                    positions[j] += 0.5 * overlap * normal

                    relative_velocity = velocities[j] - velocities[i]
                    normal_speed = float(np.dot(relative_velocity, normal))
                    if normal_speed >= 0:
                        continue

                    impulse = -(1 + RESTITUTION) * normal_speed / 2
                    impulse_vector = impulse * normal
                    velocities[i] -= impulse_vector
                    velocities[j] += impulse_vector

                    collision_count += 1
                    collision_events.append((t, (positions[i] + positions[j]) * 0.5))

                    i_active = math.isfinite(active_time[i])
                    j_active = math.isfinite(active_time[j])
                    if i_active and not j_active:
                        active_time[j] = t
                    elif j_active and not i_active:
                        active_time[i] = t

    return {
        "positions": np.array(position_frames),
        "velocities": np.array(velocity_frames),
        "active_time": active_time,
        "collision_events": collision_events,
        "collision_count": collision_count,
    }


def choose_isolated_particle(data):
    final_positions = data["positions"][-1]
    final_velocities = data["velocities"][-1]
    active = np.isfinite(data["active_time"])
    speeds = np.linalg.norm(final_velocities, axis=1)

    delta = final_positions[:, None, :] - final_positions[None, :, :]
    distances = np.linalg.norm(delta, axis=2)
    np.fill_diagonal(distances, np.inf)
    nearest = distances.min(axis=1)

    active_positions = final_positions[active]
    center = np.median(active_positions, axis=0) if len(active_positions) else np.array([0.0, 0.0])
    radial = np.linalg.norm(final_positions - center, axis=1)

    score = 2.2 * nearest + 0.7 * radial + 1.0 * speeds
    score[~active] = -np.inf
    score[0] = -np.inf
    score[speeds < 0.18] -= 2.0

    selected = int(np.argmax(score))
    if not np.isfinite(score[selected]):
        selected = int(np.argmax(np.where(active, speeds, -np.inf)))
    return selected


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def viewport_at(t, selected_position, selected_velocity):
    fixed_center = np.array([(WORLD_X[0] + WORLD_X[1]) * 0.5, (WORLD_Y[0] + WORLD_Y[1]) * 0.5])
    fixed_width = WORLD_X[1] - WORLD_X[0]

    amount = smoothstep((t - FOLLOW_START) / (FOLLOW_END - FOLLOW_START))

    target_center = np.array(selected_position, dtype=float)
    center = (1 - amount) * fixed_center + amount * target_center
    width = (1 - amount) * fixed_width + amount * 5.6
    height = width * HEIGHT / WIDTH
    speed = np.linalg.norm(selected_velocity)
    target_angle = math.atan2(selected_velocity[1], selected_velocity[0]) if speed > 1e-6 else 0.0
    angle = amount * target_angle
    return center, width, height, angle


def world_to_px(point, viewport):
    center, width, height, angle = viewport
    rel = np.array(point, dtype=float) - center
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rotated = np.array(
        [
            cos_a * rel[0] + sin_a * rel[1],
            -sin_a * rel[0] + cos_a * rel[1],
        ]
    )
    x = WIDTH * 0.5 + rotated[0] / width * WIDTH
    y = HEIGHT * 0.5 - rotated[1] / height * HEIGHT
    return np.array([x, y], dtype=float)


def world_radius_to_px(radius, viewport):
    _, width, _, _ = viewport
    return radius / width * WIDTH


def world_vector_to_px(vector, viewport):
    _, width, height, angle = viewport
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rotated = np.array(
        [
            cos_a * vector[0] + sin_a * vector[1],
            -sin_a * vector[0] + cos_a * vector[1],
        ]
    )
    return np.array(
        [
            rotated[0] / width * WIDTH,
            -rotated[1] / height * HEIGHT,
        ],
        dtype=float,
    )


def mix(a, b, amount):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return tuple(np.clip((1 - amount) * a + amount * b, 0, 255).astype(int))


def draw_marble(draw, center, radius, color, glow_alpha=18, fill_alpha=255, outline_alpha=110):
    x, y = center
    for factor, alpha in [(1.55, glow_alpha)]:
        r = radius * factor
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*color, alpha))

    rim = mix(color, (20, 24, 34), 0.34)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*rim, fill_alpha))

    for step in range(7, 0, -1):
        amount = step / 7
        r = radius * (0.18 + 0.76 * amount)
        offset = np.array([-0.08 * radius * (1 - amount), -0.10 * radius * (1 - amount)])
        shade = mix(color, (255, 255, 255), 0.18 * (1 - amount))
        draw.ellipse(
            (
                x + offset[0] - r,
                y + offset[1] - r,
                x + offset[0] + r,
                y + offset[1] + r,
            ),
            fill=(*shade, fill_alpha),
        )

    highlight_center = np.array([x - radius * 0.36, y - radius * 0.38])
    highlight_radius = radius * 0.22
    draw.ellipse(
        (
            highlight_center[0] - highlight_radius,
            highlight_center[1] - highlight_radius,
            highlight_center[0] + highlight_radius,
            highlight_center[1] + highlight_radius,
        ),
        fill=(255, 255, 255, 95),
    )
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=(255, 255, 255, outline_alpha), width=1)


def draw_arrow(draw, start, end, color, width=5, tip_length=None, tip_width=None):
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direction = end - start
    length = np.linalg.norm(direction)
    if length < 1:
        return
    direction /= length
    normal = np.array([-direction[1], direction[0]])
    tip_len = min(length * 0.42, tip_length if tip_length is not None else max(28, width * 4.2))
    tip_w = tip_width if tip_width is not None else max(16, width * 2.2)
    shaft_end = end - direction * tip_len * 0.72
    draw.line((tuple(start), tuple(shaft_end)), fill=color, width=width)
    p1 = end
    p2 = end - direction * tip_len + normal * tip_w
    p3 = end - direction * tip_len - normal * tip_w
    draw.polygon([tuple(p1), tuple(p2), tuple(p3)], fill=color)


def draw_velocity_label(draw, center, velocity_px, radius, opacity):
    speed = np.linalg.norm(velocity_px)
    if speed < 1e-4 or opacity <= 0:
        return

    direction = velocity_px / speed
    normal = np.array([-direction[1], direction[0]])
    start = center
    end = start + direction * radius * 5.0
    alpha = int(255 * opacity)
    arrow_color = (255, 230, 135, alpha)
    draw_arrow(
        draw,
        start,
        end,
        arrow_color,
        width=max(6, int(radius * 0.20)),
        tip_length=radius * 1.10,
        tip_width=radius * 0.44,
    )

    label_pos = end + normal * radius * 0.78 - direction * radius * 0.08
    draw.text(tuple(label_pos), "v", font=VELOCITY_FONT, anchor="mm", fill=(255, 235, 150, alpha))


def draw_trail(draw, points, color, viewport, width=3):
    if len(points) < 2:
        return
    for idx in range(1, len(points)):
        a = world_to_px(points[idx - 1], viewport)
        b = world_to_px(points[idx], viewport)
        alpha = int(25 + 180 * idx / max(1, len(points) - 1))
        draw.line((tuple(a), tuple(b)), fill=(*color, alpha), width=width)


def draw_background(draw, viewport):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=BACKGROUND_RGBA)


def render_frames(data, selected):
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    for existing in FRAME_DIR.glob("frame_*.png"):
        existing.unlink()

    positions = data["positions"]
    velocities = data["velocities"]
    active_time = data["active_time"]
    collision_events = data["collision_events"]

    palette = [
        (69, 199, 255),
        (255, 107, 107),
        (45, 212, 191),
        (184, 243, 90),
        (244, 114, 182),
        (167, 139, 250),
        (74, 222, 128),
        (245, 158, 11),
        (56, 189, 248),
    ]
    colors = [palette[i % len(palette)] for i in range(positions.shape[1])]
    colors[0] = (255, 209, 102)

    event_cursor = 0
    recent_events = []

    for frame_idx, frame_positions in enumerate(positions):
        t = frame_idx / FPS
        viewport = viewport_at(t, frame_positions[selected], velocities[frame_idx, selected])
        contact_radius_px = world_radius_to_px(RADIUS, viewport)
        radius_px = contact_radius_px * DRAW_RADIUS_SCALE
        img = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND_RGBA)
        draw = ImageDraw.Draw(img, "RGBA")
        draw_background(draw, viewport)

        while event_cursor < len(collision_events) and collision_events[event_cursor][0] <= t:
            recent_events.append(collision_events[event_cursor])
            event_cursor += 1
        recent_events = [event for event in recent_events if t - event[0] < 0.18]

        if frame_idx > 1:
            draw_trail(
                draw,
                positions[max(0, frame_idx - 42) : frame_idx + 1, 0, :],
                (255, 209, 102),
                viewport,
                width=3,
            )

        selected_active = math.isfinite(active_time[selected]) and t >= active_time[selected]
        if selected_active and frame_idx > 10:
            start = max(0, frame_idx - 90)
            draw_trail(draw, positions[start : frame_idx + 1, selected, :], (255, 235, 153), viewport, width=4)

        for event_t, event_pos in recent_events:
            age = t - event_t
            amount = max(0.0, 1.0 - age / 0.18)
            center = world_to_px(event_pos, viewport)
            ring_radius = contact_radius_px * (0.85 + 2.2 * age / 0.18)
            alpha = int(85 * amount)
            draw.ellipse(
                (
                    center[0] - ring_radius,
                    center[1] - ring_radius,
                    center[0] + ring_radius,
                    center[1] + ring_radius,
                ),
                outline=(255, 218, 121, alpha),
                width=1,
            )

        order = np.argsort(frame_positions[:, 1])
        for particle_idx in order:
            center = world_to_px(frame_positions[particle_idx], viewport)
            was_hit = t >= active_time[particle_idx]

            if particle_idx == selected and selected_active:
                base = (255, 227, 121)
                fill_alpha = 255
                glow_alpha = 70
            elif was_hit:
                age = max(0.0, t - active_time[particle_idx])
                flash = max(0.0, 1.0 - age / 0.45)
                base = mix(colors[particle_idx], (255, 255, 255), 0.35 * flash)
                fill_alpha = 245
                glow_alpha = 28
            else:
                base = (92, 101, 125)
                fill_alpha = 160
                glow_alpha = 8

            draw_marble(draw, center, radius_px, base, glow_alpha=glow_alpha, fill_alpha=fill_alpha)

        if selected_active and t > SIM_TIME * 0.70:
            center = world_to_px(frame_positions[selected], viewport)
            pulse = 1 + 0.12 * math.sin(2 * math.pi * 2.0 * t)
            r = radius_px * 2.45 * pulse
            draw.ellipse(
                (center[0] - r, center[1] - r, center[0] + r, center[1] + r),
                outline=(255, 235, 153, 150),
                width=2,
            )

        if selected_active and t > VELOCITY_LABEL_START:
            center = world_to_px(frame_positions[selected], viewport)
            opacity = smoothstep((t - VELOCITY_LABEL_START) / 0.55)
            velocity_px = world_vector_to_px(velocities[frame_idx, selected], viewport)
            draw_velocity_label(draw, center, velocity_px, radius_px, opacity)

        frame_path = FRAME_DIR / f"frame_{frame_idx:04d}.png"
        if TRANSPARENT_BACKGROUND:
            img.save(frame_path)
        else:
            img.convert("RGB").save(frame_path, quality=95)


def main():
    data = simulate()
    selected = choose_isolated_particle(data)
    render_frames(data, selected)

    final_speed = float(np.linalg.norm(data["velocities"][-1, selected]))
    print(f"frames={len(data['positions'])}")
    print(f"particles={data['positions'].shape[1]}")
    print(f"collisions={data['collision_count']}")
    print(f"selected_particle={selected}")
    print(f"selected_final_speed={final_speed:.3f}")
    print(f"frame_dir={FRAME_DIR}")


if __name__ == "__main__":
    main()
