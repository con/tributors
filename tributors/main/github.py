"""

Copyright (C) 2020-2022 Vanessa Sochat.

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

repository_regex = "(?P<owner>[\w,\-,\_]+)/(?P<repo>[\w,\-,\_\.]+)"

bot = logging.getLogger("github")


class GitHubRepository:
    """A GitHub repository parses a repo and exposes repository and contributor
    metadata.
    """

    def __init__(self, repo, skip_users=None, params=None):
        self._repo = {}
        self._contributors = []
        self._topics = []
        self.uid = get_github_repository(repo)
        self.skip_users = skip_users or []
        self.params = params or {}
        self.cache = {}

    def include_contributor(self, login):
        """Given a threshold (and preference to not include bots) return a boolean
        to indicate including the contributor or not
        """
        contributor = self.contributors.get(login)

        # if the login is marked to skip
        if login in self.skip_users:
            return False

        # Skip GitHub bots
        if contributor["type"] == "Bot" or "[bot]" in contributor["login"]:
            return False
        return True

    # GitHub repository can serve as a metadata parser
    def update_lookup(self):
        """update the .tributors file using GitHub contributors"""
        if not self.skip_users:
            self.skip_users = self.params.get("--skip-users", "").split(" ")

        # Iterate through GitHub and update metadata
        for login, contributor in self.contributors.items():

            # Don't include bots, and others specified with --skip-user
            if not self.include_contributor(login):
                continue

            # Look up a GitHub username, possibly email and site
            user = get_user(login)

            entry = {"name": user.get("name") or login}
            if login in self.cache:
                entry = self.cache[login]
            else:
                bot.info(f"⭐️ new contributor {login}")

            # Update cache with fields that aren't defined yet
            for key in ["email", "bio", "blog"]:
                if user.get(key) and key not in entry:
                    entry[key] = user.get(key)
                    bot.info(f"  Updating {login} with {key}: {entry[key]}")
            self.cache[login] = entry
        return self.cache

    def __str__(self):
        return "[github][%s]" % self.uid

    def __repr__(self):
        return self.__str__()

    @property
    def repo(self):
        """Retrieve the GitHub repository, if we don't have it yet"""
        if not self._repo:
            self._repo = get_repo(self.uid)
        return self._repo

    # Equivalent methods to a parser to get lookups based on primary ids
    @property
    def email_lookup(self):
        """Return loaded metadata as an email lookup."""
        return {}

    @property
    def name_lookup(self):
        """Return loaded metadata as an orcid lookup."""
        return {}

    @property
    def orcid_lookup(self):
        """Return loaded metadata as an orcid lookup."""
        return {}

    @property
    def login_lookup(self):
        """Return loaded metadata as a github login lookup."""
        return self.contributors

    @property
    def contributors(self):
        """Return list of contributors, and retrieve if we don't have yet"""
        if not self._contributors:
            self._contributors = get_contributors(self.uid)
        return self._contributors

    def topics(self, topics=None):
        """Return list of topics, optionally add extras and return unique set"""
        if not self._topics:
            self._topics = get_topics(self.uid)
        topics = topics or []
        return list(set(self._topics + topics))

    @property
    def description(self):
        return self.repo["description"]

    @property
    def html_url(self):
        return self.repo["html_url"]

    @property
    def name(self):
        return self.repo["name"]

    @property
    def issues_url(self):
        return "%s/issues" % self.repo["html_url"]

    @property
    def license(self):
        return "https://spdx.org/licenses/%s" % self.repo["license"]["spdx_id"]


def get_topics(repo):
    """Given a repository, get topics associated."""
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
    page = 1
    contributors = {}
    while True:
        paginated_url = "%s?page=%s" % (url, page)
        bot.debug(paginated_url)
        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            message = "Response %s from GitHub: %s, cannot retrieve contributors " % (
                response.status_code,
                response.reason,
            )
            if not os.environ.get("GITHUB_TOKEN"):
                message += " you should export GITHUB_TOKEN to increase your API limits"
            sys.exit(message)
        new_contributors = {x["login"]: x for x in response.json()}

        # This is the signal for we don't have any more pages
        if not new_contributors:
            break
        contributors.update(new_contributors)
        page += 1

    # Return a lookup based on GitHub Login
    return contributors


def get_headers():
    """Get headers, including a Github token if found in the environment"""
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
            "Response %s: %s, cannot retrieve GitHub user %s."
            % (response.status_code, response.reason, username)
        )
    return response.json()


def get_github_repository(repo):
    """First preference goes to repo variable provided, then check the environment,
    and then check for a local .git repo. Finally, verify that format is
    correct. Return the repository name.
    """
    if isinstance(repo, GitHubRepository):
        return repo.uid
    repo = repo or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        command = Command("git config --get remote.origin.url")
        command.execute()

        # Issue running command
        if command.returncode != 0 or not command.out:
            sys.exit("Could not determine repository from local .git.")
        repo = "/".join(command.out[0].strip().split("/")[-2:])

    match = re.search(repository_regex, repo)

    # Must conform to correct name
    if not match:
        sys.exit("Malformed repository address %s" % repo)
    owner, repo = match.groups()
    return "%s/%s" % (owner, re.sub(".git$", "", repo, 1))
