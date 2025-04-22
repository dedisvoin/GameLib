import time
import importer
import pygame
from src.promises import BasePromise
from src.app import AppWindow

import random
from noise import pnoise2

class TestChunkGeneration:
    def setUp(self):
        self.app = AppWindow([1800, 800], "Chunk Generation Test", vsync=False)
        self.app.set_waited_fps(60)
        self.app.set_view_information_in_title()
        self.chunk_size = 8
        self.tile_size = 4
        self.chunks = {}
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 20
        self.noise_scale = 25.0  
        self.chunk_surfaces = {}  
        self.generating_chunks = set() 
        
    def generate_chunk(self, chunk_x, chunk_y):
        chunk = []
        for y in range(self.chunk_size):
            row = []
            for x in range(self.chunk_size):
                nx = (chunk_x * self.chunk_size + x) / self.noise_scale
                ny = (chunk_y * self.chunk_size + y) / self.noise_scale
                noise_value = pnoise2(nx, ny, octaves=3, persistence=0.5, lacunarity=2.0)
                noise_value = (noise_value + 1) / 2

                if noise_value < 0.3:
                    tile = 0 
                elif noise_value < 0.45:
                    tile = 1  
                elif noise_value < 0.55:
                    tile = 2  
                elif noise_value < 0.7:
                    tile = 3 
                elif noise_value < 0.85:
                    tile = 4  
                else:
                    tile = 5 
                row.append(tile)
            chunk.append(row)

        return chunk

    def create_chunk_surface(self, chunk_data):
        surface = pygame.Surface((self.chunk_size * self.tile_size, self.chunk_size * self.tile_size)).convert()
        for row_idx, row in enumerate(chunk_data):
            for col_idx, tile in enumerate(row):

                colors = {
                    0: (0, 0, 139),    
                    1: (0, 50, 255),  
                    2: (238, 214, 175), 
                    3: (34, 139, 34),   
                    4: (0, 100, 0),   
                    5: (128, 128, 128)  
                }
                pygame.draw.rect(surface, colors[tile],
                            (col_idx * self.tile_size, row_idx * self.tile_size,
                             self.tile_size, self.tile_size))

        return surface

    def test_async_chunk_generation(self):
        def chunk_generator(promise, x, y):
            chunk_key = f"{x}:{y}"
            chunk_data = self.generate_chunk(x, y)
            self.chunks[chunk_key] = chunk_data
            chunk_surface = self.create_chunk_surface(chunk_data)
            time.sleep(3)
            self.chunk_surfaces[chunk_key] = chunk_surface
            self.generating_chunks.remove(chunk_key)


        running = True

        screen_width = self.app.surf.get_width()
        screen_height = self.app.surf.get_height()
        chunks_x = (screen_width // (self.chunk_size * self.tile_size)) + 2
        chunks_y = (screen_height // (self.chunk_size * self.tile_size)) + 2

        promises = []
        start_x = -chunks_x // 2
        start_y = -chunks_y // 2
        for x in range(start_x, start_x + chunks_x):
            for y in range(start_y, start_y + chunks_y):
                promise = BasePromise(chunk_generator)
                chunk_key = f"{x}:{y}"
                self.generating_chunks.add(chunk_key)
                promise(True, x, y)
                promises.append(promise)

        while self.app.is_opened:
            keys = pygame.key.get_pressed()
            old_camera_x = self.camera_x
            old_camera_y = self.camera_y
            
            if keys[pygame.K_LEFT]:
                self.camera_x += self.camera_speed
            if keys[pygame.K_RIGHT]:
                self.camera_x -= self.camera_speed
            if keys[pygame.K_UP]:
                self.camera_y += self.camera_speed
            if keys[pygame.K_DOWN]:
                self.camera_y -= self.camera_speed

            current_chunk_x = -int(self.camera_x / (self.chunk_size * self.tile_size))
            current_chunk_y = -int(self.camera_y / (self.chunk_size * self.tile_size))
            
            visible_start_x = current_chunk_x - chunks_x // 2
            visible_end_x = current_chunk_x + chunks_x // 2
            visible_start_y = current_chunk_y - chunks_y // 2
            visible_end_y = current_chunk_y + chunks_y // 2
            
            for x in range(visible_start_x - 1, visible_end_x + 8):
                for y in range(visible_start_y - 1, visible_end_y + 8):
                    chunk_key = f"{x}:{y}"
                    if chunk_key not in self.chunks and chunk_key not in self.generating_chunks:
                        promise = BasePromise(chunk_generator)
                        self.generating_chunks.add(chunk_key)
                        promise(True, x, y)
                        promises.append(promise)

            self.app.fill((100, 100, 100))
            
            for promise in promises[:]:
                if promise.is_ready():
                    chunk_data = promise.await_result()
                    promises.remove(promise)

            try:
                visible_chunks = []
                for chunk_key, surface in self.chunk_surfaces.items():
                    x, y = map(int, chunk_key.split(':'))
                    chunk_screen_x = (x * self.chunk_size) * self.tile_size + 400 + self.camera_x
                    chunk_screen_y = (y * self.chunk_size) * self.tile_size + 300 + self.camera_y
                    chunk_width = self.chunk_size * self.tile_size
                    
                    if (chunk_screen_x + chunk_width < -chunk_width or 
                        chunk_screen_x > self.app.surf.get_width() + chunk_width or 
                        chunk_screen_y + chunk_width < -chunk_width or 
                        chunk_screen_y > self.app.surf.get_height() + chunk_width):
                        continue
                        
                    visible_chunks.append((surface, (chunk_screen_x, chunk_screen_y)))
                
                self.app.surf.blits(visible_chunks)

                for chunk_key in self.generating_chunks:
                    x, y = map(int, chunk_key.split(':'))
                    chunk_screen_x = (x * self.chunk_size) * self.tile_size + 400 + self.camera_x
                    chunk_screen_y = (y * self.chunk_size) * self.tile_size + 300 + self.camera_y
                    chunk_width = self.chunk_size * self.tile_size
                    pygame.draw.rect(self.app.surf, (200, 100, 100), 
                                   (chunk_screen_x, chunk_screen_y, chunk_width, chunk_width), 1)
                    
            except Exception as e:
                print(f"Error rendering chunks: {e}")

            self.app.update()

        pygame.quit()

if __name__ == '__main__':
    test = TestChunkGeneration()
    test.setUp()
    test.test_async_chunk_generation()