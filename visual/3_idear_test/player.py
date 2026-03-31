from mlx import Mlx

class player:
    def __init__(self, Y, X, facing, maze):
        self.Y =Y
        self.X=X
        self.facing = facing
        self.maze = maze

    def find_view(self, max_depth=3):
        if self.facing == "N":
            return self.view_N(max_depth)

    def view_N(self, max_depth):
        view = []

        for depth in range(1, max_depth + 1):
            y = self.Y + depth
            x = self.X

            front = self.get_wall(y, x, 1)

            right = self.get_wall(y, x, 2)

            left = self.get_wall(y, x, 4)

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
    view = player.view_N()


def render(player):
    view = player.find_view()

    for depth in reversed(range(len(view))):
        left, front, right = view[depth]

        if front:
            draw_front(depth)

        if left:
            draw_left_wall(depth)
#need to place left wall for good place

        if right:
            draw_right(depth)
            #need to place righr wall for good place


def draw_left_wall(player, depth, max_depth = 3, wall):
    if depth == 3:
        if wall:
            pass
    if depth == 2:
        if wall:
            pass
    if depth == 1:
        if wall:
            pass
    if not wall:
        if depth < max_depth:
            if depth + 1 < max_depth:
                if player.get_wall(player.Y + depth, player.X - 1, 1):
                    pass
                else:
                    if depth + 2 < max_depth:
                        if player.get_wall(player.Y + depth + 1, player.X - 1, 4):
            


def start(maze, X =1, Y = 1, facing ="N"):
    player = player(Y, X, facing, maze)
