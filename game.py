import numpy as np

class Game:
    def __init__(self):
        self.MAX_GROUP_SIZE = 4
        self.maxY = 12
        self.maxX = 6
        self.points = 0
        self.grid = np.zeros((self.maxY,self.maxX))


    def printBoard(self):
        for row in self.grid:
            print(row)

    def dropSoloPuyo(self, x, color):
        yIndex = 0
        while yIndex < self.maxY and self.grid[yIndex,x] == 0:
            yIndex += 1
        self.grid[yIndex-1][x] = color     

    # for dropping a puyo in a horizontal formation
    # x1 is the coordinate of the leftmost puyo, x1 < self.maxX
    def dropHorizontalPuyo(self, x1, color1, color2):
        assert(x1 < self.maxX)
        self.dropSoloPuyo(x1, color1)
        self.dropSoloPuyo(x1+1, color2)

    # for dropping a puyo in a vertical formation, color1 above color2
    def dropVerticalPuyo(self, x, color1, color2):
        self.dropSoloPuyo(x, color2)
        self.dropSoloPuyo(x, color1)

    # Goes through every index running BFS to find the group size, pops if above the threshold.
    # Appears like it could take O(n^2m^2) time but if we amortize it only takes O(nm) time
    def popLargePuyoGroups(self):
        yIndex = 0
        xIndex = 0
        currGroup = []
        currGroupColor = 0
        while xIndex < self.maxX and yIndex < self.maxY:
            if self.grid[yIndex][xIndex] != 0:
                currGroupColor = self.grid[yIndex][xIndex]
                currGroup = self.findAdjacentGroup(currGroupColor, yIndex, xIndex)
                if len(currGroup >= self.MAX_GROUP_SIZE):
                    for ele in currGroup:
                        self.grid[ele[0]][ele[1]] = 0
            if xIndex + 1 == self.maxX:
                xIndex = 0
                yIndex += 1
            else:
                xIndex += 1
  
    # The actual BFS that is called as a helper to popLargePuyoGroups
    def findAdjacentGroup(self, currGroupColor, yIndex, xIndex):
        currGroup = [[yIndex, xIndex]]
        queue = {[yIndex, xIndex]}
        visited = {[yIndex, xIndex]}
        while queue:
            nextIndex = queue.pop()
            yIndex = nextIndex[0]
            xIndex = nextIndex[1]
            if yIndex > 0:
                queue.append([yIndex-1,xIndex])
            if yIndex < self.maxY:
                queue.append(



X = Game()
X.dropHorizontalPuyo(2,3,4)
X.dropHorizontalPuyo(1,1,1)
X.printBoard()
