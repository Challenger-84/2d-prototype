from arcade import View
from arcade import color
from arcade import SpriteSolidColor
from arcade import draw_text


class GameOverView(View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.rec = rec = SpriteSolidColor(self.window.width, self.window.height, color.RED)
        viewport = self.window.get_viewport()
        self.rec.left = viewport[0]
        self.rec.bottom = viewport[2]
        self.rec.alpha = 100

    def on_show(self):
        self.rec.draw()

        viewport = self.window.get_viewport()
        draw_text('GAME OVER', start_x=viewport[1]-self.window.width/2, start_y= viewport[3]/2, color=color.WHITE,
                  font_size=100, anchor_x='center')

        score = self.game_view.player.center_x // 100
        draw_text(f'Score: {score: .0f}', start_x=viewport[1]-self.window.width/2, start_y= viewport[2] + 300, color=color.GOLD,
                  font_size=50, anchor_x='center')

        draw_text('CLICK TO CONTINUE', start_x=viewport[1]-self.window.width/2, start_y= viewport[2] + 100,
                  color=color.WHITE, font_size=30, anchor_x='center')

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.game_view.setup()
        self.window.show_view(self.game_view)


