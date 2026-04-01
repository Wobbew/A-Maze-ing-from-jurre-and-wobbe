import subprocess
import new_ter
def parser():
    maze = []
    entry = None
    exit_pos = None
    path = None
    with open("maze.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                break
            row = []
            for c in line:
                row.append(int(c, 16))
            maze.append(row)
        entry = file.readline().strip()
        exit_pos = file.readline().strip()
        path = file.readline().strip()
    return maze, entry, exit_pos, path


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
    else:
        place_MLX(walls)
    return vis_maze


def place_ascii(walls, vis_maze, i, j):
    left = j * 3
    right = j * 3 + 3
    top = i * 2
    bottom = i * 2 + 2

    if walls[0]:
        for k in range(4):
            if vis_maze[top][left + k] != '+':
                vis_maze[top][left + k] = '-'
    if walls[2]:
        for k in range(4):
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
        vis_maze[top+1][left+1] = '■'
        vis_maze[top+1][left+2] = '■'

    return vis_maze


def place_MLX(walls):
    pass


def tmp_name():
    maze, entry, exit_pos, path = parser()
    ascii = True
    HEIGHT = len(maze)
    WIDTH = len(maze[0])
    vis_maze = []
    for _ in range(HEIGHT * 2 + 1):
        row = []
        for _ in range(WIDTH * 3 + 1):
            row.append(" ")
        vis_maze.append(row)

    i = 0
    for i in range(HEIGHT):
        j = 0
        for j in range(WIDTH):
            vis_maze = render_cell(maze[i][j], vis_maze, i, j)
            j = j + 1
        i = i + 1
    if ascii:
        new_ter.ascii_uitput(vis_maze)
        
# tmp_name()