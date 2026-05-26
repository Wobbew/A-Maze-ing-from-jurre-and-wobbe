from printing_ascii import tmp_name
from visual.opsions import ascii_uitput


def main():
    message, X, Y = tmp_name()
    ascii_uitput(message, X, Y)


main()
