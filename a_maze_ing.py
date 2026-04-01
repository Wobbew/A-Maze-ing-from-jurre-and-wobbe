import random, sys
from enum import IntEnum, auto


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
        total = self.width * self.height
        list_dict = [[{}]]
        y = 0
        for x in range(total):
            list_dict[y][x] = {"marked": False, "walls": 0b1111}
            if x == self.width:
                x = 0
                y += 1
        self.list_dict = list_dict
        x, y = [0, 0]
        self.x = x
        self.y = y
        marked = 0
        last_multioption = [[]]
        multioption_count = 0
        while marked != total:
            if x == self.width:
                x = 0
                y += 1
            if list_dict[y][x]["walls"] != 1 or 2 or 4 or 8:
                last_multioption[multioption_count].append = [x, y]
                multioption_count += 1
            choice = self.Random()
            if choice == "Error":
                x, y = last_multioption
                choice = self.Random()
            if choice == "N":
                list_dict[y][x]["walls"] = list_dict[y][x]["walls"] - 1
                list_dict[y - 1][x]["walls"] = list_dict[y - 1][x]["walls"] - 4
                y -= 1
            elif choice == "S":
                list_dict[y][x]["walls"] = list_dict[y][x]["walls"] - 4
                list_dict[y + 1][x]["walls"] = list_dict[y + 1][x]["walls"] - 1
                y += 1
            elif choice == "E":
                list_dict[y][x]["walls"] = list_dict[y][x]["walls"] - 2
                list_dict[y][x + 1]["walls"] = list_dict[y][x + 1]["walls"] - 8
                x -= 1
            elif choice == "W":
                list_dict[y][x]["walls"] = list_dict[y][x]["walls"] - 8
                list_dict[y][x - 1]["walls"] = list_dict[y][x - 1]["walls"] - 2
                x += 1
            else:
                [x, y] = last_multioption[multioption_count]
                multioption_count - 1
            if list_dict[y][x]["marked"] is False:
                list_dict[y][x]["marked"] = True
                marked += 1

    def Random(self) -> str:
        choice = []
        x = self.x
        y = self.y
        if x > 0 and self.list_dict[y][x - 1]["marked"] is False:
            choice.append("E")
        if x < self.width - 1 and self.list_dict[y][x + 1]["marked"] is False:
            choice.append("W")
        if y > 0 and self.list_dict[y - 1][x]["marked"] is False:
            choice.append("N")
        if y < self.height - 1 and self.list_dict[y + 1][x]["marked"] is False:
            choice.append("S")
        try:
            choice = random.choice(choice)
        except IndexError:
            return "Error"
        return choice


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