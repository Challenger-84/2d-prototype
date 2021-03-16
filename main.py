# Importing Dependencies
import arcade
import arcade.gui
from arcade.gui import UIManager
from ui_buttons import StartButton, OptionsButton, QuitButton, BackButton

from in_game import GameView

# Constants
screen_height = 800
screen_width = 1200
screen_title = "Plat former"


class StartView(arcade.View):

    def __init__(self):
        super().__init__()
        self.blink_val = 0
        self.max_blink_val = 40
        self.blink = False

        self.uimanager = UIManager()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        # Start Button
        button = StartButton(self.window.width / 2, 500, 200, view=self, game_view=GameView)
        self.uimanager.add_ui_element(button)

        # Options Button
        button = OptionsButton(self.window.width / 2, 400, 200, view=self, options_view=OptionView)
        self.uimanager.add_ui_element(button)

        # Quit Button
        button = QuitButton(self.window.width / 2, 300, 200, view=self)
        self.uimanager.add_ui_element(button)

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
        self.bg = arcade.SpriteSolidColor(screen_width, screen_height, arcade.color.BLACK_OLIVE)
        self.bg.bottom = 0
        self.bg.left = 0

    def on_show(self):

        button = BackButton(self.window.width / 2, 300, 200, self, start_view=StartView)
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        self.bg.draw()
        arcade.draw_text('OPTIONS', self.window.width / 2, 600,
                         arcade.color.ORANGE, font_size=80, anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()


def main():
    window = arcade.Window(screen_width, screen_height, screen_title)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
