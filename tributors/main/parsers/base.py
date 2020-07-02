"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main.github import get_user
from tributors.main.orcid import get_orcid, OrcidIdentifier

import logging

bot = logging.getLogger("tributors")


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

    def include_contributor(self, login):
        """Given a threshold (and preference to not include bots) return a boolean
           to indicate including the contributor or not
        """
        contributor = self.repo.contributors.get(login)

        # If they don't meet the threshold, continue
        if contributor["contributions"] < self.thresh:
            return False

        # Skip GitHub bots
        if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
            return False
        return True

    def update_cache(self):
        """A shared function to get updated GitHub contributors to update
           the local cache. This is where we parse all the data that we need 
           and return common fields that some given parser might need.
           For users that have an email, we can attempt lookup with Orcid. 
        """
        for login, contributor in self.repo.contributors.items():

            # Look up a GitHub username, possibly email and site
            user = get_user(login)

            entry = {"name": user.get("name") or login}
            if login in self.cache:
                entry = self.cache[login]
            else:
                bot.info(f"⭐️ new contributor {login}")

            # Update cache with fields that aren't defined yet
            for key in ["email", "bio", "blog"]:
                if user.get(key) and key not in entry:
                    entry[key] = user.get(key)

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

        # If the parser has it's own function to update cache, use it
        if hasattr(self, "_update_cache"):
            self._update_cache()
