"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main.github import GitHubRepository
from .allcontrib import AllContribParser
from .codemeta import CodeMetaParser
from .zenodo import ZenodoParser
from .mailmap import MailmapParser
import re


def get_named_parser(name, repo=None, filename=None, params=None):
    """get a named parser, meaning determining based on name and not uri.
    Typically a parser is used to update a metadata file and also
    update the shared .tributors cache, but in a few cases (where we don't
    have any metadata file to update) the parser is just used as a resource
    to update the cache.
    """
    if repo and not isinstance(repo, GitHubRepository):
        repo = GitHubRepository(repo)
    parser = None

    # These parsers have contributors files, and used to update .tributors
    if re.search("(allcontrib|all-contrib)", name):
        parser = AllContribParser(filename, repo, params)
    elif re.search("zenodo", name):
        parser = ZenodoParser(filename, repo, params)
    elif re.search("codemeta", name):
        parser = CodeMetaParser(filename, repo, params)

    # These parsers only update .tributors metadata
    elif re.search("mailmap", name):
        parser = MailmapParser(filename=filename, params=params)
    elif re.search("github", name):
        parser = GitHubRepository(repo=repo, params=params)

    if not parser:
        raise NotImplementedError(f"There is no matching parser for {name}")

    return parser
