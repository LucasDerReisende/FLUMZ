from math import cos, sin
import numpy as np


class Projectile:

    def __init__(self, speed, x, y, direction, radius, tank_index):
        self.speed = speed
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = radius
        self.tank_index = tank_index

    def move_timestep(self, x_max, y_max):
        if 0 <= self.x + sin(self.direction) * self.speed <= x_max:
            self.x += sin(self.direction) * self.speed
        if 0 <= self.y + cos(self.direction) * self.speed < y_max:
            self.y += cos(self.direction) * self.speed

    def is_hitting_tank(self, tanks):
        arr = []
        for i in tanks:
            if self.tank_index != len(arr):
                if (i.x - self.x) ** 2 + (i.y - self.y) ** 2 <= self.radius ** 2:
                    arr.append(True)
                else:
                    arr.append(False)
            else:
                arr.append(False)
        return arr

    def is_at_border(self, x_max, y_max):
        return not (0 <= self.x <= x_max and 0 <= self.y <= y_max)
