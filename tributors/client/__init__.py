#!/usr/bin/env python3

"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.logger import LOG_LEVEL, LOG_LEVELS

import tributors
import argparse
import logging
import sys


def get_parser():
    parser = argparse.ArgumentParser(description="Tributors Python Metadata Parser")

    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices=LOG_LEVELS,
        default=LOG_LEVEL,
        help="Customize logging level for a2z parser.",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--skip-cache",
        dest="skip_cache",
        help="Skip loading and saving a .tributors cache file",
        default=False,
        action="store_true",
    )

    description = "actions for tributors"
    subparsers = parser.add_subparsers(
        help="tributors actions",
        title="actions",
        description=description,
        dest="command",
    )

    init = subparsers.add_parser(
        "init", help="Initialize an empty .all-contributorsrc."
    )
    init.add_argument(
        "--force",
        dest="force",
        help="If exists, overwrite existing .all-contributorsrc",
        default=False,
        action="store_true",
    )

    # print version and exit
    subparsers.add_parser("version", help="show software version")

    # Update the .tributors lookup
    update_lookup = subparsers.add_parser(
        "update-lookup",
        help="Update shared .tributors metadata file",
    )
    update_lookup.add_argument(
        "files",
        help="One or more files to use for update.",
        nargs="*",
        default="unset",
        choices=["mailmap", "allcontrib", "codemeta", "zenodo", "unset", "github"],
    )

    # Update an existing contributors file
    update = subparsers.add_parser(
        "update",
        help="Update existing all-contributorsrc",
    )
    update.add_argument(
        "--thresh",
        dest="thresh",
        help="Minimum number of contributions required to add user as contributor",
        default=1,
        type=int,
    )

    for command in [update, init]:
        command.add_argument(
            "--interactive",
            dest="interactive",
            help="Allow interactive selection of orcid ids.",
            default=False,
            action="store_true",
        )
        command.add_argument(
            "parsers",
            help="Metadata file parsers to update or initialize.",
            nargs="*",
            default="unset",
            choices=["zenodo", "allcontrib", "codemeta", "all", "unset"],
        )
        command.add_argument(
            "--repo",
            help="The repository URI, if not exported to GITHUB_REPOSITORY",
        )
        command.add_argument(
            "--skip-users",
            help="GitHub aliases to skip adding to .tributors file",
            dest="skip_users",
            nargs="*",
            default="unset",
        )
        command.add_argument(
            "--from",
            dest="from_resources",
            help="Update records FROM one resource TO another using unique ids (email, orcid, GitHub login)",
            default="unset",
            choices=[
                "unset",
                "tributors",
                "codemeta",
                "zenodo",
                "github",
                "allcontrib",
                "mailmap",
            ],
            nargs="*",
        )

    return parser


def main():
    """main entrypoint for tributors"""

    parser = get_parser()

    def help(return_code=0):
        print("\nTributors Python")
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # Each parser takes extra arguments
    args, extra = parser.parse_known_args()

    # Set the logging level
    logging.basicConfig(level=getattr(logging, args.log_level))
    bot = logging.getLogger("tributors")
    bot.setLevel(getattr(logging, args.log_level))

    # Show the version and exit
    if args.command == "version" or args.version:
        print(tributors.__version__)
        sys.exit(0)

    # Initialize or update one or more configuration files
    if args.command == "init":
        from .init import main
    elif args.command == "update":
        from .update import main
    elif args.command == "update-lookup":
        from .lookup import main
    else:
        help()

    main(args, extra)


if __name__ == "__main__":
    main()
