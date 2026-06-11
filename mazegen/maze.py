import random
from typing import List, Tuple, Dict, Any, Optional, Sequence, Union


class MazeGenerator:
    def __init__(
            self,
            height: int,
            width: int,
            perfect: bool,
            entry: Tuple[int, int],
            exit: Tuple[int, int],
            seed: str) -> None:
        errors = self.verify(height, width, perfect, entry, exit, seed)
        if errors is not None:
            raise ValueError("\n".join(errors))
        self.height = height
        self.width = width
        self.perfect = perfect
        self.entry = entry
        self.exit = exit
        self.error_meg = None
        if seed != "0":
            random.seed(seed)
        else:
            random.seed()

    def verify(
        self,
        height: int,
        width: int,
        perfect: bool,
        entry: Sequence[int] | Tuple[int, int],
        exit: Sequence[int] | Tuple[int, int],
        seed: Union[int, str],
    ) -> Optional[List[str]]:
        errors: List[str] = []

        if not isinstance(height, int) or height <= 0:
            errors.append("height error: must be a positive int")

        if not isinstance(width, int) or width <= 0:
            errors.append("width error: must be a positive int")

        if perfect not in (True, False, "True", "False"):
            errors.append("perfect error: must be True or False")

        if not isinstance(entry, (list, tuple)) or len(entry) != 2:
            errors.append("entry error: must be two ints separated by ','")
        else:
            ex, ey = entry
            if not isinstance(ex, int) or not isinstance(ey, int) \
                    or ex < 0 or ex >= width or ey < 0 or ey >= height:
                errors.append("entry error: coords must be within maze bounds")

        if not isinstance(exit, (list, tuple)) or len(exit) != 2:
            errors.append("exit error: must be two ints separated by ','")
        else:
            lx, ly = exit
            if not isinstance(lx, int) or not isinstance(ly, int) \
                    or lx < 0 or lx >= width or ly < 0 or ly >= height:
                errors.append("exit error: coords must be within maze bounds")

        if not isinstance(seed, (int, str)):
            errors.append("seed error: must be an int or string")

        return errors if errors else None
    
    def write_hex(self, filename: str = "maze.txt") -> None:
        with open(filename, "w") as f:
            for row in self.list_dict:
                line = ""  # type: str
                for cell in row:
                    line += format(cell["walls"], "X")
                f.write(line + "\n")

    def logostamp(self) -> int:
        placeable = False
        for y in range(self.height):
            for x in range(self.width):
                placeable = self.hardlogo(x, y)
                if placeable:
                    break
            if placeable:
                break
        if not placeable:
            self.error_meg = "42error: No available space to place 42"
            self.fortytwo = []
        else:
            for n in self.fortytwo:
                xtmp, ytmp = n
                self.list_dict[ytmp][xtmp]["marked"] = True
                self.marked += 1
        return self.marked

    def hardlogo(self, x: int, y: int) -> bool:
        fortytwo: List[List[int]] = [[x - 3, y - 2],
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
        return self.connected(fortytwo)

    def connected(self, fortytwo: List[List[int]]) -> bool:
        blocked = {(lx, ly) for lx, ly in fortytwo}
        total_open = self.width * self.height - len(blocked)
        start: Tuple[int, int] = (self.entry[0], self.entry[1])
        seen = {start}
        stack = [start]
        while stack:
            cx, cy = stack.pop()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy),
                           (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and (nx, ny) not in blocked \
                        and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        return len(seen) == total_open

    def maze_gen(self) -> List[List[Dict[str, Any]]]:
        total = self.width * self.height
        list_dict: List[List[Dict[str, Any]]] = [[{"marked": False, "walls": 0b1111}
                      for _ in range(self.width)] for _ in range(self.height)]
        self.list_dict = list_dict
        x, y = self.entry
        self.x = x
        self.y = y
        marked = 1
        list_dict[y][x]["marked"] = True
        self.marked = marked
        last_multioption: List[List[int]] = []
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
                            if not list_dict[i][j]["marked"] \
                                    or [j, i] in self.fortytwo:
                                continue
                            if (i > 0 and not list_dict[i - 1][j]["marked"]) \
                                or (i < self.height - 1
                                    and not list_dict[i + 1][j]["marked"]) \
                                or (j > 0
                                    and not list_dict[i][j - 1]["marked"]) \
                                or (j < self.width - 1
                                    and not list_dict[i][j + 1]["marked"]):
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
        self.list_dict = list_dict
        if self.perfect is False or self.perfect == "False":
            self.inperfect()
        return self.list_dict

    def Random(self) -> str:
        choice: List[str] = []
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
        choice_val = random.choice(choice)
        return choice_val

    def solve(self) -> List[List[str]]:
        moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        wall_bits = {"N": 0b0001, "E": 0b0010, "S": 0b0100, "W": 0b1000}
        self.moves = moves
        self.wall_bits = wall_bits
        routes: List[List[str]] = []
        self._explore(self.entry, [self.entry], [], routes)
        if not routes:
            print("Error: No more options available")
        return routes

    def _explore(self, location, loc_route, route, routes) -> None:
        if location == self.exit:
            routes.append(route.copy())
            return
        for direction in self.options(location, loc_route):
            dx, dy = self.moves[direction]
            nxt = (location[0] + dx, location[1] + dy)
            loc_route.append(nxt)
            route.append(direction)
            self._explore(nxt, loc_route, route, routes)
            loc_route.pop()   # backtrack: free the cell for other branches
            route.pop()

    def options(self, location, loc_route) -> List[str]:
        x, y = location
        opts = []
        for direction, (dx, dy) in self.moves.items():
            if self.list_dict[y][x]["walls"] & self.wall_bits[direction] == 0 \
                    and (x + dx, y + dy) not in loc_route:
                opts.append(direction)
        return opts

    def quickest(self) -> list:
        routes = self.solve()
        route = min(routes, key=len)
        return route

    def inperfect(self) -> None:
        dead_ends = []

        def is_dead_end(wall: int) -> bool:
            return wall in (0b1110, 0b1101, 0b1011, 0b0111)

        for y in range(self.height):
            for x in range(self.width):
                cell = self.list_dict[y][x]
                if is_dead_end(cell['walls']):
                    dead_ends.append((x, y))

        random.shuffle(dead_ends)
        remove_walls = max(1, len(dead_ends) // 4)
        logo_cells = {(lx, ly) for lx, ly in self.fortytwo}

        for i in range(remove_walls):
            x, y = dead_ends[i]
            if (x, y) in logo_cells:
                continue
            directions = []
            if y > 0 and self.list_dict[y][x]['walls'] & 0b0001 \
                    and (x, y - 1) not in logo_cells:
                directions.append('N')
            if x < self.width - 1 and self.list_dict[y][x]['walls'] & 0b0010 \
                    and (x + 1, y) not in logo_cells:
                directions.append('E')
            if y < self.height - 1 and self.list_dict[y][x]['walls'] & 0b0100 \
                    and (x, y + 1) not in logo_cells:
                directions.append('S')
            if x > 0 and self.list_dict[y][x]['walls'] & 0b1000 \
                    and (x - 1, y) not in logo_cells:
                directions.append('W')

            if not directions:
                continue

            chosen = random.choice(directions)
            if chosen == 'N':
                self.list_dict[y][x]['walls'] &= ~0b0001
                self.list_dict[y - 1][x]['walls'] &= ~0b0100
            elif chosen == 'E':
                self.list_dict[y][x]['walls'] &= ~0b0010
                self.list_dict[y][x + 1]['walls'] &= ~0b1000
            elif chosen == 'S':
                self.list_dict[y][x]['walls'] &= ~0b0100
                self.list_dict[y + 1][x]['walls'] &= ~0b0001
            elif chosen == 'W':
                self.list_dict[y][x]['walls'] &= ~0b1000
                self.list_dict[y][x - 1]['walls'] &= ~0b0010