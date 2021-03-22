import arcade
from arcade.gui import UIManager

from utils.level_generator import LevelGenerator
from objects.player import Player
from objects.shortgun import Shortgun
from changes_to_arcade.phy_engine_change import PhysicsEnginePlatformer
from ui_elem.ui_pause import BackToGameButton, QuitButton

import timeit

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 600
RIGHT_VIEWPORT_MARGIN = 600
BOTTOM_VIEWPORT_MARGIN = 250
TOP_VIEWPORT_MARGIN = 100

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

    def __init__(self, start_view):
        # Call the parent init
        super().__init__()

        self.start_view = start_view

        self.window.set_mouse_visible(True)
        # Sprite Lists
        self.player_list = None
        self.platform_list = None
        self.chunk_marker_list = None

        # A variable that holds the player sprite
        self.player = None

        # Weapons
        self.shortgun = None
        self.bullet_list = None
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

        # Points Variable
        self.points = 0
        self.time_till_add_points = 0

        # --- Variables for our statistics

        # Time for on_update
        self.processing_time = 0

        # Time for on_draw
        self.draw_time = 0

        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Setting up the game

        # Player Sprites
        self.player_list = arcade.SpriteList()
        self.player = Player(self.window, 'images/player_img/player.png')
        self.player_list.append(self.player)

        # Reset points
        self.points = 0
        self.time_till_add_points = 0

        # Giving the player shortgun
        self.shortgun = Shortgun('images/weapons/shortgun.png', scale=0.21, player=self.player)
        self.bullet_list = arcade.SpriteList()

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
        for particle in self.player.particles:
            particle.on_update(delta_time, platforms=self.platform_list)

        self.shortgun.on_update(delta_time)
        for bullet in self.bullet_list:
            bullet.on_update(delta_time, self.platform_list)

        self.platform_list.on_update(delta_time)
        self.chunk_marker_list.on_update(delta_time)

        # Adding points
        # self.time_till_add_points -= delta_time
        # if self.time_till_add_points < 0:
        #     self.points = self.player.center_x // 100
        #     self.time_till_add_points = 0.2

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

        # Pause the game
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self, self.start_view)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        """When a key is released"""
        # What key is released
        if key == arcade.key.SPACE:
            self.player.space_pressed = False
        if key == arcade.key.A:
            self.player.left_pressed = False
        if key == arcade.key.D:
            self.player.right_pressed = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.shortgun.point_at_mouse(x, y, self.view_left, self.view_bottom)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shortgun.shoot(self.bullet_list)

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
        self.platform_list.draw()
        self.player_list.draw()
        self.player.particles.draw()
        self.shortgun.draw()
        self.bullet_list.draw()
        self.red_blob.draw()

        # # Drawing score
        # view_port = self.window.get_viewport()
        # arcade.draw_text(f'Score: {self.points:.0f}', start_x=view_port[1]-100, start_y=view_port[3],
        #                  color=arcade.color.WHITE, anchor_x='center', anchor_y='top', font_size=25)

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


class PauseView(arcade.View):

    def __init__(self, cur_game_view, start_view):
        super().__init__()
        self.cur_game_view = cur_game_view
        self.ui_manager = UIManager()
        self.start_view = start_view

        viewport = self.window.get_viewport()

        self.bg_rec = arcade.SpriteSolidColor(self.window.width, self.window.height, arcade.color.WHITE)
        self.bg_rec.alpha = 100
        self.bg_rec.left = viewport[0]
        self.bg_rec.bottom = viewport[2]

    def on_show(self):
        self.bg_rec.draw()
        # Drawing the button
        button = BackToGameButton(self.window.width/2, 300, 250, self, self.cur_game_view)
        self.ui_manager.add_ui_element(button)

        button = QuitButton(self.window.width / 2, 200, 250, self, self.start_view)
        self.ui_manager.add_ui_element(button)
        arcade.set_viewport(0, self.window.width,
                            0, self.window.height)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.cur_game_view)