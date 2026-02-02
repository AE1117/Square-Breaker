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
- Some Boosts
<img width="303" height="203" alt="image" src="https://github.com/user-attachments/assets/a4ac7e24-ba81-42c9-a770-6136866bf295" />


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
  
<img width="520" height="886" alt="image" src="https://github.com/user-attachments/assets/fd71e1a5-e275-48e0-9de8-1d3077baaf49" />

# Main Corridor

Every generated level includes:
- One main corridor
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

# Bottom Wall System

The bottom wall behaves as a post-generation constraint:
- Wall thickness is probabilistic
- Wall starts exactly where the generated shape ends
- No wall is allowed to intrude upward into the playable area
 -Thicker walls are rarer by design
This creates variation without breaking gameplay balance.

<img width="535" height="884" alt="image" src="https://github.com/user-attachments/assets/39fe09f8-ac76-4169-a55c-135844906444" />

<img width="527" height="886" alt="image" src="https://github.com/user-attachments/assets/c8191d10-72de-45e6-9b2d-a7981804104f" />

# Density Control and Smoothing

To avoid noise and overfill:
- A limited smoothing pass is applied
- Corridor cells are explicitly protected
- A global thinning pass randomly removes excess bricks
- Density never approaches full solid fill

Result:
- readable negative space
- fewer repetitive blobs
- preserved paths

# Determinism and Constraints

The generator strictly respects:
- User-defined map dimensions
- Fixed input/output schema
- No mutation of UI expectations

This makes the system safe to:
- reuse
- cache
- test
- extend

# Design Goals
- Keep gameplay familiar
- Make level geometry unpredictable but readable
- Avoid “noise-only” randomness
- Preserve symmetry without monotony
- Allow future extensions:
        + vertical corridors
        + multi-corridor layouts
        + special zones
        + boss walls

# Future Work

Possible extensions without breaking the architecture:
- Multiple main corridors
- Vertical or L-shaped corridors
- Dynamic difficulty scaling
- Power-up-biased regions
- Boss arenas using wall thickness logic

# License

This project is intended for experimentation, learning, and iteration.
Use, modify, and extend freely.

