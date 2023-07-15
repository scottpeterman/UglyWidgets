import time
import os


def tail_f(file):
    file.seek(0, os.SEEK_END)

    while True:
        line = file.readline()
        if not line:
            time.sleep(1)  # Sleep briefly to avoid excessive CPU use
            print("sleeping..")
            continue
        yield line


def main():
    with open("file.txt", "r") as file:
        lines = tail_f(file)
        for line in lines:
            print(line, end="")


if __name__ == "__main__":
    main()
