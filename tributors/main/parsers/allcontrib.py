#!/usr/bin/env python3

"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import os
import sys

from tributors.main.github import GitHubRepository
from tributors.utils.file import write_json
from .base import ParserBase

bot = logging.getLogger("allcontrib")


class AllContribParser(ParserBase):

    name = "allcontrib"

    # https://allcontributors.org/docs/en/emoji-key
    contribution_types = [
        "audio",
        "ally",
        "bug",
        "blog",
        "business",
        "code",
        "content",
        "data",
        "doc",
        "design",
        "example",
        "eventOrganizing",
        "financial",
        "fundingFinding",
        "ideas",
        "infra",
        "maintenance",
        "platform",
        "plugin",
        "projectManagement",
        "question",
        "review",
        "security",
        "tool",
        "translation",
        "test",
        "tutorial",
        "talk",
        "userTesting",
        "video",
    ]

    def __init__(self, filename=None, repo=None, params=None):
        filename = filename or ".all-contributorsrc"
        self.extras = []
        super().__init__(filename, repo, params)

    def load_data(self):
        return self._load_data("--allcontrib-file")

    @property
    def login_lookup(self):
        self.load_data()
        return {
            x["login"]: x for x in self.data.get("contributors", []) if "login" in x
        }

    @property
    def name_lookup(self):
        """Return loaded metadata as an name lookup."""
        self.load_data()
        return {x["name"]: x for x in self.data.get("contributors", []) if "name" in x}

    def init(self, force=False, from_resources=None, save=True):
        """Given an allcontributors file (we default to the one expected) and
        a preference to force, write the empty file to the repository.
        If the file exists and force is false, exit on error. If the user
        has not provided a full repository name and it's not in the environment,
        also exit on error

        Arguments:
         - repo (str)     : the full name of the repository on GitHub
         - force (bool)   : if the contributors file exists, overwrite
         - filename (str) : default filename to write to.
        """
        filename = self.params.get("--allcontrib-file", self.filename)
        if os.path.exists(filename) and not force:
            sys.exit("%s exists, set --force to overwrite." % filename)

        bot.info(f"Generating {filename} for {self.repo.uid}")
        owner, repo = self.repo.uid.split("/")[:2]

        # Write metadata to empty all contributors file.
        metadata = {
            "projectName": repo,
            "projectOwner": owner,
            "repoType": "github",
            "repoHost": "https://github.com",
            "files": ["README.md"],
            "imageSize": 100,
            "commit": True,
            "commitConvention": "none",
            "contributors": [],
            "contributorsPerLine": 7,
        }
        if save:
            write_json(metadata, filename)
        return metadata

    def update(self, thresh=1, from_resources=None, save=True):
        """Given an existing contributors file, use the GitHub API to retrieve
        all contributors, and then use subprocess to update the file
        """
        self.thresh = thresh
        self.load_data()
        from_resources = from_resources or {}

        bot.info(f"Updating {self.filename}")

        # Get optional (or default) contributor type
        ctype = self.params.get("--allcontrib-type", "code")
        if ctype not in self.contribution_types:
            sys.exit(
                f"Invalid contribution type {ctype}. See https://allcontributors.org/docs/en/emoji-key for types."
            )

        # Sanity check that we have the correct repository
        repo = "%s/%s" % (self.data["projectOwner"], self.data["projectName"])

        if repo != self.repo.uid:
            bot.warning(
                f"Found different repository {repo} in {self.filename}, updating from {self.repo.uid}"
            )
            self._repo = GitHubRepository(repo)

        # Update the cache from GitHub, and .tributors lookup
        self.update_cache()

        # Parse over logins, start with existing values
        self.lookup = {
            x["login"]: x for x in self.data.get("contributors", []) if "login" in x
        }
        self.extras = [x for x in self.data.get("contributors", []) if "login" not in x]

        # This client only supports update from names and logins
        self.update_from_logins(from_resources.get("login", []), ctype)
        self.update_from_names(from_resources.get("names", []), ctype)
        self.update_from_orcids(from_resources.get("orcid", []))
        self.update_from_emails(from_resources.get("email", []))

        # Update the contributors
        self.data["contributors"] = list(self.lookup.values()) + self.extras

        if save:
            write_json(self.data, self.filename)
        return self.data

    def update_from_names(self, names, ctype):
        """Given a list of names, update the loaded logins"""
        for name in names:
            if name not in self.name_lookup:
                bot.info(f"⭐️ Found new contributor {name} in {self.filename}")
                entry = {
                    "name": name,
                    "contributions": [ctype],
                }
                self.extras.append(entry)

    def update_from_logins(self, logins, ctype):
        """Given a list of logins, update the loaded logins"""
        for login in logins:

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            if login in self.login_lookup:
                entry = self.login_lookup[login]
            else:
                bot.info(f"⭐️ Found new contributor {login} in {self.filename}")
                entry = {
                    "login": login,
                    "name": cache.get("name") or login,
                    "contributions": [ctype],
                }

            # Only add profile and profile if not added yet
            if "profile" not in entry:
                entry["profile"] = cache.get("blog") or self.repo.contributors.get(
                    login, {}
                ).get("html_url")
            if "avatar_url" not in entry:
                entry["avatar_url"] = (
                    self.repo.contributors.get(login, {}).get("avatar_url"),
                )

            if ctype not in entry["contributions"]:
                entry["contributions"].append(ctype)
            self.lookup[login] = entry

    def update_lookup(self):
        """Each client optionally has it's own function to update the cache.
        In the case of allcontributors, we run this function on update after
        self.lookup is defined with current data. We use this lookup to
        update a shared cache that might be used for other clients. Since
        we also have self.contributors (with GitHub responses) we don't need
        to add items that would be found there.
        """
        self.load_data()
        bot.info(f"Updating .tributors cache from {self.filename}")
        for login, metadata in self.login_lookup.items():
            if login in self.cache:
                entry = self.cache[login]
            else:
                entry = {}
                bot.info(f"⭐️ Found new contributor {login} in {self.filename}")
            if "name" not in entry and "name" in metadata:
                entry["name"] = metadata["name"]
                bot.info(f"   Updating {login} with name: {entry['name']}")
            if "blog" not in entry and "profile" in metadata:
                entry["blog"] = metadata["profile"]
                bot.info(f"   Updating {login} with blog: {entry['blog']}")
            self.cache[login] = entry
