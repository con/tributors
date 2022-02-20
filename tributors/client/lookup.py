"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main import TributorsClient
from .utils import parse_extra
import os
import sys


def main(args, extra):

    client = TributorsClient(skip_cache=args.skip_cache)

    # Parse extra arguments
    extra = parse_extra(extra)

    # Start with user provided parsers
    resources = args.files

    # If unset, try to detect files
    if "unset" in resources:
        lookup = {
            "allcontrib": extra.get("--allcontrib-file", ".all-contributorsrc"),
            "zenodo": extra.get("--zenodo-file", ".zenodo.json"),
            "codemeta": extra.get("--codemeta-file", "codemeta.json"),
            "mailmap": extra.get("--mailmap-file", ".mailmap"),
        }

        resources = []
        for resource, filename in lookup.items():
            if os.path.exists(filename):
                resources.append(resource)

        # Exit if no parsers auto-detected
        if not resources:
            sys.exit("No resources auto-detected. Specify one or more instead?")

    if "all" in resources:
        client.update_resource(
            resources=["zenodo", "allcontrib", "codemeta", "mailmap", "github"],
            params=extra,
        )

    else:
        client.update_resource(resources=resources, params=extra)
