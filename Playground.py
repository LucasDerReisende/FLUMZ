from random import randint

from Player1 import do_move_player_1
from Player2 import do_move_player_2
from Tank import Tank


class Playground:
    projectiles_array = []

    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.tank1 = Tank(0.1, randint(0, x_max), randint(0, y_max), randint(0, 359))
        self.tank2 = Tank(0.1, randint(0, x_max), randint(0, y_max), randint(0, 359))


    def _do_timestep(self):
        objects_to_remove = []
        for i in self.projectiles_array:
            i.move_timestep(self.x_max, self.y_max)
            if not i.is_at_border(self.x_max, self.y_max):
                result = i.is_hitting_tank((self.tank1, self.tank2))
                if result[0] == True:
                    return 'Projectile hit Tank 1'
                elif result[1] == True:
                    return 'Projectile hit Tank 2'
            else:
                objects_to_remove.append(i)

        for i in objects_to_remove:
            self.projectiles_array.remove(i)

        self.tank1.move_timestep(self.x_max, self.y_max)
        self.tank2.move_timestep(self.x_max, self.y_max)

        player_1_result = do_move_player_1()
        if player_1_result == 'right':
            self.tank1.turn_right()
        elif player_1_result == 'left':
            self.tank1.turn_left()
        elif player_1_result == 'shoot':
            self.projectiles_array.append(self.tank1.shoot_projectile())

        player_2_result = do_move_player_2()
        if player_2_result == 'right':
            self.tank2.turn_right()
        elif player_2_result == 'left':
            self.tank2.turn_left()
        elif player_2_result == 'shoot':
            projectile = self.tank2.shoot_projectile()
            self.projectiles_array.append(projectile)

        return 'still playing'

    def start_game(self):
        while True:
            timestep_result = self._do_timestep()
            if timestep_result != 'still playing':
                return timestep_result
