---
title: Examples
tags: 
 - allcontrib
 - zenodo
 - docker
description: Getting started with examples
---

# Examples

The following are basic examples for using tributors on the command line.
For these examples, we've exported an `ORCID_TOKEN` [see environment details]({{ site.baseurl }}/docs/getting-started#environment).
to parse Orcid identifiers from emails.

## Create a Zenodo JSON

First, clone your repository or change directory to it.

```bash
$ git clone https://github.com/con/open-brain-consent
cd open-brain-consent
```

Then generate an empty zenodo.json.

```bash
$ tributors init zenodo
```

Take a look! If you didn't export an Orcid id, you likely will just see a list of
names. But if you did, you should have affiliations and orcids.

```json
cat .zenodo.json 
{
    "creators": [
        {
            "name": "Stefan Appelhoff",
            "affiliation": "Max Planck Institute for Human Development",
            "orcid": "0000-0001-8002-0877"
        },
...
        {
            "name": "Peer Herholz",
            "affiliation": "McGill University",
            "orcid": "0000-0002-9840-6257"
        }
    ],
    "upload_type": "software",
    "keywords": []
}
```

If you just have names, try running an update to update from GitHub metadata.

```bash
$ tributors update
```

The default functionality will add identifiers _from_ GitHub. However you
could also have initialized from a .tributors lookup. Now that we have one,
let's delete the .zenodo.json and redo the action:

```bash
$ rm .zenodo.json
$ tributors init zenodo --from tributors
```

## Update a Zenodo.json from an all-contributors file

We again could initialize a zenodo.json directly from an all-contributorsrc:

```bash
$ rm .zenodo.json
$ tributors init zenodo --from allcontrib
```

And then update from GitHub (default) - these are the same.

```bash
$ tributors update zenodo
$ tributors update zenodo --from github
```

If you are looking for a specific use case or example, please [open an issue](https://github.com/con/tributors/issues).


