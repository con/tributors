"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.21"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "tributors"
PACKAGE_URL = "http://www.github.com/con/tributors"
KEYWORDS = "contributions, tributes"
DESCRIPTION = "give tribute to your repository contributors."
LICENSE = "LICENSE"

################################################################################
# Global requirements


INSTALL_REQUIRES = (("requests", {"min_version": "2.23.0"}),)
CODEMETA_REQUIRES = (("codemetapy", {"min_version": "0.3.2"}),)
TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

ALL_REQUIRES = INSTALL_REQUIRES + CODEMETA_REQUIRES
