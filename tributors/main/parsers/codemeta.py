"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import os
import sys

from tributors.utils.file import read_json, write_json
from .base import ParserBase

bot = logging.getLogger("codemeta")


class CodeMetaParser(ParserBase):

    name = "codemeta"

    def __init__(self, filename=None, repo=None, **kwargs):
        filename = filename or "codemeta.json"
        self.data = {}
        super().__init__(filename, repo)

    def init(self, params=None, force=False, contributors=None):
        """Codemeta already has many good generators.
        """
        print(
            "Codemeta provides several tools to generate this for you: https://codemeta.github.io/tools/"
        )

    def update(self, params=None, contributors=None, thresh=1):
        """Given an existing .zenodo.json file, update it with contributors
           from an allcontributors file.
        """
        params = params or {}
        self.thresh = thresh
        filename = params.get("--codemeta-file", self.filename)

        # Ensure codemeta file already exists
        if not os.path.exists(filename):
            sys.exit("%s does not exist" % filename)

        bot.info("Updating %s" % filename)

        # We don't currently have a reliable identifier for zenodo, so we recreate each time
        self.data = read_json(filename)
        self.lookup = self.data.get("contributor", [])
        self.update_cache()

        # Get fields from repo
        self.update_metadata()

        # Keep track of orcids and emails that we've seen
        seen = set()

        # First update current members with emails, orcids in the cache
        for entry in self.lookup:
            email = entry.get("email")
            orcid = entry.get("@id")
            if orcid and "orcid" in orcid:
                orcid = orcid.split("/")[-1]

            # Find matches based on orcid and/or email
            for login, cache in self.cache.items():
                compare_orcid = cache.get("orcid")
                compare_email = cache.get("email")
                seen.add(compare_email)
                seen.add(compare_orcid)

                # We have a match based on orcid or email
                if (compare_orcid and orcid and compare_orcid == orcid) or (
                    compare_email and email and compare_email == email
                ):
                    if (
                        "givenName" not in entry
                        and "familyName" not in entry
                        and "name" in cache
                    ):
                        entry["givenName"] = cache["name"].split(" ")[0]
                        entry["familyName"] = " ".join(cache["name"].split(" ")[1:])
                    if "email" not in entry and "email" in cache:
                        entry["email"] = cache["email"]
                    if "orcid" not in entry and "orcid" in cache:
                        entry["@id"] = "https://orcid.org/%s" % cache["orcid"]
                    break

        # Ensure empty records are not considered seen
        for item in [None, ""]:
            if item in seen:
                seen.remove(item)

        # Now add contributors using cache (new GitHub contributors) with known email or orcid that isn't present
        for login, _ in self.repo.contributors.items():

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            email = cache.get("email")
            orcid = cache.get("orcid")

            # We can only update if we have an email or orcid
            if (email != None or orcid != None) and (
                email not in seen and orcid not in seen
            ):
                entry = {
                    "@type": "Person",
                    "givenName": cache["name"].split(" ")[0],
                    "familyName": " ".join(cache["name"].split(" ")[1:]),
                }
                if email != None:
                    entry["email"] = email
                if orcid != None:
                    entry["@id"] = "https://orcid.org/%s" % orcid
                self.lookup.append(entry)

        self.data["contributor"] = self.lookup
        write_json(self.data, filename)
        return self.data

    def update_metadata(self):
        """Update codemeta metadata from the repository, if we can.
        """
        self.data["keywords"] = self.repo.topics(self.data["keywords"])
        self.data["description"] = self.data.get("description") or self.repo.description
        self.data["codeRepository"] = (
            self.data.get("codeRepository") or self.repo.html_url
        )
        self.data["name"] = self.data.get("name") or self.repo.name
        self.data["issueTracker"] = (
            self.data.get("issueTracker") or self.repo.issues_url
        )
        self.data["license"] = self.data.get("license") or self.repo.license

    def _update_cache(self):
        """We can only keep track of users here based on email addresses or
           orcid, so we can only update the cache for existing users.
        """
        for entry in self.lookup:
            match = False
            email = entry.get("email")
            orcid = entry.get("@id")
            if orcid and "orcid" in orcid:
                orcid = orcid.split("/")[-1]

            # Find matches based on orcid and/or email
            for login, metadata in self.cache.items():
                compare_orcid = metadata.get("orcid")
                compare_email = metadata.get("email")

                # We have a match based on orcid
                if compare_orcid and orcid and compare_orcid == orcid:
                    match = True
                elif compare_email and email and compare_email == email:
                    match = True

                # If we have a match, update records
                if match:
                    if (
                        "name" not in metadata
                        and "givenName" in entry
                        and "familyName" in entry
                    ):
                        metadata["name"] = "%s %s" % (
                            entry["givenName"],
                            entry["familyName"],
                        )
                    if "email" not in metadata:
                        metadata["email"] = email
                    if "orcid" not in metadata:
                        metadata["orcid"] = orcid
                    break
