# Pacman Game

A Python implementation of the classic Pacman game using Pygame.

## Features

- Classic Pacman gameplay with modern graphics
- Smooth character animations
- Enemy AI with chase and scatter behavior
- Multiple levels with increasing difficulty
- Score tracking and level progression
- Bonus points collection system

## Installation

1. Make sure you have Python 3.x installed
2. Clone this repository:
```bash
git clone <repository-url>
cd pacman
```

3. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python main.py
```

### Controls
- Use arrow keys to move Pacman
- Collect all bonus points to advance to the next level
- Avoid the ghosts (red and orange)
- Press 'R' to restart when game is over

### Game Rules
- Move Pacman around the maze to collect all bonus points
- Ghosts will chase you but occasionally retreat to their corners
- Complete each level by collecting all bonus points
- Game ends if a ghost catches Pacman

## Project Structure

- `main.py`: Main game logic and loop
- `constants.py`: Game constants and configurations
- `images.py`: Image loading and management
- `images/`: Directory containing game sprites
- `requirements.txt`: Project dependencies

## Dependencies

- Python 3.x
- Pygame 2.5.2

## Building for Distribution

To create a standalone executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create the executable:
```bash
pyinstaller --onefile --windowed main.py
```

The executable will be created in the `dist` directory.

## License

This project is open source and available under the MIT License.
