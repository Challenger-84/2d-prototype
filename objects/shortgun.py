# Importing Dependencies
from arcade import Sprite
import math


class Shortgun(Sprite):

    def __init__(self, filename, scale,
                 player: Sprite = None):

        super().__init__(filename, scale)
        self.player = player

        self.left = player.center_x - 10
        self.center_y = player.center_y - 10

        self.force = 1500

    def point_at_mouse(self, mouse_x, mouse_y, scroll_left, scroll_bottom):
        x_diff = (mouse_x + scroll_left) - self.right
        y_diff = (mouse_y + scroll_bottom) - self.center_y
        angle_between = math.degrees(math.atan2(y_diff, x_diff))
        self.angle = angle_between

    def shoot(self):
        angle = math.radians(self.angle)
        x_force = - (math.cos(angle) * self.force)
        y_force = - (math.sin(angle) * self.force)
        # print(f'{math.sin(angle):.2f}')
        # print(x_force, y_force)

        self.player.x_vel = x_force
        self.player.y_vel = y_force

    def on_update(self, delta_time: float = 1/60):

        self.left = self.player.center_x - 10
        self.center_y = self.player.center_y - 10