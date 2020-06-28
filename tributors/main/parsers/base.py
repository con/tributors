"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main.github import get_contributors, get_user
from tributors.main.orcid import get_orcid


class ParserBase:
    """A parser base exists to provide structure to init and update contributor
       configuration files.
    """

    name = "base"

    def __init__(self, filename=None, repo=None):
        """initialize a new contributor parser.
        """
        self.filename = filename
        self._repo = repo
        self.cache = {}
        self.contributors = {}
        self.thresh = 1
        self.orcid_token = None

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

    def update_cache(self, contributors=None):
        """A shared function to get updated GitHub contributors to update
           the local cache. This is where we parse all the data that we need 
           and return common fields that some given parser might need.
           For users that have an email, we can attempt lookup with Orcid. 
        """
        # This updates GitHub contributors, without parsing
        self.contributors = contributors or get_contributors(self.repo)

        for login, contributor in self.contributors.items():

            # If they don't meet the threshold, continue
            if contributor["contributions"] < self.thresh:
                continue

            # Skip GitHub bots
            if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
                continue

            # Look up a GitHub username, possibly email and site
            user = get_user(login)

            entry = {"name": user.get("name") or login}
            if login in self.cache:
                entry = self.cache[login]

            # Update cache with fields that aren't defined yet
            for key in ["email", "bio", "blog"]:
                if user.get(key) and key not in entry:
                    entry[key] = user.get(key)

            # If we have an email, and orcid isn't defined
            orcid = get_orcid(entry.get("email"), self.orcid_token, entry.get("name"))
            if orcid:
                entry["orcid"] = orcid
            self.cache[login] = entry

        # If the parser has it's own function to update cache, use it
        if hasattr(self, "_update_cache"):
            self._update_cache()
