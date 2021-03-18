import arcade
from utils.level_generator import LevelGenerator
from objects.player import Player
from changes_to_arcade.phy_engine_change import PhysicsEnginePlatformer

import timeit

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 600
RIGHT_VIEWPORT_MARGIN = 600
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50

screen_height = 800
screen_width = 1200
# Scroll value
scroll = 100
gravity = 4.0


# View when in game
class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        # Call the parent init
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.window.set_mouse_visible(True)
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
        self.red_blob = arcade.SpriteSolidColor(500, self.window.height, arcade.color.RED)
        self.red_blob.center_x = -250
        self.red_blob.center_y = self.window.height / 2

        # Keep track for our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.directional_move = 0
        self.directional_move_rate = 1

        # --- Variables for our statistics

        # Time for on_update
        self.processing_time = 0

        # Time for on_draw
        self.draw_time = 0

        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def setup(self):
        # Setting up the game

        # Player Sprites
        self.player_list = arcade.SpriteList()
        self.player = Player(self.window, 50, 50, arcade.color.CYAN, self.setup)
        self.player_list.append(self.player)

        # Platform Sprites
        self.platform_list = arcade.SpriteList()

        # Chunk Marker Sprite
        self.chunk_marker_list = arcade.SpriteList()

        # Procedural Generator
        self.proGenerator = LevelGenerator(self.platform_list, self.chunk_marker_list, self.window)

        # Physics Engine
        self.physics_engine = PhysicsEnginePlatformer(self.player, self.platform_list, gravity_constant=gravity)

    def manage_viewport(self):
        """This function moves the view"""
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left + self.directional_move
            changed = True

        # Scroll right
        right_boundary = self.view_left + screen_width - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary + self.directional_move
            changed = True

        # # Scroll up
        # top_boundary = self.view_bottom + screen_height - TOP_VIEWPORT_MARGIN
        # if self.player.top > top_boundary:
        #     self.view_bottom += self.player.top - top_boundary
        #     changed = True
        #
        # # Scroll down
        # bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        # if self.player.bottom < bottom_boundary:
        #     self.view_bottom -= bottom_boundary - self.player.bottom
        #     changed = True

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

        # Start timing how long this takes
        start_time = timeit.default_timer()

        # Adding scroll
        self.player.center_x -= int(scroll * delta_time)
        for platform in self.platform_list:
            platform.center_x -= int(scroll * delta_time)

        # Manage view of the screen
        self.manage_viewport()

        # Updates the physics engine
        self.physics_engine.update()

        # Updating the player and platforms
        self.player.on_update(delta_time, self.physics_engine, self)
        self.platform_list.on_update(delta_time)
        self.chunk_marker_list.on_update(delta_time)

        # Updating the procedural generator
        self.proGenerator.update(self.player.center_x, scroll, delta_time)

        # Stop the draw timer, and calculate total on_draw time.
        self.processing_time = timeit.default_timer() - start_time

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        # What key is pressed
        if key == arcade.key.SPACE:
            self.player.space_pressed = True
        if key == arcade.key.A:
            self.player.left_pressed = True
        if key == arcade.key.D:
            self.player.right_pressed = True

        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.window.change_fullscreen()

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
        # Start timing how long this takes
        start_time = timeit.default_timer()

        # --- Calculate FPS

        fps_calculation_freq = 60
        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1

        # Start Drawing
        arcade.start_render()

        # Draw our sprites
        self.player_list.draw()
        self.platform_list.draw()
        self.red_blob.draw()

        # Display timings
        if self.window.show_fps:
            output = f"Processing time: {self.processing_time:.3f}"
            arcade.draw_text(output, self.player.center_x-400, screen_height - 25, arcade.color.WHITE, 18)

            output = f"Drawing time: {self.draw_time:.3f}"
            arcade.draw_text(output, self.player.center_x-400, screen_height - 50, arcade.color.WHITE, 18)

            if self.fps is not None:
                output = f"FPS: {self.fps:.0f}"
                arcade.draw_text(output, self.player.center_x-400, screen_height - 75, arcade.color.WHITE, 18)

            # Stop the draw timer, and calculate total on_draw time.
            self.draw_time = timeit.default_timer() - start_time

        # self.chunk_marker_list.draw()