from mlx import Mlx

KEY_ESCAPE = 65307
KEY_W = 119
KEY_A = 97
KEY_D = 100
images = {}


class player:
    def __init__(self, Y, X, facing, maze, mlx=None, ptr=None):
        self.Y = Y
        self.X = X
        self.facing = facing
        self.maze = maze
        self.mlx = mlx
        self.ptr = ptr

    def move(self, window):
        x, y = cells_around(self, 0, 0, 1)
        if self.is_valid((x, y)) and not self.get_wall(cells_around(
                    self, 0, 0, 0), facing_to_bit(self.facing, "F")):
            self.X = x
            self.Y = y
            tmp_name(self, window, self.mlx, self.ptr)
        else:
            print("blocked")

    def view(self, max_depth=3):
        view = []

        for depth in range(1, max_depth+1):
            pos = cells_around(self, 0, 0, depth-1)

            front = self.get_wall(pos, facing_to_bit(self.facing, "F"))
            right = self.get_wall(pos, facing_to_bit(self.facing, "R"))
            left = self.get_wall(pos, facing_to_bit(self.facing, "L"))

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


def tmp_name(p, window, mlx, ptr):
    view = p.view()
    mlx.mlx_clear_window(ptr, window)
    mlx.mlx_put_image_to_window(ptr, window, get_image(
        "images/floor and ceiling.xpm", ptr, mlx), 0, 0)
    print(f"view: {view}\t p {p.maze[p.Y][p.X]}\t{p.facing}")
    for depth in reversed(range(len(view))):
        left, front, right = view[depth]
        print(f"depth={depth} left={left} front={front} right={right}")
        draw_left_wall(p, depth+1, window, mlx, ptr, wall=left)
        draw_right_wall(p, depth+1, window, mlx, ptr, wall=right)
        if front:
            draw_front(depth+1, window, mlx, ptr)


def draw_front(depth, window, mlx, ptr):
    if depth == 3:
        mlx.mlx_put_image_to_window(ptr, window, get_image(
            "images/FWall3.xpm", ptr, mlx), 0, 0)
        print("Fwall3")
    elif depth == 2:
        mlx.mlx_put_image_to_window(ptr, window, get_image(
            "images/FWall2.xpm", ptr, mlx), 0, 0)
    elif depth == 1:
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
            if p.get_wall(cells_around(p, 1, 0, 1),
                          facing_to_bit(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall-1 2.xpm", ptr, mlx), 0, 0)
    elif depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/LWall1.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(cells_around(p, 1, 0, 0),
                          facing_to_bit(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall-1 1.xpm", ptr, mlx), 0, 0)
                print("FWall-1 1.xpm")
            elif p.get_wall(cells_around(p, 1, 0, 1),
                            facing_to_bit(p.facing, "L")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/LWall-1 2.xpm", ptr, mlx), 0, 0)
                print("FWall-1 2.xpm")
            else:
                if p.get_wall(cells_around(p, 2, 0, 1),
                              facing_to_bit(p.facing, "L")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/LWall-2 2.xpm", ptr, mlx), 0, 0)
                    print("LWall-2 2.xpm")
                if p.get_wall(cells_around(p, 2, 0, 1),
                              facing_to_bit(p.facing, "F")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/FWall-2 2.xpm", ptr, mlx), 0, 0)
                    print("FWall-2 2.xpm")


def draw_right_wall(p, depth, window, mlx, ptr, wall=True):
    if depth == 3:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall3.xpm", ptr, mlx), 0, 0)
        else:
            if p.get_wall(cells_around(p, 0, 1, 2),
                          facing_to_bit(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 3.xpm", ptr, mlx), 0, 0)
    if depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall2.xpm", ptr, mlx), 0, 0)
            pass
        else:
            if p.get_wall(cells_around(p, 0, 1, 1),
                          facing_to_bit(p.facing, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 2.xpm", ptr, mlx), 0, 0)
    if depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image(
                "images/RWall1.xpm", ptr, mlx), 0, 0)
            pass
        else:
            if p.get_wall(cells_around(p, 0, 1, 0), facing_to_bit(p.facing,
                                                                  "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                    "images/FWall+1 1.xpm", ptr, mlx), 0, 0)
            elif p.get_wall(cells_around(p, 0, 1, 1), facing_to_bit(p.facing,
                                                                    "R")):
                mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/RWall+1 2.xpm", ptr, mlx), 0, 0)
            else:
                if p.get_wall(cells_around(p, 0, 2, 1), facing_to_bit(p.facing,
                                                                      "R")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image(
                        "images/RWall+2 2.xpm", ptr, mlx), 0, 0)
                if p.get_wall(cells_around(p, 0, 2, 1), facing_to_bit(p.facing,
                                                                      "F")):
                    if p.get_wall(cells_around(p, 0, 0, 1),
                                  facing_to_bit(p.facing, "R")):

                        mlx.mlx_put_image_to_window(ptr, window, get_image(
                            "images/FWall+2 2.xpm", ptr, mlx), 0, 0)
                    else:
                        mlx.mlx_put_image_to_window(ptr, window, get_image(
                            "images/FWall+2 2.xpm", ptr, mlx), 0, 0)


def cells_around(p, to_L: int, to_R: int, to_F: int):
    if p.facing == 'N':
        return (p.X + to_R - to_L, p.Y - to_F)
    if p.facing == 'S':
        return (p.X + to_L - to_R, p.Y + to_F)
    if p.facing == 'E':
        return (p.X + to_F, p.Y + to_R - to_L)
    if p.facing == 'W':
        return (p.X - to_F, p.Y - to_R + to_L)


def facing_to_bit(facing, side):
    mapping = {
        'N': {'F': 1, 'R': 2, 'B': 4, 'L': 8},
        'E': {'F': 2, 'R': 4, 'B': 8, 'L': 1},
        'S': {'F': 4, 'R': 8, 'B': 1, 'L': 2},
        'W': {'F': 8, 'R': 1, 'B': 2, 'L': 4},
    }
    return mapping[facing][side]


def render_3d(maze, entry, facing="N"):
    mlx = Mlx()
    ptr = mlx.mlx_init()
    X, Y = int(entry[0]), int(entry[1])
    p = player(Y, X, facing, maze, mlx, ptr)

    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")

    def on_key(keynum, param):
        if keynum == KEY_ESCAPE:
            mlx.mlx_destroy_window(ptr, window)
            mlx.mlx_loop_exit(ptr)
        if keynum == KEY_W:
            p.move(window)
        if keynum == KEY_A:
            p.turn_left()
            tmp_name(p, window, mlx, ptr)
        if keynum == KEY_D:
            p.turn_right()
            tmp_name(p, window, mlx, ptr)

    mlx.mlx_key_hook(window, on_key, None)
    tmp_name(p, window, mlx, ptr)
    mlx.mlx_loop(ptr)
    clear_images()


def get_image(name, ptr, mlx):
    if name not in images:
        images[name] = mlx.mlx_xpm_file_to_image(ptr, name)[0]
    return images[name]


def clear_images():
    images.clear()
