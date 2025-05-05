from copy import copy
from enum import Enum
from uuid import uuid4
import pygame
from pygame import gfxdraw
import sys

sys.path.append('./')
from src.maths import Vector2D, collision_rect_rect

class COLLIDER_TYPES(Enum):
    STATIC = 0
    DYNAMIC = 1
    KINEMATIC = 2

class RectColliderObject:
    __slots__ = ('_width', '_height', '_type', '_id', '_pos', '_prev_pos', 'speed', '_bouncy', '_resistance')

    def __init__(self, width: int, height: int, type: COLLIDER_TYPES = COLLIDER_TYPES.STATIC, 
                 bouncy: float = 0.5, resistance: float | Vector2D = 0.99):
        self._width = width
        self._height = height
        self._type = type
        self._id = None
        self._pos = Vector2D(0, 0)
        self._prev_pos = Vector2D(0, 0)
        self.speed = Vector2D(0, 0)
        self._bouncy = bouncy
        self._resistance = Vector2D(resistance, resistance) if isinstance(resistance, (int, float)) else resistance

    def set_position(self, x: int, y: int):
        self._pos.x = x
        self._pos.y = y

    def set_speed(self, speed: Vector2D):
        self.speed.x = speed.x
        self.speed.y = speed.y

    def set_size(self, width: int, height: int):
        self._width = width
        self._height = height

    def set_id(self, id: str | int | None = None):
        self._id = uuid4() if id is None else id
        print(self._id)

    @property
    def bouncy(self) -> float:
        return self._bouncy
    
    @bouncy.setter
    def bouncy(self, bouncy: float):
        self._bouncy = bouncy

    @property
    def resistance(self) -> Vector2D:
        return self._resistance
    
    @resistance.setter
    def resistance(self, resistance: Vector2D | float):
        self._resistance = Vector2D(resistance, resistance) if isinstance(resistance, (int, float)) else resistance

    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def pos(self) -> Vector2D:
        return self._pos
    
    @pos.setter
    def pos(self, pos: Vector2D):
        self._pos.x = pos.x
        self._pos.y = pos.y

    @property
    def prev_pos(self) -> Vector2D:
        return self._prev_pos
    
    @prev_pos.setter
    def prev_pos(self, pos: Vector2D):
        self._prev_pos.x = pos.x
        self._prev_pos.y = pos.y

    @property
    def type(self) -> COLLIDER_TYPES:
        return self._type
    
    @property
    def id(self):
        return self._id
    
    @property
    def center(self) -> Vector2D:
        return Vector2D(self._pos.x + self._width / 2, self._pos.y + self._height / 2)
    
    @property
    def up_axis_y(self) -> float:
        return self._pos.y
    
    @up_axis_y.setter
    def up_axis_y(self, up_axis_y: float):
        self._pos.y = up_axis_y
    
    @property
    def down_axis_y(self) -> float:
        return self._pos.y + self._height
    
    @down_axis_y.setter
    def down_axis_y(self, down_axis_y: float):
        self._pos.y = down_axis_y - self._height
    
    @property
    def left_axis_x(self) -> float:
        return self._pos.x
    
    @left_axis_x.setter
    def left_axis_x(self, left_axis_x: float):
        self._pos.x = left_axis_x
    
    @property
    def right_axis_x(self) -> float:
        return self._pos.x + self._width
    
    @right_axis_x.setter
    def right_axis_x(self, right_axis_x: float):
        self._pos.x = right_axis_x - self._width

    def new(self, x: int, y: int, speed: Vector2D = Vector2D(0, 0), id: str | int | None = None):
        obj = copy(self)
        obj.set_position(x, y)
        obj.set_speed(speed)
        obj.set_id(id)
        
        return obj

