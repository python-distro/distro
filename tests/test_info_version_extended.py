"""Extended info / version / best-version coverage for distro.

Probed behaviours pinned here:

* ``version(best=True)`` picks the candidate with the most dots
  (``1.2.3`` from a pretty-name parse beats ``1.2`` from
  ``VERSION_ID``); without ``best`` the first non-empty candidate
  wins.
* ``version(pretty=True)`` appends ``" (<codename>)"`` only when a
  codename exists.
* ``info()`` returns the same values as the individual accessors,
  with ``version_parts`` as a dict (not the tuple returned by
  ``version_parts()``).
* ``LinuxDistribution.__repr__`` starts with the class name and the
  file paths used.
"""

import pytest

from distro import LinuxDistribution

MISSING = "/nonexistent/os-release"
NO_RELEASE = "/nonexistent/nofile"


def make(tmp_path, content):
    path = tmp_path / "os-release"
    path.write_text(content)
    return LinuxDistribution(
        os_release_file=str(path),
        distro_release_file=NO_RELEASE,
        include_lsb=False,
        include_uname=False,
    )


def test_info_matches_accessors(tmp_path):
    path = tmp_path / "os-release"
    path.write_text(
        'PRETTY_NAME="Ubuntu 24.04.5 LTS"\nNAME="Ubuntu"\nVERSION_ID="24.04"\n'
        'VERSION="24.04.5 LTS (Noble Numbat)"\nVERSION_CODENAME=noble\nID=ubuntu\nID_LIKE=debian\n'
    )
    d = LinuxDistribution(
        os_release_file=str(path),
        distro_release_file=NO_RELEASE,
        include_lsb=False,
        include_uname=False,
    )
    assert d.info() == {
        "id": "ubuntu",
        "version": "24.04",
        "version_parts": {"major": "24", "minor": "04", "build_number": ""},
        "like": "debian",
        "codename": "noble",
    }
    assert d.info(pretty=True)["version"] == "24.04 (noble)"


def test_version_best_picks_most_dots(tmp_path):
    d = make(tmp_path, 'ID=x\nVERSION_ID="1.2"\nPRETTY_NAME="X 1.2.3"\n')
    assert d.version() == "1.2"
    assert d.version(best=True) == "1.2.3"
    assert d.version_parts(best=True) == ("1", "2", "3")
    assert d.version_parts() == ("1", "2", "")


def test_version_pretty_without_codename_has_no_suffix(tmp_path):
    d = make(tmp_path, 'ID=x\nVERSION_ID="8.10"\nNAME="Oracle Linux"\n')
    assert d.version(pretty=True) == "8.10"


def test_version_parts_for_single_number_and_empty(tmp_path):
    d = make(tmp_path, 'ID=x\nVERSION_ID="7"\n')
    assert d.version_parts() == ("7", "", "")
    assert d.major_version() == "7"
    assert d.minor_version() == ""
    assert d.build_number() == ""


def test_version_parts_best_flag(tmp_path):
    d = make(tmp_path, 'ID=x\nVERSION_ID="1.2"\nPRETTY_NAME="X 1.2.3"\n')
    assert d.major_version(best=True) == "1"
    assert d.minor_version(best=True) == "2"
    assert d.build_number(best=True) == "3"


def test_like_returns_id_like_verbatim(tmp_path):
    d = make(tmp_path, 'ID=x\nID_LIKE="rhel fedora"\n')
    assert d.like() == "rhel fedora"


def test_name_pretty_falls_back_to_name_plus_version(tmp_path):
    # The pretty fallback does *not* use the os-release NAME: it uses
    # the distro-release name (empty here) plus the pretty version,
    # hence the leading space -- the same quirk as the Oracle case.
    d = make(tmp_path, 'ID=x\nNAME="X"\nVERSION_ID="2.0"\nVERSION_CODENAME=two\n')
    assert d.name(pretty=True) == " 2.0 (two)"


def test_repr_contains_class_and_paths(tmp_path):
    d = make(tmp_path, 'ID=x\n')
    text = repr(d)
    assert text.startswith("LinuxDistribution(")
    assert "os_release_file=" in text
    assert "distro_release_file=" in text


def test_package_version_is_pinned(tmp_path):
    import distro

    assert distro.__version__ == "1.9.0"


def test_linux_distribution_tuple_shape(tmp_path):
    d = make(tmp_path, 'ID=x\nNAME="X"\nVERSION_ID="1.0"\n')
    result = d.linux_distribution()
    assert isinstance(result, tuple) and len(result) == 3


def test_deprecated_linux_distribution_module_function_shape(tmp_path):
    # The module-level linux_distribution() is deprecated but still
    # returns a 3-tuple for the instance; check the instance method
    # here, since the module function reflects the host, not fixtures.
    d = make(tmp_path, 'ID=x\nNAME="X"\nVERSION_ID="1.0"\n')
    assert d.linux_distribution(full_distribution_name=False)[0] == "x"
