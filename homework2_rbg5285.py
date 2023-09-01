############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Robert Gramlich"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import copy
from collections import deque

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
#For this problem we are just finding n^2 choose n
    numer = math.factorial(n*n)
    denom = math.factorial(n) * math.factorial(n*n-n)
    return int(numer/denom)


def num_placements_one_per_row(n):
#Only concerned with rows so each piece can be put in n rows n times
    return n**n


def n_queens_valid(board):
#Since the board stores the column location and its index is the row we will never get a board where queens share a row
#For this function we need to check if queens share a column or a diagonal.
#Create a new list that has (row, col)
#check for duplicates in the board because a duplicate means that queens share a column
#Then we check for shared diagonals by using the definition of slope
#if the row = col then that means that the slope = 1 and the two points lie on the same line
    row_col = []
    if len(board) != len(set(board)):
        return False
    for i in board:
        row_col.append((board.index(i), i))
    c=1
    for i in row_col:
        for x in row_col[c:]:
            row = abs(x[0] - i[0])
            col = abs(x[1] - i[1])
            if row == col:
                return False
        c+=1
    return True


def n_queens_helper(n, board):
#We use this function to find valid adjacent nodes
#This is pretty easy because we just need to add 0...n-1 to the end of the current node we are passed and 
#check if it's valid
    edges = [tuple(n + [i]) for i in range(board)]
    for i in edges:
        if n_queens_valid(i):
            yield i[-1]
            

def n_queens_solutions(n):
#We start by filling the frontier with all the possible columns given n
#We start by populating the frontier with all the columns in row 0, 
#each column in row 0 will act as a root node and each row is a level of the tree
#We find valid moves in the next row(level of tree) using n_queens_helper()
#If length = n and is valid then we found a solution and we return it 
#If we reach a point where we can't find a valid solution with the current root the popped element is disregarded and 
#we go to the next root node and start the search again
    frontier = [[i] for i in range(n)]
    explored = []
    while len(frontier) != 0:
        node = frontier.pop()
        explored.append(node)
        for i in n_queens_helper(node, n):
            child = node + [i]
            if child not in explored:
                if n_queens_valid(child):
                    if len(child) == n:
                        yield child
                    else:
                        frontier.append(child)


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.row = len(board)
        self.col = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
    #To perform a move we need to change the state of the current cell as well as the 4 next to it
    #We also need to make sure that the cell we are trying to change is contained within the board
        self.board[row][col] = not self.board[row][col]
        if (row + 1) in range(self.row):
            self.board[row + 1][col] = not self.board[row + 1][col]
        if (row - 1) in range(self.row):
            self.board[row - 1][col] = not self.board[row - 1][col]
        if (col + 1) in range(self.col):
            self.board[row][col + 1] = not self.board[row][col + 1]
        if (col - 1) in range(self.col):
            self.board[row][col - 1] = not self.board[row][col - 1]
        
    def scramble(self):
    #Go through each cell on the board one by one and randomly choose whether to perform a move on it 
        for row in range(self.row):
            for col in range(self.col):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
    #Checking each cell to make sure the light is turned off and if it is not we have not solved the problem
        for row in self.board:
            for col in row:
                if col:
                    return False
        return True

    def copy(self):
    #making a deep copy of the board
        cavernouscopy = copy.deepcopy(self.board)
        return LightsOutPuzzle(cavernouscopy)

    def successors(self):
    #For every state its successor is when we go through each cell and turn it either on or off if it is in 
    #the bounds of the board.
    #We return the cell that was selected and the board that resulted from selecting that cell.
        for row in range(self.row):
            for col in range(self.col):
                boardcopy = self.copy()
                boardcopy.perform_move(row, col)
                yield ((row, col), boardcopy)

    def get_path(self, node, action):
    #This function is used to get the final path from the board
    #The way I got the paths means that the cells are not paired 
    #The cell coordinates are next to eachother in the final solution
    #So we use a deque to pop from the left to get the correct order without having to reverse a list
        goodpops = deque([])
        solnpath = []
        goodpops = goodpops + deque(node + action)
        while goodpops:
            row = goodpops.popleft()
            col = goodpops.popleft()
            solnpath.append((row, col))
        return solnpath

    def find_solution(self):
    #We perform BFS and we use a deque so that we can efficently pop from the front of the list
    #The cells closest to the start cell are going to be added first to the queue and then popped first
    #This gives us the BFS search
    #I stored the board state in explored as a tuple for fast identification
    #The frontier stores each board state along with the path it took to get there
        frontier = deque([((), self.copy())])
        explored = []
        if self.copy().is_solved():
            return 
        while frontier:
            node = frontier.popleft()
            explored.append(tuple(tuple(i) for i in node[1].get_board()))
            for action, child in node[1].successors():
                if tuple(tuple(i) for i in child.get_board()) not in explored:
                    if child.is_solved():
                        return self.get_path(node[0], action)
                    else:
                        frontier.append((node[0] + action, child))
        return None                

def create_puzzle(rows, cols):
#Creating the board as a list of list of Falses based off of the given rows and cols 
    return LightsOutPuzzle([[False for i in range(cols)] for i in range(rows)])


############################################################
# Section 3: Linear Disk Movement
############################################################

def copy_board(board):
#Making a copy of the current board
    cavernouscopy = copy.deepcopy(board)
    return cavernouscopy

def is_idn_soln(n, board):
#checking if the last n elements are 0(disks)
    for i in board[-n:]:
        if i:
            return False
    return True

