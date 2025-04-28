import pygame
import moderngl
import numpy as np
from typing import Tuple, Optional, Union

class Shader:
    def __init__(self, vertex_shader: str, fragment_shader: str):
        try:
            self.vertex_shader = vertex_shader
            self.fragment_shader = fragment_shader

            self.__ctx = moderngl.create_context()
            self.__program = self.__ctx.program(
                vertex_shader=self.vertex_shader,
                fragment_shader=self.fragment_shader
            )
            self.__vertices = np.array([
                # x, y    # u, v
                -1, -1,    0, 0,
                1, -1,    1, 0,
                -1,  1,    0, 1,
                1,  1,    1, 1
            ], dtype='f4')
            self.__vbo = self.__ctx.buffer(self.__vertices)
            self.__vao = self.__ctx.simple_vertex_array(self.__program, self.__vbo, 'in_vert', 'in_uv')
            self.__inited = True
        except Exception as e:
            print(f"Shader is not inited. Use OpenGL flag.")
            self.__inited = False


    def send(self, name: str, value: int | float):
        if self.__inited:
            try:
                self.__program[name] = value
            except KeyError:
                print(f"Error: {name} is not a valid uniform name.")

    def render_from_surf(self, surf: pygame.Surface):
        if self.__inited:
            texture = self.__ctx.texture(surf.get_size(), 4)
            texture.write(surf.get_buffer())
            texture.use(0)
            self.__ctx.clear()
            self.__vao.render(moderngl.TRIANGLE_STRIP)
            texture.release()


        
