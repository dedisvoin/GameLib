import numpy as np
from time import time
import importer
from src.core.gpu import GPU
from src.app import AppWindow, AppSubProcess
from src.render.base import draw_circle

class ParticleApp:
    def __init__(self, width=800, height=600, num_particles=10000):
        self.width = width
        self.height = height
        self.app = AppWindow((width, height), "Particle Simulation", vsync=False)
        self.app.set_waited_fps(6000)
        self.app.set_view_information_in_title()
        self.num_particles = num_particles

        self.gpu = GPU(use_async=True)

        self.init_particles()
        self.load_kernel()

    def init_particles(self):
        self.positions_x = np.random.uniform(0, self.width, self.num_particles).astype(np.float32)
        self.positions_y = np.random.uniform(0, self.height, self.num_particles).astype(np.float32)
        self.velocities_x = np.zeros(self.num_particles, dtype=np.float32)
        self.velocities_y = np.zeros(self.num_particles, dtype=np.float32)
        self.colors = np.random.rand(self.num_particles, 3).astype(np.float32)

        if self.gpu:
            self.pos_x_buf = self.gpu.buffer(self.positions_x)
            self.pos_y_buf = self.gpu.buffer(self.positions_y)
            self.vel_x_buf = self.gpu.buffer(self.velocities_x)
            self.vel_y_buf = self.gpu.buffer(self.velocities_y)
            self.colors_buf = self.gpu.buffer(self.colors)

    def load_kernel(self):
        PARTICLE_KERNEL = """
        __kernel void update_particles(
            __global float* pos_x,
            __global float* pos_y,
            __global float* vel_x,
            __global float* vel_y,
            __global float* colors,
            float delta_time,
            float center_x,
            float center_y,
            float gravity,
            float width,
            float height
        ) {
            int idx = get_global_id(0);

            float dx = center_x - pos_x[idx];
            float dy = center_y - pos_y[idx];
            float dist = sqrt(dx*dx + dy*dy);

            if (dist > 0.1f) {
                float force = gravity / (dist + 0.1f);
                vel_x[idx] += dx * force * delta_time;
                vel_y[idx] += dy * force * delta_time;
            }

            pos_x[idx] += vel_x[idx] * delta_time;
            pos_y[idx] += vel_y[idx] * delta_time;

            if (pos_x[idx] < 0 || pos_x[idx] > width) vel_x[idx] *= -0.5f;
            if (pos_y[idx] < 0 || pos_y[idx] > height) vel_y[idx] *= -0.5f;

            float speed = sqrt(vel_x[idx]*vel_x[idx] + vel_y[idx]*vel_y[idx]);
            colors[idx*3] = min(1.0f, speed * 0.1f);
            colors[idx*3+1] = max(0.0f, 1.0f - speed*0.2f);
            float b = pos_x[idx] / width;
            if (b < 0) b = 0;
        }
        """

        if self.gpu:
            self.gpu.compile(PARTICLE_KERNEL, "particle_program")

    def update(self):
        center_x = self.width / 2.0
        center_y = self.height / 2.0
        gravity = 100.0

        if self.gpu:
            self.gpu.run(
                "particle_program", "update_particles", (self.num_particles,),
                self.pos_x_buf, self.pos_y_buf, self.vel_x_buf, self.vel_y_buf, self.colors_buf,
                np.float32(0.01), np.float32(center_x), np.float32(center_y), np.float32(gravity),
                np.float32(self.width), np.float32(self.height)
            )

            self.positions_x = self.gpu.result(self.pos_x_buf)
            self.positions_y = self.gpu.result(self.pos_y_buf)
            self.velocities_x = self.gpu.result(self.vel_x_buf)
            self.velocities_y = self.gpu.result(self.vel_y_buf)
            self.colors = self.gpu.result(self.colors_buf).reshape(self.num_particles, 3)
        

    def render(self):
        self.app.fill((0, 0, 0))

        for i in range(self.num_particles):
            x = int(self.positions_x[i])
            y = int(self.positions_y[i])
            color = (int(self.colors[i,0] * 255), int(self.colors[i,1] * 255), int(self.colors[i,2] * 255))
            draw_circle(self.app.surf, (x, y), 1, color)

        self.app.update()

    def run(self):
        while self.app.is_opened:
            self.render()




if __name__ == "__main__":
    app = ParticleApp(width=800, height=600, num_particles=10000)

    AppSubProcess(app.update, 0, 'update').start()
    app.run()