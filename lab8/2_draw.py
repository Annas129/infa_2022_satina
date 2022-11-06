import pygame
from random import randint
from PIL import Image, ImageDraw

pygame.init()
window = pygame.display.set_mode((1200, 700))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
sum = 0


class Circle():
    def __init__(self):
        self.x = randint(100, 1100)
        self.y = randint(100, 600)
        self.radius = randint(10, 100)
        self.vel_x = 1
        self.vel_y = 1
        self.color = COLORS[randint(0, 5)]

class Rectangle():
    def __init__(self):
        self.x = randint(100, 1100)
        self.y = randint(100, 600)
        self.a = randint(10, 100)
        self.b = randint(10, 100)
        self.vel_y = 1
        self.color = COLORS[randint(0, 5)]
    def rotate(self, angle):
        self.rect = pygame.transform.rotate(self.rect, angle)

def click(event):
    '''Добавляет к сумме попаданий 1, если пользователь попал в шарик '''
    event.x, event.y = event.pos
    global sum
    if ((((event.x - ball1.x)**2 + (event.y - ball1.y)**2) < ball1.radius**2) or (((event.x - ball2.x)**2 + (event.y - ball2.y)**2) < ball2.radius**2)):
        sum+=1
    if (event.x - rec.x) < rec.a and (event.y - rec.y) < rec.b:
        sum+=2

print('За попадание в шар дается одно очко, за попадание в прямоугольник - два очка. Чтобы начать игру. нажмите пробел')
ball1 = Circle()
ball2 = Circle()
rec = Rectangle()

run = True
start = False
clock = pygame.time.Clock()

while run:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        start = True

    bounds = window.get_rect()
    if start:
        ball1.y -= ball1.vel_y
        ball1.x += ball1.vel_x
        ball2.y -= ball2.vel_y
        ball2.x += ball2.vel_x
        rec.y += rec.vel_y

        if ball1.x - ball1.radius < bounds.left or ball1.x + ball1.radius > bounds.right:
            ball1.vel_x *= -1
        if ball1.y - ball1.radius < bounds.top or ball1.y + ball1.radius > bounds.bottom:
            ball1.vel_y *= -1

        if ball2.x - ball2.radius < bounds.left or ball2.x + ball2.radius > bounds.right:
            ball2.vel_x *= -1
        if ball2.y - ball2.radius < bounds.top or ball2.y + ball2.radius > bounds.bottom:
            ball2.vel_y *= -1

        if rec.y - rec.b < bounds.top or rec.y + rec.b > bounds.bottom:
            rec.vel_y *= -1

    window.fill((0,0,0))
    pygame.draw.rect(window, (255, 0, 0), bounds, 1)
    pygame.draw.circle(window, ball1.color, (ball1.x, ball1.y), ball1.radius)
    pygame.draw.circle(window, ball2.color, (ball2.x, ball2.y), ball2.radius)
    pygame.draw.rect(window, rec.color, (rec.x, rec.y, rec.a, rec.b))
    pygame.display.update()

print("Вы набрали ", sum, " очка(ов)")

pygame.quit()
