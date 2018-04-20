import pygame
import sys
import json
from training.mars_lander.pygame_test.lander import Lander
from training.mars_lander.pygame_test.terrain import Terrain
from training.mars_lander.pygame_test.ui import Ui
from training.mars_lander.pygame_test.path_manager import PathManager


class GameEngine():

    def __init__(self, terrain_topology, lander_init_values):
        pygame.init()
        self.window = pygame.display.set_mode((700, 300))
        self.screen = pygame.display.get_surface()
        self.lander = Lander(lander_init_values)
        self.terrain = Terrain(terrain_topology)
        self.path_mng = PathManager(lander_init_values, terrain_topology)
        self.ui = Ui(self.path_mng)

        self.is_running = True
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0

    def start(self):
        self.prepare()
        self.draw()
        self.path_edit_loop()

    def prepare(self):
        pygame.key.set_repeat(200, 50)
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0
        self.lander.restart()

    def path_edit_loop(self):
        while self.is_running:
            self.process_event()
            self.path_mng.draw(self.screen)
            pygame.display.flip()
            pygame.time.wait(100)

    def game_loop(self):
        delta_time = 0
        self.clock.tick(10)
        while self.is_running:
            self.process_event()
            # update data of objects on screen
            self.update(delta_time)
            # update objects position on screend
            self.draw()
            pygame.time.wait(100)
            delta_time = self.clock.get_rawtime() / 10

    def update(self, dt):
        self.elapsed_time += dt
        #
        self.lander.update(0, 0, 0)
        self.ui.update(dt, self.elapsed_time)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.ui.draw(self.screen)
        self.terrain.draw(self.screen)
        self.lander.draw(self.screen)
        pygame.display.flip()

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            # Si saisi d'un nouvel input, recalcule le path
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     input = event.pos
            #     self.path_mng.update(input)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("In path edit mode")
                    self.path_edit_loop()
                if event.key == pygame.K_r:
                    print("In game loop mode")
                    self.prepare()
                    self.draw()
                    self.game_loop()
            # print(event)


with open("../game_data.json") as json_data:
    dict = json.load(json_data)
data = dict.get("1")
game = GameEngine(lander_init_values=data.get("lander"), terrain_topology=data.get("topo"))

game.start()
pygame.quit()
sys.exit()
