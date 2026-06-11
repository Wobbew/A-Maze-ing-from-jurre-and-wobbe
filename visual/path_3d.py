import time
from mlx import Mlx
from .render_3d import player, find_walls, clear_images

State = dict[str, object]


def render_path(
    path: list[str],
    entry: str | list[str],
    exit: str | list[str],
    maze: list[list[int]],
) -> None:
    if isinstance(entry, str):
        entry = entry.split(",")
    if isinstance(exit, str):
        exit = exit.split(",")

    mlx = Mlx()
    ptr = mlx.mlx_init()
    X, Y = int(entry[0]), int(entry[1])
    exit_pos: tuple[int, int] = (int(exit[0]), int(exit[1]))
    p = player(Y, X, "N", maze, exit_pos, mlx, ptr)
    window = mlx.mlx_new_window(ptr, 1920, 1080, "test")
    state: State = {
        "i": 0, "path": path, "p": p, "window": window,
        "last_time": time.time(), "delay": 0.3, "mlx": mlx, "ptr": ptr,
    }

    def loop_hook(param: object) -> None:
        move_step(state)

    mlx.mlx_loop_hook(ptr, loop_hook, None)
    find_walls(p, window, mlx, ptr)
    mlx.mlx_loop(ptr)
    clear_images()


def move_step(state: State) -> None:
    last_time = state["last_time"]
    assert isinstance(last_time, float)
    delay = state["delay"]
    assert isinstance(delay, float)
    if time.time() - last_time < delay:
        return
    state["last_time"] = time.time()

    path = state["path"]
    assert isinstance(path, list)
    i = state["i"]
    assert isinstance(i, int)
    p = state["p"]
    assert isinstance(p, player)
    window = state["window"]
    mlx = state["mlx"]
    assert isinstance(mlx, Mlx)
    ptr = state["ptr"]

    if i >= len(path):
        mlx.mlx_destroy_window(ptr, window)
        mlx.mlx_loop_exit(ptr)
        return
    facing = path[i]
    assert isinstance(facing, str)
    if p.facing != facing:
        p.facing = facing
    else:
        p.move(window)
        state["i"] = i + 1
    find_walls(p, window, mlx, ptr)
