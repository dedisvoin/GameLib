import sys
from typing import Union
sys.path.append('./')

from src.render import base, colors, sprites
from src.maths import Vector2D
from src.app import AppSubProcess
import pygame
from pygame import gfxdraw

from copy import deepcopy, copy

from enum import Enum, auto

import random


class ParticleShapes(Enum):
    RECT = auto()
    CIRCLE = auto()
    TRIANGLE = auto()
    SPRITE = auto()
    ANIMATED_SPRITE = auto()

    def __str__(self) -> str:
        return self.name
    

class Point:
    def __init__(self):
        self.pos: Vector2D

        self.speed: Vector2D
        self.max_start_speed: float = 10
        self.min_start_speed: float = 10
        self.start_speed_angle: float = 0
        self.speed_spread: float = 360
        self.speed_air_friction: Vector2D = Vector2D(0.9, 0.9)
        self.speed_rotation_angle: float = 0
        self.max_speed_rotation_angle: float = 0
        self.min_speed_rotation_angle: float = 0

        
        self.angle: float = 0
        self.rotate_speed: float = 0
        self.max_rotate_speed: float = 10
        self.min_rotate_speed: float = 10
        self.start_rotate_angle: float = 0
        self.use_random_start_angle: bool = False
        self.use_speed_vector_for_angle: bool = False


        self.mass: float

    

class EmitterTypes(Enum):
    POINT = auto()
    RECT = auto()
    CIRCLE = auto()
    LINE = auto()

class BaseEmmiter:
    def __init__(self, type: EmitterTypes, pos: Vector2D | tuple[int, int] | list[int]):
        self.__type = type
        self.__pos = Vector2D.from_tuple(pos) if isinstance(pos, (tuple, list)) else pos

    def get_type(self) -> EmitterTypes:
        return self.__type
    
    def get_pos(self) -> Vector2D:
        return self.__pos
    
    def set_pos(self, pos: Vector2D) -> Vector2D:
        self.__pos = pos

    def match_pos(self) -> Vector2D:
        pass

class RectEmitter(BaseEmmiter):
    def __init__(self, pos: Vector2D, width: int, height: int):
        super().__init__(EmitterTypes.RECT, pos)
        self.width = width
        self.height = height

    def match_pos(self, center: bool = False) -> Vector2D:
        x = random.randint(0, self.width) + self.get_pos().x
        y = random.randint(0, self.height) + self.get_pos().y
        if center:
            x -= self.width / 2
            y -= self.height / 2
        return Vector2D(x, y)
    
class CircleEmitter(BaseEmmiter):
    def __init__(self, pos: Vector2D, radius: int):
        super().__init__(EmitterTypes.CIRCLE, pos)
        self.radius = radius

    def match_pos(self) -> Vector2D:
        dummy_pos = self.get_pos().copy()
        angle_vector = Vector2D.random_angle() * random.randint(0, self.radius)
        dummy_pos += angle_vector
        return dummy_pos
        
        
type EmitterType = Union[RectEmitter, CircleEmitter, BaseEmmiter]
    

class Particle(Point):
    def __init__(self):
        super().__init__()

        self.__shape: ParticleShapes = ParticleShapes.CIRCLE
        self.life_time: int = 30
        self.start_life_time: int = 30


        self.color: colors.Color | list[colors.Color] = colors.Color(100, 100, 200)

        self.shadowing: bool = False
        self.shadow_color: colors.Color = colors.Color(0, 0, 0)
        self.shadow_offset: Vector2D = Vector2D(0, 0)


        self.max_start_radius: float = 10
        self.min_start_radius: float = 10
        self.start_radius: float = 0
        self.radius: float = 0

        self.radius_resize_speed: float = 0.1
        self.resize_radius_for_life_time: bool = False
        self.gravity: Vector2D = Vector2D(0, 0.1)

        self.lightning: bool = False
        self.lightning_color: colors.Color = colors.Color(255, 255, 255)
        
        
        


    def set_shape(self, shape: ParticleShapes):
        self.__shape = shape

    def get_shape(self) -> ParticleShapes:
        return self.__shape
    

