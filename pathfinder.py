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

        return True

    # parsing commands
    mode = ""
    mapFile = ""
    algo = ""
    heuristic = ""
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
            self.st = [int(x) for x in file.readline().split()]
            self.en = [int(x) for x in file.readline().split()]

            self.adj = [x.split() for x in file.read().splitlines()]

        # set Variables
        self.path = [[0] * self.c for _ in range(self.r)]
        self.visits = [[0] * self.c for _ in range(self.r)]
        self.firstVisit = [[0] * self.c for _ in range(self.r)]
        self.lastVisit = [[0] * self.c for _ in range(self.r)]

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


    # algos
    path = []
    visits = []
    firstVisit = []
    lastVisit = []

    # BFS Algo
    def BFS(self):
        q = []

import sys
def main():
    pf = PathFinder()

    # run simulation
    if not pf.run(sys.argv[1:]):
        print("[EXIT] exiting...")

if __name__ == "__main__":
    main()
