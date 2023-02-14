import pygame
import math
import random
import tkinter
from tkinter import messagebox


class cube(object):
    width = 1000
    rows = 20

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False, score=False):
        dis = self.width // self.rows
        r = self.pos[0]
        c = self.pos[1]

        pygame.draw.rect(surface, self.color, (r * dis + 1, c * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 5
            circleMiddle = (r * dis + centre - radius, c * dis + 20)
            circleMiddle2 = (r * dis + dis - radius * 2, c * dis + 20)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


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
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


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
    global rows, width, s , snack
    BLACK = (0, 0, 0)
    surface.fill(BLACK)  # fill the window with black
    drawGrid(width, rows, surface)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()  # update the screen


def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


if __name__ == '__main__':
    global width, rows, s , snack
    width = 1000  # width of the screen
    rows = 20  # number of rows to split the screen
    pygame.init()
    window = pygame.display.set_mode((width, width))  # square screen
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    s = snake(RED, (10, 10))  # snake color and position
    snack = cube(randomSnack(rows, s), color=GREEN)
    running = True

    clock = pygame.time.Clock()  # to control the speed of the game

    while running:
        pygame.time.delay(50)  # delay in milliseconds
        clock.tick(10)  # 10 frames per second
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=GREEN)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                #message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(window)
        for event in pygame.event.get():  # check if game not crashed. window will not show without this loop
            if event.type == pygame.QUIT:
                pygame.quit()
