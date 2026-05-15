from mlx import Mlx

KEY_ESCAPE = 65307
KEY_W = 119
KEY_A = 97
KEY_D = 100
images = {}
end: tuple[int, int] = (0, 0)


class Player:
    def __init__(self, Y, X, facing, maze, exit, mlx=None, ptr=None):
        self.Y = Y
        self.X = X
        self.facing = facing
        self.maze = maze
        self.exit = exit
        self.mlx = mlx
        self.ptr = ptr

    def move(self, window):
        x, y = pos_cells_around(self, 0, 0, 1)
        if self.is_valid((x, y)) and not self.get_wall(pos_cells_around(
                    self, 0, 0, 0), facing_to_bit_mask(self.facing, "F")):
            self.X = x
            self.Y = y
            find_walls(self, window, self.mlx, self.ptr)
        else:
            print("blocked")

    def view(self, max_depth=3):
        view = []

        for depth in range(1, max_depth+1):
            pos = pos_cells_around(self, 0, 0, depth-1)

            front = self.get_wall(pos, facing_to_bit_mask(self.facing, "F"))
            right = self.get_wall(pos, facing_to_bit_mask(self.facing, "R"))
            left = self.get_wall(pos, facing_to_bit_mask(self.facing, "L"))

            view.append((left, front, right))

            if front:
                break

        return view

    def get_wall(self, pos, mask):
        x, y = pos
        if not self.is_valid((y, x)):
            return True
        return bool(self.maze[y][x] & mask)

    def is_valid(self, pos):
        x, y = pos
        if y < 0 or x < 0 or y >= len(self.maze) or x >= len(self.maze[0]):
            return False
        return True

    def turn_left(self):
        order = ['N', 'W', 'S', 'E']
        self.facing = order[(order.index(self.facing) + 1) % 4]

    def turn_right(self):
        order = ['N', 'E', 'S', 'W']
        self.facing = order[(order.index(self.facing) + 1) % 4]


def find_walls(p, window, mlx, ptr):
    view = p.view()
    mlx.mlx_clear_window(ptr, window)
    mlx.mlx_put_image_to_window(ptr, window, get_image(
        "images/floor and ceiling.xpm", ptr, mlx), 0, 0)
    print(f"view: {view}\t p {p.maze[p.Y][p.X]}\t{p.facing}")
    for depth in reversed(range(len(view))):
        left, front, right = view[depth]
        p.is_end(left, front, right, depth+1)
        print(f"depth={depth} left={left} front={front} right={right}")
        draw_left_wall(p, depth+1, window, mlx, ptr, wall=left)
        draw_right_wall(p, depth+1, window, mlx, ptr, wall=right)
        draw_front(p, front, depth+1, window, mlx, ptr)


def draw_front(p, wall, depth, window, mlx, ptr):
    if depth == 3 and wall:
        mlx.mlx_put_image_to_window(ptr, window, get_image(
            "images/FWall3.xpm", ptr, mlx), 0, 0)
    if is_end(pos_cells_around(p, 0, 0, 3), p.exit):
            # mlx.mlx_put_image_to_window(ptr, window, get_image(
            #     "images/Exit3.xpm", ptr, mlx), 0, 0)
            pass
    elif depth == 2 and wall:
        mlx.mlx_put_image_to_window(ptr, window, get_image(
            "images/FWall2.xpm", ptr, mlx), 0, 0)
    if is_end(pos_cells_around(p, 0, 0, 2), p.exit):
        # mlx.mlx_put_image_to_window(ptr, window, get_image(
        #     "images/Exit2.xpm", ptr, mlx), 0, 0)
        pass
    elif depth == 1 and wall:
        mlx.mlx_put_image_to_window(ptr, window, get_image(
            "images/FWall1.xpm", ptr, mlx), 0, 0)
        print("Fwall1")


