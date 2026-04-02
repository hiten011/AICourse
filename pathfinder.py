from pprint import pprint
from collections import deque

class PathFinder:
    # run simulation
    def run(self, cmds):
        # 1. parse commands
        try:
            self.parseInput(cmds)
        except:
            print("[Error] Parsing CMDS Failed")
            return False

        # 2. parse input from text file
        try:
            self.parseMap(cmds)
        except:
            print("[Error] Parsing Text File Failed")
            return False

        # running Algo
        if (self.algo == "BFS"):
            self.BFS()

        # update path
        isValidPath = self.updatePath()

        # printing final path
        if (self.isDebug):  
            print("path: ")
            pprint(self.path) if isValidPath else print("null") 

            print("#visits: ")
            pprint(self.visits) if isValidPath else print("...") 

            print("first visit: ")
            pprint(self.firstVisit) if isValidPath else print("...") 

            print("last visit: ")
            pprint(self.lastVisit) if isValidPath else print("...") 
        else:
            pprint(self.path) if isValidPath else print("null") 

        return True


    # parsing commands
    mode = ""
    mapFile = ""
    algo = ""
    heuristic = ""
    isDebug = False
    def parseInput(self, parsed):
        self.mode = parsed[0]
        self.isDebug = self.mode == "debug"

        self.mapFile = parsed[1]

        self.algo = parsed[2]
        if (self.algo == "A*"):
            self.heuristic = parsed[3]


    # parsing input text file
    adj = ""
    r = 0
    c = 0
    st = []
    en = []
    def parseMap(self, parsed):
        with open(self.mapFile, 'r') as file:
            self.r, self.c = [int(x) for x in file.readline().split()]
            self.st = [int(x) - 1 for x in file.readline().split()]
            self.en = [int(x) - 1 for x in file.readline().split()]

            self.adj = [x.split() for x in file.read().splitlines()]

        # set Variables
        self.path = [[0] * self.c for _ in range(self.r)]
        self.visits = [[0] * self.c for _ in range(self.r)]
        self.firstVisit = [[0] * self.c for _ in range(self.r)]
        self.lastVisit = [[0] * self.c for _ in range(self.r)]
        self.prevVisit = [[(-1, -1)] * self.c for _ in range(self.r)]

        for i in range(0, self.r):
            for j in range(0, self.c):
                if (self.adj[i][j] == 'X'):
                    self.path[i][j] = 'X'
                    self.visits[i][j] = 'X'
                    self.firstVisit[i][j] = 'X'
                    self.lastVisit[i][j] = 'X'
                else:
                    self.path[i][j] = int(self.adj[i][j])
                    self.adj[i][j] = int(self.adj[i][j])

    # update path
    def updatePath(self):
        x, y = self.en
        if self.prevVisit[x][y] == (-1, -1):
            return False

        sx, sy = self.st
        while ((x, y) != (sx, sy)):
            self.path[x][y] = '*'
            x, y = self.prevVisit[x][y]

        self.path[x][y] = '*'
        return True

    # algos
    path = []
    visits = []
    firstVisit = []
    lastVisit = []
    prevVisit = []
    dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    # BFS Algo
    def BFS(self):
        print("BFS")

        # counter: tracks current visit'th
        counter = 0

        # min cost at each cell
        dp = [[-1] * self.c for _ in range(self.r)]

        q = deque() # queue
        q.append((0, self.st)) # q: {curCost, [x, y]}
        while (q):
            counter += 1

            cost, cur = q.popleft()
            x, y = cur
            
            for dx, dy in self.dir:   
                # new cord
                i = dx + x
                j = dy + y

                isValid = i >= 0 and j >= 0 and i < self.r and j < self.c and not self.path[i][j] == 'X' and (dp[i][j] == -1 or dp[i][j] > cost + self.calcCost(x, y, i, j))
                if (isValid):
                    dp[i][j] = cost + self.calcCost(x, y, i, j)
                    q.append((dp[i][j], (i, j)))

                    self.prevVisit[i][j] = (x, y)

                    # Debug Mode
                    if self.isDebug:
                        self.visits[i][j] += 1
                        self.lastVisit[i][j] = counter
                        self.firstVisit[i][j] = self.firstVisit[i][j] if self.firstVisit[i][j] else counter

        # print(dp[self.en[0]][self.en[1]])


    # helper functions
    calcCost = lambda self, x, y, i, j : 1 + max(self.path[i][j] - self.path[x][y], 0)



import sys
def main():
    pf = PathFinder()

    # run simulation
    if not pf.run(sys.argv[1:]):
        print("[EXIT] exiting...")

if __name__ == "__main__":
    main()
