#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import pytest


def test_queries(tmp_path):
    """test that changing order of First Last and Last, First returns same result
    """
    from tributors.main.orcid import get_orcid, record_search

    orcid_id = "0000-0003-3456-2493"

    # Test different orders of name
    result = get_orcid(email=None, name="Yaroslav Halchenko")
    assert result == orcid_id
    result = get_orcid(email=None, name="Halchenko, Yaroslav")
    assert result == orcid_id

    # Test lookup by email
    result = get_orcid(email="debian@onerussian.com")
    assert result == orcid_id

    # Test search for other name
    result = get_orcid(email=None, name="Ярослав Олеговіч Гальченко")
    assert result == orcid_id

    # Test returning None
    result = get_orcid(email=None, name="Zumbudda")
    assert not result

    # TODO this looks like the API is changed
    # Test find by other-names (can't do because more than one result)
    # result = get_orcid(email=None, name="Horea Christian")
    # assert result == "0000-0001-7037-2449"
