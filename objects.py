import pygame
import math

SPEED = 2

PROJECTILE = pygame.image.load("resources/images/fire.png")

def rotate(pos, theta):
    x = pos[0]
    y = pos[1]
    return [(x * math.cos(theta)) - (y * math.sin(theta)), (x * math.sin(theta)) + (y * math.cos(theta))]

def add_points(a, b):
    return [a[0] + b[0], a[1] + b[1]]

class Player:
    resource = "resources/images/player.png"

    # WASD keys
    movement_keys = [False, False, False, False]

    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.image = pygame.image.load(self.resource)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.pos = [100, 100]
        self.rect = self.image.get_rect()

    def blit(self, screen):
        position = pygame.mouse.get_pos()
        angle = 4.71239 - math.atan2(position[1] - self.pos[1], position[0] - self.pos[0])
        rotated_player = pygame.transform.rotate(self.image, math.degrees(angle))

        rotated_pos = self.draw_pos(angle)
        screen.blit(rotated_player, rotated_pos)

        self.rect.top = rotated_pos[1]
        self.rect.left = rotated_pos[0]

    def draw_pos(self, theta):
        w = self.width / 2
        h = self.height / 2

        bounds = [rotate([-w, -h], theta),
                  rotate([-w, h], theta),
                  rotate([w, -h], theta),
                  rotate([w, h], theta)]

        min_x = bounds[0][0]
        min_y = bounds[1][0]

        for pos in bounds:
            if pos[0] < min_x:
                min_x = pos[0]
            if pos[1] < min_y:
                min_y = pos[1]

        return [min_x + self.pos[0], min_y + self.pos[1]]


    def process_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            value = event.type == pygame.KEYDOWN
            index = self.get_key_index(event.key)
            if index != -1:
                self.movement_keys[index] = value

    def update_position(self):
        if self.movement_keys[0]:
            self.pos[1] -= SPEED
        if self.movement_keys[1]:
            self.pos[0] -= SPEED
        if self.movement_keys[2]:
            self.pos[1] += SPEED
        if self.movement_keys[3]:
            self.pos[0] += SPEED

        if self.pos[0] <= 0:
            self.pos[0] = 0
        elif self.pos[0] > self.x_max:
            self.pos[0] = self.x_max
        if self.pos[1] <= 0:
            self.pos[1] = 0
        elif self.pos[1] > self.y_max:
            self.pos[1] = self.y_max



    def get_key_index(self, key):
        if key == pygame.K_w:
            return 0
        elif key == pygame.K_a:
            return 1
        elif key == pygame.K_s:
            return 2
        elif key == pygame.K_d:
            return 3
        else:
            return -1


class Projectile:
    def __init__(self):
        self.pos = [640, 240]
        self.update = rotate([-2, 0], 0)

    def update_position(self):
        self.pos = add_points(self.pos, self.update)

        return self.pos[0] > 0 and self.pos[1] > 0

    def blit(self, screen):
        screen.blit(PROJECTILE, self.pos)

    def hit(self, player_rect):
        rect = pygame.Rect(PROJECTILE.get_rect())
        rect.top = self.pos[1]
        rect.left = self.pos[0]

        return rect.colliderect(player_rect)
