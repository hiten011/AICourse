from collections import deque
import heapq
import math

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

        # 3. running Algo
        if (self.algo == "bfs"):
            self.BFS()
        elif (self.algo == "ucs"):
            self.UCS()
        elif (self.algo == "astar"):
            self.A()
        else:
            print("[Error] Not valid Algo")
            return False

        # 4. update path
        isValidPath = self.updatePath()

        # 5. printing final path
        if (self.isDebug):  
            print("path: ")
            self.pprint(self.path) if isValidPath else print("null") 

            print("#visits: ")
            self.pprint(self.visits) if isValidPath else print("...") 

            print("first visit: ")
            self.pprint(self.firstVisit) if isValidPath else print("...") 

            print("last visit: ")
            self.pprint(self.lastVisit) if isValidPath else print("...") 
        else:
            self.pprint(self.path) if isValidPath else print("null") 

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
        if (self.algo == "astar"):
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
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rank = 0

    # BFS Algo
    def BFS(self):
        # counter: tracks current visit'th
        counter = 0

        # min cost at each cell
        visited = [[-1] * self.c for _ in range(self.r)]

        q = deque() # queue
        q.append(self.st) # q: [x, y]
        while (q):
            counter += 1

            cur = q.popleft()
            x, y = cur

            # Debug Mode
            if self.isDebug:
                self.visits[x][y] += 1
                self.lastVisit[x][y] = counter
                self.firstVisit[x][y] = self.firstVisit[x][y] if self.firstVisit[x][y] else counter
            
            for dx, dy in self.dir:   
                # new cord
                i = dx + x
                j = dy + y

                isValid = i >= 0 and j >= 0 and i < self.r and j < self.c and not self.path[i][j] == 'X' and visited[i][j] == -1
                if (isValid):
                    visited[i][j] = 0
                    q.append((i, j))

                    self.prevVisit[i][j] = (x, y)

                    if i == self.en[0] and j == self.en[1]:
                        return True

    # UCS
    def UCS(self):
        # counter: tracks current visit'th
        counter = 0

        # min cost at each cell
        dp = [[-1] * self.c for _ in range(self.r)]

        q = [] # queue
        heapq.heappush(q, (0, self.nextRank(), self.st)) # q: {curCost, counter, [x, y]}
        while (q):
            counter += 1

            cost, rank, cur = heapq.heappop(q)  
            x, y = cur

            # Debug Mode
            if self.isDebug:
                self.visits[x][y] += 1
                self.lastVisit[x][y] = counter
                self.firstVisit[x][y] = self.firstVisit[x][y] if self.firstVisit[x][y] else counter
            
            for dx, dy in self.dir:   
                # new cord
                i = dx + x
                j = dy + y

                isValid = i >= 0 and j >= 0 and i < self.r and j < self.c and not self.path[i][j] == 'X' and (dp[i][j] == -1 or dp[i][j] > cost + self.calcCost(x, y, i, j))
                if (isValid):
                    dp[i][j] = cost + self.calcCost(x, y, i, j)
                    heapq.heappush(q, (dp[i][j], self.nextRank(), (i, j)))

                    self.prevVisit[i][j] = (x, y)


    # A* algo
    def A(self):
        # counter: tracks current visit'th
        counter = 0

        # min cost at each cell
        dp = [[-1] * self.c for _ in range(self.r)]

        q = [] # queue
        heapq.heappush(q, (self.heuristicCost(self.st[0], self.st[1]), 0, self.nextRank(), self.st)) # q: {curCost, [x, y]}
        while (q):
            counter += 1

            h, cost, rank, cur = heapq.heappop(q)  
            x, y = cur

            # Debug Mode
            if self.isDebug:
                self.visits[x][y] += 1
                self.lastVisit[x][y] = counter
                self.firstVisit[x][y] = self.firstVisit[x][y] if self.firstVisit[x][y] else counter
            
            for dx, dy in self.dir:   
                # new cord
                i = dx + x
                j = dy + y

                isValid = i >= 0 and j >= 0 and i < self.r and j < self.c and not self.path[i][j] == 'X' and (dp[i][j] == -1 or dp[i][j] > cost + self.calcCost(x, y, i, j))
                if (isValid):
                    dp[i][j] = cost + self.calcCost(x, y, i, j)
                    heapq.heappush(q, (self.heuristicCost(i, j) + dp[i][j], dp[i][j], self.nextRank(), (i, j)))

                    self.prevVisit[i][j] = (x, y)

    def heuristicCost(self, x, y):
        ex, ey = self.en
        if self.heuristic == "euclidean":
            return math.sqrt((ex - x)**2 + (ey - y)**2)
        else:  # manhattan
            return abs(ex - x) + abs(ey - y)
        

    # helper functions
    calcCost = lambda self, x, y, i, j : 1 + max(self.path[i][j] - self.path[x][y], 0)

    def nextRank(self): 
        self.rank += 1
        return self.rank

    # print function to print grids
    def pprint(self, grid, width = 1):
        for row in grid:
            print(" ".join(str(cell).rjust(width) for cell in row))



import sys
def main():
    pf = PathFinder()

    # run simulation
    if not pf.run(sys.argv[1:]):
        print("[EXIT] exiting...")

if __name__ == "__main__":
    main()
