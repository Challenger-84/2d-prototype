# Importing Dependencies
from arcade import Sprite
from arcade import SpriteList
from arcade import SpriteCircle
import arcade.color

import math
import random


class Shortgun(Sprite):

    def __init__(self, filename, scale,
                 player: Sprite = None):
        super().__init__(filename, scale)
        self.player = player

        self.left = player.center_x - 10
        self.center_y = player.center_y - 10
        self.__sprite_list = SpriteList()
        self.__sprite_list.append(self)

        self.force = 1500

        self.muzzle_flash = None

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
        num_of_bullets = random.randint(5, 8)
        for i in range(0, num_of_bullets):
            angle_for_bullet = self.angle + random.randint(-10, 10)
            bullet = Bullet(filename='images/weapons/bullet.png', scale=.1,
                            x=self.left, y=self.center_y, angle=angle_for_bullet)
            bullet_list.append(bullet)

        self.muzzle_flash = MuzzleFlash(self.right, self.center_y, 20)

        # Knock back
        self.player.x_vel = x_force
        self.player.y_vel = y_force

    def on_update(self, delta_time: float = 1 / 60):
        self.left = self.player.center_x - 10
        self.center_y = self.player.center_y - 10

        if self.muzzle_flash:
            self.muzzle_flash.on_update(delta_time, self)

    def draw(self):
        self.__sprite_list.draw()
        if self.muzzle_flash:
            self.muzzle_flash.draw()


class Bullet(Sprite):

    def __init__(self, filename, scale,
                 x, y, angle):
        super().__init__(filename, scale, center_x=x, center_y=y)
        self.angle = angle

        self.speed = 2000
        self.lifetime: float = 0.0

    def on_update(self, delta_time: float = 1 / 60, platform_list: SpriteList = None):
        self.lifetime += delta_time

        if self.lifetime > 2.0:
            self.kill()

        angle = math.radians(self.angle)
        self.center_x += (math.cos(angle) * self.speed) * delta_time
        self.center_y += (math.sin(angle) * self.speed) * delta_time

        if self.collides_with_list(platform_list):
            self.kill()


class MuzzleFlash(SpriteCircle):

    def __init__(self, x, y, radius):
        super().__init__(radius, arcade.color.WHITE, soft=True)
        self.center_x = x
        self.center_y = y
        self.alpha = 255
        self.radius = radius

        self.lifetime = 0

    def on_update(self, delta_time: float = 1 / 60, shortgun: Shortgun = None):
        x = shortgun.right - 5
        y = shortgun.center_y + 5

        self.center_x = x
        self.center_y = y

        self.lifetime += delta_time
        if self.lifetime > 1 / 60:
            if self.radius > 2:
                shortgun.muzzle_flash = MuzzleFlash(x, y, self.radius - 2)
            self.kill()
