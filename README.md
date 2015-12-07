ld
==

[![Build Status](https://travis-ci.org/nir0s/ld.svg?branch=master)](https://travis-ci.org/nir0s/ld)
[![PyPI](http://img.shields.io/pypi/dm/ld.svg)](http://img.shields.io/pypi/dm/ld.svg)
[![PypI](http://img.shields.io/pypi/v/ld.svg)](http://img.shields.io/pypi/v/ld.svg)

Python 3.5 deprecates `platform.linux_distribution()` and Python 3.7 removes it altogether.

Still, there are many cases in which you need access to that information.

see [https://bugs.python.org/issue1322](https://bugs.python.org/issue1322) for more information.

`ld` (linux distribution) attempts to implement a more robust and inclusive way of retrieving the distro related information based on new standards and old methods - namely:

* `/etc/os-release`
* `/etc/lsb-release`
* `/etc/*-release`

## Installation

```shell
pip install ld
```

For dev:

```shell
pip install https://github.com/nir0s/ld/archive/master.tar.gz
```

## Distribution Support

The following distributions are handled (not all versions are tested of course):

* Red Hat
* CentOS
* Ubuntu
* Debian
* OpenSuSE
* SuSE
* Arch
* Slackware
* Exherbo
* Oracle

Soon:

* Gentoo
* Enterprise


## Usage

```python

import ld

ld.linux_distribution(full_distribution_name=False)

'('centos', '7.1.1503', 'Core')'
```

## Exposed Distribution Properties

`ld` exposes the following parmeters:

### `ld.linux_distribution(full_distribution_name=False)`

Attempts to implement Python's `platform.linux_distribution()`.

### `ld.id()`

Returns the id of the distribution - e.g. `ubuntu`, `fedora`, `debian`...

The id should be machine-readable.

#### Retrieval Hierarchy

* os-release['ID']
* lsb-release['DISTRIB_ID'] (in lowercase)
* *-release file name prefix (e.g. redhat from redhat-release)
* first part of the first line of the *-release file

### `ld.name()`

Returns the name of the distribution - e.g. `Red Hat Enterprise Linux Server`, `Ubuntu`, `openSUSE Leap`

#### Retrieval Hierarchy

* os-release['NAME']
* lsb-release['DISTRIB_ID']
* first part of the first line of the *-release file
* `ld.id()`

### `ld.name(pretty=True)`

Returns a prettified name of the distribution - e.g. `openSUSE Leap 42.1 (x86_64)`, `CentOS Linux 7 (Core)`, `Oracle Linux Server 7.1`

#### Retrieval Hierarchy

* os-release['PRETTY_NAME']
* lsb-release['DISTRIB_ID'] + `ld.version(pretty=True)`
* first part of the first line of the *-release file + `ld.version(pretty=True)`
* `ld.id()` + `ld.version(pretty=True)`

### `ld.version()`

Returns the version (i.e. release) of the distribution - e.g. .. well.. the version number.

### Retrieval Hierarchy

* os-release['VERSION_ID']
* lsb-release['DISTRIB_RELEASE']
* second part of the first line of the *-release file

`ld.minor_version()`, `ld.major_version()` and `ld.build_number()` are also exposed and are based on `ld.version_parts()`.

### `ld.version(pretty=True)`

Returns a prettified version of the distribution  - e.g. `7 (Core)`, `23 (Twenty Three)`

### Retrieval Hierarchy

* os-release['VERSION']
* lsb-release['DISTRIB_RELEASE'] + `ld.codename()` (if codename exists)
* second part of the first line of the *-release file + `ld.codename()` (if codename exists)

### `ld.like()`

Returns the os-release['ID_LIKE'] field - e.g. `suse`, `rhel fedora`, `debian`


### `ld.codename()`

Returns the distribution version's codename - e.g. `Core`, `trusty`, `Maipo`

Note that not all distributions provide a codename for their releases.

#### Retrieval Hierarchy

* The second part of os-release['VERSION'] (between parentheses or after a comma)
* lsb-release['DISTRIB_CODENAME']
* third part of the first line of the *-release files (between parentheses)

### `ld.base()`

Returns the base distribution - e.g. `arch`, `gentoo`, `rhel`

`constants.py` contains the table in which each distro is mapped to its base distro.

Matching is one first by `ld.name()` and then by `ld.like()`


### Retrieving information directly

* `ld.os_release_info()` - returns a dictionary containing the info found in `/etc/os-release`
* `ld.lsb_release_info()` - returns a dictionary containing the info found in `/etc/lsb-release`
* `ld.distro_release_info()` - returns a dictionary containing the info found in '/etc/*-release' matching your distribution.

You can also get the information from some of the release files directly. This allows you to retrieve information that is not exposed via the API.

For instance, RHEL 7's os-release file contains the following:

`REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 7"`

`ld.get_os_release_attr('redhat_bugzilla_product')` will get the value for that field.

`ld.get_lsb_release_attr()` and `ld.get_dist_release_attr()` are also exposed.


## Lookup files

* [os-release](http://www.freedesktop.org/software/systemd/man/os-release.html) is a new standard for providing distro-specific information. This is the first file looked at when attempting to retrieve the distro specific info.
* [lsb-release](http://linux.die.net/man/1/lsb_release) is usually found by default in Ubuntu. When `/etc/debian_version` is found, we also check for `/etc/lsb-release` to retrieve the information from it.
* `*-release` - We fallback to the release file specific to the distribution (e.g. `/etc/redhat-release`, `/etc/centos-release`) and try to extract information (like the version and codename) from it. This is done by looking up the a release file and parsing it.

## Testing

```shell
git clone git@github.com:nir0s/ld.git
cd ld
pip install tox
tox
```

## Contributions..

Pull requests are always welcome to deal with specific distributions or just for general merriment.
