"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.utils.file import write_file, get_tmpfile
from tributors.utils.prompt import choice_prompt, entry_prompt
import logging
import os
import requests
import urllib

bot = logging.getLogger("github")


class OrcidIdentifier:
    """A simple class to retrieve an orcid record, and expose needed fields"""

    def __init__(self, orcid):
        self.orcid = orcid
        self._record = {}
        self.found = False

    def __str__(self):
        if self.orcid:
            return "[orcid][%s]" % self.orcid
        return "[orcid]"

    def __repr__(self):
        return self.__str__()

    @property
    def record(self):
        """Given an orcid id, retrieve a record for it"""
        if not self._record and self.orcid:
            self.get_record()
        return self._record

    @property
    def firstName(self):
        return (
            self.record.get("person", {})
            .get("name", {})
            .get("given-names", {})
            .get("value")
        )

    @property
    def affiliation(self):
        """We consider the affiliation the most recent employment (top of the list)"""
        employer = (
            self.record.get("activities-summary", {})
            .get("employments", {})
            .get("employment-summary", [])
        )
        if employer:
            return employer[0].get("organization", {}).get("name")

    @property
    def lastName(self):
        return (
            self.record.get("person", {})
            .get("name", {})
            .get("family-name", {})
            .get("value")
        )

    def get_record(self):
        if not self.orcid:
            return

        response = requests.get(
            "https://pub.orcid.org/v2.1/%s/record" % self.orcid,
            headers={
                "Accept": "application/json",
            },
        )
        if response.status_code != 200:
            return
        self.found = True
        self._record = response.json()


def get_orcid_token():
    """If the user has exported a token, we discover and return it here.
    Otherwise we prompt him or her to open a browser and copy paste a code
    to the calling client. This is currently not used, but kept in case
    we need to add it back.
    """
    orcid_token = os.environ.get("ORCID_TOKEN")
    orcid_id = os.environ.get("ORCID_ID")
    orcid_secret = os.environ.get("ORCID_SECRET")

    if not orcid_token and orcid_id is not None and orcid_secret is not None:
        response = requests.post(
            "https://orcid.org/oauth/token",
            headers={"Accept": "application/json"},
            data={
                "client_id": orcid_id,
                "client_secret": orcid_secret,
                "grant_type": "client_credentials",
                "scope": "/read-public",
            },
        )

        if response.status_code != 200:
            return

        response = response.json()
        orcid_token = response["access_token"]
        orcid_refresh = response["refresh_token"]

        # Write the token to file and direct the user to use it
        tmp_file = get_tmpfile()
        content = "export ORCID_TOKEN=%s\nexport ORCID_REFRESH_TOKEN=%s\n" % (
            orcid_token,
            orcid_refresh,
        )
        write_file(tmp_file, content)
        print(
            f"Orcid token exports written to {tmp_file}. "
            "In the future export these variables for headless usage."
        )

    return orcid_token


