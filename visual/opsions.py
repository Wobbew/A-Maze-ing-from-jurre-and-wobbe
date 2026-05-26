import threading
import os
from mazegen import MazeGenerator
from .render_3d import render_3d
from .path_3d import render_path
from .parser import parser
from .printing_ascii import printing_path, tmp_name
from mlx import Mlx

mlx = Mlx()
ptr = mlx.mlx_init()
KEY_ESCAPE = 65307
needs_redraw = [True]
path_is = ["on", False, None]
maze_name = "maze"
colors = {
    "white":   0xFFFFFF,
    "red":     0x0000FF,
    "green":   0x00FF00,
    "blue":    0xFF0000,
    "yellow":  0xFFFF00,
    "cyan":    0x00FFFF,
    "magenta": 0xFF00FF,
    "gray":    0xAAAAAA,
}


def ascii_uitput(message, sizeX, sizeY, dic):
    line_height = 15
    chr_weight = 10
    window = mlx.mlx_new_window(ptr, sizeX * chr_weight, sizeY * line_height,
                                maze_name)
    maze, entry, exit_pos, path = parser()
    exit_pos = exit_pos.split(",")
    exit_posX, exit_posY = int(exit_pos[0]), int(exit_pos[1])
    entry = entry.split(",")
    entryX, entryY = int(entry[0]), int(entry[1])
    color = [0xFFFFFF, 0x0000FF]

    def render(param):
        if not needs_redraw[0]:
            return
        needs_redraw[0] = False

        mlx.mlx_clear_window(ptr, window)
        for _ in range(2):
            for i, row in enumerate(message):
                line = "".join(str(cell) for cell in row)
                mlx.mlx_string_put(ptr, window, 0, i * line_height, color[0],
                                   line)
        mlx.mlx_string_put(ptr, window, ((entryX * 2) + 1) * chr_weight, (
            (entryY * 2) + 1) * line_height, color[1], "S")

        mlx.mlx_string_put(ptr, window, ((exit_posX * 2) + 1) * chr_weight, (
            (exit_posY * 2) + 1) * line_height, color[1], "E")

        if path_is[1]:
            for _ in range(2):
                for i, row in enumerate(path_is[2]):
                    line = "".join(str(cell) for cell in row)
                    mlx.mlx_string_put(ptr, window, 0, i * line_height,
                                       color[1], line)

    mlx.mlx_loop_hook(ptr, render, None)

    t = threading.Thread(target=mlx.mlx_loop, args=(ptr,), daemon=True)
    t.start()

    color_names = list(colors.keys())
    while t.is_alive():
        os.system("clear")
        i = input("1 to Exit\n"
                  "2 to change color\n"
                  f"3 to turn show path {path_is[0]}\n"
                  "4 to Enter the 3d environment\n"
                  "5 to Enter the path environment\n"
                  "6 to Generate a new maze\n"
                  "Enter: ")
        if i == "1":
            mlx.mlx_loop_exit(ptr)
            break
        if i == "2":
            while True:
                j = input(
                        "1. white\n"
                        "2. red\n"
                        "3. green\n"
                        "4. blue\n"
                        "5. yellow\n"
                        "6. cyan\n"
                        "7. magenta\n"
                        "8. gray\n"
                        "Enter: ")
                if not j.isdigit() or int(j) not in range(
                                                1, len(color_names) + 1):
                    print(f"{j} is not a valid option")
                else:
                    color[0] = colors[color_names[int(j) - 1]]
                    color[1] = colors[color_names[int(j) % len(color_names)]]
                    needs_redraw[0] = True
                    break
        if i == "3":
            if path_is[1]:
                path_is[1] = False
                path_is[0] = "on"
            else:
                path_is[1] = True
                path_is[0] = "off"
            maze, entry, exit_pos, path = parser()
            path_is[2] = printing_path(maze, entry, exit_pos, path)
            needs_redraw[0] = True
        if i == "4":
            render_3d(maze, entry, exit_pos)
        if i == "5":
            render_path(path, entry, exit_pos, maze)
        if i == "6":
            m = MazeGenerator(
                    int(dic.get("HEIGHT")),
                    int(dic.get("WIDTH")), str(dic.get("PERFECT")),
                    tuple(int(v) for v in dic.get("ENTRY").split(",")),
                    tuple(int(v) for v in dic.get("EXIT").split(",")),
                    dic.get("SEED")
                )
            m.maze_gen()
            m.write_hex("maze.txt")
            route = m.solve()
            with open("maze.txt", "a") as f:
                f.write("\n" + ", ".join(str(int(v))
                        for v in dic.get("ENTRY").split(",")))
                f.write("\n" + ", ".join(str(int(v))
                        for v in dic.get("EXIT").split(",")))
                f.write("\n" + "".join(route))
            message, X, Y = tmp_name()
            if path_is[1]:
                maze, entry, exit_pos, path = parser()
                path_is[2] = printing_path(maze, entry, exit_pos, path)
            needs_redraw[0] = True