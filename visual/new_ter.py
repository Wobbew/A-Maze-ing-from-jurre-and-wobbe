import subprocess
import time
import threading

color = "gray"
running = True
def open_terminal(message = "testing",):
    global color
    return subprocess.Popen([
        "xterm", "-T", "Output",
        "-fg",  color,
        "-e", f'echo "{message}"; stty -echo; sleep infinity'
    ])


proc = open_terminal()


def keep_alive():
    global proc
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
            i = int(input("1 = black\n2 = white\n3 = red\n4 = green\n5 = blue\n6 =yellow\n7 = cyan\n8 = magenta\n9 = gray\nEnter:"))
            if i not in range(10):
                print(f"{i} is not a faled opion")
            else:
                color = colors[i - 1]
                proc.terminate()
                break