"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging

from tributors.utils.file import write_json
from .base import ParserBase

bot = logging.getLogger("  codemeta")


class CodeMetaParser(ParserBase):

    name = "codemeta"

    def __init__(self, filename=None, repo=None, params=None, **kwargs):
        filename = filename or "codemeta.json"
        self.data = {}
        super().__init__(filename, repo, params)

    def init(self, force=False):
        """Codemeta already has many good generators."""
        print(
            "Codemeta provides several tools to generate this for you: https://codemeta.github.io/tools/"
        )

    def load_data(self):
        """If not yet loaded, load data into client"""
        return self._load_data("--codemeta-file")

    def update(self, thresh=1, from_resources=None, save=True):
        """Given an existing .zenodo.json file, update it with contributors
        from an allcontributors file.
        """
        self.thresh = thresh
        self.load_data()

        bot.info("Updating %s" % self.filename)

        # Read in contributors, and update cache (also runs update_lookup)
        self.lookup = self.data.get("contributor", [])
        self.update_cache()

        # Get fields from repo
        self.update_metadata()

        self.update_from_logins(from_resources.get("login", []))
        self.update_from_orcids(from_resources.get("orcid", []))
        self.update_from_names(from_resources.get("name", []))
        self.update_from_emails(from_resources.get("email", []))

        self.data["contributor"] = self.lookup
        if save:
            write_json(self.data, self.filename)
        return self.data

    def update_metadata(self):
        """Update codemeta metadata from the repository, if we can."""
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

    def update_from_emails(self, emails):
        """Update codemeta entries from emails"""
        # Now add contributors using cache (new GitHub contributors) with known email or orcid that isn't present
        for email in emails:
            if email not in self.email_lookup:
                bot.info(f"   Updating with new added email: {email}")
                entry = {"@type": "Person", "email": email}
                self.lookup.append(entry)

    def update_from_logins(self, logins):
        """Update codemeta entries from GitHub logins"""
        # Now add contributors using cache (new GitHub contributors) with known email or orcid that isn't present
        for login in logins:

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            email = cache.get("email")
            orcid = cache.get("orcid")

            # We can only add completely new entries that don't already exist
            if (email != None or orcid != None) and (
                email not in self.email_lookup and orcid not in self.orcid_lookup
            ):
                bot.info(f"   Updating {login}")
                parts = (cache.get("name") or login).split(" ")
                entry = {"@type": "Person", "givenName": parts[0]}

                # Add the last name if it's defined
                if len(parts) > 1:
                    entry["familyName"] = " ".join(parts[1:])

                if email != None:
                    entry["email"] = email
                if orcid != None:
                    entry["@id"] = "https://orcid.org/%s" % orcid
                self.lookup.append(entry)

    @property
    def email_lookup(self):
        """Return loaded metadata as an email lookup"""
        if not hasattr(self, "_email_lookup"):
            self._email_lookup = {}
            self.load_data()
        for entry in self.data.get("contributor", []):
            if "email" in entry:
                self._email_lookup[entry["email"]] = entry
        return self._email_lookup

    @property
    def orcid_lookup(self):
        """Return loaded metadata as an orcid lookup"""
        if not hasattr(self, "_orcid_lookup"):
            self._orcid_lookup = {}
            self.load_data()
            for entry in self.data.get("contributor", []):
                if "@id" in entry:
                    # Orcid represented as full URL but we just want id
                    orcid = entry["@id"].split("/")[-1]
                    self._orcid_lookup[orcid] = entry
        return self._orcid_lookup

    def update_lookup(self):
        """We can only keep track of users here based on email addresses or
        orcid, so we can only update the cache for existing users.
        """
        bot.info(f"Updating .tributors cache from {self.filename}")

        # Find matches based on orcid and/or email
        for login, cache in self.cache.items():
            orcid = cache.get("orcid")
            email = cache.get("email")

            # Case 1: double match (unlikely but possible)
            entry = None
            if email in self.email_lookup and orcid in self.orcid_lookup:

                # If they don't point to the same entry, stop
                if self.email_lookup[email] != self.orcid_lookup[orcid]:
                    bot.warning(
                        "Found email {email} and orcid {orcid} in cache from different entries, skipping."
                    )
                else:
                    entry = self.email_lookup[email]

            # Case 2: We have a matching orcid
            elif orcid in self.orcid_lookup:
                entry = self.orcid_lookup[orcid]

            # Case 2: We have a matching email
            elif email in self.email_lookup:
                entry = self.email_lookup[email]

            # If we have a match (entry is defined) use it to update the record
            if entry is not None:

                # Update the name
                if (
                    "givenName" in entry
                    and "familyName" in entry
                    and "name" not in cache
                ):
                    cache["name"] = "%s %s" % (entry["givenName"], entry["familyName"])
                    bot.info(f"   Updating {login} with name: {cache['name']}")

                # Update the email
                if "email" in entry and "emali" not in cache:
                    cache["email"] = entry["email"]
                    bot.info(f"   Updating {login} with email: {cache['email']}")

                # Update the orcid id
                if "@id" in entry and "orcid" not in cache:
                    cache["orcid"] = entry["@id"].split("/")[-1]
                    bot.info(f"   Updating {login} with orcid: {cache['orcid']}")
