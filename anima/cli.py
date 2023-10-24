from argparse import ArgumentParser, Namespace
from os import path as _path

from utils.conf import Conf
from utils.text import Messege as Msg

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-v","--verbose",
        metavar="",
        help="Verbose mode"
    )

    parser.add_argument(
        "--resume",
        metavar="",
        help="Continuing recent progresss"
    )


    subparsers = parser.add_subparsers(
        title="Existing commands"
    )
    subparsers.required = True

    padd = subparsers.add_parser("add")
    padd.add_argument(
        "src",
        metavar="source",
        help="Location of the folder to be added"
    )

    pconfig = subparsers.add_parser("config")
    pconfig.add_argument(
        "-p","--partition",
        metavar="",
        dest="part"
    )

    pconfig.add_argument(
        "-d", "--destination",
        metavar="",
        dest="dest"
    )

    plog = subparsers.add_parser("log")
    plog.add_argument(
        "-a","--all"
    )

    pbackup = subparsers.add_parser("backup")
    pbackup.add_argument(
        "select",
        help="You can choose what to back up"
    )

    args:Namespace = parser.parse_args()
    print(args)

    # if args.part:
    #     if not _path.exists(args.part):
    #         print(args.part,Msg.FileFolderNotFound)
    #         exit()
    #     Conf.write(
    #         "partition",args.part
    #     )
    # if args.dest:
    #     if not _path.exists(args.dest):
    #         print(f"{args.dest} - {Msg.FileFolderNotFound}")
    #         exit()
    #     Conf.write(
    #         "destination",args.dest
    #         )


if __name__ == "__main__":
    main()