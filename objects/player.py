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

        self.moving_left = False
        self.moving_right = True
        self.time_from_no_key_pressed = 0

        self.change_x = 0
        self.change_y = 0

    def on_update(self, delta_time: float = 1 / 60, physics_engine=None, view = None):

        # Check if player fell down
        if self.top < 0:
            self.reset_func()

        # Movement
        self.change_x = 0

        if self.right_pressed:
            self.change_x = self.speed
            self.moving_right = True
        else:
            self.moving_right = False

        if self.left_pressed:
            self.change_x = -self.speed
            self.moving_left = True
        else:
            self.moving_left = False

        if self.space_pressed and physics_engine.can_jump(): # If space is pressed and we can jump
            self.jump()

        # Changing the directional move
        if self.moving_right:
            if view.directional_move < 60:
                view.directional_move += view.directional_move_rate
            self.time_from_no_key_pressed = 0

        elif self.moving_left:
            if view.directional_move > -60:
                view.directional_move -= view.directional_move_rate
            self.time_from_no_key_pressed = 0

        else:
            self.time_from_no_key_pressed += 1
            if self.time_from_no_key_pressed > 120:
                if view.directional_move > 0:
                    view.directional_move -= view.directional_move_rate
                elif view.directional_move < 0:
                    view.directional_move += view.directional_move_rate

    def jump(self):
        # Jumping
        self.change_y = self.jump_speed
