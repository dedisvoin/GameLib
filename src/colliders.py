from copy import copy
import pygame
from src.maths import *
from src.render.base import draw_rect
from uuid import uuid4


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
        self.__friction = 0.9

        self.__id: str | int | None = None


    @property
    def pos(self) -> Vector2D:
        return self.__pos
    
    @print
    def speed(self) -> Vector2D:
        return self.__speed
    
    def set_friction(self, value: float = 0) -> None:
        self.__friction = value

    def get_friction(self) -> float:
        return self.__friction
    
    def set_mass(self, value: float = 1) -> None:
        self.__mass = value

    def get_mass(self) -> float:
        return self.__mass

    def get_size(self) -> tuple[int, int]:
        return self.__size
    
    def get_type(self) -> str:
        return self.__type
    
    def set_size(self, size: tuple[int, int]):
        self.__size = size

    def set_pos(self, pos: tuple[int, int]):
        self.__pos = Vector2D.from_tuple(pos)

    def set_id(self, id: int | str | None):
        self.__id = str(id) if id is not None else uuid4()

    def get_id(self) -> str:
        return self.__id

    def create(self, pos: tuple[int, int], id: int | str | None = None) -> 'BaseRectCollider':
        obj = copy(self)
        obj.set_pos(pos)
        obj.set_id(id)
        return obj
        

class RectCollideLayer:
    def __init__(self):
        self.__colliders: list[BaseRectCollider] = []

    def add_collider(self, collider: BaseRectCollider):
        self.__colliders.append(collider)

    def remove_collider(self, collider: BaseRectCollider):
        self.__colliders.remove(collider)

    def get_colliders(self) -> list[BaseRectCollider]:
        return self.__colliders
    
    def get_collider(self, id: int | str) -> BaseRectCollider | None:
        for collider in self.__colliders:
            if collider.get_id() == str(id):
                return collider
        return None
    
    def get_colliders_by_type(self, type: str) -> list[BaseRectCollider]:
        return list(filter(lambda collider: collider.get_type() == type, self.__colliders))
    
    def update(self):
        dynamic_colliders = self.get_colliders_by_type(COLLIDER_DYNAMIC)
        
        for d_collider in dynamic_colliders:

            for s_collider
            

            
        
    
    def view(self, surf: pygame.Surface):
        for collider in self.__colliders:
            if collider.get_type() == COLLIDER_STATIC:
                color = (1, 1, 1)
            elif collider.get_type() == COLLIDER_DYNAMIC:
                color = (255, 0, 0)
            elif collider.get_type() == COLLIDER_KINEMATIC:
                color = (0, 0, 255)

            draw_rect(surf, collider.get_pos(), collider.get_size(), color)
        

    



        
        