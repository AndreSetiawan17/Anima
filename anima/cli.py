#!/var/python3_env/bin/python3

from argparse import ArgumentParser, Namespace
from os import path as _path

from utils.conf import Conf

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-v","--verbose",
        action="store_true",
        help="Verbose mode"
    )
    parser.add_argument(
        "-y","--yes",
        action="store_true"
    )
    # parser.add_argument(
    #     "--mount",
    #     action="store_true"
    # )
    # parser.add_argument(
    #     "--umount",
    #     action="store_true"
    # )
    # parser.add_argument(
    #     "--resume",
    #     action="store_true",
    #     help="Continuing recent progresss"
    # )

    subparsers = parser.add_subparsers(
        title="Existing commands",
        dest="command"
    )

    padd = subparsers.add_parser("add")
    padd.add_argument(
        "source",
        nargs="+",
        help="Location of the folder to be added"
    )
    padd.add_argument(
        "-d","--delete",
        action="store_true",
        help="Delete source files"
    )
    padd.add_argument(
        "-i","--ignore",
        metavar="",
        nargs="+",
        default=[]
    )
    padd.add_argument(
        # Clamav
        "-s","--scan",
        action="store_true"
    )
    padd.add_argument(
        "-nr","--no-rename",
        dest="rename",
        action="store_false"
    )
    padd.add_argument(
        "-nra","--no-restrict-access",
        dest="restrict_access",
        action="store_false"
    )

    prename = subparsers.add_parser("rename")
    prename.add_argument(
        "path",
        metavar="",
        nargs="+",
        help="Manual rename"
    )
    prename.add_argument(
        "--ignore",
        metavar="",
        nargs="+",
        default=[]
    )
    prename.add_argument(
        "-nra","--not-restrict-access",
        action="store_false",
        dest="restrict_access"
    )

    # plog = subparsers.add_parser("log")
    # plog.add_argument(
    #     "-a","--all",
    #     metavar="",
    # )
    # plog.add_argument(
    #     "-c","--clear",
    #     metavar=""
    # )

    # pbackup = subparsers.add_parser("export")
    # pbackup.add_argument(
    #     "select",
    #     metavar="",
    #     nargs="+",
    #     help="You can choose what to back up"
    # )

    pconfig = subparsers.add_parser("config")
    pconfig.add_argument(
        "-p","--partition",
        metavar="",
    )
    pconfig.add_argument(
        "-l", "--location",
        metavar="",
    )
    pconfig.add_argument(
        "-u","--user",
        metavar="",
    )
    pconfig.add_argument(
        "-g","--group",
        metavar="",
    )

    args:Namespace = parser.parse_args()
    print(args,sep="",end="\n\n")

    conf = Conf(verbose=args.verbose)

    match args.command:
        case "add":
            if conf.partition_mountpoint(partition=conf.partition) is False:
                conf.mount()

            paths = []
            for source in args.source:
                if not _path.exists(source):
                    print(f"{source} not found.")
                    continue

                if conf.free < conf.size(source):
                    print(f"[Warning] Cannot copying {source} because not enough space")
                    continue

                path = _path.join(conf.location,source.rstrip("/").split("/")[-1])
                paths.append(path)

                for i in range(3):
                    conf.sync(source,args.delete)

            for path in paths:
                conf.rename(path,args.ignore,args.yes) if args.rename else None
                conf.restrict_access(path) if args.restrict_access else None

        case "rename":
            for path in args.path:
                conf.rename(path)

        case "config":          
            if partition := args.partition:
                conf.partition = partition
            if location := args.location:
                conf.location = location
            if user := args.user:
                conf.user = user
            if group := args.group:
                conf.group = group
            
            print(conf.conf)

if __name__ == "__main__": 
    debug = True
    main()