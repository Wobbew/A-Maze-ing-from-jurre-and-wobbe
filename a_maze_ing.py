import sys
from mazegen import MazeGenerator


if __name__ == "__main__":
    try:
        name = sys.argv
        dic = dict()
        with open(name[1]) as file1:
            info = file1.read()
            tmp = info.split("\n")
            for i in tmp:
                if '=' in i:
                    key, inp = i.split('=', 1)
                    dic.update({key: inp})
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
            f.write(f"\n{m.entry[0]},{m.entry[1]}\n{m.exit[0]},{m.exit[1]}")
            f.write("\n" + "".join(route))
    except FileNotFoundError:
        print("File not found")
