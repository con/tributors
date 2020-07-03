---
title: The Tributors File
tags: 
 - allcontrib
 - zenodo
 - docker
description: The .tributors file is a shared metadata file.
---

# The Tributors File

After running a `tributors update`, you'll save a single metadata file in your repository that includes common fields
to use to update other metadata files, the ".tributors" file. As an example, here we see a file generated
after an initial run - we index by the GitHub username since on GitHub that is our
"unit of truth." These are a few entries for Singularity Registry Server:

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessasaurus",
        "bio": "I'm the Vanessasaurus!",
        "blog": "https://vsoch.github.io"
    },
    "tschoonj": {
        "name": "Tom Schoonjans",
        "bio": "I'm a research software engineer working @rosalindfranklininstitute, and am passionate about developing quality open source software.",
        "blog": "tschoonj.github.io"
    },
    "Aneoshun": {
        "name": "Antoine Cully",
        "blog": "antoinecully.com"
    },
    "yarikoptic": {
        "name": "Yaroslav Halchenko",
        "email": "debian@onerussian.com",
        "bio": "Cheers!",
        "blog": "www.onerussian.com"
    },
    "victorsndvg": {
        "name": "victorsndvg",
        "email": "victorsv@gmail.com",
        "bio": "Scientific software engineer",
        "blog": "http://sourceforge.net/u/victorsndvg/profile/"
    },
    "RonaldEnsing": {
        "name": "Ronald Ensing"
    }
}
```

You'll notice that we only save fields that we can find (e.g., if no email is
exposed, it won't be defined. 

## Manual Update

At this point we might want to manually update metadata
to our liking - any particular subfield for a user won't be overwritten if it's
already defined. For example, my GitHub name from the API is "Vanessasaurus" and
I might want to put a different name for a "professional" repository:

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessa",
        "bio": "Research Software Engineer at Stanford University",
        "blog": "https://vsoch.github.io"
    },
    "tschoonj": {
        "name": "Tom Schoonjans",
        "bio": "I'm a research software engineer working @rosalindfranklininstitute, and am passionate about developing quality open source software.",
        "blog": "tschoonj.github.io"
    },
    "Aneoshun": {
        "name": "Antoine Cully",
        "blog": "antoinecully.com"
    },
    "yarikoptic": {
        "name": "Yaroslav Halchenko",
        "email": "debian@onerussian.com",
        "bio": "Cheers!",
        "blog": "www.onerussian.com"
    },
    "victorsndvg": {
        "name": "victorsndvg",
        "email": "victorsv@gmail.com",
        "bio": "Scientific software engineer",
        "blog": "http://sourceforge.net/u/victorsndvg/profile/"
    },
    "RonaldEnsing": {
        "name": "Ronald Ensing"
    }
}
```

You can also add missing information, for example, affiliations or orcid identifiers.

```bash
$ cat .tributors 
{
    "vsoch": {
        "name": "Vanessa",
        "bio": "I'm the Vanessasaurus!",
        "affiliation": "Research Software Engineer at Stanford University",
        "blog": "https://vsoch.github.io"
    }
}
```

Notice that for all operations, if a field is already defined it won't be over-written, as you might have edited
it and don't want to lose those edits. You of course are free to update or otherwise
manually edit all of these files to your liking.

## Automated Update

Along with providing parsers to update specific contributor files (e.g., .zenodo.json uses
a Zenodo parser) tributors also provides these parsers (and other resources for metadata)
that can be used to update the .tributors file. For example, a `.mailmap` file would have a mapping between names
and emails, and any of the parsers that have contributors files (e.g., Zenodo, All Contributors,
or CodeMeta) can also be used as metadata lookups without touching a contributors
metadata file. We do this by way of the `update-lookup` command. Let's say that we 
want to just update our .tributors shared metadata cache from known lookups
we find in the present working directory:

```bash
# auto-detect lookup files in the present working directory
$ tributors update-lookup
```
or from a particular source such as a mailmap file:
```
# target a specific metadata file, .mailmap
$ tributors update-lookup mailmap
```

This would update fields in our .tributors file, and then we could run `tributors update`
to pass on new metadata files into our contributor files. To read more about resources
that are available to update the .tributors file, see the [parsers]({{ site.baseurl }}/docs/parsers)
documentation.


## Fields

The following fields are known to a `.tributors` file

 - **name**: the name of the contributor
 - **email**: the email of the contributor
 - **bio**: a short bio for the contributor
 - **affiliation**: institution or other affiliation (usually comes from Orcid)
 - **blog**: a website or blog address
 - **orcid**: the orcid identifier for the contributor

For example, you might generate this file automatically to start, update
it in a text editor, and then easily update all of your other contributor files. Neat!
