import arcade


class PhysicsEnginePlatformer(arcade.PhysicsEnginePlatformer):

    def __init__(self, player_sprite: arcade.Sprite,
                 platform_spritelist: arcade.SpriteList,
                 gravity_constant: float = 0.5,
                 ladder: arcade.SpriteList = None):
        super().__init__(player_sprite, platform_spritelist, gravity_constant, ladder)

    def can_jump(self, y_distance=5, x_distance=10) -> bool:

        # Move down to see if we are on a platform
        self.player_sprite.center_y -= y_distance
        self.player_sprite.center_x -= x_distance

        # Check for wall hit
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.platforms)

        self.player_sprite.center_y += y_distance
        self.player_sprite.center_x += x_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        if len(hit_list) > 0 or self.allow_multi_jump and self.jumps_since_ground < self.allowed_jumps:
            return True
        else:
            return False