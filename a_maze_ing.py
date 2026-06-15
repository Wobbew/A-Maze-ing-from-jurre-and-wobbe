import sys
from typing import Dict, Tuple

from mazegen import MazeGenerator
from visual import make_canvas
from visual import ascii_output


def parse_config(path: str) -> Dict[str, str]:
    dic: Dict[str, str] = {}
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            if " " in line:
                for part in line.split():
                    if "=" in part:
                        line = part
                        break
            key, val = line.split("=", 1)
            dic[key.strip()] = val.strip()
    return dic


def parse_bool(val: str) -> bool:
    if isinstance(val, bool):
        return val
    if val is None:
        raise ValueError("Missing boolean value")
    v = val.strip().lower()
    return v in ("true",)


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
    required = (
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT", "SEED"
    )
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
        m = MazeGenerator(height, width, perfect, entry, exit_coord, seed)
        m.maze_gen()
        m.write_hex(output_file)
        route = m.quickest()
        with open(output_file, "a") as f:
            f.write("\n" + ",".join(str(int(v)) for v in entry))
            f.write("\n" + ",".join(str(int(v)) for v in exit_coord))
            f.write("\n" + "".join(route))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        message, X, Y = make_canvas()
        ascii_output(message, X, Y, dic, m.error_meg or "")
    except Exception as e:
        print(f"Visualisation failed: {e}")
