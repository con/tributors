#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import pytest


def test_from_resources_default(tmp_path):
    """test that from resources returns appropriate resources
    """
    from tributors.main import TributorsClient

    client = TributorsClient()

    # Default should be from GitHub repo
    logins = client.get_resource_lookups()
    assert logins["login"]
    comparator = client.get_resource_lookups(["github"])
    assert comparator == logins


def test_parser_allcontrib(tmp_path):
    """test each executor type with the filesystem
    """
    from tributors.main.parsers import get_named_parser

    # Prepare from resources
    from_resources = {"login": set(["vsoch", "manbat", "yarikoptic"])}

    # Create a dummy output file
    allcontrib = os.path.join(str(tmp_path), ".all-contributorsrc")
    params = {"--allcontrib-file": allcontrib}
    repo = "singularityhub/sregistry"

    # Output file should not exist before inint
    assert not os.path.exists(allcontrib)
    parser = get_named_parser("allcontrib", repo=repo, params=params)
    result = parser.init()

    # Trying to write existing file raises system exit
    with pytest.raises(SystemExit):
        result = parser.init()
    assert os.path.exists(allcontrib)

    # Ensure the result matches the template
    template = {
        "projectName": "sregistry",
        "projectOwner": "singularityhub",
        "repoType": "github",
        "repoHost": "https://github.com",
        "files": ["README.md"],
        "imageSize": 100,
        "commit": True,
        "commitConvention": "none",
        "contributors": [],
        "contributorsPerLine": 7,
    }
    assert template == result

    # Test adding contributors, default from GitHub
    result = parser.update(from_resources=from_resources, save=False)
    assert len(result["contributors"]) == 3
    for login in [x["login"] for x in result["contributors"]]:
        assert login in from_resources["login"]

    # Test adding by email or orcid should not change output
    byemail = parser.update(
        from_resources={"email": set(["poodles@dog.com"])}, save=False
    )
    byorcid = parser.update(
        from_resources={"orcid": set(["0000-0000-0000-0000"])}, save=False
    )
    assert byemail == byorcid == result


def test_parser_zenodo(tmp_path):
    """test each executor type with the filesystem
    """
    from tributors.main.parsers import get_named_parser

    # Prepare from resources
    from_resources = {"login": set(["vsoch", "manbat", "yarikoptic"])}

    # Create a dummy output file
    zenodo = os.path.join(str(tmp_path), ".zenodo.json")
    params = {"--zenodo-file": zenodo}
    repo = "singularityhub/sregistry"

    # Output file should not exist before init
    assert not os.path.exists(zenodo)
    parser = get_named_parser("zenodo", repo=repo, params=params)
    result = parser.init(save=False)
    assert len(result["creators"]) == 0

    # With from resources, should add to creators
    result = parser.init(from_resources=from_resources)
    assert len(result["creators"]) == 3

    # Trying to write existing file raises system exit
    with pytest.raises(SystemExit):
        result = parser.init()
    assert os.path.exists(zenodo)

    # Ensure the result matches the template
    template = {
        "creators": [{"name": "yarikoptic"}, {"name": "manbat"}, {"name": "vsoch"}],
        "upload_type": "software",
        "keywords": [
            "singularity",
            "management",
            "containers",
            "registry",
            "singularity-containers",
            "singularityhub",
        ],
    }
    assert set(template["keywords"]) == set(result["keywords"])
    assert template["upload_type"] == result["upload_type"]
    assert len(result["creators"]) == 3
    for login in [x["name"] for x in result["creators"]]:
        assert login in from_resources["login"]

    # Test adding contributors, default from GitHub
    parser = get_named_parser("zenodo", repo=repo, params=params)
    from_github = parser.update(from_resources=from_resources, save=False)
    assert from_github == result

    # Test adding by email or orcid should not change output
    parser = get_named_parser("zenodo", repo=repo, params=params)
    byemail = parser.update(
        from_resources={"email": set(["poodles@dog.com"])}, save=False
    )
    assert byemail == result

    # Support adding by orcid, if not known
    parser = get_named_parser("zenodo", repo=repo, params=params)
    byorcid = parser.update(
        from_resources={"orcid": set(["0000-0000-0000-0000"])}, save=False
    )
    assert len(byorcid["creators"]) == 4
