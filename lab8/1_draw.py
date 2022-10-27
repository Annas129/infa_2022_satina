import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
color = (169, 169, 169)
screen.fill(color)

circle(screen, (255, 255, 0), (200, 175), 100)      #голова
circle(screen, (0, 0, 0), (200, 175), 100, 1)

circle(screen, (255, 0, 0), (150, 150), 20)    #глаза
circle(screen, (255, 0, 0), (250, 150), 15)
circle(screen, (0, 0, 0), (150, 150), 8)
circle(screen, (0, 0, 0), (250, 150), 8)
circle(screen, (0, 0, 0), (250, 150), 15, 1)
circle(screen, (0, 0, 0), (150, 150), 20, 1)

rect(screen, (0, 0, 0), (150, 210, 100, 20))       #рот

line(screen, (0,0,0), (120, 110), (180, 130), 10)      #брови
line(screen, (0,0,0), (220, 140), (280, 100), 10)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
