# tributors

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## What is tributors?

Tributors is a Python library and GitHub action that helps you to pay tribute to your
contributors. Tribute interacts with several well-known repository metadata files:

 - [all-contributors](https://github.com/all-contributors)
 - [Zenodo](https://zenodo.org)
 - [CodeMeta](https://codemeta.github.io/) **under development**

Each of the services above allows you to generate some kind of metadata file
that has one or more repository contributors. This file typically needs to be
generated and updated manually, and this is where tributors comes in to help!
Tributors will allow you to programatically create and update these files.
By way of using a shared cache, a `.tributors` file that can store common
identifiers, it becomes easy to update several of these metadata files at once.
You can set criteria such as a threshold for contributions to add a contributor,
export an Orcid ID token to ensure that you have Orcid Ids where needed,
or use an interactive mode to make decisions as you go.

## How does it work?

Tributors uses the following sources of information to update your contributor
files.

### GitHub API

Since these files are served in GitHub repositories, it's fairly easy to
retrieve repository contributors using the GitHub API in both cases.

### Orcid

Given that you provide an Orcid token and secret to request API tokens, we can find [Orcid records](https://members.orcid.org/api/tutorial/read-orcid-records) based on email addresses.

### Zenodo

Zenodo also has a [rest API](https://developers.zenodo.org/) that can be used to create an initial `.zenodo.json` for a repository. 

The GitHub Action details are included below. See the [docs](docs) for more detailed
usage, both on your local machine, and via a Docker container.

## GitHub Action

Since [all-contributors](https://github.com/all-contributors) requires node,
you might find it easiest to interact with the tool via a GitHub action.
You can see examples in the [examples](examples) folder.

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

If you aren't familiar with all-contributors, you'll need to add some
[commenting in your repository README](https://allcontributors.org/docs/en/cli/usage)
so the client knows where to write.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->


## @vsoch TODO

 - an example should be added to push to a repository / open PR
