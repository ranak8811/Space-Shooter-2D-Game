# Space Shooter 2D Game

This is a 2D space shooter game implemented using OpenGL and GLUT in Python. Two players control spaceships and try to shoot each other down while avoiding collisions with the walls.

## Table of Contents

- [How to Run](#how-to-run)
- [How to Play](#how-to-play)
- [Game Controls](#game-controls)
- [Game Mechanics](#game-mechanics)
- [Features](#features)
- [Dependencies](#dependencies)
- [Code Structure](#code-structure)
- [Future Improvements](#future-improvements)

## How to Run

1.  **Install Python:** If you don't have Python installed, download and install the latest version from [python.org](https://www.python.org/).
2.  **Install Dependencies:** Open your terminal or command prompt and install the required libraries using pip:

    ```bash
    pip install pyopengl pyopengl-accelerate
    ```

3.  **Clone the Repository (Optional):** If you have the code in a repository (like GitHub), clone it:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

4.  **Run the Game:** Navigate to the directory containing the Python script (`your_script_name.py`) and run it:

    ```bash
    python your_script_name.py
    ```

## How to Play

The game features two players. Each player controls a spaceship and can shoot bullets at the other player. The goal is to deplete the other player's health to zero.

## Game Controls

**Player 1:**

- **W:** Move Up
- **S:** Move Down
- **D:** Shoot

**Player 2:**

- **Up Arrow:** Move Up
- **Down Arrow:** Move Down
- **Left Arrow:** Shoot

**Other Controls:**

- **N:** Increase Night (Darkens background, lowers sun)
- **M:** Increase Day (Lightens background, raises sun)
- **Click on Pause Button (Top Left):** Pause/Resume the game.
- **Click on Cross Button (Top Right):** Exit the game.
- **Click on Restart Button (Top Middle):** Restart the game.

## Game Mechanics

- **Health:** Each player starts with 10 health points. Successful shots reduce the opponent's health by 1.
- **Score:** Each successful hit increases the player's score by 1.
- **Walls:** There are two walls in the middle of the screen. Bullets cannot pass through them. The walls gradually decrease in height over time, making it easier to hit the opponent.
- **Bullets:** Players can shoot bullets with a cooldown period to prevent rapid firing.
- **Game Over:** The game ends when one player's health reaches zero. The player with the higher score wins.
- **Day/Night Cycle:** The 'N' and 'M' keys control a simple day/night cycle, changing the background color and the sun's position and color.

## Features

- Two-player gameplay.
- Dynamic wall height.
- Bullet shooting with cooldown.
- Health and score tracking.
- Game over condition.
- Pause/Resume functionality.
- Restart functionality.
- Day/Night cycle.
- Graphical representation of players, walls, bullets, and environment.

## Dependencies

- Python 3
- PyOpenGL
- PyOpenGL-accelerate

## Code Structure

The code is organized into several functions:

- `draw_player1()`, `draw_player2()`: Draw the player spaceships.
- `draw_walls()`: Draws the walls.
- `draw_bullets()`: Draws the bullets.
- `move_player1()`, `move_player2()`: Handles player movement.
- `shoot_bullet()`: Handles shooting.
- `check_bullet_collision()`: Detects collisions between bullets and players.
- `move_bullets()`: Updates bullet positions.
- `showScreen()`: Main display function, draws all elements.
- `keyboardListener()`, `specialKeyListener()`: Handles keyboard input.
- `mouseListener()`: Handles mouse input for buttons.
- `draw_text()`: Draws text on the screen.
- `draw_pause_button()`, `draw_cross_button()`, `draw_restart_button()`: Draws interactive buttons.
- `getBackgroundColor()`: Controls the background color based on the day/night cycle.
- `getSunColor()`: Controls the sun's color based on the day/night cycle.
- `draw_sun()`: Draws the sun and its rays.
- `draw_river()`: Draws the river.
- Helper functions for drawing basic shapes (lines, circles, points).

## Future Improvements

- Add sound effects.
- Implement a more sophisticated menu system.
- Improve collision detection.
- Add power-ups or other game elements.
- Refactor the code for better organization and readability.
- Add AI opponent for single-player mode.
- Implement different levels or difficulty settings.
