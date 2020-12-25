
# coding: utf-8

# ## Soduko Solving With Matrix
# ### Solving Sudoku by representing a board as a set of equations and solving them

# In[3]:


import numpy as np


# In[2]:


class Board:
    def __init__(self, board: np.ndarray):
        """
        initing a board.
        Args:
          board: initial sudoko board represented with 0's on empty spots, and numbers on 
        """

