"""Extended os-release parsing coverage for distro.

Every instance here is built from a temporary os-release file with
lsb/uname disabled and a nonexistent distro-release file, so no test
depends on the host distribution. Probed behaviours pinned here:

* Single- and double-quoted values are unquoted; comments and
  blank lines are ignored; a bare ``EMPTY=`` line is kept as ``""``.
* ``VERSION="... (Codename)"`` yields both ``codename`` (from
  ``VERSION_CODENAME`` when present, which wins) and
  ``release_codename`` (from the parenthesised part of ``VERSION``).
* ``name(pretty=True)`` without a ``PRETTY_NAME`` builds
  ``"<name> <pretty version>"`` -- with an empty name that is just
  ``" <version>"`` (a leading space), as probed for Oracle Linux.
* ``singular``/``version`` fallbacks: a missing os-release file
  yields empty strings everywhere, not exceptions.
"""

import pytest

from distro import LinuxDistribution

UBUNTU = """PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
"""

ORACLE = """NAME="Oracle Linux"
VERSION="8.10"
ID="ol"
VERSION_ID="8.10"
ID_LIKE="rhel fedora"
"""

QUOTED = """NAME='Single Quoted'
ID="double"
VERSION_ID='1.2.3'
PRETTY_NAME="Pretty 'Quoted' Name"
"""

COMMENTS = """# a comment

ID=commented
#VERSION_ID="9"
EMPTY=
"""


def make(tmp_path, content):
    path = tmp_path / "os-release"
    path.write_text(content)
    return LinuxDistribution(
        os_release_file=str(path),
        distro_release_file="/nonexistent/nofile",
        include_lsb=False,
        include_uname=False,
    )


def test_ubuntu_full_profile(tmp_path):
    d = make(tmp_path, UBUNTU)
    assert d.id() == "ubuntu"
    assert d.name() == "Ubuntu"
    assert d.name(pretty=True) == "Ubuntu 24.04.5 LTS"
    assert d.version() == "24.04"
    assert d.version(pretty=True) == "24.04 (noble)"
    assert d.version_parts() == ("24", "04", "")
    assert (d.major_version(), d.minor_version(), d.build_number()) == ("24", "04", "")
    assert d.like() == "debian"
    assert d.codename() == "noble"
    assert d.linux_distribution() == ("Ubuntu", "24.04", "Noble Numbat")
    assert d.linux_distribution(full_distribution_name=False) == ("ubuntu", "24.04", "Noble Numbat")


def test_ubuntu_os_release_info_dict(tmp_path):
    d = make(tmp_path, UBUNTU)
    info = d.os_release_info()
    assert info["pretty_name"] == "Ubuntu 24.04.5 LTS"
    assert info["version_id"] == "24.04"
    assert info["codename"] == "noble"
    assert info["release_codename"] == "Noble Numbat"
    assert info["id_like"] == "debian"


def test_oracle_id_is_normalized(tmp_path):
    d = make(tmp_path, ORACLE)
    assert d.os_release_attr("id") == "ol"
    assert d.id() == "oracle"
    assert d.name() == "Oracle Linux"
    assert d.version() == "8.10"
    assert d.like() == "rhel fedora"
    assert d.codename() == ""


def test_oracle_pretty_name_without_pretty_name_has_leading_space(tmp_path):
    d = make(tmp_path, ORACLE)
    assert d.name(pretty=True) == " 8.10"


def test_quoted_values_are_unquoted(tmp_path):
    d = make(tmp_path, QUOTED)
    assert d.name() == "Single Quoted"
    assert d.id() == "double"
    assert d.version() == "1.2.3"
    assert d.version_parts() == ("1", "2", "3")
    assert d.name(pretty=True) == "Pretty 'Quoted' Name"


def test_comments_blank_lines_and_empty_values(tmp_path):
    d = make(tmp_path, COMMENTS)
    assert d.id() == "commented"
    assert d.version() == ""
    assert d.os_release_info() == {"id": "commented", "empty": ""}


def test_minimal_file_and_missing_file(tmp_path):
    d = make(tmp_path, "ID=testos\n")
    assert d.id() == "testos"
    assert d.name() == ""
    assert d.version() == ""
    assert d.info() == {
        "id": "testos",
        "version": "",
        "version_parts": {"major": "", "minor": "", "build_number": ""},
        "like": "",
        "codename": "",
    }
    missing = LinuxDistribution(
        os_release_file="/nonexistent/os-release",
        distro_release_file="/nonexistent/nofile",
        include_lsb=False,
        include_uname=False,
    )
    assert missing.id() == ""
    assert missing.info()["id"] == ""
    assert missing.version_parts() == ("", "", "")


def test_os_release_attr_missing_key_is_empty(tmp_path):
    d = make(tmp_path, UBUNTU)
    assert d.os_release_attr("nope") == ""


def test_parse_os_release_content_directly(tmp_path):
    import io

    d = make(tmp_path, UBUNTU)
    parsed = d._parse_os_release_content(
        io.StringIO('ID=foo\nNAME="Bar Baz"\n# c\nBADLINE\nVERSION_ID=1.0\n')
    )
    assert parsed == {"id": "foo", "name": "Bar Baz", "version_id": "1.0"}


def test_version_codename_beats_version_parentheses(tmp_path):
    content = (
        'NAME="X"\nID=x\nVERSION_ID="1.0"\n'
        'VERSION="1.0 (FromVersion)"\nVERSION_CODENAME=fromfield\n'
    )
    d = make(tmp_path, content)
    assert d.codename() == "fromfield"
    assert d.os_release_info()["release_codename"] == "FromVersion"


def test_empty_version_codename_means_no_codename(tmp_path):
    content = 'NAME="X"\nID=x\nVERSION_ID="1.0"\nVERSION_CODENAME=""\n'
    d = make(tmp_path, content)
    assert d.codename() == ""


def test_root_dir_layout(tmp_path):
    root = tmp_path / "root"
    (root / "etc").mkdir(parents=True)
    (root / "etc" / "os-release").write_text(UBUNTU)
    d = LinuxDistribution(root_dir=str(root))
    assert d.id() == "ubuntu"
    assert d.version() == "24.04"
    assert d.os_release_file == str(root / "etc" / "os-release")


def test_debian_version_file_via_root_dir(tmp_path):
    root = tmp_path / "root"
    (root / "etc").mkdir(parents=True)
    (root / "etc" / "os-release").write_text('ID=debian\nNAME="Debian"\n')
    (root / "etc" / "debian_version").write_text("12.4\n")
    d = LinuxDistribution(root_dir=str(root))
    assert d.id() == "debian"
    assert d.version() == "12.4"
