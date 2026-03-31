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

        return True

    # parsing commands
    mode = ""
    mapFile = ""
    algo = ""
    heuristic = ""
    def parseInput(self, parsed):
        self.mode = parsed[0]
        self.mapFile = parsed[1]
        self.algo = parsed[2]
        self.heuristic = parsed[3]

    # parsing input text file
    adj = ""
    r = ""
    c = ""
    st = ""
    en = ""
    def parseMap(self, parsed):
        with open(self.mapFile, 'r') as file:
            self.r, self.c = file.readline().split(" ")
            self.st = file.readline().split(" ")
            self.en = file.readline().split(" ")

            self.adj = file.read()

import sys
def main():
    pf = PathFinder()

    # run simulation
    if not pf.run(sys.argv[1:]):
        print("[EXIT] exiting...")

if __name__ == "__main__":
    main()
