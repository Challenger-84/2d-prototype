# Importing Dependencies
import arcade


class Player(arcade.SpriteSolidColor):

    def __init__(self, screen, width, height, color, reset_func):
        super().__init__(width, height, color)
        self.screen = screen
        self.reset_func = reset_func

        # Positional variables
        self.center_y = screen.height / 2
        self.center_x = 300

        # Movement related variable
        self.speed = 20
        self.jump_speed = 55

        self.right_pressed = False
        self.left_pressed = False
        self.space_pressed = False

        self.change_x = 0
        self.change_y = 0

    def on_update(self, delta_time: float = 1 / 60, physics_engine=None):

        # Check if player fell down
        if self.top < 0:
            self.reset_func()

        # Movement
        self.change_x = 0

        if self.right_pressed and not self.left_pressed:
            self.change_x = self.speed
        if self.left_pressed and not self.right_pressed:
            self.change_x = -self.speed
        if self.space_pressed and physics_engine.can_jump(): # If space is pressed and we can jump
            self.jump()

    def jump(self):
        # Jumping
        self.change_y = self.jump_speed
