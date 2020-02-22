from math import cos, sin

from Projectile import Projectile


class Tank:
    _delta_angle = 10
    _cooldown = 10
    _current_charge = 0
    _projectile_speed = 40
    _projectile_radius = 5.0

    def __init__(self, speed, x, y, direction, size, tank_index):
        self.speed = speed
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.hp = 50
        self.tank_index = tank_index

    def move_timestep(self, x_max, y_max):
        if 0 <= self.x + sin(self.direction) * self.speed <= x_max:
            self.x += sin(self.direction) * self.speed
        if 0 <= self.y + cos(self.direction) * self.speed < y_max:
            self.y += cos(self.direction) * self.speed
        self._current_charge += 1

    def turn_right(self):
        self.direction += self._delta_angle
        self._current_charge += 1

    def turn_left(self):
        self.direction -= self._delta_angle
        self._current_charge += 1

    def shoot_projectile(self):
        if self._current_charge >= self._cooldown:
            self._current_charge = 0
            projectile = Projectile(self._projectile_speed, self.x + self.size * sin(self.direction), self.y + self.size * cos(self.direction), self.direction, self._projectile_radius, self.tank_index)
            return projectile
