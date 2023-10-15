import os

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="Hehe"
    )

    # System command
    parser.add_argument(
        "--set-path",
        nargs=1,
        metavar="",

    )


    # 
    parser.add_argument(
        "-a","--add",
        nargs="+",
        metavar="",
        help="Menambahkan folder yang dipilih pada rak"
    )

    parser.add_argument(
        "-rn","--rename",
        nargs="+",
        metavar="",
        help="Melakukan rename secara manual"
    )

    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    print(os.geteuid())
    exit()
    main()