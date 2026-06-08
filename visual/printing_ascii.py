from .parser import parser


def render_cell(num, vis_maze, i, j, mode="ascii"):
    walls = [False, False, False, False]
    if num >= 8:
        num -= 8
        walls[3] = True
    if num >= 4:
        num -= 4
        walls[2] = True
    if num >= 2:
        num -= 2
        walls[1] = True
    if num >= 1:
        num -= 1
        walls[0] = True
    if mode == "ascii":
        vis_maze = place_ascii(walls, vis_maze, i, j)
    return vis_maze


def place_ascii(walls, vis_maze, i, j):
    left = j * 2
    right = j * 2 + 2
    top = i * 2
    bottom = i * 2 + 2
    if walls[0]:
        for k in range(3):
            if vis_maze[top][left + k] != '+':
                vis_maze[top][left + k] = '-'
    if walls[2]:
        for k in range(3):
            if vis_maze[bottom][left + k] != '+':
                vis_maze[bottom][left + k] = '-'
    if walls[3]:
        for k in range(3):
            if vis_maze[top + k][left] != '+':
                vis_maze[top + k][left] = '|'
    if walls[1]:
        for k in range(3):
            if vis_maze[top + k][right] != '+':
                vis_maze[top + k][right] = '|'
    if walls[0] and walls[3]:
        vis_maze[top][left] = '+'
    if walls[0] and walls[1]:
        vis_maze[top][right] = '+'
    if walls[2] and walls[3]:
        vis_maze[bottom][left] = '+'
    if walls[2] and walls[1]:
        vis_maze[bottom][right] = '+'
    if walls[0] and walls[1] and walls[2] and walls[3]:
        vis_maze[top + 1][left + 1] = '+'
    return vis_maze


def place_mlx(walls):
    pass


def tmp_name():
    maze, entry, exit_pos, path = parser()
    height = len(maze)
    width = len(maze[0])
    vis_maze = [[" "] * (width * 2 + 1) for _ in range(height * 2 + 1)]
    for i in range(height):
        for j in range(width):
            vis_maze = render_cell(maze[i][j], vis_maze, i, j)
    return vis_maze, len(vis_maze[0]), len(vis_maze)


def printing_path(maze, entry, exit_pos, path):
    if isinstance(entry, str):
        entry = entry.split(",")
    if isinstance(exit_pos, str):
        exit_pos = exit_pos.split(",")
    height = len(maze)
    width = len(maze[0])
    vis_path = [[" "] * (width * 2 + 1) for _ in range(height * 2 + 1)]
    x, y = int(entry[0]) * 2 + 1, int(entry[1]) * 2 + 1
    vis_path[y][x] = "*"
    for go_to in path:
        x, y, vis_path = add_cell(x, y, go_to, vis_path)
    vis_path[int(exit_pos[1]) * 2 + 1][int(exit_pos[0]) * 2 + 1] = ' '
    return vis_path


def add_cell(x, y, go_to, vis_path):
    max_row = len(vis_path) - 1
    max_col = len(vis_path[0]) - 1
    if go_to == "N":
        if y - 1 >= 0:
            vis_path[y - 1][x] = "*"
        if y - 2 >= 0:
            vis_path[y - 2][x] = "*"
        return x, max(y - 2, 0), vis_path
    if go_to == "E":
        if x + 1 <= max_col:
            vis_path[y][x + 1] = "*"
        if x + 2 <= max_col:
            vis_path[y][x + 2] = "*"
        return min(x + 2, max_col), y, vis_path
    if go_to == "S":
        if y + 1 <= max_row:
            vis_path[y + 1][x] = "*"
        if y + 2 <= max_row:
            vis_path[y + 2][x] = "*"
        return x, min(y + 2, max_row), vis_path
    if go_to == "W":
        if x - 1 >= 0:
            vis_path[y][x - 1] = "*"
        if x - 2 >= 0:
            vis_path[y][x - 2] = "*"
        return max(x - 2, 0), y, vis_path
