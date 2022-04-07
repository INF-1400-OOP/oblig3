# Oblig 3 - OOP

*Author: Christian Salomonsen - csa047*

---

## TOC

1. [Usage](#usage)
2. [Requirements](#requirements)
3. [Todo](#todo)

---

## Usage

To run the game, navigate to `src/`. Then run `python3 main.py`.

Controls are configured such that player 1 (left screen) use `wasd` and player 2 (right screen) use `arrow` keys.

---

## Requirements

The game requires a python version >= 3.9, therefore make sure to use the correct version of python when executing `main.py`. Check your Python version with `python3 -V`.

### Libraries used

1. [Numpy](https://pypi.org/project/numpy/)
2. [Pygame](https://pypi.org/project/pygame/)

### Installing libraries to current Python version

A `requirements.txt` has been provided, therefore you can install these when in `src/` directory with:

`pip3 install -r requirements.txt`

## TODO

- [x] Map module which reads map text file
- [x] Implement camera in main game
- [x] Implement gravity
- [x] Implement rotation on player
- [x] Actual well-ish designed map
- [x] More textures - piskelApp
- [x] 2 player with split-screen
- [x] Overall directory structure - config and images in resources or similar
- [x] Either remove custom events or implement properly
- [x] Laser beams
- [x] Fix scoreboard
- [ ] Make a custom exception for duplicate controllers.