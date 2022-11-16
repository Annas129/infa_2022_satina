import math
from random import randrange as rnd,choice
from random import randint
import datetime
import time

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x > 780:                         #отскок от стены
            self.vx = -self.vx / 2
            self.x = 779

        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99

        else:
            if self.vx ** 2 + self.vy ** 2 > 10:                #отскок от пола, исключающий случай покоя
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499

            if self.live <= 0:
                balls.pop(balls.index(self))
            else:
                self.live -= 1


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, ob):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if type(ob) == Target:
            if abs(ob.x - self.x) <= (self.r + ob.r) and abs(ob.y - self.y) <= (self.r + ob.r):
                return True
            else:
                return False
        if type(ob) == Bomba:
            if abs(ob.x - self.x) <= (self.r + ob.a) and abs(ob.y - self.y) <= (self.r + ob.a):
                return True
            else:
                return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = 450
        self.z = 50
        self.d = 420
        self.vx = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.x = self.x
        new_ball.y = self.y
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if ((event.pos[0]-20) !=0):
                self.an = math.atan((-450 + event.pos[1]) / (event.pos[0]-20))
            self.z = -60 * math.cos(self.an) + self.x
            self.d = 60 * math.sin(self.an) + self.y
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.x, self.y), (self.z, self.d), width=7)
        pygame.draw.rect(self.screen, GREY, (self.x - 30, self.y, 50, 30))
        pygame.draw.circle(self.screen, GREY,
                           (self.x + 10, self.y + 37), 10)
        pygame.draw.circle(self.screen, GREY,
                           (self.x - 18, self.y + 37), 10)

    def move(self):
        self.x += self.vx
        self.z = 60 * math.cos(self.an) + self.x
        self.d = 60 * math.sin(self.an) + self.y





    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.vy = -1
        self.new_target()

    def move(self):
        self.y-=self.vy
        if self.y + self.r > 550 or self.y - self.r < 0:
            self.vy *= -1

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 750)
        y = self.y = rnd(300, 500)
        r = self.r = rnd(5, 50)
        self.live = 1
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

class Bomba:
    def __init__(self):
        self.x = 0
        self.y = 30
        self.points = 0
        self.live = 1
        self.screen = screen
        self.vy = -3
        self.a = 30
        self.new_target()

    def move(self):
        self.y-=self.vy
        if self.y + self.a > 540:
            self.new_target()

    def popa(self):
        if abs(gun.x - self.x) <= (self.a + 25) and abs(gun.y - self.y) <= (0.5*self.a + 15):
            return True
        else:
            return False

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = gun.x
        self.y = 30
        self.a = 30
        self.live = 1
        self.color = GAME_COLORS[randint(0, 5)]

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += 0.5*points

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.a, self.a))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []


clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
bomb = Bomba()
finished = False

#текст на экране
font = pygame.font.SysFont('comicsansms', 30)
str2 = font.render("Очки:", 1, RED)
str3 = font.render("Вы проиграли,в вас попала бомба!", 1, GREY)
str4 = font.render("Попадание", 1, GREY)

while not finished:
    target2.move()
    target1.move()
    bomb.move()
    gun.move()
    screen.fill(WHITE)
    gun.draw()
    str1 = font.render(str(target1.points + target2.points + bomb.points), 1, RED)
    screen.blit(str2, (0, 0))
    screen.blit(str1, (100, 0))
    target1.draw()
    target2.draw()
    bomb.draw()
    if bomb.popa():
        screen.blit(str3, (180, 200))
        pygame.display.update()
        time.sleep(1)
        finished = True
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            gun.vx = 10
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            gun.vx = -10
        else:
            gun.vx = 0

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
        if b.hittest(bomb) and bomb.live:
            bomb.live = 0
            bomb.hit()
            bomb.new_target()
            time.sleep(0.08)
            balls.pop(balls.index(b))
    gun.power_up()
print(target1.points + target2.points + bomb.points)
pygame.quit()
