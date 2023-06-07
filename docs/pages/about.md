---
title: About
permalink: /about/
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
Tributors will allow you to programmatically create and update these files.
By way of using a shared cache, a `.tributors` file that can store common
identifiers, it becomes easy to update several of these metadata files at once.
You can set criteria such as a threshold for contributions to add a contributor,
export an Orcid ID token to ensure that you have Orcid Ids where needed,
or use an interactive mode to make decisions as you go.

## How does it work?

Tributors uses the GitHub API, Orcid API, and Zenodo API to update your contributor
files. You can use it locally, via a Docker container, or GitHub Workflow.
See the {% include doc.html name="Getting Started" path="getting-started" %} page to
get started. 

## How was it started?

In late June 2020, [@yarikoptic](https://github.com/yarikoptic) [opened an issue](https://github.com/con/tributors/issues/1)
to request some kind of tool to convert between the all-contributors metadata file
(.all-contributorsrc) and a Zenodo metadata file (.zenodo.json). 
[@vsoch](https://github.com/vsoch) jumped on the opportunity, and decided
to make a more modular, robust solution that would allow sharing of metadata
between multiple providers. The original problem statement is included below.

### Problem Statement

https://github.com/all-contributors is an awesome project which helps to collect and display contributors in github hosted projects.
It produces .all-contributorsrc (json) such as

```
{
  "files": [
    "README.md"
  ],
  "imageSize": 100,
  "commit": false,
  "contributors": [
    {
      "login": "yarikoptic",
      "name": "Yaroslav Halchenko",
      "avatar_url": "https://avatars3.githubusercontent.com/u/39889?v=4",
      "profile": "http://www.onerussian.com",
      "contributions": [
        "infra",
        "projectManagement",
        "code",
        "content",
        "review",
        "maintenance"
      ]
    },
    {
      "login": "adswa",
      "name": "Adina Wagner",
      "avatar_url": "https://avatars1.githubusercontent.com/u/29738718?v=4",
      "profile": "http://www.adina-wagner.com",
      "contributions": [
        "infra"
      ]
    },
..
  ],
  "contributorsPerLine": 7,
  "projectName": "open-brain-consent",
  "projectOwner": "con",
  "repoType": "github",
  "repoHost": "https://github.com",
  "skipCi": true
}
```

which contains pointers to github logins, names, their contributions etc.

There is also zenodo.org which is used by many projects to get citeable references for their research software.  See e.g. our DataLad's [.zenodo.json](https://github.com/datalad/datalad/blob/master/.zenodo.json) for an example.  A typical entry in that one would contain also affiliation and an [orcid id](https://orcid.org/):

```json
{
      "affiliation": "Dartmouth College, Hanover, NH, United States",
      "name": "Halchenko, Yaroslav O.",
      "orcid": "0000-0003-3456-2493"
},
```

ORCID has an API: https://members.orcid.org/api/tutorial/search-orcid-registry allowing for search of an orcid record via email.
GitHub has an API allowing to get email for the account: https://developer.github.com/v3/users/ .

So we just need a helper tool to create/update/maintain .zenodo.json based on allcontributors by querying github and orcid for the missing fields.

The tool (if not a github bot?!) could retain a local cache or even some global registry of mapping from github id to orcid id (with more or less up to date affiliation)

## Support

If you would like to request a feature or contribute please
[Open an issue]({{ site.repo }}/issues).
