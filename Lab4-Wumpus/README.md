# Hunt the Wumpus

A classic text-based adventure game "Hunt the Wumpus". Currently, 20 rooms are implemented. 

## Overview

- The player starts in a random cave room.
- Hazards include:
    - **Wumpus**: one lurking creature; if you enter its room, you lose.
    - **Pits**: two bottomless pits; falling in ends the game.
    - **Bats**: two super-bats; if encountered, you’re carried to a random room (and may face hazards again).
- You have 5 arrows to shoot through up to three adjacent rooms in an attempt to slay the Wumpus.
- Sensory hints warn of nearby hazards:
    - "You smell a terrible stench." (Wumpus nearby)
    - "You feel a breeze." (Pit nearby)
    - "You hear rustling of bat wings." (Bat nearby)


## Gameplay Instructions

1. **Move (M)** or **Shoot (S)** each turn.  
2. If you choose **Move**:  
    - Enter the number of one of the three tunnels adjacent to your current room.  
    - You may be eaten, fall into a pit, or get carried by bats.  
3. If you choose **Shoot**:  
    - Input up to three adjacent room numbers to direct your arrow’s path.  
    - Arrows ricochet if you specify a non-adjacent room, randomly choosing an adjacent tunnel.  
    - If your arrow returns to your room, it kills you instantly.  
    - After a miss, the Wumpus may wake and move (75% chance).  
4. **Win** by killing the Wumpus. **Lose** if eaten, fall into a pit, or shot yourself.

## Code Structure

- `CAVE`: Adjacency list defining the 20-room dodecahedral cave.  
- `WumpusGame` class:  
    - `reset_game()`: Randomly places hazards and player.  
    - `adjacent_hazards()`: Returns sensory warnings for current room.  
    - `move_player(room)`: Handles movement and hazard checks.  
    - `shoot_arrow(path)`: Processes arrow shooting and Wumpus movement.  
    - `move_wumpus()`: Randomly moves the Wumpus after missed shot.  
    - `play()`: Main loop handling user input and game state.  

## Game Mechanics Details

- **Hazard Placement**: All placements are random at each new game.  
- **Sensory Feedback**: Only immediate neighbors are checked for hazards.  
- **Arrow Physics**:  
    - Up to three-room trajectory.  
    - Invalid room in path → arrow ricochets randomly.  
    - Self-inflicted death if arrow loops back.  
- **Wumpus Mobility**: After a missed shot, the Wumpus moves with a 75% probability.  

