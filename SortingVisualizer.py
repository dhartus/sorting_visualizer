import pygame
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Sort Visualizer")
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

#  Colours
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

    def final(self):
        self.colour = PURPLE

    def checking(self):
        self.colour = RED

    def sorted(self):
        self.colour = GREEN

    def checked(self):
        self.colour = TURQUOISE


def insertionsort(win, bars: Bar):
    for i in range(1, len(bars)):
        j = i
        while j > 0:

            bars[j].checking()
            bars[j-1].checking()
            draw_bars(win, bars)

            if bars[j].height < bars[j-1].height:
                bars[j].height, bars[j-1].height = bars[j-1].height, bars[j].height

                bars[j].sorted()
                bars[j-1].sorted()
                draw_bars(win, bars)
                j -= 1

            else:
                bars[j].sorted()
                bars[j-1].sorted()
                draw_bars(win,bars)
                break

        #  If i == len(bars)-1 , all bars have been sorted , change color of all bars to final color.
        if i == len(bars)-1:
            j = i
            while j >= 0:
                bars[j].final()
                draw_bars(win, bars)
                j -= 1


def bubblesort(win, bars:Bar):
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

        bars[len(bars) - 1 - i].final()
        draw_bars(win, bars)

def mergesort(win, array):
    helper = []
    for bar in array:
        helper.append(bar.height)
    mergesorthelper(array, helper, 0, len(array)-1, win)
    return


def mergesorthelper(array, helper, startIdx, endIdx, win):
    if startIdx == endIdx:
        return

    mid = (startIdx + endIdx) // 2

    mergesorthelper(array, helper, startIdx, mid, win)
    mergesorthelper(array, helper, mid + 1, endIdx, win)
    doMerge(array, helper, startIdx, mid, endIdx, win)


def doMerge(array, helper, startIdx, mid, endIdx, win):

    for i in range(startIdx, endIdx + 1):
        helper[i] = array[i].height

    leftpointer = startIdx
    rightpointer = mid + 1

    current = startIdx
    array[leftpointer].checking()
    array[rightpointer].checking()
    draw_bars(win, array)
    while leftpointer <= mid and rightpointer <= endIdx:

        if helper[leftpointer] <= helper[rightpointer]:
            array[current].height = helper[leftpointer]
            array[current].final() if (startIdx == 0 and endIdx == len(array)-1) else array[current].sorted()
            draw_bars(win, array)
            leftpointer += 1
        else:
            array[current].height = helper[rightpointer]
            array[current].final() if (startIdx == 0 and endIdx == len(array)-1) else array[current].sorted()
            draw_bars(win, array)
            rightpointer += 1

        current += 1

    while leftpointer <= mid:
        array[current].height = helper[leftpointer]
        array[current].final() if (startIdx == 0 and endIdx == len(array)-1) else array[current].sorted()
        draw_bars(win, array)
        leftpointer += 1
        current += 1

    while rightpointer <= endIdx:
        array[current].height = helper[rightpointer]
        array[current].final() if (startIdx == 0 and endIdx == len(array)-1) else array[current].sorted()
        draw_bars(win, array)
        rightpointer += 1
        current += 1

def draw_bars(win, bars, *args):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            global ANIMATIONSPEED
            if event.key == pygame.K_UP:
                ANIMATIONSPEED += 50
                print(ANIMATIONSPEED)

            if event.key == pygame.K_DOWN:
                if ANIMATIONSPEED - 50 >=0:
                    ANIMATIONSPEED -= 50
                print(ANIMATIONSPEED)

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
    sorting_algorithm = None
    sorted = False
    while True:

        draw_bars(win, bars, True)  # Draw random generated bars onto the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    sorting_algorithm = "bubblesort"
                if event.key == pygame.K_i:
                    sorting_algorithm = "insertionsort"
                if event.key == pygame.K_m:
                    print("m")
                    sorting_algorithm = "mergesort"

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # Left or Right mouse click
                bars = generateRandomBars()  # Generate new Random bars
                sorted = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not sorted:  # If Space key is pressed
                    if sorting_algorithm is not None:
                        if sorting_algorithm == "bubblesort":
                            bubblesort(win, bars)
                        elif sorting_algorithm == "insertionsort":
                            insertionsort(win, bars)
                        elif sorting_algorithm == "mergesort":
                            mergesort(win, bars)
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
