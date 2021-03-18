# Importing Dependencies
import arcade
import arcade.gui
from arcade.gui import UIManager
from ui_elem.ui_start import StartButton, OptionsButton, QuitButton
from ui_elem.ui_options import BackButton, ShowFPSButton, FullScreenButton, ResolutionButton

from in_game import GameView

# Constants
screen_height = 800
screen_width = 1200
screen_title = "Plat former"


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.show_fps = False
        self.is_fullscreen = False

    def change_fullscreen(self):
        # Change to full screen or not
        is_fullscr = self.is_fullscreen
        self.set_fullscreen(not is_fullscr)
        self.is_fullscreen = not is_fullscr

        # Set view because our game has scroll
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

    def on_resize(self, width: float, height: float):
        global screen_width, screen_height
        screen_width = width
        screen_height = height


class StartView(arcade.View):

    def __init__(self):
        super().__init__()
        self.blink_val = 0
        self.max_blink_val = 40
        self.blink = False

        self.uimanager = UIManager()
        self.ui_elems = []

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        # Start Button
        button = StartButton(int(screen_width/2), 500, 200, view=self, game_view=GameView)
        self.uimanager.add_ui_element(button)
        self.ui_elems.append(button)

        # Options Button
        button = OptionsButton(int(screen_width/2), 400, 200, view=self, options_view=OptionView)
        self.uimanager.add_ui_element(button)
        self.ui_elems.append(button)

        # Quit Button
        button = QuitButton(int(screen_width/2), 300, 200, view=self)
        self.uimanager.add_ui_element(button)
        self.ui_elems.append(button)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, screen_width - 1, 0, screen_height - 1)

    def on_hide_view(self):
        print('Hide')
        self.uimanager.unregister_handlers()

    def on_update(self, delta_time: float):
        self.blink_val += 1
        if self.blink_val >= self.max_blink_val:
            self.blink = not self.blink
            self.blink_val = 0

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        if not self.blink:
            arcade.draw_text("Square Rush", screen_width / 2, screen_height / 2 + 200,
                             arcade.color.WHITE, font_size=100, anchor_x="center")


class OptionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.bg = arcade.SpriteSolidColor(self.window.width, self.window.height, arcade.color.BLACK_OLIVE)
        self.bg.bottom = 0
        self.bg.left = 0

    def on_show(self):

        # Back Button
        button = BackButton(self.window.width / 2, 200, 200, self, start_view=StartView)
        self.ui_manager.add_ui_element(button)

        # Options Button
        button = ShowFPSButton(self.window.width/2, 500, 300, self)
        self.ui_manager.add_ui_element(button)

        # Change Full screen Button
        button = FullScreenButton(self.window.width/2, 400, 200, self)
        self.ui_manager.add_ui_element(button)

        # Change Res Button
        button = ResolutionButton(self.window.width/2, 300, 200, self, main)
        self.ui_manager.add_ui_element(button)

    def on_update(self, delta_time: float):
        width, height = self.window.get_size()
        self.bg.width = width
        self.bg.height = height

    def on_draw(self):
        print(self.bg.width)
        self.bg.draw()
        arcade.draw_text('OPTIONS', self.window.width / 2, 600,
                         arcade.color.ORANGE, font_size=80, anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()


def main():
    window = GameWindow(screen_width, screen_height, screen_title)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
