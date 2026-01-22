# Square-Breaker
Advanced Procedural Brick Breaker

This project is a procedural world–driven brick breaker game that combines the classical block-breaking mechanics with roguelike-inspired level generation.


The core idea is simple:
----------------------------------------
The gameplay is deterministic and familiar,
but the level geometry is never trivial.
----------------------------------------

# Overview

The game consists of two main layers:

1) Gameplay Layer (UI / Runtime)
- Classic brick breaker mechanics
- Paddle, ball, collision-based brick destruction
- No procedural logic here

2) World Generation Layer
- Generates complex brick layouts dynamically
- Inspired by dungeon generation and roguelike design
- Strictly bounded by user-defined map dimensions

This separation allows the UI to stay simple while the world logic evolves independently.

# Gameplay (UI Layer)

The UI behaves exactly like a traditional brick breaker game:
- Player controls a horizontal paddle
- A ball bounces inside the canvas
- Bricks are destroyed on collision

The UI does not decide:
- where bricks are placed
- how dense the level is
- where corridors or walls exist

It only consumes structured data produced by the generator.

# World Generation System
# Grid-Based World Model

The world is generated on a discrete grid:
- Each cell represents a potential brick
- The grid size is configurable:
    + columns
    + rows
    + brick size
    + padding
- The generator only fills the left half of the grid
- The right half is created via mirroring for symmetry
  
This guarantees:
- visual balance
- predictable canvas size
- performance stability
  
<img width="538" height="880" alt="image" src="https://github.com/user-attachments/assets/fd7406a7-4488-40c6-82b2-df31e2e5a084" />

# Guaranteed Main Corridor

Every generated level includes:
- One guaranteed main corridor
- Orientation: horizontal
- Position: randomized vertically
- The corridor is:
        + continuous
        + never filled by smoothing
        + protected from density operations

This ensures:
- navigability
- visual readability
- consistent gameplay flow

<img width="536" height="885" alt="image" src="https://github.com/user-attachments/assets/e577d302-8c04-45f5-a151-e8fd8955f15f" />

# Room and Shape Generation

Rooms are generated using mixed shape logic:
- Rectangular regions
- Diamond-like regions
- Organic “blob” regions

Key properties:
- Shapes may overlap
- Shapes may touch walls
- Shapes may be partially outside bounds (automatically clipped)
Density is intentionally limited to avoid overfilling.

<img width="535" height="884" alt="image" src="https://github.com/user-attachments/assets/39fe09f8-ac76-4169-a55c-135844906444" />


