from argparse import ArgumentParser, Namespace

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
        "--partition",
    )

    pconfig.add_argument(
        "-d", "--destination",
    )

    plog = subparsers.add_parser("log")
    plog.add_argument(
        "-a","--all"
    )

    args:Namespace = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()