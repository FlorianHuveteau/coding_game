import pygame


class Terrain():

    def __init__(self, topo):
        self.topo = []
        for e in topo:
            x =int(e[0] /10)
            y = 300- int(e[1]/10)
            self.topo.append((x,y))
        print("Terrain x/y coordinates: ", self.topo)

    def draw(self, surface):
        color = (255, 255, 255)
        pygame.draw.lines(surface, color, False, self.topo, 2)
