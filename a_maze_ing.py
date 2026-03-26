import random, sys
from enum import IntEnum, auto


class Dir(IntEnum):
    N = 0b1110
    E = 0b1101
    S = 0b1011
    W = 0b0111
    aN = auto()
    aE = auto()
    aS = auto()
    aW = auto()


class maze():
    def __init__(self, dic):
        self.height = int(dict.get("HEIGHT"))
        self.width = int(dict.get("WIDTH"))
        self.perfect = str(dict.get("PERFECT"))
        self.entry = tuple(dict.get("ENTRY"))
        self.exit = tuple(dict.get("EXIT"))
        if dict.get("SEED") != "0":
            self.seed = random.seed(dict.get("SEED"))
        else:
            self.seed = random.seed()

    def maze_gen(self):
        self.total = self.width * self.height
        arr = [['f' for _ in range(self.width)] for _ in range(self.height)]
        loc_width, loc_height = self.entry




class cell(maze):
    def __init__(self, walls):
        


if __name__ == "__main__":
    try:
        name = sys.argv()
        with open(name[1]) as file:
            info = file.read()
            tmp = info.split("\n")
            for i in tmp:
                dic = dict()
                key, inp = i.split('=')
                dic.update({key: inp})
    except FileNotFoundError:
        print("File not found")
