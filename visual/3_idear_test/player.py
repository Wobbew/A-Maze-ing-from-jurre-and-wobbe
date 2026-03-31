from mlx import Mlx

class player():
    def __init__(self, Y, X, facing, maze):
        self.Y =Y
        self.X=X
        self.facing = facing
        self.maze = maze

    def  find_view(self):
        if self.facing == "N":
            self.view_N()

    def view_N(self, max_depth=3):
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

for depth in reversed(range(len(view))):
    left, front, right = view[depth]

    if left:
        draw_left(depth)
        #need to place left wall for good place

    if right:
        draw_right(depth)
        #need to place righr wall for good place

    if front:
        draw_front(depth)