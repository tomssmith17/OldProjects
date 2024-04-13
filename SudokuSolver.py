# This script solves sudoku puzzles using recursion and back tracking!

#once working, make nice GUI
#indexing: grid[3][5] == row 4, column 6 > grid[y][x]

#%%

import numpy as np
#%%
grid = [[0,0,0,0,2,0,1,0,0],
        [7,0,8,0,0,0,0,0,6], 
        [2,3,0,0,7,0,0,0,0],
        [0,0,7,0,0,4,0,3,0],
        [5,1,0,0,0,0,0,6,4],
        [0,8,0,5,0,0,7,0,0],
        [0,0,0,0,3,0,0,4,8],
        [8,0,0,0,0,0,6,0,2],
        [0,0,5,0,9,0,0,0,0]]

print(np.matrix(grid))

#%%
def possible(y,x,n):
    global grid
    for i in range(0,9): #checks columns for specific row
        if grid[y][i] == n:
            return False
    for i in range(0,9): #checks rows for specific column
        if grid[i][x] == n: 
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0,3): #checks squares
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

#%%
def solve():
    global grid
    for y in range(0,9):
        for x in range(0,9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x] = n
                        solve() #recursion 
                        grid[y][x] = 0 #backtracking, if recursive solve reaches a deadend before solution
                return
    print(np.matrix(grid))
    input('More?')
#%%


