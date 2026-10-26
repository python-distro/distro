"""Extended distro-release / lsb-release / uname coverage for distro.

Probed behaviours pinned here:

* A distro-release file's ``id`` comes from its *file name*
  (``centos-release`` -> ``centos``, ``redhat-release`` -> ``redhat``
  then normalised to ``rhel``); a file with a random name yields no
  ``id`` even though name/version/codename still parse.
* ``lsb_release`` output is only used when ``include_lsb`` is true,
  and its ``Distributor ID`` goes through the same normalisation
  table (``RedHatEnterpriseServer`` -> ``rhel``).
* ``_parse_uname_content`` deliberately returns ``{}`` for Linux
  (so the kernel version never becomes the distro version) and
  parses other systems (``FreeBSD 13.2-RELEASE`` -> freebsd/13.2).
"""

import os
import stat

import pytest

from distro import LinuxDistribution

MISSING = "/nonexistent/os-release"


def distro_only(tmp_path, filename, content):
    path = tmp_path / filename
    path.write_text(content)
    return LinuxDistribution(
        os_release_file=MISSING,
        distro_release_file=str(path),
        include_lsb=False,
        include_uname=False,
    )


def test_centos_release_file(tmp_path):
    d = distro_only(tmp_path, "centos-release", "CentOS Linux release 7.9.2009 (Core)\n")
    assert d.id() == "centos"
    assert d.name() == "CentOS Linux"
    assert d.version() == "7.9.2009"
    assert d.version_parts() == ("7", "9", "2009")
    assert d.codename() == "Core"
    assert d.distro_release_info() == {
        "name": "CentOS Linux",
        "version_id": "7.9.2009",
        "codename": "Core",
        "id": "centos",
    }


def test_redhat_release_file_id_is_normalized_to_rhel(tmp_path):
    d = distro_only(tmp_path, "redhat-release", "Red Hat Enterprise Linux release 7.9 (Maipo)\n")
    assert d.id() == "rhel"
    assert d.name() == "Red Hat Enterprise Linux"
    assert d.version() == "7.9"
    assert d.codename() == "Maipo"


def test_fedora_release_file(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    assert d.id() == "fedora"
    assert d.version() == "30"
    assert d.codename() == "Thirty"


def test_randomly_named_release_file_has_no_id(tmp_path):
    d = distro_only(tmp_path, "myfile.txt", "CentOS Linux release 7.9.2009 (Core)\n")
    assert d.id() == ""
    assert d.name() == "CentOS Linux"
    assert d.version() == "7.9.2009"


def test_parse_distro_release_content_directly(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    assert d._parse_distro_release_content("Fedora release 30 (Thirty)\n") == {
        "name": "Fedora",
        "version_id": "30",
        "codename": "Thirty",
    }
    assert d._parse_distro_release_content("Some Unparsed Line\n") == {
        "name": "Some Unparsed Line"
    }
    assert d._parse_distro_release_content("") == {}


def test_parse_lsb_release_content_directly(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    parsed = d._parse_lsb_release_content(
        [
            "Distributor ID:\tDebian\n",
            "Description:\tDebian GNU/Linux 12 (bookworm)\n",
            "Release:\t12\n",
            "Codename:\tbookworm\n",
            "No colon here\n",
        ]
    )
    assert parsed == {
        "distributor_id": "Debian",
        "description": "Debian GNU/Linux 12 (bookworm)",
        "release": "12",
        "codename": "bookworm",
    }


def test_lsb_n_a_becomes_empty(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    parsed = d._parse_lsb_release_content(["Codename:\tn/a\n"])
    assert parsed == {"codename": ""}


def test_fake_lsb_release_command_via_path(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    script = bindir / "lsb_release"
    script.write_text(
        "#!/bin/sh\n"
        "printf 'Distributor ID:\\tRedHatEnterpriseServer\\n"
        "Description:\\tRed Hat Enterprise Linux Server release 7.9 (Maipo)\\n"
        "Release:\\t7.9\\nCodename:\\tMaipo\\n'\n"
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", str(bindir) + os.pathsep + os.environ["PATH"])
    d = LinuxDistribution(
        os_release_file=MISSING,
        distro_release_file="/nonexistent/nofile",
        include_lsb=True,
        include_uname=False,
    )
    assert d.id() == "rhel"
    assert d.name() == "RedHatEnterpriseServer"
    assert d.version() == "7.9"
    assert d.codename() == "Maipo"
    assert d.lsb_release_info()["release"] == "7.9"


def test_lsb_disabled_ignores_command(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    script = bindir / "lsb_release"
    script.write_text("#!/bin/sh\nprintf 'Distributor ID:\\tDebian\\nRelease:\\t12\\n'\n")
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", str(bindir) + os.pathsep + os.environ["PATH"])
    d = LinuxDistribution(
        os_release_file=MISSING,
        distro_release_file="/nonexistent/nofile",
        include_lsb=False,
        include_uname=False,
    )
    assert d.lsb_release_info() == {}
    assert d.id() == ""


def test_parse_uname_content(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    assert d._parse_uname_content(["Linux 6.8.0"]) == {}
    assert d._parse_uname_content([]) == {}
    assert d._parse_uname_content(["FreeBSD 13.2-RELEASE"]) == {
        "id": "freebsd",
        "name": "FreeBSD",
        "release": "13.2",
    }


def test_to_str_decodes_bytes(tmp_path):
    d = distro_only(tmp_path, "fedora-release", "Fedora release 30 (Thirty)\n")
    assert d._to_str(b"hello") == "hello"
