"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main.orcid import get_orcid, OrcidIdentifier
from tributors.utils.file import read_json

import logging
import os
import sys

bot = logging.getLogger("tributors")


class ParserBase:
    """A parser base exists to provide structure to init and update contributor
       configuration files.
    """

    name = "base"

    def __init__(self, filename=None, repo=None, params=None):
        """initialize a new contributor parser.
        """
        self.filename = filename
        self._repo = repo
        self.cache = {}
        self.contributors = {}
        self.thresh = 1
        self.orcid_token = None
        self.params = params or {}
        self.data = {}

    def __str__(self):
        if self.filename:
            return "[%s:%s]" % (self.name, self.filename)
        return "[%s]" % (self.name)

    def __repr__(self):
        return self.__str__()

    @property
    def repo(self):
        """after some initial parsing, we can retrieve the name of the GitHub repo
        """
        return self._repo

    def init(self, *args, **kwargs):
        """init a new configuration file
        """
        raise NotImplementedError

    def update(self, *args, **kwargs):
        """update a configuration file
        """
        raise NotImplementedError

    def _load_data(self, fileattr):
        """Load self.filename unless a file attribute is defined
        """
        if not self.data:
            filename = self.params.get(fileattr, self.filename)

            # Ensure codemeta file already exists
            if not os.path.exists(filename):
                sys.exit("%s does not exist" % filename)

            self.data = read_json(filename)
            self.filename = filename
        return self.data

    def include_contributor(self, login):
        """Given a threshold (and preference to not include bots) return a boolean
           to indicate including the contributor or not
        """
        contributor = self.repo.contributors.get(login)

        # if the login is marked to skip
        if login in self.repo.skip_users:
            return False

        # If they don't meet the threshold, continue
        if contributor["contributions"] < self.thresh:
            return False

        # Skip GitHub bots
        if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
            return False
        return True

    def update_cache(self, update_lookup=True):
        """A shared function to run additional parsing on the cache, such
           as adding an orcid id when an email is defined. 
        """
        # If the parser can be used as a resource, use it to update .tributors
        if hasattr(self, "update_lookup") and update_lookup:
            self.update_lookup()

        # Then add an Orcid lookup
        for login, entry in self.cache.items():

            # If we have an email, and orcid isn't defined
            if "orcid" not in entry:
                orcid = get_orcid(
                    entry.get("email"), self.orcid_token, entry.get("name")
                )
                if orcid:
                    entry["orcid"] = orcid
                    cli = OrcidIdentifier(orcid, self.orcid_token)

                    # If we found the record, update metadata
                    if (
                        cli.found
                        and not entry.get("name")
                        or entry.get("name") == login
                    ):
                        entry["name"] = "%s %s" % (cli.firstName, cli.lastName)
                    if cli.affiliation and not entry.get("affiliation"):
                        entry["affiliation"] = cli.affiliation

            self.cache[login] = entry
