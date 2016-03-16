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
.. # .. module:: ld
.. #    :platform: Linux
.. #    :synopsis: Information about the current Linux distribution.

.. # TODO: At the top of the module docstring, the module: statement
.. #       complains about duplicate id if 'ld' is used as a value.

Overview and motivation
-----------------------

The :mod:`ld` (linux distribution) package provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's original
:py:func:`platform.linux_distribution` function, but it also provides much more
functionality.
An alternative implementation became necessary because Python 3.5 deprecated
this function, and Python 3.7 is expected to remove it altogether.
Its predecessor function :py:func:`platform.dist` was already deprecated since
Python 2.6 and is also expected to be removed in Python 3.7.
Still, there are many cases in which access to that information is needed.
See `Python issue 1322 <https://bugs.python.org/issue1322>`_ for more
information.

Data sources
------------

The :mod:`ld` package implements a robust and inclusive way of retrieving the
information about a Linux distribution based on new standards and old methods,
namely from these data sources (from high to low precedence):

* The os-release file, if present.
  See `Format of the os-release file`_ for details.

* The output of the lsb_release command, if available.
  See `Format of the lsb_release command output`_ for details.

* The distro release file(s), if present.
  See `Format of the distro release file`_ for details.

Access to the information
-------------------------

The distribution information is available as single information items through
specific accessor functions (e.g. :func:`ld.id`).

It is also possible to get the machine-readable part of the information in a
more aggregated way from :func:`ld.info`.

For compatibility, there is a :func:`ld.linux_distribution` function with an
interface that is compatible the original
:py:func:`platform.linux_distribution` function, supporting a subset of its
parameters.
The data it returns may not exactly be the same, because the :mod:`ld`
package uses more data sources, and that may lead to different data if the
Linux distribution is not consistent across multiple data sources it provides
(there are indeed such distributions ...).
Another reason for differences is the fact that the :mod:`ld` package
normalizes the distribution ID string to a reliable machine-readable value for
a number of popular Linux distributions.

The precedence of the data sources listed above is in the listed order (top to
bottom).
The precedence is applied for each information item separately. Therefore, it
is possible that not all information items provided by this package come from
the same data source. For example, on a distribution that has an lsb_release
command that returns the 'Distributor ID' field but not the 'Codename' field,
and that has a distro release file that specifies a codename inside, the
distro ID will come from the lsb_release command (because it has higher
precedence), and the codename will come from the distro release file (because
it is not provided by the lsb_release command).

For distributions that provide multiple inconsistent data sources, it is
possible to get all information items consistently from a particular data
source by using the :func:`ld.os_release_info`, :func:`ld.lsb_release_info`,
and :func:`ld.distro_release_info` functions. These functions also provide
information items that are not provided by the specific accessor functions
for single information items. For example, the os-release file of RHEL 7
contains the following:

    REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 7"

The value for this attribute can be retrieved with:

    ld.get_os_release_attr('redhat_bugzilla_product')

It is also possible to retrieve single information items from a particular data
source, by using the :func:`ld.get_os_release_attr`,
:func:`ld.get_lsb_release_attr`, and :func:`ld.get_distro_release_attr`
functions.

Format of the os-release file
-----------------------------

The os-release file is expected to be encoded in UTF-8.

It is parsed using the standard python :py:mod:`shlex` package, which treats it
like a shell script.

The attribute names found in the file are translated to lower case and then
become the keys of the information items from the os-release file data source.
These keys can be used to retrieve single items with the
:func:`ld.get_os_release_attr` function, and they are also used as keys in the
dictionary returned by :func:`ld.os_release_info`.

The attribute values found in the file are processed using shell rules (e.g.
for whitespace, escaping, and quoting) before they become the values of the
information items from the os-release file data source.

If the attribute "VERSION" is found in the file, the distro codename is
extracted from its value if it can be found there. If a codename is found, it
becomes an additional information item with key "codename".

See the `os-release man page
<http://www.freedesktop.org/software/systemd/man/os-release.html>`_
for a list of possible attributes in the file.

**Example:**

This os-release file content:

::

    NAME='Ubuntu'
    VERSION="14.04.3 LTS, Trusty Tahr"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 14.04.3 LTS"
    VERSION_ID="14.04"
    HOME_URL="http://www.ubuntu.com/"
    SUPPORT_URL="http://help.ubuntu.com/"
    BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"

