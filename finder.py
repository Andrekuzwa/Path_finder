import pygame
import math

from tkinter import *
from tkinter.ttk import *
# Define some colors


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
START_COLOR = (0,200,200)
END_COLOR = (255,165,0)
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

start_test = [None,None]
chosen_alg = 1
from tkinter import *
from tkinter.ttk import *
def setup():
    window = Tk()

    window.title("Finder Setup")

    window.geometry('250x200')

    lbl = Label(window, text="Set start point coordinates in range 0-49:")
    lbl.place(x=0,y=15)

    lbl2 = Label(window, text="Start point:")
    lbl2.place(x=0,y=40)

    lbl2x = Label(window, text="x:")
    lbl2x.place(x=80,y=40)
    lbl2y = Label(window, text="y:")
    lbl2y.place(x=130,y=40)

    x_ = Entry(window,width=3)
    x_.place(x=91,y=40)

    y_ = Entry(window,width=3)
    y_.place(x=141,y=40)


    lbl = Label(window, text="Choose algorithm:")
    lbl.place(x=0,y=70)

    var = IntVar()
    def get_alg():
        global chosen_alg
        chosen_alg = var.get()

    rad1 = Radiobutton(window, text='A* algorithm', variable=var, value=1, command=get_alg)
    rad1.place(x=0, y=90)
    rad2 = Radiobutton(window, text="Dijkstra's algorithm", variable=var, value=2, command=get_alg)
    rad2.place(x=0, y=110)

    def clicked():
        global start_test
        start_test[0]= int(x_.get())
        start_test[1] = int(y_.get())
        window.destroy()

    btn = Button(window, text="START",command = clicked)
    btn.place(x=150,y=145)

    window.mainloop()


setup()
if start_test[0] != None and start_test[1] != None:
    grid[start_test[0]][start_test[1]]= 5
start_test = tuple(start_test)


# Draw the grid

def get_end_nodes(grid):
    end_nodes=[]
    for row in range(50):
        for column in range(50):
            if grid[row][column] == 6:
                end_nodes.append((row,column))
    return end_nodes
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
                color = START_COLOR
            elif grid[row][column] == 6:
                color = END_COLOR
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
def erase(grid):
    for row in range(50):
        for column in range(50):
            if grid[row][column] != 5:
                grid[row][column] = 0
def erase_full(grid):
    for row in range(50):
        for column in range(50):
            grid[row][column] = 0

def clearRG(grid):
    for row in range(50):
        for column in range(50):
            if grid[row][column] != 5 and grid[row][column] != 6 and grid[row][column] != 1 and grid[row][column] != 2:
                grid[row][column] = 0

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
            if i.position is not None and grid[i.position[0]][i.position[1]]!=5 and grid[i.position[0]][i.position[1]]!=6:
                grid[i.position[0]][i.position[1]] = 4

        for i in closed:
            if i.position is not None and grid[i.position[0]][i.position[1]]!=5 and grid[i.position[0]][i.position[1]]!=6:
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
                        if children[-1].position == open_item.position and children[-1].g >= open_item.g:
                            flag = True
                    if flag == False:
                        open.append(children[-1])

class D_Node:
    def __init__(self,parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0

def dijskra(grid,start,end_positions):

    open = []
    closed = []

    startNode = D_Node(None,start)
    startNode.g = 0
    end_nodes = []
    for position in end_positions:
        end_nodes.append(D_Node(None,position))
        end_nodes[-1].g = 0

    open.append(startNode)

    children_vectors = ((-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))

    path_list = []

    while len(open)>0:

        draw(grid)
        pygame.display.flip()
        print("OPEN-------->", len(open))
        print(len(closed))

        for i in open:
            if i.position is not None and grid[i.position[0]][i.position[1]] != 5 and grid[i.position[0]][i.position[1]] != 6:
                grid[i.position[0]][i.position[1]] = 4

        for i in closed:
            if i.position is not None and grid[i.position[0]][i.position[1]] != 5 and grid[i.position[0]][i.position[1]] != 6:
                grid[i.position[0]][i.position[1]] = 3

        current_node = open[0]
        current_index = 0

        for index, item in enumerate(open):
            if item.g < current_node.g:
                current_node = item
                current_index = index

        open.pop(current_index)
        closed.append(current_node)



        if current_node.position in [end_node.position for end_node in end_nodes]:
            path = []
            current = current_node
            while current.parent != None:
                path.append(current.position)
                current = current.parent
            path_list.append(path[::-1])
            for index,node in enumerate(end_nodes):
                if node.position == current_node.position:
                    end_nodes.pop(index)

        if len(end_nodes) == 0:
            return path_list


        children = []
        for j in children_vectors:
            if (current_node.position[0] + j[0]) >= 0 and (current_node.position[0] + j[0]) < 50 and (
                    current_node.position[1] + j[1]) >= 0 and (current_node.position[1] + j[1]) < 50:
                if grid[current_node.position[0] + j[0]][current_node.position[1] + j[1]] != 1 and D_Node(current_node, (
                current_node.position[0] + j[0], current_node.position[1] + j[1])) not in closed:
                    children.append(
                        D_Node(current_node, (current_node.position[0] + j[0], current_node.position[1] + j[1])))
                    if (j[0] ** 2 + j[1] ** 2) > 1:
                        children[-1].g = children[-1].parent.g + math.sqrt(2)
                    else:
                        children[-1].g = children[-1].parent.g + 1

                    flag = False
                    for open_item in open:
                        if children[-1].position == open_item.position and children[-1].g >= open_item.g:
                            flag = True
                    if flag == False:
                        open.append(children[-1])




path_list = []
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if chosen_alg == 1:
                    for end_node in get_end_nodes(grid):
                        path = aStar(grid,start_test,end_node)
                        path_list.append(path)
                    for each in path_list:
                        for i in each:
                            if grid[i[0]][i[1]] != 5 and grid[i[0]][i[1]] != 6:
                                grid[i[0]][i[1]] = 2
                    # clearRG(grid)
                elif chosen_alg == 2:
                    paths = dijskra(grid,start_test,get_end_nodes(grid))
                    for each in paths:
                        for i in each:
                            if grid[i[0]][i[1]] != 5 and grid[i[0]][i[1]] != 6:
                                grid[i[0]][i[1]] = 2
            if event.key == pygame.K_RETURN:
                # erase_full(grid)
                # draw(grid)
                # start_test = list(start_test)
                # setup()

            if event.key == pygame.K_BACKSPACE:
                erase(grid)
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
                grid[row][column] = 6
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






















