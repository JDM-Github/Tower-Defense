from math import sqrt
from random import choice, randint
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.utils import get_random_color, get_color_from_hex
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color
from configuration import COLS, ROWS, WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.vector import Vector


class EntityEnemy(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = WINDOW_WIDTH/(COLS*2), WINDOW_HEIGHT/(ROWS*2)
        self.pos = (-self.width*2, 290)
        self.x += randint(0, 20)
        self.y += randint(0, 20)
        self.var_changeable()
        self.all_movement_var()

    def var_changeable(self):
        self.money_on_death = 10
        self.health = 100
        self.speed = 10
        self.color = get_color_from_hex("#FFFFFF")

    def all_movement_var(self):
        self.old_color = self.color
        self.oldpathx = self.x
        self.oldpathy = self.y
        self.location_index = 0
        self.already = False
        self.stop = False

    def hurt_animation(self):
        anim = Animation(color=(1, 0, 0, 1), d=0.05, t="linear")
        anim += Animation(color=self.old_color, d=0.05, t="linear")
        anim.start(self)

    def update(self):
        minmax = (-2, 2)
        if self.stop is False and self.parent.parent.all_game_path != []:
            if self.already is False:
                self.pathx = (self.parent.parent.all_game_path[self.location_index]
                              [0] + randint(*minmax))
                self.pathy = (self.parent.parent.all_game_path[self.location_index]
                              [1] + randint(*minmax))
                self.already = True
            if sqrt((self.x-self.pathx)*(self.x-self.pathx) +
                    (self.y-self.pathy)*(self.y-self.pathy)) > 5:
                pathx = self.pathx - self.oldpathx
                pathy = self.pathy - self.oldpathy
                self.pos = Vector((pathx/1000)*self.speed,
                                  (pathy/1000) * self.speed) + self.pos
                for hero in self.parent.parent.all_hero.children:
                    self.check_collision(hero)
            else:
                self.location_index += 1
                self.oldpathx = self.pathx
                self.oldpathy = self.pathy
                self.already = False
                if self.location_index >= len(self.parent.parent.all_game_path):
                    self.stop = True
                    self.parent.remove_widget(self)

    def check_collision(self, hero):
        x_pos = self.x + (self.width/2)
        y_pos = self.y + (self.height/2)
        x_hero = hero.x + (hero.width/2)
        y_hero = hero.y + (hero.height/2)
        distance = sqrt(((x_pos-x_hero) * (x_pos-x_hero))
                        + ((y_pos-y_hero) * (y_pos-y_hero)))
        if self not in hero.all_in_range:
            if hero.radius_ < distance <= hero.radius:
                hero.all_in_range.append(self)
        else:
            if not hero.radius_ < distance <= hero.radius:
                hero.all_in_range.remove(self)


class EntityHero(Image):
    price = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = WINDOW_WIDTH/COLS, WINDOW_HEIGHT/ROWS
        self.var_changeable()
        self.all_variable()

    def var_changeable(self):
        self.damage = 50
        self.radius = 100
        self.radius_ = 25
        self.cooldown = 100

    def all_variable(self):
        self.reload_ = self.cooldown
        self.target = None
        self.all_in_range = list()

    def update(self):
        if self.reload_ <= 0:
            self.reload_ = self.cooldown
            self.attack()
        self.reload_ -= 1

    def attack(self):
        if self.all_in_range != []:
            if self.target is None:
                self.target = choice(self.all_in_range)
            self.do_damage()

    def do_damage(self):
        if self.target is not None:
            self.target.health -= self.damage
            self.target.hurt_animation()
            if self.target.health <= 0:
                for hero in self.parent.children:
                    if self.target in hero.all_in_range and hero != self:
                        hero.all_in_range.remove(self.target)
                        hero.target = None
                if self.target in self.all_in_range:
                    self.all_in_range.remove(self.target)
                if self.target is not None:
                    try:
                        self.target.parent.remove_widget(self.target)
                    except AttributeError:
                        pass
                self.parent.parent.all_money.money += self.target.money_on_death
                self.target = None

    def show_range(self):
        if hasattr(self, "range"):
            if self.range in self.parent.parent.check_range.children:
                self.parent.parent.check_range.clear_widgets()
                return False

        self.parent.parent.check_range.clear_widgets()
        if not hasattr(self, "range"):
            self.range = Widget()
            with self.range.canvas:
                # RADIUS TO ATTACK
                Color(rgba=(1, 0, 0, 0.2))
                Ellipse(size=(self.radius*2, self.radius*2),
                        pos=((self.x-self.radius)+(self.width/2), (self.y-self.radius)+(self.height/2)))
                # RADIUS WHEN TO STOP ATTACKING
                Color(rgba=(1, 1, 1, 0.2))
                Ellipse(size=(self.radius_*2, self.radius_*2),
                        pos=((self.x-self.radius_)+(self.width/2), (self.y-self.radius_)+(self.height/2)))
        self.parent.parent.check_range.add_widget(self.range)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.show_range()
        return super().on_touch_down(touch)
