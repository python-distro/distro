# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The ``distro`` package (``distro`` stands for Linux Distribution) provides
information about the Linux distribution it runs on, such as a reliable
machine-readable distro ID, or version information.

It is a renewed alternative implementation for Python's original
:py:func:`platform.linux_distribution` function, but it provides much more
functionality. An alternative implementation became necessary because Python
3.5 deprecated this function, and Python 3.7 is expected to remove it
altogether. Its predecessor function :py:func:`platform.dist` was already
deprecated since Python 2.6 and is also expected to be removed in Python 3.7.
Still, there are many cases in which access to Linux distribution information
is needed. See `Python issue 1322 <https://bugs.python.org/issue1322>`_ for
more information.
"""
import platform


def distribution(full_distribution_name=True):
    """
    Return information about the current distribution as a tuple
    ``(id_name, version, codename)`` with items as follows:

    * ``id_name``:  If *full_distribution_name* is false, the result of
      :func:`distro.id`. Otherwise, the result of :func:`distro.name`.

    * ``version``:  The result of :func:`distro.version`.

    * ``codename``:  The result of :func:`distro.codename`.

    The interface of this function is compatible with the original
    :py:func:`platform.linux_distribution` function, supporting a subset of
    its parameters.

    The data it returns may not exactly be the same, because it uses more data
    sources than the original function, and that may lead to different data if
    the Linux distribution is not consistent across multiple data sources it
    provides (there are indeed such distributions ...).

    Another reason for differences is the fact that the :func:`distro.id`
    method normalizes the distro ID string to a reliable machine-readable value
    for a number of popular Linux distributions.
    """
    return _distro.linux_distribution(full_distribution_name)


def linux_distribution(full_distribution_name=True):
    return distribution(full_distribution_name)


def id():
    """
    Return the distro ID of the current Linux distribution, as a
    machine-readable string.

    For a number of Linux distributions, the returned distro ID value is
    *reliable*, in the sense that it is documented and that it does not change
    across releases of the distribution.

    This package maintains the following reliable distro ID values:

    ==============  =========================================
    Distro ID       Distribution
    ==============  =========================================
    "ubuntu"        Ubuntu
    "debian"        Debian
    "rhel"          RedHat Enterprise Linux
    "centos"        CentOS
    "fedora"        Fedora
    "sles"          SUSE Linux Enterprise Server
    "opensuse"      openSUSE
    "amazon"        Amazon Linux
    "arch"          Arch Linux
    "cloudlinux"    CloudLinux OS
    "exherbo"       Exherbo Linux
    "gentoo"        GenToo Linux
    "ibm_powerkvm"  IBM PowerKVM
    "kvmibm"        KVM for IBM z Systems
    "linuxmint"     Linux Mint
    "mageia"        Mageia
    "mandriva"      Mandriva Linux
    "parallels"     Parallels
    "pidora"        Pidora
    "raspbian"      Raspbian
    "oracle"        Oracle Linux (and Oracle Enterprise Linux)
    "scientific"    Scientific Linux
    "slackware"     Slackware
    "xenserver"     XenServer
    ==============  =========================================

    If you have a need to get distros for reliable IDs added into this set,
    or if you find that the :func:`distro.id` function returns a different
    distro ID for one of the listed distros, please create an issue in the
    `distro issue tracker`_.

    **Lookup hierarchy and transformations:**

    First, the ID is obtained from the following sources, in the specified
    order. The first available and non-empty value is used:

    * the value of the "ID" attribute of the os-release file,

    * the value of the "Distributor ID" attribute returned by the lsb_release
      command,

    * the first part of the file name of the distro release file,

    The so determined ID value then passes the following transformations,
    before it is returned by this method:

    * it is translated to lower case,

    * blanks (which should not be there anyway) are translated to underscores,

    * a normalization of the ID is performed, based upon
      `normalization tables`_. The purpose of this normalization is to ensure
      that the ID is as reliable as possible, even across incompatible changes
      in the Linux distributions. A common reason for an incompatible change is
      the addition of an os-release file, or the addition of the lsb_release
      command, with ID values that differ from what was previously determined
      from the distro release file name.
    """
    return _distro.id()


def name(pretty=False):
    """
    Return the name of the current Linux distribution, as a human-readable
    string.

    If *pretty* is false, the name is returned without version or codename.
    (e.g. "CentOS Linux")

    If *pretty* is true, the version and codename are appended.
    (e.g. "CentOS Linux 7.1.1503 (Core)")

    **Lookup hierarchy:**

    The name is obtained from the following sources, in the specified order.
    The first available and non-empty value is used:

    * If *pretty* is false:

      - the value of the "NAME" attribute of the os-release file,

      - the value of the "Distributor ID" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file.

    * If *pretty* is true:

      - the value of the "PRETTY_NAME" attribute of the os-release file,

      - the value of the "Description" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file, appended
        with the value of the pretty version ("<version_id>" and "<codename>"
        fields) of the distro release file, if available.
    """
    return _distro.name(pretty)


def version(pretty=False, best=False):
    """
    Return the version of the current Linux distribution, as a human-readable
    string.

    If *pretty* is false, the version is returned without codename (e.g.
    "7.0").

    If *pretty* is true, the codename in parenthesis is appended, if the
    codename is non-empty (e.g. "7.0 (Maipo)").

    Some distributions provide version numbers with different precisions in
    the different sources of distribution information. Examining the different
    sources in a fixed priority order does not always yield the most precise
    version (e.g. for Debian 8.2, or CentOS 7.1).

    The *best* parameter can be used to control the approach for the returned
    version:

    If *best* is false, the first non-empty version number in priority order of
    the examined sources is returned.

    If *best* is true, the most precise version number out of all examined
    sources is returned.

    **Lookup hierarchy:**

    In all cases, the version number is obtained from the following sources.
    If *best* is false, this order represents the priority order:

    * the value of the "VERSION_ID" attribute of the os-release file,
    * the value of the "Release" attribute returned by the lsb_release
      command,
    * the version number parsed from the "<version_id>" field of the first line
      of the distro release file,
    * the version number parsed from the "PRETTY_NAME" attribute of the
      os-release file, if it follows the format of the distro release files.
    * the version number parsed from the "Description" attribute returned by
      the lsb_release command, if it follows the format of the distro release
      files.
    """
    return _distro.version(pretty, best)


def version_parts(best=False):
    """
    Return the version of the current Linux distribution as a tuple
    ``(major, minor, build_number)`` with items as follows:

    * ``major``:  The result of :func:`distro.major_version`.

    * ``minor``:  The result of :func:`distro.minor_version`.

    * ``build_number``:  The result of :func:`distro.build_number`.

    For a description of the *best* parameter, see the :func:`distro.version`
    method.
    """
    return _distro.version_parts(best)


def major_version(best=False):
    """
    Return the major version of the current Linux distribution, as a string,
    if provided.
    Otherwise, the empty string is returned. The major version is the first
    part of the dot-separated version string.

    For a description of the *best* parameter, see the :func:`distro.version`
    method.
    """
    return _distro.major_version(best)


def minor_version(best=False):
    """
    Return the minor version of the current Linux distribution, as a string,
    if provided.
    Otherwise, the empty string is returned. The minor version is the second
    part of the dot-separated version string.

    For a description of the *best* parameter, see the :func:`distro.version`
    method.
    """
    return _distro.minor_version(best)


def build_number(best=False):
    """
    Return the build number of the current Linux distribution, as a string,
    if provided.
    Otherwise, the empty string is returned. The build number is the third part
    of the dot-separated version string.

    For a description of the *best* parameter, see the :func:`distro.version`
    method.
    """
    return _distro.build_number(best)


def like():
    """
    Return a space-separated list of distro IDs of distributions that are
    closely related to the current Linux distribution in regards to packaging
    and programming interfaces, for example distributions the current
    distribution is a derivative from.

    **Lookup hierarchy:**

    This information item is only provided by the os-release file.
    For details, see the description of the "ID_LIKE" attribute in the
    `os-release man page
    <http://www.freedesktop.org/software/systemd/man/os-release.html>`_.
    """
    return _distro.like()


def codename():
    """
    Return the codename for the release of the current Linux distribution,
    as a string.

    If the distribution does not have a codename, an empty string is returned.

    Note that the returned codename is not always really a codename. For
    example, openSUSE returns "x86_64". This function does not handle such
    cases in any special way and just returns the string it finds, if any.

    **Lookup hierarchy:**

    * the codename within the "VERSION" attribute of the os-release file, if
      provided,

    * the value of the "Codename" attribute returned by the lsb_release
      command,

    * the value of the "<codename>" field of the distro release file.
    """
    return _distro.codename()


def info(pretty=False, best=False):
    """
    Return certain machine-readable information items about the current Linux
    distribution in a dictionary, as shown in the following example:

    .. sourcecode:: python

        {
            'id': 'rhel',
            'version': '7.0',
            'version_parts': {
                'major': '7',
                'minor': '0',
                'build_number': ''
            },
            'like': 'fedora',
            'codename': 'Maipo'
        }

    The dictionary structure and keys are always the same, regardless of which
    information items are available in the underlying data sources. The values
    for the various keys are as follows:

    * ``id``:  The result of :func:`distro.id`.

    * ``version``:  The result of :func:`distro.version`.

    * ``version_parts -> major``:  The result of :func:`distro.major_version`.

    * ``version_parts -> minor``:  The result of :func:`distro.minor_version`.

    * ``version_parts -> build_number``:  The result of
      :func:`distro.build_number`.

    * ``like``:  The result of :func:`distro.like`.

    * ``codename``:  The result of :func:`distro.codename`.

    For a description of the *pretty* and *best* parameters, see the
    :func:`distro.version` method.
    """
    return _distro.info(pretty, best)

if platform.system() == 'Linux':
    from ._linux import get_distribution
    _distro = get_distribution()
else:
    raise ImportError('Unsupported platform: {0}'.format(platform.system()))

import argparse
import json
import logging
import sys
from . import name, info, version, codename


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = argparse.ArgumentParser(description="Linux distro info tool")
    parser.add_argument(
        '--json',
        '-j',
        help="Output in machine readable format",
        action="store_true")
    args = parser.parse_args()

    if args.json:
        logger.info(json.dumps(info(), indent=4, sort_keys=True))
    else:
        logger.info('Name: %s', name(pretty=True))
        distribution_version = version(pretty=True)
        logger.info('Version: %s', distribution_version)
        distribution_codename = codename()
        logger.info('Codename: %s', distribution_codename)


if __name__ == '__main__':
    main()

