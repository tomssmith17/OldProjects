#initial state
#define rules
#loop through all values in initial state, checking rules and changing values of a new state
#while loop to keep going through for looping until certain iteration is reached or user declares stop
#at end, visualize


#%%

import numpy as np

#%%

grid = np.random.randint(2, size=(10, 10))


#%%

def rules(n, neighborList): 
    if n == 0:
        if any(x == 1 for x in neighborList):
            N = 1
        else:
            N = 0
    else:
        N = 0
    return N

def neighborPossible(nRowsY, nColsX, i, j):
    neighborExist = []  #[up, down, left, right]
    if i == 0:
        neighborExist.append(False)
    if i != 0:
        neighborExist.append(True)
    if i == nRowsY-1:
        neighborExist.append(False)
    if i != nRowsY-1:
        neighborExist.append(True)
    if j == 0:
        neighborExist.append(False)
    if j != 0:
        neighborExist.append(True)
    if j == nColsX-1:
        neighborExist.append(False)
    if j != nColsX-1:
        neighborExist.append(True)
    return neighborExist 


   
def start():
    global grid # need to figure our how to use newGrid in next recursion
    newGrid = np.tile(9, grid.shape)
    nRowsY = grid.shape[0]   
    nColsX = grid.shape[1]   
    for i in range(0,nRowsY):
        for j in range(0,nColsX):
            n = grid[i][j]
            neighborExist = neighborPossible(nRowsY, nColsX, i, j)
            neighborList = []
            if neighborExist[0] == True:  
                neighborList.append(grid[i-1][j])
            if neighborExist[1] == True:
                neighborList.append(grid[i+1][j])
            if neighborExist[2] == True:
                neighborList.append(grid[i][j-1])
            if neighborExist[3] == True:
                neighborList.append(grid[i][j+1])
            N = rules(n, neighborList)
            newGrid[i][j] = N
    print(grid)
    print('\n')
    print(newGrid)

