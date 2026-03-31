import subprocess
import time
import threading


def ascii_uitput(message):
    color = "gray"
    running = True

    display = "\n".join("".join(str(cell) for cell in row) for row in message)
    
    def open_terminal():
        return subprocess.Popen([
            "xterm", "-T", "Output",
            "-fg",  color,
            "-e", f'echo "{display}"; stty -echo; sleep infinity'
        ])

    proc = open_terminal()

    def keep_alive():
        nonlocal proc
        while running:
            if proc.poll() is not None:
                proc = open_terminal()
            time.sleep(1)

    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()

    while True:
        i = input("1 to Exit: \n2 to chang color:\nEnter:")
        if i == "1":
            running = False
            proc.terminate()
            break
        if i == "2":
            colors = ["black", "white", "red", "green", "blue", "yellow", "cyan", "magenta", "gray"]
            while True:
                i = (input("1 = black\n2 = white\n3 = red\n4 = green\n5 = blue\n6 =yellow\n7 = cyan\n8 = magenta\n9 = gray\nEnter:"))
                if not i.isdigit() or int(i) not in range(1, 10):
                    print(f"{i} is not a faled opion")
                else:
                    color = colors[int(i) - 1]
                    proc.terminate()
                    break

