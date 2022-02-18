"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import json
import os
import tempfile


def write_json(json_obj, filename, pretty=True):
    """write_json will write a json object to file, pretty printed

    Arguments:
     - json_obj (dict) : the dict to print to json
     - filename (str)  : the output file to write to
    """
    with open(filename, "w", encoding="utf8") as filey:
        if pretty:
            filey.writelines(
                json.dumps(
                    json_obj, indent=4, ensure_ascii=False, separators=(",", ": ")
                )
            )
        else:
            filey.writelines(json.dumps(json_obj), ensure_ascii=False)
    return filename


def read_json(input_file):
    """Read json from an input file.

    Arguments:
      - input_file (str) : the filename to read
    """
    with open(input_file, "r") as filey:
        data = json.loads(filey.read())
    return data


def read_file(filename, readlines=True):
    """write_file will open a file, "filename" and write content
    and properly close the file.

    Arguments:
      - filename (str) : the filename to read
      - readlines (bool) : read lines of the file (vs all raw)
    """
    with open(filename, "r") as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def write_file(filename, content):
    """write some content to a filename"""
    with open(filename, "w") as fd:
        fd.writelines(content)
    return filename


def get_tmpfile(prefix="tributors-"):
    """get a temporary file with an optional prefix. By default, the file
    is closed (and just a name returned).

    Arguments:
     - prefix (str) : prefix with this string
    """
    tmpdir = tempfile.gettempdir()
    prefix = os.path.join(tmpdir, os.path.basename(prefix))
    fd, tmp_file = tempfile.mkstemp(prefix=prefix)
    os.close(fd)
    return tmp_file
