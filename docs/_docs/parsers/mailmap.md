---
title: Mailmap
description: How to interact with a Mailmap file
---

# MailMap

A mailmap file (typically .mailmap) can be used as a lookup to match emails
with names, so it's a good resource to look to update the shared [.tributors]({{ site.baseurl }}/docs/tributors)
cache. If you haven't already, make sure that you [install tributors]({{ site.baseurl }}/docs/getting-started#1-install-tributors).
Here we show basic commands for interacting with the allcontrib generator, and a table of optional arguments.

## Optional Arguments

| name | description | required | default |
|------|-------------|----------|---------|
| `--mailmap-file` | .mailmap to use as a lookup | false | .mailmap | 

## Update .tributors

Let's say that we have a local mailmap file, it might look like this:

```
Yaroslav O. Halchenko <debian@onerussian.com>
Yaroslav O. Halchenko <site-github-private@onerussian.com>
Valentina Borghesani <vborghe@users.noreply.github.com>
Marie-Luise Kieseler <kieseler.gr@dartmouth.edu>
Cyril Pernet <wamcyril@gmail.com>
Cyril Pernet <cyril.pernet@ed.ac.uk>
Stephan Heunis <jsheunis@gmail.com>
P.-J. Toussaint <4642250+pjtoussaint@users.noreply.github.com>
```

We would be able to update our .tributors file doing the following:

```bash
$ tributors update-lookup mailmap
```

And if you want it auto-discovered (with other known files) you can just do:

```bash
$ tributors update-lookup
```

You can also provide the filename via `--mailmap-file` if different from the default.
