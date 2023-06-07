"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import os
import sys

from tributors.utils.file import read_file
from .base import ParserBase

bot = logging.getLogger("   mailmap")


class MailmapParser(ParserBase):
    name = "mailmap"

    def __init__(self, filename=None, params=None, **kwargs):
        filename = filename or ".mailmap"
        super().__init__(filename=filename, params=params)

    def load_data(self):
        """Since mailmap has format Name <email> on each line, we have a custom
        loading function, and we don't ever need to write anything
        """
        if not self.data:
            self.filename = self.params.get("--mailmap-file", self.filename)

            # Ensure codemeta file already exists
            if not os.path.exists(self.filename):
                sys.exit("%s does not exist" % self.filename)

            for line in read_file(self.filename):
                # keep track of the previous name, in case multiple per line
                name = None

                # mailmap line can have more than one entry, split by right >
                for entry in line.strip().split(">"):
                    if not entry:
                        continue
                    new_name, email = map(str.strip, entry.split("<"))
                    # only the first name matters
                    if not name and new_name:
                        name = new_name
                    if not name:
                        raise ValueError(f"Could not figure out name in {line!r}")
                    self.data[email] = {"name": name}
        return self.data

    @property
    def email_lookup(self):
        """Return loaded metadata as an email lookup. In this case, this
        is just the entire data.
        """
        if not hasattr(self, "_email_lookup"):
            self.load_data()
            self._email_lookup = self.data
        return self._email_lookup

    def update_lookup(self):
        """Each client optionally has it's own function to update the cache.
        In the case of zenodo, we aren't necessarily aware of GitHub
        login (the current mapping mechanism) so we cannot update the
        cache yet. When orcid is added this might be an option.
        """
        bot.info(f"Updating .tributors cache from {self.filename}")
        self.load_data()

        # Find matches based on email
        for login, cache in self.cache.items():
            email = cache.get("email")
            if email in self.email_lookup:
                if "name" not in cache:
                    cache["name"] = self.email_lookup[email]["name"]
                    bot.info(f"   Updating {login} with name: {cache['name']}")
