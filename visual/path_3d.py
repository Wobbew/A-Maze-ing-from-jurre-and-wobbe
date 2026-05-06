import time
from mlx import Mlx
from render_3d import player, tmp_name, clear_images


def render_path(path, entry, maze):
    mlx = Mlx()
    ptr = mlx.mlx_init()
    X, Y = int(entry[0]), int(entry[1])
    p = player(Y, X, "N", maze, mlx, ptr)
    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")

    state = {
        "i": 0, "path": path, "p": p, "window": window,
        "last_time": time.time(), 'delay': 0.3, 'mlx': mlx, 'ptr': ptr
    }

    def loop_hook(param):
        move_step(state)
    mlx.mlx_loop_hook(ptr, loop_hook, None)

    tmp_name(p, window, mlx, ptr)
    mlx.mlx_loop(ptr)
    clear_images()


def move_step(state):
    if time.time() - state["last_time"] < state["delay"]:
        return
    state["last_time"] = time.time()

    path = state["path"]
    i = state["i"]
    p = state["p"]
    window = state["window"]
    mlx = state["mlx"]
    ptr = state["ptr"]

    if i >= len(path):
        mlx.mlx_destroy_window(ptr, window)
        mlx.mlx_loop_exit(ptr)
        return

    facing = path[i]

    if p.facing != facing:
        p.facing = facing
    else:
        p.move(window)
        state["i"] += 1

    tmp_name(p, window, mlx, ptr)
