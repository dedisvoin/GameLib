import sys
from time import sleep
sys.path.append("./")
import pygame
from src.promises import BasePromise
from src.app import AppWindow
from src.maths import get_perlin_noise
from src.render.text import TextField
import math
import threading

window = AppWindow((800, 600), "2D World Generator", vsync=False)
window.set_view_information_in_window(True)
window.set_waited_fps(120)

CHUNK_SIZE = 32
TILE_SIZE = 5
VIEW_DISTANCE = 15

chunk_width = CHUNK_SIZE * TILE_SIZE

CHINK_GENERATED_TEXT_FIELD = TextField('arial', 16, 'black', True)

def generate_chunk(promise: BasePromise, chunk_pos: tuple[int, int]) -> pygame.Surface:
    chunk_surface = pygame.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))
    colors = {
        0: (34, 139, 34),
        1: (0, 191, 255),
        2: (238, 214, 175),
        3: (169, 169, 169)
    }
    
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            world_x = chunk_pos[0] * CHUNK_SIZE + x
            world_y = chunk_pos[1] * CHUNK_SIZE + y
            
            uper = get_perlin_noise(world_x, world_y - 1, 6, 0.5, 0.1)
            height = get_perlin_noise(world_x, world_y, 6, 0.5, 0.1)
            
            if height > 0.1 and uper < 0.1:
                tile_type = 0
            elif height > 0.1:
                tile_type = 3
            else:
                tile_type = 1
            
            pygame.draw.rect(chunk_surface, colors[tile_type], 
                           (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    sleep(1)
    return chunk_surface

class WorldGenerator:
    def __init__(self):
        self.chunks = {}
        self.pending_chunks = {}
        self.colors = {
            0: (34, 139, 34),
            1: (0, 191, 255),
            2: (238, 214, 175),
            3: (169, 169, 169)
        }
        self.generation_thread = threading.Thread(target=self.chunk_generation_loop, daemon=True)
        self.generation_thread.start()
        self.camera_x = 0
        self.camera_y = 0
        self.lock = threading.Lock()

    def get_chunk_key(self, chunk_x: int, chunk_y: int) -> str:
        return f"{chunk_x}:{chunk_y}"

    def chunk_generation_loop(self):
        while True:
            try:
                center_chunk_x = math.floor(self.camera_x / (CHUNK_SIZE * TILE_SIZE))
                center_chunk_y = math.floor(self.camera_y / (CHUNK_SIZE * TILE_SIZE))
                self.generate_chunks_around(center_chunk_x, center_chunk_y)
                self.check_pending_chunks()
                sleep(0.5)
            except: ...

    def generate_chunks_around(self, center_x: int, center_y: int):
        needed_chunks = []
        
        for dy in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
            for dx in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
                chunk_x = center_x + dx
                chunk_y = center_y + dy
                chunk_key = self.get_chunk_key(chunk_x, chunk_y)
                
                with self.lock:
                    if chunk_key not in self.chunks and chunk_key not in self.pending_chunks:
                        needed_chunks.append((chunk_x, chunk_y))

        for chunk_pos in needed_chunks:
            chunk_key = self.get_chunk_key(chunk_pos[0], chunk_pos[1])
            promise = BasePromise(generate_chunk, timeout=5.0, id=chunk_key)
            promise(True, chunk_pos)


            with self.lock:
                self.pending_chunks[chunk_key] = promise
            

    def check_pending_chunks(self):
        completed_chunks = []
        with self.lock:
            for chunk_key, promise in self.pending_chunks.items():
                if promise.is_ready():
                    try:
                        self.chunks[chunk_key] = promise.await_result()

                        completed_chunks.append(chunk_key)
                    except Exception as e:
                        print(f"Error generating chunk {chunk_key}: {e}")
                        completed_chunks.append(chunk_key)
            
            for chunk_key in completed_chunks:
                del self.pending_chunks[chunk_key]

    def render(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        self.camera_x = camera_x
        self.camera_y = camera_y
        center_chunk_x = math.floor(camera_x / (CHUNK_SIZE * TILE_SIZE))
        center_chunk_y = math.floor(camera_y / (CHUNK_SIZE * TILE_SIZE))
        
        for dy in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
            for dx in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
                chunk_x = center_chunk_x + dx
                chunk_y = center_chunk_y + dy
                chunk_key = self.get_chunk_key(chunk_x, chunk_y)
                
                chunk_screen_x = chunk_x * CHUNK_SIZE * TILE_SIZE - camera_x
                chunk_screen_y = chunk_y * CHUNK_SIZE * TILE_SIZE - camera_y
                
                with self.lock:
                    if chunk_key in self.chunks:
                        chunk_surface = self.chunks[chunk_key]
                        surface.blit(chunk_surface, (chunk_screen_x, chunk_screen_y))
                        pygame.draw.rect(surface, (100, 100,100), (chunk_screen_x, chunk_screen_y, chunk_width, chunk_width),1)
                    elif chunk_key in self.pending_chunks:
                        pygame.draw.rect(surface, (200, 100,100), (chunk_screen_x, chunk_screen_y, chunk_width, chunk_width),1)

world = WorldGenerator()

camera_x = 0
camera_y = 0
camera_speed = 20

while window.is_opened:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= camera_speed
    if keys[pygame.K_RIGHT]:
        camera_x += camera_speed
    if keys[pygame.K_UP]:
        camera_y -= camera_speed
    if keys[pygame.K_DOWN]:
        camera_y += camera_speed

    window.fill((128, 128, 128))

    world.render(window.surf, camera_x, camera_y)

    window.update()

pygame.quit()