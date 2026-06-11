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
needs_redraw = [True]
path_is = ["on", False, None]
maze_name = "maze"
window = [None]
line_height = 15
chr_weight = 10
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


def ascii_output(message, sizeX, sizeY, dic):
    # global line_height, chr_weight

    window[0] = mlx.mlx_new_window(
        ptr, sizeX * chr_weight, sizeY * line_height, maze_name
    )
    maze, entry, exit_pos, path = parser()
    exit_pos_parts = exit_pos.split(",")
    exit_posX, exit_posY = int(exit_pos_parts[0]), int(exit_pos_parts[1])
    entry_parts = entry.split(",")
    entryX, entryY = int(entry_parts[0]), int(entry_parts[1])
    color = [0xFFFFFF, 0x0000FF]

    def render(param):
        if not needs_redraw[0]:
            return
        needs_redraw[0] = False

        mlx.mlx_clear_window(ptr, window[0])
        for _ in range(2):
            for idx, row in enumerate(message):
                line = "".join(str(cell) for cell in row)
                mlx.mlx_string_put(
                    ptr, window[0], 0, idx * line_height, color[0], line
                )
        mlx.mlx_string_put(
            ptr, window[0],
            ((entryX * 2) + 1) * chr_weight,
            ((entryY * 2) + 1) * line_height,
            color[1], "S"
        )
        mlx.mlx_string_put(
            ptr, window[0],
            ((exit_posX * 2) + 1) * chr_weight,
            ((exit_posY * 2) + 1) * line_height,
            color[1], "E"
        )

        if path_is[1]:
            for _ in range(2):
                for idx, row in enumerate(path_is[2]):
                    line = "".join(str(cell) for cell in row)
                    mlx.mlx_string_put(
                        ptr, window[0], 0, idx * line_height, color[1], line
                    )

    mlx.mlx_loop_hook(ptr, render, None)

    t = threading.Thread(target=mlx.mlx_loop, args=(ptr,), daemon=True)
    t.start()

    color_names = list(colors.keys())
    while t.is_alive():
        os.system("clear")
        choice = input(
            "1 to Exit\n"
            "2 to change color\n"
            f"3 to turn show path {path_is[0]}\n"
            "4 to Enter the 3d environment\n"
            "5 to Enter the path environment\n"
            "6 to Generate a new maze\n"
            "Enter: "
        )
        if choice == "1":
            mlx.mlx_loop_exit(ptr)
            break
        if choice == "2":
            while True:
                j = input(
                    "1. white\n2. red\n3. green\n4. blue\n"
                    "5. yellow\n6. cyan\n7. magenta\n8. gray\nEnter: "
                )
                if not j.isdigit() or int(j) not in range(
                    1, len(color_names) + 1
                ):
                    print(f"{j} is not a valid option")
                else:
                    color[0] = colors[color_names[int(j) - 1]]
                    color[1] = colors[color_names[int(j) % len(color_names)]]
                    needs_redraw[0] = True
                    break
        if choice == "3":
            path_is[1] = not path_is[1]
            path_is[0] = "off" if path_is[1] else "on"
            maze, entry, exit_pos, path = parser()
            path_is[2] = printing_path(maze, entry, exit_pos, path)
            needs_redraw[0] = True
        if choice == "4":
            render_3d(maze, entry, exit_pos)
        if choice == "5":
            render_path(path, entry, exit_pos, maze)
        if choice == "6":
            mlx.mlx_loop_exit(ptr)
            t.join()
            try:
                if input("want to change the settings (Y/N): ") == "Y":
                    tmp = input(
                        f"current height is {dic.get('HEIGHT')}."
                        " Enter the height: "
                    )
                    if tmp.isdigit():
                        dic["HEIGHT"] = tmp
                    else:
                        print("not a valid input")
                    tmp = input(
                        f"current width is {dic.get('WIDTH')}."
                        " Enter the width: "
                    )
                    if tmp.isdigit():
                        dic["WIDTH"] = tmp
                    else:
                        print("not a valid input")
                    tmp = input(
                        f"current entry is {dic.get('ENTRY')}."
                        " Enter the entry: "
                    )
                    if (
                        tmp.count(",") == 1
                        and all(p.strip().isdigit() for p in tmp.split(","))
                    ):
                        dic["ENTRY"] = tmp
                    else:
                        print(f"{tmp} is not a valid entry point")
                    tmp = input(
                        f"current exit is {dic.get('EXIT')}."
                        " Enter the exit: "
                    )
                    if (
                        tmp.count(",") == 1
                        and all(p.strip().isdigit() for p in tmp.split(","))
                    ):
                        dic["EXIT"] = tmp
                    else:
                        print("not a valid input")
                    if input(
                        f"current perfect is {dic.get('PERFECT')}."
                        " Enter 'Y' to change: "
                    ) == "Y":
                        dic["PERFECT"] = (
                            "False" if dic["PERFECT"] == "True" else "True"
                        )
                    tmp = input(
                        f"current seed is {dic.get('SEED')}, 0 is random."
                        " Enter the seed: "
                    )
                    if tmp.isdigit():
                        dic["SEED"] = tmp
                    else:
                        print("not a valid input")

                perf_raw = dic.get("PERFECT")
                perf_val = (
                    str(perf_raw).strip().lower() in ("true")
                    if perf_raw is not None
                    else False
                )

                m = MazeGenerator(
                    int(dic.get("HEIGHT")),
                    int(dic.get("WIDTH")),
                    perf_val,
                    tuple(int(v) for v in dic.get("ENTRY").split(",")),
                    tuple(int(v) for v in dic.get("EXIT").split(",")),
                    dic.get("SEED"),
                )
                m.maze_gen()
                m.write_hex("maze.txt")
                route = m.quickest()
            except Exception as e:
                print(f"Error occurred: {e}")
                continue

            exit_pos_parts = dic.get("EXIT").split(",")
            exit_posX = int(exit_pos_parts[0])
            exit_posY = int(exit_pos_parts[1])
            entry_parts = dic.get("ENTRY").split(",")
            entryX = int(entry_parts[0])
            entryY = int(entry_parts[1])
            with open("maze.txt", "a") as f:
                f.write(
                    "\n" + ",".join(
                        str(int(v)) for v in dic.get("ENTRY").split(",")
                    )
                )
                f.write(
                    "\n" + ",".join(
                        str(int(v)) for v in dic.get("EXIT").split(",")
                    )
                )
                f.write("\n" + "".join(route))
            message, sizeX, sizeY = tmp_name()
            if path_is[1]:
                maze, entry, exit_pos, path = parser()
                path_is[2] = printing_path(maze, entry, exit_pos, path)
            needs_redraw[0] = True
            mlx.mlx_destroy_window(ptr, window[0])
            window[0] = mlx.mlx_new_window(
                ptr, sizeX * chr_weight, sizeY * line_height, maze_name
            )
            t = threading.Thread(
                target=mlx.mlx_loop, args=(ptr,), daemon=True
            )
            t.start()
