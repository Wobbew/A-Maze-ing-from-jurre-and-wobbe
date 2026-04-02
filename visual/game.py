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

    def view(self, max_depth =4):
        view = []

        for depth in range(1, max_depth + 1):
            pos = cells_around(self, 0, 0, depth-1)

            front = self.get_wall(pos, facing_to_bit(self, "F"))
            right = self.get_wall(pos, facing_to_bit(self, "R"))
            left  = self.get_wall(pos, facing_to_bit(self, "L"))

            view.append((left, front, right))

            if front:
                break

        return view

    def get_wall(self, pos, mask):
        x, y =pos
        if not self.is_valid((y, x)):
            return True 
        return bool(self.maze[y][x] & mask)

    def is_valid(self, pos):
        x, y =pos
        if y < 0 or x < 0 or y >= len(self.maze) or x >= len(self.maze[0]):
            return False
        return True
         
    def move(self, window):
        x, y = cells_around(self, 0, 0, 1)
        print(f"X={x} Y={y}")
        if self.is_valid((x, y)):
            self.X = x
            self.Y = y
            tmp_name(self, window)
            print(self.X, self.Y)
        else:
            print("test")

    def turn_left(self):
        order = ['N', 'W', 'S', 'E']
        self.facing = order[(order.index(self.facing) + 1) % 4]

    def turn_right(self):
        order = ['N', 'E', 'S', 'W']
        self.facing = order[(order.index(self.facing) + 1) % 4]

        

            
            


def tmp_name(p, window):
    view = p.view()
    mlx.mlx_clear_window(ptr, window)
    mlx.mlx_put_image_to_window(ptr, window, get_image("images/floor and ceiling.png"), 0, 0)
    print(f"view: {view}\t p {p.maze[p.Y][p.X]}\t{p.facing}")
    for depth in reversed(range(len(view))):
        left, front, right = view[depth]
        print(f"depth={depth} left={left} front={front} right={right}") 
        draw_left_wall(p, depth+1, window, wall=left)
        draw_right_wall(p, depth+1, window, wall=right)
        if front:
            draw_front(depth+1, window)
        elif depth == 2:
            mlx.mlx_put_image_to_window(ptr, window, get_image( "images2/FNoWall3.png"), 0, 0)

def draw_front(depth, window):
    if depth == 3:
        mlx.mlx_put_image_to_window(ptr, window, get_image( "images/FWall3.png"), 0, 0)
        print("Fwall3")
    elif depth == 2:
        mlx.mlx_put_image_to_window(ptr, window, get_image( "images/FWall2.png"), 0, 0)
    elif depth == 1: 
        mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall1.png"), 0, 0)
        print("Fwall1")
    
    

def draw_left_wall(p, depth, window, max_depth = 4, wall = True):
    if depth == 3:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall3.png"), 0, 0)
    elif depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall2.png"), 0, 0)
        else:
            if p.get_wall(cells_around(p, 1, 0, 1), facing_to_bit(p, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall-1 2.png"), 0, 0)
    elif depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall1.png"), 0, 0)
        else:
            if p.get_wall(cells_around(p, 1, 0, 0), facing_to_bit(p, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall-1 1.png"), 0, 0)
            elif p.get_wall(cells_around(p, 1, 0, 1), facing_to_bit(p, "L")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image("images/LWall-1 2.png"), 0, 0)


    # if not wall:
    #     if depth < max_depth:
    #         if depth + 1 < max_depth:
    #             if p.get_wmlx.mlx_put_image_to_window(ptr, window, get_image("images/floor and ceiling.png"), 0, 0)all(p.Y + depth, p.X - 1, 1):
    #                 pass
    #             else:
    #                 if depth + 2 < max_depth:
    #                     if p.get_wall(p.Y + depth + 1, p.X - 1, 4):
    #                         pass


def draw_right_wall(p, depth, window, max_depth=3, wall=True):
    if depth == 3:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall3.png"), 0, 0)
    if depth == 2:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall2.png"), 0, 0)
        else:
            if p.get_wall(cells_around(p, 0, 1, 1), facing_to_bit(p, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall+1_2.png"), 0, 0)
    if depth == 1:
        if wall:
            mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall1.png"), 0, 0)
        else:
            if p.get_wall(cells_around(p, 0, 1, 0), facing_to_bit(p, "F")):
                mlx.mlx_put_image_to_window(ptr, window, get_image("images/FWall+1 1.png"), 0, 0)
            elif p.get_wall(cells_around(p, 0, 1, 1), facing_to_bit(p, "R")):
                    mlx.mlx_put_image_to_window(ptr, window, get_image("images/RWall+1 2.png"), 0, 0)
def cells_around(p, to_L, to_R, to_F):
    if p.facing == 'N':
        return (p.X + to_R - to_L, p.Y - to_F)
    if p.facing == 'S':
        return (p.X + to_L - to_R, p.Y + to_F)
    if p.facing == 'E':
        return (p.X + to_F, p.Y + to_L - to_R)
    if p.facing == 'W':
        return (p.X - to_F, p.Y + to_R - to_L)
    
def facing_to_bit(p, side):
    mapping = {
        'N': {'F':1, 'R':2, 'B':4, 'L':8},
        'E': {'F':2, 'R':4, 'B':8, 'L':1},
        'S': {'F':4, 'R':8, 'B':1, 'L':2},
        'W': {'F':8, 'R':1, 'B':2, 'L':4},
    }
    return mapping[p.facing][side]
    

def render_3d(maze, X=1, Y=8, facing="N"):
    p = player(Y, X, facing, maze)

    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")

    def on_key(keynum, param):
        if keynum == KEY_ESCAPE:
            mlx.mlx_loop_exit(ptr)
        if keynum == KEY_W:
            p.move(window)
        if keynum == KEY_A:
            p.turn_left()
            tmp_name(p, window)
        if keynum == KEY_D:
            p.turn_right()
            tmp_name(p, window)

    mlx.mlx_key_hook(window, on_key, None)
    tmp_name(p, window)
    mlx.mlx_loop(ptr)


def get_image(name):
    return mlx.mlx_png_file_to_image(ptr, name)[0]
    

maze, entry, exit_pos, path = printing.parser()
render_3d(maze)