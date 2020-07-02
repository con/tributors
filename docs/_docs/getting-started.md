---
title: Getting Started
tags: 
 - allcontrib
 - zenodo
 - docker
description: Getting started with tributors
---

# Getting Started

This guide will provide getting started instructions for local and Docker Usage,
along with GitHub Workflows.

## Quick Start

### 1. Install
Install tributors

```bash
pip install tributors
```

### 2. Environment

Especially if you need orcid ids in your metadata, for a first time go you
should export an id and secret to interact with the Orcid API. It'a also recommended
to export a GitHub token to increase your API limit:

```bash
export ORCID_ID=APP-XXXXXXX
export ORCID_SECRET=12345678910111213141516171819202122
export GITHUB_TOKEN=XXXXXXXXXXXXXXX
```

Once you generate an orcid token, it will be written to a temporary file,
and you can read the file and export the variable for later discovery (and you'll
no longer need the ID and secret):

```bash
export ORCID_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXX
```

### 3. Update
If you have a repository with files already defined, you can use the auto-detect
update (not specifying a particular contributor parser):

```bash
$ tributors update
```

or update a specific one:

```bash
$ tributors update allcontrib
$ tributors update zenodo
$ tributors update codemeta
```

### 3. Init
You can also create empty files if you don't have them yet:

```bash
$ tributors init allcontrib
$ tributors init zenodo
```

You can read more about the various [parsers]({{ site.baseurl }}/docs/parsers)
for specific-parser arguments, and more details about the above commands in the
sections below.

## Docker Usage

If you don't want to use the GitHub Action and don't want to install npm on
your local machine, you can instead interact with the tool in a container.

### 1. Prepare the Container

First, build the container from the included [Dockerfile](..Dockerfile):

```bash
docker build -t tributors .
```

Then shell inside, ensuring that the entrypoint is changed to bash. You'll also
want to bind your repository to somewhere in the container (not `/code`).

```bash
docker run -it --entrypoint bash -v $PWD/:/data tributors
```

In the container, tributors is already installed and on the path:

```bash
$ which tributors
/usr/local/bin/tributors
```

The all contributors client is also on the path (and this might be
the reason you want to use a container, because this install required npm/node).

```bash
$ which cli.js
/code/node_modules/all-contributors-cli/dist/cli.js
```

You'll notice that the present working directory is the `/github/workspace`,
and we do this so the container runs easily for a GitHub action (where the 
code for the user is found here).

### 2. Generate 

Generation coincides with initializing a new file. This is supported for
all-contributors and zenodo.json. For codemeta, there are already a 
suite of [tools available](https://codemeta.github.io/tools/).

#### Generate .all-contributorsrc

Let's now change directory to where we bound our repository as a volume.

```bash
cd /data
```

If you don't have an `.all-contributorsrc` in your present working directory (the
root of the repository) you can use tributors to generate an empty one. Tributors
will discover the repository name from the .git folder, so you don't need to
provide it.

```bash
$ tributors init allcontrib
INFO:allcontrib:Generating .all-contributorsrc for con/tributors
```

If you don't have a .git repository, you can export your repository name to the environment as `GITHUB_REPOSITORY` (e.g., to run it for a repository outside of the one you are sitting
in):

```bash
export GITHUB_REPOSITORY=singularityhub/sregistry
$ tributors init allcontrib
INFO:allcontrib:Generating .all-contributorsrc for con/tributors
```

and you can define the repository on the command line too:

```bash
$ tributors init allcontrib --repo singularityhub/sregistry
INFO:allcontrib:Generating .all-contributorsrc for con/tributors
```

or change the path to the file to generate:

```bash
$ tributors init allcontrib --allcontrib-file .mycontibrc
INFO:allcontrib:Generating .mycontibrc for con/tributors
```

In all cases, you'll generate an empty file:

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

#### Generate .zenodo.json

If you want to generate a fresh Zenodo.json, you can do that as follows:

```bash
$ tributors init zenodo --doi 10.5281/zenodo.1012531
```

The same repository rules apply as stated previously - you can define the repository
with `--repo`, in the environment via `GITHUB_REPOSITORY`, or allow it
to be detected from a local .git folder.


If you need to change the path of the file, you can do that too:

```bash
$ tributors init zenodo --doi 10.5281/zenodo.1012531 --zenodo-file another-zenodo.json
INFO:zenodo:Generating another-zenodo.json
```

### 3. Update contributors

We next want to use the GitHub api to discover contributors to the repository,
for either both the `.all-contributorsrc` and the `.zenodo.json`, or just one of the two.

#### Update all

If you want to update both the allcontributors file and the zenodo.json, you
can kill two birds with one stone (and essentially cache the GitHub API request)
and do the following:

```bash
$ tributors update all
```

