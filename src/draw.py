from kivy.graphics import Rectangle, Color
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.metrics import sp
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import BooleanProperty
from kivy.uix.label import Label

from configuration import COLS, ROWS, WINDOW_HEIGHT, WINDOW_WIDTH
from widgets.colorpicker import WidColorPicker


class Tile(Image):

    def __init__(self, pos_x=None, pos_y=None, **kwargs):
        super().__init__(**kwargs)
        self.already = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        if self.pos_x is not None and self.pos_y is not None:
            self.opacity = 0.5
        else:
            self.color = get_color_from_hex("#339935")

    def on_touch_down(self, touch):
        return self.draw_tile(touch)

    def on_touch_move(self, touch):
        return self.draw_tile(touch)

    def draw_tile(self, touch):
        root = self.parent.parent.parent.parent
        if self.collide_point(*touch.pos):
            if root.draw_activator.state == "down" and self.parent.active:
                if self.parent.parent.parent.GRID_ACTIVE:
                    self.color = root.pen_color.color
                    return True
                else:
                    if self.already is False:
                        self.already = True
                        self.draw_path()
                    return True
        return False

    def draw_path(self):
        self.opacity = 1
        root = self.parent.parent.parent.parent
        self.color = get_color_from_hex("#FF0000")
        root.create_maptext += f"Button{root.number_way:03} = ({self.pos_x},{self.pos_y})\n"
        self.lab = Label(font_size=sp(10), text=str(root.number_way),
                         pos=self.pos, size=self.size)
        self.add_widget(self.lab)
        root.number_way += 1

    def reset(self):
        self.already = False
        if self.pos_x is not None and self.pos_y is not None:
            self.opacity = 0.5
        self.color = get_color_from_hex("#FFFFFF")
        if hasattr(self, "lab"):
            self.remove_widget(self.lab)


class Canvas(ScatterLayout):
    GRID_ACTIVE = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_bring_to_front = False
        self.do_rotation = False
        self.do_scale = False
        self.size = (WINDOW_WIDTH-100, WINDOW_HEIGHT-100)
        self.x = (WINDOW_WIDTH/2)-(self.width/2)
        self.y = (WINDOW_HEIGHT/2)-(self.height/2)
        self.get_grid()
        self.bind(GRID_ACTIVE=self.set_active)

    def get_grid(self):
        self.grid = GridLayout(rows=ROWS, cols=COLS)
        setattr(self.grid, "active", True)
        self.grid_move = GridLayout(rows=ROWS, cols=COLS)
        setattr(self.grid_move, "active", False)
        self.add_widget(self.grid)
        self.add_widget(self.grid_move)
        self.grid_child()
        self.set_active()

    def set_active(self, *_):
        if self.GRID_ACTIVE:
            self.grid_move.opacity = 0
            self.grid.opacity = 1
            self.grid.active = True
            self.grid_move.active = False
        else:
            self.grid_move.opacity = 1
            self.grid.opacity = 0.5
            self.grid.active = False
            self.grid_move.active = True

    def grid_child(self):
        for rows in range(self.grid.rows):
            for cols in range(self.grid.cols):
                self.grid.add_widget(Tile())
                self.grid_move.add_widget(Tile(cols, abs(rows-(ROWS-1))))


