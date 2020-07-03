---
title: Parsers
description: Metadata parsers provided by tributors
tags:
 - zenodo
 - allcontrib
 - parser
---

# Parsers

A parser is generally a service (API, command line tool, or similar) that helps
to generate some kind of metadata file to list your contributors. Tributors
currently supports several interfaces to common metadata formats:

 - [All-Contributors](allcontrib)
 - [Zenodo](zenodo)
 - [Codemeta](codemeta)

# Resources

In addition to being able to update the contributor metadata file types listed
above, tributors also can use some resource as a lookup to update the shared
[.tributors]({{ site.baseurl }}/docs/tributors) cache. All of the parsers
above can be used in this manner, and in addition, the following parsers
allow for updating the metadata (but doesn't have it's own contributors file).

 - [Mailmap](mailmap)

Would you like to see another metadata type? Please [open an issue])({{ site.repo }}/issues/new).
