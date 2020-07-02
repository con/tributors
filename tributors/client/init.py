"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main import TributorsClient
from .utils import parse_extra
import logging
import sys

bot = logging.getLogger("github")


def main(args, extra):

    client = TributorsClient(skip_cache=args.skip_cache)

    # Parse extra arguments
    extra = parse_extra(extra)

    # Tell the user to init a particular parser
    if "unset" in args.parsers:
        bot.info("Please specify one or more parsers, one of zenodo, codemeta")
        sys.exit(0)

    if "all" in args.parsers:
        client.init(
            parsers=["zenodo", "allcontrib"],
            repo=args.repo,
            params=extra,
            force=args.force,
        )

    else:
        parsers = [x for x in args.parsers if x != "unset"]
        client.init(parsers=parsers, repo=args.repo, params=extra, force=args.force)
