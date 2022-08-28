from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.uix.slider import Slider
from kivy.core.window import Window


class WidColorPicker(Widget):

    R_COLOR = NumericProperty(0)
    G_COLOR = NumericProperty(0)
    B_COLOR = NumericProperty(0)
    A_COLOR = NumericProperty(0)

    def __init__(self, widget=Image(), width: float = 200, height: float = 175, x: float = None, y: float = None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Color Picker"
        self.size = (width, height)
        self.pos = ((Window.width/2)-(self.width/2) if x is None else x,
                    (Window.height/2)-(self.height/2) if y is None else y)
        self.widget_color = widget
        self.all_variable()
        self.display_body()
        self.display_title()
        self.display_widget()
        self.set_position()

    def all_variable(self):
        self.x_margin = None
        self.y_margin = None
        self.color_hex = ["0x33", "0x33", "0x55", "0xFF"]
        self.R_COLOR = int(self.color_hex[0], 16)
        self.G_COLOR = int(self.color_hex[1], 16)
        self.B_COLOR = int(self.color_hex[2], 16)
        self.A_COLOR = int(self.color_hex[3], 16)
        self.bind(R_COLOR=self.set_hex_text)
        self.bind(G_COLOR=self.set_hex_text)
        self.bind(B_COLOR=self.set_hex_text)
        self.bind(A_COLOR=self.set_hex_text)

    def set_hex_text(self, *_):
        if hasattr(self, "grid_text"):
            self.grid_text.text = get_hex_from_color(
                (self.R_COLOR/255, self.G_COLOR/255, self.B_COLOR/255, self.A_COLOR/255)).upper()
            self.widget_color.color = get_color_from_hex(self.grid_text.text)

    def display_title(self):
        self.lab_title = Label(text=self.title)
        self.lab_title.size = (self.width, 25)
        self.lab_image = Image(color=self.set_hexcolor())
        self.lab_image.size = self.lab_title.size
        self.lab_bg_image = Image(color=get_color_from_hex("#000000"))
        self.lab_bg_image.size = self.lab_title.size
        self.exit_button = Image(color=get_color_from_hex("AA1111"))
        self.exit_button.size = (25, 25)
        self.add_widget(self.lab_bg_image)
        self.add_widget(self.lab_image)
        self.add_widget(self.lab_title)
        self.add_widget(self.exit_button)

    def set_hexcolor(self):
        return get_color_from_hex(
            (self.color_hex[0])[2:] + (self.color_hex[1])[2:] +
            (self.color_hex[2])[2:] + (self.color_hex[3])[2:])

    def display_body(self):
        with self.canvas:
            Color(rgb=get_color_from_hex("#5cafff"))
            self.body = RoundedRectangle()
            self.body.radius = [0, 0, 10, 10]
            self.body.size = self.size

    def display_widget(self):
        self.grid = GridLayout(cols=1, rows=5)
        self.grid.size = (self.width - dp(20), self.height - dp(20))
        self.grid_children()

    def grid_children(self):
        self.grid_text = TextInput(text=(
            "#" + (self.color_hex[0])[2:] + (self.color_hex[1])[2:] +
            (self.color_hex[2])[2:] + (self.color_hex[3])[2:]), readonly=True)
        self.grid.add_widget(self.grid_text)
        self.grid.add_widget(self.get_boxlayout("R"))
        self.grid.add_widget(self.get_boxlayout("G"))
        self.grid.add_widget(self.get_boxlayout("B"))
        self.grid.add_widget(self.get_boxlayout("A"))
        self.add_widget(self.grid)

    def get_boxlayout(self, attr):
        box = BoxLayout()
        lab = Label(text=attr, size_hint=(0.1, 1))
        num = TextInput(text=str(getattr(self, attr+"_COLOR")),
                        size_hint=(0.25, 1), multiline=False)
        slid = Slider(value=num.text, max=255, min=0,
                      step=1, size_hint=(0.65, 1))
        setattr(self, attr, box)
        setattr(num, "value_property", attr+"_COLOR")
        slid.bind(value=partial(self.set_box_text, num))
        num.bind(text=partial(self.set_slid_value, slid))
        for i in [lab, slid, num]:
            box.add_widget(i)
        return getattr(self, attr)

    def set_box_text(self, lab, _, value):
        lab.text = str(int(value))
        setattr(self, getattr(lab, "value_property"), int(lab.text))

    def set_slid_value(self, slid, wid, text):
        try:
            if not wid.text[-1].isnumeric() or text == "00":
                wid.text = wid.text[:len(
                    text)-1] if len(wid.text) > 1 else "0"
            elif not wid.text.isnumeric():
                wid.text = "0"
            else:
                wid.text = "255" if int(text) > 255 else wid.text
            setattr(self, getattr(wid, "value_property"), int(wid.text))
        except IndexError or ValueError:
            wid.text = ""
            setattr(self, getattr(wid, "value_property"), 0)
            return
        slid.value = int(wid.text)

    def set_position(self):
        self.body.pos = self.pos
        self.lab_title.pos = (self.x, self.y+self.body.size[1])
        self.lab_image.pos = (self.x, self.y+self.body.size[1])
        self.lab_bg_image.pos = (self.x, self.y+self.body.size[1])
        self.exit_button.pos = (
            (self.x + self.body.size[0]) - 25, self.y+self.body.size[1])
        self.grid.pos = (self.x + dp(10), self.y + dp(10))

    def on_touch_down(self, touch):
        if self.lab_image.collide_point(*touch.pos) and not self.exit_button.collide_point(*touch.pos):
            self.x_grab = self.x - touch.x
            self.y_grab = self.y - touch.y
            touch.grab(self)
        elif self.exit_button.collide_point(*touch.pos):
            self.parent.parent.color_activator.state = "normal"
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x = touch.x + self.x_grab
            self.y = touch.y + self.y_grab
            self.set_position()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        return super().on_touch_up(touch)
