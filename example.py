import random, sys


# 42 logo bitmap: 5 rows x 7 cols
# 1 = logo cell (all walls closed, hex 'f'), 0 = normal maze cell
_LOGO_42 = [
    [0, 1, 1, 0, 1, 1, 1],  # row 0
    [1, 0, 1, 0, 1, 0, 0],  # row 1
    [1, 1, 1, 0, 1, 1, 1],  # row 2
    [0, 0, 1, 0, 0, 0, 1],  # row 3
    [0, 0, 1, 0, 1, 1, 1],  # row 4
]

LOGO_HEIGHT = 5
LOGO_WIDTH  = 7


def make_logo_cells(maze_height: int, maze_width: int) -> set[tuple[int, int]]:
    """
    Return a set of (row, col) cell coordinates that form the '42' logo.

    The logo bitmap is 5 rows x 7 cols and is centred inside the maze.
    Raises ValueError when the maze is too small to fit the logo.
    """
    if maze_height < LOGO_HEIGHT or maze_width < LOGO_WIDTH:
        raise ValueError(
            f"Maze must be at least {LOGO_HEIGHT} rows x {LOGO_WIDTH} cols "
            f"to fit the 42 logo (got {maze_height}x{maze_width})."
        )

    row_offset = (maze_height - LOGO_HEIGHT) // 2
    col_offset = (maze_width  - LOGO_WIDTH)  // 2

    logo_cells: set[tuple[int, int]] = set()
    for r, row in enumerate(_LOGO_42):
        for c, filled in enumerate(row):
            if filled:
                logo_cells.add((row_offset + r, col_offset + c))

    return logo_cells


def output_hex(maze_obj, logo_cells: set[tuple[int, int]]) -> str:
    """
    Return a multi-line string representing the maze as a hex grid.

    Each cell is one hex digit (0-f) based on its wall bitmask:
        bit 3 (8) = North wall
        bit 2 (4) = South wall
        bit 1 (2) = East wall
        bit 0 (1) = West wall

    Logo cells are always rendered as 'f' (0b1111 — all walls closed),
    regardless of whatever wall value they may have been assigned during
    maze generation.  Cells are separated by spaces; rows by newlines.
    """
    rows = []
    for r in range(maze_obj.height):
        row_chars = []
        for c in range(maze_obj.width):
            if (r, c) in logo_cells:
                row_chars.append('f')
            else:
                wall_value = maze_obj.list_dict[r][c]["walls"]
                # Clamp to 0-15 so we always get a single hex digit.
                row_chars.append(format(wall_value & 0xF, 'x'))
        rows.append(' '.join(row_chars))
    return '\n'.join(rows)


class maze():
    def __init__(self, dic):
        self.height = int(dic.get("HEIGHT"))
        self.width  = int(dic.get("WIDTH"))
        self.perfect = str(dic.get("PERFECT"))
        self.entry  = tuple(int(v) for v in dic.get("ENTRY").split(','))
        self.exit   = tuple(int(v) for v in dic.get("EXIT").split(','))
        if dic.get("SEED") != "0":
            random.seed(dic.get("SEED"))
        else:
            random.seed()

    def maze_gen(self):
        total     = self.width * self.height
        list_dict = {}
        for r in range(self.height):
            list_dict[r] = {}
            for c in range(self.width):
                list_dict[r][c] = {"marked": False, "walls": 0b1111}
        self.list_dict = list_dict

        x, y   = 0, 0
        self.x = x
        self.y = y
        marked = 0

        # Stack of cells that had multiple unvisited neighbours at visit time,
        # used for backtracking when the current cell is a dead end.
        backtrack_stack = []

        while marked < total:
            self.x = x
            self.y = y

            choice = self.Random()

            if choice == "Error":
                # Dead end — backtrack to the most recent branching cell.
                if not backtrack_stack:
                    break
                x, y = backtrack_stack.pop()
                continue

            # Record this position for potential backtracking before moving.
            backtrack_stack.append((x, y))

            if choice == "N":
                list_dict[y][x]["walls"]     &= ~0b1000  # remove North wall
                list_dict[y - 1][x]["walls"] &= ~0b0100  # remove South wall of neighbour
                y -= 1
            elif choice == "S":
                list_dict[y][x]["walls"]     &= ~0b0100  # remove South wall
                list_dict[y + 1][x]["walls"] &= ~0b1000  # remove North wall of neighbour
                y += 1
            elif choice == "E":
                list_dict[y][x]["walls"]     &= ~0b0010  # remove East wall
                list_dict[y][x + 1]["walls"] &= ~0b0001  # remove West wall of neighbour
                x += 1
            elif choice == "W":
                list_dict[y][x]["walls"]     &= ~0b0001  # remove West wall
                list_dict[y][x - 1]["walls"] &= ~0b0010  # remove East wall of neighbour
                x -= 1

            if not list_dict[y][x]["marked"]:
                list_dict[y][x]["marked"] = True
                marked += 1

    def Random(self) -> str:
        choice = []
        x = self.x
        y = self.y
        if x > 0 and not self.list_dict[y][x - 1]["marked"]:
            choice.append("W")
        if x < self.width - 1 and not self.list_dict[y][x + 1]["marked"]:
            choice.append("E")
        if y > 0 and not self.list_dict[y - 1][x]["marked"]:
            choice.append("N")
        if y < self.height - 1 and not self.list_dict[y + 1][x]["marked"]:
            choice.append("S")
        if not choice:
            return "Error"
        return random.choice(choice)


if __name__ == "__main__":
    try:
        args = sys.argv
        with open(args[1]) as file:
            dic = {}
            for line in file.read().splitlines():
                if '=' in line:
                    key, inp = line.split('=', 1)
                    dic[key.strip()] = inp.strip()

        m = maze(dic)
        m.maze_gen()

        logo = make_logo_cells(m.height, m.width)
        print(output_hex(m, logo))

    except FileNotFoundError:
        print("File not found")
    except IndexError:
        print("Usage: python a_maze_ing.py <config_file>")