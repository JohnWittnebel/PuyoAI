import numpy as np

class Game:
    def __init__(self):
        self.MAX_GROUP_SIZE = 4
        self.maxY = 12
        self.maxX = 6
        self.points = 0
        self.currentPuyo = []
        self.nextPuyo = []
        self.nextNextPuyo = []
        self.grid = np.zeros((self.maxY,self.maxX))

    def printBoard(self):
        for row in self.grid:
            print(row)
        print(self.points)
        print(self.currentPuyo)
        print(self.nextPuyo)
        print(self.nextNextPuyo)

    def initializeRandomPuyos(self):
        pass

    def dropSoloPuyo(self, x, color):
        yIndex = 0
        while yIndex < self.maxY and self.grid[yIndex,x] == 0:
            yIndex += 1
        self.grid[yIndex-1][x] = color


    def dropCurrentPuyoHorizontal(self, leftIndex, orientation):
        if orientation == 0:
            self.dropHorizontalPuyo(leftIndex, self.currentPuyo[0], self.currentPuyo[1])
        else:
            self.dropHorizontalPuyo(leftIndex, self.currentPuyo[1], self.currentPuyo[0])
        self.currentPuyo = self.nextPuyo
        self.nextPuyo = self.nextNextPuyo
        self.nextNextPuyo = self.generateNewPuyo
    
    def dropCurrentPuyoVertical(self, index, orientation):
        if orientation == 0:
            self.dropVerticalPuyo(index, self.currentPuyo[0], self.currentPuyo[1])
        else:
            self.dropVerticalPuyo(index, self.currentPuyo[1], self.currentPuyo[0])
        self.currentPuyo = self.nextPuyo
        self.nextPuyo = self.nextNextPuyo
        self.nextNextPuyo = self.generateNewPuyo

    # for dropping a puyo in a horizontal formation
    # x1 is the coordinate of the leftmost puyo, x1 < self.maxX
    def dropHorizontalPuyo(self, x1, color1, color2):
        assert(x1 < self.maxX)
        self.dropSoloPuyo(x1, color1)
        self.dropSoloPuyo(x1+1, color2)

        pointMultiplier = 1
        numPopped = self.popLargePuyoGroups()
        while (numPopped > 0):
            self.points += (numPopped * pointMultiplier)
            pointMultiplier *= 3
            self.poppingAftermath()
            numPopped = self.popLargePuyoGroups()

    # for dropping a puyo in a vertical formation, color1 above color2
    def dropVerticalPuyo(self, x, color1, color2):
        self.dropSoloPuyo(x, color2)
        self.dropSoloPuyo(x, color1)
        
        pointMultiplier = 1
        numPopped = self.popLargePuyoGroups()
        while (numPopped > 0):
            self.points += (numPopped * pointMultiplier)
            pointMultiplier *= 3
            self.poppingAftermath()
            numPopped = self.popLargePuyoGroups()


    # function that adjusts the grid after a group of puyos has been popped. In particular, drops the puyos that are 
    # now hanging in the air
    def poppingAftermath(self):
        for xIndex in range(len(self.grid[0])):
            yIndex = 0
            numZeroes = 0
            temp = []
            while yIndex < self.maxY:
                if self.grid[yIndex][xIndex] == 0:
                    numZeroes += 1
                else:
                    temp.append(self.grid[yIndex][xIndex])
                yIndex += 1
            yIndex = 0
            while yIndex < self.maxY:
                if numZeroes > 0:
                    self.grid[yIndex][xIndex] = 0
                else:
                    self.grid[yIndex][xIndex] = temp[numZeroes * -1]
                numZeroes -= 1
                yIndex += 1

    # Goes through every index running BFS to find the group size, pops if above the threshold.
    # Appears like it could take O(n^2m^2) time but if we amortize it only takes O(nm) time
    def popLargePuyoGroups(self):
        yIndex = 0
        xIndex = 0
        currGroup = []
        currGroupColor = 0
        totalPopped = 0
        while xIndex < self.maxX and yIndex < self.maxY:
            if self.grid[yIndex][xIndex] != 0:
                currGroupColor = self.grid[yIndex][xIndex]
                currGroup = self.findAdjacentGroup(currGroupColor, yIndex, xIndex)
                if len(currGroup) >= self.MAX_GROUP_SIZE:
                    totalPopped += len(currGroup)
                    for ele in currGroup:
                        self.grid[ele[0]][ele[1]] = 0
            if xIndex + 1 == self.maxX:
                xIndex = 0
                yIndex += 1
            else:
                xIndex += 1
        return totalPopped
  
    # The actual BFS that is called as a helper to popLargePuyoGroups
    def findAdjacentGroup(self, currGroupColor, yIndex, xIndex):
        currGroup = []
        queue = [[yIndex, xIndex]]
        visited = {}
        while queue:
            nextIndex = queue.pop()
            yIndex = nextIndex[0]
            xIndex = nextIndex[1]
            if self.grid[yIndex, xIndex] != currGroupColor or (yIndex, xIndex) in visited:
                visited[(yIndex, xIndex)] = 1
                continue
            else:
                currGroup.append([yIndex,xIndex])

            if yIndex > 0 and (yIndex-1,xIndex) not in visited:
                queue.append([yIndex-1,xIndex])
            if yIndex < self.maxY - 1 and (yIndex+1,xIndex) not in visited:
                queue.append([yIndex+1,xIndex])
            if xIndex > 0 and (yIndex,xIndex-1) not in visited:
                queue.append([yIndex, xIndex-1])
            if xIndex < self.maxX - 1 and (yIndex,xIndex+1) not in visited:
                queue.append([yIndex, xIndex+1])

            visited[(yIndex,xIndex)] = 1
        return currGroup

    def generateNewPuyo(self):
        pass

    def 



X = Game()
X.dropHorizontalPuyo(2,1,1)
X.dropHorizontalPuyo(2,1,2)
X.dropHorizontalPuyo(2,2,1)
X.dropHorizontalPuyo(4,2,2)
X.dropHorizontalPuyo(4,3,3)
X.dropHorizontalPuyo(4,2,3)
X.dropVerticalPuyo(5,2,3)

X.printBoard()
