# Importing Dependencies
import arcade


class Platform(arcade.SpriteSolidColor):

    def __init__(self, x, y, width, height, color):
        super().__init__(width, height, color)

        self.left = x
        self.bottom = y

    def on_update(self, delta_time: float = 1/60):
        if self.right < 0:
            self.kill()