#### Update (auto)

If you have a repository with one or more default contributor files, you can
update all of these files that are detected by leaving out the parser name:

```bash
$ tributors update
INFO:zenodo:Updating .zenodo.json
INFO:allcontrib:Updating .all-contributorsrc
```
Note that for any multiple updates, we query the GitHub API to get updated contributors,
and also use a cached [.tributors]({{ site.baseurl }}/docs/tributors) file to
keep track of shared metadata.

#### Update allcontributors

Since we already have the contributors file we don't need to provide the repository name again, however it's suggested that you export a `GITHUB_TOKEN` to increase your API limits (if necessary).

```bash
$ tributors update allcontrib
INFO:allcontrib:Updating .all-contributorsrc
```

You can optionally set a minimum number of contributors threshold to add (defaults to 1), or
a string to represent the kind of contribution (defaults to "core")

```bash
$ tributors update allcontrib --thresh 10 --allcontrib-type doc
```

Keep in mind that when you run the command above, the update will only happen
for those users with contributors greater than or equal to the threshold.

Note that GitHub bots are not included as contributors, and they are indicated with
"[bot]" in the name. If you find that you hit the API limit, then you will see this:

```bash
$ tributors update allcontrib
INFO:a2z:Updating .all-contributorsrc
Response 403: rate limit exceeded, cannot retrieve user RonaldEnsing.
```
And should export a `GITHUB_TOKEN` to increase it.

#### Update zenodo.json

Zenodo contributors can be updated similarly:

```bash
$ tributors update zenodo
INFO:zenodo:Updating .zenodo.json
```

You can again export `GITHUB_REPOSITORY` instead.

#### Update codemeta

You can quickly update your contributors for a codemeta.json or codemeta.jsonld file
that already exists.

```bash
$ tributors update codemeta
```

## Local Usage

Local usage means using the Python package directly on your local machine.

### 1. Install tributors

You can install it from pypi:

```bash
pip install tributors
```

or clone the repository and install locally:

```bash
git clone git@github.com:con/tributors
cd tributors
pip install .[all]
```

or for a development install:

```bash
pip install -e .[all]
```

### 2. Environment

You can set a log level via the environment via exporting `TRIBUTORS_LOG_LEVEL`:

```bash
export TRIBUTORS_LOG_LEVEL=DEBUG
```

Tokens can also be exported to increase interaction limits with various APIs:

```bash
export ZENODO_TOKEN=xxxxxx
export GITHUB_TOKEN=xxxxxx
```

If you want to link emails with Orcid id's, it is suggested to generate and export an `ORCID_TOKEN` to ensure that you can look up these identifiers based on email addresses. 
However to disable this, simply export the token as "disabled"

```bash
export ORCID_TOKEN=disabled
```

