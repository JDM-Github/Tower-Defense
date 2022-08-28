from random import choice
from kivy.graphics import Ellipse, Color
from kivy.utils import get_color_from_hex as gc
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from entities import EntityHero


class Sniper(EntityHero):

    price = 120

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("#55FF88")
        self.attributes()
        self.arrow_widget()

    def arrow_widget(self):
        self.all_arrow = Widget()
        self.add_widget(self.all_arrow)

    def attributes(self):
        self.damage = 45
        self.radius = 120
        self.radius_ = 40
        self.cooldown = 30
        self.arrow_speed = 10

    def do_damage(self):
        self.shoot_animation()
        return super().do_damage()

    def shoot_animation(self):
        arrow = Image(size=(10, 10), pos=(
            self.x+(self.width/2)-5, self.y+(self.height/2)-5))
        self.all_arrow.add_widget(arrow)
        anim = Animation(pos=self.target.pos, d=(
            self.arrow_speed/100), t="linear")
        anim.start(arrow)
        anim.bind(on_complete=lambda *_: self.all_arrow.remove_widget(arrow))


class Golem(EntityHero):

    price = 250

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("#333333")
        self.attributes()

    def attributes(self):
        self.damage = 30
        self.radius = 75
        self.radius_ = 10
        self.cooldown = 175

    def attack(self):
        if self.all_in_range != []:
            self.golem_animation()

    def golem_animation(self):
        with self.canvas:
            color = Color(rgb=self.color, a=0.3)
            damage_radius = Ellipse()
            damage_radius.pos = self.center_x, self.center_y
            damage_radius.size = (0, 0)
        anim = Animation(size=(self.radius*2, self.radius*2),
                         pos=(self.center_x - self.radius,
                              self.center_y - self.radius), d=(self.cooldown/100))
        anim.start(damage_radius)
        anim.bind(on_complete=lambda *_: self.do_damage(color))

    def do_damage(self, color):
        Animation(a=0, d=(self.cooldown/100)).start(color)
        for target in self.all_in_range:
            target.health -= self.damage
            target.hurt_animation()
            if target.health <= 0:
                for hero in self.parent.children:
                    if target in hero.all_in_range and hero != self:
                        hero.all_in_range.remove(target)
                        hero.target = None
                target.parent.remove_widget(target)
                self.parent.parent.all_money.money += target.money_on_death
        self.all_in_range.clear()


class Mortar(EntityHero):

    price = 300

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("#FF5555")
        self.attributes()
        self.cannon_widget()

    def cannon_widget(self):
        self.all_cannon = Widget()
        self.add_widget(self.all_cannon)

    def attributes(self):
        self.damage = 100
        self.radius = 160
        self.radius_ = 40
        self.cooldown = 150
        self.cannon_size = (18, 18)

    def attack(self):
        if self.all_in_range != []:
            self.cannon_lauch_animation()

    def do_damage(self, cann):
        self.all_cannon.remove_widget(cann)
        for target in self.all_in_range:
            if cann.collide_widget(target):
                target.health -= self.damage
                target.hurt_animation()
                if target.health <= 0:
                    for hero in self.parent.children:
                        if target in hero.all_in_range and hero != self:
                            hero.all_in_range.remove(target)
                            hero.target = None
                    target.parent.remove_widget(target)
                    self.parent.parent.all_money.money += target.money_on_death
        self.all_in_range.clear()
        self.target = None

    def cannon_lauch_animation(self):
        cannon = Image()
        cannon.size = self.cannon_size
        cannon.pos = (self.x+(self.width/2)-(cannon.width/2),
                      self.y+(self.height/2)-(cannon.height/2))
        self.all_cannon.add_widget(cannon)
        anim = Animation(size=(0, 0), d=((self.cooldown/2)/100))
        anim &= Animation(pos=(cannon.x+(cannon.width/2),
                          cannon.y+(cannon.height/2)), d=((self.cooldown/2)/100))
        anim.start(cannon)
        anim.bind(on_complete=lambda *_: self.cannon_hit_animation(cannon))

    def cannon_hit_animation(self, cann):
        if self.target is None and self.all_in_range != []:
            self.target = choice(self.all_in_range)
            self.all_cannon.remove_widget(cann)
            cannon = Image(color=self.color)
            cannon.size = (10, 10)
            cannon.center = (self.target.center)
            self.all_cannon.add_widget(cannon)
            anim = Animation(size=self.cannon_size, d=((self.cooldown/2)/100))
            anim &= Animation(center=self.target.center,
                              d=((self.cooldown/2)/100))
            anim.start(cannon)
            anim.bind(on_complete=lambda *_: self.do_damage(cannon))
