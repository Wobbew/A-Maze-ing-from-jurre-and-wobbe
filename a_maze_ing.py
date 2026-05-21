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
                self.marked += 1
        return self.marked

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
        x, y = self.entry
        self.x = x
        self.y = y
        marked = 0
        self.marked = marked
        last_multioption = []
        marked = self.logostamp()
        while marked != total:
            if list_dict[y][x]["walls"] not in (1, 2, 4, 8):
                last_multioption.append([x, y])
            self.x = x
            self.y = y
            choice = self.Random()
            while choice == "Error":
                if last_multioption:
                    x, y = last_multioption.pop()
                    self.x = x
                    self.y = y
                    choice = self.Random()
                while choice == "Error" and not last_multioption:
                    for i in range(self.height):
                        for j in range(self.width):
                            if list_dict[i][j]["marked"] and \
                                list_dict[i][j]["walls"] not in (1, 2, 4, 8):
                                last_multioption.append([j, i])
                    if not last_multioption:
                        print("Error: No more options available")
                        return list_dict
                    x, y = last_multioption.pop()
                    self.x = x
                    self.y = y
                    choice = self.Random()
            if choice == "N":
                list_dict[y][x]["walls"] &= ~0b0001
                list_dict[y - 1][x]["walls"] &= ~0b0100
                y -= 1
            elif choice == "S":
                list_dict[y][x]["walls"] &= ~0b0100
                list_dict[y + 1][x]["walls"] &= ~0b0001
                y += 1
            elif choice == "E":
                list_dict[y][x]["walls"] &= ~0b0010
                list_dict[y][x + 1]["walls"] &= ~0b1000
                x += 1
            elif choice == "W":
                list_dict[y][x]["walls"] &= ~0b1000
                list_dict[y][x - 1]["walls"] &= ~0b0010
                x -= 1
            if not list_dict[y][x]["marked"]:
                list_dict[y][x]["marked"] = True
                marked += 1
        print(marked)
        self.list_dict = list_dict
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

    def solve(self) -> list:
        loc_route = []
        route = []
        location = self.entry
        self.checked = [self.entry]
        while location != self.exit:
            choice = self.choice(location)
            while choice is None:
                if loc_route:
                    location = loc_route.pop()
                    route.pop()
                    choice = self.choice(location)
                else:
                    print("Error: No more options available")
                    return []
            if choice == "N":
                location = (location[0], location[1] - 1)
            elif choice == "S":
                location = (location[0], location[1] + 1)
            elif choice == "E":
                location = (location[0] + 1, location[1])
            elif choice == "W":
                location = (location[0] - 1, location[1])
            loc_route.append(location)
            route.append(choice)
            self.checked.append(location)
        return route

    def choice(self, location):
        x, y = location
        options = []
        if self.list_dict[y][x]["walls"] & 0b0001 == 0 \
                and (x, y - 1) not in self.checked:
            options.append("N")
        if self.list_dict[y][x]["walls"] & 0b0010 == 0 \
                and (x + 1, y) not in self.checked:
            options.append("E")
        if self.list_dict[y][x]["walls"] & 0b0100 == 0 \
                and (x, y + 1) not in self.checked:
            options.append("S")
        if self.list_dict[y][x]["walls"] & 0b1000 == 0 \
                and (x - 1, y) not in self.checked:
            options.append("W")
        choice = random.choice(options) if options else None
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
        route = m.solve()
        with open("maze.txt", "a") as f:
            f.write("\n" + ", ".join(str(int(v))
                    for v in dic.get("ENTRY").split(",")))
            f.write("\n" + ", ".join(str(int(v))
                    for v in dic.get("EXIT").split(",")))
            f.write("\n" + "".join(route))
    except FileNotFoundError:
        print("File not found")
