import sys
import random


class maze():
    def __init__(self, dic):
        self.height = int(dic.get("HEIGHT"))
        self.width = int(dic.get("WIDTH"))
        self.perfect = str(dic.get("PERFECT"))
        self.entry = tuple(dic.get("ENTRY"))
        self.exit = tuple(dic.get("EXIT"))
        if dic.get("SEED") != "0":
            self.seed = random.seed(dic.get("SEED"))
        else:
            self.seed = random.seed()

    def maze_gen(self):
        total = self.width * self.height
        list_dict = [[{"marked": False, "walls": 0b1111}
                      for _ in range(self.width)] for _ in range(self.height)]
        self.list_dict = list_dict
        x, y = 0, 0
        self.x = x
        self.y = y
        marked = 0
        last_multioption = []
        multioption_count = 0
        while marked != total:
            if list_dict[y][x]["walls"] not in (1, 2, 4, 8):
                last_multioption.append([x, y])
                multioption_count += 1
            self.x = x
            self.y = y
            choice = self.Random()
            if choice == "Error":
                if last_multioption:
                    x, y = last_multioption[-1]
                choice = self.Random()
            if choice == "N":
                list_dict[y][x]["walls"] &= ~0b1000
                list_dict[y - 1][x]["walls"] &= ~0b0100
                y -= 1
            elif choice == "S":
                list_dict[y][x]["walls"] &= ~0b0100
                list_dict[y + 1][x]["walls"] &= ~0b1000
                y += 1
            elif choice == "E":
                list_dict[y][x]["walls"] &= ~0b0010
                list_dict[y][x + 1]["walls"] &= ~0b0001
                x += 1
            elif choice == "W":
                list_dict[y][x]["walls"] &= ~0b0001
                list_dict[y][x - 1]["walls"] &= ~0b0010
                x -= 1
            else:
                if last_multioption:
                    [x, y] = last_multioption[multioption_count - 1]
                multioption_count -= 1
            if not list_dict[y][x]["marked"]:
                list_dict[y][x]["marked"] = True
                marked += 1

    def logostamp(self):
        placeble = False
        for y in range(self.height):
            for x in range(self.width):
                placeble = self.hardlogo(x, y)
                if placeble:
                    break
        if not placeble:
            print("42error: No available space to place 42")
        else:
            for n in self.fortytwo:
                xtmp, ytmp = n
                self.list_dict[xtmp][ytmp]["marked"] = True

    def hardlogo(self, x, y) -> bool:
        fortytwo = [[x - 3, y - 2],
                    [x - 3, y - 1],
                    [x - 3, y],
                    [x - 2, y],
                    [x - 1, y],
                    [x - 1, y + 1],
                    [x - 1, y + 2],
                    [x + 1, y - 2],
                    [x + 2, y - 2],
                    [x + 3, y - 2],
                    [x + 3, y - 1],
                    [x + 3, y],
                    [x + 2, y],
                    [x + 1, y],
                    [x + 1, y + 1],
                    [x + 1, y + 2],
                    [x + 2, y + 2],
                    [x + 3, y + 2]]
        self.fortytwo = fortytwo
        possible = True
        for loc in fortytwo:
            if loc == self.entry or self.exit:
                possible = False
            if not possible:
                return False
        return True

    def Random(self) -> str:
        choice = []
        x = self.x
        y = self.y
        if x > 0 and self.list_dict[y][x - 1]["marked"] is False:
            choice.append("W")
        if x < self.width - 1 and self.list_dict[y][x + 1]["marked"] is False:
            choice.append("E")
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
        name = sys.argv
        dic = dict()
        with open(name[1]) as file:
            info = file.read()
            tmp = info.split("\n")
            for i in tmp:
                if '=' in i:
                    key, inp = i.split('=')
                    dic.update({key: inp})
        m = maze(dic)
        m.maze_gen()
    except FileNotFoundError:
        print("File not found")
