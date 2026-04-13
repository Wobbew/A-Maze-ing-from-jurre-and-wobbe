
def parser():
    maze = []
    entry = None
    exit_pos = None
    path = None
    with open("maze.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                break
            row = []
            for c in line:
                row.append(int(c, 16))
            maze.append(row)
        entry = file.readline().strip()
        exit_pos = file.readline().strip()
        path = file.readline().strip()
    return maze, entry, exit_pos, path
