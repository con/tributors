"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import sys


def parse_extra(extra):
    """Given a list of extra arguments, parse for known"""
    known_single = [
        "--zenodo-file",
        "--doi",
        "--allcontrib-type",
        "--allcontrib-file",
        "--codemeta-file",
        "--mailmap-file",
        "--skip-users",
    ]
    known_bool = []

    # Parse extra arguments, all are pairs
    kwargs = {}

    while extra:
        arg = extra.pop(0)
        if arg in known_single:
            if not extra:
                sys.exit(f"Argument {arg} requires a value.")
            kwargs[arg] = extra.pop(0)
        elif arg in known_bool:
            kwargs[arg] = True
    return kwargs
