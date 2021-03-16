# Importing Dependencies
import arcade
from arcade.gui import UIManager
from ui_buttons import BackButton


class OptionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        arcade.set_background_color(arcade.color.PINK)

    def on_show(self):
        arcade.set_background_color(arcade.color.PINK)

        button = BackButton(self.window.width / 2, 300, 200, self, start_view=StartView)
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        arcade.draw_text('OPTIONS', self.window.width / 2, 600,
                         arcade.color.ORANGE, font_size=80, anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
