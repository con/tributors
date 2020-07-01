---
title: Zenodo
description: How to add interact with Zenodo
---

# Zenodo

[Zenodo](https://zenodo.org) allows you to create digital object identifiers (DOIs) for
artifacts such as software, and even connect directly to code releases on version
control (like GitHub!) A somewhat known (not official, but used) feature is the ability
to define a `.zenodo.json` file in a repository to update a record. This file isn't
well documented, so tributors makes it easy to generate and then update using the
GitHub API. If you haven't already, make sure that you [install tributors]({{ site.baseurl }}/docs/getting-started#1-install-tributors).
Here we show basic commands for interacting with the allcontrib generator, and a table of optional arguments.

## Optional Arguments

| name | description | required | default |
|------|-------------|----------|---------|
| `--zenodo_file` | .zenodo.json to update. If does not exist, must define zenodo_doi | false | .zenodo.json | 
| `--zenodo_doi` | Zenodo DOI needed for init. Leave unset to skip init. | false | unset | 
| `--log-level` | Log level to use, one of INFO, DEBUG, CRITICAL, ERROR, WARNING, FATAL (default INFO) | false | INFO | 
| `--thresh` | the minimum number of contributions required to add a user | false | 1 | 
| `--force` | if files exist, force overwrit | false | false |


## Init .zenodo.json

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

### The .tributors file

After you run this command, you'll also notice you have a `.tributors` file
in your repository. You can choose to add this to version control or not - it contains
shared metadata between the services. Read more about the [tributors file here]({{ site.baseurl }}/docs/tributors).

## Update

Now that we've initialized one or more files and possibly also have a .tributors
lookup (if one of the parsers generates it on init) we would want to use
the GitHub API to discover contributors to the repository.
Here is how to update a .zenodo.json that must already exist.

```bash
$ tributors update zenodo
INFO:zenodo:Updating .zenodo.json
```

You can also provide the filename via `--zenodo-file` if different from the default.
