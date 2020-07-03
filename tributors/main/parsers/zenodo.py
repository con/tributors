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

bot = logging.getLogger("    zenodo")


class ZenodoParser(ParserBase):

    name = "zenodo"

    def __init__(self, filename=None, repo=None, params=None, **kwargs):
        filename = filename or ".zenodo.json"
        super().__init__(filename, repo, params)

    def load_data(self):
        """A shared function to load the zenodo file, if data is not defined
        """
        return self._load_data("--zenodo-file")

    def init(self, force=False):
        """Generate an empty .zenodo.json if it doesn't exist
        """
        # A doi is required
        doi = self.params.get("--doi")
        if not doi:
            sys.exit("Please provide the zenodo doi with --doi")

        # Zenodo file defaults to expected .zenodo.json
        zenodo_file = self.params.get("--zenodo-file", self.filename)
        if os.path.exists(zenodo_file) and not force:
            sys.exit("%s exists, set --force to overwrite." % zenodo_file)

        bot.info("Generating %s" % zenodo_file)
        record = get_zenodo_record(doi)

        # Assume we want to add known contributors
        creators = record["metadata"].get("creators", [])
        self.update_cache(update_lookup=False)

        for login, _ in self.repo.contributors.items():

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            entry = {"name": cache.get("name") or login}
            if "orcid" in cache:
                entry["orcid"] = cache["orcid"]
            if "bio" in cache or "affiliation" in cache:
                entry["affilitation"] = cache.get("affiliation", cache.get("bio"))
            creators.append(entry)

        # Update final metadata
        metadata = {
            "creators": creators,
            "upload_type": record["metadata"]["resource_type"]["type"],
            "keywords": self.repo.topics(record["metadata"]["keywords"]),
            "access_right": record["metadata"]["access_right"],
            "license": record["metadata"]["license"]["id"],
        }

        write_json(metadata, zenodo_file)
        return metadata

    def update(self, thresh=1):
        """Given an existing .zenodo.json file, update it with contributors
           from an allcontributors file.
        """
        self.thresh = thresh
        self.load_data()
        bot.info("Updating %s" % self.filename)

        # We don't currently have a reliable identifier for zenodo, so we recreate each time
        self.lookup = self.data.get("creators", [])
        creators = []

        self.update_cache()

        for login, _ in self.repo.contributors.items():

            # Check against contribution threshold, and not bot
            if not self.include_contributor(login):
                continue

            cache = self.cache.get(login) or {}
            entry = {"name": cache.get("name") or login}
            if login in self.cache:
                for field in ["name", "affiliation", "orcid"]:
                    if field in self.cache[login]:
                        entry[field] = self.cache[login][field]
            if "orcid" in cache and "orcid" not in entry:
                entry["orcid"] = cache["orcid"]
            if "affiliation" in cache and "affiliation" not in entry:
                entry["affilitation"] = cache["affiliation"]
            creators.append(entry)

        self.data["creators"] = creators
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
    """Given a doi, retrieve a record using the Zenodo API
    """
    # Get the record number from the doi
    record = doi.split("/")[-1].replace("zenodo.", "")
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        response = requests.get(
            "https://zenodo.org/api/records/%s" % record, json={"access_token": token},
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
