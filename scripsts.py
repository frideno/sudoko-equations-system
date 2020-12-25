
# coding: utf-8

# ## Soduko Solving With Matrix
# ### Solving Sudoku by representing a board as a set of equations and solving them

# In[12]:


import numpy as np


# In[7]:


class Variable:
    def __init__(self, options=[]):
        self.options = options


# In[18]:


class SumConstraint:
    def __init__(self, variables: List[Variable], variables_sum: int):
        self.variables = variables
        self.sum = variables_sum
    
    def to_equation(self) -> np.array:
        pass


# In[9]:


class BoardSolver:
    def __init__(self, board: np.ndarray):
        """
        initing equations set by given board.
        Args:
          board: initial sudoko board represented with 0's on empty spots, and numbers on 
        """
        self.board = board
        self.equations = self._create_empty_board_equations_set(n=len(board))
        self.equations = self._eliminate_equations_by_initial_board(board)
        
    
    def solve(self) -> np.ndarray:
        # solve on self.equations, and put results in self.board, which will be returned.
        pass
    
    def _create_empty_board_equations_set(self, n):
        # create n variables for each of the n**2 squares- total of n**3 variables.
        self.variables = {}
        for square_i in range(n):
            for square_j in range(n):
                self.variables[(square_i, square_j)] = Variable(options=[0, 1])
    
        # add rows constraints
        
        # add columns constraints
        
        # add boxes constraints
        
    
            

