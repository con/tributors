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

from tributors.main.github import (
    get_github_repository,
    get_topics,
)
from tributors.utils.file import read_json, write_json
from .base import ParserBase

bot = logging.getLogger("zenodo")


class ZenodoParser(ParserBase):

    name = "zenodo"

    def __init__(self, filename=None, repo=None, **kwargs):
        filename = filename or ".zenodo.json"
        super().__init__(filename, repo)

    def init(self, repo, params=None, force=False, contributors=None):
        """Generate an empty .zenodo.json if it doesn't exist
        """
        params = params or {}

        # A doi is required
        doi = params.get("--doi")
        if not doi:
            sys.exit("Please provide the zenodo doi with --doi")

        # Zenodo file defaults to expected .zenodo.json
        zenodo_file = params.get("--zenodo-file", self.filename)
        if os.path.exists(zenodo_file) and not force:
            sys.exit("%s exists, set --force to overwrite." % zenodo_file)

        bot.info("Generating %s" % zenodo_file)
        self._repo = get_github_repository(repo)
        record = get_zenodo_record(doi)

        # Assume we want to add known contributors
        creators = record["metadata"].get("creators", [])
        self.update_cache()

        for login, metadata in self.cache.items():
            entry = {"name": metadata.get("name") or login}
            if "orcid" in metadata:
                entry["orcid"] = metadata["orcid"]
            if "bio" in metadata or "affiliation" in metadata:
                entry["affilitation"] = metadata.get("affiliation", metadata.get("bio"))
            creators.append(entry)

        # Get keywords from GitHub topis
        keywords = get_topics(self.repo)
        keywords = list(set(record["metadata"]["keywords"] + keywords))

        # Update final metadata
        metadata = {
            "creators": creators,
            "upload_type": record["metadata"]["resource_type"]["type"],
            "keywords": keywords,
            "access_right": record["metadata"]["access_right"],
            "license": record["metadata"]["license"]["id"],
        }

        write_json(metadata, zenodo_file)
        return metadata

    def update(self, repo=None, params=None, contributors=None, thresh=1):
        """Given an existing .zenodo.json file, update it with contributors
           from an allcontributors file.
        """
        params = params or {}
        self.thresh = thresh
        zenodo_file = params.get("--zenodo-file", self.filename)

        # Ensure contributors file and zenodo.json exist
        if not os.path.exists(zenodo_file):
            sys.exit("%s does not exist" % zenodo_file)

        bot.info("Updating %s" % zenodo_file)

        # We don't currently have a reliable identifier for zenodo, so we recreate each time
        data = read_json(zenodo_file)
        self.lookup = data.get("creators", [])
        creators = []

        self._repo = get_github_repository(repo)
        self.update_cache()

        for login, metadata in self.cache.items():
            entry = {"name": metadata.get("name") or login}
            if login in self.cache:
                for field in ["name", "affiliation", "orcid"]:
                    if field in self.cache[login]:
                        entry[field] = self.cache[login][field]
            if "orcid" in metadata and "orcid" not in entry:
                entry["orcid"] = metadata["orcid"]
            if "affiliation" in metadata and "affiliation" not in entry:
                entry["affilitation"] = metadata["affiliation"]
            creators.append(entry)

        data["creators"] = creators
        write_json(data, zenodo_file)
        return data

    def _update_cache(self):
        """Each client optionally has it's own function to update the cache.
            In the case of zenodo, we aren't necessarily aware of GitHub
            login (the current mapping mechanism) so we cannot update the
            cache yet. When orcid is added this might be an option.
         """
        pass


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
