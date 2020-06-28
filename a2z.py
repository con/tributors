#!/usr/bin/env python3

"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import argparse
import logging
import json
import os
import re
import requests
import sys

repository_regex = "(?P<owner>[\w,\-,\_]+)/(?P<repo>[\w,\-,\_]+)"


def get_parser():
    parser = argparse.ArgumentParser(
        description="AllContributors to Zenodo (a2z) Metadata Parser"
    )

    parser.add_argument(
        "--log_level",
        dest="log_level",
        choices=LOG_LEVELS,
        default=LOG_LEVEL,
        help="Customize logging level for a2z parser.",
    )

    description = "actions for a2z"
    subparsers = parser.add_subparsers(
        help="a2z actions", title="actions", description=description, dest="command",
    )

    # Initialize an empty .all-contributorsrc
    init = subparsers.add_parser(
        "init", help="Initialize an empty .all-contributorsrc."
    )
    init.add_argument(
        "--zenodo",
        dest="zenodo",
        help="Initialize a .zenodo.json file instead, provide the DOI.",
        default=None,
    )
    init.add_argument(
        "--zenodo-file",
        dest="zenodo_file",
        help="The zenodo filename to use (defaults to .zenodo.json)",
        default=".zenodo.json",
    )
    init.add_argument(
        "--force",
        dest="force",
        help="If exists, overwrite existing .all-contributorsrc",
        default=False,
        action="store_true",
    )
    # Update existing all-contributorsrc or .zenodo.json
    update = subparsers.add_parser("update", help="Update existing all-contributorsrc",)
    update.add_argument(
        "--thresh",
        dest="threshold",
        help="Minimum number of contributions required to add user.",
        default=1,
        type=int,
    )
    update.add_argument(
        "utype",
        help="Update type (default to 'all' for contributors and zenodo.json",
        default="all",
        choices=["all", "zenodo", "allcontrib"],
    )
    update.add_argument(
        "--zenodo-file",
        dest="zenodo_file",
        help="If updating all or zenodo, target this .zenodo.json",
        default=".zenodo.json",
    )
    update.add_argument(
        "--ctype",
        dest="ctype",
        help="The contribution type to use for updated users.",
        default="code",
    )

    for command in [update, init]:
        command.add_argument(
            "repo",
            help="The repository URI, if not exported to GITHUB_REPOSITORY",
            nargs="?",
        )
        command.add_argument(
            "--filename",
            dest="filename",
            help="Path for filename",
            default=".all-contributorsrc",
        )

    return parser


def get_contributors(repo):
    """Given a GitHub repository address, retrieve a list of contributors
       from the API endpoint. We look to use the GITHUB_TOKEN if exported
       to the environment, and exit if the response has any issue
    """
    if not repo:
        sys.exit("A repository is required to get contributors.")
    url = "https://api.github.com/repos/%s/contributors" % repo
    headers = get_headers()
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        sys.exit(
            "Response %s: %s, cannot retrieve contributors."
            % (response.status_code, response.reason)
        )
    return response.json()


def get_headers():
    """Get headers, including a Github token if found in the environment
    """
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = "token %s" % token
    return headers


def get_user(username):
    """Given a username, retrieve the user metadata from GitHub. We need to do
       this to get the profile (blog) url from the metadata
    """
    url = "https://api.github.com/users/%s" % username
    headers = get_headers()
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        sys.exit(
            "Response %s: %s, cannot retrieve user %s."
            % (response.status_code, response.reason, username)
        )
    return response.json()


def get_github_repository(repo):
    """First preference goes to repo variable provided, then check the environment,
       and then verify that format is correct. Return the repository name
    """
    repo = repo or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        sys.exit("Provide repository name to client or export GITHUB_REPOSITORY")
    match = re.search(repository_regex, repo)

    # Must conform to correct name
    if not match:
        sys.exit("Malformed repository address %s" % repo)
    owner, repo = match.groups()
    return "%s/%s" % (owner, repo)


