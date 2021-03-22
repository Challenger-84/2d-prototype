from arcade.gui import UIFlatButton
from arcade import View as arcade_View


class BackToGameButton(UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade_View = None, game_view=None):
        super().__init__('BACK TO GAME', center_x, center_y, width)
        self.view = view
        self.game_view = game_view

    def on_click(self):
        self.view.window.show_view(self.game_view)


class QuitButton(UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade_View = None, start_view=None):
        super().__init__('QUIT', center_x, center_y, width)
        self.view = view
        self.start_view = start_view

    def on_click(self):
        start_view = self.start_view.start_class()
        self.view.window.show_view(start_view())
