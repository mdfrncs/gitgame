# 1 - Import library
import pygame
import time
from pygame.locals import *

from objects import Player
from objects import Projectile

# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


# 3 - Create objects
class World:

    def __init__(self):
        self.player = Player(width, height)
        self.count = 100
        self.projectiles = []

    def update_objects(self):
        self.player.update_position()

        if self.count == 0:
            self.projectiles.append(Projectile())
            self.count = 100

        self.count -= 1

        to_remove = []
        for bullet in self.projectiles:
            if not bullet.update_position():
                to_remove.append(bullet)

        for bullet in to_remove:
            self.projectiles.remove(bullet)


    def update_health(self):
        to_remove = []
        player_rect = self.player.rect
        for bullet in self.projectiles:
            if bullet.hit(player_rect):
                print "I'm Hit!"
                to_remove.append(bullet)

        for bullet in to_remove:
            self.projectiles.remove(bullet)

    def draw_objects(self):
        # 5 - clear the screen before drawing it again
        screen.fill(0)

        # 6 - Re-draw all game elements
        self.player.blit(screen)

        for bullet in self.projectiles:
            bullet.blit(screen)

        # 7 - update the screen
        pygame.display.flip()

    def process_event(self, event):
        self.player.process_event(event)
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)


world = World()

# main loop
while 1:
    time.sleep(0.01)
    world.update_objects()
    world.draw_objects()
    world.update_health()
    for event in pygame.event.get():
        world.process_event(event)
