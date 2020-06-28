# allcontributors-zenodo (a2z)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## What is a2z?

A2z (All contributors to zenodo) is a tool and GitHub action that will allow you to:

 - generate or update an [all-contributors](https://github.com/all-contributors) entry.
 - add contributors to the all-contributors file via finding them via the GitHub API
 - updating a .zenodo.json file with these same individuals

To retrieve repository contributors, we use the GitHub API in both cases.
**Under development** we will look for Orcid identifiers to go along with 
associated emails, and add them to the Zenodo.json, along with keeping
a cache.

## GitHub Action

Since [all-contributors](https://github.com/all-contributors) requires node,
you might find it easiest to interact with the tool via a GitHub action.
You can see examples in the [examples](examples) folder.

### Inputs

| name | description | required | default |
|------|-------------|----------|---------|
| zenodo_file | .zenodo.json to update. If does not exist, must define zenodo_doi | false | .zenodo.json | 
| zenodo_doi | Zenodo DOI needed for init. Leave unset to skip init. | false | unset | 
| log_level | Log level to use, one of INFO, DEBUG, CRITICAL, ERROR, WARNING, FATAL (default INFO) | false | INFO | 
| threshold | the minimum number of contributions required to add a user | false | 1 | 
| force | if files exist, force overwrit | false | false |
| ctype |Contribution type, which defaults to "code" if not set. | false | code |
| skip_generate | skip running all-contributors generate | false | false |

If you aren't familiar with all-contributors, you'll need to add some
[commenting in your repository README](https://allcontributors.org/docs/en/cli/usage)
so the client knows where to write.

## Docker Usage

If you don't want to use the GitHub Action but want to interact with the tool
in a container, you can do that too! 

### 1. Prepare the Container

First, build the container from the included
Dockerfile:

```bash
docker build -t allcontributors .
```

Then shell inside, ensuring that the entrypoint is changed to bash. You'll also
want to bind your repository to somewhere in the container (not `/code`).

```bash
docker run -it --entrypoint bash -v $PWD/:/data allcontributors
```

In the container, a2z is installed as a python "binary" on the path:

```bash
# which a2z
/usr/local/bin/a2z
```

The all contributors client is also on the path:

```bash
$ which cli.js
/code/node_modules/all-contributors-cli/dist/cli.js
```

### 2. Generate .all-contributorsrc

Let's now change directory to where we bound our repository as a volume.

```bash
cd /data
```

If you don't have an `.all-contributorsrc` in your present working directory (the
root of the repository) you can use [a2z.py](a2z.py) to generate an empty one. You
can either provide the repository name directly:

```bash
$ a2z init singularityhub/sregistry
INFO:a2z:Generating .all-contributorsrc
```

or export it to the environment as `GITHUB_REPOSITORY` (this is how it would be discovered
during a GitHub workflow run).

```bash
export GITHUB_REPOSITORY=singularityhub/sregistry
$ a2z init
INFO:a2z:Generating .all-contributorsrc
```
In both cases, you'll generate an empty file:

```bash
$ cat .all-contributorsrc 
{
    "projectName": "sregistry",
    "projectOwner": "singularityhub",
    "repoType": "github",
    "repoHost": "https://github.com",
    "files": [
        "README.md"
    ],
    "imageSize": 100,
    "commit": true,
    "commitConvention": "none",
    "contributors": [],
    "contributorsPerLine": 7
}
```

### 2. Generate .zenodo.json

If you want to generate a fresh Zenodo.json, you can do that as follows:

```bash
$ a2z init --zenodo 10.5281/zenodo.1012531 singularityhub/sregistry
```

While the GitHub repository is sometimes found as a related identifier,
this isn't always the case, so you should again provide it on the command
line or exported to `GITHUB_REPOSITORY`. By default, we parse contributors
from the GitHub API, and include the creators already defined in Zenodo.
You will need this `.zenodo.json` file to exist in order to update it.

### 3. Update contributors

We next want to use the GitHub api to discover contributors to the repository,
for either both the `.all-contributorsrc` and the `.zenodo.json`, or just one of the two.

#### Update all

If you want to update both the allcontributors file and the zenodo.json, you
can kill two birds with one stone (and essentially cache the GitHub API request)
and do the following:

```bash
$ a2z update all
```

Note that for the update, we query the GitHub API to update both the zenodo.json
and contributors file.

#### Update allcontributors

Since we already have the contributors file we don't need to provide the repository name again, however it's suggested that you export a `GITHUB_TOKEN` to increase your API limits (if necessary).

```bash
$ a2z update allcontrib
```

You can optionally set a minimum number of contributors threshold to add (defaults to 1), or
a string to represent the kind of contribution (defaults to "core")

```bash
$ a2z update --thresh 10 --ctype docs
```

Note that GitHub bots are not included as contributors, and they are indicated with
"[bot]" in the name. If you find that you hit the API limit, then you will see this:

```bash
$ a2z update allcontrib
INFO:a2z:Updating .all-contributorsrc
Response 403: rate limit exceeded, cannot retrieve user RonaldEnsing.
```
And should export a `GITHUB_TOKEN` to increase it.

#### Update zenodo.json

For the zenodo update alone, since we don't read a repository from the .all-contributors file,
 you should provide it on the command line.

```bash
$ az2 update zenodo singularityhub/sregistry
INFO:a2z:Updating zenodo
```
You can again export `GITHUB_REPOSITORY` instead.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## TODO

 - Orcid API needs to be added to get ORCIDids based on emails
 - a cache of some kind should be kept for orcid ids
 - an example should be added to push to a repository / open PR

## Problem statement

https://github.com/all-contributors is an awesome project which helps to collect and display contributors in github hosted projects.
It produces .all-contributorsrc (json) such as

```
{
  "files": [
    "README.md"
  ],
  "imageSize": 100,
  "commit": false,
  "contributors": [
    {
      "login": "yarikoptic",
      "name": "Yaroslav Halchenko",
      "avatar_url": "https://avatars3.githubusercontent.com/u/39889?v=4",
      "profile": "http://www.onerussian.com",
      "contributions": [
        "infra",
        "projectManagement",
        "code",
        "content",
        "review",
        "maintenance"
      ]
    },
    {
      "login": "adswa",
      "name": "Adina Wagner",
      "avatar_url": "https://avatars1.githubusercontent.com/u/29738718?v=4",
      "profile": "http://www.adina-wagner.com",
      "contributions": [
        "infra"
      ]
    },
..
  ],
  "contributorsPerLine": 7,
  "projectName": "open-brain-consent",
  "projectOwner": "con",
  "repoType": "github",
  "repoHost": "https://github.com",
  "skipCi": true
}
```

which contains pointers to github logins, names, their contributions etc.

There is also zenodo.org which is used by many projects to get citeable references for their research software.  See e.g. our DataLad's [.zenodo.json](https://github.com/datalad/datalad/blob/master/.zenodo.json) for an example.  A typical entry in that one would contain also affiliation and an [orcid id]():

```json
{
      "affiliation": "Dartmouth College, Hanover, NH, United States",
      "name": "Halchenko, Yaroslav O.",
      "orcid": "0000-0003-3456-2493"
},
```

ORCID has an API: https://members.orcid.org/api/tutorial/search-orcid-registry allowing for search of an orcid record via email.
GitHub has an API allowing to get email for the account: https://developer.github.com/v3/users/ .

So we just need a helper tool to create/update/maintain .zenodo.json based on allcontributors by querying github and orcid for the missing fields.

The tool (if not a github bot?!) could retain a local cache or even some global registry of mapping from github id to orcid id (with more or less up to date affiliation)