class ScrollableTileSet(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = WINDOW_WIDTH-200, WINDOW_HEIGHT-200
        self.x = (WINDOW_WIDTH/2)-(self.width/2)
        self.y = (WINDOW_HEIGHT/2)-(self.height/2)
        self.stack = StackLayout()
        self.stack.orientation = "lr-tb"
        self.stack.size_hint_y = None
        self.stack.bind(minimum_height=self.stack.setter("height"))
        self.add_widget(self.stack)

    def add_stack_children(self):
        image = Image(size_hint=(None, None))
        image.size = self.width/5, self.width/5
        self.stack.add_widget(image)


class MapDrawer(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_background()
        self.all_variables()
        self.get_canvas()
        self.all_widget()
        self.all_button()
        self.all_button_bind()

    def display_background(self):
        with self.canvas:
            Color(rgb=get_color_from_hex("#5588FF"))
            self.background = Rectangle()
            self.background.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

    def all_variables(self):
        self.create_maptext = str()
        self.number_way = 0
        self.diactivated_canvas = False
        self.block_width = WINDOW_WIDTH/10
        self.block_height = WINDOW_HEIGHT*0.1
        self.block_size = (self.block_width, self.block_height)

    def get_canvas(self):
        self.drawing_canvas = Canvas()
        self.add_widget(self.drawing_canvas)

    def all_widget(self):
        self.pen_color = Image(color=get_color_from_hex(
            "#333355"), pos=(0, 0), size=self.block_size)
        self.tileset_widget = Widget()
        self.colorpicker_widget = Widget()
        self.stack = StackLayout()
        self.stack.size = WINDOW_WIDTH, self.block_height
        self.stack.pos = (0, WINDOW_HEIGHT-self.stack.height)
        self.add_widget(self.tileset_widget)
        self.add_widget(self.colorpicker_widget)
        self.add_widget(self.stack)
        self.add_widget(self.pen_color)

    def all_button(self):
        self.save_activator = Button(
            text="Save", size_hint=(None, None), size=self.block_size, state="normal")
        self.new_activator = Button(
            text="Reset", size_hint=(None, None), size=self.block_size, state="normal")
        self.draw_activator = ToggleButton(
            text="Draw", size_hint=(None, None), size=self.block_size, state="normal")
        self.tileset_activator = ToggleButton(
            text="Tileset", size_hint=(None, None), size=self.block_size, state="normal")
        self.color_activator = ToggleButton(
            text="Color", size_hint=(None, None), size=self.block_size, state="normal")
        self.window_activator = Button(
            text="1", size_hint=(None, None), size=self.block_size, state="normal")

        self.stack.add_widget(self.save_activator)
        self.stack.add_widget(self.new_activator)
        self.stack.add_widget(self.draw_activator)
        self.stack.add_widget(self.tileset_activator)
        self.stack.add_widget(self.color_activator)
        self.stack.add_widget(self.window_activator)

    def save_map(self, *_):
        with open("createdmap/createdmap.txt", "w") as file:
            file.write(self.create_maptext)
        self.drawing_canvas.grid.export_to_png(
            "createdmap/createdmap.png")

    def all_button_bind(self):
        self.save_activator.bind(on_release=self.save_map)
        self.new_activator.bind(on_release=self.reset_all)
        self.tileset_activator.bind(state=self.open_tileset)
        self.color_activator.bind(state=self.open_colorpicker)
        self.window_activator.bind(on_release=self.change_window)

    def reset_all(self, *_):
        if self.drawing_canvas.GRID_ACTIVE:
            for tile in self.drawing_canvas.grid.children:
                tile.reset()
        else:
            self.number_way = 0
            for tile in self.drawing_canvas.grid_move.children:
                tile.reset()

    def change_window(self, *_):
        self.drawing_canvas.GRID_ACTIVE = False if self.drawing_canvas.GRID_ACTIVE else True
        self.window_activator.text = "1" if self.drawing_canvas.GRID_ACTIVE else "2"

    def open_tileset(self, _, state):
        if state == "down":
            if not hasattr(self, "tileset_"):
                self.big_bg = Image(
                    color=(0, 0, 0, 1), opacity=0.5, size=self.background.size)
                self.tileset_ = ScrollableTileSet()
                self.tileset_bg = Image(
                    color=(0, 0, 0, 1), opacity=0.5, size=self.tileset_.size, pos=self.tileset_.pos)
            self.display_tileset_widget()
        else:
            if hasattr(self, "tileset_"):
                self.tileset_widget.remove_widget(self.big_bg)
                self.tileset_widget.remove_widget(self.tileset_)
                self.tileset_widget.remove_widget(self.tileset_bg)

    def display_tileset_widget(self):
        self.tileset_widget.add_widget(self.big_bg)
        self.tileset_widget.add_widget(self.tileset_bg)
        self.tileset_widget.add_widget(self.tileset_)

    def open_colorpicker(self, _, state):
        if state == "down":
            if not hasattr(self, "colorpicker_"):
                self.colorpicker_ = WidColorPicker(self.pen_color)
            self.colorpicker_widget.add_widget(self.colorpicker_)
            # self.drawing_canvas.grid.disabled = True
        else:
            if hasattr(self, "colorpicker_"):
                self.colorpicker_widget.remove_widget(self.colorpicker_)
            # self.drawing_canvas.grid.disabled = False
