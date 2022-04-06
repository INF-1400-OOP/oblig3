""" Configuration file containing the settings to use in the implementation.

If pygame display goes outside of your monitor adjust the respective parameters for WIDTH or HEIGHT by adjusting its scale.
"""

# General settings
FPS = 100
BACKGROUND_COLOR = (100, 100, 100)
TILESIZE = 32
WIDTH, HEIGHT = TILESIZE * 48, TILESIZE * 28

NICE_COL = (255, 182, 193)

# Sprite settings
SPRITE_SPEED = 300
SPRITE_LOAD_DURATION = 0.2
GRAVITY_MAG = 200

# Projectile settings
PROJECTILE_SPEED = 500
