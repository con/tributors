---
layout: page
title: Tributors
permalink: /
---

![{{ site.baseurl }}/assets/img/logo.png]({{ site.baseurl }}/assets/img/logo.png)

## What is tributors?

Tributors is a Python library and GitHub action that helps you to pay tribute to your
contributors. Tribute interacts with several well-known repository metadata files:

 - [all-contributors](https://github.com/all-contributors)
 - [Zenodo](https://zenodo.org)
 - [CodeMeta](https://codemeta.github.io/)

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

Tributors uses the GitHub API, Orcid API, and Zenodo API to update your contributor
files. You can use it locally, via a Docker container, or GitHub Workflow.
See the {% include doc.html name="Getting Started" path="getting-started" %} page to
get started. If you would like to request a feature or contribute please
[Open an issue]({{ site.repo }}/issues).
