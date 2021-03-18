# Importing Dependencies
import arcade
from objects.player_particle import PlayerMoveParticle
import random


class Player(arcade.Sprite):

    def __init__(self, screen, filename, reset_func):
        super().__init__(filename, 0.9)
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

        # Add images for player animation
        self.append_texture(arcade.load_texture('images/player_img/player1.png'))
        self.append_texture(arcade.load_texture('images/player_img/player2.png'))
        self.append_texture(arcade.load_texture('images/player_img/player3.png'))
        self.append_texture(arcade.load_texture('images/player_img/player_right.png'))
        self.append_texture(arcade.load_texture('images/player_img/player_left.png'))
        # Blink animation variables
        self.time_idle = 0
        self.time_between_textures = 0
        self.animate_back = False
        self.blinking = False

        # var for storing particles
        self.particles = arcade.SpriteList()

    def on_update(self, delta_time: float = 1 / 60, physics_engine=None, view=None):

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

        if self.space_pressed and physics_engine.can_jump():  # If space is pressed and we can jump
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

        # Making the player Blink
        if self.change_x == 0 and self.change_y == 0:
            self.time_idle += delta_time
        else:
            self.time_idle = 0

        if self.time_idle > 4:
            self.time_between_textures += delta_time
            if self.time_between_textures > 0.091666:
                self.blink()
                self.time_between_textures = 0

        # Animate the player appropriately when he moves right of left
        if self.change_x > 0:
            self.set_texture(4)
        elif self.change_x < 0:
            self.set_texture(5)

        # Spawn particles is moving and on ground
        if self.change_x and physics_engine.can_jump():
            # 50 50 chance a particle wil spawn before this
            if random.randint(0,1):
                particle = PlayerMoveParticle('images/player_img/playerparticle.png', scale=random.uniform(0.3, 0.7),
                                              x=random.uniform(self.left, self.center_x), y=self.bottom, up_vel=random.uniform(1.0, 5.0),
                                              alpha=random.randint(150, 255), lifetime=random.uniform(0.5, 1.5))
                self.particles.append(particle)

            particle = PlayerMoveParticle('images/player_img/playerparticle.png', scale=random.uniform(0.3, 0.7),
                                          x=random.uniform(self.left, self.center_x), y=self.bottom, up_vel=random.uniform(1.0, 5.0),
                                          alpha= random.randint(150, 255), lifetime=random.uniform(0.5, 1.5))
            self.particles.append(particle)

    def blink(self):

        if self.cur_texture_index < 3 and not self.animate_back:
            self.set_texture(self.cur_texture_index + 1)
            self.cur_texture_index += 1
        elif self.cur_texture_index - 1 >= 0 and self.animate_back:
            self.set_texture(self.cur_texture_index - 1)
            self.cur_texture_index -= 1
            if self.cur_texture_index == 0:
                self.animate_back = False
                self.time_idle = 0
        else:
            self.set_texture(self.cur_texture_index - 1)
            self.cur_texture_index -= 1
            self.animate_back = True

    def jump(self):
        # Jumping
        self.change_y = self.jump_speed