results in the following information items:

=================  ======================
Key                Value
=================  ======================
name               "Ubuntu"
version            "14.04.3 LTS, Trusty Tahr"
id                 "ubuntu"
id_like            "debian"
pretty_name        "Ubuntu 14.04.3 LTS"
version_id         "14.04"
home_url           "http://www.ubuntu.com/"
support_url        "http://help.ubuntu.com/"
bug_report_url     "http://bugs.launchpad.net/ubuntu/"
=================  ======================

Format of the lsb_release command output
----------------------------------------

The command output is expected to be encoded in UTF-8.

Only lines in the command output with the following format will be used:

    ``<attr-name>: <attr-value>``

Where:

* ``<attr-name>`` is the name of the attribute, and
* ``<attr-value>`` is the attribute value.

The attribute names are stripped from surrounding blanks, any remaining blanks
are translated to underscores, they are translated to lower case, and then
become the keys of the information items from the lsb_release command output
data source.

The attribute values are stripped from surrounding blanks, and then become the
values of the information items from the lsb_release command output data
source.

See the `lsb_release man page
<http://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/
LSB-Core-generic/lsbrelease.html>`_
for a description of standard attributes returned by the lsb_release command.

**Example:**

This lsb_release command output:

::

    No LSB modules are available.
    Distributor ID: Ubuntu
    Description:    Ubuntu 14.04.3 LTS
    Release:        14.04
    Codename:       trusty

results in the following information items:

=================  ======================
Key                Value
=================  ======================
distributor_id     "Ubuntu"
description        "Ubuntu 14.04.3 LTS"
release            "14.04"
codename           "trusty"
=================  ======================

Format of the distro release file
---------------------------------

The distro release file is expected to be encoded in UTF-8.

Only its first line is used, and it must have the following format:

    ``<name> [[[release] <version_id>] (<codename>)]``

Where:

* square brackets indicate optionality,
* ``<name>`` is the distro name,
* ``<version_id>`` is the distro version, and
* ``<codename>`` is the distro codename.

The following information items can be found in a distro release file
(shown with their keys and data types):

* ``id`` (string):  Distro ID, taken from the first part of the file name
  before the hyphen (``-``) or underscore (``_``).

  Note that the distro ID is not normalized or translated to lower case at this
  point; this happens only for the result of the :func:`ld.id` function.

* ``name`` (string):  Distro name, as found in the first line of the file.

* ``version_id`` (string):  Distro version, as found in the first line of the
  file. If not found, this information item will not exist.

* ``codename`` (string):  Distro codename, as found in the first line of the
  file. If not found, this information item will not exist.

  Note that the string in the codename field is not always really a
  codename. For example, in openSUSE, it contains ``x86_64``.

**Examples:**

1.  The following distro release file ``/etc/centos-release``:

    ::

        CentOS Linux release 7.1.1503 (Core)

    results in the following information items:

    =================  ======================
    Key                Value
    =================  ======================
    id                 "centos"
    name               "CentOS Linux"
    version_id         "7.1.1503"
    codename           "Core"
    =================  ======================

2.  The following distro release file ``/etc/oracle-release``:

    ::

        Oracle Linux Server release 7.1

    results in the following information items:

    =================  ======================
    Key                Value
    =================  ======================
    id                 "oracle"
    name               "Oracle Linux Server"
    version_id         "7.1"
    =================  ======================

3.  The following distro release file ``/etc/SuSE-release``:

    ::

        openSUSE 42.1 (x86_64)

    results in the following information items:

    =================  ======================
    Key                Value
    =================  ======================
    id                 "SuSE"
    name               "openSUSE"
    version_id         "42.1"
    codename           "x86_64"
    =================  ======================

Compatibility
-------------

The :mod:`ld` package is tested on Python 2.6, 2.7 and 3.5, with test data that
mimics the exact behavior of the underlying data sources for the following
Linux distributions:

* Arch Linux
* CentOS 5/7
* Debian 8
* Exherbo
* Fedora 23
* Mageia 5
* openSUSE Leap 42
* Oracle Linux Server 7
* RHEL 6/7
* Slackware 14
* Ubuntu 14

