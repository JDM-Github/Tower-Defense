from random import choice
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.metrics import dp
from configuration import COLS, ROWS, WINDOW_HEIGHT, WINDOW_WIDTH


class Tile(Image):

    def __init__(self, color, name, parent_tile,  ** kwargs):
        super().__init__(**kwargs)
        self.size = (WINDOW_WIDTH/COLS, WINDOW_HEIGHT/ROWS)
        self.parent_tile = parent_tile
        self.color = color
        self.name = name

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.parent.parent.all_hero_position(
                    *self.parent_tile.position, self.name):
                self.parent_tile.parent.check_slot.clear_widgets()
                self.parent_tile.parent.remove_widget(self.parent_tile)
        return super().on_touch_down(touch)


class Slot(Image):

    def __init__(self, position, **kwargs):
        super().__init__(**kwargs)
        self.already = False
        self.size = (WINDOW_WIDTH/COLS, WINDOW_HEIGHT/ROWS)
        self.position = position
        self.picklist_widget = Widget()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.picklist_widget in self.parent.check_slot.children:
                self.parent.check_slot.clear_widgets()
                return False

            self.parent.check_slot.clear_widgets()
            if self.picklist_widget.children == []:
                self.pick_list()
            self.parent.check_slot.add_widget(self.picklist_widget)
        return super().on_touch_down(touch)

    def pick_list(self):
        spacing = dp(5)
        for index, choose in enumerate([("#55ff88", "sniper"), ("#333333", "golem"), ("#FF5555", "mortar")]):
            tile = Tile(*choose, self)
            tile.pos = ((self.x-(self.width+spacing)) +
                        ((self.width+spacing)*index), self.top+spacing)
            self.picklist_widget.add_widget(tile)
