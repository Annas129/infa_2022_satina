import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

x1 = randint(100, 1100)
y1 = randint(100, 900)
r1 = randint(10, 100)
x2 = randint(100, 1100)
y2 = randint(100, 900)
r2 = randint(10, 100)
sum = 0

def new_ball():
    '''рисует заданное количество(до 2-х) новых шариков '''
    global x1, y1, r1
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x1, y1), r1)
    global x2, y2, r2
    x2 = randint(100, 1100)
    y2 = randint(100, 900)
    r2 = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x2, y2), r2)

def click(event):
    '''Добавляет к сумме попаданий 1, если пользователь попал в шарик '''
    event.x, event.y = event.pos
    global sum
    if ((((event.x - x1)**2 + (event.y - y1)**2) < r1**2) or (((event.x - x2)**2 + (event.y - y2)**2) < r2**2)):
        sum+=1

def movement():
    dt = clock.tick(50) / 1000.0
    vx = 10
    vy = 10
    global x1, y1
    x1 += vx * dt
    y1 += vy * dt

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    movement()
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

print("Вы попали ", sum, " раз(а)")

pygame.quit()
