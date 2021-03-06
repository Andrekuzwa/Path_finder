import pygame
import math
import time

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
START_COLOR = (0,200,200)
END_COLOR = (255,165,0)

WIDTH = 12
HEIGHT = 12

MARGIN = 1

grid = []
for row in range(50):
    grid.append([])
    for column in range(50):
        grid[row].append(0)

pygame.init()

WINDOW_SIZE = [651, 701]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Finder")

done = False

clock = pygame.time.Clock()

start_test = [None,None]
chosen_alg = 1

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

def switch_clear(grid):
    for row in range(50):
        for column in range(50):
            if grid[row][column] != 5 and grid[row][column] != 6 and grid[row][column] != 1:
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

        for i in open:
            if i.position is not None and grid[i.position[0]][i.position[1]]!=5 and grid[i.position[0]][i.position[1]]!=6:
                grid[i.position[0]][i.position[1]] = 4

        for i in closed:
            if i.position is not None and grid[i.position[0]][i.position[1]]!=5 and grid[i.position[0]][i.position[1]]!=6:
                grid[i.position[0]][i.position[1]] = 3

        current_node = open[0]
        current_index = 0

        for index,item in enumerate(open):
            if item.f < current_node.f:
                current_node = item
                current_index = index


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





exec_time = None
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if chosen_alg == 1:
                    time_start = time.time()
                    path_list = []
                    for end_node in get_end_nodes(grid):
                        path = aStar(grid,start_test,end_node)
                        path_list.append(path)
                    for each in path_list:
                        for i in each:
                            if grid[i[0]][i[1]] != 5 and grid[i[0]][i[1]] != 6:
                                grid[i[0]][i[1]] = 2
                    time_end = time.time()
                    exec_time = time_end - time_start
                    print(exec_time)
                elif chosen_alg == 2:
                    time_start = time.time()
                    paths = dijskra(grid,start_test,get_end_nodes(grid))
                    for each in paths:
                        for i in each:
                            if grid[i[0]][i[1]] != 5 and grid[i[0]][i[1]] != 6:
                                grid[i[0]][i[1]] = 2
                    time_end = time.time()
                    exec_time = time_end - time_start
                    print(exec_time)
            if event.key == pygame.K_RETURN:
                erase_full(grid)
                start_test = list(start_test)
                setup()
                exec_time = None
                grid[start_test[0]][start_test[1]] = 5
                print(start_test)
                print(grid[start_test[0]][start_test[1]])
            if event.key == pygame.K_BACKSPACE:
                erase(grid)
                exec_time = None
            if event.key == pygame.K_s:
                switch_clear(grid)
                exec_time = None
                if chosen_alg == 1:
                    chosen_alg = 2
                else:
                    chosen_alg = 1
            if event.key == pygame.K_p:
                clearRG(grid)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


        if pygame.mouse.get_pressed()[0]:
            try:
                pos = event.pos
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                grid[row][column] = 1
            except AttributeError:
                pass
            except IndexError:
                print("Out of grid!")
        if pygame.mouse.get_pressed()[2]:
            try:
                pos = event.pos
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                grid[row][column] = 6
            except AttributeError:
                pass
            except IndexError:
                print("Out of grid!")


    screen.fill(WHITE)

    font = pygame.font.Font('freesansbold.ttf', 32)
    if exec_time == None:
        if chosen_alg == 1:
            text = font.render('A* - Execution time: ', True, BLACK, WHITE)
        else:
            text = font.render('Dijskra - Execution time: ', True, BLACK, WHITE)
    else:
        if chosen_alg == 1:
            text = font.render('A* - Execution time: {}s'.format(round(exec_time, 2)), True, BLACK, WHITE)
        else:
            text = font.render('Dijskra - Execution time: {}s'.format(round(exec_time, 2)), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (330,675)
    screen.blit(text, textRect)
    draw(grid)


    clock.tick(60)

    pygame.display.flip()

pygame.quit()






