def draw_left_wall(p, depth, window, mlx, ptr, wall=True,):
    if depth == 3:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/LWall3.xpm", ptr, mlx), 0, 0)
        else:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/FWall-1 3.xpm", ptr, mlx), 0, 0)
    elif depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/LWall2.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(pos_cells_around(p, 1, 0, 1),
                          facing_to_bit_mask(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall-1 2.xpm", ptr, mlx), 0, 0)
            elif is_end(pos_cells_around(p, 1, 0, 2)[0], p.exit):
                # mlx.mlx_put_image_to_window(ptr, window, get_image(
                #     "images/Exit-1 3.xpm", ptr, mlx), 0, 0)
                pass
    elif depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/LWall1.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(pos_cells_around(p, 1, 0, 0),
                          facing_to_bit_mask(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall-1 1.xpm", ptr, mlx), 0, 0)
                print("FWall-1 1.xpm")
            elif p.get_wall(pos_cells_around(p, 1, 0, 1),
                            facing_to_bit_mask(p.facing, "L")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/LWall-1 2.xpm", ptr, mlx), 0, 0)
                print("FWall-1 2.xpm")
            else:
                if p.get_wall(pos_cells_around(p, 2, 0, 1),
                              facing_to_bit_mask(p.facing, "L")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/LWall-2 2.xpm", ptr, mlx), 0, 0)
                    print("LWall-2 2.xpm")
                if p.get_wall(pos_cells_around(p, 2, 0, 1),
                              facing_to_bit_mask(p.facing, "F")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/FWall-2 2.xpm", ptr, mlx), 0, 0)
                    print("FWall-2 2.xpm")


def draw_right_wall(p, depth, window, mlx, ptr, wall=True):
    if depth == 3:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall3.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(pos_cells_around(p, 0, 1, 2),
                          facing_to_bit_mask(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 3.xpm", ptr, mlx), 0, 0)
    if depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall2.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(pos_cells_around(p, 0, 1, 1),
                          facing_to_bit_mask(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 2.xpm", ptr, mlx), 0, 0)
            elif is_end(pos_cells_around(p, 0, 1, 2)[0], p.exit):
                # mlx.mlx_put_image_to_window(ptr, window, get_image(
                #     "images/Exit+1 3.xpm", ptr, mlx), 0, 0)
                pass
    if depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall1.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(pos_cells_around(p, 0, 1, 0), facing_to_bit_mask(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 1.xpm", ptr, mlx), 0, 0)
            elif p.get_wall(pos_cells_around(p, 0, 1, 1), facing_to_bit_mask(p.facing, "R")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/RWall+1 2.xpm", ptr, mlx), 0, 0)
            else:
                if p.get_wall(pos_cells_around(p, 0, 2, 1), facing_to_bit_mask(p.facing, "R")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/RWall+2 2.xpm", ptr, mlx), 0, 0)
                if p.get_wall(pos_cells_around(p, 0, 2, 1), facing_to_bit_mask(p.facing, "F")):
                    if p.get_wall(pos_cells_around(p, 0, 0, 1),
                                  facing_to_bit_mask(p.facing, "R")):

                        mlx.mlx_put_image_to_window(ptr, window, get_image(
                            "images/FWall+2 2.xpm", ptr, mlx), 0, 0)
                    else:
                        mlx.mlx_put_image_to_window(ptr, window, get_image(
                            "images/FWall+2 2.xpm", ptr, mlx), 0, 0)


def pos_cells_around(p, to_L: int, to_R: int, to_F: int):
    if p.facing == 'N':
        return (p.X + to_R - to_L, p.Y - to_F)
    if p.facing == 'S':
        return (p.X + to_L - to_R, p.Y + to_F)
    if p.facing == 'E':
        return (p.X + to_F, p.Y + to_R - to_L)
    if p.facing == 'W':
        return (p.X - to_F, p.Y - to_R + to_L)
    raise ValueError(f"Invalid facing direction: {p.facing}")


def facing_to_bit_mask(facing, side):
    mapping = {
        'N': {'F': 1, 'R': 2, 'B': 4, 'L': 8},
        'E': {'F': 2, 'R': 4, 'B': 8, 'L': 1},
        'S': {'F': 4, 'R': 8, 'B': 1, 'L': 2},
        'W': {'F': 8, 'R': 1, 'B': 2, 'L': 4},
    }
    return mapping[facing][side]


def is_end(pos: tuple[int, int], exit: tuple[int, int]) -> bool:
    if pos == exit:
        return True
    return False


def render_3d(maze, entry, exit, facing="N"):
    mlx = Mlx()
    ptr = mlx.mlx_init()
    X, Y = int(entry[0]), int(entry[1])
    p = Player(Y, X, facing, maze, exit, mlx, ptr)

    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")

    def on_key(keynum, param):
        if keynum == KEY_ESCAPE:
            mlx.mlx_destroy_window(ptr, window)
            mlx.mlx_loop_exit(ptr)
        if keynum == KEY_W:
            p.move(window)
        if keynum == KEY_A:
            p.turn_left()
            find_walls(p, window, mlx, ptr)
        if keynum == KEY_D:
            p.turn_right()
            find_walls(p, window, mlx, ptr)

    mlx.mlx_key_hook(window, on_key, None)
    find_walls(p, window, mlx, ptr)
    mlx.mlx_loop(ptr)
    clear_images()


def get_image(name, ptr, mlx):
    if name not in images:
        images[name] = mlx.mlx_xpm_file_to_image(ptr, name)[0]
    return images[name]


def clear_images():
    images.clear()
