import threading
import time
from random import randint
import tkinter as tk
import numpy as np
import cProfile

from Player import Player
from Tank import Tank
from math import sin, cos, ceil


class Playground:
    projectiles_array = []

    def __init__(self, x_max, y_max, is_displayed, player1, player2):
        self.x_max = x_max
        self.y_max = y_max
        self.zones_x = 20
        self.zones_y = 20

        self.tank1 = Tank(5, randint(0, x_max), randint(0, y_max), randint(0, 359), 10, 0)
        self.tank2 = Tank(5, randint(0, x_max), randint(0, y_max), randint(0, 359), 10, 1)

        self.player1 = player1
        self.player2 = player2

        self.is_displayed = is_displayed

        if self.is_displayed:
            self.master = tk.Tk()
            canvas_width, canvas_height = 800, 800
            screen_width, screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            x, y = (screen_width / 2) - (canvas_width / 2), (screen_height / 2) - (canvas_height / 2)
            self.master.geometry('%dx%d+%d+%d' % (canvas_width, canvas_height, x, y))
            self.visual_playground = tk.Canvas(self.master, width=canvas_width, height=canvas_height)
            self.hp = tk.Label(master = self.master, text="Hp: ")
            self.hp.pack()

    def draw_tanks_on_field(self):
        size = 10
        scale_x, scale_y = self.visual_playground.winfo_width() / self.x_max, self.visual_playground.winfo_height() / self.y_max
        x1, y1, dir1, x2, y2, dir2 = self.tank1.x * scale_x, self.tank1.y * scale_y, self.tank1.direction, self.tank2.x * scale_x, self.tank2.y * scale_y, self.tank2.direction
        points_tank1, points_tank2, delta_x, delta_y = [], [], [-size, size, size, -size], [size, size, -size, -size]
        for i in range(0,4,1):
            rot_x1, rot_y1 = x1 + (delta_x[i] * cos(dir1) - delta_y[i] * sin(dir1)), y1 + (delta_x[i] * sin(dir1) + delta_y[i] * cos(dir1))
            rot_x2, rot_y2 = x2 + (delta_x[i] * cos(dir2) - delta_y[i] * sin(dir2)), y2 + (delta_x[i] * sin(dir2) + delta_y[i] * cos(dir2))
            points_tank1.append(rot_x1)
            points_tank1.append(rot_y1)
            points_tank2.append(rot_x2)
            points_tank2.append(rot_y2)
        self.visual_playground.create_polygon(points_tank1, fill='blue')
        self.visual_playground.create_polygon(points_tank2, fill='red')
        self.tank1 = Tank(0.1, randint(0, self.x_max), randint(0, self.y_max), randint(0, 359), 0)
        self.tank2 = Tank(0.1, randint(0, self.x_max), randint(0, self.y_max), randint(0, 359), 1)

    def draw_projectiles_on_field(self):
        scale_x, scale_y = self.visual_playground.winfo_width() / self.x_max, self.visual_playground.winfo_height() / self.y_max
        for i in [e for e in self.projectiles_array if e is not None]:
            self.visual_playground.create_oval(i.x * scale_x, i.y * scale_y, (i.x * scale_x) + 5, (i.y * scale_y) + 5, fill="red")

    def visualize_updated_playground(self):
        self.visual_playground.delete("all")
        self.draw_tanks_on_field()
        self.draw_projectiles_on_field()
        self.hp.config(text="Hp Tank1: " + str(self.tank1.hp) + "          Hp Tank2: " + str(self.tank2.hp))
        self.visual_playground.update()
        self.visual_playground.pack()

    def _do_timestep(self, move_player1, move_player2):
        objects_to_remove = []
        for i in [e for e in self.projectiles_array if e is not None]:
            i.move_timestep(self.x_max, self.y_max)
            if not i.is_at_border(self.x_max, self.y_max):
                result = i.is_hitting_tank((self.tank1, self.tank2))
                if result[0] == True:
                    self.tank1.hp -= 10
                    #print('Projectile hit Tank 1')
                    return 'Projectile hit Tank 1'
                elif result[1] == True:
                    self.tank2.hp -= 10
                    #print('Projectile hit Tank 2')
                    return 'Projectile hit Tank 2'
            else:
                objects_to_remove.append(i)

        for i in objects_to_remove:
            self.projectiles_array.remove(i)

        self.tank1.move_timestep(self.x_max, self.y_max)
        self.tank2.move_timestep(self.x_max, self.y_max)

        player_1_result = self.player1.do_move(self.get_state(self.player1), move_player1)
        if player_1_result == 'right':
            self.tank1.turn_right()
        elif player_1_result == 'left':
            self.tank1.turn_left()
        elif player_1_result == 'shoot':
            projectile = self.tank1.shoot_projectile()
            if projectile != None:
                self.projectiles_array.append(projectile)

        player_2_result = self.player2.do_move(self.get_state(self.player2), move_player2)
        if player_2_result == 'right':
            self.tank2.turn_right()
        elif player_2_result == 'left':
            self.tank2.turn_left()
        elif player_2_result == 'shoot':
            projectile = self.tank2.shoot_projectile()
            if projectile != None:
                self.projectiles_array.append(projectile)

        return 'still playing'

    def reset_game(self):
        self.tank1 = Tank(5, randint(0, self.x_max), randint(0, self.y_max), randint(0, 359), 10, 0)
        self.tank2 = Tank(5, randint(0, self.x_max), randint(0, self.y_max), randint(0, 359), 10, 1)

    def start_game(self):
        self.reset_game()
        print('Start game')
        x = 0
        while x <= 1000:
            x += 1
            timestep_result = self._do_timestep(None, None)
            if self.is_displayed:
                time.sleep(0.05)
                thread_visual = threading.Thread(target=self.visualize_updated_playground())
                thread_visual.daemon = True
                thread_visual.start()
            #if timestep_result != 'still playing':
            #    return timestep_result
            if self.tank1.hp == 0:
                return "Tank 2 won the game with " + str(self.tank2.hp) + " hp"
            elif self.tank2.hp == 0:
                return "Tank 1 won the game with " + str(self.tank1.hp) + " hp"
        if self.is_displayed:
            self.field_to_play_on.master.mainloop()

    def get_state(self, player):
        state = np.zeros((self.zones_x, self.zones_y))
        zone_x_tank1, zone_y_tank1, zone_x_tank2, zone_y_tank2 = ceil((self.tank1.x/self.x_max) * self.zones_x), ceil((self.tank1.y/self.y_max) * self.zones_y), ceil((self.tank2.x/self.x_max) * self.zones_x), ceil((self.tank2.y/self.y_max) * self.zones_y)
        if player == self.player1:
            state[zone_x_tank1-1, zone_y_tank1-1] = 1
            state[zone_x_tank2-1, zone_y_tank2-1] = -1
        elif player == self.player2:
            state[zone_x_tank1-1, zone_y_tank1-1] = -1
            state[zone_x_tank2-1, zone_y_tank2-1] = 1
        else:
            print('Player does not exist')

        for projectile in [e for e in self.projectiles_array if e is not None]:
            if projectile.x < self.x_max and projectile.y < self.y_max:
                zone_x_proj, zone_y_proj = ceil((projectile.x / self.x_max) * self.zones_x), ceil(
                    (projectile.y / self.y_max) * self.zones_y)
                if player == self.player1:
                    if projectile.tank_index == 0:
                        state[zone_x_proj-1, zone_y_proj-1] = 0.5
                    else:
                        state[zone_x_proj - 1, zone_y_proj - 1] = -0.5
                elif player == self.player2:
                    if projectile.tank_index == 0:
                        state[zone_x_proj - 1, zone_y_proj - 1] = 0.5
                    else:
                        state[zone_x_proj - 1, zone_y_proj - 1] = -0.5

        #return state.reshape(1, 20, 20)
        return state.reshape([1, 1, self.zones_x * self.zones_y])



    def reward(self, player):
        if player == self.player1:
            reward = (self.tank1.hp / 50.0) - (self.tank2.hp / 50.0)
        elif player == self.player2:
            reward = (self.tank2.hp / 50.0) - (self.tank1.hp / 50.0)
        else:
            print('Player does not exist')

        return reward

    def simulate_time_step(self, player, action):
        if player == self.player1:
            self._do_timestep(action, None)
        elif player == self.player2:
            self._do_timestep(None, action)
        else:
            print('Player does not exist')

        done = False
        if self.tank1.hp == 0 or self.tank2.hp == 0:
            done = True

        return self.get_state(player), self.reward(player), done