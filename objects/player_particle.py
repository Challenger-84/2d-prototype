from arcade import Sprite, SpriteList


class PlayerMoveParticle(Sprite):

    def __init__(self, filename, scale, x, y,
                 alpha: int = 255, lifetime: float = 1.0,
                 scroll: float = -1.0, up_vel: float = 0):

        super().__init__(filename, scale,
                         center_x=x, center_y=y)
        self.alpha = alpha
        self.scroll = scroll
        self.lifetime_max = lifetime
        self.lifetime = 0
        self.up_vel = up_vel

        # When needed to die
        self.die = False

    def on_update(self, delta_time: float = 1 / 60, gravity_constant: float = -0.5,
                  platforms: SpriteList = None):

        if not self.die:
            self.up_vel += gravity_constant
            # moving the particle
            self.center_y += self.up_vel

            for platform in self.collides_with_list(platforms):
                self.bottom = platform.top

            self.center_x += self.scroll

            # Adding to th lifetime and removing if over lifetime
            self.lifetime += delta_time
            if self.lifetime > self.lifetime_max:
                self.die = True
        else:
            self.center_y += gravity_constant
            self.lifetime += delta_time
            if self.lifetime > self.lifetime_max + 0.3:
                self.remove_from_sprite_lists()
                self.kill()

