from mlx import Mlx
import printing

KEY_ESCAPE = 65307
KEY_W = 119
KEY_A = 97
KEY_S = 115
KEY_D = 100
mlx = Mlx()
ptr = mlx.mlx_init()


class player:
    def __init__(self, Y, X, facing, maze):
        self.Y = Y
        self.X = X
        self.facing = facing
        self.maze = maze

    def find_view(self, max_depth=3):
        if self.facing == "N":
            return self.view_N(max_depth)

    def view_N(self, max_depth):
        view = []

        for depth in range(1, max_depth + 1):
            y = self.Y - depth + 1
            x = self.X

            front = self.get_wall(y, x, 1)

            right = self.get_wall(y, x, 2)

            left = self.get_wall(y, x, 8)

            view.append((left, front, right))

            if front:
                break

        return view

    def get_wall(self, y, x, mask):
        if not self.is_valid(y, x):
            return True 
        return bool(self.maze[y][x] & mask)

    def is_valid(self, y, x):
        if y < 0 or x < 0 or y >= len(self.maze) or x >= len(self.maze[0]):
            return False
        return True


def tmp_name(p, window):
    view = p.find_view()
    print(f"view: {view}\n p {p.maze[p.Y][p.X]}")  
    for depth in reversed(range(len(view))):
        left, front, right = view[depth]
        print(f"depth={depth} left={left} front={front} right={right}") 
        if front:
            draw_front(depth+1, window)
        draw_left_wall(p, depth+1, window, wall=left)
        draw_right_wall(p, depth+1, window, wall=right)

def draw_front(depth, window):
    if depth == 3:
        mlx.mlx_put_image_to_window(ptr, window, get_image( "images/FWall3.png"), 0, 0)
        print("Fwall3")
    if depth == 2:
        mlx.mlx_put_image_to_window(ptr, window, get_image( "images/FWall2.png"), 0, 0)
    if depth == 1: 
        mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall1.png"), 0, 0)
        print("Fwall1")

def draw_left_wall(p, depth, window, max_depth = 3, wall = True):
    if depth == 3:
        if wall:
            pass
    if depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall2.png"), 0, 0)
    if depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall1.png"), 0, 0)
    # if not wall:
    #     if depth < max_depth:
    #         if depth + 1 < max_depth:
    #             if p.get_wall(p.Y + depth, p.X - 1, 1):
    #                 pass
    #             else:
    #                 if depth + 2 < max_depth:
    #                     if p.get_wall(p.Y + depth + 1, p.X - 1, 4):
    #                         pass


def draw_right_wall(p, depth, window, max_depth=3, wall=True):
    if depth == 3:
        if wall:
            pass
    if depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall2.png"), 0, 0)
        else:
            if p.get_wall(p.Y + depth, p.X - 1, 1):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall+1_2.png"), 0, 0)
    if depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall1.png"), 0, 0)
        else:
            if p.get_wall(p.Y + depth, p.X - 1, 1):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall+1 1.png"), 0, 0)
            elif p.get_wall(p.Y + depth + 1, p.X - 1, 4):
                    mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall+1_2.png"), 0, 0)


def render_3d(maze, X=0, Y=0, facing="N"):
    p = player(Y, X, facing, maze)

    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")

    def on_key(keynum, dummy):
        if keynum == KEY_ESCAPE:  
            mlx.mlx_loop_exit(ptr)

    mlx.mlx_key_hook(window, on_key, None)
    mlx.mlx_put_image_to_window(ptr, window, get_image("images/floor and ceiling.png"), 0, 0)
    tmp_name(p, window)
    mlx.mlx_loop(ptr)


def get_image(name):
    return mlx.mlx_png_file_to_image(ptr, name)[0]
    

maze, entry, exit_pos, path = printing.parser()
render_3d(maze)