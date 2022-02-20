"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import requests
import os
import sys

from tributors.utils.file import write_json
from .base import ParserBase
from tributors.main.orcid import get_orcid

bot = logging.getLogger("    zenodo")


class ZenodoParser(ParserBase):

    name = "zenodo"

    def __init__(self, filename=None, repo=None, params=None, **kwargs):
        filename = filename or ".zenodo.json"
        super().__init__(filename, repo, params)

    def load_data(self):
        """A shared function to load the zenodo file, if data is not defined"""
        return self._load_data("--zenodo-file")

    @property
    def email_lookup(self):
        """Return loaded metadata as an email lookup."""
        self.load_data()
        return {x["email"]: x for x in self.data.get("creators", []) if "email" in x}

    @property
    def orcid_lookup(self):
        """Return loaded metadata as an orcid lookup."""
        self.load_data()
        return {x["orcid"]: x for x in self.data.get("creators", []) if "orcid" in x}

    def init(self, force=False, from_resources=None, save=True):
        """Generate an empty .zenodo.json if it doesn't exist"""
        from_resources = from_resources or {}
        doi = self.params.get("--doi")

        # Zenodo file defaults to expected .zenodo.json
        zenodo_file = self.params.get("--zenodo-file", self.filename)
        if os.path.exists(zenodo_file) and not force:
            sys.exit("%s exists, set --force to overwrite." % zenodo_file)

        bot.info("Generating %s" % zenodo_file)

        # If a doi is provided, generate
        record = None
        self.data["creators"] = []
        if doi:
            record = get_zenodo_record(doi)
            self.data["creators"] = record["metadata"].get("creators", [])

        self.update_cache(update_lookup=False)

        # Update zenodo file from GitHub logins (default) or other
        self.update_from_logins(from_resources.get("login", []))
        self.update_from_orcids(from_resources.get("orcid", []))
        self.update_from_names(from_resources.get("name", []))
        self.update_from_emails(from_resources.get("email", []))

        # Update final metadata
        metadata = {
            "creators": self.data["creators"],
            "upload_type": "software",
            "keywords": self.repo.topics(),
        }

        # If we have a zenodo record, update it
        if record:
            metadata["upload_type"] = record["metadata"]["resource_type"]["type"]
            metadata["keywords"] = self.repo.topics(record["metadata"]["keywords"])
            metadata["access_right"] = record["metadata"]["access_right"]
            metadata["license"] = record["metadata"]["license"]["id"]

        if save:
            write_json(metadata, zenodo_file)
        return metadata

    def update_from_orcids(self, orcids):
        """Given a list of orcids, update the contributor file from it"""
        lookup = {x["orcid"]: x for _, x in self.cache.items() if "orcid" in x}
        for orcid in orcids:
            if orcid in self.orcid_lookup:
                continue
            entry = {"orcid": orcid}
            if orcid in lookup:
                for field in ["name", "affiliation", "orcid"]:
                    if field in lookup[orcid] and field not in entry:
                        entry[field] = lookup[orcid][field]
            if entry and entry not in self.data["creators"]:
                self.data["creators"].append(entry)
        return self.data["creators"]

    def update_orcids(self):
        """Zenodo is a special case that has emails and real usernames, so we
        can parse through the existing file and look for orcid identifiers
        """
        interactive = self.params.get("--interactive", False)
        creators = []
        for user in self.data.get("creators", []):
            orcid = user.get("orcid")
            name = user.get("name")
            email = user.get("email")
            if orcid is not None:
                creators.append(user)
                continue
            if email or name:
                orcid = get_orcid(
                    email=email, name=name.strip(), interactive=interactive
                )
                if orcid:
                    user["orcid"] = orcid
            creators.append(user)
        self.data["creators"] = creators

    def update_from_emails(self, emails):
        """Given a list of emails, update the contributor file from it. We also
        look for new orcid ids for emails that don't have them.
        """
        # First loop through emails in the cache
        lookup = {x["email"]: x for _, x in self.cache.items() if "email" in x}
        for email in emails:
            if email in self.email_lookup:
                continue
            entry = {}
            for field in ["name", "affiliation", "orcid"]:
                if email in lookup and field in lookup[email]:
                    entry[field] = lookup[email][field]
            if entry and entry not in self.data["creators"]:
                self.data["creators"].append(entry)
        return self.data["creators"]

    def update_from_logins(self, logins):
        """Given a list of logins, update the zenodo.json from it. We only
        do this on init when we haven't added /updated logins with
        people's actual names.
        """
        # GitHub contributors are the source of truth
        for login in logins:

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            orcid = cache.get("orcid")
            email = cache.get("email")

            # Make sure we don't have already
            if (orcid and orcid in self.orcid_lookup) or (
                email and email in self.email_lookup
            ):
                continue

            entry = {"name": cache.get("name") or login}
            if login in self.cache:
                for field in ["name", "affiliation", "orcid"]:
                    if field in self.cache[login]:
                        entry[field] = self.cache[login][field]
            if "orcid" in cache and "orcid" not in entry:
                entry["orcid"] = cache["orcid"]
            if "affiliation" in cache and "affiliation" not in entry:
                entry["affilitation"] = cache["affiliation"]

            # Don't add duplicates
            if entry not in self.data["creators"]:
                self.data["creators"].append(entry)
        return self.data["creators"]

    def update(self, thresh=1, from_resources=None, save=True):
        """Given an existing .zenodo.json file, update it with contributors
        from an allcontributors file.
        """
        from_resources = from_resources or {}
        self.thresh = thresh
        self.load_data()
        bot.info("Updating %s" % self.filename)

        self.update_cache()

        # Here we can only reasonable update from orcids (not logins)
        self.update_orcids()
        self.update_from_emails(from_resources.get("email", []))
        self.update_from_orcids(from_resources.get("orcid", []))
        self.update_from_names(from_resources.get("names", []))
        if save:
            write_json(self.data, self.filename)
        return self.data

    def update_lookup(self):
        """Each client optionally has it's own function to update the cache.
        In the case of zenodo, we aren't necessarily aware of GitHub
        login (the current mapping mechanism) so we cannot update the
        cache yet. When orcid is added this might be an option.
        """
        self.load_data()
        bot.info(f"Updating .tributors cache from {self.filename}")

        # We have to update based on orcid
        lookup = {}
        for entry in self.data.get("creators", []):
            if "orcid" in entry:
                lookup[entry["orcid"]] = entry

        # Now loop through cache
        for login, cache in self.cache.items():
            if "orcid" in cache and cache["orcid"] in lookup:
                for field in ["name", "affiliation"]:
                    if field in lookup[cache["orcid"]] and field not in cache:
                        value = lookup[cache]["orcid"][field]
                        bot.info(f"   Updating {login} with {field}: {value}")
                        cache[field] = value


def get_zenodo_record(doi):
    """Given a doi, retrieve a record using the Zenodo API"""
    # Get the record number from the doi
    record = doi.split("/")[-1].replace("zenodo.", "")
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        response = requests.get(
            "https://zenodo.org/api/records/%s" % record,
            json={"access_token": token},
        )
    else:
        response = requests.get("https://zenodo.org/api/records/%s" % record)

    # Successful query!
    if response.status_code != 200:
        sys.exit(
            "Response %s: %s, cannot retrieve zenodo %s."
            % (response.status_code, response.reason, doi)
        )
    return response.json()
