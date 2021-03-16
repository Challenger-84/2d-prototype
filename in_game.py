import arcade
from utils.level_generator import LevelGenerator
from objects.player import Player
from changes_to_arcade.phy_engine_change import PhysicsEnginePlatformer

import timeit
import time
import collections

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


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


# View when in game
class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        # Call the parent init
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        self.fullscreen = False

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

        # FPS
        self.processing_time = 0
        self.draw_time = 0
        self.program_start_time = timeit.default_timer()
        self.sprite_count_list = []
        self.fps_list = []
        self.processing_time_list = []
        self.drawing_time_list = []
        self.last_fps_reading = 0
        self.fps = FPSCounter()

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

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

        # Total time program has been running
        total_program_time = int(timeit.default_timer() - self.program_start_time)
        if total_program_time > self.last_fps_reading:
            self.last_fps_reading = total_program_time

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
            self.window.set_fullscreen(not self.fullscreen)
            self.fullscreen = True

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)

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
        draw_start_time = timeit.default_timer()

        arcade.start_render()

        # Draw our sprites
        self.player_list.draw()
        self.platform_list.draw()
        self.red_blob.draw()

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, self.player.center_x, screen_height - 80, arcade.color.WHITE, 30)

        self.draw_time = timeit.default_timer() - draw_start_time
        self.fps.tick()
        # self.chunk_marker_list.draw()