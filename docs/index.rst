
**ld** package (Linux Distribution) version |version|)
******************************************************

.. automodule:: ld

Consolidated accessor functions
===============================

The consolidated accessor functions provide information taking into acount
all data sources in priority order. They should be the normal way to access
the information about the current Linux distribution.

In situations where control is needed over the exact data sources that are
used, the `Single source accessor functions`_ or the
`LinuxDistribution class`_ can be used.

.. autofunction:: ld.linux_distribution
.. autofunction:: ld.id
.. autofunction:: ld.name
.. autofunction:: ld.version
.. autofunction:: ld.version_parts
.. autofunction:: ld.major_version
.. autofunction:: ld.minor_version
.. autofunction:: ld.build_number
.. autofunction:: ld.like
.. autofunction:: ld.codename
.. autofunction:: ld.info

Single source accessor functions
================================

The single source accessor functions provide information from a single data
source. They can be used in situations where control is needed over which
single data source is used.

In addition, they provide information items that are specific to the data
sources, and that are not returned by the consolidated accessor functions.

.. autofunction:: ld.os_release_info
.. autofunction:: ld.lsb_release_info
.. autofunction:: ld.distro_release_info
.. autofunction:: ld.get_os_release_attr
.. autofunction:: ld.get_lsb_release_attr
.. autofunction:: ld.get_distro_release_attr

LinuxDistribution class
=======================

The :class:`ld.LinuxDistribution` class allows specifying the path names of the
os-release file and distro release file and whether the lsb_release command
should be used. It can be used in situations where control is needed about
that.

.. autoclass:: ld.LinuxDistribution
   :members:
   :undoc-members:

Normalization tables
====================

These translation tables are used to normalize the parsed distro ID values
into reliable IDs. See :func:`ld.id` for details.

.. autodata:: ld.constants.NORMALIZED_OS_ID
.. autodata:: ld.constants.NORMALIZED_LSB_ID
.. autodata:: ld.constants.NORMALIZED_DISTRO_ID

Format of the os-release file
=============================

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
========================================

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
=================================

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