Classes and functions
---------------------

.. # TODO: The heading above should really be handled differently (it is at the
.. #       end of the module docstring currently).
"""

import sys
import os
import re
import subprocess
import shlex
import six

from . import constants as const

# Pattern for content of distro release file (reversed)
_DISTRO_RELEASE_CONTENT_REVERSED_PATTERN = re.compile(
    r'(?:[^)]*\)(.*)\()? *([\d.+\-a-z]*\d) *(?:esaeler *)?(.+)')

# Pattern for base file name of distro release file
_DISTRO_RELEASE_BASENAME_PATTERN = re.compile(
    r'(\w+)[-_](release|version)')

# Base file names to be ignored when searching for distro release file
_DISTRO_RELEASE_IGNORE_BASENAMES = [
    'debian_version',
    'system-release',
    const._OS_RELEASE_BASENAME
]


class LinuxDistribution(object):
    """
    Provides information about the Linux distribution this package runs on.

    The :mod:`ld` package creates a private module-global instance of this
    class and makes its methods available as module-global functions
    (e.g. :func:`ld.id`).

    Normally, it is not necessary to create additional instances of this
    class. However, in situations where control is needed over the exact
    data sources that are used, instances of this class can be created
    with a specific distro release file, or a specific os-release file, or
    without invoking the lsb_release command.
    """

    def __init__(self,
                 include_lsb=True,
                 os_release_file='',
                 distro_release_file=''):
        """
        The initialization method of this class gathers information from the
        available data sources, and stores that in private instance attributes.
        Subsequent access to the information items uses these private instance
        attributes, so that the data sources are read only once.

        Parameters:

        * ``include_lsb`` (bool): Controls whether the output of the
          lsb_release command is included as a data source.

          See `Format of the lsb_release command output`_ for details.

          If the lsb_release command is not available in the execution path,
          the data source for the lsb_release command will be empty.

        * ``os_release_file`` (string): The path name of the os-release file
          that is to be used as a data source.

          See `Format of the os-release file`_ for details.

          An empty string (the default) will cause ``/etc/os-release`` to be
          used as an os-release file.

          If the specified (or defaulted) os-release file does not exist, the
          data source for the os-release file will be empty.

        * ``distro_release_file`` (string): The path name of the distro release
          file that is to be used as a data source.

          See `Format of the distro release file`_ for details.

          An empty string (the default) will cause the first match to be used
          in the alphabetically sorted list of the files matching the following
          file patterns:

          * ``/etc/*-release``
          * ``/etc/*_release``
          * ``/etc/*-version``
          * ``/etc/*_version``

          where the following special file names are excluded:

          * ``/etc/debian_version``
          * ``/etc/system-release``
          * ``/etc/os-release``

          and where the first line within the file has the expected format.

          The algorithm to sort the files alphabetically is far from perfect,
          but the distro release file has the least priority as a data source,
          and it is expected that Linux distributions provide one of the other
          data sources.

          If the specified distro release file does not exist, or if no default
          distro release file can be found, the data source for the distro
          release file will be empty.

        Raises:

        * :py:exc:`IOError`: Some I/O issue with an os-release file or distro
          release file.

        * :py:exc:`subprocess.CalledProcessError`: The lsb_release command
          had some issue (other than not being found).

        * :py:exc:`UnicodeError`: A data source has unexpected characters or
          uses an unexpected encoding.
        """
        self.os_release_file = os_release_file or \
            os.path.join(const._UNIXCONFDIR, const._OS_RELEASE_BASENAME)
        self.distro_release_file = distro_release_file or ''
        self._os_release_info = self._get_os_release_info()
        self._lsb_release_info = self._get_lsb_release_info() \
            if include_lsb else {}
        self._distro_release_info = self._get_distro_release_info()

    def __repr__(self):
        return \
            "LinuxDistribution(" \
            "os_release_file=%r, " \
            "distro_release_file=%r, " \
            "_os_release_info=%r, " \
            "_lsb_release_info=%r, " \
            "_distro_release_info=%r)" % \
            (self.os_release_file,
             self.distro_release_file,
             self._os_release_info,
             self._lsb_release_info,
             self._distro_release_info)

    def os_release_info(self):
        """Return a dictionary containing key-value pairs for the information
        items from the os-release file data source.

        See `Format of the os-release file`_ for details about these
        information items.
        """
        return self._os_release_info

    def lsb_release_info(self):
        """Return a dictionary containing key-value pairs for the information
        items from the lsb_release command data source.

        See `Format of the lsb_release command output`_ for details about these
        information items.
        """
        return self._lsb_release_info

    def distro_release_info(self):
        """Return a dictionary containing key-value pairs for the
        information items from the distro release file data source.

        See `Format of the distro release file`_ for details about these
        information items.
        """
        return self._distro_release_info

    def get_os_release_attr(self, attribute):
        """Return an information item from the os-release file data source.

        Parameters:

        * ``attribute`` (string): Key of the information item.

        Returns:

        * (string): Value of the information item, if the item exists.
          The empty string, if the item does not exist.

        See `Format of the os-release file`_ for details about these
        information items.
        """
        return self._os_release_info.get(attribute, '')

    def get_lsb_release_attr(self, attribute):
        """Return an information item from the lsb_release command output
        data source.

        Parameters:

        * ``attribute`` (string): Key of the information item.

        Returns:

        * (string): Value of the information item, if the item exists.
          The empty string, if the item does not exist.

        See `Format of the lsb_release command output`_ for details about these
        information items.
        """
        return self._lsb_release_info.get(attribute, '')

    def get_distro_release_attr(self, attribute):
        """Return an information item from the distro release file data source.

        Parameters:

        * ``attribute`` (string): Key of the information item.

        Returns:

        * (string): Value of the information item, if the item exists.
          The empty string, if the item does not exist.

        See `Format of the distro release file`_ for details about these
        information items.
        """
        return self._distro_release_info.get(attribute, '')

    def _get_os_release_info(self):
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def _get_lsb_release_info(self):
        cmd = 'lsb_release -a'
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = p.communicate()
        rc = p.returncode
        if rc == 0:
            return self._parse_lsb_release(out.splitlines())
        elif rc == 127:  # Command not found
            return {}
        else:
            if sys.version_info[0:2] >= (2, 7):
                raise subprocess.CalledProcessError(rc, cmd, err)
            else:
                raise subprocess.CalledProcessError(rc, cmd)

    def _get_distro_release_info(self):
        """Parse a distro release file and return a dictionary containing all
        information found within the file.
        """
        if self.distro_release_file:
            # If it was specified, we use it and parse what we can, even if
            # its file name or content does not match the expected pattern.
            distro_info = self._parse_distro_release_file(
                self.distro_release_file)
            basename = os.path.basename(self.distro_release_file)
            # The file name pattern for user-specified distro release files
            # is somewhat more tolerant (compared to when searching for the
            # file), because we want to use what was specified as best as
            # possible.
            match = _DISTRO_RELEASE_BASENAME_PATTERN.match(basename)
            if match:
                distro_info['id'] = match.group(1)
            return distro_info
        else:
            basenames = os.listdir(const._UNIXCONFDIR)
            # We sort for repeatability in cases where there are multiple
            # distro specific files; e.g. CentOS, Oracle, Enterprise all
            # containing `redhat-release` on top of their own.
            basenames.sort()
            for basename in basenames:
                if basename in _DISTRO_RELEASE_IGNORE_BASENAMES:
                    continue
                match = _DISTRO_RELEASE_BASENAME_PATTERN.match(basename)
                if match:
                    filepath = os.path.join(const._UNIXCONFDIR, basename)
                    distro_info = self._parse_distro_release_file(filepath)
                    if 'name' in distro_info:
                        # The name is always present if the pattern matches
                        self.distro_release_file = filepath
                        distro_info['id'] = match.group(1)
                        return distro_info
            return {}

    @staticmethod
    def _parse_key_value_files(content):
        """Parse the content of an os-release file and return a dictionary
        containing all information items found within the file.

        Parameters:

        * content: Iterable through the lines in the os-release file.
                   Each line must be a unicode string or a UTF-8 encoded byte
                   string.
        """
        props = {}
        lexer = shlex.shlex(content, posix=True)
        lexer.whitespace_split = True

        # The shlex module defines its `wordchars` variable using literals,
        # making it dependent on the encoding of the Python source file.
        # In Python 2.6 and 2.7, the shlex source file is encoded in
        # 'iso-8859-1', and the `wordchars` variable is defined as a byte
        # string. This causes a UnicodeDecodeError to be raised when the
        # parsed content is a unicode object. The following fix resolves that
        # (... but it should be fixed in shlex...):
        if sys.version_info[0] == 2 and isinstance(lexer.wordchars, str):
            lexer.wordchars = lexer.wordchars.decode('iso-8859-1')

        tokens = list(lexer)
        for token in tokens:
            # At this point, all shell-like parsing has been done (i.e.
            # comments processed, quotes and backslash escape sequences
            # processed, multi-line values assembled, trailing newlines
            # stripped, etc.), so the tokens are now either:
            # * variable assignments: var=value
            # * commands or their arguments (not allowed in os-release)
            if '=' in token:
                k, v = token.split('=', 1)
                if isinstance(v, six.binary_type):
                    v = v.decode('utf-8')
                props[k.lower()] = v
                if k == 'VERSION':
                    # this handles cases in which the codename is in
                    # the `(CODENAME)` (rhel, centos, fedora) format
                    # or in the `, CODENAME` format (Ubuntu).
                    codename = re.search(r'(\(\D+\))|,(\s+)?\D+', v)
                    if codename:
                        codename = codename.group()
                        codename = codename.strip('()')
                        codename = codename.strip(',')
                        codename = codename.strip()
                        # codename appears within paranthese.
                        props['codename'] = codename
                    else:
                        props['codename'] = ''
            else:
                # Ignore any tokens that are not variable assignments
                pass
        return props

    @staticmethod
    def _parse_lsb_release(lines):
        """Parse the content of the output of the lsb_release command and
        return a dictionary containing all information items found within the
        output.

        Parameters:

        * content: Iterable through the lines of the lsb_release output.
                   Each line must be a unicode string or a UTF-8 encoded byte
                   string.
        """
        props = {}
        for line in lines:
            if isinstance(line, six.binary_type):
                line = line.decode('utf-8')
            kv = line.strip('\n').split(':', 1)
            if len(kv) != 2:
                # Ignore lines without colon.
                continue
            k, v = kv
            props.update({k.replace(' ', '_').lower(): v.strip()})
        return props

    def _parse_distro_release_file(self, filepath):
        """Parse a distro release file and return a dictionary containing all
        information items found.

        Parameters:

        * filepath: string with path name of the distro release file.
        """
        if os.path.isfile(filepath):
            with open(filepath, 'r') as fp:
                # Only parse the first line. For instance, on SLES there
                # are multiple lines. We don't want them...
                return self._parse_distro_release_content(fp.readline())
        return {}

    @staticmethod
    def _parse_distro_release_content(line):
        """Parse a line from a distro release file and return a dictionary
        containing all information items found.

        Parameters:
        * line: Line from the distro release file. Must be a unicode string
                or a UTF-8 encoded byte string.
        """
        if isinstance(line, six.binary_type):
            line = line.decode('utf-8')
        m = _DISTRO_RELEASE_CONTENT_REVERSED_PATTERN.match(
            line.strip()[::-1])
        distro_info = {}
        if m:
            distro_info['name'] = m.group(3)[::-1]   # regexp ensures non-None
            if m.group(2):
                distro_info['version_id'] = m.group(2)[::-1]
            if m.group(1):
                distro_info['codename'] = m.group(1)[::-1]
        return distro_info

    def id(self):
        """Return the ID for the distribution, as a machine-readable string.

        For a number of Linux distributions, the returned distro ID value is
        *reliable*, in the sense that it is documented and that it does not
        change across releases of the distribution.

        This package maintains the following reliable distro ID values:

        TODO: This list is preliminary and needs review.

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
        "nexus_centos"  TODO: Clarify
        "parallels"     Parallels
        "pidora"        Pidora
        "raspbian"      Raspbian
        "oracle"        Oracle Linux (and Oracle Enterprise Linux)
        "scientific"    Scientific Linux
        "slackware"     Slackware
        "xenserver"     XenServer
        ==============  =========================================

        **Lookup hierarchy and transformations:**

        First, the ID is obtained from the following sources, in the specified
        order. The first available and non-empty value is used:

        * the value of the "ID" attribute of the os-release file,

        * the value of the "Distributor ID" attribute returned by the
          lsb_release command,

        * the first part of the file name of the distro release file,

        The so determined ID value then passes the following transformations,
        before it is returned by this method:

        * it is translated to lower case,

        * blanks (which should not be there anyway) are translated to
          underscores,

        * a normalization of the ID is performed, based upon translation
          tables in the :mod:`ld.constants` module. The purpose of this
          normalization is to ensure that the ID is as reliable as possible,
          even across incompatible changes in the Linux distributions. A common
          case for such a change is the addition of an os-release file, or the
          addition of the lsb_release command, with ID values that differ from
          what was previously determined from the distro release file name.
        """
        distro_id = self.get_os_release_attr('id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_OS_ID.get(distro_id, distro_id)

        distro_id = self.get_lsb_release_attr('distributor_id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_LSB_ID.get(distro_id, distro_id)

        distro_id = self.get_distro_release_attr('id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_DISTRO_ID.get(distro_id, distro_id)

        return ''

    def name(self, pretty=False):
        """Return the name of the distribution, as a human-readable string.

        If ``pretty=False``, the name is returned without version or codename.
        (e.g. "CentOS Linux")

        If ``pretty=True``, the version and codename are appended.
        (e.g. "CentOS Linux 7.1.1503 (Core)")

        **Lookup hierarchy:**

        The name is obtained from the following sources, in the specified
        order. The first available and non-empty value is used:

        * For ``pretty=False``:

          - the value of the "NAME" attribute of the os-release file,

          - the value of the "Distributor ID" attribute returned by the
            lsb_release command,

          - the value of the "<name>" field of the distro release file.

        * For ``pretty=True``:

          - the value of the "PRETTY_NAME" attribute of the os-release file,

          - the value of the "Description" attribute returned by the
            lsb_release command,

          - the value of the "<name>" field of the distro release file,
            appended with the value of the pretty version ("<version_id>" and
            "<codename>" fields) of the distro release file, if available.

        """
        name = self.get_os_release_attr('name') \
            or self.get_lsb_release_attr('distributor_id') \
            or self.get_distro_release_attr('name')
        if pretty:
            name = self.get_os_release_attr('pretty_name') \
                or self.get_lsb_release_attr('description')
            if not name:
                name = self.get_distro_release_attr('name')
                version = self.version(pretty=True)
                if version:
                    name = name + ' ' + version
        return name or ''

    def version(self, pretty=False, best=False):
        """Return the version of the distribution, as a human-readable string.

        If ``pretty=False``, the version is returned without codename
        (e.g. "7.0").

        If ``pretty=True``, the codename in parenthesis is appended (e.g.
        "7.0 (Maipo)"), if the codename is non-empty.

        Some distributions provide version numbers with different precisions in
        the different sources of distribution information. Examining the
        different sources in a fixed priority order does not always yield the
        most precise version (e.g. for Debian 8.2, or CentOS 7.1).

        The ``best`` parameter can be used to control the approach for the
        returned version:

        If ``best=False``, the first non-empty version number in priority order
        of the examined sources is returned.

        If ``best=True``, the most precise version number out of all examined
        sources is returned.

        **Lookup hierarchy:**

        In all cases, the version number is obtained from the following
        sources. For `best=False`, this order represents the priority order:

        * the value of the "VERSION_ID" attribute of the `os-release` file,
        * the value of the "Release" attribute returned by the `lsb_release`
          command,
        * the version number parsed from the "<version_id>" field of the first
          line of the distro release file,
        * the version number parsed from the "PRETTY_NAME" attribute of the
          `os-release` file, if it follows the format of the distro release
          files.
        * the version number parsed from the "Description" attribute returned
          by the `lsb_release` command, if it follows the format of the distro
          release files.
        * the empty string.

        TODO: So far, the tested distributions do not have a more precise
        version in the description fields than in the the official version
        fields. Review whether parsing the description fields should be done
        at all.
        """
        versions = [
            self.get_os_release_attr('version_id'),
            self.get_lsb_release_attr('release'),
            self.get_distro_release_attr('version_id'),
            self._parse_distro_release_content(
              self.get_os_release_attr('pretty_name')).get('version_id', ''),
            self._parse_distro_release_content(
              self.get_lsb_release_attr('description')).get('version_id', ''),
        ]
        version = ''
        if best:
            # This algorithm uses the last version in priority order that has
            # the best precision. If the versions are not in conflict, that
            # does not matter; otherwise, using the last one instead of the
            # first one might be considered a surprise.
            for v in versions:
                if v.count(".") > version.count(".") or version == '':
                    version = v
        else:
            for v in versions:
                if v != '':
                    version = v
                    break
        if pretty and version and self.codename():
            version = u'{0} ({1})'.format(version, self.codename())
        return version

    def version_parts(self, best=False):
        """Return the version of the distribution as a tuple (major,
        minor, build_number), as strings. Parts of the version that do not
        exist, are returned as an empty string in this tuple.

        For a description of the ``best`` parameter, see the
        :func:`ld.LinuxDistribution.version` method.
        """
        version_str = self.version(best=best)
        if version_str:
            g = re.compile(r'(\d+)\.?(\d+)?\.?(\d+)?')
            m = g.match(version_str)
            if m:
                major, minor, build_number = m.groups()
                return (major, minor or '', build_number or '')
        return ('', '', '')

    def major_version(self, best=False):
        """Return the major version of the distribution, as a string, if
        provided. Otherwise, the empty string is returned. The major version is
        the first part of the dot-separated version string.

        For a description of the ``best`` parameter, see the
        :func:`ld.LinuxDistribution.version` method.
        """
        return self.version_parts(best=best)[0]

    def minor_version(self, best=False):
        """Returns the minor version of the distribution as a string, if
        provided. Otherwise, the empty string is returned. The minor version is
        the second part of the dot-separated version string.

        For a description of the ``best`` parameter, see the
        :func:`ld.LinuxDistribution.version` method.
        """
        return self.version_parts(best=best)[1]

    def build_number(self, best=False):
        """Returns the build number of the distribution as a string, if
        provided. Otherwise, the empty string is returned. The build number is
        the third part of the dot-separated version string.

        For a description of the ``best`` parameter, see the
        :func:`ld.LinuxDistribution.version` method.
        """
        return self.version_parts(best=best)[2]

    def like(self):
        """Returns a space-separated list of distro IDs of distributions that
        are closely related to the current distribution in regards to packaging
        and programming interfaces, for example distributions the current
        distribution is a derivative from.

        **Lookup hierarchy:**

        This information item is only provided by the os-release file.
        For details, see the description of the "ID_LIKE" attribute in the
        `os-release man page
        <http://www.freedesktop.org/software/systemd/man/os-release.html>`_.
        """
        return self.get_os_release_attr('id_like') or ''

    def codename(self):
        """Return the codename for the distribution's release.

        Note that not all distributions have codenames, in which case an empty
        string is returned.

        Note that the codename field if provided, does not always contain a
        codename.

        **Lookup hierarchy:**

        * the codename within the "VERSION" attribute of the os-release file,
          if provided,

        * the value of the "Codename" attribute returned by the lsb_release
          command,

        * the value of the "<codename>" field of the distro release file.
        """
        return self.get_os_release_attr('codename') \
            or self.get_lsb_release_attr('codename') \
            or self.get_distro_release_attr('codename') \
            or ''

    def linux_distribution(self, full_distribution_name=True):
        """Return a tuple ``(id_name, version, codename)`` with items as
        follows:

        * ``id_name``:  If ``full_distribution_name=False``, the result of
          :func:`ld.LinuxDistribution.id`. Otherwise, the result of
          :func:`ld.LinuxDistribution.name`.

        * ``version``:  The result of :func:`ld.LinuxDistribution.version`.

        * ``codename``:  The result of :func:`ld.LinuxDistribution.codename`.

        The interface of this function is compatible with the original
        :py:func:`platform.linux_distribution` function, supporting a subset of
        its parameters.

        The data it returns may not exactly be the same, because it uses more
        data sources than the original function, and that may lead to different
        data if the Linux distribution is not consistent across multiple data
        sources it provides (there are indeed such distributions ...).

        Another reason for differences is the fact that the
        :func:`ld.LinuxDistribution.id` method normalizes the distro ID string
        to a reliable machine-readable value for a number of popular
        Linux distributions.
        """
        return (
            self.name() if full_distribution_name else self.id(),
            self.version(),
            self.codename()
        )

    def info(self):
        """Return certain machine-readable information items in a dictionary,
        as shown in the following example:

        ::

            {
                'id': 'rhel',
                'version': '7.0',
                'version_parts': {
                    'major': '7',
                    'minor': '0',
                    'build_number': ''
                },
                'like': 'fedora',
                'codename': 'maipo',
            }

        TODO: Should the version be provided in best precision (best=True)?
        """
        return dict(
            id=self.id(),
            version=self.version(),
            version_parts=dict(
                major=self.major_version(),
                minor=self.minor_version(),
                build_number=self.build_number()
            ),
            like=self.like(),
        )

_ldi = LinuxDistribution()


def id():
    """
    Return the ID of the current distribution, as a string.

    For details, see :func:`ld.LinuxDistribution.id`.
    """
    return _ldi.id()


def name(pretty=False):
    """
    Return the name of the current distribution, as a string.

    For details, see :func:`ld.LinuxDistribution.name`.
    """
    return _ldi.name(pretty)


def version(pretty=False, best=False):
    """
    Return the version of the current distribution, as a string.

    For details, see :func:`ld.LinuxDistribution.version`.
    """
    return _ldi.version(pretty, best)


def version_parts(best=False):
    """
    Return the version of the current distribution, as a tuple of version
    numbers.

    For details, see :func:`ld.LinuxDistribution.version_parts`.
    """
    return _ldi.version_parts(best)


def major_version(best=False):
    """
    Return the major version number of the current distribution.

    For details, see :func:`ld.LinuxDistribution.major_version`.
    """
    return _ldi.major_version(best)


def minor_version(best=False):
    """
    Return the minor version number of the current distribution.

    For details, see :func:`ld.LinuxDistribution.minor_version`.
    """
    return _ldi.minor_version(best)


def build_number(best=False):
    """
    Return the build number of the current distribution.

    For details, see :func:`ld.LinuxDistribution.build_number`.
    """
    return _ldi.build_number(best)


def like():
    """
    Return the IDs of distributions that are like the current distribution.

    For details, see :func:`ld.LinuxDistribution.like`.
    """
    return _ldi.like()


def codename():
    """
    Return the codename of the current distribution.

    For details, see :func:`ld.LinuxDistribution.codename`.
    """
    return _ldi.codename()


def linux_distribution(full_distribution_name=True):
    """
    Return information about the current distribution that is compatible
    with Python's :func:`platform.linux_distribution`, supporting a subset of
    its parameters.

    For details, see :func:`ld.LinuxDistribution.linux_distribution`.
    """
    return _ldi.linux_distribution(full_distribution_name)


def os_release_info():
    """
    Return information about the current distribution that is only from the
    os-release file, if present.

    For details, see :func:`ld.LinuxDistribution.os_release_info`.
    """
    return _ldi.os_release_info()


def lsb_release_info():
    """
    Return information about the current distribution that is only from the
    lsb_release command, if available.

    For details, see :func:`ld.LinuxDistribution.lsb_release_info`.
    """
    return _ldi.lsb_release_info()


def distro_release_info():
    """
    Return information about the current distribution that is only from the
    distro release file, if present.

    For details, see :func:`ld.LinuxDistribution.distro_release_info`.
    """
    return _ldi.distro_release_info()


def get_os_release_attr(attribute):
    """
    Return an information item from the os-release file data source.

    For details, see :func:`ld.LinuxDistribution.get_os_release_attr`.
    """
    return _ldi.get_os_release_attr(attribute)


def get_lsb_release_attr(attribute):
    """
    Return an information item from the lsb_release command output
    data source.

    For details, see :func:`ld.LinuxDistribution.get_lsb_release_attr`.
    """
    return _ldi.get_lsb_release_attr(attribute)


def get_distro_release_attr(attribute):
    """
    Return an information item from the distro release file data source.

    For details, see :func:`ld.LinuxDistribution.get_distro_release_attr`.
    """
    return _ldi.get_distro_release_attr(attribute)


def info():
    """
    Return certain machine-readable information about the current distribution.

    For details, see :func:`ld.LinuxDistribution.info`.
    """
    return _ldi.info()
