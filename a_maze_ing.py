import sys
from mazegen import MazeGenerator
from visual import tmp_name
from visual import ascii_uitput

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
            f.write("\n" + ", ".join(str(int(v))
                    for v in dic.get("ENTRY").split(",")))
            f.write("\n" + ", ".join(str(int(v))
                    for v in dic.get("EXIT").split(",")))
            f.write("\n" + "".join(route))
    except FileNotFoundError:
        print("File not found")
    message, X, Y = tmp_name()
    ascii_uitput(message, X, Y, dic)