class ParticleSystem:
    def __init__(self):
        self.__particles: list[Particle] = []

    def get_count(self) -> int:
        return len(self.__particles)
        

    def add_particle(self, particle: Particle):
        self.__particles.append(particle)

    def construct_particle(self, emitter: EmitterType, particle: Particle) -> Particle:
        dummy_particle = deepcopy(particle)

        dummy_particle.life_time = particle.start_life_time
        dummy_particle.start_life_time = particle.start_life_time

        # start position
        dummy_particle.pos = emitter.match_pos()

        # start speed
        dummy_particle.speed = Vector2D.random_angle(-particle.speed_spread // 2, particle.speed_spread // 2) *\
        (random.randint(particle.min_start_speed * 100, particle.max_start_speed * 100) / 100)


        # start rotate speed
        dummy_particle.rotate_speed = random.uniform(particle.min_rotate_speed, particle.max_rotate_speed)

        dummy_particle.speed_rotation_angle = random.uniform(particle.min_speed_rotation_angle, particle.max_speed_rotation_angle)

        
        if particle.use_random_start_angle:
            dummy_particle.angle = random.randint(0, 360)
        else:
            dummy_particle.angle = particle.start_rotate_angle


        # start radius

        dummy_particle.start_radius = random.randint(particle.min_start_radius * 100, particle.max_start_radius * 100) / 100
        dummy_particle.radius = copy(dummy_particle.start_radius)

        

        if type(particle.color) in (list, tuple):
            if type(particle.color[0]) == colors.Color:
                dummy_particle.color = random.choice(particle.color)
            elif type(particle.color[0]) in (int, float):
                dummy_particle.color = colors.Color(*particle.color)
            else:
                dummy_particle.color = colors.Color(*random.choice(particle.color))
        else:
            if type(particle.color) == colors.Color:
                dummy_particle.color = particle.color
            else:
                dummy_particle.color = colors.Color(*particle.color)
            

        return dummy_particle

    def emit(self, emitter: EmitterType, particle: Particle, count: int = 1):
        for _ in range(count):
            self.add_particle(self.construct_particle(emitter, particle))

    def _particle_out_of_window(self, surf: pygame.Surface, particle: Particle) -> bool:
        return not (0 <= particle.pos.x <= surf.get_width() and 0 <= particle.pos.y <= surf.get_height())   

    def render_particle(self, surf: pygame.Surface, particle: Particle):
        if particle.get_shape() == ParticleShapes.CIRCLE:
            gfxdraw.filled_circle(surf, int(particle.pos.x), int(particle.pos.y), int(particle.radius), particle.color.rgb_int)
            #base.draw_circle(surf, particle.pos.xy, particle.radius, particle.color.rgb)
        if particle.get_shape() == ParticleShapes.RECT:
            base.draw_polygon_circle(surf, particle.pos.xy, particle.radius, particle.color.rgb, segments_count=4, rotate=particle.angle)

    def render_particle_shadow(self, surf: pygame.Surface, particle: Particle):
        if particle.shadowing:
            if particle.get_shape() == ParticleShapes.CIRCLE:
                base.draw_circle(surf, (particle.pos + particle.shadow_offset).xy, particle.radius, particle.shadow_color.rgb)
            if particle.get_shape() == ParticleShapes.RECT:
                base.draw_polygon_circle(surf, (particle.pos + particle.shadow_offset).xy, particle.radius, particle.shadow_color.rgb, segments_count=4, rotate=particle.angle)

    def render(self, surf: pygame.Surface):
        for particle in self.__particles:
            if self._particle_out_of_window(surf, particle):
                continue
            self.render_particle_shadow(surf, particle)
        for particle in self.__particles:
            if self._particle_out_of_window(surf, particle):
                continue
            self.render_particle(surf, particle)

    


    def update_particle(self, particle: Particle):
        particle.speed += particle.gravity
        particle.speed *= particle.speed_air_friction

        if particle.use_speed_vector_for_angle:
            particle.angle = particle.speed.get_angle_degrees() + 45
        else: ...
        particle.speed.rotate(particle.speed_rotation_angle)


        particle.pos += particle.speed
        particle.angle += particle.rotate_speed
        if particle.resize_radius_for_life_time:
            particle.radius = particle.life_time / particle.start_life_time * particle.start_radius
        else:
            particle.radius -= particle.radius_resize_speed
        
        particle.life_time -= 1



    def update(self):
        for particle in self.__particles:
            self.update_particle(particle)

        self.__particles = list(filter(lambda particle: ((particle.life_time > 0) and (particle.radius > 0)), self.__particles))
        

