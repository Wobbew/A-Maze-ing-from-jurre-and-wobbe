import sys
from typing import Dict, Tuple

from mazegen import MazeGenerator
from visual import tmp_name
from visual import ascii_output


def parse_config(path: str) -> Dict[str, str]:
    """Read KEY=VALUE lines from path into a dict.

    Ignore comments and blank lines.
    """
    d: Dict[str, str] = {}
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            d[key.strip()] = val.strip()
    return d


def parse_bool(val: str) -> bool:
    """Parse a boolean-like string into a bool.

    Recognises true/1/y/yes on (case-insensitive).
    """
    if isinstance(val, bool):
        return val
    if val is None:
        raise ValueError("Missing boolean value")
    v = val.strip().lower()
    return v in ("1", "true", "t", "y", "yes")


def parse_coord(text: str) -> Tuple[int, int]:
    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coord: {text}")
    return (int(parts[0].strip()), int(parts[1].strip()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(2)

    cfg_path = sys.argv[1]
    try:
        dic = parse_config(cfg_path)
    except FileNotFoundError:
        print("File not found")
        sys.exit(2)

    # Required keys
    required = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")
    missing = [k for k in required if k not in dic]
    if missing:
        print("Missing config keys:", ", ".join(missing))
        sys.exit(2)

    try:
        width = int(dic["WIDTH"])
        height = int(dic["HEIGHT"])
        entry = parse_coord(dic["ENTRY"])
        exit_coord = parse_coord(dic["EXIT"])
        perfect = parse_bool(dic["PERFECT"]) if "PERFECT" in dic else False
        seed = dic.get("SEED", "0")
        output_file = dic["OUTPUT_FILE"]
    except ValueError as e:
        print(f"Config parse error: {e}")
        sys.exit(2)

    try:
        print("Generating maze...")
        m = MazeGenerator(height, width, perfect, entry, exit_coord, seed)
        m.maze_gen()
        m.write_hex(output_file)
        route = m.solve()
        with open(output_file, "a") as f:
            f.write("\n" + ", ".join(str(int(v)) for v in entry))
            f.write("\n" + ", ".join(str(int(v)) for v in exit_coord))
            f.write("\n" + "".join(route))
        print("Maze generated and written to", output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        message, X, Y = tmp_name()
        ascii_output(message, X, Y, dic)
    except Exception as e:
        print(f"Visualisation failed: {e}")