class RectColliderSpace:
    __slots__ = ('_gravity', '_static_colliders', '_dynamic_colliders', '_kinematic_colliders')

    def __init__(self, gravity: Vector2D | float = 0.1):
        self._gravity = Vector2D(0, gravity) if isinstance(gravity, (float, int)) else gravity
        self._static_colliders = []
        self._dynamic_colliders = []
        self._kinematic_colliders = []

    def get_static_colliders(self) -> list[RectColliderObject]:
        return self._static_colliders
    
    def get_dynamic_colliders(self) -> list[RectColliderObject]:
        return self._dynamic_colliders
    
    def get_kinematic_colliders(self) -> list[RectColliderObject]:
        return self._kinematic_colliders

    @property 
    def gravity(self) -> Vector2D:
        return self._gravity
    
    @gravity.setter
    def gravity(self, gravity: Vector2D | float):
        self._gravity = Vector2D(0, gravity) if isinstance(gravity, (float, int)) else gravity

    def add_collider(self, collider: RectColliderObject):
        if collider.type == COLLIDER_TYPES.STATIC:
            self._static_colliders.append(collider)
        elif collider.type == COLLIDER_TYPES.DYNAMIC:
            self._dynamic_colliders.append(collider)
        elif collider.type == COLLIDER_TYPES.KINEMATIC:
            self._kinematic_colliders.append(collider)
    
    def add_colliders(self, colliders: list[RectColliderObject]):
        self._static_colliders.extend(c for c in colliders if c.type == COLLIDER_TYPES.STATIC)
        self._dynamic_colliders.extend(c for c in colliders if c.type == COLLIDER_TYPES.DYNAMIC)
        self._kinematic_colliders.extend(c for c in colliders if c.type == COLLIDER_TYPES.KINEMATIC)

    def get_colliders(self) -> list[RectColliderObject]:
        return self._static_colliders + self._dynamic_colliders + self._kinematic_colliders
    
    def get_collider_by_id(self, id: str | int) -> RectColliderObject | None:
        for collider in self.get_colliders():
            if collider.id == id:
                return collider
        return None
    
    def remove_collider(self, collider: RectColliderObject):
        if collider.type == COLLIDER_TYPES.STATIC:
            self._static_colliders.remove(collider)
        elif collider.type == COLLIDER_TYPES.DYNAMIC:
            self._dynamic_colliders.remove(collider)
        elif collider.type == COLLIDER_TYPES.KINEMATIC:
            self._kinematic_colliders.remove(collider)

    def remove_collider_by_id(self, id: str | int):
        if collider := self.get_collider_by_id(id):
            self.remove_collider(collider)
    
    def update(self):
        for kc in self._kinematic_colliders:
            kc.prev_pos.x = kc.pos.x
            kc.prev_pos.y = kc.pos.y
            kc.pos.x += kc.speed.x
            kc.pos.y += kc.speed.y

        for dc in self._dynamic_colliders:
            dc.speed.x += self._gravity.x
            dc.speed.y += self._gravity.y
            dc.pos.x += dc.speed.x
            dc.pos.y += dc.speed.y

        for dc in self._dynamic_colliders:
            dc_rect = [dc.pos.x, dc.pos.y, dc.width, dc.height]
            
            for sc in self._static_colliders:
                if collision_rect_rect(dc_rect, [sc.pos.x, sc.pos.y, sc.width, sc.height]):
                    self._process_static_collision(dc, sc)
            
            for kc in self._kinematic_colliders:
                if collision_rect_rect(dc_rect, [kc.pos.x, kc.pos.y, kc.width, kc.height]):
                    self._process_kinematic_collision(dc, kc)

    def _process_static_collision(self, dc, static):
        overlap_x = min(dc.right_axis_x, static.right_axis_x) - max(dc.left_axis_x, static.left_axis_x)
        overlap_y = min(dc.down_axis_y, static.down_axis_y) - max(dc.up_axis_y, static.up_axis_y)
        
        if overlap_x < overlap_y:
            if dc.center.x < static.center.x:
                dc.right_axis_x = static.left_axis_x
            else:
                dc.left_axis_x = static.right_axis_x
            dc.speed.x *= -dc.bouncy
        else:
            if dc.center.y < static.center.y:
                dc.down_axis_y = static.up_axis_y
                dc.speed.x *= static.resistance.x
            else:
                dc.up_axis_y = static.down_axis_y
            dc.speed.y *= -dc.bouncy

    def _process_kinematic_collision(self, dc, kinematic):
        platform_move = Vector2D(
            kinematic.pos.x - kinematic.prev_pos.x,
            kinematic.pos.y - kinematic.prev_pos.y
        )
        
        was_above = (dc.down_axis_y <= kinematic.prev_pos.y and 
                    dc.right_axis_x > kinematic.left_axis_x and 
                    dc.left_axis_x < kinematic.right_axis_x)
        
        overlap_x = min(dc.right_axis_x, kinematic.right_axis_x) - max(dc.left_axis_x, kinematic.left_axis_x)
        overlap_y = min(dc.down_axis_y, kinematic.down_axis_y) - max(dc.up_axis_y, kinematic.up_axis_y)
        
        if was_above and overlap_y > 0 and dc.speed.y >= 0:
            dc.down_axis_y = kinematic.up_axis_y
            dc.pos.x += platform_move.x
            dc.pos.y += platform_move.y
            dc.speed.y = 0
            dc.speed.x *= kinematic.resistance.x
            
        else:
            if overlap_x < overlap_y:
                if dc.center.x < kinematic.center.x:
                    dc.right_axis_x = kinematic.left_axis_x
                else:
                    dc.left_axis_x = kinematic.right_axis_x
                dc.speed.x *= -dc.bouncy
            else:
                if dc.center.y < kinematic.center.y:
                    dc.down_axis_y = kinematic.up_axis_y
                    dc.speed.y = 0
                else:
                    dc.up_axis_y = kinematic.down_axis_y
                    dc.speed.y *= -dc.bouncy

    def render(self, surf: pygame.Surface):
        width, height = surf.get_width(), surf.get_height()
        
        for collider in self._static_colliders:
            self._draw_collider(surf, collider, (100, 100, 100), width, height)
        
        for collider in self._dynamic_colliders:
            self._draw_collider(surf, collider, (0, 150, 0), width, height)
        
        for collider in self._kinematic_colliders:
            self._draw_collider(surf, collider, (0, 0, 150), width, height)

    def _draw_collider(self, surf, collider, color, surf_width, surf_height):
        x, y = int(collider.pos.x), int(collider.pos.y)
        if not (0 <= x <= surf_width and 0 <= y <= surf_height):
            return
            
        w, h = int(collider.width), int(collider.height)
        gfxdraw.rectangle(surf, (x, y, w, h), color)
        gfxdraw.line(surf, x, y, x + w, y + h, color)
        gfxdraw.line(surf, x + w, y, x, y + h, color)
        
        if collider.speed.x != 0 or collider.speed.y != 0:
            start_x, start_y = x, y - 5
            end_x = start_x + int(collider.speed.x * 2)
            end_y = start_y + int(collider.speed.y * 2)
            gfxdraw.line(surf, start_x, start_y, end_x, end_y, (255, 0, 0))