import arcade
import pathlib


class Game(arcade.Window):
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500

    def __init__(self):
        super().__init__(
            width = self.SCREEN_WIDTH, 
            height = self.SCREEN_HEIGHT,
            title = "Junktion"
        )
        self.center_window()

        self.car_list = []
        self.lights_list = []
    
    def setup(self):
        self.car_list = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()
        self.car_list.draw()

    def update(self, delta_time):
        pass


if __name__ == "__main__":
    game = Game()
    game.setup()
    arcade.run()
