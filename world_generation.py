import random


def create_brick(c, r, size, padding, offset_top, color):
    return {
        "x": c * (size + padding),
        "y": r * (size + padding) + offset_top,
        "w": size,
        "h": size,
        "color": color,
        "status": 1
    }


def generate_world_data(level, settings):
    cols = settings.get('cols', 35)
    rows = settings.get('rows', 40)
    brick_size = settings.get('brick_size', 11)
    brick_padding = settings.get('brick_padding', 1)
    offset_top = settings.get('offset_top', 60)

    colors = ['#f87171', '#60a5fa', '#4ade80', '#fbbf24', '#a78bfa', '#f472b6', '#2dd4bf']
    current_color = random.choice(colors)

    center_x = (cols - 1) // 2
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    protected = set()

    # Corridor
    corridor_y = random.randint(6, rows - 6)
    for c in range(center_x + 1):
        grid[corridor_y][c] = 0
        protected.add((corridor_y, c))

    # Room Generation
    room_count = random.randint(5, 8)
    room_centers = []

    for _ in range(room_count):
        shape = random.choice(["rect", "diamond", "blob"])
        w = random.randint(6, 12)
        h = random.randint(5, 9)

        cx = random.randint(0, center_x)
        cy = random.randint(3, rows - 4)
        room_centers.append((cx, cy))

        for r in range(cy - h, cy + h):
            if not (0 <= r < rows):
                continue
            for c in range(cx - w, cx + w):
                if not (0 <= c <= center_x):
                    continue

                if (r, c) in protected:
                    continue

                if shape == "rect" and random.random() < 0.65:
                    grid[r][c] = 1
                elif shape == "diamond":
                    if abs(c - cx) + abs(r - cy) < (w + h) // 2 and random.random() < 0.6:
                        grid[r][c] = 1
                elif shape == "blob" and random.random() < 0.45:
                    grid[r][c] = 1

    # Room-Corridor Connections
    for cx, cy in room_centers:
        r = cy
        step = 1 if corridor_y > r else -1
        while r != corridor_y:
            if 0 <= r < rows and 0 <= cx <= center_x:
                grid[r][cx] = 0
                protected.add((r, cx))
            r += step

    # Bottom wall
    wall_probs = [(0, 0.1), (1, 0.15), (2, 0.25), (3, 0.2), (4, 0.2)]
    rnd = random.random()
    acc = 0
    thickness = 0
    for t, p in wall_probs:
        acc += p
        if rnd <= acc:
            thickness = t
            break

    shape_bottom = max((r for r in range(rows) for c in range(center_x + 1) if grid[r][c]), default=0)
    for r in range(shape_bottom + 1, min(rows, shape_bottom + 1 + thickness)):
        for c in range(center_x + 1):
            grid[r][c] = 1

    # Smoothing
    new = [row[:] for row in grid]
    for r in range(1, rows - 1):
        for c in range(1, center_x):
            if (r, c) in protected:
                continue
            n = sum(
                grid[r + i][c + j]
                for i in (-1, 0, 1)
                for j in (-1, 0, 1)
            )
            if n >= 6:
                new[r][c] = 1
            elif n <= 2:
                new[r][c] = 0
    grid = new

    # Add Corridor
    for r in range(2, rows - 2):
        for c in range(2, center_x - 1):
            if (r, c) not in protected and grid[r][c] == 1 and random.random() < 0.12:
                grid[r][c] = 0

    # Crate Brick and Mirror
    bricks = []
    for r in range(rows):
        for c in range(center_x + 1):
            if grid[r][c]:
                bricks.append(create_brick(c, r, brick_size, brick_padding, offset_top, current_color))
                if c != center_x:
                    bricks.append(create_brick(cols - 1 - c, r, brick_size, brick_padding, offset_top, current_color))

    return {
        "config": {
            "canvas_width": cols * (brick_size + brick_padding),
            "canvas_height": 800,
            "paddle_y": 720,
            "drop_chance": settings.get('drop_chance', 1.0),
            "ball_speed": settings.get('ball_speed', 6)
        },
        "bricks": bricks,
        "color": current_color,
        "level": level,
        "saved_score": settings.get('current_score', 0)
    }
