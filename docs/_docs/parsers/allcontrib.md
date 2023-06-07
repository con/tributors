---
title: All Contributors
description: How to add interact with all Contributors
---

# All-Contributors

[All contributors](https://allcontributors.org/docs/en/cli/installation) provides a client,
and bot to generate an `.allcontributorsrc` file that can easily render one or more snippets
in markdown files into a beautiful badge or table of contributors. Tributors
supports creating this initial file, and then updating it from th GitHub API.
If you haven't already, make sure that you [install tributors]({{ site.baseurl }}/docs/getting-started#1-install-tributors).
Here we show basic commands for interacting with the allcontrib generator, and a table of optional arguments.

## Optional Arguments

| name | description | required | default |
|------|-------------|----------|---------|
| `--allcontrib-type` | the [type](https://allcontributors.org/docs/en/emoji-key) of contribution | false | unset | 
| `--allcontrib-file` | the allcontributors file, if changed from default | false | .all-contributorsrc | 
| `--log-level` | Log level to use, one of INFO, DEBUG, CRITICAL, ERROR, WARNING, FATAL (default INFO) | false | INFO | 
| `--thresh` | the minimum number of contributions required to add a user | false | 1 | 
| `--force` | if files exist, force overwrit | false | code |

## Init .all-contributorsrc

If you don't have a file yet, you'll want to use `init`:

```bash
$ tributors init allcontrib 
INFO:allcontrib:Generating .all-contributorsrc for con/tributors
```

Of course if the file already exists, you will need to use `--force`

```bash
$ tributors init allcontrib 
.all-contributorsrc exists, set --force to overwrite.
```

If you can't parse the name from the repository, you can either define it on
the command line:

```bash
$ tributors init allcontrib --repo singularityhub/sregistry
INFO:a2z:Generating .all-contributorsrc
```

or export it to the environment as `GITHUB_REPOSITORY`:

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

Note that the list of files includes files that the all-contributors client
will render content into. For example, here are the snippets that you would
include to render a badge and table - put these in your README.md (or other
files) that you want rendered.

```markdown
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->
```

Read more about this
[commenting in your repository README](https://allcontributors.org/docs/en/cli/usage)
so the client knows where to write. 

### The .tributors file

After you run this command, you'll also notice you have a `.tributors` file
in your repository. You can choose to add this to version control or not - it contains
shared metadata between the services. Read more about the [tributors file here]({{ site.baseurl }}/docs/tributors).

## Update

Now that we've initialized one or more files and possibly also have a .tributors
lookup (if one of the parsers generates it on init) we would want to use
the GitHub API to discover contributors to the repository. Before you do this,
it's suggested that you export a `GITHUB_TOKEN` to increase your API limits (if necessary).

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

and definitely then should export a `GITHUB_TOKEN` to increase it!

## Update .tributors

Let's say that we have a local .all-contributorsrc, and we just want to use it to update our
.tributors file. We could do:

```bash
$ tributors update-lookup allcontrib
```

And if you want it auto-discovered (with other known files) you can just do:

```bash
$ tributors update-lookup
```


## Generate 

Once you've update your .all-contributorsrc, you can either [install](https://allcontributors.org/docs/en/cli/overview) the
client and then run generate:

```bash
all-contributors generate
```

Or use the docker container to provide the client to do it for you:

```bash
docker run -it --entrypoint bash -v $PWD/:/data {{ site.docker_container }}
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
code for the user is found here). But your data, via the command above,
will be mounted at data. So let's change directory there:

```bash
cd /data
```

And then run generate using the client. Your README.md (or other file you've
marked for parsing) will be updated with your table or badge!

```bash
cli.js generate
```
