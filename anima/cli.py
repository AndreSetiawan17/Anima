from argparse import ArgumentParser, Namespace
from os import path as _path, getuid, rmdir

from utils.text import Messege as Msg
from utils.conf import Conf
from utils.func import rename

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
        # nargs="+",
        help="Location of the folder to be added"
    )
    padd.add_argument(
        "-t","--title",
        metavar="",
        # nargs="+"
    )
    padd.add_argument(
        "-r","--resolution",
        metavar="",
        # nargs="+"
    )
    padd.add_argument(
        "-p","--platform",
        metavar="",
        # nargs="+",
        choices=["TV","BD"],
    )
    padd.add_argument(
        # Clamav
        "-s","--scan",
        action="store_true"
    )
    padd.add_argument(
        "--no-rename",
        dest="rename",
        action="store_false"
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

    pedit = subparsers.add_parser("edit")
    pedit.add_argument(
        "-f","--folder",
        metavar="",
        # nargs="+",
    )
    pedit.add_argument(
        "-t","--title",
        metavar="",
        # nargs="+"
    )
    pedit.add_argument(
        "-r","--resolution",
        metavar="",
        # nargs="+"
    )
    pedit.add_argument(
        "-p","--platform",
        metavar="",
        # nargs="+",
        choices=["TV","BD"],
        default=["TV"]
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


    args:Namespace = parser.parse_args()
    command:str    = args.command
    print(args)

    conf = Conf.read()

    if args.umount:
        Conf.umount()
    if args.mount:
        Conf.mount()
    
    if command == "add":
        if getuid() != 0:
            print(Msg.PermissionError)
            exit()

        src     = args.src
        device  = conf["partition"]

        if not Conf.disk_free() > Conf.folder_size(src):
            print("Not enough space")
            exit()
        
        folder_name = []
        if title:=args.title:
            folder_name.append(title)
        if ress:=args.resolution:
            folder_name.append(ress)
        if plat:=args.platform:
            folder_name.append(plat)

        if args.rename:
            src = rename(src," ".join(folder_name))
        del title,ress,plat
        Conf.manage_permission(src)
        if Conf.partition_mountpoint(device=device):
            Conf.umount(device)
        Conf.mount()
        Conf.sync(src)
        rmdir(src)
        Conf.umount(Conf.partition_mountpoint(device=device))
        Conf.mount(True)


    elif command == "config":
        if part := args.part:
            if not _path.exists(part):
                print(f"{part} - {Msg.FileFolderNotFound}")
                exit()
            Conf.write(
                "partition",part
            )
        if dest := args.dest:
            if not _path.exists(dest):
                print(f"{dest} - {Msg.FileFolderNotFound}")
                exit()
            Conf.write(
                "destination",dest
            )
        
        if not part and not dest:
            print(Conf.read())

if __name__ == "__main__":    
    debug = True    
    main()