In order to generate this token
for the first time, you should export an `ORCID_ID` and `ORCID_SECRET` that you need to 
generate in the [developer tools](https://orcid.org/developer-tools). The callback
uri can be either one of the defaults that they provide (we don't use it).
Once you have your id and secret, export them to the environment.

```bash
export ORCID_ID=xxxxxxxx
export ORCID_SECRET=xxxxx
```

The `ORCID_TOKEN` and `ORCID_REFRESH_TOKEN` will be written to a temporary file,
and you can export these in the future to be discovered by the tributors client.
Subsequent requests use the token to interact with the [public search API](https://members.orcid.org/api/tutorial/search-orcid-registry). Note that we haven't
yet implemented using the refresh token to request a new one, so if you
hit this use case, please [open an issue](https://github.com/con/tributors/issues).

### 2. Generate

Generate means that you don't have a particular metadata file for a service,
and you want to initialize an "empty" one. For each service this means the following:

 - zenodo: .zenodo.json
 - all-contributors: .all-contributorsrc


#### .all-contributorsrc

The main configuration file for all contributors is the `.all-contributorsrc`.
While you can use the [all contributors](https://allcontributors.org/docs/en/cli/installation) client to generate an empty file, this might not be ideal if you don't want to install npm or use the GitHub bot. You can use tributors to generate one without needing these dependencies.
To generate one, if you are sitting in the root of your repository, then you don't need
to provide a name:

```bash
$ tributors init allcontrib 
INFO:allcontrib:Generating .all-contributorsrc for con/tributors
```

Of course if the file already exists, you will need to use `--force`

```bash
$ tributors init allcontrib 
.all-contributorsrc exists, set --force to overwrite.
```

If you cann't parse the name from the repository, you can either define it on
the command line:

```bash
$ tributors init allcontrib --repo singularityhub/sregistry
INFO:a2z:Generating .all-contributorsrc
```

or export it to the environment as `GITHUB_REPOSITORY` (this is how it would be discovered
during a GitHub workflow run).

```bash
export GITHUB_REPOSITORY=singularityhub/sregistry
$ tributors init allcontrib
INFO:allcontrib:Generating .all-contributorsrc
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

#### .zenodo.json

If you want to generate a fresh Zenodo.json, you can do that as follows:

```bash
$ tributors init zenodo --doi 10.5281/zenodo.1012531
```

You can also change the zenodo.json file from the default, for example, if you
are generating one in a subfolder:

```bash
$ tributors init zenodo --doi 10.5281/zenodo.1012531 --zenodo-file subfolder/.zenodo.json
```

And akin to the all contributors parser, the client will either extract
the GitHub repository name directly via git, or you can export it to 
 `GITHUB_REPOSITORY`. By default, we parse contributors
from the GitHub API, and include the creators already defined in Zenodo.
You will need this `.zenodo.json` file to exist in order to update it.


### 3. Update contributors

Now that we've initialized one or more files and possibly also have a .tributors
lookup (if one of the parsers generates it on init) we would want to use
the GitHub API to discover contributors to the repository,
for either both the `.all-contributorsrc` and the `.zenodo.json`, or just one of the two.
Note that you can read more about the [.tributors]({{ site.baseurl }}/docs/tributors) file, and notably
you can edit it to add or change metadata that you want then used across your
files.

#### Update all

If you want to update both the allcontributors file and the zenodo.json (or more
generally all client parsers), you can kill two birds with one stone (and essentially cache the GitHub API request) and do the following:

```bash
$ tributors update all
INFO:zenodo:Updating .zenodo.json
INFO:allcontrib:Updating .all-contributorsrc
```

#### Update (auto)

If you have a repository with one or more default contributor files, you can
update all of these files that are detected by leaving out the parser name:

```bash
$ tributors update
```

For an update, each parser will load cached metadata, and then update the 
contributor metadata file in question (e.g., a .zenodo.json) with new or
updated fields.


#### Update allcontributors

It's suggested that you export a `GITHUB_TOKEN` to increase your API limits (if necessary).

```bash
$ tributors update allcontrib
INFO:allcontrib:Updating .all-contributorsrc
```

You can optionally set a minimum number of contributors threshold to add (defaults to 1), or
a string to represent the kind of contribution (defaults to "core")

```bash
$ tributors update allcontrib --thresh 10 --allcontrib-type doc
```

or change the file path

```bash
$ tributors update allcontrib --thresh 10 --allcontrib-type doc --allcontrib-file subfolder/.all-contributorsrc
```

If you give an invalid type it will tell you:

```bash
$ tributors update allcontrib --thresh 10 --allcontrib-type pizza
INFO:allcontrib:Updating .all-contributorsrc
Invalid contribution type pizza. See https://allcontributors.org/docs/en/emoji-key for types.
```

Also note that GitHub bots are not included as contributors, and they are indicated with
"[bot]" in the name. If you find that you hit the API limit, then you will see this:

```bash
$ tributors update allcontrib
INFO:allcontrib:Updating .all-contributorsrc
Response 403: rate limit exceeded, cannot retrieve user RonaldEnsing.
```

and should export a `GITHUB_TOKEN` to increase it.

#### Update zenodo.json

Here is how to update a .zenodo.json that must already exist.

```bash
$ tributors update zenodo
INFO:zenodo:Updating .zenodo.json
```

You can also provide the filename via `--zenodo-file` if different from the default.

## GitHub Workflows

Since [all-contributors](https://github.com/all-contributors) requires node,
you might find it easiest to interact with the tool via a GitHub action.
You can see examples in the [examples](https://github.com/con/tributors/tree/master/examples) folder.
Inputs are listed below.

#### Inputs

| name | description | required | default |
|------|-------------|----------|---------|
| parsers | a space separated list of parsers (e.g., "zenodo allcontrib") or just "all" | false | all | 
| zenodo_file | .zenodo.json to update. If does not exist, must define zenodo_doi | false | .zenodo.json | 
| zenodo_doi | Zenodo DOI needed for init. Leave unset to skip init. | false | unset | 
| log_level | Log level to use, one of INFO, DEBUG, CRITICAL, ERROR, WARNING, FATAL (default INFO) | false | INFO | 
| threshold | the minimum number of contributions required to add a user | false | 1 | 
| force | if files exist, force overwrit | false | false |
| allcontrib_file |The all contributors file | false | .all-contributorsrc |
| allcontrib_type |Contribution type, which defaults to "code" if not set. | false | code |
| allcontrib_skip_generate | skip running all-contributors generate | false | false |
| codemeta-file | the codemeta file to update, if defined | false | unset |

If you aren't familiar with all-contributors, you'll need to add some
[commenting in your repository README](https://allcontributors.org/docs/en/cli/usage)
so the client knows where to write.
