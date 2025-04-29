from copy import copy, deepcopy
import pygame
from src.maths import *
from src.render.base import draw_rect
from uuid import uuid4
from colorama import Fore


COLLIDER_STATIC = 'static'
COLLIDER_DYNAMIC = 'dynamic'
COLLIDER_KINEMATIC = 'kinematic'

class BaseRectCollider:
    def __init__(self, size: tuple[int, int], type: str = COLLIDER_STATIC):
        self.__size = Vector2D.from_tuple(size)
        self.__type = type
        self.__pos = Vector2D(0, 0)
        self.__speed = Vector2D(0, 0)
        self.__mass = 1
        self.__friction = 0.8
        self.__bouncing = 0.8
        self.__id: str | int | None = None

    @property
    def pos(self) -> Vector2D:
        return self.__pos

    @pos.setter
    def pos(self, value: Vector2D):
        self.__pos = value
    
    @property
    def speed(self) -> Vector2D:
        return self.__speed

    @speed.setter
    def speed(self, value: Vector2D):
        self.__speed = value

    @property
    def bouncing(self) -> float:
        return self.__bouncing

    @bouncing.setter
    def bouncing(self, value: float):
        self.__bouncing = value
    
    @property
    def friction(self) -> float:
        return self.__friction

    @friction.setter
    def friction(self, value: float):
        self.__friction = value
    
    @property
    def mass(self) -> float:
        return self.__mass

    @mass.setter
    def mass(self, value: float):
        self.__mass = value

    @property
    def size(self) -> Vector2D:
        return self.__size
    
    @size.setter
    def size(self, value: tuple[int, int]):
        self.__size = Vector2D.from_tuple(value)

    @property
    def type(self) -> str:
        return self.__type

    def set_pos(self, pos: tuple[int, int]):
        self.__pos = Vector2D.from_tuple(pos)

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: int | str | None):
        self.__id = str(value) if value is not None else str(uuid4())

    def create(self, pos: tuple[int, int], id: int | str | None = None) -> 'BaseRectCollider':
        obj = deepcopy(self)
        obj.set_pos(pos)
        obj.id = id
        return obj

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__id} {self.__pos.xy} {self.__size.xy} {self.__type}'
        

class RectCollideLayer:
    def __init__(self, gravity: Vector2D | float | int = 0.5, debug: bool = False):
        self.__gravity = gravity if isinstance(gravity, Vector2D) else Vector2D(0, gravity)
        self.__colliders: list[BaseRectCollider] = []
        self.__debug = debug

    def add_collider(self, collider: BaseRectCollider):
        self.__colliders.append(collider)

    def remove_collider(self, collider: BaseRectCollider):
        self.__colliders.remove(collider)

    @property
    def colliders(self) -> list[BaseRectCollider]:
        return self.__colliders
    
    def get_collider_by_id(self, id: int | str) -> BaseRectCollider | None:
        return next((c for c in self.__colliders if c.id == str(id)), None)
    
    def get_colliders_by_type(self, type: str, exclude: bool = False) -> list[BaseRectCollider]:
        return [c for c in self.__colliders if (c.type != type) == exclude]

    def update(self):
        dynamic_colliders = self.get_colliders_by_type(COLLIDER_DYNAMIC)
        static_kinematic_colliders = [c for c in self.__colliders if c.type != COLLIDER_DYNAMIC]

        if self.__debug:
            print(f'{Fore.RED}Dynamic colliders: {len(dynamic_colliders)}{Fore.RESET}')
            print(f'{Fore.GREEN}Static colliders: {len(static_kinematic_colliders)}{Fore.RESET}')
            print()
            for d_c in dynamic_colliders:
                print(f'{Fore.RED}{d_c}{Fore.RESET}')
            for a_c in static_kinematic_colliders:
                print(f'{Fore.GREEN}{a_c}{Fore.RESET}')

        for d_collider in dynamic_colliders:
            collided_colliders = []
            d_collider.speed += self.__gravity

            d_collider.pos.y += d_collider.speed.y
            for collider in static_kinematic_colliders:
                collider.pos.y += collider.speed.y
            for a_collider in static_kinematic_colliders:
                rect_1 = [*d_collider.pos.xy, *d_collider.size.xy]
                rect_2 = [*a_collider.pos.xy, *a_collider.size.xy]
                
                if collision_rect_rect(rect_1, rect_2):
                    collided_colliders.append(a_collider)

            for c_collider in collided_colliders:
                if c_collider.type == COLLIDER_STATIC:
                    if d_collider.pos.y < c_collider.pos.y:
                        d_collider.speed.y = -d_collider.speed.y * d_collider.bouncing
                        d_collider.speed.x = d_collider.speed.x * c_collider.friction
                        d_collider.pos.y = c_collider.pos.y - d_collider.size.y
                    else:
                        d_collider.speed.y = -d_collider.speed.y * d_collider.bouncing
                        d_collider.pos.y = c_collider.pos.y + c_collider.size.y
                        d_collider.speed.x = -d_collider.speed.x * c_collider.friction
                if c_collider.type == COLLIDER_KINEMATIC:
                    if d_collider.pos.y < c_collider.pos.y:
                        d_collider.speed.y = -d_collider.speed.y * d_collider.bouncing
                        d_collider.speed.x = d_collider.speed.x * c_collider.friction
                        d_collider.speed.y = c_collider.speed.y
                        d_collider.pos.x += c_collider.speed.x
                        d_collider.pos.y = c_collider.pos.y - d_collider.size.y
                    else:
                        d_collider.speed.y = -d_collider.speed.y  * d_collider.bouncing
                        d_collider.speed.y = c_collider.speed.y
                        d_collider.pos.y = c_collider.pos.y + c_collider.size.y
                       
                        
                    
        
            collided_colliders = []
            d_collider.pos.x += d_collider.speed.x
            for collider in static_kinematic_colliders:
                collider.pos.x += collider.speed.x
            for a_collider in static_kinematic_colliders:
                rect_1 = [*d_collider.pos.xy, *d_collider.size.xy]
                rect_2 = [*a_collider.pos.xy, *a_collider.size.xy]
                
                if collision_rect_rect(rect_1, rect_2):
                    collided_colliders.append(a_collider)

            for c_collider in collided_colliders:
                if c_collider.type == COLLIDER_STATIC:
                    if d_collider.pos.x < c_collider.pos.x:
                        d_collider.speed.x = -d_collider.speed.x * d_collider.bouncing
                        d_collider.pos.x = c_collider.pos.x - d_collider.size.x
                    else:
                        d_collider.speed.x = -d_collider.speed.x * d_collider.bouncing
                        d_collider.pos.x = c_collider.pos.x + c_collider.size.x
                if c_collider.type == COLLIDER_KINEMATIC:
                    if d_collider.pos.x < c_collider.pos.x:
                        d_collider.speed.x = -d_collider.speed.x * d_collider.bouncing
                        d_collider.pos.x = c_collider.pos.x - d_collider.size.x
                    else:
                        
                        d_collider.speed.x = -d_collider.speed.x * d_collider.bouncing
                        d_collider.pos.x = c_collider.pos.x + c_collider.size.x
                        
        
        
    
    def view(self, surf: pygame.Surface):
        colors = {
            COLLIDER_STATIC: (1, 1, 1),
            COLLIDER_DYNAMIC: (255, 0, 0),
            COLLIDER_KINEMATIC: (0, 0, 255)
        }
        
        for collider in self.__colliders:
            draw_rect(surf, collider.pos.xy, collider.size.xy, colors[collider.type], 1)