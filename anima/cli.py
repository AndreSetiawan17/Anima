#!/var/python3_env/bin/python3

from argparse import ArgumentParser, Namespace
from os import path as _path

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
        "-d","--delete",
        action="store_true",
        help="Delete source files"
    )
    padd.add_argument(
        "-i","--ignore",
        metavar="",
        nargs="+"
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

    # pedit = subparsers.add_parser("edit")
    # pedit.add_argument(
    #     "-f","--folder",
    #     metavar="",
    # )
    # pedit.add_argument(
    #     "-t","--title",
    #     metavar="",
    # )
    # pedit.add_argument(
    #     "-r","--resolution",
    #     metavar="",
    # )
    # pedit.add_argument(
    #     "-p","--platform",
    #     metavar="",
    #     choices=["TV","BD"],
    # )

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
        "-d", "--destination",
        metavar="",
        dest="dest"
    )
    pconfig.add_argument(
        "-u","--user",
        metavar="",
        nargs="?",
    )
    pconfig.add_argument(
        "-g","--group",
        metavar="",
        nargs="?",
    )

    args:Namespace = parser.parse_args()
    print(args,sep="",end="\n\n")

    conf = Conf(verbose=args.verbose)

    match args.command:
        case "add":            
            source = args.source
            device = conf["partition"]
            dest   = conf["destination"]

            if dev := conf.partition_mountpoint(device=device):
                conf.umount(dev)
            conf.mount()

            disk_free   = conf.disk_free
            folder_size = sum([conf.folder_size(i) for i in source])

            if disk_free < folder_size + 1024:
                raise OSError(
                    "Not enough space"
                )

            if len(source) == 1:
                folder_name = [i for i in [
                    args.title,
                    args.resolution,
                    args.platform
                ] if i ]
            else:
                folder_name = False  # noqa: F841

            for src in source:
                if not conf.partition_mountpoint(dest,device):
                    conf.umount()
                    conf.mount()

                new_path = _path.join(dest,src.rstrip("/").split("/")[-1])

                conf.sync(src,args.delete)
                if args.rename:
                    new_path = rename(
                        path=new_path,
                        ignore=args.ignore,
                        ver=not args.yes
                    )
                if args.restrict_access:
                    conf.restrict_access(new_path)

            conf.umount(device=device)
            conf.mount(True)

    #     case "rename":                
    #         for path in args.rename:
    #             rename(path,ignore=args.ignore,use_rename_file=args.use_rename_file,ver=args.yes)

        case "config":
            if part := args.part:
                if not _path.exists(part):
                    raise FileNotFoundError(f"{part} not found")
                conf["partition"] = part

            if dest := args.dest:
                if not _path.exists(dest):
                    raise FileNotFoundError(f"{dest} not found")
                conf["destination"] = dest

            if user := args.user:
                conf.user = user
            if group := args.group:
                conf.group = group

            if not part and not dest:
                print(conf.conf)

if __name__ == "__main__": 
    debug = True
    main()