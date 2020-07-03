---
title: CodeMeta
description: How to add interact with CodeMeta
---

# CodeMeta

[CodeMeta](https://codemeta.github.io) is likely the best source of metadata, as the files
typically have emails and orcid ids. Since CodeMeta already provide several high
quality [generation tools]() we don't provide an init function here, however the
`update` function can serve to update your .tributors metadata file and the 
codemeta file if an email, orcid, or name is missing.
If you haven't already, make sure that you [install tributors]({{ site.baseurl }}/docs/getting-started#1-install-tributors).
Here we show basic commands for interacting with the allcontrib generator, and a table of optional arguments.

## Optional Arguments

| name | description | required | default |
|------|-------------|----------|---------|
| `--codemeta-file` | the codemeta file, if changed from default | false | codemeta.json | 
| `--log-level` | Log level to use, one of INFO, DEBUG, CRITICAL, ERROR, WARNING, FATAL (default INFO) | false | INFO | 
| `--thresh` | the minimum number of contributions required to add a user | false | 1 | 
| `--force` | if files exist, force overwrit | false | code |

## Init codemeta

As mentioned above, there is no init defined because tools already exist! If you
run an init for codemeta you'll see this message:

```bash
$ tributors init codemeta
Codemeta provides several tools to generate this for you: https://codemeta.github.io/tools/
```

### The .tributors file

After you run this command, you'll also notice you have a `.tributors` file
in your repository. You can choose to add this to version control or not - it contains
shared metadata between the services. Read more about the [tributors file here]({{ site.baseurl }}/docs/tributors).

## Update

If you already have a codemeta.json or codemeta.jsonld, you can update it as follows
(and importantly, extract emails or orcids from it for user's that you've already
defined in your .tributors file):

```bash
$ tributors update codemeta
INFO:codemeta:Updating codemeta.json
```

You can also target a different filename;

```bash
$ tributors update codemeta --codemeta-file codemeta.jsonld
```

## Update .tributors

Let's say that we have a local codemeta.json, and we just want to use it to update our
.tributors file. We could do:

```bash
$ tributors update-lookup codemeta
```

And if you want it auto-discovered (with other known files) you can just do:

```bash
$ tributors update-lookup
```

For both of the above, since the cache is kept based on GitHub user id, we aren't able to store
codemeta entries unless they have an email or orcid that we can match
to an existing entry.
