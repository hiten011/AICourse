split = "/?"

class PathFinder:
    mode = ""
    mapFile = ""
    algo = ""
    heuristic = ""

    # parsing commands
    def parseInput(self, cmds):
        parsed = cmds.split(split)

        self.mode = parsed[0]
        self.mapFile = parsed[1]
        self.algo = parsed[2]
        self.heuristic = parsed[3]

    # run simulation
    def run(self, cmds):
        try:
            self.parseInput(cmds)
        except:
            print("[Error] Parsing Failed")
            return False

        return True

import sys
def main():
    pf = PathFinder()

    # parse commands
    cmds = split.join(sys.argv[1:])

    # run simulation
    if not pf.run(cmds):
        print("[EXIT] exiting...")

if __name__ == "__main__":
    main()
