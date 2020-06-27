# allcontributors-to-zenodo

## Problem statement

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

There is also zenodo.org which is used by many projects to get citeable references for their research software.  See e.g. our DataLad's [.zenodo.json](https://github.com/datalad/datalad/blob/master/.zenodo.json) for an example.  A typical entry in that one would contain also affiliation and an [orcid id]():

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
