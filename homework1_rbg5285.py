############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Robert Gramlich"

############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(i) for i in l if p(i)]
    

def concatenate(seqs):
    return [x for i in seqs for x in i]

def transpose(matrix):
    return [[i[x] for i in matrix] for x in range(len(matrix[0]))]
    

############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    return seq[::]

def all_but_last(seq):
    return seq[0:-1]

def every_other(seq):
    return seq[0::2]

############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq)):
        yield seq[0:i]
    yield seq[::]

def suffixes(seq):
    yield seq[::]
    for i in range(len(seq)):
        yield seq[i+1:]

def slices(seq):
    x = 0
    while x <= len(seq):
        for i in range(x, len(seq)):
            yield seq[x:i+1]
        x += 1 

############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return " ".join(text.lower().split())
    
def no_vowels(text):
    vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
    return "".join([i for i in text if i not in vowels])
    
def digits_to_words(text):
    nums = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
    return " ".join([nums[i] for i in text if i in nums])

def to_mixed_case(name):
    nAme = name.split('_')
    nAme = [i for i in nAme if i] 
    for i in range(len(nAme)):
        if i == 0:
            nAme[0] = nAme[0].lower()
        else:
            nAme[i] = nAme[i].capitalize()
    return "".join(nAme)

############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.poly = tuple(polynomial)

    def get_polynomial(self):
        return self.poly

    def __neg__(self):
        negpoly = self.poly
        negpoly = [list(i) for i in negpoly]
        for i in range(len(negpoly)):
            negpoly[i][0] = -negpoly[i][0]
        negpoly = [tuple(i) for i in negpoly]
        return Polynomial(negpoly)
      
    def __add__(self, other):
        return Polynomial(self.poly + other.poly)

    def __sub__(self, other):
        other = other.__neg__()
        return self.__add__(other)

    def __mul__(self, other):
        return Polynomial([tuple([i[0] * z[0], i[1] + z[1]]) for i in self.poly for z in other.poly])

    def __call__(self, x):
        return sum([i[0]*x**i[1] for i in self.poly])

    def simplify(self):
        dict={}
        for i in self.poly:
            if i[1] in dict:
                dict[i[1]] = (dict.get(i[1]) + i[0])
                if dict.get(i[1]) == 0:
                    dict.pop(i[1])
            else:
                dict[i[1]] = i[0]
        if len(dict) == 0:
            dict[0] = 0
        self.poly = tuple(sorted(tuple([(dict.get(key), key) for key in dict]), key = lambda x:x[1], reverse = True))

    def __str__(self):
        q=[]
        z=[]
        for i in self.poly:
            if i[1] == 0:
                q.append('%+d' % (i[0]))
            elif i[1] == 1:
                if i[0] == 1:
                    q.append('+x')
                elif i[0] == -1:
                    q.append('-x')
                elif i[0] > 0:
                    q.append('%+dx' % (i[0]))
                else:
                    q.append('%+dx' % (i[0]))
            elif i[0] == 1:
                q.append('+x^%d' % (i[1]))
            elif i[0] == -1:
                q.append('-x^%d' % (i[1]))
            elif i[0] > 1:
                q.append('%+dx^%d' % (i[0], i[1]))
            else:
                q.append('%+dx^%d' % (i[0], i[1]))
        for i in q:
            x = i[0]
            y = i[1:]
            z.append("{} {}".format(x,y))
        z=" ".join(z)
        if z[0] == '+':
            return '{}'.format((z[1:]).lstrip())
        elif z[0] == '-':
            return'-{}'.format((z[1:].lstrip()))

############################################################
# Section 6: Feedback
############################################################

feedback_question_1 = """
For this assignment I spent approximately 15 hrs on this assignment
"""

feedback_question_2 = """
Working on the Polynomial class was the most challenging part for me. The first few methods were not too challenging. Most of my
time was spent on the simplify() and __str()__ methods.
"""

feedback_question_3 = """
While it was the hardest part for me, I enjoyed working on the Polynomial class the most. It made me read through the
documentation and I came away with a better understanding. I wouldn't change much about this assignment except adding some tips 
in the beginning on how to set of different working environments for python. 
"""

def n_queens_valid(board):
#Since the board stores the column location and its index is the row we will never get a board where queens share a row
#For this function we need to check if queens share a column or a diagonal.
    #Create a new list that has (row, col)
    row_col = list(enumerate(board))
    #checking for duplicates in the orginal board because a duplicate means that queens share a column
    if len(board) != len(set(board)):
        return False
    #Here we check for shared diagonals by using the definition of slope
    #if the row = col then that means that the slope = 1 and the two points lie on the same line
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
    dic = {}
    forvalid = [i for i in n]
    edges = [tuple(forvalid + [i]) for i in range(board)]
    for i in edges:
        if n_queens_valid(i):
            yield i[-1]
        
            
def n_queens_solutions(n):
    visited = []
    stack = []
    for i in range(n):
        stack.append(i)
        while len(stack) != 0:
            cell = stack.pop()
            if cell not in visited:
                visited.append(cell)
                for i in n_queens_helper(visited, n):
                    stack.append(i)
                        
                
            print('stack:{}'.format(stack))
            print('visited:{}'.format(visited))
            print('')
        soln = [i for i in visited]
        if n_queens_valid(soln) and len(soln) != 1:
            yield soln
            visited = []
        else:
            visited = []