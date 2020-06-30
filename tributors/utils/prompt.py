"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


enter_input = getattr(__builtins__, "raw_input", input)


def request_input():
    """Wait for the user to input some string, optionally with multiple lines.
    """
    lines = []

    # The message can be multiple lines
    while True:
        try:
            line = enter_input()
        except EOFError:
            break
        if line:
            lines.append(line)

    return "\n".join(lines)
