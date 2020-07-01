"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .allcontrib import AllContribParser
from .codemeta import CodeMetaParser
from .zenodo import ZenodoParser
import re


def get_named_parser(name, repo=None, filename=None):
    """get a named parser, meaning determining based on name and not uri
    """
    parser = None
    if re.search("(allcontrib|all-contrib)", name):
        parser = AllContribParser(filename, repo)
    elif re.search("zenodo", name):
        parser = ZenodoParser(filename, repo)
    elif re.search("codemeta", name):
        parser = CodeMetaParser(filename, repo)

    if not parser:
        raise NotImplementedError(f"There is no matching parser for {name}")

    return parser
