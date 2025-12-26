# Flappy Bird Game

A classic Flappy Bird game implementation using Python and Pygame.

## Features

- **Classic Gameplay**: Tap to flap and navigate through pipes
- **Smooth Physics**: Realistic gravity and flapping mechanics
- **Collision Detection**: Accurate collision with pipes and boundaries
- **Score Tracking**: Keep track of your high score
- **Game States**: Start screen, active gameplay, and game over screen
- **Simple Controls**: Use spacebar or mouse click to play

## Installation

1. Make sure you have Python 3.7+ installed on your system

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
```

3. Install the required dependencies:
```bash
./venv/bin/pip install -r requirements.txt
```

Or install Pygame directly:
```bash
./venv/bin/pip install pygame
```

## How to Run

### Easy Method (Recommended)
Simply run the provided script:
```bash
./run.sh
```

### Manual Method
Navigate to the game directory and run:
```bash
./venv/bin/python flappy_bird.py
```

## Controls

- **SPACE** or **Mouse Click**: Flap the bird's wings
- **SPACE** or **Mouse Click** (on start screen): Start the game
- **SPACE** or **Mouse Click** (on game over): Restart the game

## Gameplay

- Guide the yellow bird through the green pipes
- Each pipe you pass increases your score by 1
- Avoid hitting the pipes or the ground
- Try to beat your high score!

## Requirements

- Python 3.7+
- Pygame 2.5.0+

## Game Mechanics

- **Gravity**: The bird constantly falls due to gravity
- **Flapping**: Each flap gives the bird an upward boost
- **Pipes**: Randomly positioned pipes scroll from right to left
- **Collision**: Game ends if the bird hits a pipe or the boundaries

Enjoy playing Flappy Bird!
