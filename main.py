# Importing Dependencies
import arcade
import arcade.gui
from arcade.gui import UIManager

from in_game import GameView

# Constants
screen_height = 800
screen_width = 1200
screen_title = "Plat former"


class MyFlatButton(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def __init__(self, text, center_x, center_y, width, view):
        super().__init__(text, center_x, center_y, width)
        self.view = view

    def on_click(self):
        """ Called when user lets off button """
        game_view = GameView()
        game_view.setup()
        self.view.window.show_view(game_view)


class StartView(arcade.View):

    def __init__(self):
        super().__init__()
        self.blink_val = 0
        self.max_blink_val = 40
        self.blink = False

        self.uimanager = UIManager()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        button = MyFlatButton(
            'CLICK HERE',
            center_x=600,
            center_y=300,
            width=200,
            view=self
        )

        self.uimanager.add_ui_element(button)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, screen_width - 1, 0, screen_height - 1)

    def on_hide_view(self):
        self.uimanager.unregister_handlers()

    def on_update(self, delta_time: float):
        self.blink_val += 1
        if self.blink_val >= self.max_blink_val:
            self.blink = not self.blink
            self.blink_val = 0

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_text("Welcome!", screen_width / 2, screen_height / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        if not self.blink:
            arcade.draw_text("Press enter to begin the game", screen_width / 2, screen_height / 2 - 75,
                             arcade.csscolor.NAVAJO_WHITE, font_size=30, anchor_x="center")

    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(screen_width, screen_height, screen_title)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
