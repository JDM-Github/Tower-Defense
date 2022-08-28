import sys
from random import randint
from configuration import ROWS, COLS, WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.uix.widget import Widget
from heroes import Golem, Mortar, Sniper, EntityHero
from entities import EntityEnemy
from kivy.uix.image import Image
from kivy.clock import Clock
from slot import Slot
from ui import MoneyBar
with open("createdmap\createdmap.txt", "r") as file:
    exec(file.read())


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_variable()
        self.create_path()
        self.set_background()
        self.all_widget()

    def start_loop(self):
        self.start_clock = Clock.schedule_interval(
            lambda _: self.game_loop(), 1.0/60.0)

    def game_loop(self):
        for enemy in self.all_enemy.children:
            enemy.update()
        for hero in self.all_hero.children:
            hero.update()
        if randint(0, 100) == 20:
            self.spawn_enemy()

    def all_variable(self):
        self.block_width = WINDOW_WIDTH/COLS
        self.block_height = WINDOW_HEIGHT/ROWS
        self.all_hero_pos = [
            (2, 16), (7, 18), (7, 14), (7, 10), (7, 6),
            (11, 12), (12, 9), (15, 15), (16, 11)
        ]

    def set_background(self):
        self.background = Image(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.allow_stretch = True
        self.background.source = "createdmap/createdmap.png"
        self.add_widget(self.background)

    def create_path(self):
        self.all_game_path = []
        index = 1
        while True:
            try:
                self.all_game_path.append(
                    self.give_destination_node(*getattr(sys.modules[__name__], f"Button{index:03}")))
                index += 1
            except AttributeError:
                nodes = getattr(sys.modules[__name__], f"Button{index-1:03}")
                self.all_game_path.append(
                    self.give_destination_node(nodes[0]+1, nodes[1]))
                self.all_game_path.append(
                    self.give_destination_node(nodes[0]+2, nodes[1]))
                break
        print(self.all_game_path)

    def all_widget(self):
        self.check_range = Widget()
        self.all_enemy = Widget()
        self.all_hero = Widget()
        self.check_slot = Widget()
        self.all_money = MoneyBar()
        self.add_widget(self.check_range)
        self.add_widget(self.all_enemy)
        self.add_widget(self.all_hero)
        self.add_widget(self.check_slot)
        self.add_widget(self.all_money)
        self.set_stage()

    def set_stage(self):
        self.spawn_enemy()
        for position in self.all_hero_pos:
            slot = Slot(position)
            slot.pos = (self.block_width *
                        (position[0]-1), self.block_height*(position[1]-1))
            self.add_widget(slot)

    def all_hero_position(self, x, y, type=None):
        position = (self.block_width*(x-1), self.block_height*(y-1))
        if type is None:
            if self.check_hero(EntityHero, position):
                return True
        elif type == "sniper":
            if self.check_hero(Sniper, position):
                return True
        elif type == "golem":
            if self.check_hero(Golem, position):
                return True
        elif type == "mortar":
            if self.check_hero(Mortar, position):
                return True
        return False

    def check_hero(self, hero, position):
        if self.all_money.money - hero.price >= 0:
            self.all_money.money -= hero.price
            self.all_hero.add_widget(hero(pos=position))
            return True
        return False

    def spawn_enemy(self, type=None):
        if type is None:
            self.all_enemy.add_widget(EntityEnemy())

    def give_destination_node(self, *pos):
        x_des = (self.block_width*pos[0]+1)+((self.block_width/4))
        y_des = (self.block_height*pos[1]+1)+((self.block_height/4))
        return (x_des, y_des)
