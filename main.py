# Kivy Main Auto Template
from configuration import WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from src import GameWidget, MapDrawer

Window.size = WINDOW_WIDTH, WINDOW_HEIGHT
Config.set("graphics", "width", WINDOW_WIDTH)
Config.set("graphics", "height", WINDOW_HEIGHT)
Config.set("graphics", "resizable", False)
Config.write()


class GameApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "GameApp"

    def get_game_widget(self):
        self.game_screen = Screen()
        self.game_widget = GameWidget()
        self.game_screen.add_widget(self.game_widget)
        self.sm.add_widget(self.game_screen)

    def get_drawer_widget(self):
        self.draw_screen = Screen()
        self.draw_widget = MapDrawer()
        self.draw_screen.add_widget(self.draw_widget)
        self.sm.add_widget(self.draw_screen)

    def build(self):
        self.sm = ScreenManager()
        # self.get_drawer_widget()
        self.get_game_widget()
        self.game_widget.start_loop()
        return self.sm


if __name__ == "__main__":
    GameApp().run()
