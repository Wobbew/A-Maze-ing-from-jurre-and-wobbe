from typing import Optional, Sequence, Tuple, List, Union


def verify(
    height: int,
    width: int,
    perfect: bool,
    entry: Sequence[int] | Tuple[int, int],
    exit: Sequence[int] | Tuple[int, int],
    seed: Union[int, str],
) -> Optional[List[str]]:
    errors: List[str] = []

    if not isinstance(height, int) or height <= 0:
        errors.append("height error: must be a positive int")

    if not isinstance(width, int) or width <= 0:
        errors.append("width error: must be a positive int")

    if not isinstance(perfect, bool):
        errors.append("perfect error: must be True or False")

    if not isinstance(entry, (list, tuple)) or len(entry) != 2:
        errors.append("entry error: must be two ints separated by ','")
    else:
        ex, ey = entry
        if not isinstance(ex, int) or not isinstance(ey, int) \
                or ex < 0 or ex >= width or ey < 0 or ey >= height:
            errors.append("entry error: coords must be within maze bounds")

    if not isinstance(exit, (list, tuple)) or len(exit) != 2:
        errors.append("exit error: must be two ints separated by ','")
    else:
        lx, ly = exit
        if not isinstance(lx, int) or not isinstance(ly, int) \
                or lx < 0 or lx >= width or ly < 0 or ly >= height:
            errors.append("exit error: coords must be within maze bounds")

    if not isinstance(seed, (int, str)):
        errors.append("seed error: must be an int or string")

    return errors if errors else None
