import math
class XD:
    def __init__(self,beka,meh):
        self.beka = beka
        self.meh = meh

    def __eq__(self, other):
        return self.beka == other.beka

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
            if (current_node.position[0]+j[0]) > 0 and (current_node.position[0]+j[0]) < 50 and (current_node.position[1]+j[1]) > 0 and (current_node.position[1]+j[1]) < 50:
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
                        if children[-1] == open_item and children[-1].g > open_item.g:
                            flag = True
                    if flag == False:
                        open.append(children[-1])


grid = []
for row in range(50):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(50):
        grid[row].append(0)  # Append a cell

print(aStar(grid,(0,0),(10,15)))