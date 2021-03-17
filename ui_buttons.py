import arcade.gui


class BackButton(arcade.gui.UIFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade.View = None, start_view=None):
        super().__init__('BACK', center_x, center_y, width)
        self.view = view
        self.StartView = start_view

    def on_click(self):
        start_view = self.StartView()
        self.view.window.show_view(start_view)


class StartButton(arcade.gui.UIGhostFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """

    def __init__(self, center_x, center_y, width,
                 view: arcade.View = None, game_view=None):
        super().__init__('START', center_x, center_y, width)
        self.view = view
        self.GameView = game_view

    def on_click(self):
        """ Called when user lets off button """
        game_view = self.GameView()
        game_view.setup()
        self.view.window.show_view(game_view)


class OptionsButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade.View = None, options_view=None):
        super().__init__('OPTIONS', center_x, center_y, width)
        self.view = view
        self.OptionView = options_view

    def on_click(self):
        option_view = self.OptionView()
        self.view.window.show_view(option_view)


class QuitButton(arcade.gui.UIGhostFlatButton):

    def __init__(self, center_x, center_y, width,
                 view: arcade.View = None):
        super().__init__('QUIT', center_x, center_y, width)
        self.view = view

    def on_click(self):
        exit()

