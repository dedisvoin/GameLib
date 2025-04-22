import importer

from src.app import AppWindow, AppSubProcess

from src.maths import Vector2D

from src.render import base, colors
from random import randint, uniform
import pygame

sprite_group = pygame.sprite.Group()

class Ball:
    def __init__(self):
        self.pos = Vector2D(300, 300)
        self.speed = Vector2D(uniform(-10, 10), uniform(-10, 10))
        self.surf = pygame.Surface((20, 20))
        self.surf.set_colorkey((0, 0, 0))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.surf
        
        
        base.draw_circle(self.surf, (10, 10), 10, colors.Color.Random().rgb)    

    def render(self):
        self.sprite.rect = self.surf.get_rect(center=self.pos.xy)
        sprite_group.add(self.sprite)

    def update(self):
        self.pos += self.speed
        if self.pos.x > 600:
            self.speed.x = -self.speed.x
        if self.pos.x < 0:
            self.speed.x = -self.speed.x
        if self.pos.y > 600:
            self.speed.y = -self.speed.y
        if self.pos.y < 0:
            self.speed.y = -self.speed.y


window = AppWindow([600, 600], "Test", vsync=False)
window.set_waited_fps(10000)
window.set_view_information_in_title()




balls = [Ball() for _ in range(10000)]



def update():
    for ball in balls:
        ball.update()


AppSubProcess(update, 1/60).start()

while window.is_opened:
    window.fill()
    for ball in balls:
        ball.render()
    sprite_group.draw(window.surf)
    window.update()