from argparse import ArgumentParser, Namespace
from os import path as _path, getuid

from utils.error import NotEnoughSpace
from utils.conf  import Conf
from utils.func  import rename, rename_preview, check  # noqa: F401

def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-v","--verbose",
        action="store_true",
        help="Verbose mode"
    )
    parser.add_argument(
        "--mount",
        action="store_true"
    )
    parser.add_argument(
        "--umount",
        action="store_true"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continuing recent progresss"
    )

    subparsers = parser.add_subparsers(
        title="Existing commands",
        dest="command"
    )

    padd = subparsers.add_parser("add")
    padd.add_argument(
        "src",
        metavar="source",
        nargs="+",
        help="Location of the folder to be added"
    )
    padd.add_argument(
        "-t","--title",
        metavar="",
    )
    padd.add_argument(
        "-r","--resolution",
        metavar="",
    )
    padd.add_argument(
        "-p","--platform",
        metavar="",
        choices=["TV","BD"],
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

    pedit = subparsers.add_parser("edit")
    pedit.add_argument(
        "-f","--folder",
        metavar="",
    )
    pedit.add_argument(
        "-t","--title",
        metavar="",
    )
    pedit.add_argument(
        "-r","--resolution",
        metavar="",
    )
    pedit.add_argument(
        "-p","--platform",
        metavar="",
        choices=["TV","BD"],
    )

    prename = subparsers.add_parser("rename")
    prename.add_argument(
        "rename",
        metavar="",
        nargs="+",
        help="Manual rename"
    )
    prename.add_argument(
        "--ignore",
        metavar="",
        nargs="+"
    )
    prename.add_argument(
        "-y","--yes",
        action="store_false"
    )
    prename.add_argument(
        "-nra","--not-restrict-access",
        action="store_false",
        dest="restrict_access"
    )
    prename.add_argument(
        "-urf","--use-rename-file",
        action="store_true",
        dest="use_rename_file"
    )

    plog = subparsers.add_parser("log")
    plog.add_argument(
        "-a","--all",
        metavar="",
    )
    plog.add_argument(
        "-c","--clear",
        metavar=""
    )

    pbackup = subparsers.add_parser("backup")
    pbackup.add_argument(
        "select",
        metavar="",
        nargs="+",
        help="You can choose what to back up"
    )

    pconfig = subparsers.add_parser("config")
    pconfig.add_argument(
        "-p","--partition",
        metavar="",
        dest="part"
    )
    pconfig.add_argument(
        "-pl","--partition-label",
        metavar="",
        dest="part_label"
    )
    pconfig.add_argument(
        "-d", "--destination",
        metavar="",
        dest="dest"
    )

    args:Namespace = parser.parse_args()
    print("\n\n",args,sep="",end="\n\n")

    conf = Conf.read()

    if args.umount:
        Conf.umount()
    elif args.mount:
        Conf.mount()

    match args.command:
        case "add":
            
            src     = args.src
            device  = conf["partition"]

            if not Conf.disk_free() > Conf.folder_size(src) + 1024:
                raise NotEnoughSpace
            
            if len(src) == 1:
                folder_name = [i for i in [
                    args.title,
                    args.resolution,
                    args.platform
                ] if i ]

            for src in args.src:
                if args.rename and len(src) < 1:
                    src = rename(src," ".join(folder_name))
                Conf.restrict_access(src)
                if Conf.partition_mountpoint(device=device):
                    Conf.umount(device)
                Conf.mount()
                Conf.sync(src,False)
                Conf.umount(Conf.partition_mountpoint(device=device))
                Conf.mount(True)

        case "rename":                
            for path in args.rename:
                rename(path,ignore=args.ignore,use_rename_file=args.use_rename_file,ver=args.yes)

        case "config":
            if part := args.part:
                if not _path.exists(part):
                    # Partisi tidak ada
                    exit()
                Conf.write(
                    "partition",part
                )
            if dest := args.dest:
                if not _path.exists(dest):
                    # Tujuan tidak ada
                    exit()
                Conf.write(
                    "destination",dest
                )
            
            if not part and not dest:
                print(Conf.read())

if __name__ == "__main__":    
    debug = True
    main()