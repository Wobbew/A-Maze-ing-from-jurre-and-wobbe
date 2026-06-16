import threading
import os
from mazegen import MazeGenerator
from .render_3d import render_3d
from .path_3d import render_path
from .parser import parser
from .printing_ascii import printing_path, make_canvas
from mlx import Mlx

VisMaze = list[list[str]]

mlx = Mlx()
ptr = mlx.mlx_init()
needs_redraw: list[bool] = [True]
path_is: list[object] = ["on", False, None]
maze_name = "maze"
window: list[object] = [None]
line_height = 15
chr_weight = 10
colors: dict[str, int] = {
    "white":   0xFFFFFF,
    "red":     0x0000FF,
    "green":   0x00FF00,
    "blue":    0xFF0000,
    "yellow":  0xFFFF00,
    "cyan":    0x00FFFF,
    "magenta": 0xFF00FF,
    "gray":    0xAAAAAA,
}


def ascii_output(
    message: VisMaze,
    sizeX: int,
    sizeY: int,
    dic: dict[str, str],
    error_meg: str,
) -> None:

    window[0] = mlx.mlx_new_window(
        ptr, sizeX * chr_weight, sizeY * line_height, maze_name
    )
    maze, entry, exit_pos, path_str = parser()
    exit_pos_parts = exit_pos.split(",")
    exit_posX, exit_posY = int(exit_pos_parts[0]), int(exit_pos_parts[1])
    entry_parts = entry.split(",")
    entryX, entryY = int(entry_parts[0]), int(entry_parts[1])
    color: list[int] = [0xFFFFFF, 0x0000FF]

    def render(param: object) -> None:
        if not needs_redraw[0]:
            return
        needs_redraw[0] = False

        mlx.mlx_clear_window(ptr, window[0])
        for _ in range(2):
            for i, row in enumerate(message):
                line = "".join(str(cell) for cell in row)
                mlx.mlx_string_put(
                    ptr, window[0], 0, i * line_height, color[0], line
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
            vis: VisMaze = path_is[2]  # type: ignore[assignment]
            for _ in range(2):
                for i, row in enumerate(vis):
                    line = "".join(str(cell) for cell in row)
                    mlx.mlx_string_put(
                        ptr, window[0], 0, i * line_height, color[1], line
                    )

    mlx.mlx_loop_hook(ptr, render, None)

    t = threading.Thread(target=mlx.mlx_loop, args=(ptr,), daemon=True)
    t.start()

    color_names = list(colors.keys())
    while t.is_alive():
        os.system("clear")
        if error_meg:
            print(error_meg)
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
                tmp = input(
                    "1. white\n2. red\n3. green\n4. blue\n"
                    "5. cyan\n6. yellow\n7. magenta\n8. gray\nEnter: "
                )
                if not tmp.isdigit() or int(tmp) not in range(
                    1, len(color_names) + 1
                ):
                    print(f"{tmp} is not a valid option")
                else:
                    color[0] = colors[color_names[int(tmp) - 1]]
                    color[1] = colors[color_names[int(tmp) % len(color_names)]]
                    needs_redraw[0] = True
                    break
        if choice == "3":
            path_is[1] = not path_is[1]
            path_is[0] = "off" if path_is[1] else "on"
            maze, entry, exit_pos, path_str = parser()
            path_is[2] = printing_path(
                maze, entry, exit_pos, list(path_str)
            )
            needs_redraw[0] = True
        if choice == "4":
            render_3d(maze, entry, exit_pos)
        if choice == "5":
            render_path(list(path_str), entry, exit_pos, maze)
        if choice == "6":
            mlx.mlx_loop_exit(ptr)
            t.join()
            try:
                if input("want to change the settings (y): ") == "y":
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
                        " Enter 'y' to change: "
                    ) == "y":
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

                entry_xy: tuple[int, int] = (
                    int(dic["ENTRY"].split(",")[0]),
                    int(dic["ENTRY"].split(",")[1]),
                )
                exit_xy: tuple[int, int] = (
                    int(dic["EXIT"].split(",")[0]),
                    int(dic["EXIT"].split(",")[1]),
                )
                seed = dic.get("SEED") or "0"
                m = MazeGenerator(
                    int(dic["HEIGHT"]),
                    int(dic["WIDTH"]),
                    str(dic.get("PERFECT")),
                    entry_xy,
                    exit_xy,
                    seed,
                )
                m.maze_gen()
                m.write_hex("maze.txt")
                route = m.quickest()
                error_meg = m.error_meg or ""
            except Exception as e:
                print(f"Error occurred: {e}")
                continue

            exit_pos_parts = dic["EXIT"].split(",")
            exit_posX = int(exit_pos_parts[0])
            exit_posY = int(exit_pos_parts[1])
            entry_parts = dic["ENTRY"].split(",")
            entryX = int(entry_parts[0])
            entryY = int(entry_parts[1])
            with open("maze.txt", "a") as f:
                f.write(
                    "\n" + ",".join(
                        str(int(v)) for v in dic["ENTRY"].split(",")
                    )
                )
                f.write(
                    "\n" + ",".join(
                        str(int(v)) for v in dic["EXIT"].split(",")
                    )
                )
                f.write("\n" + "".join(route))
            message, sizeX, sizeY = make_canvas()
            if path_is[1]:
                maze, entry, exit_pos, path_str = parser()
                path_is[2] = printing_path(
                    maze, entry, exit_pos, list(path_str)
                )
            needs_redraw[0] = True
            mlx.mlx_destroy_window(ptr, window[0])
            window[0] = mlx.mlx_new_window(
                ptr, sizeX * chr_weight, sizeY * line_height, maze_name
            )
            t = threading.Thread(
                target=mlx.mlx_loop, args=(ptr,), daemon=True
            )
            t.start()
