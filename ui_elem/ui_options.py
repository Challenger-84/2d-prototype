from arcade.gui import UIFlatButton
from arcade import View as arcade_View


class BackButton(UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade_View = None, start_view=None):
        super().__init__('BACK', center_x, center_y, width)
        self.view = view
        self.StartView = start_view

    def on_click(self):
        start_view = self.StartView()
        self.view.window.show_view(start_view)


class ShowFPSButton(UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade_View = None):
        super().__init__('SHOW STATISTICS', center_x, center_y, width)
        self.view = view

    def on_click(self):
        self.view.window.show_fps = not self.view.window.show_fps


class FullScreenButton(UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade_View = None):
        super().__init__('FULLSCREEN', center_x, center_y, width)
        self.view = view

    def on_click(self):
        self.view.window.change_fullscreen()
