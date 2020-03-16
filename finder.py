import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 12
HEIGHT = 12

# This sets the margin between each cell
MARGIN = 1

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(50):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(50):
        grid[row].append(0)  # Append a cell


def heuristic(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)


# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [651, 651]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Finder")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        #Drawing with left click
        if pygame.mouse.get_pressed()[0]:
            # User clicks the mouse. Get the position
            try:
                pos = event.pos
                # Change the x/y screen coordinates to grid coordinates pjyf
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 1
                print("Click ", pos, "Grid coordinates: ", row, column)
            except AttributeError:
                pass
        #Erasing with rightclick
        if pygame.mouse.get_pressed()[2]:
            # User clicks the mouse. Get the position
            try:
                pos = event.pos
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 0
                print("Click ", pos, "Grid coordinates: ", row, column)
            except AttributeError:
                pass



    # Set the screen background
    screen.fill(WHITE)

    # Draw the grid
    for row in range(50):
        for column in range(50):
            color = BLACK
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()



class Node:
    def __init__(self,parent = None,position = None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.postion == other.position


def aStar(grid,start,end):

    open = []
    closed = []

    startNode = Node(None,start)
    endNode = Node(None,end)

    open.append(startNode)










