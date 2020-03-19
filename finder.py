import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
SMTH = (100,0,100)
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

# for i in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (6, 7), (7, 8), (7, 9), (8, 10), (8, 11), (9, 12), (9, 13), (9, 14), (10, 15)]:
#     grid[i[0]][i[1]] = 1


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

start_test = (1,1)
end_test = (20,20)

# Draw the grid
def draw(grid):
    for row in range(50):
        for column in range(50):
            color = BLACK
            if grid[row][column] == 1:
                color = WHITE
            elif grid[row][column] == 2:
                color = BLUE
            elif grid[row][column] == 3:
                color = RED
            elif grid[row][column] == 4:
                color = GREEN
            elif grid[row][column] == 5:
                color = SMTH
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

class Node:
    def __init__(self,parent = None,position = None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0




def aStar(grid,start,end):

    open = []
    closed = []

    startNode = Node(None,start)
    startNode.f,startNode.h,startNode.g = 0,0,0
    endNode = Node(None,end)
    endNode.f,endNode.h,endNode.g = 0,0,0

    open.append(startNode)

    children_vectors = ((-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0))

    while len(open) > 0:

        draw(grid)
        pygame.display.flip()
        print("OPEN-------->",len(open))
        print(len(closed))

        for i in open:
            if i.position is not None:
                if grid[i.position[0]][i.position[1]] == 4:
                    grid[i.position[0]][i.position[1]] = 5
                else:
                    grid[i.position[0]][i.position[1]] = 4

        for i in closed:
            if i.position is not None:
                # if grid[i.position[0]][i.position[1]] == 3:
                #     grid[i.position[0]][i.position[1]] = 5
                # else:
                    grid[i.position[0]][i.position[1]] = 3

        current_node = open[0]
        current_index = 0

        #finding node with best f value
        for index,item in enumerate(open):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        #remove best node from open and add to closed list
        open.pop(current_index)
        closed.append(current_node)

        if current_node.position == endNode.position:
            path = []
            current = current_node
            while current.parent != None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for j in children_vectors:
            if (current_node.position[0]+j[0]) >= 0 and (current_node.position[0]+j[0]) < 50 and (current_node.position[1]+j[1]) >= 0 and (current_node.position[1]+j[1]) < 50:
                if grid[current_node.position[0]+j[0]][current_node.position[1]+j[1]] != 1 and Node(current_node,(current_node.position[0]+j[0],current_node.position[1]+j[1])) not in closed:
                    children.append(Node(current_node,(current_node.position[0]+j[0],current_node.position[1]+j[1])))
                    if (j[0]**2 + j[1]**2)>1:
                        children[-1].g = children[-1].parent.g + math.sqrt(2)
                    else:
                        children[-1].g = children[-1].parent.g + 1
                    children[-1].h = math.sqrt((children[-1].position[0]-endNode.position[0])**2 + (children[-1].position[1]-endNode.position[1])**2)
                    children[-1].f = children[-1].h + children[-1].g

                    flag = False
                    for open_item in open:
                        if children[-1] == open_item:
                            flag = True
                    if flag == False:
                        open.append(children[-1])



while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("POSZLO")
                path = aStar(grid,start_test,end_test)
                for i in path:
                    grid[i[0]][i[1]] = 2
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

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


    draw(grid)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()





















