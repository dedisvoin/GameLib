import pygame
import math
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простой физический движок")
clock = pygame.time.Clock()
FPS = 60

class Polygon:
    def __init__(self, vertices, color, position=(0, 0)):
        self.vertices = [list(v) for v in vertices]  # Вершины в локальных координатах
        self.position = list(position)  # Позиция объекта [x, y]
        self.velocity = [0.0, 0.0]  # Скорость [vx, vy]
        self.color = color  # Цвет для отрисовки
        self.static = False  # Если True, объект не двигается при столкновениях

    def get_edges(self):
        """Возвращает вектора всех рёбер полигона"""
        edges = []
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            edge = [p2[0] - p1[0], p2[1] - p1[1]]
            edges.append(edge)
        return edges

    def get_axes(self):
        """Возвращает нормали к рёбрам (для SAT)"""
        axes = []
        for edge in self.get_edges():
            # Перпендикуляр к ребру (нормаль)
            normal = [-edge[1], edge[0]]
            # Нормализуем вектор
            length = math.sqrt(normal[0]**2 + normal[1]**2)
            if length > 0:
                normal = [normal[0]/length, normal[1]/length]
            axes.append(normal)
        return axes

    def get_projection(self, axis):
        """Проецирует полигон на ось и возвращает [min, max]"""
        dots = []
        for vertex in self.vertices:
            # Глобальная позиция вершины
            global_vertex = [vertex[0] + self.position[0], vertex[1] + self.position[1]]
            # Проекция на ось
            dot = global_vertex[0] * axis[0] + global_vertex[1] * axis[1]
            dots.append(dot)
        return [min(dots), max(dots)]

    def get_global_vertices(self):
        """Возвращает вершины в глобальных координатах (для отрисовки)"""
        return [[v[0] + self.position[0], v[1] + self.position[1]] for v in self.vertices]

    def draw(self, surface):
        """Отрисовывает полигон на экране"""
        global_vertices = self.get_global_vertices()
        pygame.draw.polygon(surface, self.color, [(int(v[0]), int(v[1])) for v in global_vertices])


def check_collision(poly1, poly2):
    """Проверяет столкновение между двумя полигонами с помощью SAT"""
    axes = poly1.get_axes() + poly2.get_axes()

    for axis in axes:
        proj1 = poly1.get_projection(axis)
        proj2 = poly2.get_projection(axis)

        # Если проекции не пересекаются - нет столкновения
        if proj1[1] < proj2[0] or proj2[1] < proj1[0]:
            return False

    return True


def resolve_collision(poly1, poly2):
    """Разрешает столкновение между двумя полигонами"""
    overlap = float('inf')
    smallest_axis = None

    axes = poly1.get_axes() + poly2.get_axes()

    for axis in axes:
        proj1 = poly1.get_projection(axis)
        proj2 = poly2.get_projection(axis)

        # Находим глубину перекрытия
        current_overlap = min(proj1[1], proj2[1]) - max(proj1[0], proj2[0])

        if current_overlap < overlap:
            overlap = current_overlap
            smallest_axis = axis

    # Сдвигаем полигоны вдоль smallest_axis
    if smallest_axis is not None:
        direction = [smallest_axis[0] * overlap, smallest_axis[1] * overlap]
        
        if not poly1.static and not poly2.static:
            poly1.position[0] -= direction[0] * 0.5
            poly1.position[1] -= direction[1] * 0.5
            poly2.position[0] += direction[0] * 0.5
            poly2.position[1] += direction[1] * 0.5
        elif poly1.static:
            poly2.position[0] += direction[0]
            poly2.position[1] += direction[1]
        else:
            poly1.position[0] -= direction[0]
            poly1.position[1] -= direction[1]


def update_physics(objects, dt):
    """Обновляет физику для всех объектов"""
    # Обновление позиций
    for obj in objects:
        if not obj.static:
            obj.position[0] += obj.velocity[0] * dt
            obj.position[1] += obj.velocity[1] * dt

    # Проверка столкновений между всеми парами объектов
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if check_collision(objects[i], objects[j]):
                resolve_collision(objects[i], objects[j])


# Создаём тестовые объекты
objects = [
    # Статичный "пол" (невыпуклый)
    Polygon([[0, 550], [200, 500], [400, 550], [600, 500], [800, 550], [800, 600], [0, 600]], 
             (100, 100, 100), position=(0, 0)),
    
    # Квадрат
    Polygon([[0, 0], [50, 0], [50, 50], [0, 50]], (255, 0, 0), position=(100, 100)),
    
    # Треугольник
    Polygon([[0, 0], [25, 50], [50, 0]], (0, 255, 0), position=(300, 100)),
    
    # Звезда (невыпуклая)
    Polygon([[0, 0], [10, 30], [30, 30], [15, 50], [25, 80], [0, 60], [-25, 80], [-15, 50], [-30, 30], [-10, 30]], 
             (0, 0, 255), position=(500, 100))
]

# Делаем пол статичным
objects[0].static = True

# Задаём начальные скорости
objects[1].velocity = [0, 100]  # Квадрат падает вниз
objects[2].velocity = [20, 80]   # Треугольник движется вправо и вниз
objects[3].velocity = [-20, 120] # Звезда движется влево и вниз

# Основной игровой цикл
running = True
while running:
    dt = 1.0 / FPS
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Обновление физики
    update_physics(objects, dt)
    
    # Отрисовка
    screen.fill((240, 240, 240))
    for obj in objects:
        obj.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()