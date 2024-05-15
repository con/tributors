"""

Copyright (C) 2020-2022 Vanessa Sochat.
              2024      Yaroslav O. Halchenko

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


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

    if not choice_prefix:
        choice_prefix = "/".join(choices)
    message = "[%s] : " % (choice_prefix)

    while choice not in choices:
        choice = input(message).strip()

        # If multiple allowed, add selection to choices if includes all valid
        if multiple is True:
            contenders = choice.strip().split(" ")
            if all(x in choices for x in contenders):
                choices.append(choice)
        message = "Please enter a valid option in [%s]" % choice_prefix
    return choice


