from parser import parser


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
        vis_maze[top+1][left+1] = '+'

    return vis_maze


def place_MLX(walls):
    pass


def tmp_name():
    maze, entry, exit_pos, path = parser()
    HEIGHT = len(maze)
    WIDTH = len(maze[0])
    vis_maze = []
    for _ in range(HEIGHT * 2 + 1):
        row = []
        for _ in range(WIDTH * 2 + 1):
            row.append(" ")
        vis_maze.append(row)

    i = 0
    for i in range(HEIGHT):
        j = 0
        for j in range(WIDTH):
            vis_maze = render_cell(maze[i][j], vis_maze, i, j)
            j = j + 1
        i = i + 1
    return vis_maze, len(vis_maze[0]), len(vis_maze)


def printing_path(maze, entry, exit_pos, path):
    HEIGHT = len(maze)
    WIDTH = len(maze[0])
    vis_path = []
    for _ in range(HEIGHT * 2 + 1):
        row = []
        for _ in range(WIDTH * 2 + 1):
            row.append(" ")
        vis_path.append(row)
    X, Y = int(entry[0])*2+1, int(entry[1])*2+1
    for go_to in path:
        X, Y, vis_path = add_cell(X, Y, go_to, vis_path)
    vis_path[int(exit_pos[1])*2+1][int(exit_pos[0])*2+1] = ' '
    return vis_path


def add_cell(X, Y, go_to, vis_path):
    if go_to == "N":
        vis_path[Y-1][X] = "*"
        vis_path[Y-2][X] = "*"
        return X, Y-2, vis_path
    if go_to == "E":
        vis_path[Y][X+1] = "*"
        vis_path[Y][X+2] = "*"
        return X+2, Y, vis_path
    if go_to == "S":
        vis_path[Y+1][X] = "*"
        vis_path[Y+2][X] = "*"
        return X, Y+2, vis_path
    if go_to == "W":
        vis_path[Y][X-1] = "*"
        vis_path[Y][X-2] = "*"
        return X-2, Y, vis_path
