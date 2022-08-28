from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.metrics import sp
from kivy.properties import NumericProperty

from configuration import WINDOW_HEIGHT, WINDOW_WIDTH


class MoneyBar(Widget):

    money = NumericProperty(999)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_label()
        self.bind(money=self.check_money)

    def display_label(self):
        self.lab = Label(text=f"{self.money}")
        self.lab.pos = ((WINDOW_WIDTH/2)-(self.width/2),
                        WINDOW_HEIGHT-self.height)
        self.lab.font_size = sp(32)
        self.add_widget(self.lab)

    def check_money(self, *_):
        self.lab.text = f"{self.money}"
