"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.utils.command import Command
import logging
import os
import re
import requests
import sys

repository_regex = "(?P<owner>[\w,\-,\_]+)/(?P<repo>[\w,\-,\_]+)"

bot = logging.getLogger("github")


def get_topics(repo):
    """Given a repository, get topics associated.
    """
    repo = get_repo(repo) or {}
    return repo.get("topics", [])


def get_repo(repo):
    """get_repo will return a single repo, username/reponame
       given authentication with user    
    """
    headers = get_headers()
    headers["Accept"] = "application/vnd.github.mercy-preview+json"
    url = "https://api.github.com/repos/%s" % repo
    response = requests.get(url, headers=headers)

    # Case 2: public and private
    if response.status_code != 200:
        bot.warning(f"Issue getting {repo}: {response.status_code}, {response.reason}")
        return

    return response.json()


def get_contributors(repo):
    """Given a GitHub repository address, retrieve a lookup of contributors
       from the API endpoint. We look to use the GITHUB_TOKEN if exported
       to the environment, and exit if the response has any issue.
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
    # Return a lookup based on GitHub Login
    return {x["login"]: x for x in response.json()}


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
       and then check for a local .git repo. Finally, verify that format is 
       correct. Return the repository name.
    """
    repo = repo or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        command = Command("git config --get remote.origin.url")
        command.execute()

        # Issue running command
        if command.returncode != 0 or not command.out:
            sys.exit("Could not determine repository from local .git.")
        repo = command.out[0]

    match = re.search(repository_regex, repo)

    # Must conform to correct name
    if not match:
        sys.exit("Malformed repository address %s" % repo)
    owner, repo = match.groups()
    return "%s/%s" % (owner, repo)
