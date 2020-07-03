"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main.parsers import get_named_parser
from tributors.utils.file import write_json, read_json
from .orcid import get_orcid_token
from .github import GitHubRepository
import logging
import os

bot = logging.getLogger("tributors.main")


class TributorsClient:
    """The tributors client is the handler to interact with one or more
       contributor actions. If we do an update for multiple, for example,
       we can cache and re-use the GitHub calls.
    """

    def __init__(self, skip_cache=False):
        """create a tributors client to control one or more updates to
           contribution files. The .tributors cache stores identifiers that
           would need to be looked up, and the client stores a contributors
           cache (from GitHub) that can be used between parser clients.
        """
        if not skip_cache:
            self.load_cache()
        self.skip_cache = skip_cache

    def load_cache(self):
        """load a cache to serve as a lookup for contributors.
           Each parser will use the cache to find common identifiers,
           and update it if necessary. We use the cache as a place to
           store emails / orcid id / username combos. For temporary 
           (GitHub request) caches, we use /tmp.
        """
        self.cache = {}
        if os.path.exists(".tributors"):
            self.cache = read_json(".tributors")

    def save_cache(self):
        """Save the current self.cache to the cache file .tributors in the PWD
        """
        if not self.skip_cache:
            bot.debug("Saving cache to .tributors")
            write_json(self.cache, ".tributors")

    def __str__(self):
        return "[TributorsClient]"

    def __repr__(self):
        return self.__str__()

    def init(self, parsers=None, repo=None, params=None, force=False, skip_users=None):
        """Init one or more contributor parsers. Specifically, this is the
           action that runs the parser.init() to generate some initial file.
        """
        parsers = parsers or []

        # Generate a shared repository object
        repo = GitHubRepository(repo, skip_users)

        for parser in parsers:
            client = get_named_parser(name=parser, repo=repo, params=params)
            client.cache = self.cache
            client.init(force=force)
            self.cache.update(client.cache)

        # Save the cache
        self.save_cache()

    def update_resource(self, resources=None, params=None, skip_users=None):
        """Given one or more resource types (an external file or source of
           metadata) update the .tributors cache lookup
        """
        resources = resources or []
        for name in resources:
            resource = get_named_parser(name=name, params=params)
            resource.cache = self.cache
            resource.update_lookup()

        # Save the cache
        self.save_cache()

    def update(self, parsers=None, repo=None, params=None, thresh=1, skip_users=None):
        """Update one or more contributor parsers. Specifically, this is the
           action that runs the parser.update() after obtaining contributions
           from GitHub or a cache.
        """
        parsers = parsers or []
        self.orcid_token = get_orcid_token()

        # Generate a shared repository object
        repo = GitHubRepository(repo, skip_users=skip_users)

        for parser in parsers:
            client = get_named_parser(name=parser, repo=repo, params=params)
            client.orcid_token = self.orcid_token
            client.cache = self.cache
            client.update(thresh=thresh)
            self.cache.update(client.cache)

        # Save the cache
        self.save_cache()
