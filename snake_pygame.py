import pygame, sys, os, time, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
snakeBody = [(0, 0), (20, 0)]
resolution = (800, 700)
length = width = 20
x, y = snakeBody[-1][0], 0
clock = pygame.time.Clock()
screen = pygame.display.get_surface()
window = pygame.display.set_mode((resolution[0], resolution[1] + 50))
fps = 5
background = (1, 50, 32)
danger = [(153, 0, 0), (255, 0, 0)]
body = (242, 170, 76)
strap = (246, 233, 109)
toggle = True
crashed = False
fx = snakeBody[-1][0] + 20
fy = snakeBody[-1][1]
food_colour = (242, 76, 146)
score = -1
bar = (254, 231, 21)
cb = (255, 255, 255)
tex = (0, 0, 0)

eat_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "food.wav"))
crash_sound= pygame.mixer.Sound(os.path.join(os.getcwd(), "crash.wav"))
temp = False


def c_sound():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()


def food():
    global fx, fy, score, fps
    global temp
    if (temp):
        pygame.mixer.Sound.play(eat_sound)
        pygame.mixer.music.stop()
    temp = True
    fx = random.randrange(0, resolution[0], 20)
    fy = random.randrange(0, resolution[1], 20)
    if (fx, fy) in snakeBody:
        food()
    pygame.draw.rect(screen, food_colour, (fx, fy, width, length))
    score += 1
    if fps < 20:
        fps += 0.2
    pygame.draw.line(screen, bar, (resolution[0] // 4, resolution[1] + 20), (resolution[0], resolution[1] + 20), 50)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(score), True, background, bar)
    tb = text.get_rect()
    tb.center = (resolution[0] // 2, resolution[1] + 20)
    screen.blit(text, tb)
    pygame.display.update()


def quit():
    pygame.quit()
    sys.exit()


def end(x, y, c=True):
    screen = pygame.display.get_surface()
    for i in range(1, 1200, 20):
        pygame.draw.circle(screen, cb, (x, y), i, 0)
        pygame.display.update()
        clock.tick(80)
    if c:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("You Crashed", True, tex, cb)
        tb = text.get_rect()
        tb.center = (resolution[0] // 2, resolution[1] // 2)
        screen.blit(text, tb)
        pygame.display.update()
        text = font.render(f"Score : {score} ", True, tex, cb)
        tb = text.get_rect()
        tb.center = (resolution[0] // 2, resolution[1] // 2 + 70)
        screen.blit(text, tb)
        pygame.display.update()
        text = font.render("press any key to exit", True, tex, cb)
        tb = text.get_rect()
        tb.center = (resolution[0] // 2, resolution[1] // 2 - 70)
        screen.blit(text, tb)
        pygame.display.update()
    while True:
        for i in pygame.event.get():
            if i.type == KEYDOWN or i.type == QUIT:
                quit()


def crash(a, b):
    global crashed
    crashed = True
    c_sound()
    screen = pygame.display.get_surface()
    global toggle
    if a < 0:
        a = 0
    elif a >= resolution[0]:
        a = resolution[0] - width - 10
    if b < 0:
        b = 0
    elif b >= resolution[1]:
        b = resolution[1] - width - 10
    for i in range(3):
        if toggle:
            toggle = False
            pygame.draw.rect(screen, danger[1], (a, b, width + 10, length + 10))
            pygame.display.update()
        else:
            toggle = True
            pygame.draw.rect(screen, danger[0], (a, b, width + 10, length + 10))
            time.sleep(0.15)
        pygame.display.update()
        clock.tick(3)


def draw(a, b, do):
    screen = pygame.display.get_surface()
    global toggle
    if do:
        if toggle:
            toggle = False
            pygame.draw.rect(screen, body, (a, b, width, length))
        else:
            toggle = True
            pygame.draw.rect(screen, strap, (a, b, width, length))
    else:
        pygame.draw.rect(screen, background, (a, b, width, length))


def body_update(update_axis, Magnitude):  # x axis , y axis , update_axis True-> update x False-> update y
    global snakeBody
    global x, y
    if update_axis:
        if Magnitude:
            x += width
        else:
            x -= width
    else:
        if Magnitude:
            y += width
        else:
            y -= width

    if (x, y) in snakeBody or x < 0 or y < 0 or y >= resolution[1] or x >= resolution[0]:
        crash(x, y)
        end(x, y)
    snakeBody.append((x, y))
    draw(x, y, True)
    if ((x, y) == (fx, fy)):
        food()
    else:
        a, b = snakeBody.pop(0)
        draw(a, b, False)


previous = pygame.K_RIGHT
oppkey = pygame.K_LEFT
map_dict = {pygame.K_RIGHT: [True, True], pygame.K_LEFT: [True, False], pygame.K_UP: [False, False],
            pygame.K_DOWN: [False, True]}
screen = pygame.display.get_surface()
screen.fill(background)
pygame.draw.line(screen, bar, (0, resolution[1] + 20), (resolution[0], resolution[1] + 20), 50)
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Score : ", True, background, bar)
tb = text.get_rect()
tb.center = (resolution[0] // 6, resolution[1] + 20)
screen.blit(text, tb)
pygame.display.update()
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(score), True, background, bar)
tb = text.get_rect()
tb.center = (resolution[0] // 2, resolution[1] + 20)
screen.blit(text, tb)

while not crashed:

    for i in pygame.event.get():
        if i.type == QUIT:
            quit()
        if i.type == pygame.KEYDOWN:
            if previous == i.key or oppkey == i.key:
                pass
            elif i.key == pygame.K_RIGHT:
                previous = i.key
                oppkey = pygame.K_LEFT
                body_update(True, True)
            elif i.key == pygame.K_LEFT:
                oppkey = pygame.K_RIGHT
                previous = i.key
                body_update(True, False)
            elif i.key == pygame.K_UP:
                oppkey = pygame.K_DOWN
                previous = i.key
                body_update(False, False)
            elif i.key == pygame.K_DOWN:
                oppkey = pygame.K_UP
                previous = i.key
                body_update(False, True)
    else:
        body_update(map_dict[previous][0], map_dict[previous][1])
        pygame.display.update()
        clock.tick(fps)
    body_update(map_dict[previous][0], map_dict[previous][1])
    pygame.display.update()
    clock.tick(fps)
