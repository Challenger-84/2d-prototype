# Importing Dependencies
import arcade
from objects.player import Player
from objects.utils.level_generator import LevelGenerator
from changes_to_arcade.phy_engine_change import PhysicsEnginePlatformer

# Constants
screen_height = 800
screen_width = 1200
screen_title = "Plat former"

gravity = 4.5

# Scroll value
scroll = 100

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 650
RIGHT_VIEWPORT_MARGIN = 650
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50
# todo make the view good


class MyGame(arcade.Window):
    """
    Main application class
    """

    def __init__(self):
        # Call the parent init
        super().__init__(screen_width, screen_height, screen_title)

        arcade.set_background_color(arcade.color.BLACK)

        # Sprite Lists
        self.player_list = None
        self.platform_list = None
        self.chunk_marker_list = None

        # A variable that holds the player sprite
        self.player = None
        # Physics Engine
        self.physics_engine = None
        # Procedural Level Generator
        self.proGenerator = None
        # Back Ground Sprite
        self.red_blob = arcade.SpriteSolidColor(500, self.height, arcade.color.RED)
        self.red_blob.center_x = -250
        self.red_blob.center_y = self.height/2

        # Keep track for our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        # Setting up the game

        # Player Sprites
        self.player_list = arcade.SpriteList()
        self.player = Player(self, 50, 50, arcade.color.CYAN, self.setup)
        self.player_list.append(self.player)

        # Platform Sprites
        self.platform_list = arcade.SpriteList()

        # Chunk Marker Sprite
        self.chunk_marker_list = arcade.SpriteList()

        # Procedural Generator
        self.proGenerator = LevelGenerator(self.platform_list, self.chunk_marker_list, self)

        # Physics Engine
        self.physics_engine = PhysicsEnginePlatformer(self.player, self.platform_list, gravity_constant=gravity)

    def manage_viewport(self):
        """This function moves the view"""
        changed = False
        dir_scroll = 0.3

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left - dir_scroll
            changed = True

        # Scroll right
        right_boundary = self.view_left + screen_width - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + screen_height - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                screen_width + self.view_left,
                                self.view_bottom,
                                screen_height + self.view_bottom)

    def on_update(self, delta_time: float):
        # Adding scroll
        self.player.center_x -= int(scroll * delta_time)
        for platform in self.platform_list:
            platform.center_x -= int(scroll * delta_time)

        # Manage view of the screen
        self.manage_viewport()

        # Updates the physics engine
        self.physics_engine.update()

        # Updating the player and platforms
        self.player.on_update(delta_time, self.physics_engine)
        self.platform_list.on_update(delta_time)
        self.chunk_marker_list.on_update(delta_time)

        # Updating the procedural generator
        self.proGenerator.update(self.player.center_x, scroll, delta_time)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        # What key is pressed
        if key == arcade.key.SPACE:
            self.player.space_pressed = True
        if key == arcade.key.A:
            self.player.left_pressed = True
        if key == arcade.key.D:
            self.player.right_pressed = True

    def on_key_release(self, key, modifiers):
        """When a key is released"""
        # What key is released
        if key == arcade.key.SPACE:
            self.player.space_pressed = False
        if key == arcade.key.A:
            self.player.left_pressed = False
        if key == arcade.key.D:
            self.player.right_pressed = False

    def on_draw(self):
        # Renders the screen

        arcade.start_render()

        # Draw our sprites
        self.player_list.draw()
        self.platform_list.draw()
        self.red_blob.draw()
        # self.chunk_marker_list.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()