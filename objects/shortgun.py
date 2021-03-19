# Importing Dependencies
from arcade import Sprite
from arcade import SpriteList
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

    def shoot(self, bullet_list: SpriteList = None):
        angle = math.radians(self.angle)
        x_force = - (math.cos(angle) * self.force)
        y_force = - (math.sin(angle) * self.force)
        # print(f'{math.sin(angle):.2f}')
        # print(x_force, y_force)
        # Shoot bullet
        bullet = Bullet(filename='images/weapons/bullet.png', scale=.1,
                        x=self.left, y=self.center_y, angle=self.angle)
        bullet_list.append(bullet)

        # Knock back
        self.player.x_vel = x_force
        self.player.y_vel = y_force

    def on_update(self, delta_time: float = 1 / 60):
        self.left = self.player.center_x - 10
        self.center_y = self.player.center_y - 10


class Bullet(Sprite):

    def __init__(self, filename, scale,
                 x, y, angle):
        super().__init__(filename, scale, center_x=x, center_y=y)
        self.angle = angle

        self.speed = 2000
        self.lifetime: float = 0.0

    def on_update(self, delta_time: float = 1/60, platform_list: SpriteList = None):
        self.lifetime += delta_time

        if self.lifetime > 2.0:
            self.kill()

        angle = math.radians(self.angle)
        self.center_x += (math.cos(angle) * self.speed) * delta_time
        self.center_y += (math.sin(angle) * self.speed) * delta_time

        if self.collides_with_list(platform_list):
            self.kill()