
# coding: utf-8

# ## Soduko Solving With Matrix
# ### Solving Sudoku by representing a board as a set of equations and solving them

# In[101]:


import numpy as np
import z3
from typing import List


# In[131]:


class BooleanVariable:
    def __init__(self, name: str):
        self.name = name
        self.var = z3.Bool(name)
        self.value = None
 


# In[194]:


class OneIsTrueConstraint:
    def __init__(self, variables: List[BooleanVariable]):
        self.variables = variables
    
    def to_cnf(self):
        # cnf that states that one of the variables and only one of them is true:

        vars = [var.var for var in self.variables]
        clauses = []
        for i in range(len(vars)):
            var_i = vars[i]
            other_vars = [vars[j] for j in range(len(vars))  if j != i]
            # checks that only i var is true and rest is false.
            clause = z3.And([z3.Not(v) for v in other_vars] + [var_i])
            clauses.append(clause)
        total_cnf = z3.Or(clauses)
        return total_cnf
    
    def __repr__(self):
        return '+'.join([var.name for var in self.variables]) + f'=1'
    


# In[354]:


class BoardSolver:
    def __init__(self, board: np.ndarray):
        """
        initing equations set by given board.
        Args:
          board: initial sudoko board represented with 0's on empty spots, and numbers on 
        """
        self.board = board
        self.n = len(board)
        self._create_empty_board_equations_set()
        self._assign_variables_by_initial_board(board)
        
    
    def _name_giver(self, square_i_j, value):
        return f'is_square[{square_i_j[0] + 1}][{square_i_j[1] + 1}]_equals_{value+1}'
        
    def _create_empty_board_equations_set(self):
        # create n variables for each of the n**2 squares- total of n**3 variables
        n = self.n
        variables = {}
        constraints = []
        
        for square_i in range(n):
            for square_j in range(n):
                for k in range(n):
                    name = self._name_giver((square_i, square_j), k)
                    variables[name] =  BooleanVariable(name=name)
                    
        # the representation of a square by n boolean variables and not one int makes us add a constraint per square, that says the sum of those variables is 1.
        for square_i in range(n):
            for square_j in range(n):
                vars = [variables[self._name_giver((square_i, square_j), k)] for k in range(n)]
                constraints.append(OneIsTrueConstraint(variables=vars))


            
        # add rows constraints
        for square_row in range(n):
            for val in range(n):
                # constraint - for each possible square value, make sure that only one of the row variables of that value is 1 - i.e. their sum is 1.
                vars = [variables[self._name_giver((square_row, col), val)] for col in range(n)]
                constraints.append(OneIsTrueConstraint(variables=vars))
        
        # add columns constraints
        for square_col in range(n):
            for val in range(n):
                # constraint - for each possible square value, make sure that only one of the column variables of that value is 1 - i.e. their sum is 1.
                vars = [variables[self._name_giver((row, square_col), val)] for row in range(n)]
                constraints.append(OneIsTrueConstraint(variables=vars))
        
        # add boxes constraints
        sqrtn = int(n**0.5)
        for i in range(sqrtn):
            for j in range(sqrtn):
                box_indexes = [(i * sqrtn + ind_i, j * sqrtn + ind_j) for ind_j in range(sqrtn) for ind_i in range(sqrtn)]
                for val in range(n):
                    constraints.append(OneIsTrueConstraint(variables=[variables[self._name_giver((bi, bj), val)] for bi,bj in box_indexes]))
        
        self.variables = variables
        self.constraints = constraints
    
        
    def _assign_variables_by_initial_board(self, board: np.ndarray):
        for square_i in range(board.shape[0]):
            for square_j in range(board.shape[1]):
                board_val = board[square_i][square_j]
                if board_val != 0:
                    board_val = board_val - 1
                    for val in range(self.n):
                        if val == board_val:
                            self.variables[self._name_giver((square_i, square_j), val)].value = True                
                        else:
                            self.variables[self._name_giver((square_i, square_j), val)].value = False
                            
                            
    def solve(self):
        n = self.n
        slvr = z3.Solver()
        # add already assinged values to the solver.
        for var in self.variables.values():
            if var.value is not None:
                slvr.add(var.var == var.value)
        
        
         # add the cnfs of the constraints:
        for cons in self.constraints:
            slvr.add(cons.to_cnf())
        
        problem_type = slvr.check()
        if str(problem_type) == 'sat':
            model = slvr.model()

            # create full board based on sat solution:
            solved_board = self.board.copy()
            for square_i in range(n):
                for square_j in range(n):
                    if self.board[square_i][square_j] == 0:
                        for val in range(n):
                            variable = self.variables[self._name_giver((square_i, square_j), val)]
                            if model.eval(variable.var == True):
                                solved_board[square_i][square_j] = val + 1
                                break
            return solved_board
        elif str(problem_type) == 'unsat':
            return 'Board is not solvable'
    


# In[356]:
if __name__ == "__main__":

    example_board = np.array([[5,3,0,0,7,0,0,0,0],
                    [6,0,0,1,9,5,0,0,0],
                    [0,9,8,0,0,0,0,6,0],
                    [8,0,0,0,6,0,0,0,3],
                    [4,0,0,8,0,3,0,0,1],
                    [7,0,0,0,2,0,0,0,6],
                    [0,6,0,0,0,0,2,8,0],
                    [0,0,0,4,1,9,0,0,5],
                    [0,0,0,0,8,0,0,7,9]])
    example_board.shape


    # In[357]:


    s = BoardSolver(example_board)


    # In[358]:


    len(s.constraints)


    # In[359]:


    len(s.variables)


    # In[360]:


    solution = s.solve()


    # In[361]:


    solution


    # In[362]:


    board = np.array([[3,7,0,5,9,0,0,0,1],
                    [0,0,5,8,0,0,0,0,6],
                    [0,1,0,3,0,6,4,0,0],
                    [2,0,8,0,4,9,0,6,5],
                    [0,0,9,0,0,0,7,0,0],
                    [5,4,0,0,6,0,8,0,2],
                    [0,0,4,6,0,8,0,1,0],
                    [6,0,0,0,0,7,9,0,0],
                    [7,0,0,0,5,2,0,3,4]])
    print(board.shape)
    s = BoardSolver(board)
    solution = s.solve()
    solution


    # In[363]:


    board = np.array([[0, 4, 0, 3, 0, 7, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 8, 0],
                    [7, 2, 3, 0, 0, 0, 0, 6, 0],
                    [0, 0, 6, 9, 0, 0, 0, 4, 5],
                    [0, 0, 2, 0, 4, 1, 3, 0, 6],
                    [0, 0, 0, 0, 0, 0, 0, 0, 7],
                    [0, 0, 0, 0, 6, 0, 0, 0, 9],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 4, 5, 1, 8, 0, 0, 0]])
    print(board.shape)
    s = BoardSolver(board)
    solution = s.solve()
    solution


    # In[364]:


    # error:
    board = np.array([[0, 4, 0, 3, 0, 7, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 8, 0],
                    [7, 2, 3, 0, 0, 0, 0, 6, 0],
                    [0, 0, 6, 9, 0, 0, 0, 4, 5],
                    [0, 0, 2, 0, 4, 1, 3, 0, 6],
                    [0, 0, 0, 0, 0, 0, 0, 0, 7],
                    [0, 0, 0, 0, 6, 0, 0, 0, 9],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [2, 0, 4, 5, 1, 8, 0, 0, 0]])
    print(board.shape)
    s = BoardSolver(board)
    solution = s.solve()
    solution


