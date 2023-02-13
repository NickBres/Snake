import pygame
import math
import random
import tkinter
from tkinter import messagebox


class cube(object):
    rows = 0
    width = 0

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        pass

    def move(self, dirnx, dirny):
        pass

    def draw(self, surface, eyes=False):
        pass


class snake(object):
    body = []  # list of cubes
    turns = {}  # dictionary of positions to turn the body

    def __init__(self, color, pos):
        self.color = color  # snake color
        self.head = cube(pos)  # snake head
        self.body.append(self.head)  # add the head to the body
        self.dirnx = 0  # direction of the snake
        self.dirny = 1  # down

    def move(self):
        for event in pygame.event.get():  # get all the events
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()  # get all the keys pressed
            for key in keys:  # check if any key is pressed
                if keys[pygame.K_LEFT]:
                    self.setDir(-1, 0)  # set the direction of the snake to left
                elif keys[pygame.K_RIGHT]:
                    self.setDir(1, 0)  # set the direction of the snake to right
                elif keys[pygame.K_UP]:
                    self.setDir(0, -1)  # set the direction of the snake to up
                elif keys[pygame.K_DOWN]:
                    self.setDir(0, 1)  # set the direction of the snake to down

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])  # move the cube to the direction of the turn
                if i == len(self.body) - 1:
                    self.turns.pop(p)  # remove the turn from the dictionary
            else:  # screen edges collision
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])  # move the cube to the other side of the screen
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def setDir(self, x, y):
        self.dirnx = x
        self.dirny = y
        self.turns[self.head.pos[:]] = [s.dirnx, self.dirny]  # add the position of the head to the turns dictionary

    def reset(self, pos):
        pass

    def addCube(self):
        pass

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(width, rows, surface):
    gapSize = width // rows  # gap between each line

    x = 0
    y = 0
    for i in range(rows):
        x = x + gapSize
        y = y + gapSize

        pygame.draw.line(surface, (255, 255, 255), (x, 0),
                         (x, width))  # draw on the screen while line on x horizontally
        pygame.draw.line(surface, (255, 255, 255), (0, y),
                         (width, y))  # draw on the screen while line on y vertically


def redrawWindow(surface):
    global rows, width
    surface.fill((0, 0, 0))  # fill the screen with black
    drawGrid(width, rows, surface)
    pygame.display.update()  # update the screen


def randomSnack(rows, item):
    pass


def message_box(subject, content):
    pass


if __name__ == '__main__':
    global width, rows
    width = 1000  # width of the screen
    rows = 20  # number of rows to split the screen
    pygame.init()
    window = pygame.display.set_mode((width, width))  # square screen
    RED = (255, 0, 0)
    s = snake(RED, (10, 10))  # snake color and position
    running = True

    clock = pygame.time.Clock()  # to control the speed of the game

    while running:
        pygame.time.delay(50)  # delay in milliseconds
        clock.tick(10)  # 10 frames per second
        redrawWindow(window)

