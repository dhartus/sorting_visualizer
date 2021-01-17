import pygame
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Bubble Sort Visualizer")
WIDTHOFBAR = 1 / 100 * WIDTH
xpos = (5 / 100) * WIDTH
ypos = (5 / 100) * WIDTH
MINHEIGHTOFBAR = 1
MAXHEIGHTOFBAR = WIDTH - 6*ypos
ANIMATIONSPEED = 10
TEXT1 = "Press SPACE to Start Sorting"
TEXT2 = "Generate New Array - Left or Right Mouse Click"
TEXT3 = "Control Animation Speed - UP or Down Key"
TEXT4 = "Control Number Of Bars - Left or Right Arrow Keys"
TEXT_SIZE = int(4/100 * WIDTH)
TEXT_GAP = TEXT_SIZE
TEXT1_YPOS = MAXHEIGHTOFBAR + ypos + TEXT_GAP
TEXT2_YPOS = TEXT1_YPOS + TEXT_GAP
TEXT3_YPOS = TEXT2_YPOS + TEXT_GAP
TEXT4_YPOS = TEXT3_YPOS + TEXT_GAP



# Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Bar:

    def __init__(self, displaywidth, colour, xpos, ypos, width, height):
        self.displaywidth = displaywidth
        self.colour = colour
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    def issorted(self):
        self.colour = PURPLE

    def checking(self):
        self.colour = RED

    def checked(self):
        self.colour = TURQUOISE


def bubblesort(win, bars):
    for i in range(len(bars)):
        for j in range(0, len(bars) - 1 - i):

            firstbar = bars[j]
            secondbar = bars[j + 1]

            firstbar.checking()
            secondbar.checking()

            draw_bars(win, bars)

            if firstbar.height > secondbar.height:
                firstbar.height, secondbar.height = secondbar.height, firstbar.height
                firstbar.colour = GREEN
                secondbar.colour = GREEN
                draw_bars(win, bars)

            firstbar.checked()
            secondbar.checked()
            draw_bars(win, bars)

        bars[len(bars) - 1 - i].issorted()
        draw_bars(win, bars)


def draw_bars(win, bars, *args):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            global ANIMATIONSPEED
            if event.key == pygame.K_UP:
                ANIMATIONSPEED += 50

            if event.key == pygame.K_DOWN:
                ANIMATIONSPEED -= 50

    win.fill(WHITE)
    for bar in bars:
        pygame.draw.rect(win, bar.colour, (bar.xpos, bar.ypos, bar.width, bar.height))
    draw_text(win)
    pygame.display.flip()  # pushes the drawn surface to the display

    firststart = args  # If first run , no need to give delay
    if firststart:
        return

    pygame.time.wait(ANIMATIONSPEED)


def generateRandomBars():
    gap = WIDTHOFBAR
    start = xpos
    bars = []
    while start + WIDTHOFBAR < WIDTH - xpos:
        height = random.randint(MINHEIGHTOFBAR, MAXHEIGHTOFBAR)
        bar = Bar(WIDTH, TURQUOISE, start, ypos, WIDTHOFBAR, height)
        start += WIDTHOFBAR + gap
        bars.append(bar)
    return bars


def draw_text(win):
    # font = pygame.font.Font("OliviaRegular.ttf", TEXT_SIZE)
    font = pygame.font.Font("AlohaSummer.ttf", TEXT_SIZE)
    text1 = font.render(TEXT1, True, BLACK)
    text2 = font.render(TEXT2, True, BLACK)
    text3 = font.render(TEXT3, True, BLACK)
    text4 = font.render(TEXT4, True, BLACK)
    win.blit(text1, (WIDTH // 2 - text1.get_width() // 2, TEXT1_YPOS))
    win.blit(text2, (WIDTH // 2 - text2.get_width() // 2, TEXT2_YPOS))
    win.blit(text3, (WIDTH // 2 - text3.get_width() // 2, TEXT3_YPOS))
    win.blit(text4, (WIDTH // 2 - text4.get_width() // 2, TEXT4_YPOS))


def main(win):
    pygame.init()
    bars = generateRandomBars()

    sorted = False
    while True:

        draw_bars(win, bars, True)  # Draw random generated bars onto the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # Left or Right mouse click
                bars = generateRandomBars()  # Generate new Random bars
                sorted = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not sorted:  # If Space key is pressed
                    bubblesort(win, bars)  # Sort the bars
                    sorted = True

            if event.type == pygame.KEYDOWN:
                global WIDTHOFBAR
                if event.key == pygame.K_LEFT:  # If Left Key is pressed
                    if WIDTHOFBAR > 1:
                        WIDTHOFBAR -= 1
                        bars = generateRandomBars()
                        sorted = False

                if event.key == pygame.K_RIGHT:  # If Right Key is pressed
                    if WIDTHOFBAR < WIDTH:
                        WIDTHOFBAR += 5
                        bars = generateRandomBars()
                        sorted = False



main(WIN)
