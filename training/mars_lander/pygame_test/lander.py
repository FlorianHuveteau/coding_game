import pygame
import math


class Lander(pygame.sprite.Sprite):

    def __init__(self,init_values):
        pygame.sprite.Sprite.__init__(self)
        self.init_values = init_values
        self.restart()

        try:
            img = pygame.image.load("../lander.png")
            self.img = img.convert()
            self.rect = self.img.get_rect()
        except pygame.error:
            print("oups, y a pas l'image du vaisseau")
            raise SystemExit

    def update(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation

    def draw(self, screen):
        # screen.blit(self.img, (self.x // 10, self.y // 10))
        pass

    def restart(self):
        self.x = self.init_values.get("x", 0)
        self.y = 3000 - int(self.init_values.get("y", 0))
        self.rotation = self.init_values.get("rotation", 0)