def soln_path(node, action):
#Getting the solution path and we have to do this for the same reason as the Lights Out puzzle 
    goodpops = deque([])
    solnpath = []
    goodpops = goodpops + deque(node + action)
    while goodpops:
        to = goodpops.popleft()
        frm = goodpops.popleft()
        solnpath.append((to, frm))
    return solnpath

def find_idn_succ(length, board):
#Function to find the successors
#I change the board from a tuple to list so that I can the indexes later on and I called enumerate so that I 
#could get the index of each element and eaisly change it
#For reasons I could find calling .index() to get the index does not work when the list is only 1s and 0s
#Need to check if a move can be made by checking the cell to left and right and by checking the cell two cells
#away on the left and right
#There is definetly a better way to do this but i couldnt figure it out
#return a new board that contains the (to, from) info and a tuple of the new board
    board = [list(i) for i in enumerate(copy_board(board))]
    for i in range(len(board)):
        if not board[i][1]:
            if i + 1 < length:
                if board[i + 1][1]:
                    succboard = copy_board(board)
                    succboard[i][1] = 1
                    succboard[i + 1][1] = 0
                    yield ((i, i + 1), tuple(i[1] for i in succboard))
                elif i + 2 < length:
                    if board[i + 2][1]:
                        succboard = copy_board(board)
                        succboard[i][1] = 1
                        succboard[i + 2][1] = 0
                        yield ((i, i + 2), tuple(i[1] for i in succboard)) 
            if i - 1 >= 0:
                if board[i - 1][1]:
                    succboard = copy_board(board)
                    succboard[i][1] = 1
                    succboard[i - 1][1] = 0
                    yield ((i, i - 1), tuple(i[1] for i in succboard)) 
                elif i - 2 >= 0:
                    if board[i - 2][1]:
                        succboard = copy_board(board)
                        succboard[i][1] = 1
                        succboard[i - 2][1] = 0
                        yield ((i, i - 2), tuple(i[1] for i in succboard))

def solve_identical_disks(length, n):
#Run BFS
#The logic here is identical to the Lights Out puzzle
    temp = tuple([0 for i in range(n)] + [1 for i in range(n, length)])
    board = copy_board(temp)
    frontier = deque([((), board)])
    explored = []
    if is_idn_soln(n, board):
        return 
    while frontier:
        node = frontier.popleft()
        explored.append(node[1])
        for action, child in find_idn_succ(length, node[1]):
            if child not in explored:
                if is_idn_soln(n, child):
                    return soln_path(node[0], action)
                else:
                    frontier.append((node[0] + action, child))
    return None


def is_dis_soln(n, board):
#checking if the last n elements are 0(disks) and making sure they are in the right order
    for i in board[-n:]:
        if i[1]:
            return False
        if i[0] != n-1:
            return False
        else:
            n = n-1
    return True

def find_dis_succ(length, board):
#Very similar to the identical case except now we are completely swaping the element in the list so that we 
#can keep track of their inital position 
    board = [list(i) for i in copy_board(board)]
    for i in range(len(board)):
        if not board[i][1]:
            if i + 1 < length:
                if board[i + 1][1]:
                    succboard = copy_board(board)
                    succboard[i] = board[i + 1]
                    succboard[i + 1] = board[i]
                    yield ((i, i + 1), tuple(tuple(i) for i in succboard))
                elif i + 2 < length:
                    if board[i + 2][1]:
                        succboard = copy_board(board)
                        succboard[i] = board[i + 2]
                        succboard[i + 2] = board[i]
                        yield ((i, i + 2), tuple(tuple(i) for i in succboard)) 
            if i - 1 >= 0:
                if board[i - 1][1]:
                    succboard = copy_board(board)
                    succboard[i] = board[i - 1]
                    succboard[i - 1] = board[i]
                    yield ((i, i - 1), tuple(tuple(i) for i in succboard)) 
                elif i - 2 >= 0:
                    if board[i - 2][1]:
                        succboard = copy_board(board)
                        succboard[i] = board[i - 2]
                        succboard[i - 2] = board[i]
                        yield ((i, i - 2), tuple(tuple(i) for i in succboard))

def solve_distinct_disks(length, n):
#Same logic as identical case except now we dont find a solution until the disks are in the right order
#Used enumerate to keep track of original positions
    temp = tuple([0 for i in range(n)] + [1 for i in range(n, length)])
    board = tuple(enumerate(copy_board(temp)))
    frontier = deque([((), board)])
    explored = []
    if is_dis_soln(n, board):
        return 
    while frontier:
        node = frontier.popleft()
        explored.append(node[1])
        for action, child in find_dis_succ(length, node[1]):
            if child not in explored:
                if is_dis_soln(n, child):
                    return soln_path(node[0], action)
                else:
                    frontier.append((node[0] + action, child))
    return None

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
In total I spent about 20 hours working on this assignment. With most of the time being spent on the Lights Out puzzle
and figuring out how to get the solution path.
"""

feedback_question_2 = """
I found the Lights Out puzzle to be the hardest puzzle of the 4. The part I found most challenging was being able to trace
the path back from goal to source, that took me a long time to figure out.
"""

feedback_question_3 = """
I liked doing the n-queens puzzle because getting the path was straightforward and I didn't struggle with it like in the 
Lights out. The two disk problems were fun as well because I was able to use a lot of what I learned in the 
Lights Out puzzle and apply it to them. Some things I would change would be to have more test cases and to know if there
is a maximum time that our algorithms should take to run. Having the GUI to play the Lights Out game was really nice too.
I didn't use it for debugging but it was nice to be able to see the algorithm work. It's especially cool because it allowed
me to show other people what I worked on in a fun and interactive way.  
"""