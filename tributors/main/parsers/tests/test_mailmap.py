from ..mailmap import MailmapParser

import pytest


def test_simple(tmp_path):
    mailmap = tmp_path / ".mailmap"
    mailmap.write_text("""
Joe Smith <joe.smith@gmail.com>
Neuroimaging Community <committer@example.com>
Neuroimaging Community <committer@example.com> blah <blah@example.com>
Neuroimaging Community <committer@example.com> <test@example.com>""")
    parser = MailmapParser(str(mailmap))
    r = parser.load_data()
    assert r == {
        'joe.smith@gmail.com': {'name': 'Joe Smith'},
        'committer@example.com': {'name': 'Neuroimaging Community'},
        'blah@example.com': {'name': 'Neuroimaging Community'},
        'test@example.com': {'name': 'Neuroimaging Community'}
    }


def test_noname(tmp_path):
    mailmap = tmp_path / ".mailmap"
    l = " <joe.smith@gmail.com>"
    mailmap.write_text(l)
    with pytest.raises(ValueError) as cme:
        r = MailmapParser(str(mailmap)).load_data()
    assert l in str(cme.value)

