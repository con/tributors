"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


enter_input = getattr(__builtins__, "raw_input", input)


def request_input():
    """Wait for the user to input some string, optionally with multiple lines."""
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


def choice_prompt(prompt, choices, choice_prefix=None, multiple=False):
    """Ask the user for a prompt, and only return when one of the requested
    options is provided.

    Parameters
    ==========
    prompt: the prompt to ask the user
    choices: a list of choices that are valid.
    multiple: allow multiple responses (separated by spaces)
    """
    choice = None
    print(prompt)

    # Support for Python 2 (raw_input)
    get_input = getattr(__builtins__, "raw_input", input)

    if not choice_prefix:
        choice_prefix = "/".join(choices)
    message = "[%s] : " % (choice_prefix)

    while choice not in choices:
        choice = get_input(message).strip()

        # If multiple allowed, add selection to choices if includes all vaid
        if multiple is True:
            contenders = choice.strip().split(" ")
            if all(x in choices for x in contenders):
                choices.append(choice)
        message = "Please enter a valid option in [%s]" % choice_prefix
    return choice
