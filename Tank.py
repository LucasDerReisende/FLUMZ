from math import cos, sin

from Projectile import Projectile


class Tank:
    _delta_angle = 10
    _cooldown = 100
    _current_charge = 0
    _projectile_speed = 0.5
    _projectile_radius = 1.0

    def __init__(self, speed, x, y, direction):
        self.speed = speed
        self.x = x
        self.y = y
        self.direction = direction

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
            projectile = Projectile(self._projectile_speed, self.x, self.y, self.direction, self._projectile_radius)
            return projectile
