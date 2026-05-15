import sys
import random


class maze():
    def __init__(self, dic):
        self.height = int(dic.get("HEIGHT"))
        self.width = int(dic.get("WIDTH"))
        self.perfect = str(dic.get("PERFECT"))
        self.entry = tuple(int(v) for v in dic.get("ENTRY").split(","))
        self.exit = tuple(int(v) for v in dic.get("EXIT").split(","))
        if dic.get("SEED") != "0":
            random.seed(dic.get("SEED"))
        else:
            random.seed()

    def write_hex(self, filename="maze.txt"):
        with open(filename, "w") as f:
            for row in self.list_dict:
                line = ""
                for cell in row:
                    line += format(cell["walls"], "X")
                f.write(line + "\n")
    
    def logostamp(self):
        placeable = False
        for y in range(self.height):
            for x in range(self.width):
                placeable = self.hardlogo(x, y)
                if placeable:
                    break
            if placeable:
                break
        if not placeable:
            print("42error: No available space to place 42")
        else:
            for n in self.fortytwo:
                xtmp, ytmp = n
                self.list_dict[ytmp][xtmp]["marked"] = True
        return self.list_dict

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

        for loc in fortytwo:
            lx, ly = loc
            if not (0 <= lx < self.width and 0 <= ly < self.height):
                return False
            if list(loc) == list(self.entry) or list(loc) == list(self.exit):
                return False
        return True

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
        list_dict = self.logostamp()
        while marked != total:
            if list_dict[y][x]["walls"] not in (1, 2, 4, 8):
                last_multioption.append([x, y])
            self.x = x
            self.y = y
            print(x, y)
            choice = self.Random()
            while choice == "Error":
                if last_multioption:

                    x, y = last_multioption.pop()
                    self.x = x
                    self.y = y
                    choice = self.Random()
                if choice == "Error":
                    continue
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
            if not list_dict[y][x]["marked"]:
                list_dict[y][x]["marked"] = True
                marked += 1
        print(marked)
        return list_dict

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
        if choice == []:
            return "Error"
        choice = random.choice(choice)
        return choice


if __name__ == "__main__":
    try:
        name = sys.argv
        dic = dict()
        with open(name[1]) as file1:
            info = file1.read()
            tmp = info.split("\n")
            for i in tmp:
                if '=' in i:
                    key, inp = i.split('=', 1)
                    dic.update({key: inp})
        m = maze(dic)
        m.maze_gen()
        m.write_hex("maze.txt")
    except FileNotFoundError:
        print("File not found")