def get_zenodo_record(doi):
    """Given a doi, retrieve a record using the Zenodo API
    """
    # Get the record number from the doi
    record = doi.split("/")[-1].replace("zenodo.", "")
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        response = requests.get(
            "https://zenodo.org/api/records/%s" % record,
            json={"access_token": self.token},
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


def update_zenodo(repo=None, zenodo_file=".zenodo.json", contributors=None):
    """Given an existing .zenodo.json file, update it with contributors
       from an allcontributors file.

       Arguments:
        - filename (str) : default filename to write to.
    """
    # Ensure contributors file and zenodo.json exist
    if not os.path.exists(zenodo_file):
        sys.exit("%s does not exist" % zenodo_file)

    if not contributors:
        contributors = get_contributors(repo)

    # Load the previous contributors, create a lookup
    metadata = read_json(zenodo_file)
    lookup = {x["name"]: x for x in metadata.get("creators", [])}
    for contributor in contributors:
        user = get_user(contributor["login"])
        if user["name"] and user["name"] not in lookup:
            lookup[user["name"]] = {
                "name": user.get("name") or contributor.get("login"),
            }

    metadata["creators"] = list(lookup.values())
    write_json(metadata, zenodo_file)
    return metadata


def update_allcontributors(
    filename=".all-contributorsrc", thresh=1, ctype="code", contributors=None
):
    """Given an existing contributors file, use the GitHub API to retrieve
       all contributors, and then use subprocess to update the file

       Arguments:
        - filename (str) : default filename to write to.
        - thresh (int)   : minimum number of contributions to include
        - ctype (str)    : the contribution type to add (defaults to code)
    """
    if not os.path.exists(filename):
        sys.exit(
            "%s does not exist, set --filename or run a2z init to create" % filename
        )

    # Load the previous contributors, create a lookup
    metadata = read_json(filename)
    lookup = {x["login"]: x for x in metadata.get("contributors", [])}
    repo = "%s/%s" % (metadata["projectOwner"], metadata["projectName"])

    if not contributors:
        contributors = get_contributors(repo)

    # This doesn't seem to be paginated
    for contributor in contributors:

        # If they don't meet the threshold, continue
        if contributor["contributions"] < thresh:
            continue

        # Skip GitHub bots
        if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
            continue

        # if the username isn't in the lookup, do an extra call to get profile
        if contributor["login"] not in lookup:
            user = get_user(contributor["login"])
            lookup[contributor["login"]] = {
                "login": contributor["login"],
                "name": user.get("name", "") or "",
                "avatar_url": contributor.get("avatar_url"),
                "profile": user.get("blog", contributor.get("html_url")),
                "contributions": [ctype],
            }
        else:
            if ctype not in lookup[contributor["login"]]["contributions"]:
                lookup[contributor["login"]]["contributions"].append(ctype)

    # Update the contributors
    metadata["contributors"] = list(lookup.values())
    write_json(metadata, filename)
    return metadata


def generate_zenodo(repo, doi, zenodo_file=".zenodo.json", force=False):
    """Generate an empty .zenodo.json if it doesn't exist
    """
    # A doi is required
    if not doi:
        sys.exit("Please provide the zenodo doi with --zenodo")

    if os.path.exists(zenodo_file) and not force:
        sys.exit("%s exists, set --force to overwrite." % zenodo_file)

    repo = get_github_repository(repo)
    record = get_zenodo_record(doi)

    # Get repository contributors
    contributors = get_contributors(repo)

    # Assume we want to add known contributors
    creators = record["metadata"].get("creators", [])
    for contributor in contributors:

        # Skip GitHub bots
        if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
            continue

        # TODO: no unique identifier can identify already existing users
        user = get_user(contributor["login"])
        entry = {"name": user.get("name", contributor["login"])}
        bio = user.get("bio")
        if bio:
            entry["affiliation"] = bio.strip()
        creators.append(entry)

    # TODO: should we get keywords from GitHub topics too?
    metadata = {
        "creators": creators,
        "upload_type": record["metadata"]["resource_type"]["type"],
        "keywords": record["metadata"]["keywords"],
        "access_right": record["metadata"]["access_right"],
        "license": record["metadata"]["license"]["id"],
    }

    write_json(metadata, zenodo_file)
    return metadata


def generate_allcontributors(repo=None, force=False, filename=".all-contributorsrc"):
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
    if os.path.exists(filename) and not force:
        sys.exit("%s exists, set --force to overwrite." % filename)

    # A repository is required via the command line or environment
    repo = get_github_repository(repo)
    owner, repo = repo.split("/")[:2]

    # Write metadata to empty all contributors flie.
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
    write_json(metadata, filename)


def write_json(json_obj, filename, pretty=True):
    """write_json will write a json object to file, pretty printed

       Arguments:
        - json_obj (dict) : the dict to print to json
        - filename (str)  : the output file to write to
    """
    with open(filename, "w") as filey:
        if pretty:
            filey.writelines(json.dumps(json_obj, indent=4, separators=(",", ": ")))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_json(input_file):
    """Read json from an input file.

       Arguments:
         - input_file (str) : the filename to read
    """
    with open(input_file, "r") as filey:
        data = json.loads(filey.read())
    return data


# Allow setting log level via the environment
LOG_LEVEL = os.environ.get("A2Z_LOG_LEVEL", "INFO")
LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "QUIET", "FATAL"]
if LOG_LEVEL not in LOG_LEVELS:
    LOG_LEVEL = "INFO"


def main():
    """main entrypoint for a2z
    """

    parser = get_parser()

    def help(return_code=0):
        print("\nAllcontributors to Zenodo Parser")
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Set the logging level
    logging.basicConfig(level=getattr(logging, args.log_level))
    bot = logging.getLogger("a2z")
    bot.setLevel(getattr(logging, args.log_level))

    # Does the user want a shell?
    if args.command == "init":
        if args.zenodo:
            bot.info("Generating %s" % args.zenodo_file)
            generate_zenodo(
                repo=args.repo,
                zenodo_file=args.zenodo_file,
                doi=args.zenodo,
                force=args.force,
            )
        else:
            bot.info("Generating %s" % args.filename)
            generate_allcontributors(
                repo=args.repo, force=args.force, filename=args.filename
            )

    elif args.command == "update":

        bot.info("Updating %s" % args.utype)

        # If we are doing both calls, cache the contributors list
        if args.utype == "all":
            metadata = update_allcontributors(filename=args.filename, ctype=args.ctype)
            repo = "%s/%s" % (metadata["projectOwner"], metadata["projectName"])
            update_zenodo(zenodo_file=args.zenodo_file, repo=repo)

        # Update contributors
        elif args.utype == "allcontrib":
            update_allcontributors(filename=args.filename, ctype=args.ctype)

        # Update Zenodo
        if args.utype == "zenodo":
            update_zenodo(repo=args.repo, zenodo_file=args.zenodo_file)


if __name__ == "__main__":
    main()