def record_search(url, terms, interactive=False, search_type=""):
    """Given a url (with a name or terms) do a record search looking for an orcid id.

    Arguments:
      - url (str) : url to perform request
      - terms (str) : terms, used just for logging
      - interactive (bool) : if True, ask user if there is more than a single response
      - search_type (str) : description on what search is based on, used just for logging
    """
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.status_code != 200:
        return

    results = response.json().get("expanded-result", []) or []

    if not results:
        return

    # We found only one matching result
    if len(results) == 1:
        return results[0]["orcid-id"]

    term_str = terms[0] % terms[1:]
    # Only stream results to screen in interactive mode
    if not interactive:
        bot.info(
            f"{term_str}: found more than one ({len(results)}) result for ORCID search {search_type}, "
            "run with --interactive mode to select."
        )
        return Ellipsis

    # One or more results
    if len(results) > 10:
        bot.warning("Found more than 10 results, will only show top 10.")

    print("\n\n%s\n======================================================" % term_str)
    for idx, r in enumerate(results):
        # Limit is ten results, count starting at 0
        idx = idx + 1
        if idx > 10:
            break

        record = "  Name: %s, %s\n  ORCID: %s (https://orcid.org/%s)" % (
            r["family-names"],
            r["given-names"],
            r["orcid-id"],
            r["orcid-id"],
        )
        if r["institution-name"]:
            record = "%s\n  Institutions: %s" % (
                record,
                ", ".join(r["institution-name"]),
            )
        if r["other-name"]:
            record = "%s\n  Other Names: %s" % (record, ", ".join(r["other-name"]))
        if r["email"]:
            record = "%s\n  Email: %s" % (record, r["email"])
        if not interactive:
            print("%s\n" % record)
        else:
            print("[%s]\n%s\n" % (idx, record))

    # TODO: here we should remember for a person on what we already presented as
    # options and not to show them again.
    #
    # If interactive, ask for choice prompt
    if interactive:
        skip_choices = ["s", "S", "skip"]
        enter_choices = ["e", "E", "enter"]
        quit_choices = ["q"]
        choices = (
            [str(i) for i, _ in enumerate(results, 1)]
            + skip_choices
            + enter_choices
            + quit_choices
        )
        prefix = "1:%s or s to skip, e to enter, q to quit the loop" % min(
            10, len(results)
        )
        choice = choice_prompt(
            "Please enter a choice, or s to skip, e to enter.",
            choices=choices,
            choice_prefix=prefix,
            multiple=False,
        )
        if choice in quit_choices:
            raise StopIteration("Requested by user")

        if choice in enter_choices:
            return entry_prompt(
                f"Please enter the ORCID for {term_str}.",
                regex="[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$",
            )

        if not choice or choice in skip_choices:
            return

        # Return the orcid identifier
        return results[int(choice) - 1]["orcid-id"]


def extended_search_url(q, *args):
    """Helper to properly quote args and avoid duplicating URL etc"""
    # We will show only up to 10, so requesting 11, no need to get all default 1000
    url = f"https://pub.orcid.org/v3.0/expanded-search?q={q}&args=11"
    if args:
        url %= tuple(map(urllib.parse.quote, args))
    return url


strict, loose = True, False


def gen_searches(email, name):
    if email:
        yield (("email:%s", email), "by email", strict)

    # Next attempts will use name
    if name is not None:
        delim = "," if "," in name else " "
        cleaner = "," if delim == " " else " "

        parts = [_.strip(cleaner) for _ in name.split(delim)]

        # No go if only a first or last name
        if len(parts) == 1:
            bot.debug(f"Skipping {name}, first and last are required for search.")
            return

        # Just as is
        yield (
            ('credit-name:"%s"+OR+other-names:"%s"', name, name),
            "by full credit or other names",
            strict,
        )

        if delim == ",":
            # Last, First Middle
            last, given = parts[0], " ".join(parts[1:])
        else:
            # First Middle Last
            given, last = " ".join(parts[:-1]), parts[-1]

        yield (
            ('given-names:"%s"+AND+family-name:"%s"', given, last),
            "by name",
            strict,
        )

        # Attempt # 3 will try removing the middle name
        if " " in given:
            yield (
                (
                    'given-names:"%s"+AND+family-name:"%s"',
                    given.split(" ")[0].strip(),
                    last,
                ),
                "by name",
                loose,
            )

        # Just a combination of all parts of the name
        yield (
            ("+AND+".join(["%s"] * len(parts)),) + tuple(parts),
            "by name parts",
            loose,
        )


def get_orcid(email: str | None, name: str | None = None, interactive=False):
    """Get an orcid identifier for a given email or name."""
    # We must have an email OR name
    if not email and not name:
        return

    for search_args, search_desc, strictness in gen_searches(email, name):
        url = extended_search_url(*search_args)
        if (
            orcid_id := record_search(url, search_args, interactive, search_desc)
        ) is not Ellipsis and orcid_id:
            return orcid_id
        if orcid_id is Ellipsis:
            orcid_id = None
            if strict:
                break
        # if loose, and still got multiple results, continue
