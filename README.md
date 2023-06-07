# tributors

![docs/assets/img/logo.png](https://raw.githubusercontent.com/con/tributors/master/docs/assets/img/logo.png)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[Documentation](https://con.github.io/tributors/)

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

Tributors uses the GitHub API, Zenodo API, and Orcid API to look up shared identifiers
for common metadata services like all contributors, Zenodo, and CodeMeta. The
tool is available for local or container usage, and as a GitHub Action (see the [examples](examples) folder).
See the full [documentation](https://con.github.io/tributors/) for getting started.


## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="www.onerussian.com"><img src="https://avatars3.githubusercontent.com/u/39889?v=4?s=100" width="100px;" alt="Yaroslav Halchenko"/><br /><sub><b>Yaroslav Halchenko</b></sub></a><br /><a href="https://github.com/con/tributors/commits?author=yarikoptic" title="Code">💻</a> <a href="https://github.com/con/tributors/commits?author=yarikoptic" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://vsoch.github.io"><img src="https://avatars0.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt="Vanessasaurus"/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/con/tributors/commits?author=vsoch" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pgrimaud"><img src="https://avatars1.githubusercontent.com/u/1866496?v=4?s=100" width="100px;" alt="Pierre Grimaud"/><br /><sub><b>Pierre Grimaud</b></sub></a><br /><a href="https://github.com/con/tributors/commits?author=pgrimaud" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vuillaut"><img src="https://avatars.githubusercontent.com/u/4263646?v=4?s=100" width="100px;" alt="vuillaut"/><br /><sub><b>vuillaut</b></sub></a><br /><a href="https://github.com/con/tributors/commits?author=vuillaut" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jwodder"><img src="https://avatars.githubusercontent.com/u/98207?v=4?s=100" width="100px;" alt="jwodder"/><br /><sub><b>jwodder</b></sub></a><br /><a href="https://github.com/con/tributors/commits?author=jwodder" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
