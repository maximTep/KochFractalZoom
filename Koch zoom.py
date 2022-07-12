import pygame
import math
from colour import Color
import copy
import random

pygame.init()
screenWidth = 1280
screenHeight = 1024
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Fractal")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

red = Color('red')
colorRange = list(red.range_to(Color(color='purple'), 19))
colorArray = copy.deepcopy(colorRange)


def visible_lines(lines_: list, scale_, scale_shift_W_, scale_shift_H_):
    it = 0
    expander = 0
    LB = -expander
    RB = screenWidth + expander
    UB = -expander
    DB = screenHeight + expander
    while it < len(lines_):
        line_ = [lines_[it][0], lines_[it][1]]
        line_[0] = [line_[0][0] * scale_ - scale_shift_W, line_[0][1] * scale_ - scale_shift_H]
        line_[1] = [line_[1][0] * scale_ - scale_shift_W, line_[1][1] * scale_ - scale_shift_H]
        if line_[0][0] < LB or line_[0][0] > RB or line_[0][1] < UB or line_[0][1] > DB:
            if line_[1][0] < LB or line_[1][0] > RB or line_[1][1] < UB or line_[1][1] > DB:
                lines_.pop(it)
                continue
        it += 1

    return lines_


# def getRandColor():
#     global colorArray
#     if len(colorArray) == 0:
#         colorArray = copy.deepcopy(colorRange)
#         r = random.randint(0, len(colorArray)-1)
#         color = [colorArray[r].get_red()*255, colorArray[r].get_green()*255, colorArray[r].get_blue()*255]
#         colorArray.pop(r)
#     else:
#         r = random.randint(0, len(colorArray) - 1)
#         color = [colorArray[r].get_red() * 255, colorArray[r].get_green() * 255, colorArray[r].get_blue() * 255]
#         colorArray.pop(r)
#
#     return color


def getRandColor():
    color = random.choice([RED, GREEN, BLUE])
    return color


def line_len(line_: list):
    p1 = line_[0]
    p2 = line_[1]
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


def line_to_fract(p1: list, p2: list):
    newLines = []
    x = (p2[0]-p1[0])/3
    y = (p2[1]-p1[1])/3

    vec = [x, y]
    angle = 3.1415/3

    cs = math.cos(-angle)
    sn = math.sin(-angle)
    rx = x * cs - y * sn
    ry = x * sn + y * cs

    upVec = [rx, ry]



    cs = math.cos(angle)
    sn = math.sin(angle)
    rx = x * cs - y * sn
    ry = x * sn + y * cs

    downVec = [rx, ry]


    start = p1
    end = [start[0] + vec[0], start[1] + vec[1]]
    newLines.append([start, end])

    start = end
    end = [start[0] + upVec[0], start[1] + upVec[1]]
    newLines.append([start, end])

    start = end
    end = [start[0] + downVec[0], start[1] + downVec[1]]
    newLines.append([start, end])

    start = end
    end = [start[0] + vec[0], start[1] + vec[1]]
    newLines.append([start, end])



    for line in newLines:
        pygame.draw.line(screen, getRandColor(), line[0], line[1], width=1)

    return newLines


p1 = [400, 275]
p2 = [screenWidth - 400, 275]
p3 = [screenWidth - 400, 275+480]
p4 = [400, 275+480]

lines = [[p1, p2],
         [p2, p3],
         [p3, p4],
         [p4, p1]]

for ln in lines:
    pygame.draw.line(screen, getRandColor(), ln[0], ln[1])
pygame.display.update()




clock = pygame.time.Clock()
time = pygame.time.get_ticks()
max_iterations = 6
iterations = 0
scale = 1
scale_speed = 0.04
scale_acceleration = 1
running = True
while running:
    scale *= scale_speed + 1
    scale_shift_W = (scale - 1) * 400  # (scale-1) * screenWidth / 2
    scale_shift_H = (scale - 1) * 275 # (scale - 1) * 136.3 # (scale-1) * screenHeight / 2
    screen.fill(BLACK)
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if line_len(lines[len(lines)//2]) * scale > 10:          # not Done:
        time = pygame.time.get_ticks()
        iterations += 1

        lines = visible_lines(lines, scale, scale_shift_W, scale_shift_H)
        newLines = []
        for ind, line in enumerate(lines):
            if line[0][1] < screenHeight // 2 and line[1][1] < screenHeight // 2:
                for fractLine in line_to_fract(line[0], line[1]):
                    newLines.append(fractLine)
            else:
                newLines.append(line)


        lines = newLines

        for i in lines:
            pygame.draw.line(screen,
                               getRandColor(),
                               [i[0][0] * scale - scale_shift_W, i[0][1] * scale - scale_shift_H],
                               [i[1][0] * scale - scale_shift_W, i[1][1] * scale - scale_shift_H])

    else:
        for i in lines:
            pygame.draw.line(screen,
                               getRandColor(),
                               [i[0][0] * scale - scale_shift_W, i[0][1] * scale - scale_shift_H],
                               [i[1][0] * scale - scale_shift_W, i[1][1] * scale - scale_shift_H])



    pygame.display.update()


